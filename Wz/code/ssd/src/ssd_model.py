import torch
from torch import nn, Tensor
from torch.jit.annotations import List

from .res50_backbone import resnet50
from .utils import dboxes300_coco, Encoder, PostProcess

#----------------------------------------#
#   调整resnet50的backbone
#----------------------------------------#
class Backbone(nn.Module):
    def __init__(self, pretrain_path=None):
        super(Backbone, self).__init__()
        net = resnet50()
        self.out_channels = [1024, 512, 512, 256, 256, 256]

        if pretrain_path is not None:
            net.load_state_dict(torch.load(pretrain_path))

        #----------------------------------------#
        #   找到所有卷积层
        #   [:7] conv1 bn1 relu layer1 layer2 layer3 layer4
        #----------------------------------------#
        self.feature_extractor = nn.Sequential(*list(net.children())[:7])

        #----------------------------------------#
        #   修改conv4_block1的步距，从2->1
        #----------------------------------------#
        conv4_block1 = self.feature_extractor[-1][0]
        conv4_block1.conv1.stride = (1, 1)    # ResNet50本来就是1,不用管,不过ResNet18和34的第一个卷积步长为2
        conv4_block1.conv2.stride = (1, 1)
        conv4_block1.downsample[0].stride = (1, 1)

    def forward(self, x):
        x = self.feature_extractor(x)
        return x

#----------------------------------------#
#   
#----------------------------------------#
class SSD300(nn.Module):
    def __init__(self, backbone=None, num_classes=21):
        super(SSD300, self).__init__()
        #----------------------------------------#
        #   必须有backbone且必须有out_channels属性
        #----------------------------------------#
        if backbone is None:
            raise Exception("backbone is None")
        if not hasattr(backbone, "out_channels"):
            raise Exception("the backbone not has attribute: out_channel")

        #----------------------------------------#
        #   特征提取部分
        #----------------------------------------#
        self.feature_extractor = backbone

        self.num_classes = num_classes

        #----------------------------------------#
        #   构建额外的添加层 5层
        #   out_channels = [1024, 512, 512, 256, 256, 256] for resnet50
        #----------------------------------------#
        self._build_additional_features(self.feature_extractor.out_channels)


        #----------------------------------------#
        #   构建预测部分,位置的分类分开预测
        #   6个特征层的框的数量
        #----------------------------------------#
        self.num_defaults       = [4, 6, 6, 6, 4, 4]
        location_extractors     = []
        confidence_extractors   = []
        #----------------------------------------#
        #    out_channels = [1024, 512, 512, 256, 256, 256] for resnet50
        #----------------------------------------#
        for nd, oc in zip(self.num_defaults, self.feature_extractor.out_channels):
            # nd is number_default_boxes, oc is output_channel
            location_extractors.append(nn.Conv2d(oc, nd * 4, kernel_size=3, padding=1))                     # num_anchor * 4
            confidence_extractors.append(nn.Conv2d(oc, nd * self.num_classes, kernel_size=3, padding=1))    # num_anchor * num_classes
        self.loc    = nn.ModuleList(location_extractors)
        self.conf   = nn.ModuleList(confidence_extractors)

        self._init_weights()

        #----------------------------------------#
        #    默认框
        #----------------------------------------#
        default_box         = dboxes300_coco()          # [8732, 4] 4: x1y1x2y2
        self.compute_loss   = Loss(default_box)
        self.encoder        = Encoder(default_box)
        self.postprocess    = PostProcess(default_box)

    #----------------------------------------#
    #   构建额外的添加层 5层
    #----------------------------------------#
    def _build_additional_features(self, input_size):
        """
        为backbone(resnet50)添加额外的一系列卷积层，得到相应的一系列特征提取器
        :param input_size: [1024, 512, 512, 256, 256, 256]
        :return:
        """
        additional_blocks = []
        # input_size = [1024, 512, 512, 256, 256, 256] for resnet50

        #----------------------------------------#
        #   生成的5个卷积块的中间维度
        #----------------------------------------#
        middle_channels = [256, 256, 128, 128, 128]
        #----------------------------------------#
        #   进出维度是相同的
        #----------------------------------------#
        for i, (input_ch, output_ch, middle_ch) in enumerate(zip(input_size[:-1], input_size[1:], middle_channels)):
            #----------------------------------------#
            #   前三个卷积块的s=2,p=1
            #----------------------------------------#
            padding, stride = (1, 2) if i < 3 else (0, 1)
            #----------------------------------------------------------#
            #   1x1Conv -> BN -> ReLU -> 3x3Conv -> BN -> ReLU
            #----------------------------------------------------------#
            layer = nn.Sequential(
                nn.Conv2d(input_ch, middle_ch, kernel_size=1, bias=False),
                nn.BatchNorm2d(middle_ch),
                nn.ReLU(inplace=True),
                nn.Conv2d(middle_ch, output_ch, kernel_size=3, padding=padding, stride=stride, bias=False),
                nn.BatchNorm2d(output_ch),
                nn.ReLU(inplace=True),
            )
            additional_blocks.append(layer)
        self.additional_blocks = nn.ModuleList(additional_blocks)

    def _init_weights(self):
        layers = [*self.additional_blocks, *self.loc, *self.conf]
        for layer in layers:
            for param in layer.parameters():
                if param.dim() > 1:
                    nn.init.xavier_uniform_(param)

    #----------------------------------------#
    #   Shape the classifier to the view of bboxes
    #   得到预测的位置参数和分类参数
    #   Feature Map 38x38x4, 19x19x6, 10x10x6, 5x5x6, 3x3x4, 1x1x4
    #----------------------------------------#
    def bbox_view(self, features, loc_extractor, conf_extractor):
        """
        :param
            features:       6个特征层
            loc_extractor:  位置预测器
            conf_extractor: 分类预测器
        :return:

        """
        locs = []
        confs = []
        for f, l, c in zip(features, loc_extractor, conf_extractor):
            #----------------------------------------#
            #   n = 9 9个框
            #   [batch, n*4, feat_size, feat_size] -> [batch, 4, -1]                [batch, 4, 所有框]
            #----------------------------------------#
            locs.append(l(f).view(f.size(0), 4, -1))
            #----------------------------------------#
            #   [batch, n*classes, feat_size, feat_size] -> [batch, classes, -1]    [batch, classes, 所有框]
            #----------------------------------------#
            confs.append(c(f).view(f.size(0), self.num_classes, -1))

        #----------------------------------------#
        # loc和conf分别在最后维度拼接
        #----------------------------------------#
        locs, confs = torch.cat(locs, 2).contiguous(), torch.cat(confs, 2).contiguous()
        return locs, confs

    def forward(self, image, targets=None):
        #----------------------------------------#
        #    提取特征
        #----------------------------------------#
        x = self.feature_extractor(image)

        #----------------------------------------#
        #   存储预测特征层的列表
        #   Feature Map 38x38x1024, 19x19x512, 10x10x512, 5x5x256, 3x3x256, 1x1x256
        #----------------------------------------#
        detection_features = torch.jit.annotate(List[Tensor], [])  # [x]
        #----------------------------------------#
        #    先将特征提取的结果放入列表,再循环额外层,将结果也放入列表
        #----------------------------------------#
        detection_features.append(x)
        for layer in self.additional_blocks:
            x = layer(x)
            detection_features.append(x)

        #----------------------------------------#
        #   得到预测的位置参数和分类参数
        #   Feature Map 38x38x4, 19x19x6, 10x10x6, 5x5x6, 3x3x4, 1x1x4
        #----------------------------------------#
        locs, confs = self.bbox_view(detection_features, self.loc, self.conf)

        # For SSD 300, shall return nbatch x 8732 x {nlabels, nlocs} results
        # 38x38x4 + 19x19x6 + 10x10x6 + 5x5x6 + 3x3x4 + 1x1x4 = 8732

        #----------------------------------------#
        #   训练模式求损失
        #----------------------------------------#
        if self.training:
            if targets is None:
                raise ValueError("In training mode, targets should be passed")
            # bboxes_out (Tensor 8732 x 4), labels_out (Tensor 8732)
            bboxes_out = targets['boxes']
            bboxes_out = bboxes_out.transpose(1, 2).contiguous()
            # print(bboxes_out.is_contiguous())
            labels_out = targets['labels']
            # print(labels_out.is_contiguous())

            # ploc, plabel, gloc, glabel
            loss = self.compute_loss(locs, confs, bboxes_out, labels_out)
            return {"total_losses": loss}

        #----------------------------------------#
        #   将预测回归参数叠加到default box上得到最终预测box，并执行非极大值抑制虑除重叠框
        #----------------------------------------#
        # results = self.encoder.decode_batch(locs, confs)
        results = self.postprocess(locs, confs)
        return results


#----------------------------------------#
#   计算loss
#----------------------------------------#
class Loss(nn.Module):
    """
        Implements the loss as the sum of the followings:
        1. Confidence Loss: All labels, with hard negative mining
        2. Localization Loss: Only on positive labels
        Suppose input dboxes has the shape 8732x4
    """
    def __init__(self, dboxes):
        """
        dboxes: default boxes
        """
        super(Loss, self).__init__()
        #----------------------------------------#
        #   超参数,位置loss的缩放因子
        #   Two factor are from following links
        #   http://jany.st/post/2017-11-05-single-shot-detector-ssd-from-scratch-in-tensorflow.html
        #----------------------------------------#
        self.scale_xy = 1.0 / dboxes.scale_xy  # 10
        self.scale_wh = 1.0 / dboxes.scale_wh  # 5

        #----------------------------------------#
        #   定位损失,SmoothL1Loss
        #----------------------------------------#
        self.location_loss = nn.SmoothL1Loss(reduction='none')
        #----------------------------------------#
        #   将xywh转换为torch参数
        #----------------------------------------#
        # [num_anchors, 4] -> [4, num_anchors] -> [1, 4, num_anchors]
        self.dboxes = nn.Parameter(dboxes(order="xywh").transpose(0, 1).unsqueeze(dim=0),
                                   requires_grad=False)

        #----------------------------------------#
        #   分类是交叉熵损失
        #----------------------------------------#
        self.confidence_loss = nn.CrossEntropyLoss(reduction='none')


    #----------------------------------------#
    #   计算gt真实框的location回归参数
    #----------------------------------------#
    def _location_vec(self, loc):
        # type: (Tensor) -> Tensor
        """
        Generate Location Vectors
        计算ground truth相对anchors的回归参数
        :param loc: anchor匹配到的对应GTBOX  Nx4x8732
        :return: [Nx4x8732]
        """
        #----------------------------------------#
        #   中心参数 = (真实框坐标 - 先验框坐标) / 先验框宽高
        #   scale_xy: 缩放因子 = 10     后处理时是0.1
        #----------------------------------------#
        gxy = self.scale_xy * (loc[:, :2, :] - self.dboxes[:, :2, :]) / self.dboxes[:, 2:, :]  # Nx2x8732
        #----------------------------------------#
        #   宽高参数 = ln(真实框宽高 / 先验框宽高)
        #   scale_wh: 缩放因子 = 5      后处理时是0.2
        #----------------------------------------#
        gwh = self.scale_wh * (loc[:, 2:, :] / self.dboxes[:, 2:, :]).log()  # Nx2x8732
        #----------------------------------------#
        #   在中间维度拼接 [Nx4x8732]
        #----------------------------------------#
        return torch.cat((gxy, gwh), dim=1).contiguous()


    def forward(self, ploc, plabel, gloc, glabel):
        # type: (Tensor, Tensor, Tensor, Tensor) -> Tensor
        """
            ploc, plabel: Nx4x8732, Nxlabel_numx8732
                predicted location and labels       预测的位置和类别

            gloc, glabel: Nx4x8732, Nx8732
                ground truth location and labels    真实的位置和类别
        """

        #----------------------------------------#
        #   获取正样本的mask  Tensor: [N, 8732]
        #   匹配到正样本才有值,否则为0 [[True, False...]]
        #----------------------------------------#
        mask = torch.gt(glabel, 0)  # (gt: >)
        # mask1 = torch.nonzero(glabel)
        #----------------------------------------#
        #   计算一个batch中的每张图片的正样本个数 Tensor: [N]
        #   N中的每个数代表每张图片的正样本数量 [2, 3, 4, 5...]
        #----------------------------------------#
        pos_num = mask.sum(dim=1)

        #----------------------------------------#
        #   计算gt真实框的location回归参数Tensor: [N, 4, 8732] 注意是 [4, 8732] 顺序是:4个参数,box个数
        #   return: [N, 4, 8732]
        #----------------------------------------#
        vec_gd = self._location_vec(gloc)

        #----------------------------------------#
        #   sum on four coordinates, and mask
        #   计算定位损失(只有正样本)
        #   SmoothL1Loss损失,在xywh维度求和,包含正负样本损失
        #----------------------------------------#
        loc_loss = self.location_loss(ploc, vec_gd).sum(dim=1)  # Tensor: [N, 8732]
        #----------------------------------------#
        #   选择正样本损失
        #----------------------------------------#
        loc_loss = (mask.float() * loc_loss).sum(dim=1)  # Tenosr: [N]

        #----------------------------------------#
        #   分类损失:交叉熵损失
        #   hard negative mining Tenosr: [N, 8732]  全部框的分类损失
        #----------------------------------------#
        con = self.confidence_loss(plabel, glabel)  # glabel为真实标签或者0,0代表背景

        #----------------------------------------#
        #   positive mask will never selected
        #   正样本已经得到了,mask就是正样本,只获取负样本
        #   对剩余样本计算confidence loss,根据计算出的loss,选择排在前面的框,选取个数是正样本的3倍
        #----------------------------------------#
        con_neg = con.clone()
        con_neg[mask] = 0.0     # 将正样本的值设为0
        #----------------------------------------#
        #   按照confidence_loss降序排列 con_idx(Tensor: [N, 8732])
        #   第一次降序排序内容,返回所有idx
        #   第二次对获取的idx降序排序,返回idx
        #----------------------------------------#
        _, con_idx = con_neg.sort(dim=1, descending=True)
        _, con_rank = con_idx.sort(dim=1)  # 这个步骤比较巧妙

        #----------------------------------------#
        #   number of negative three times positive
        #   用于损失计算的负样本数是正样本的3倍（在原论文Hard negative mining部分）， 就是 clamp(3 * pos_num)
        #   但不能超过总样本数8732
        #----------------------------------------#
        neg_num = torch.clamp(3 * pos_num, max=mask.size(1)).unsqueeze(-1)
        #----------------------------------------#
        #   比较得到True False， 需要的为True，含义是损失最大的值，用True，False对第一行的*confidence_loss*进行取值
        #----------------------------------------#
        neg_mask = torch.lt(con_rank, neg_num)  # (lt: <) Tensor [N, 8732]

        #----------------------------------------#
        #   confidence最终loss使用选取的正样本loss+选取的负样本loss
        #   正负样本mask相加，mask选择的为True,否则为False
        #----------------------------------------#
        con_loss = (con * (mask.float() + neg_mask.float())).sum(dim=1)  # Tensor [N]

        #----------------------------------------#
        #   定位损失和分类损失相加
        #----------------------------------------#
        total_loss = loc_loss + con_loss
        #----------------------------------------#
        #   avoid no object detected
        #   避免出现图像中没有GTBOX的情况
        #   eg. [15, 3, 5, 0] -> [1.0, 1.0, 1.0, 0.0]
        #----------------------------------------#
        num_mask = torch.gt(pos_num, 0).float()                 # 统计一个batch中的每张图像中是否存在正样本

        #----------------------------------------#
        #   只计算存在正样本的图像损失,公式中除以N
        #----------------------------------------#
        pos_num = pos_num.float().clamp(min=1e-6)               # 防止出现分母为零的情况
        ret = (total_loss * num_mask / pos_num).mean(dim=0)
        return ret

