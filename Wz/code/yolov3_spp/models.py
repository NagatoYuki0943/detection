from build_utils.layers import *
from build_utils.parse_config import *

ONNX_EXPORT = False


def create_modules(modules_defs: list, img_size):
    """
    Constructs module list of layer blocks from module configuration in module_defs
    :param modules_defs: 通过.cfg文件解析得到的每个层结构的列表
    :param img_size:
    :return:
    """

    img_size = [img_size] * 2 if isinstance(img_size, int) else img_size
    #-------------------------------------------------#
    #   删除解析cfg列表中的第一个配置(对应[net]的配置)
    #-------------------------------------------------#
    modules_defs.pop(0)  # cfg training hyperparams (unused)
    #-------------------------------------------------#
    #   记录搭建每个模块时输出的channel,开始为3, rgb
    #-------------------------------------------------#
    output_filters = [3]
    module_list = nn.ModuleList()
    #-------------------------------------------------#
    #   统计哪些特征层的输出会被后续的层使用到(可能是特征融合，也可能是拼接)
    #-------------------------------------------------#
    routs = []  # list of layers which rout to deeper layers
    #-------------------------------------------------#
    #   
    #-------------------------------------------------#
    yolo_index = -1

    # 遍历搭建每个层结构
    for i, mdef in enumerate(modules_defs):
        modules = nn.Sequential()

        #-------------------------------------------------#
        #   卷积
        #-------------------------------------------------#
        if mdef["type"] == "convolutional":
            bn = mdef["batch_normalize"]    # 1 or 0 / 是否使用BN
            filters = mdef["filters"]       # out_channel
            k = mdef["size"]                # kernel size
            stride = mdef["stride"] if "stride" in mdef else (mdef['stride_y'], mdef["stride_x"])   # stride,后面的v3用不到
            # kernel_size 必须为整数
            if isinstance(k, int):
                modules.add_module("Conv2d", nn.Conv2d(in_channels=output_filters[-1],
                                                       out_channels=filters,
                                                       kernel_size=k,
                                                       stride=stride,
                                                       padding=k // 2 if mdef["pad"] else 0,
                                                       bias=not bn))
            else:
                raise TypeError("conv2d filter size must be int type.")

            if bn:
                modules.add_module("BatchNorm2d", nn.BatchNorm2d(filters))
            else:
                #-------------------------------------------------#
                #   如果该卷积操作没有bn层，意味着该层为yolo的predictor,记录索引
                #-------------------------------------------------#
                routs.append(i)  # detection output (goes into yolo layer)

            #-------------------------------------------------#
            #   激活函数
            #-------------------------------------------------#
            if mdef["activation"] == "leaky":
                modules.add_module("activation", nn.LeakyReLU(0.1, inplace=True))
            else:
                pass

        #-------------------------------------------------#
        #   BatchNorm2d
        #-------------------------------------------------#
        elif mdef["type"] == "BatchNorm2d":
            pass


        #-------------------------------------------------#
        #   maxpool spp结构 k= 5 9 13
        #-------------------------------------------------#
        elif mdef["type"] == "maxpool":
            k = mdef["size"]  # kernel size
            stride = mdef["stride"]
            modules = nn.MaxPool2d(kernel_size=k, stride=stride, padding=(k - 1) // 2)

        #-------------------------------------------------#
        #   upsample Upsample(scale_factor=2)
        #-------------------------------------------------#
        elif mdef["type"] == "upsample":
            if ONNX_EXPORT:  # explicitly state size, avoid scale_factor
                g = (yolo_index + 1) * 2 / 32  # gain
                modules = nn.Upsample(size=tuple(int(x * g) for x in img_size))
            else:
                modules = nn.Upsample(scale_factor=mdef["stride"])

        #-------------------------------------------------#
        #   route
        #-------------------------------------------------#
        elif mdef["type"] == "route":  # [-2],  [-1,-3,-5,-6], [-1, 61]
            layers = mdef["layers"]
            #-------------------------------------------------#
            #   记录当前特征层的out_channel
            #   l + 1 if l > 0 else l  l > 0要加一,因为开始有一个3,要跳过它
            #-------------------------------------------------#
            filters = sum([output_filters[l + 1 if l > 0 else l] for l in layers])
            #-------------------------------------------------#
            #   记录使用哪些层的输出
            #   小于0时比如 -1 说明要上一层的输出
            #-------------------------------------------------#
            routs.extend([i + l if l < 0 else l for l in layers])
            modules = FeatureConcat(layers=layers)

        #-------------------------------------------------#
        #   shortcut 残差部分  -3 和 -1 相加
        #-------------------------------------------------#
        elif mdef["type"] == "shortcut":
            # 与前面哪一层拼接, 残差使用了
            layers = mdef["from"]
            # 获取上一层输出 -1 的输出
            filters = output_filters[-1]
            # routs.extend([i + l if l < 0 else l for l in layers])
            routs.append(i + layers[0])
            modules = WeightedFeatureFusion(layers=layers, weight="weights_type" in mdef)

        #-------------------------------------------------#
        #   yolo是对预测结果进行处理生成anchors
        #-------------------------------------------------#
        elif mdef["type"] == "yolo":
            #-------------------------------------------------#
            #   记录是第几个yolo_layer [0, 1, 2]
            #-------------------------------------------------#
            yolo_index += 1
            stride = [32, 16, 8]  # 预测特征层对应原图的缩放比例

            modules = YOLOLayer(anchors=mdef["anchors"][mdef["mask"]],  # anchor list   选择合适的anchor
                                nc=mdef["classes"],                     # number of classes
                                img_size=img_size,                      # onnx使用
                                stride=stride[yolo_index])              # 不同图像大小不同的步长

            #-------------------------------------------------#
            #   初始化偏置
            #-------------------------------------------------#
            # Initialize preceding Conv2d() bias (https://arxiv.org/pdf/1708.02002.pdf section 3.3)
            try:
                j = -1 # yolo上一层
                # bias: shape(255,) 索引0对应Sequential中的Conv2d
                # view: shape(3, 85)
                b = module_list[j][0].bias.view(modules.na, -1)
                b.data[:, 4] += -4.5  # obj
                b.data[:, 5:] += math.log(0.6 / (modules.nc - 0.99))  # cls (sigmoid(p) = 1/nc)
                module_list[j][0].bias = torch.nn.Parameter(b.view(-1), requires_grad=True)
            except Exception as e:
                print('WARNING: smart bias initialization failure.', e)
        else:
            print("Warning: Unrecognized Layer Type: " + mdef["type"])

        #-------------------------------------------------#
        # 放入模型列表
        #-------------------------------------------------#
        module_list.append(modules)
        #-------------------------------------------------#
        #   这一层的out_channel当做下一层的in_channel
        #-------------------------------------------------#
        output_filters.append(filters)

    #-------------------------------------------------#
    #   多少个模块存入多少个False,需要记录输出的设置为True
    #-------------------------------------------------#
    routs_binary = [False] * len(modules_defs)
    for i in routs: # routs 统计哪些特征层的输出会被后续的层使用到(可能是特征融合，也可能是拼接)
        routs_binary[i] = True
    return module_list, routs_binary


class YOLOLayer(nn.Module):
    """
    对YOLO的输出进行处理,将中心宽高调整到原图尺寸上
    """
    def __init__(self, anchors, nc, img_size, stride):
        super(YOLOLayer, self).__init__()
        self.anchors = torch.Tensor(anchors)
        self.stride = stride    # layer stride 特征图上一步对应原图上的步距 [32, 16, 8]
        self.na = len(anchors)  # 3 种 anchors
        self.nc = nc            # 分类数 80
        self.no = nc + 5        # 85: x, y, w, h, obj, cls1, ...
        self.nx, self.ny, self.ng = 0, 0, (0, 0)  # initialize number of x, y gridpoints
        #-------------------------------------------------#
        #   将anchors大小缩放到grid尺度,缩小
        #-------------------------------------------------#
        self.anchor_vec = self.anchors / self.stride
        #-------------------------------------------------#
        #   batch_size, na, grid_h, grid_w, wh,
        #   值为1的维度对应的值不是固定值，后续操作可根据broadcast广播机制自动扩充
        #-------------------------------------------------#
        self.anchor_wh = self.anchor_vec.view(1, self.na, 1, 1, 2)  # 1, 3, 1, 1, 2  batch, 框的个数, 宽, 高, 宽高     batch,宽,高会随着图像变化, 剩余两个不会
        self.grid = None

        if ONNX_EXPORT:
            self.training = False
            self.create_grids((img_size[1] // stride, img_size[0] // stride))  # number x, y grid points

    def create_grids(self, ng=(13, 13), device="cpu"):
        """
        更新grids信息并生成新的grids参数
        :param ng: 特征图大小
        :param device:
        :return:
        """
        self.nx, self.ny = ng
        self.ng = torch.tensor(ng, dtype=torch.float)

        #-------------------------------------------------#
        #   build xy offsets 构建每个cell处的anchor的xy偏移量(在feature map上的)
        #-------------------------------------------------#
        # 训练模式不需要回归到最终预测boxes,预测才需要生成网格
        if not self.training:
            #-------------------------------------------------#
            # xv = yv = 13,26,52
            # 所有点的x,y轴坐标通过meshgrid组合成坐标
            # xv = [[0,1,2,3],
            #       [0,1,2,3],
            #       [0,1,2,3],
            #       [0,1,2,3]]
            # yv = [[0,0,0,0],
            #       [1,1,1,1],
            #       [2,2,2,2],
            #       [3,3,3,3]]
            #-------------------------------------------------#
            yv, xv = torch.meshgrid([torch.arange(self.ny, device=device),
                                     torch.arange(self.nx, device=device)])
            #-------------------------------------------------#
            # 通过stack拼接
            # grid = [[[0,0],[1,0],[2,0].[3,0],
            #          [0,1],[1,1],[2,1].[3,1],
            #          [0,2],[1,2],[2,2].[3,2],
            #          [0,3],[1,3],[2,3].[3,3],]]
            # [grid_h, grid_w, wh] -> [batch_size, anchor数量, grid_h, grid_w, wh]
            #-------------------------------------------------#
            self.grid = torch.stack((xv, yv), 2).view((1, 1, self.ny, self.nx, 2)).float()

        if self.anchor_vec.device != device:
            self.anchor_vec = self.anchor_vec.to(device)
            self.anchor_wh = self.anchor_wh.to(device)

    def forward(self, p):
        """
        p: 预测参数   [b, _, h, w]
        """
        if ONNX_EXPORT:
            bs = 1  # batch size
        else:
            #-------------------------------------------------#
            #   batch_size, predict_param(255), grid(13), grid(13)
            #-------------------------------------------------#
            bs, _, ny, nx = p.shape

            if (self.nx, self.ny) != (nx, ny) or self.grid is None:  # fix no grid bug
                self.create_grids((nx, ny), p.device)

        #-------------------------------------------------#
        #   view:     [batch_size, 255, 13, 13] -> [batch_size, 3, 85, 13, 13]
        #   permute:  [batch_size, 3, 85, 13, 13)] -> [batch_size, 3, 13, 13, 85]
        #   [bs, anchor, h, w, xywh + obj + classes]
        #-------------------------------------------------#
        p = p.view(bs, self.na, self.no, self.ny, self.nx).permute(0, 1, 3, 4, 2).contiguous()  # prediction

        #-------------------------------------------------#
        #   训练模式直接返回数据
        #-------------------------------------------------#
        if self.training:
            return p
        elif ONNX_EXPORT:
            # Avoid broadcasting for ANE operations
            m = self.na * self.nx * self.ny  # 3*
            ng = 1. / self.ng.repeat(m, 1)
            grid = self.grid.repeat(1, self.na, 1, 1, 1).view(m, 2)
            anchor_wh = self.anchor_wh.repeat(1, 1, self.nx, self.ny, 1).view(m, 2) * ng

            p = p.view(m, self.no)
            # xy = torch.sigmoid(p[:, 0:2]) + grid  # x, y
            # wh = torch.exp(p[:, 2:4]) * anchor_wh  # width, height
            # p_cls = torch.sigmoid(p[:, 4:5]) if self.nc == 1 else \
            #     torch.sigmoid(p[:, 5:self.no]) * torch.sigmoid(p[:, 4:5])  # conf
            p[:, :2] = (torch.sigmoid(p[:, 0:2]) + grid) * ng  # x, y
            p[:, 2:4] = torch.exp(p[:, 2:4]) * anchor_wh  # width, height
            p[:, 4:] = torch.sigmoid(p[:, 4:])
            p[:, 5:] = p[:, 5:self.no] * p[:, 4:5]
            return p
        else:
            #-------------------------------------------------#
            # inference
            # [bs, anchor, h, w, xywh + obj + classes]
            #   中心调整: 先验框坐标 + sigmoid(预测结果) = 最终坐标
            #   宽高调整: 先验框宽高 * e^预测结果        = 最终宽高
            #-------------------------------------------------#
            io = p.clone()  # inference output 复制一份作为输出
            io[..., :2]  = torch.sigmoid(io[..., :2]) + self.grid    # xy 计算在feature map上的xy坐标   ... 取前4个维度
            io[..., 2:4] = torch.exp(io[..., 2:4]) * self.anchor_wh  # wh yolo method 计算在feature map上的wh
            io[..., :4]  *= self.stride                              # 换算映射回原图尺度
            torch.sigmoid_(io[..., 4:])                              # 分类全都经过sigmoid

            # 调整到原图尺寸以及sigmoid置信度和分类的值 view [1, 3, 13, 13, 85] as [1, 507, 85]
            # 将预测进行转置处理                       [bs, anchor, h, w, xywh + obj + classes]
            return io.view(bs, -1, self.no), p


class Darknet(nn.Module):
    """
    YOLOv3 spp object detection model
    """
    def __init__(self, cfg, img_size=(416, 416), verbose=False):
        super(Darknet, self).__init__()
        #-------------------------------------------------#
        #   训练时分辨率是动态的
        #   这里传入的img_size只在导出ONNX模型时起作用
        #-------------------------------------------------#
        self.input_size = [img_size] * 2 if isinstance(img_size, int) else img_size
        #-------------------------------------------------#
        #   解析网络对应的.cfg文件,返回列表
        #-------------------------------------------------#
        self.module_defs = parse_model_cfg(cfg)
        #-------------------------------------------------#
        #   根据解析的网络结构一层一层去搭建
        #   返回模块列表和 True/False列表,这个列表代表是否需要保存这一层的输出
        #-------------------------------------------------#
        self.module_list, self.routs = create_modules(self.module_defs, img_size)
        #-------------------------------------------------#
        #   获取3个YOLOLayer层的索引 [89, 101, 113]
        #-------------------------------------------------#
        self.yolo_layers = get_yolo_layers(self)

        #-------------------------------------------------#
        #   打印下模型的信息，如果verbose为True则打印详细信息
        #-------------------------------------------------#
        self.info(verbose) if not ONNX_EXPORT else None  # print model description

    def forward(self, x, verbose=False):
        return self.forward_once(x, verbose=verbose)

    def forward_once(self, x, verbose=False):
        """
        x: 图像数据
        """
        #-------------------------------------------------#
        #   yolo_out收集每个yolo_layer层的输出
        #   out收集每个模块的输出
        #-------------------------------------------------#
        yolo_out, out = [], []
        if verbose:
            print('0', x.shape)
            str = ""

        #-------------------------------------------------#
        #   遍历搭建的所有模块
        #-------------------------------------------------#
        for i, module in enumerate(self.module_list):
            name = module.__class__.__name__
            #-------------------------------------------------#
            # sum, concat
            #-------------------------------------------------#
            if name in ["WeightedFeatureFusion", "FeatureConcat"]:
                if verbose:
                    l = [i - 1] + module.layers  # layers
                    sh = [list(x.shape)] + [list(out[i].shape) for i in module.layers]  # shapes
                    str = ' >> ' + ' + '.join(['layer %g %s' % x for x in zip(l, sh)])
                # 将 x 和每一层输出的放入
                x = module(x, out)  # WeightedFeatureFusion(), FeatureConcat()
            elif name == "YOLOLayer":
                #-------------------------------------------------#
                #   将yolo放入 yolo_out 中
                #-------------------------------------------------#
                yolo_out.append(module(x))
            else:
                #-------------------------------------------------#
                #   其余直接返回就可
                #   run module directly, i.e. mtype = 'convolutional', 'upsample', 'maxpool', 'batchnorm2d' etc.
                #-------------------------------------------------#
                x = module(x)

            #-------------------------------------------------#
            #   routs: True/False列表,这个列表代表是否需要保存这一层的输出
            #-------------------------------------------------#
            out.append(x if self.routs[i] else [])
            if verbose:
                print('%g/%g %s -' % (i, len(self.module_list), name), list(x.shape), str)
                str = ''

        # 训练直接返回数据
        if self.training:
            return yolo_out
        elif ONNX_EXPORT:  # export
            # x = [torch.cat(x, 0) for x in zip(*yolo_out)]
            # return x[0], torch.cat(x[1:3], 1)  # scores, boxes: 3780x80, 3780x4
            p = torch.cat(yolo_out, dim=0)

            # # 根据objectness虑除低概率目标
            # mask = torch.nonzero(torch.gt(p[:, 4], 0.1), as_tuple=False).squeeze(1)
            # # onnx不支持超过一维的索引（pytorch太灵活了）
            # # p = p[mask]
            # p = torch.index_select(p, dim=0, index=mask)
            #
            # # 虑除小面积目标，w > 2 and h > 2 pixel
            # # ONNX暂不支持bitwise_and和all操作
            # mask_s = torch.gt(p[:, 2], 2./self.input_size[0]) & torch.gt(p[:, 3], 2./self.input_size[1])
            # mask_s = torch.nonzero(mask_s, as_tuple=False).squeeze(1)
            # p = torch.index_select(p, dim=0, index=mask_s)  # width-height 虑除小目标
            #
            # if mask_s.numel() == 0:
            #     return torch.empty([0, 85])

            return p
        else:
            #-------------------------------------------------#
            #   x指的是调整到原图尺寸以及sigmoid置信度和分类的值  [1, 507, 85]
            #   p只将预测进行转置处理                           [bs, anchor, h, w, xywh + obj + classes]
            #-------------------------------------------------#
            x, p = zip(*yolo_out)   # inference output, training output
            x = torch.cat(x, 1)     # 在通道上拼接,将三个输出拼接到一起

            return x, p

    def info(self, verbose=False):
        """
        打印模型的信息
        :param verbose:
        :return:
        """
        torch_utils.model_info(self, verbose)


def get_yolo_layers(self):
    """
    获取网络中三个"YOLOLayer"模块对应的索引
    :param self:
    :return:
    """
    return [i for i, m in enumerate(self.module_list) if m.__class__.__name__ == 'YOLOLayer']  # [89, 101, 113]
