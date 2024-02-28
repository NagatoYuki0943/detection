#---------------------------------------------------#
#   官方实现的default_collate可以参考
#   https://github.com/pytorch/pytorch/blob/67b7e751e6b5931a9f45274653f4f653a4e6cdf6/torch/utils/data/_utils/collate.py
#   默认情况下pytorch会将taget进行stack()拼接,对于分类网络可以,但是对于目标检测,target就会报错
#   先用zip打包,再放入tuple中
#   zip变为两个列表,分别为image和target,再用tuple放入一起
#   [[1, "a"], [2, "b"], [3, "c"]]  ->  ((1, 2, 3), ('a', 'b', 'c'))
#---------------------------------------------------#
def collate_fn(batch):
    return tuple(zip(*batch))


#---------------------------------------------------#
#   和上面效果相同
#---------------------------------------------------#
def collate_fn(batch):
    images = []
    bboxes = []
    for img, box in batch:
        images.append(img)
        bboxes.append(box)
    images = np.array(images)
    return images, bboxes