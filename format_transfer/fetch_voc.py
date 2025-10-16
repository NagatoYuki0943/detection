"""Fetch voc dataset"""

from pathlib import Path
import traceback
from xml.etree import ElementTree
from tqdm import tqdm
from collections import Counter
from functions import save_names_to_yaml


def filter_voc(
    xml_dirs: str | Path | list[str | Path], output_yaml_path: str | Path | None = None
) -> None:
    """Fetch VOC dataset

    Args:
        xml_dirs (str | Path | list[str | Path): VOC 格式的 xml 文件目录, 支持多个目录
        output_yaml_path: 输出的 yaml 文件路径, 默认为 None, 不输出 yaml 文件
    """
    print(f"Fetch VOC ...\nxml_dirs: {xml_dirs}\noutput_yaml_path: {output_yaml_path}")

    xml_dirs = [xml_dirs] if isinstance(xml_dirs, (str, Path)) else xml_dirs
    xml_dirs = [Path(xml_dir) for xml_dir in xml_dirs]

    xml_paths = []
    for xml_dir in xml_dirs:
        if not xml_dir.exists():
            raise FileNotFoundError(f"xml_dir not exists: {xml_dir}")
        xml_paths.extend(xml_dir.glob("*.xml"))

    names = []
    for xml_path in tqdm(xml_paths, desc="check val xml files"):
        try:
            with open(xml_path, "r", encoding="utf-8") as in_file:
                tree = ElementTree.parse(in_file)
            root = tree.getroot()

            objs = tree.findall("object")
            for obj in objs:
                root.remove(obj)
                name = obj.find("name").text
                names.append(name)

        except Exception:
            print(f"Error: {traceback.format_exc()}")

    print(f"total {len(xml_paths)} xml files, {len(names)} objects")
    counters = dict(sorted(Counter(names).items(), key=lambda x: x[0]))
    print("object counts:")
    for name, count in counters.items():
        print(f"    {name}: {count}")

    if output_yaml_path is not None:
        output_yaml_path = Path(output_yaml_path)
        save_names_to_yaml(output_yaml_path, list(counters))
        print(f"save yaml file to: {output_yaml_path}")


if __name__ == "__main__":
    # xml 文件所在的目录, 支持多个目录
    xml_dirs = [
        "../VOC/xmls/test2007",
    ]
    # 生成的类别 yaml 文件
    output_yaml_path = "../VOC/data.yaml"

    filter_voc(xml_dirs, output_yaml_path)
