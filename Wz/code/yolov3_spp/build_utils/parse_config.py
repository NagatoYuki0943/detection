import os
import numpy as np


def parse_model_cfg(path: str): # 路径
    #-----------------------------------------------#
    # 检查文件是否存在,必须是cfg文件
    #-----------------------------------------------#
    if not path.endswith(".cfg") or not os.path.exists(path):
        raise FileNotFoundError("the cfg file not exist...")

    # 读取文件信息
    with open(path, "r") as f:
        lines = f.read().split("\n")

    #-----------------------------------------------#
    # 去除空行和注释行,放入列表  if x 代表当前行不为空
    #-----------------------------------------------#
    lines = [x for x in lines if x and not x.startswith("#")]
    #-----------------------------------------------#
    # 去除每行开头和结尾的空格符
    #-----------------------------------------------#
    lines = [x.strip() for x in lines]

    #-----------------------------------------------#
    #   
    #-----------------------------------------------#
    mdefs = []  # module definitions
    for line in lines:
        #-----------------------------------------------#
        #   开始为 "[" 说明开启一个新block
        #   添加一个新字典,添加键值
        #-----------------------------------------------#
        if line.startswith("["):  # this marks the start of a new block
            mdefs.append({})
            mdefs[-1]["type"] = line[1:-1].strip()  # 记录module类型    [1:-1] 不要两边的 []
            #-----------------------------------------------#
            # 如果是卷积模块，设置默认不使用BN(普通卷积层后面会重写成1，最后的预测层conv保持为0)
            #-----------------------------------------------#
            if mdefs[-1]["type"] == "convolutional":
                mdefs[-1]["batch_normalize"] = 0
        else:
            #-----------------------------------------------#
            #   开始不为 "[" 说明是block参数
            #   通过等号分隔得到 key value
            #-----------------------------------------------#
            key, val = line.split("=")
            key = key.strip()
            val = val.strip()

            #-----------------------------------------------#
            #   yolo层的anchor
            #-----------------------------------------------#
            if key == "anchors":
                # anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
                val = val.replace(" ", "")  # 将空格去除
                # 通过逗号分隔获取数据,转换为浮点数,改变形状到二维数据,放入列表
                mdefs[-1][key] = np.array([float(x) for x in val.split(",")]).reshape((-1, 2))  # np anchors
            elif (key in ["from", "layers", "mask"]) or (key == "size" and "," in val):
                #-----------------------------------------------#
                #   逗号分隔,主要是shortcut 和 root 模块,转换为int,放入列表
                #-----------------------------------------------#
                mdefs[-1][key] = [int(x) for x in val.split(",")]
            else:
                #-----------------------------------------------#
                #   卷积层
                #-----------------------------------------------#
                # TODO: .isnumeric() actually fails to get the float case
                if val.isnumeric():  # return int or float
                    #-----------------------------------------------#
                    #   如果是数值的情况
                    #   判断是int还是float
                    #   假设是int 转化为 int 还是 float 相等,减去为0,就说明是int
                    #-----------------------------------------------#
                    mdefs[-1][key] = int(val) if (int(val) - float(val)) == 0 else float(val)
                else:
                    # 是字符的情况
                    mdefs[-1][key] = val  # return string

    #-----------------------------------------------#
    # 类型名支持的列表
    #-----------------------------------------------#
    supported = ['type', 'batch_normalize', 'filters', 'size', 'stride', 'pad', 'activation', 'layers', 'groups',
                 'from', 'mask', 'anchors', 'classes', 'num', 'jitter', 'ignore_thresh', 'truth_thresh', 'random',
                 'stride_x', 'stride_y', 'weights_type', 'weights_normalization', 'scale_x_y', 'beta_nms', 'nms_kind',
                 'iou_loss', 'iou_normalizer', 'cls_normalizer', 'iou_thresh', 'probability']

    #-----------------------------------------------#
    # 遍历检查每个模型的配置
    #-----------------------------------------------#
    for x in mdefs[1:]:  # 0对应net配置
        #-----------------------------------------------#
        # 遍历每个配置字典中的key值
        #-----------------------------------------------#
        for k in x:
            if k not in supported:
                raise ValueError("Unsupported fields:{} in cfg".format(k))

    return mdefs


def parse_data_cfg(path):
    # Parses the data configuration file
    if not os.path.exists(path) and os.path.exists('data' + os.sep + path):  # add data/ prefix if omitted
        path = 'data' + os.sep + path

    with open(path, 'r') as f:
        lines = f.readlines()

    options = dict()
    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        key, val = line.split('=')
        options[key.strip()] = val.strip()

    return options



if __name__ == "__main__":
    cfg = parse_model_cfg('../cfg/yolov3-spp.cfg')
    print(cfg)
    """
    [{'type': 'net', 'batch': 64, 'subdivisions': 16, 'width': 608, 'height': 608, 'channels': 3, 'momentum': '0.9', 'decay': '0.0005', 'angle': 0, 'saturation': '1.5', 'exposure': '1.5', 'hue': '.1', 'learning_rate': '0.001', 'burn_in': 1000, 'max_batches': 500200, 'policy': 'steps', 'steps': '400000,450000', 'scales': '.1,.1'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 32, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 64, 'size': 3, 'stride': 2, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 32, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 64, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 3, 'stride': 2, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 64, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 64, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 2, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 2, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 1024, 'size': 3, 'stride': 2, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 1024, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 1024, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 1024, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 1024, 'size': 3, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'shortcut', 'from': [-3], 'activation': 'linear'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 1024, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'maxpool', 'stride': 1, 'size': 5}, {'type': 'route', 'layers': [-2]}, {'type': 'maxpool', 'stride': 1, 'size': 9}, {'type': 'route', 'layers': [-4]}, {'type': 'maxpool', 'stride': 1, 'size': 13}, {'type': 'route', 'layers': [-1, -3, -5, -6]}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 1024, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 512, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 1024, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 0, 'size': 1, 'stride': 1, 'pad': 1, 'filters': 255, 'activation': 'linear'}, {'type': 'yolo', 'mask': [6, 7, 8], 'anchors': array([[ 10.,  13.],
        [ 16.,  30.],
        [ 33.,  23.],
        [ 30.,  61.],
        [ 62.,  45.],
        [ 59., 119.],
        [116.,  90.],
        [156., 198.],
        [373., 326.]]), 'classes': 80, 'num': 9, 'jitter': '.3', 'ignore_thresh': '.7', 'truth_thresh': 1, 'random': 1}, {'type': 'route', 'layers': [-4]}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'upsample', 'stride': 2}, {'type': 'route', 'layers': [-1, 61]}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 512, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 512, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 256, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 512, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 0, 'size': 1, 'stride': 1, 'pad': 1, 'filters': 255, 'activation': 'linear'}, {'type': 'yolo', 'mask': [3, 4, 5], 'anchors': array([[ 10.,  13.],
        [ 16.,  30.],
        [ 33.,  23.],
        [ 30.,  61.],
        [ 62.,  45.],
        [ 59., 119.],
        [116.,  90.],
        [156., 198.],
        [373., 326.]]), 'classes': 80, 'num': 9, 'jitter': '.3', 'ignore_thresh': '.7', 'truth_thresh': 1, 'random': 1}, {'type': 'route', 'layers': [-4]}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'upsample', 'stride': 2}, {'type': 'route', 'layers': [-1, 36]}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 256, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 256, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'filters': 128, 'size': 1, 'stride': 1, 'pad': 1, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 1, 'size': 3, 'stride': 1, 'pad': 1, 'filters': 256, 'activation': 'leaky'}, {'type': 'convolutional', 'batch_normalize': 0, 'size': 1, 'stride': 1, 'pad': 1, 'filters': 255, 'activation': 'linear'}, {'type': 'yolo', 'mask': [0, 1, 2], 'anchors': array([[ 10.,  13.],
        [ 16.,  30.],
        [ 33.,  23.],
        [ 30.,  61.],
        [ 62.,  45.],
        [ 59., 119.],
        [116.,  90.],
        [156., 198.],
        [373., 326.]]), 'classes': 80, 'num': 9, 'jitter': '.3', 'ignore_thresh': '.7', 'truth_thresh': 1, 'random': 1}]
    """