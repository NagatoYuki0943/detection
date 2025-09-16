"""Label Convert

Convert from VOC -> YOLO
"""

from pathlib import Path
from shutil import copy
import traceback
from PIL import Image
from xml.etree import ElementTree
from tqdm import tqdm
from functions import get_image_path


def voc2yolo(
    xml_dir: str | Path,
    txt_dir: str | Path,
    image_dir: str | Path,
    name2id: dict[str, int],
    new_image_dir: str | Path = None,
) -> None:
    """Convert VOC to YOLO

    Args:
        xml_dir (str | Path): 已有 VOC 格式的 xml 文件目录
        txt_dir (str | Path): 新的 YOLO 格式的 txt 文件目录
        image_dir (str | Path): 已有图片目录
        name2id (dict[str, int]): 类别名称到 ID 的映射, 只转换存在于 name2id 中的类别
        new_image_dir (str | Path, optional): 新的图片目录, 如果为 None 则不复制图片. Defaults to None.
    """
    print(
        "Converting VOC to YOLO...\n"
        f"xml_dir: {xml_dir}\n"
        f"txt_dir: {txt_dir}\n"
        f"image_dir: {image_dir}\n"
        f"new_image_dir: {new_image_dir}\n"
        f"name2id: {name2id}"
    )

    xml_dir = Path(xml_dir)
    assert xml_dir.exists()
    image_dir = Path(image_dir)
    assert image_dir.exists()

    txt_dir = Path(txt_dir)
    txt_dir.mkdir(exist_ok=True, parents=True)

    new_image_dir = Path(new_image_dir) if new_image_dir is not None else None
    if new_image_dir is not None:
        new_image_dir.mkdir(exist_ok=True, parents=True)

    for xml_file in tqdm(list(xml_dir.glob("*.xml"))):
        try:
            xml_stem = xml_file.stem
            txt_path = txt_dir / f"{xml_stem}.txt"
            image_path = get_image_path(image_dir, xml_stem)

            with open(xml_file) as in_file:
                tree = ElementTree.parse(in_file)

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

            with open(txt_path, "w") as out_file:
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
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")


if __name__ == "__main__":
    from config import voc_name2id, coco_name2id

    xml_dir = "../voc/xmls/test2007"
    txt_dir = "../voc/labels/test2007-1"
    image_dir = "../voc/images/test2007"
    new_image_dir = None
    name2id = voc_name2id

    voc2yolo(xml_dir, txt_dir, image_dir, name2id, new_image_dir)
