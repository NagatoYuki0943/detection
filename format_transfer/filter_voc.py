"""Filter voc dataset"""

from typing import Literal
from pathlib import Path
from shutil import copy
import traceback
import xml.etree.ElementTree as ET
import yaml
from tqdm import tqdm
from collections import Counter
import cv2
from functions import get_image_path, load_names_from_yaml


def filter_voc(
    xml_dirs: str | Path | list[str | Path],
    image_dirs: str | Path | list[str | Path],
    filtered_save_dir: str | Path,
    keep_names: list[str],
    name_remap: dict[str, str] | None = None,
    save_box_height_percent: float = 0.0,
    save_box_width_percent: float = 0.0,
    save_box_percent_type: Literal["greater_eq", "less_eq"] = "greater_eq",
    train_height: int = 640,
    train_width: int = 640,
    use_train_size_calc_percent: bool = False,
) -> None:
    """Filter VOC dataset by keep_names

    Args:
        xml_dirs (str | Path | list[str | Path]): 已有 VOC 格式的 xml 文件目录
        image_dirs (str | Path | list[str | Path]): 已有图片目录
        filtered_save_dir (str | Path): 过滤后的 VOC 格式的 xml 文件和图片存放目录, 里面会有 xmls 和 images 文件夹
        keep_names (list[str]): 需要保留的类别名称 list
        id_remap (dict[int, int] | None): 类别 id 映射表, 若为 None, 则不进行映射
        save_box_height_percent (float): box 高度占图片高度的比例, 过滤掉高度小于或者大于该比例的目标框
        save_box_width_percent (float): box 宽度占图片宽度的比例, 过滤掉宽度小于或者大于该比例的目标框
        save_box_percent_type (Literal["greater_eq", "less_eq"]): 过滤掉 box 高度或者宽度大于等于或者小于等于该比例的目标框
        train_height (int): 训练时图片高度
        train_width (int): 训练时图片宽度
        use_train_size_calc_percent (bool): 是否使用训练时图片尺寸的计算最终比例
    """
    assert len(keep_names) > 0
    assert 0 <= save_box_height_percent <= 1
    assert 0 <= save_box_width_percent <= 1
    assert save_box_percent_type in ["greater_eq", "less_eq"]

    print(
        "Filter VOC dataset by keep_names...\n"
        f"xml_dirs: {xml_dirs}\n"
        f"image_dirs: {image_dirs}\n"
        f"filtered_save_dir: {filtered_save_dir}\n"
        f"keep_names: {keep_names}\n"
        f"name_remap: {name_remap}\n"
        f"save_box_height_percent: {save_box_height_percent}\n"
        f"save_box_width_percent: {save_box_width_percent}\n"
        f"save_box_percent_type: {save_box_percent_type}\n"
        f"train_height: {train_height}\n"
        f"train_width: {train_width}\n"
        f"use_train_size_calc_percent: {use_train_size_calc_percent}"
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
    new_yaml_path = filtered_save_dir / "data.yaml"

    if name_remap:
        new_names = [name_remap.get(i, i) for i in keep_names]
    else:
        new_names = keep_names
    new_names = sorted(set(new_names))
    data = {
        "names": {i: name for i, name in enumerate(new_names)},
    }

    i = 0
    j = 0
    new_names = []
    xml_path: Path
    image_path: Path
    for xml_path, image_path in tqdm(
        zip(xml_paths, image_paths), desc="filter xml files", total=len(xml_paths)
    ):
        try:
            with open(xml_path, "r", encoding="utf-8") as in_file:
                tree = ET.parse(in_file)
            root = tree.getroot()

            image = cv2.imread(str(image_path))
            height: float
            width: float
            channel: float
            height, width, channel = image.shape

            # 更新 xml 中的 size 标签
            size = tree.find("size")
            size.find("height").text = str(height)
            size.find("width").text = str(width)
            size.find("depth").text = str(channel)

            has_obj = False
            objs = tree.findall("object")
            new_objs = []
            for obj in objs:
                j += 1
                root.remove(obj)

                # 按照类别过滤
                name = obj.find("name").text
                if name not in keep_names:
                    continue

                # 按照 box 框大小忽略
                box = obj.find("bndbox")
                xmin = float(box.find("xmin").text)
                ymin = float(box.find("ymin").text)
                xmax = float(box.find("xmax").text)
                ymax = float(box.find("ymax").text)
                box_height_percent: float = (ymax - ymin) / height
                box_width_percent: float = (xmax - xmin) / width
                if use_train_size_calc_percent:
                    box_height_percent *= train_height / height
                    box_width_percent *= train_width / width

                if save_box_percent_type == "greater_eq" and (
                    box_width_percent < save_box_width_percent
                    or box_height_percent < save_box_height_percent
                ):
                    continue
                if save_box_percent_type == "less_eq" and (
                    box_width_percent > save_box_width_percent
                    or box_height_percent > save_box_height_percent
                ):
                    continue

                # name 映射
                new_name = name_remap.get(name, name) if name_remap else name
                new_names.append(new_name)
                obj.find("name").text = new_name
                new_objs.append(obj)
                has_obj = True

            # 按照类别过滤
            if not has_obj:
                continue

            for obj in new_objs:
                root.append(obj)

            # 自动调整缩进，space="\t" 使用 tab 缩进，或者 space="  " 使用两个空格
            if hasattr(ET, "indent"):
                ET.indent(tree, space="    ", level=0)

            new_xml_path = new_xml_dir / xml_path.name
            tree.write(new_xml_path)

            new_image_path = new_image_dir / image_path.name
            copy(image_path, new_image_path)

            i += 1
        except Exception:
            print(f"Error: {traceback.format_exc()}")

    print(
        f"original {len(xml_paths)} xml files, original {j} objects, filtered {i} xml files, filtered {len(new_names)} objects."
    )
    counters = dict(sorted(Counter(new_names).items(), key=lambda x: x[0]))
    print("object counts:")
    for name, count in counters.items():
        print(f"    {name}: {count}")

    data.update(
        {
            "statistics": {
                "original_files": len(xml_paths),
                "original_objects": j,
                "filtered_files": i,
                "filtered_objects": len(new_names),
                "filtered_counts": counters,
            }
        }
    )
    with open(new_yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"save yaml config to {new_yaml_path}")


if __name__ == "__main__":
    # 原本 xml 文件路径, 支持多个目录
    xml_dirs = [
        "../VOC/xmls/test2007",
    ]
    # 原本图片文件路径, 支持多个目录, 但是要和 xml_dirs 一一匹配
    image_dirs = [
        "../VOC/images/test2007",
    ]
    # 过滤后的 xmls 和 images 的存放路径, 里面会有 xmls 和 images 文件夹, 用来存放全部过滤后的数据
    filtered_save_dir = "../VOC/test2007--filtered--voc-format"
    # 对应的 yaml 文件路径(不是必须, 当前主要目的是获取类别名称)
    yaml_path = "../VOC/VOC.yaml"

    names = load_names_from_yaml(yaml_path)

    # 保留的类别名, 这里保留前一半类别
    keep_names = names[: len(names) // 2]

    # 类别的重映射
    name_remap = {i: i for i in keep_names}

    filter_voc(xml_dirs, image_dirs, filtered_save_dir, keep_names, name_remap)
