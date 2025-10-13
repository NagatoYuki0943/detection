import os
import json
import cv2
from tqdm import tqdm


# ----------------------------------#
#   将背景图片添加到coco json文件中
# ----------------------------------#

json_path = "coco/annotations/instances_train2017.json"
empty_image_dir = "empty"

# 打开json
with open(json_path, mode="r", encoding="utf-8") as f:
    data = json.load(f)

# 有标记图片
images_len = len(data["images"])
images_len

# 空白图片
empty_images = os.listdir(empty_image_dir)
empty_images = [
    empty for empty in empty_images if empty.endswith(("jpg", "jpeg", "png", "gif"))
]
empty_len = len(empty_images)

# 添加空白图片到json
pbar = tqdm(total=len(empty_images))
for i, emtpy in enumerate(empty_images):
    image = cv2.imread(os.path.join(empty_image_dir, emtpy))
    height, width, channel = image.shape
    data["images"].append(
        {"id": images_len + i, "file_name": emtpy, "width": width, "height": height}
    )
    pbar.update(1)
pbar.close()

# 添加后图片长度
new_images_len = len(data["images"])

# 保存json
with open(json_path, mode="w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(
    f"有标记图片数量为 {images_len},空白图片数量为 {empty_len},新图片长度为 {new_images_len}"
)
print(f"请手动将 {empty_image_dir} 目录下的图片移动到 coco/train2017 目录下")
