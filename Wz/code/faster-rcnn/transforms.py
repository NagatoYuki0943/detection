#---------------------------------------------------#
#   数据预处理
#---------------------------------------------------#


import random
from torchvision.transforms import functional as F


class Compose(object):
    """组合多个transform函数"""
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, image, target):
        for t in self.transforms:
            image, target = t(image, target)
        return image, target


class ToTensor(object):
    """将PIL图像转为Tensor"""
    def __call__(self, image, target):
        image = F.to_tensor(image)
        return image, target


class RandomHorizontalFlip(object):
    """随机水平翻转图像以及bboxes"""
    def __init__(self, prob=0.5):
        self.prob = prob

    def __call__(self, image, target):
        #   小于0.5就翻转
        if random.random() < self.prob:
            height, width = image.shape[-2:]    # 中心,宽高
            #---------------------------------------------------#
            #   水平翻转图片
            #---------------------------------------------------#
            image = image.flip(-1)
            bbox = target["boxes"]
            #---------------------------------------------------#
            #   翻转对应bbox坐标信息
            #   bbox: xmin, ymin, xmax, ymax
            #---------------------------------------------------#
            bbox[:, [0, 2]] = width - bbox[:, [2, 0]]
            target["boxes"] = bbox
        return image, target
