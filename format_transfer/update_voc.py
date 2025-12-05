"""Update voc xml"""

from pathlib import Path
import traceback
import xml.etree.ElementTree as ET
from tqdm import tqdm
import cv2
from functions import get_image_path


def update_voc(
    xml_dirs: str | Path | list[str | Path],
    image_dirs: str | Path | list[str | Path],
    new_xml_dir: str | Path,
) -> None:
    """Update voc xml
    目前会根据图片实际大小更新 xml 中的图片信息

    Args:
        xml_dirs (str | Path | list[str | Path]): 已有 VOC 格式的 xml 文件目录
        image_dirs (str | Path | list[str | Path]): 已有图片目录
        new_xml_dirs (str | Path): 更新后的 xml 文件目录
    """

    print(
        "Update voc xml\n"
        f"xml_dirs: {xml_dirs}\n"
        f"image_dirs: {image_dirs}\n"
        f"new_xml_dir: {new_xml_dir}",
    )

    xml_dirs = [xml_dirs] if isinstance(xml_dirs, (str, Path)) else xml_dirs
    xml_dirs = [Path(xml_dir) for xml_dir in xml_dirs]
    image_dirs = [image_dirs] if isinstance(image_dirs, (str, Path)) else image_dirs
    image_dirs = [Path(xml_dir) for xml_dir in image_dirs]
    new_xml_dir = Path(new_xml_dir)
    new_xml_dir.mkdir(exist_ok=True, parents=True)

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

    xml_path: Path
    image_path: Path
    for xml_path, image_path in tqdm(
        zip(xml_paths, image_paths), desc="filter xml files", total=len(xml_paths)
    ):
        try:
            with open(xml_path, "r", encoding="utf-8") as in_file:
                tree = ET.parse(in_file)

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

            # 自动调整缩进，space="\t" 使用 tab 缩进，或者 space="  " 使用两个空格
            if hasattr(ET, "indent"):
                ET.indent(tree, space="    ", level=0)

            new_xml_path = new_xml_dir / xml_path.name
            tree.write(new_xml_path)

        except Exception:
            print(f"Error: {traceback.format_exc()}")

    print(f"total {len(xml_paths)} xml files.")


if __name__ == "__main__":
    # 原本 xml 文件路径, 支持多个目录
    xml_dirs = [
        "../VOC/xmls/test2007",
    ]
    # 原本图片文件路径, 支持多个目录, 但是要和 xml_dirs 一一匹配
    image_dirs = [
        "../VOC/images/test2007",
    ]
    # 更新后的 xml 文件目录
    new_xml_dir = "../VOC/xmls/test2007-1"

    update_voc(xml_dirs, image_dirs, new_xml_dir)
