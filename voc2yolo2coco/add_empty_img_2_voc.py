import os
from tqdm import tqdm


# -------------------------------------#
#   将背景图片添加到voc train.txt文件中
# -------------------------------------#

train_path = "VOCdevkit/VOC2007/ImageSets/Main/train.txt"
trainval_path = "VOCdevkit/VOC2007/ImageSets/Main/trainval.txt"
empty_dir = "empty"
empty_image_dir = empty_dir + "/JPEGImages"

images = os.listdir(empty_image_dir)
images = [image for image in images if image.endswith(".jpg")]

print(len(images))
with open(train_path, mode="a", encoding="utf-8") as f1, open(
    trainval_path, mode="a", encoding="utf-8"
) as f2:
    for image in tqdm(images):
        f1.write(image + "\n")
        f2.write(image + "\n")

print(f"空白图片数量为 {len(images)}")
print(
    f"请手动将 {empty_dir} 目录下的图片和xml文件移动到 VOCdevkit/VOC2007 对应的目录下"
)
