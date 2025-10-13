"""Filter dataset"""

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
    keep_ids: dict[int, str],
    id_remap: dict[int, int] | None = None,
) -> None:
    """Filter YOLO dataset by keep_ids

    Args:
        txt_dir (str | Path): 已有 YOLO 格式的 txt 文件的目录
        image_dir (str | Path): 已有图片目录
        new_txt_dir (str | Path): 新的 YOLO 格式的 txt 文件的目录
        new_image_dir (str | Path, optional): 新的图片目录
        keep_ids (list[int]): 需要保留的类别 id list
        id_remap (dict[int, int] | None): 类别 id 映射表, 若为 None, 则不进行映射
    """
    print(
        "Filter YOLO dataset by keep_ids...\n"
        f"txt_dir: {txt_dir}\n"
        f"image_dir: {image_dir}\n"
        f"ew_txt_dir: {new_txt_dir}\n"
        f"ew_image_dir: {new_image_dir}\n"
        f"keep_ids: {keep_ids}\n"
        f"id_remap: {id_remap}"
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
                    if _id not in keep_ids:
                        continue
                    # id 映射
                    new_id = id_remap.get(_id, _id) if id_remap else _id
                    _line = [str(new_id)] + _line[1:]
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

    txt_dir = "../VOC/labels/test2007"
    image_dir = "../VOC/images/test2007"
    new_txt_dir = "../VOC/labels/test2007-2"
    new_image_dir = "../VOC/images/test2007-2"
    id_remap = {k: k for k in voc_id2name}

    # 复制前一半类别
    i = 0
    keep_ids = []
    original_half_len = len(voc_id2name) // 2
    for key in voc_id2name:
        keep_ids.append(key)
        i += 1
        if i >= original_half_len:
            break

    filter_yolo(txt_dir, image_dir, new_txt_dir, new_image_dir, keep_ids)
