import math
import os
import random
import shutil
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image, ExifTags
from torch.utils.data import Dataset
from tqdm import tqdm

from build_utils.utils import xyxy2xywh, xywh2xyxy

help_url = 'https://github.com/ultralytics/yolov3/wiki/Train-Custom-Data'
img_formats = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.dng']


# get orientation in exif tag
# 找到图像exif信息中对应旋转信息的key值
for orientation in ExifTags.TAGS.keys():
    if ExifTags.TAGS[orientation] == "Orientation":
        break


def exif_size(img):
    """
    获取图像的原始img size
    通过exif的orientation信息判断图像是否有旋转，如果有旋转则返回旋转前的size
    :param img: PIL图片
    :return: 原始图像的size
    """
    # Returns exif-corrected PIL size
    s = img.size  # (width, height)
    try:
        rotation = dict(img._getexif().items())[orientation]
        if rotation == 6:  # rotation 270  顺时针翻转90度
            s = (s[1], s[0])    # 宽高对调
        elif rotation == 8:  # ratation 90  逆时针翻转90度
            s = (s[1], s[0])    # 宽高对调
    except:
        # 如果图像的exif信息中没有旋转信息，则跳过
        pass

    return s


class LoadImagesAndLabels(Dataset):  # for training/testing
    def __init__(self,
                 path,   # 指向data/my_train_data.txt路径或data/my_val_data.txt路径
                 #------------------------------------------------#
                 # 这里设置的是预处理后输出的图片尺寸
                 # 当为训练集时，设置的是训练过程中(开启多尺度)的最大尺寸
                 # 当为验证集时，设置的是最终使用的网络大小
                 #------------------------------------------------#
                 img_size=416,
                 batch_size=16,
                 augment=False,         # 训练集设置为True(augment_hsv)，验证集设置为False 对比度,亮度等调整
                 hyp=None,              # 超参数字典，其中包含图像增强会使用到的超参数
                 rect=False,            # 是否使用rectangular training 训练不开启,验证开启
                 cache_images=False,    # 是否缓存图片到内存中
                 single_cls=False, pad=0.0, rank=-1):   # rank 单GPU = 1  多GPU为 0 1 2...

        try:
            path = str(Path(path))
            # 是否是文件
            # parent = str(Path(path).parent) + os.sep
            if os.path.isfile(path):  # file
                # 读取对应my_train/val_data.txt文件，读取每一行的图片路劲信息
                with open(path, "r") as f:
                    f = f.read().splitlines()   # 按行分隔
            else:
                raise Exception("%s does not exist" % path)

            #------------------------------------------------#
            #   检查每张图片后缀格式是否在支持的列表中，保存支持的图像路径
            #   img_formats = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.dng']
            #------------------------------------------------#
            self.img_files = [x for x in f if os.path.splitext(x)[-1].lower() in img_formats]
            self.img_files.sort()  # 防止不同系统排序不同，导致shape文件出现差异
        except Exception as e:
            raise FileNotFoundError("Error loading data from {}. {}".format(path, e))

        #------------------------------------------------#
        #   如果图片列表中没有图片，则报错
        #------------------------------------------------#
        n = len(self.img_files)
        assert n > 0, "No images found in %s. See %s" % (path, help_url)

        #------------------------------------------------#
        #   batch index
        #   将数据划分到一个个batch中
        #   图片id假设为        0 1 2 3 4 5 6 7 8 9   batch 假设为 4
        #   图片id除以batch得到 0 0 0 0 1 1 1 1 2 2
        #------------------------------------------------#
        bi = np.floor(np.arange(n) / batch_size).astype(np.int)
        # 记录数据集划分后的总batch数
        nb = bi[-1] + 1  # number of batches

        self.n          = n         # number of images 图像总数目
        self.batch      = bi        # batch index of image 记录哪些图片属于哪个batch
        self.img_size   = img_size  # 这里设置的是预处理后输出的图片尺寸
        self.augment    = augment   # 是否启用augment_hsv 对比度,亮度等调整
        self.hyp        = hyp       # 超参数字典，其中包含图像增强会使用到的超参数
        self.rect       = rect      # 是否使用rectangular training
        # 注意: 开启rect后，mosaic就默认关闭
        self.mosaic = self.augment and not self.rect  # load 4 images at a time into a mosaic (only during training)

        #------------------------------------------------#
        #   Define labels
        #   遍历设置图像对应的label路径
        #   (./my_yolo_dataset/train/images/2009_004012.jpg) -> (./my_yolo_dataset/train/labels/2009_004012.txt)
        #------------------------------------------------#
        self.label_files = [x.replace("images", "labels").replace(os.path.splitext(x)[-1], ".txt")
                            for x in self.img_files]

        #------------------------------------------------#
        #   Read image shapes (wh)
        #   查看data文件下是否缓存有对应数据集的.shapes文件，里面存储了每张图像的width, height
        #   训练之后才会有 .shapes
        #------------------------------------------------#
        sp = path.replace(".txt", ".shapes")  # shapefile path

        #------------------------------------------------#
        #   第一次读取shape会报错,没有 shapes 文件,会创建图片信息
        #------------------------------------------------#
        try:
            with open(sp, "r") as f:  # read existing shapefile
                s = [x.split() for x in f.read().splitlines()]
                #------------------------------------------------#
                #   判断现有的shape文件中的行数(图像个数)是否与当前数据集中图像个数相等
                #   如果不相等则认为是不同的数据集，故重新生成shape文件
                #------------------------------------------------#
                assert len(s) == n, "shapefile out of aync"
        except Exception as e:
            # print("read {} failed [{}], rebuild {}.".format(sp, e, sp))
            # tqdm库会显示处理的进度
            # 读取每张图片的size信息
            if rank in [-1, 0]: # rank 是否是主进程
                image_files = tqdm(self.img_files, desc="Reading image shapes")
            else:
                image_files = self.img_files
            s = [exif_size(Image.open(f)) for f in image_files]
            # 将所有图片的shape信息保存在.shape文件中
            np.savetxt(sp, s, fmt="%g")  # overwrite existing (if any)

        #------------------------------------------------#
        #   记录每张图像的原始尺寸
        #------------------------------------------------#
        self.shapes = np.array(s, dtype=np.float64)

        #------------------------------------------------#
        # Rectangular Training https://github.com/ultralytics/yolov3/issues/232
        # 如果为ture，训练网络时，会使用类似原图像比例的矩形(让最长边为img_size)，而不是img_size x img_size
        # 注意: 开启rect后，mosaic就默认关闭
        #------------------------------------------------#
        if self.rect:
            # Sort by aspect ratio
            s = self.shapes  # wh
            #------------------------------------------------#
            #   计算每个图片的高/宽比
            #------------------------------------------------#
            ar = s[:, 1] / s[:, 0]  # aspect ratio
            #------------------------------------------------#
            #   argsort函数返回的是数组值从小到大的索引值
            #   按照高宽比例进行排序，这样后面划分的每个batch中的图像就拥有类似的高宽比
            #------------------------------------------------#
            irect = ar.argsort()
            #------------------------------------------------#
            #   根据排序后的顺序重新设置图像顺序、标签顺序以及shape顺序
            #------------------------------------------------#
            self.img_files = [self.img_files[i] for i in irect]
            self.label_files = [self.label_files[i] for i in irect]
            self.shapes = s[irect]  # wh
            ar = ar[irect]          # 排序后的高/宽比

            #------------------------------------------------#
            #   set training image shapes
            #   最大尺寸相同,最小边长不同
            #   计算每个batch采用的统一尺度
            #------------------------------------------------#
            shapes = [[1, 1]] * nb  # nb: 多少个batch
            for i in range(nb):
                ari = ar[bi == i]   # bi: batch index 找每个batch对应的索引位置
                #------------------------------------------------#
                #   获取第i个batch中，最小和最大高宽比
                #------------------------------------------------#
                mini, maxi = ari.min(), ari.max()
                #------------------------------------------------#
                #   如果高/宽小于1(h < w)，将w设为img_size
                #   maxi: h相对指定尺度的比例(小于1) 1: w相对指定尺度的比例
                #   假设为 [0.75, 1] 我们会让它乘以batch中全部图片的高宽,向上取整,得到最近的32的倍数为最终大小,图片放大后填充,空余部分用灰色填充
                #   图片在左上角,其余部分填充,这样好调整
                #------------------------------------------------#
                if maxi < 1:
                    shapes[i] = [maxi, 1]
                #------------------------------------------------#
                #   如果高/宽大于1((h > w)，将h设置为img_size
                #   mini: 高/宽比, 高固定为1, 宽=1/ratio
                #   假设为 [1, 0.75] 我们会让它乘以batch中全部图片的高宽,向上取整,得到最近的32的倍数为最终大小,图片放大后填充,空余部分用灰色填充
                #   图片在左上角,其余部分填充,这样好调整
                #------------------------------------------------#
                elif mini > 1:
                    shapes[i] = [1, 1 / mini]
            # 计算每个batch输入网络的shape值(向上设置为32的整数倍)
            self.batch_shapes = np.ceil(np.array(shapes) * img_size / 32. + pad).astype(np.int) * 32

        #------------------------------------------------#
        #   cache labels
        #   n为图像总数
        #------------------------------------------------#
        self.imgs = [None] * n
        #------------------------------------------------#
        #   label: [class, x, y, w, h] 其中的xywh都为相对值
        #------------------------------------------------#
        self.labels = [np.zeros((0, 5), dtype=np.float32)] * n
        extract_bounding_boxes, labels_loaded = False, False
        #------------------------------------------------#
        #       缺少标签  找到了  空标签  重复标签
        # number mission, found, empty, duplicate
        #------------------------------------------------#
        nm, nf, ne, nd = 0, 0, 0, 0
        #------------------------------------------------#
        #   这里分别命名是为了防止出现rect为False/True时混用导致计算的mAP错误
        #   当rect为True时会对self.images和self.labels进行从新排序
        #------------------------------------------------#
        if rect is True:
            np_labels_path = str(Path(self.label_files[0]).parent) + ".rect.npy"  # saved labels in *.npy file
        else:
            np_labels_path = str(Path(self.label_files[0]).parent) + ".norect.npy"

        if os.path.isfile(np_labels_path):  # 缓存文件是否存在
            x = np.load(np_labels_path, allow_pickle=True)
            if len(x) == n:
                #------------------------------------------------#
                # 如果载入的缓存标签个数与当前计算的图像数目相同则认为是同一数据集，直接读缓存
                #------------------------------------------------#
                self.labels = x
                labels_loaded = True

        # 处理进度条只在第一个进程中显示
        if rank in [-1, 0]:     # rank 是否是主进程
            pbar = tqdm(self.label_files)
        else:
            pbar = self.label_files

        #------------------------------------------------#
        #   遍历载入标签文件
        #------------------------------------------------#
        for i, file in enumerate(pbar):
            if labels_loaded is True:
                # 如果存在缓存直接从缓存读取
                l = self.labels[i]
            else:
                # 从文件读取标签信息
                try:
                    with open(file, "r") as f:
                        # 读取每一行label，并按空格划分数据 每一行5个数据: 类别索引 x y w h 相对坐标
                        l = np.array([x.split() for x in f.read().splitlines()], dtype=np.float32)
                except Exception as e:
                    print("An error occurred while loading the file {}: {}".format(file, e))
                    nm += 1  # 错文件计数
                    continue

            #------------------------------------------------#
            # 文件有标注信息
            #------------------------------------------------#
            if l.shape[0]:
                # 标签信息每行必须是五个值[class, x, y, w, h]
                assert l.shape[1] == 5, "> 5 label columns: %s" % file
                assert (l >= 0).all(), "negative labels: %s" % file                                             # 类别id大于等于1
                assert (l[:, 1:] <= 1).all(), "non-normalized or out of bounds coordinate labels: %s" % file    # 相对坐标小于等于1

                # 检查每一行，看是否有重复信息
                if np.unique(l, axis=0).shape[0] < l.shape[0]:  # duplicate rows
                    nd += 1     # 重复行+1
                if single_cls:
                    l[:, 0] = 0  # force dataset into single-class mode

                self.labels[i] = l
                nf += 1  # 成功找到文件+1

                #------------------------------------------------#
                # Extract object detection boxes for a second stage classifier
                # True 将图片中每一个目标裁剪出来,进行保存,可以进行分类
                #------------------------------------------------#
                if extract_bounding_boxes:
                    p = Path(self.img_files[i])
                    img = cv2.imread(str(p))
                    h, w = img.shape[:2]
                    for j, x in enumerate(l):
                        f = "%s%sclassifier%s%g_%g_%s" % (p.parent.parent, os.sep, os.sep, x[0], j, p.name)
                        if not os.path.exists(Path(f).parent):
                            os.makedirs(Path(f).parent)  # make new output folder

                        # 将相对坐标转为绝对坐标
                        # b: x, y, w, h
                        b = x[1:] * [w, h, w, h]  # box
                        # 将宽和高设置为宽和高中的最大值
                        b[2:] = b[2:].max()  # rectangle to square
                        # 放大裁剪目标的宽高
                        b[2:] = b[2:] * 1.3 + 30  # pad
                        # 将坐标格式从 x,y,w,h -> xmin,ymin,xmax,ymax
                        b = xywh2xyxy(b.reshape(-1, 4)).revel().astype(np.int)

                        # 裁剪bbox坐标到图片内
                        b[[0, 2]] = np.clip[b[[0, 2]], 0, w]
                        b[[1, 3]] = np.clip[b[[1, 3]], 0, h]
                        assert cv2.imwrite(f, img[b[1]:b[3], b[0]:b[2]]), "Failure extracting classifier boxes"
            else:
                ne += 1  # 空文件+1

            # 处理进度条只在第一个进程中显示
            if rank in [-1, 0]:     # rank 是否是主进程
                # 更新进度条描述信息
                pbar.desc = "Caching labels (%g found, %g missing, %g empty, %g duplicate, for %g images)" % (
                    nf, nm, ne, nd, n)
        assert nf > 0, "No labels found in %s." % os.path.dirname(self.label_files[0]) + os.sep

        #------------------------------------------------#
        #   如果标签信息没有被保存成numpy的格式，且训练样本数大于1000则将标签信息保存成numpy的格式
        #------------------------------------------------#
        if not labels_loaded and n > 1000:
            print("Saving labels to %s for faster future loading" % np_labels_path)
            np.save(np_labels_path, self.labels)  # save for next time

        #------------------------------------------------#
        #   缓存图片到内存
        #   Cache images into memory for faster training (Warning: large datasets may exceed system RAM)
        #------------------------------------------------#
        if cache_images:  # if training
            gb = 0  # Gigabytes of cached images 用于记录缓存图像占用RAM大小
            if rank in [-1, 0]:
                pbar = tqdm(range(len(self.img_files)), desc="Caching images")
            else:
                pbar = range(len(self.img_files))

            self.img_hw0, self.img_hw = [None] * n, [None] * n
            for i in pbar:  # max 10k images
                self.imgs[i], self.img_hw0[i], self.img_hw[i] = load_image(self, i)  # img, hw_original, hw_resized
                gb += self.imgs[i].nbytes  # 用于记录缓存图像占用RAM大小
                if rank in [-1, 0]:
                    pbar.desc = "Caching images (%.1fGB)" % (gb / 1E9)

        #------------------------------------------------#
        #   检测文件是否损坏,遍历图片,严重影响速度
        #   Detect corrupted images https://medium.com/joelthchao/programmatically-detect-corrupted-image-8c1b2006c3d3
        #------------------------------------------------#
        detect_corrupted_images = False
        if detect_corrupted_images:
            from skimage import io  # conda install -c conda-forge scikit-image
            for file in tqdm(self.img_files, desc="Detecting corrupted images"):
                try:
                    _ = io.imread(file)
                except Exception as e:
                    print("Corrupted image detected: {}, {}".format(file, e))

    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, index):
        #------------------------------------------------#
        #   获取超参数
        #------------------------------------------------#
        hyp = self.hyp
        #------------------------------------------------#
        #   是否使用马赛克,训练集使用,验证集不使用
        #------------------------------------------------#
        if self.mosaic:
            # load mosaic
            img, labels = load_mosaic(self, index)
            shapes = None
        else:
            # load image
            img, (h0, w0), (h, w) = load_image(self, index)

            #------------------------------------------------#
            #   letterbox
            #   index原本是哪一个batch,找到batch的大小
            #------------------------------------------------#
            shape = self.batch_shapes[self.batch[index]] if self.rect else self.img_size  # final letterboxed shape
            # 裁剪后的图片,缩放比例,填充数值
            img, ratio, pad = letterbox(img, shape, auto=False, scale_up=self.augment)
            shapes = (h0, w0), ((h / h0, w / w0), pad)  # for COCO mAP rescaling

            #------------------------------------------------#
            #   load labels
            #   相对坐标中心宽高转化为左上右下绝对坐标
            #------------------------------------------------#
            labels = []
            x = self.labels[index]
            if x.size > 0:
                # Normalized xywh to pixel xyxy format
                labels = x.copy()  # label: class, x, y, w, h
                labels[:, 1] = ratio[0] * w * (x[:, 1] - x[:, 3] / 2) + pad[0]  # pad width
                labels[:, 2] = ratio[1] * h * (x[:, 2] - x[:, 4] / 2) + pad[1]  # pad height
                labels[:, 3] = ratio[0] * w * (x[:, 1] + x[:, 3] / 2) + pad[0]
                labels[:, 4] = ratio[1] * h * (x[:, 2] + x[:, 4] / 2) + pad[1]

        #------------------------------------------------#
        #   数据增强
        #------------------------------------------------#
        if self.augment:
            #------------------------------------------------#
            #   mosaic默认使用了变化,没用mosaic才使用
            #------------------------------------------------#
            if not self.mosaic:
                img, labels = random_affine(img, labels,
                                            degrees=hyp["degrees"],
                                            translate=hyp["translate"],
                                            scale=hyp["scale"],
                                            shear=hyp["shear"])

            #------------------------------------------------#
            #   hsv空间增强
            #------------------------------------------------#
            augment_hsv(img, h_gain=hyp["hsv_h"], s_gain=hyp["hsv_s"], v_gain=hyp["hsv_v"])

        nL = len(labels)  # number of labels
        if nL:
            #------------------------------------------------#
            #   左上角转化为中心坐标
            #------------------------------------------------#
            labels[:, 1:5] = xyxy2xywh(labels[:, 1:5])

            #------------------------------------------------#
            #   转化为相对坐标
            #------------------------------------------------#
            labels[:, [2, 4]] /= img.shape[0]  # height
            labels[:, [1, 3]] /= img.shape[1]  # width

        #------------------------------------------------#
        #   图片随机翻转
        #------------------------------------------------#
        if self.augment:
            # random left-right flip 水平
            lr_flip = True  # 随机水平翻转
            if lr_flip and random.random() < 0.5:
                img = np.fliplr(img)
                if nL:
                    labels[:, 1] = 1 - labels[:, 1]  # 1 - x_center

            # random up-down flip    竖直
            ud_flip = False
            if ud_flip and random.random() < 0.5:
                img = np.flipud(img)
                if nL:
                    labels[:, 2] = 1 - labels[:, 2]  # 1 - y_center

        # 每个label有6个值 第1个全为0,后面依次是 class,x,y,w,h
        labels_out = torch.zeros((nL, 6))  # nL: number of labels
        if nL:
            # 从1开始放入,0行全为0
            labels_out[:, 1:] = torch.from_numpy(labels)

        #------------------------------------------------#
        #   Convert BGR to RGB, and HWC to CHW(3x512x512)
        #------------------------------------------------#
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)

        #------------------------------------------------#
        #   图片,标签,图片路径,形状,图片id
        #------------------------------------------------#
        return torch.from_numpy(img), labels_out, self.img_files[index], shapes, index

    def coco_index(self, index):
        """该方法是专门为cocotools统计标签信息准备，不对图像和标签作任何处理"""
        o_shapes = self.shapes[index][::-1]  # wh to hw

        # load labels
        x = self.labels[index]
        labels = x.copy()  # label: class, x, y, w, h
        return torch.from_numpy(labels), o_shapes

    @staticmethod
    def collate_fn(batch):
        # 图片,标签,图片路径,形状,图片id
        img, label, path, shapes, index = zip(*batch)  # transposed
        for i, l in enumerate(label):
            #------------------------------------------------#
            #   同一张图片的label第一个值是相同的,作为id
            #   add target image index for build_targets()
            #------------------------------------------------#
            l[:, 0] = i
        #------------------------------------------------#
        #   stack会在0添加一维,label本身就多一个维度,所以用cat
        #------------------------------------------------#
        return torch.stack(img, 0), torch.cat(label, 0), path, shapes, index


def load_image(self, index):
    """
    缓存图片
    将载入过的图像进行缓存
    """
    # loads 1 image from dataset, returns img, original hw, resized hw
    img = self.imgs[index]
    if img is None:  # not cached
        path = self.img_files[index]
        img = cv2.imread(path)  # BGR
        assert img is not None, "Image Not Found " + path
        h0, w0 = img.shape[:2]  # 原始 hw
        # img_size 设置的是预处理后输出的图片尺寸
        r = self.img_size / max(h0, w0)  # 缩放图片大小到 img_size
        if r != 1:  # 尺寸大小不等于就缩放,不改变图片比例,只将最大边缩放到指定宽度
            interp = cv2.INTER_AREA if r < 1 and not self.augment else cv2.INTER_LINEAR
            img = cv2.resize(img, (int(w0 * r), int(h0 * r)), interpolation=interp)
        return img, (h0, w0), img.shape[:2]  # img, hw_original, hw_resized
    else:
        return self.imgs[index], self.img_hw0[index], self.img_hw[index]  # img, hw_original, hw_resized


def load_mosaic(self, index):
    """
    将四张图片拼接在一张马赛克图像中
    :param self:
    :param index: 需要获取的图像索引
    :return:
    """

    labels4 = []        # 拼接图像的label信息
    s = self.img_size   # 期待输出的图像大小尺寸 宽高是默认图像尺寸的2倍
    #------------------------------------------------#
    #   随机初始化拼接图像的中心点坐标
    #   x,y在 0.5~1.5之间,因为新图像宽高是原来的2倍
    #------------------------------------------------#
    xc, yc = [int(random.uniform(s * 0.5, s * 1.5)) for _ in range(2)]  # mosaic center x, y
    #------------------------------------------------#
    #   再从dataset中随机寻找三张图像索引进行拼接
    #------------------------------------------------#
    indices = [index] + [random.randint(0, len(self.labels) - 1) for _ in range(3)]  # 3 additional image indices
    #------------------------------------------------#
    #   遍历四张图像索引进行拼接
    #------------------------------------------------#
    for i, index in enumerate(indices):
        # load image
        img, _, (h, w) = load_image(self, index)

        # place img in img4
        if i == 0:  # 第一张图片 top left
            #------------------------------------------------#
            #   创建马赛克图像,是指定宽高的2倍
            #------------------------------------------------#
            img4 = np.full((s * 2, s * 2, img.shape[2]), 114, dtype=np.uint8)  # base image with 4 tiles
            #------------------------------------------------#
            #   计算马赛克图像中的坐标信息(将图像填充到马赛克图像中)
            #   max(xc - w, 0), max(yc - h, 0) 相减看左上角坐标是否小于(0,0)
            #------------------------------------------------#
            x1a, y1a, x2a, y2a = max(xc - w, 0), max(yc - h, 0), xc, yc  # xmin, ymin, xmax, ymax (large image)
            #------------------------------------------------#
            #   计算截取的图像区域信息(以xc,yc为第一张图像的右下角坐标填充到马赛克图像中，丢弃越界的区域)
            #   截取图片右下角
            #   w - (x2a - x1a) 宽度减去超出界限  h - (y2a - y1a) 高度减去超出边界
            #------------------------------------------------#
            x1b, y1b, x2b, y2b = w - (x2a - x1a), h - (y2a - y1a), w, h  # xmin, ymin, xmax, ymax (small image)
        elif i == 1:  # top right
            #------------------------------------------------#
            #   计算马赛克图像中的坐标信息(将图像填充到马赛克图像中)
            #------------------------------------------------#
            x1a, y1a, x2a, y2a = xc, max(yc - h, 0), min(xc + w, s * 2), yc
            #------------------------------------------------#
            #   计算截取的图像区域信息(以xc,yc为第二张图像的左下角坐标填充到马赛克图像中，丢弃越界的区域)
            #------------------------------------------------#
            x1b, y1b, x2b, y2b = 0, h - (y2a - y1a), min(w, x2a - x1a), h
        elif i == 2:  # bottom left
            #------------------------------------------------#
            #   计算马赛克图像中的坐标信息(将图像填充到马赛克图像中)
            #------------------------------------------------#
            x1a, y1a, x2a, y2a = max(xc - w, 0), yc, xc, min(s * 2, yc + h)
            #------------------------------------------------#
            #   计算截取的图像区域信息(以xc,yc为第三张图像的右上角坐标填充到马赛克图像中，丢弃越界的区域)
            #------------------------------------------------#
            x1b, y1b, x2b, y2b = w - (x2a - x1a), 0, max(xc, w), min(y2a - y1a, h)
        elif i == 3:  # bottom right
            #------------------------------------------------#
            #   计算马赛克图像中的坐标信息(将图像填充到马赛克图像中)
            #------------------------------------------------#
            x1a, y1a, x2a, y2a = xc, yc, min(xc + w, s * 2), min(s * 2, yc + h)
            #------------------------------------------------#
            #   计算截取的图像区域信息(以xc,yc为第四张图像的左上角坐标填充到马赛克图像中，丢弃越界的区域)
            #------------------------------------------------#
            x1b, y1b, x2b, y2b = 0, 0, min(w, x2a - x1a), min(y2a - y1a, h)

        #------------------------------------------------#
        #   将截取的图像区域填充到马赛克图像的相应位置
        #------------------------------------------------#
        img4[y1a:y2a, x1a:x2a] = img[y1b:y2b, x1b:x2b]  # img4[ymin:ymax, xmin:xmax]
        #------------------------------------------------#
        #   计算pad(图像边界与马赛克边界的距离，越界的情况为负值,就是没越界的情况)
        #------------------------------------------------#
        padw = x1a - x1b
        padh = y1a - y1b

        #------------------------------------------------#
        #   Labels 获取对应拼接图像的labels信息,坐标是相对坐标和宽高
        #   [class_index, x_center, y_center, w, h]
        #------------------------------------------------#
        x = self.labels[index]
        labels = x.copy()  # 深拷贝，防止修改原数据
        if x.size > 0:  # Normalized xywh to pixel xyxy format
            #------------------------------------------------#
            #   计算标注数据在马赛克图像中的坐标(相对坐标 -> 绝对坐标)
            #   从1开始取,0代表图片类别
            #------------------------------------------------#
            labels[:, 1] = w * (x[:, 1] - x[:, 3] / 2) + padw   # xmin
            labels[:, 2] = h * (x[:, 2] - x[:, 4] / 2) + padh   # ymin
            labels[:, 3] = w * (x[:, 1] + x[:, 3] / 2) + padw   # xmax
            labels[:, 4] = h * (x[:, 2] + x[:, 4] / 2) + padh   # ymax
        labels4.append(labels)

    #------------------------------------------------#
    #   有目标才拼接
    #------------------------------------------------#
    if len(labels4):
        labels4 = np.concatenate(labels4, 0)
        # 设置上下限防止越界
        np.clip(labels4[:, 1:], 0, 2 * s, out=labels4[:, 1:])  # use with random_affine

    #------------------------------------------------#
    #   Augment
    #   随机旋转，缩放，平移以及错切
    #------------------------------------------------#
    img4, labels4 = random_affine(img4, labels4,
                                  degrees=self.hyp['degrees'],
                                  translate=self.hyp['translate'],
                                  scale=self.hyp['scale'],
                                  shear=self.hyp['shear'],
                                  border=-s // 2)  # border to remove   s是期待输出图片的大小

    return img4, labels4


def random_affine(img, targets=(), degrees=10, translate=.1, scale=.1, shear=10, border=0):
    """随机旋转，缩放，平移以及错切"""
    # torchvision.transforms.RandomAffine(degrees=(-10, 10), translate=(.1, .1), scale=(.9, 1.1), shear=(-10, 10))
    # https://medium.com/uruvideo/dataset-augmentation-with-random-homographies-a8f4b44830d4
    # 这里可以参考我写的博文: https://blog.csdn.net/qq_37541097/article/details/119420860
    # targets = [cls, xyxy]

    #------------------------------------------------#
    #   最终输出的图像尺寸，等于img4.shape / 2
    #   img是马赛克背景的宽高=2s, border = -s/2  最后是  2s - s/2 * 2 = s
    #------------------------------------------------#
    height = img.shape[0] + border * 2
    width = img.shape[1] + border * 2

    #------------------------------------------------#
    #   Rotation and Scale
    #   生成旋转以及缩放矩阵
    #------------------------------------------------#
    R = np.eye(3)  # 生成对角阵
    a = random.uniform(-degrees, degrees)       # 随机旋转角度
    s = random.uniform(1 - scale, 1 + scale)    # 随机缩放因子
    R[:2] = cv2.getRotationMatrix2D(angle=a, center=(img.shape[1] / 2, img.shape[0] / 2), scale=s)

    #------------------------------------------------#
    #   Translation
    #   生成平移矩阵
    #------------------------------------------------#
    T = np.eye(3)
    T[0, 2] = random.uniform(-translate, translate) * img.shape[0] + border  # x translation (pixels)
    T[1, 2] = random.uniform(-translate, translate) * img.shape[1] + border  # y translation (pixels)

    #------------------------------------------------#
    #   Shear
    #   生成错切矩阵
    #------------------------------------------------#
    S = np.eye(3)
    S[0, 1] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # x shear (deg)
    S[1, 0] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # y shear (deg)

    #------------------------------------------------#
    #   放射矩阵相乘得到最终变化矩阵
    #------------------------------------------------#
    M = S @ T @ R  # ORDER IS IMPORTANT HERE!!
    if (border != 0) or (M != np.eye(3)).any():  # image changed
        # 进行仿射变化
        img = cv2.warpAffine(img, M[:2], dsize=(width, height), flags=cv2.INTER_LINEAR, borderValue=(114, 114, 114))

    #------------------------------------------------#
    #   对坐标进行变化
    #   Transform label coordinates
    #------------------------------------------------#
    n = len(targets)
    if n:
        #------------------------------------------------#
        #   四个顶点坐标
        #------------------------------------------------#
        xy = np.ones((n * 4, 3))
        xy[:, :2] = targets[:, [1, 2, 3, 4, 1, 4, 3, 2]].reshape(n * 4, 2)  # x1y1, x2y2, x1y2, x2y1
        # [4*n, 3] -> [n, 8]
        xy = (xy @ M.T)[:, :2].reshape(n, 8)

        #------------------------------------------------#
        #   调整目标边界框
        #   对transform后的bbox进行修正(假设变换后的bbox变成了菱形，此时要修正成矩形),框框要横平竖直,不能倾斜
        #------------------------------------------------#
        x = xy[:, [0, 2, 4, 6]]  # [n, 4]
        y = xy[:, [1, 3, 5, 7]]  # [n, 4]
        #   取最小的x,y为新的左上角; 最大的x,y为右下角
        xy = np.concatenate((x.min(1), y.min(1), x.max(1), y.max(1))).reshape(4, n).T  # [n, 4]

        #------------------------------------------------#
        #   reject warped points outside of image
        #   对坐标进行裁剪，防止越界
        #------------------------------------------------#
        xy[:, [0, 2]] = xy[:, [0, 2]].clip(0, width)
        xy[:, [1, 3]] = xy[:, [1, 3]].clip(0, height)
        w = xy[:, 2] - xy[:, 0]
        h = xy[:, 3] - xy[:, 1]

        #------------------------------------------------#
        #   计算调整后的每个box的面积
        #------------------------------------------------#
        area = w * h
        #------------------------------------------------#
        #   计算调整前的每个box的面积
        #------------------------------------------------#
        area0 = (targets[:, 3] - targets[:, 1]) * (targets[:, 4] - targets[:, 2])
        #------------------------------------------------#
        #   变化之后计算每个box的比例
        #------------------------------------------------#
        ar = np.maximum(w / (h + 1e-16), h / (w + 1e-16))  # aspect ratio
        #------------------------------------------------#
        #   选取长宽大于4个像素，且调整前后面积比例大于0.2，且比例小于10的box
        #------------------------------------------------#
        i = (w > 4) & (h > 4) & (area / (area0 * s + 1e-16) > 0.2) & (ar < 10)

        targets = targets[i]
        targets[:, 1:5] = xy[i]

    return img, targets

#------------------------------------------------#
#   hsv空间增强
#------------------------------------------------#
def augment_hsv(img, h_gain=0.5, s_gain=0.5, v_gain=0.5):
    # 这里可以参考我写的博文:https://blog.csdn.net/qq_37541097/article/details/119478023
    r = np.random.uniform(-1, 1, 3) * [h_gain, s_gain, v_gain] + 1  # random gains
    hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    dtype = img.dtype  # uint8

    x = np.arange(0, 256, dtype=np.int16)
    lut_hue = ((x * r[0]) % 180).astype(dtype)
    lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)
    lut_val = np.clip(x * r[2], 0, 255).astype(dtype)

    img_hsv = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val))).astype(dtype)
    cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR, dst=img)  # no return needed


def letterbox(img: np.ndarray,
              new_shape=(416, 416),
              color=(114, 114, 114),
              auto=True,
              scale_fill=False,
              scale_up=True):
    """
    将图片缩放调整到指定大小
    :param img:
    :param new_shape:
    :param color:
    :param auto:
    :param scale_fill:
    :param scale_up:
    :return:
    """

    shape = img.shape[:2]  # [h, w]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scale_up:  # only scale down, do not scale up (for better test mAP) 对于大于指定输入大小的图片进行缩放,小于的不变
        r = min(r, 1.0)

    # compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimun rectangle 保证原图比例不变，将图像最大边缩放到指定大小
        # 这里的取余操作可以保证padding后的图片是32的整数倍
        dw, dh = np.mod(dw, 32), np.mod(dh, 32)  # wh padding
    elif scale_fill:  # stretch 简单粗暴的将图片缩放到指定尺寸
        dw, dh = 0, 0
        new_unpad = new_shape
        ratio = new_shape[0] / shape[1], new_shape[1] / shape[0]  # wh ratios

    dw /= 2  # divide padding into 2 sides 将padding分到上下，左右两侧
    dh /= 2

    # shape:[h, w]  new_unpad:[w, h]
    if shape[::-1] != new_unpad:
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))  # 计算上下两侧的padding
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))  # 计算左右两侧的padding

    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)


def create_folder(path="./new_folder"):
    # Create floder
    if os.path.exists(path):
        shutil.rmtree(path)  # dalete output folder
    os.makedirs(path)  # make new output folder




