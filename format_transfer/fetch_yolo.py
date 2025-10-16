"""Fetch yolo dataset"""

from pathlib import Path
import traceback
from tqdm import tqdm
from collections import Counter


def filter_yolo(
    txt_dirs: str | Path | list[str | Path],
) -> None:
    """Filter YOLO dataset by keep_ids

    Args:
        txt_dirs (str | Path | list[str | Path): 已有 YOLO 格式的 txt 文件的目录
        image_dir (str | Path): 已有图片目录
        new_txt_dir (str | Path): 新的 YOLO 格式的 txt 文件的目录
        new_image_dir (str | Path, optional): 新的图片目录
        keep_ids (list[int]): 需要保留的类别 id list
        id_remap (dict[int, int] | None): 类别 id 映射表, 若为 None, 则不进行映射
    """
    print(f"Filter YOLO dataset by keep_ids...\ntxt_dirs: {txt_dirs}")

    txt_dirs = [txt_dirs] if isinstance(txt_dirs, (str, Path)) else txt_dirs
    txt_dirs = [Path(xml_dir) for xml_dir in txt_dirs]

    txt_paths = []
    for txt_dir in txt_dirs:
        if not txt_dir.exists():
            raise FileNotFoundError(f"txt_dir not exists: {txt_dir}")
        txt_paths.extend(txt_dir.glob("*.txt"))

    ids = []
    for txt_path in tqdm(txt_paths, desc="check val txt files"):
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    _line = line.rstrip().split(" ")
                    if len(_line) != 5:
                        continue
                    ids.append(int(_line[0]))

        except Exception:
            print(f"Error: {traceback.format_exc()}")

    print(f"total {len(txt_paths)} txt files, {len(ids)} objects")
    counters = dict(sorted(Counter(ids).items(), key=lambda x: x[0]))
    print("object counts:")
    for _id, count in counters.items():
        print(f"    {_id}: {count}")


if __name__ == "__main__":
    # txt 文件所在目录, 支持多个目录
    txt_dirs = [
        "../VOC/labels/test2007",
    ]

    filter_yolo(txt_dirs)
