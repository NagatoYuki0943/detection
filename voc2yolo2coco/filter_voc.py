"""Filter dataset
"""

from pathlib import Path
from shutil import copy
import traceback
from xml.etree import ElementTree
from tqdm import tqdm
from functions import get_image_path


def filter_voc(
    xml_dir: str | Path,
    image_dir: str | Path,
    new_xml_dir: str | Path,
    new_image_dir: str | Path,
    names: dict[str, int],
) -> None:
    """Filter VOC dataset by names

    Args:
        xml_dir (str | Path): 已有 VOC 格式的 xml 文件目录
        image_dir (str | Path): 已有图片目录
        new_xml_dir (str | Path): 新的 xml 文件目录
        new_image_dir (str | Path, optional): 新的图片目录
        names (list[str]): 需要保留的类别名称 list
    """
    print(
        "Filter VOC dataset by names...\n"
        f"xml_dir: {xml_dir}\n"
        f"image_dir: {image_dir}\n"
        f"ew_xml_dir: {new_xml_dir}\n"
        f"ew_image_dir: {new_image_dir}\n"
        f"names: {names}"
    )

    xml_dir = Path(xml_dir)
    assert xml_dir.exists()
    image_dir = Path(image_dir)
    assert image_dir.exists()

    new_xml_dir = Path(new_xml_dir)
    new_xml_dir.mkdir(exist_ok=True, parents=True)
    new_image_dir = Path(new_image_dir)
    new_image_dir.mkdir(exist_ok=True, parents=True)

    for xml_file in tqdm(list(xml_dir.glob("*.xml"))):
        try:
            image_path = get_image_path(image_dir, xml_file.stem)

            with open(xml_file) as in_file:
                tree = ElementTree.parse(in_file)
            root = tree.getroot()

            class_exists = False
            objs = tree.findall("object")
            new_objs = []
            for obj in objs:
                root.remove(obj)
                name = obj.find("name").text
                if name in names:
                    class_exists = True
                    new_objs.append(obj)

            if not class_exists:
                continue

            for obj in new_objs:
                root.append(obj)

            new_xml_path = new_xml_dir / xml_file.name
            tree.write(new_xml_path)

            new_image_path = new_image_dir / image_path.name
            copy(image_path, new_image_path)
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")


if __name__ == "__main__":
    from config import voc_name2id, coco_name2id

    xml_dir = "../voc/xmls/test2007"
    image_dir = "../voc/images/test2007"
    new_xml_dir = "../voc/xmls/test2007-2"
    new_image_dir = "../voc/images/test2007-2"

    # 复制前一半类别
    i = 0
    names = []
    original_half_len = len(voc_name2id) // 2
    for key in voc_name2id:
        names.append(key)
        i += 1
        if i >= original_half_len:
            break

    filter_voc(xml_dir, image_dir, new_xml_dir, new_image_dir, names)
