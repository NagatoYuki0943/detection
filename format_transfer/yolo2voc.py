"""Label Convert

Convert from YOLO -> VOC
"""

from pathlib import Path
from shutil import copy
import traceback
from PIL import Image
from tqdm import tqdm
from jinja2 import Template
from functions import get_image_path, load_id2name_from_yaml


annotation_template = """<annotation>
    <folder>{{ folder }}</folder>
    <filename>{{ filename }}</filename>
    <path>{{ path }}</path>
    <source>
        <database>{{ database }}</database>
    </source>
    <size>
        <width>{{ width }}</width>
        <height>{{ height }}</height>
        <depth>{{ depth }}</depth>
    </size>
    <segmented>{{ segmented }}</segmented>
{% for object in objects %}    <object>
        <name>{{ object.name }}</name>
        <pose>{{ object.pose }}</pose>
        <truncated>{{ object.truncated }}</truncated>
        <difficult>{{ object.difficult }}</difficult>
        <bndbox>
            <xmin>{{ object.xmin }}</xmin>
            <ymin>{{ object.ymin }}</ymin>
            <xmax>{{ object.xmax }}</xmax>
            <ymax>{{ object.ymax }}</ymax>
        </bndbox>
    </object>
{% endfor %}</annotation>
"""


class Writer:
    def __init__(
        self,
        path: str | Path,
        width: int,
        height: int,
        depth: int = 3,
        database: str = "Unknown",
        segmented: int = 0,
    ):
        self.annotation_template: Template = Template(annotation_template)

        path = Path(path)

        self.template_parameters = {
            "path": path.resolve(),
            "filename": path.name,
            "folder": path.parent.name,
            "width": width,
            "height": height,
            "depth": depth,
            "database": database,
            "segmented": segmented,
            "objects": [],
        }

    def addObject(
        self,
        name: str,
        xmin: int,
        ymin: int,
        xmax: int,
        ymax: int,
        pose: str = "Unspecified",
        truncated: int = 0,
        difficult: int = 0,
    ):
        self.template_parameters["objects"].append(
            {
                "name": name,
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax,
                "pose": pose,
                "truncated": truncated,
                "difficult": difficult,
            }
        )

    def save(self, annotation_path: str | Path):
        content = self.annotation_template.render(**self.template_parameters)
        with open(annotation_path, "w", encoding="utf-8") as file:
            file.write(content)


def yolo2voc(
    txt_dirs: str | Path | list[str | Path],
    image_dirs: str | Path | list[str | Path],
    new_xml_dir: str | Path,
    id2name: dict[int, str],
    new_image_dir: str | Path = None,
) -> None:
    """Convert YOLO to VOC

    Args:
        txt_dirs (str | Path | list[str | Path]): 已有 YOLO 格式的 txt 文件的目录
        image_dirs (str | Path | list[str | Path]): 已有图片目录
        new_xml_dir (str | Path): 新的 VOC 格式的 xml 文件目录
        id2name (dict[int, str]): 类别 ID 到名称的映射字典, 只转换存在于 id2name 中的类别
        new_image_dir (str | Path, optional): 新的图片目录, 如果为 None 则不复制图片. Defaults to None.
    """
    print(
        "Converting YOLO to VOC...\n"
        f"txt_dirs: {txt_dirs}\n"
        f"image_dirs: {image_dirs}\n"
        f"new_xml_dir: {new_xml_dir}\n"
        f"id2name: {id2name}\n"
        f"new_image_dir: {new_image_dir}"
    )

    txt_dirs = [txt_dirs] if isinstance(txt_dirs, (str, Path)) else txt_dirs
    txt_dirs = [Path(xml_dir) for xml_dir in txt_dirs]
    image_dirs = [image_dirs] if isinstance(image_dirs, (str, Path)) else image_dirs
    image_dirs = [Path(xml_dir) for xml_dir in image_dirs]

    assert len(txt_dirs) == len(image_dirs)

    txt_paths = []
    image_paths = []
    for xml_dir, image_dir in zip(txt_dirs, image_dirs):
        if not xml_dir.exists():
            raise FileNotFoundError(f"txt_dir not exists: {xml_dir}")
        if not image_dir.exists():
            raise FileNotFoundError(f"image_dir not exists: {image_dir}")
        _xml_paths = list(xml_dir.glob("*.txt"))
        txt_paths.extend(_xml_paths)
        image_paths.extend([get_image_path(image_dir, i.stem) for i in _xml_paths])

    new_image_dir = Path(new_image_dir) if new_image_dir is not None else None
    if new_image_dir is not None:
        new_image_dir.mkdir(exist_ok=True, parents=True)

    new_xml_dir = Path(new_xml_dir)
    new_xml_dir.mkdir(exist_ok=True, parents=True)

    txt_path: Path
    image_path: Path
    for txt_path, image_path in tqdm(zip(txt_paths, image_paths), desc="convert txt to xml"):
        try:
            txt_stem = txt_path.stem

            class_exists = False
            lines = []
            with open(txt_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    _line = line.rstrip().split(" ")
                    if len(_line) != 5:
                        continue
                    _id = int(_line[0])
                    if _id not in id2name:
                        continue
                    lines.append(_line)
                    class_exists = True

            if not class_exists:
                continue

            if new_image_dir is not None:
                new_image_path = new_image_dir / image_path.name
                copy(image_path, new_image_path)

            w, h = Image.open(image_path).size
            xml_path = new_xml_dir / f"{txt_stem}.xml"
            writer = Writer(xml_path, w, h)
            for line in lines:
                label, x_center, y_center, width, height = line
                _id = int(label)
                if _id not in id2name:
                    continue
                x_min = round(w * max(float(x_center) - float(width) / 2, 0))
                x_max = round(w * min(float(x_center) + float(width) / 2, 1))
                y_min = round(h * max(float(y_center) - float(height) / 2, 0))
                y_max = round(h * min(float(y_center) + float(height) / 2, 1))
                writer.addObject(id2name[_id], x_min, y_min, x_max, y_max)
            writer.save(xml_path)
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")


if __name__ == "__main__":
    # 原本的 txt 文件夹
    txt_dirs = [
        "../VOC/labels/test2007",
    ]
    # 原本图片文件夹
    image_dirs = [
        "../VOC/images/test2007",
    ]
    # 新的 xml 文件夹
    new_xml_dir = "../VOC/xmls/test2007-1"
    # yaml 配置路径
    yaml_path = "../VOC/VOC.yaml"
    id2name = load_id2name_from_yaml(yaml_path)
    # 新的图片文件夹, 如果为 None 则不复制图片
    new_image_dir = None

    yolo2voc(txt_dirs, image_dirs, new_xml_dir, id2name, new_image_dir)
