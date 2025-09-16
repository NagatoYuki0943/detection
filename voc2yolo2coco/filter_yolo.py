"""Filter dataset
"""

from pathlib import Path
from shutil import copy
import traceback
from tqdm import tqdm
from functions import get_image_path


def filter_yolo(
    txt_dir: str | Path,
    image_dir: str | Path,
    new_txt_dir: str | Path,
    new_image_dir: str | Path,
    ids: dict[int, str],
) -> None:
    """Filter YOLO dataset by ids

    Args:
        txt_dir (str | Path): 已有 YOLO 格式的 txt 文件的目录
        image_dir (str | Path): 已有图片目录
        new_txt_dir (str | Path): 新的 YOLO 格式的 txt 文件的目录
        new_image_dir (str | Path, optional): 新的图片目录
        ids (list[int]): 需要保留的类别 id list
    """
    print(
        "Filter YOLO dataset by ids...\n"
        f"txt_dir: {txt_dir}\n"
        f"image_dir: {image_dir}\n"
        f"ew_txt_dir: {new_txt_dir}\n"
        f"ew_image_dir: {new_image_dir}\n"
        f"ids: {ids}"
    )

    txt_dir = Path(txt_dir)
    assert txt_dir.exists()
    image_dir = Path(image_dir)
    assert image_dir.exists()

    new_txt_dir = Path(new_txt_dir)
    new_txt_dir.mkdir(exist_ok=True, parents=True)
    new_image_dir = Path(new_image_dir)
    new_image_dir.mkdir(exist_ok=True, parents=True)

    for txt_file in tqdm(list(txt_dir.glob("*.txt"))):
        try:
            image_path = get_image_path(image_dir, txt_file.stem)

            class_exists = False
            lines = []
            with open(txt_file) as f:
                for line in f.readlines():
                    _line = line.rstrip().split(" ")
                    if len(_line) != 5:
                        continue
                    _id = int(_line[0])
                    if _id not in ids:
                        continue
                    lines.append(_line)
                    class_exists = True

            if not class_exists:
                continue

            new_txt_file = new_txt_dir / txt_file.name
            with open(new_txt_file, "w") as f:
                for line in lines:
                    f.write(" ".join(line) + "\n")

            new_image_path = new_image_dir / image_path.name
            copy(image_path, new_image_path)
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")


if __name__ == "__main__":
    from config import voc_id2name, coco_id2name

    txt_dir = "../voc/labels/test2007"
    image_dir = "../voc/images/test2007"
    new_txt_dir = "../voc/labels/test2007-2"
    new_image_dir = "../voc/images/test2007-2"

    # 复制前一半类别
    i = 0
    ids = []
    original_half_len = len(voc_id2name) // 2
    for key in voc_id2name:
        ids.append(key)
        i += 1
        if i >= original_half_len:
            break

    filter_yolo(txt_dir, image_dir, new_txt_dir, new_image_dir, ids)
