"""Sample yolo dataset"""

import random
from pathlib import Path
from shutil import copy
import traceback
from tqdm import tqdm
import yaml
from collections import Counter
from functions import (
    get_image_path,
)


def sample_yolo(
    txt_dirs: str | Path | list[str | Path],
    image_dirs: str | Path | list[str | Path],
    sample_dir: str | Path = "output",
    val_percent: float = 0.1,
    object_min_num: int = 10,
    seed: int | None = None,
) -> None:
    """Filter YOLO dataset by keep_ids

    Args:
        txt_dirs (str | Path | list[str | Path]): 已有 YOLO 格式的 txt 文件的目录
        image_dirs (str | Path | list[str | Path]): 图片文件目录
        sample_dir (str | Path, optional): 采样结果保存目录. Defaults to "output".
        val_percent (float, optional): 验证集占比. Defaults to 0.1.
        object_min_num (int, optional): 最少的物体数量. Defaults to 10.
        seed (int | None, optional): 随机种子. Defaults to None.
    """
    assert 0 < val_percent < 1, (
        f"val_percent should be between 0 and 1, but got {val_percent}"
    )

    print(
        "Sample YOLO dataset...\n"
        f"txt_dirs: {txt_dirs}\n"
        f"image_dirs: {image_dirs}\n"
        f"sample_dir: {sample_dir}\n"
        f"val_percent: {val_percent}\n"
        f"object_min_num: {object_min_num}\n"
        f"seed: {seed}"
    )

    if seed is not None:
        random.seed(seed)

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

    sample_dir = Path(sample_dir)
    val_image_dir = sample_dir / "val" / "images"
    val_image_dir.mkdir(parents=True, exist_ok=True)
    val_label_dir = sample_dir / "val" / "labels"
    val_label_dir.mkdir(parents=True, exist_ok=True)
    train_image_dir = sample_dir / "train" / "images"
    train_image_dir.mkdir(parents=True, exist_ok=True)
    train_label_dir = sample_dir / "train" / "labels"
    train_label_dir.mkdir(parents=True, exist_ok=True)

    print(f"Save val images to {val_image_dir}")
    print(f"Save val txts to {val_label_dir}")
    print(f"Save train images to {train_image_dir}")
    print(f"Save train txts to {train_label_dir}")

    total_num = len(txt_paths)
    val_num = round(total_num * val_percent)

    i = 1
    while True:
        print(f"sample iteration {i} ...")
        i += 1

        val_ids = random.sample(range(total_num), val_num)
        val_txt_paths = [txt_paths[i] for i in val_ids]
        val_image_paths = [image_paths[i] for i in val_ids]
        train_txt_paths = [txt_paths[i] for i in range(total_num) if i not in val_ids]
        train_image_paths = [
            image_paths[i] for i in range(total_num) if i not in val_ids
        ]

        # ------------------ val ------------------ #
        j = 0
        val_ids = []
        for txt_path in tqdm(val_txt_paths, desc="check val txt files"):
            try:
                with open(txt_path, "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        _line = line.rstrip().split(" ")
                        if len(_line) != 5:
                            continue
                        j += 1
                        val_ids.append(int(_line[0]))

            except Exception:
                print(f"Error: {traceback.format_exc()}")

        print(f"val total {len(val_txt_paths)} txt files, {len(val_ids)} objects")
        val_counters = dict(sorted(Counter(val_ids).items(), key=lambda x: x[0]))
        print("val object counts:")
        for _id, count in val_counters.items():
            print(f"    {_id}: {count}")
        # ------------------ val ------------------ #

        # ------------------ train ------------------ #
        k = 0
        train_ids = []
        for txt_path in tqdm(train_txt_paths, desc="check val txt files"):
            try:
                with open(txt_path, "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        _line = line.rstrip().split(" ")
                        if len(_line) != 5:
                            continue
                        k += 1
                        train_ids.append(int(_line[0]))

            except Exception:
                print(f"Error: {traceback.format_exc()}")

        print(f"train total {len(train_txt_paths)} txt files, {len(train_ids)} objects")
        train_counters = dict(sorted(Counter(train_ids).items(), key=lambda x: x[0]))
        print("train object counts:")
        for _id, count in train_counters.items():
            print(f"    {_id}: {count}")
        # ------------------ train ------------------ #

        min_num = min(min(val_counters.values()), min(train_counters.values()))
        unqiue_val_ids = set(val_ids)
        unqiue_train_ids = set(train_ids)
        if (
            seed is not None
            or i > 100
            or (
                len(unqiue_val_ids ^ unqiue_train_ids) == 0
                and min_num >= object_min_num
            )
        ):
            break

        print()

    data = {
        "path": str(sample_dir.name),
        "train": ["train/images"],
        "val": ["val/images"],
        "names": {i: name for i, name in enumerate(sorted(unqiue_val_ids))},
        "statistics": {
            "train": {
                "files": len(train_txt_paths),
                "objects": k,
                "objects_per_class": train_counters,
            },
            "val": {
                "files": len(val_txt_paths),
                "objects": j,
                "objects_per_class": val_counters,
            },
        },
    }
    new_yaml_path = sample_dir / "data.yaml"
    with open(new_yaml_path, mode="w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"save yaml config to {new_yaml_path}")

    txt_path: Path
    image_path: Path
    for txt_path, image_path in tqdm(
        zip(val_txt_paths, val_image_paths),
        desc="move val txt and image files",
        total=len(val_txt_paths),
    ):
        try:
            new_image_path = val_image_dir / image_path.name
            copy(image_path, new_image_path)
            new_txt_path = val_label_dir / txt_path.name
            copy(txt_path, new_txt_path)
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")

    for txt_path, image_path in tqdm(
        zip(train_txt_paths, train_image_paths),
        desc="move train txt and image files",
        total=len(train_txt_paths),
    ):
        try:
            new_image_path = train_image_dir / image_path.name
            copy(image_path, new_image_path)
            new_txt_path = train_label_dir / txt_path.name
            copy(txt_path, new_txt_path)
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")


if __name__ == "__main__":
    # 原本 txt 文件路径
    txt_dirs = [
        "../VOC/labels/test2007",
    ]
    # 原本图片文件路径
    image_dirs = [
        "../VOC/images/test2007",
    ]
    # 采样后的路径, 包含 train 和 val 两个文件夹, 以及对应的 txts 和 images 文件夹, 用来存放全部采样后的数据
    sample_dir = "../VOC/test2007--sample--yolo"
    # 验证集占比
    val_percent = 0.1
    # 划分数据集时每个类别的最小数量, 如果数据集太少不一定能保证, 需要调整这个值
    object_min_num = 10
    # 随机种子, 保证可以复现, None 代表不设置
    seed = 0

    sample_yolo(txt_dirs, image_dirs, sample_dir, val_percent, object_min_num, seed)
