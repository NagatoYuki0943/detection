"""Filter voc dataset"""

from pathlib import Path
from shutil import copy
import traceback
from xml.etree import ElementTree
from tqdm import tqdm
from functions import get_image_path, load_names_from_yaml, save_names_to_yaml


def filter_voc(
    xml_dirs: str | Path | list[str | Path],
    image_dirs: str | Path | list[str | Path],
    filtered_save_dir: str | Path,
    keep_names: list[str],
    name_remap: dict[str, str] | None = None,
) -> None:
    """Filter VOC dataset by keep_names

    Args:
        xml_dirs (str | Path | list[str | Path]): 已有 VOC 格式的 xml 文件目录
        image_dirs (str | Path | list[str | Path]): 已有图片目录
        filtered_save_dir (str | Path): 过滤后的 VOC 格式的 xml 文件和图片存放目录, 里面会有 xmls 和 images 文件夹
        keep_names (list[str]): 需要保留的类别名称 list
        name_remap (dict[str, str] | None): 类别名称映射, 若为 None, 则不进行映射
    """
    print(
        "Filter VOC dataset by keep_names...\n"
        f"xml_dirs: {xml_dirs}\n"
        f"image_dirs: {image_dirs}\n"
        f"filtered_save_dir: {filtered_save_dir}\n"
        f"keep_names: {keep_names}\n"
        f"name_remap: {name_remap}"
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

    filtered_save_dir = Path(filtered_save_dir)
    new_xml_dir = filtered_save_dir / "xmls"
    new_xml_dir.mkdir(exist_ok=True, parents=True)
    new_image_dir = filtered_save_dir / "images"
    new_image_dir.mkdir(exist_ok=True, parents=True)
    new_yaml_path = filtered_save_dir / "filtered.yaml"

    if name_remap:
        new_names = [name_remap.get(i, i) for i in keep_names]
    else:
        new_names = keep_names
    new_names = sorted(new_names)
    save_names_to_yaml(new_yaml_path, new_names)

    i = 0
    xml_path: Path
    image_path: Path
    for xml_path, image_path in tqdm(
        zip(xml_paths, image_paths), desc="filter xml files", total=len(xml_paths)
    ):
        try:
            with open(xml_path, "r", encoding="utf-8") as in_file:
                tree = ElementTree.parse(in_file)
            root = tree.getroot()

            class_exists = False
            objs = tree.findall("object")
            new_objs = []
            for obj in objs:
                root.remove(obj)
                name = obj.find("name").text
                if name in keep_names:
                    class_exists = True
                    # name 映射
                    new_name = name_remap.get(name, name) if name_remap else name
                    obj.find("name").text = new_name
                    new_objs.append(obj)

            if not class_exists:
                continue

            for obj in new_objs:
                root.append(obj)

            new_xml_path = new_xml_dir / xml_path.name
            tree.write(new_xml_path)

            new_image_path = new_image_dir / image_path.name
            copy(image_path, new_image_path)

            i += 1
        except Exception:
            print(f"Error: {traceback.format_exc()}")

    print(f"total {len(xml_paths)} xml files, filtered {i} xml files.")


if __name__ == "__main__":
    # 原本 xml 文件路径, 支持多个目录
    xml_dirs = [
        "../VOC/xmls/test2007",
    ]
    # 原本图片文件路径, 支持多个目录, 但是要和 xml_dirs 一一匹配
    image_dirs = [
        "../VOC/images/test2007",
    ]
    # 过滤后的 xmls 和 images 的存放路径, 里面会有 xmls 和 images 文件夹
    filtered_save_dir = "../VOC/test2007--filtered"
    # 对应的 yaml 文件路径(不是必须, 当前主要目的是获取类别名称)
    yaml_path = "../VOC/VOC.yaml"

    names = load_names_from_yaml(yaml_path)

    # 保留的类别名, 这里保留前一半类别
    keep_names = names[: len(names) // 2]

    # 类别的重映射
    name_remap = {i: i for i in names}

    filter_voc(xml_dirs, image_dirs, filtered_save_dir, keep_names, name_remap)
