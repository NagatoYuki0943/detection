"""Fetch voc dataset"""

from pathlib import Path
import traceback
from xml.etree import ElementTree
from tqdm import tqdm
import yaml
from collections import Counter


def fetch_voc(
    xml_dirs: str | Path | list[str | Path], yaml_path: str | Path | None = None
) -> None:
    """Fetch VOC dataset

    Args:
        xml_dirs (str | Path | list[str | Path): VOC 格式的 xml 文件目录, 支持多个目录
        yaml_path: 输出的 yaml 文件路径, 默认为 None, 不输出 yaml 文件
    """
    print(f"Fetch VOC ...\nxml_dirs: {xml_dirs}\noutput_yaml_path: {yaml_path}")

    xml_dirs = [xml_dirs] if isinstance(xml_dirs, (str, Path)) else xml_dirs
    xml_dirs = [Path(xml_dir) for xml_dir in xml_dirs]

    xml_paths = []
    for xml_dir in xml_dirs:
        if not xml_dir.exists():
            raise FileNotFoundError(f"xml_dir not exists: {xml_dir}")
        xml_paths.extend(xml_dir.glob("*.xml"))

    i = 0
    names = []
    for xml_path in tqdm(xml_paths, desc="check val xml files"):
        try:
            with open(xml_path, "r", encoding="utf-8") as in_file:
                tree = ElementTree.parse(in_file)
            root = tree.getroot()

            objs = tree.findall("object")
            for obj in objs:
                i += 1
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

    if yaml_path is not None:
        yaml_path = Path(yaml_path)
        data = {
            "names": {i: name for i, name in enumerate(counters)},
            "statistics": {
                "total_files": len(xml_paths),
                "total_objects": i,
                "counts": counters,
            },
        }
        with open(yaml_path, mode="w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

        print(f"save yaml config to: {yaml_path}")


if __name__ == "__main__":
    # xml 文件所在的目录, 支持多个目录
    xml_dirs = [
        "../VOC/xmls/test2007",
    ]
    # 生成的类别 yaml 文件
    yaml_path = "../VOC/data.yaml"

    fetch_voc(xml_dirs, yaml_path)
