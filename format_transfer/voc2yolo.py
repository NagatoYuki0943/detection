"""Label Convert

Convert from VOC -> YOLO
"""

from pathlib import Path
from shutil import copy
import traceback
from PIL import Image
import xml.etree.ElementTree as ET
from tqdm import tqdm
from functions import get_image_path, load_name2id_from_yaml


def voc2yolo(
    xml_dirs: str | Path | list[str | Path],
    image_dirs: str | Path | list[str | Path],
    new_txt_dir: str | Path,
    name2id: dict[str, int],
    new_image_dir: str | Path = None,
) -> None:
    """Convert VOC to YOLO

    Args:
        xml_dirs (str | Path | list[str | Path]): 已有 VOC 格式的 xml 文件目录
        image_dirs (str | Path | list[str | Path]): 已有图片目录
        new_txt_dir (str | Path): 新的 YOLO 格式的 txt 文件目录
        name2id (dict[str, int]): 类别名称到 ID 的映射, 只转换存在于 name2id 中的类别
        new_image_dir (str | Path, optional): 新的图片目录, 如果为 None 则不复制图片. Defaults to None.
    """
    assert len(name2id) > 0

    print(
        "Converting VOC to YOLO...\n"
        f"xml_dirs: {xml_dirs}\n"
        f"image_dirs: {image_dirs}\n"
        f"new_txt_dir: {new_txt_dir}\n"
        f"new_image_dir: {new_image_dir}\n"
        f"name2id: {name2id}"
    )

    xml_dirs = [xml_dirs] if isinstance(xml_dirs, (str, Path)) else xml_dirs
    xml_dirs = [Path(xml_dir) for xml_dir in xml_dirs]
    image_dirs = [image_dirs] if isinstance(image_dirs, (str, Path)) else image_dirs
    image_dirs = [Path(xml_dir) for xml_dir in image_dirs]

    assert len(xml_dirs) == len(image_dirs)

    xml_paths = []
    image_paths = []
    for xml_dir, image_dir in zip(xml_dirs, image_dirs):
        if not xml_dir.exists():
            raise FileNotFoundError(f"xml_dir not exists: {xml_dir}")
        if not image_dir.exists():
            raise FileNotFoundError(f"image_dir not exists: {image_dir}")
        _xml_paths = list(xml_dir.glob("*.xml"))
        xml_paths.extend(_xml_paths)
        image_paths.extend([get_image_path(image_dir, i.stem) for i in _xml_paths])

    new_txt_dir = Path(new_txt_dir)
    new_txt_dir.mkdir(exist_ok=True, parents=True)

    new_image_dir = Path(new_image_dir) if new_image_dir is not None else None
    if new_image_dir is not None:
        new_image_dir.mkdir(exist_ok=True, parents=True)

    xml_path: Path
    image_path: Path
    for xml_path, image_path in tqdm(
        zip(xml_paths, image_paths), desc="convert xml to txt", total=len(xml_paths)
    ):
        try:
            xml_stem = xml_path.stem
            txt_path = new_txt_dir / f"{xml_stem}.txt"

            with open(xml_path, "r", encoding="utf-8") as in_file:
                tree = ET.parse(in_file)

            w, h = Image.open(image_path).size

            class_exists = False
            objs = tree.findall("object")
            for obj in objs:
                name = obj.find("name").text
                if name in name2id:
                    class_exists = True
                    break

            if not class_exists:
                continue

            if new_image_dir is not None:
                new_image_path = new_image_dir / image_path.name
                copy(image_path, new_image_path)

            with open(txt_path, "w", encoding="utf-8") as out_file:
                for obj in objs:
                    name = obj.find("name").text

                    # 忽略不存在的类别
                    if name not in name2id.keys():
                        continue

                    difficult = obj.find("difficult").text
                    if int(difficult) == 1:
                        continue

                    xml_box = obj.find("bndbox")

                    x_min = float(xml_box.find("xmin").text)
                    y_min = float(xml_box.find("ymin").text)

                    x_max = float(xml_box.find("xmax").text)
                    y_max = float(xml_box.find("ymax").text)

                    box_x_center = (x_min + x_max) / 2
                    box_y_center = (y_min + y_max) / 2

                    box_w = x_max - x_min
                    box_h = y_max - y_min

                    box_x = box_x_center / w
                    box_w = box_w / w

                    box_y = box_y_center / h
                    box_h = box_h / h

                    cls_id = name2id[name]
                    out_file.write(f"{cls_id} {box_x} {box_y} {box_w} {box_h}\n")
        except FileNotFoundError:
            if (not txt_path.exists())
                print(f"txt file not found: {txt_path}")
            if (not image_path.exists())
                print(f"image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")


# if __name__ == "__main__":
#     # 原本的 xml 文件夹, 支持多个目录
#     xml_dirs = [
#         "../VOC/xmls/test2007",
#     ]
#     # 原本图片文件夹, 支持多个目录
#     image_dirs = [
#         "../VOC/images/test2007",
#     ]
#     # 新的 txt 文件夹, 会将全部的转换后的 txt 文件放到这个文件夹下
#     new_txt_dir = "../VOC/labels/test2007-1"
#     # yaml 配置路径
#     yaml_path = "../VOC/VOC.yaml"
#     name2id = load_name2id_from_yaml(yaml_path)
#     # 新的图片文件夹, 会把全部图片放在这个文件夹下, 如果为 None 则不复制图片
#     new_image_dir = None

#     voc2yolo(xml_dirs, image_dirs, new_txt_dir, name2id, new_image_dir)

if __name__ == "__main__":
    # 原本的 xml 文件夹, 支持多个目录
    xml_dirs = [
        "C:/ml/code/dataset/person--sample/val/xmls",
    ]
    # 原本图片文件夹, 支持多个目录
    image_dirs = [
        "C:/ml/code/dataset/person--sample/val/images",
    ]
    # 新的 txt 文件夹, 会将全部的转换后的 txt 文件放到这个文件夹下
    new_txt_dir = "C:/ml/code/dataset/person--sample/val/labels"
    # yaml 配置路径
    yaml_path = "C:/ml/code/dataset/person--sample/data.yaml"
    name2id = load_name2id_from_yaml(yaml_path)
    # 新的图片文件夹, 会把全部图片放在这个文件夹下, 如果为 None 则不复制图片
    new_image_dir = None

    voc2yolo(xml_dirs, image_dirs, new_txt_dir, name2id, new_image_dir)
