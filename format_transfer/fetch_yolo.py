"""Fetch yolo dataset"""

from pathlib import Path
import traceback
from tqdm import tqdm
import yaml
from collections import Counter


def fetch_yolo(
    txt_dirs: str | Path | list[str | Path], yaml_path: str | Path | None = None
) -> None:
    """Fetch YOLO dataset by keep_ids

    Args:
        txt_dirs (str | Path | list[str | Path): 已有 YOLO 格式的 txt 文件的目录
        yaml_path: 输出的 yaml 文件路径, 默认为 None, 不输出 yaml 文件
    """
    print(f"Fetch VOC ...\nxml_dirs: {txt_dirs}\noutput_yaml_path: {yaml_path}")

    txt_dirs = [txt_dirs] if isinstance(txt_dirs, (str, Path)) else txt_dirs
    txt_dirs = [Path(xml_dir) for xml_dir in txt_dirs]

    txt_paths = []
    for txt_dir in txt_dirs:
        if not txt_dir.exists():
            raise FileNotFoundError(f"txt_dir not exists: {txt_dir}")
        txt_paths.extend(txt_dir.glob("*.txt"))

    i = 0
    ids = []
    for txt_path in tqdm(txt_paths, desc="check val txt files"):
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    _line = line.rstrip().split(" ")
                    if len(_line) != 5:
                        continue
                    i += 1
                    ids.append(int(_line[0]))

        except Exception:
            print(f"Error: {traceback.format_exc()}")

    print(f"total {len(txt_paths)} txt files, {len(ids)} objects")
    counters = dict(sorted(Counter(ids).items(), key=lambda x: x[0]))
    print("object counts:")
    for _id, count in counters.items():
        print(f"    {_id}: {count}")

    if yaml_path is not None:
        yaml_path = Path(yaml_path)
        data = {
            "names": {i: name for i, name in enumerate(counters)},
            "statistics": {
                "total_files": len(txt_paths),
                "total_objects": i,
                "counts": counters,
            },
        }
        with open(yaml_path, mode="w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

        print(f"save yaml config to: {yaml_path}")


if __name__ == "__main__":
    # txt 文件所在目录, 支持多个目录
    txt_dirs = [
        "../VOC/labels/test2007",
    ]
    # 生成的类别 yaml 文件
    yaml_path = "../VOC/data.yaml"

    fetch_yolo(txt_dirs, yaml_path)
