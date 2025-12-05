"""Sample voc dataset"""

import random
from pathlib import Path
from shutil import copy
import traceback
import xml.etree.ElementTree as ET
import yaml
from tqdm import tqdm
from collections import Counter
from functions import (
    get_image_path,
)


def sample_voc(
    xml_dirs: str | Path | list[str | Path],
    image_dirs: str | Path | list[str | Path],
    sample_dir: str | Path = "output",
    val_percent: float = 0.1,
    object_min_num: int = 10,
    seed: int | None = None,
) -> None:
    """Sample VOC dataset

    Args:
        xml_dirs (str | Path | list[str | Path]): VOC 格式的 xml 文件目录
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
        "Sample VOC dataset...\n"
        f"xml_dirs: {xml_dirs}\n"
        f"image_dirs: {image_dirs}\n"
        f"sample_dir: {sample_dir}\n"
        f"val_percent: {val_percent}\n"
        f"object_min_num: {object_min_num}\n"
        f"seed: {seed}"
    )

    if seed is not None:
        random.seed(seed)

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

    sample_dir = Path(sample_dir)
    val_image_dir = sample_dir / "val" / "images"
    val_image_dir.mkdir(parents=True, exist_ok=True)
    val_xml_dir = sample_dir / "val" / "xmls"
    val_xml_dir.mkdir(parents=True, exist_ok=True)
    train_image_dir = sample_dir / "train" / "images"
    train_image_dir.mkdir(parents=True, exist_ok=True)
    train_xml_dir = sample_dir / "train" / "xmls"
    train_xml_dir.mkdir(parents=True, exist_ok=True)

    print(f"Save val images to {val_image_dir}")
    print(f"Save val xmls to {val_xml_dir}")
    print(f"Save train images to {train_image_dir}")
    print(f"Save train xmls to {train_xml_dir}")

    total_num = len(xml_paths)
    val_num = round(len(xml_paths) * val_percent)

    i = 1
    while True:
        print(f"sample iteration {i} ...")
        i += 1

        val_ids = random.sample(range(total_num), val_num)
        val_xml_paths = [xml_paths[i] for i in val_ids]
        val_image_paths = [image_paths[i] for i in val_ids]
        train_xml_paths = [xml_paths[i] for i in range(total_num) if i not in val_ids]
        train_image_paths = [
            image_paths[i] for i in range(total_num) if i not in val_ids
        ]

        # ------------------ val ------------------ #
        j = 0
        val_names = []
        for xml_path in tqdm(val_xml_paths, desc="check val xml files"):
            try:
                with open(xml_path, "r", encoding="utf-8") as in_file:
                    tree = ET.parse(in_file)
                root = tree.getroot()

                objs = tree.findall("object")
                for obj in objs:
                    j += 1
                    root.remove(obj)
                    name = obj.find("name").text
                    val_names.append(name)

            except Exception:
                print(f"Error: {traceback.format_exc()}")

        print(f"val total {len(val_xml_paths)} xml files, {len(val_names)} objects")
        val_counters = dict(sorted(Counter(val_names).items(), key=lambda x: x[0]))
        print("val object counts:")
        for name, count in val_counters.items():
            print(f"    {name}: {count}")
        # ------------------ val ------------------ #

        # ------------------ train ------------------ #
        k = 0
        train_names = []
        for xml_path in tqdm(train_xml_paths, desc="check train xml files"):
            try:
                with open(xml_path, "r", encoding="utf-8") as in_file:
                    tree = ET.parse(in_file)
                root = tree.getroot()

                objs = tree.findall("object")
                for obj in objs:
                    k += 1
                    root.remove(obj)
                    name = obj.find("name").text
                    train_names.append(name)

            except Exception:
                print(f"Error: {traceback.format_exc()}")

        print(
            f"train total {len(train_xml_paths)} xml files, {len(train_names)} objects"
        )
        train_counters = dict(sorted(Counter(train_names).items(), key=lambda x: x[0]))
        print("train object counts:")
        for name, count in train_counters.items():
            print(f"    {name}: {count}")
        # ------------------ train ------------------ #

        min_num = min(min(val_counters.values()), min(train_counters.values()))
        unqiue_val_names = set(val_names)
        unqiue_train_names = set(train_names)
        if (
            seed is not None
            or i > 100
            or (
                len(unqiue_val_names ^ unqiue_train_names) == 0
                and min_num >= object_min_num
            )
        ):
            break

        print()

    data = {
        "path": str(sample_dir.name),
        "train": ["train/images"],
        "val": ["val/images"],
        "names": {i: name for i, name in enumerate(sorted(unqiue_val_names))},
        "statistics": {
            "train_files": len(train_xml_paths),
            "train_objects": k,
            "train_counts": train_counters,
            "val_files": len(val_xml_paths),
            "val_objects": j,
            "val_counts": val_counters,
        },
    }
    new_yaml_path = sample_dir / "data.yaml"
    with open(new_yaml_path, mode="w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"save yaml config to {new_yaml_path}")

    xml_path: Path
    image_path: Path
    for xml_path, image_path in tqdm(
        zip(val_xml_paths, val_image_paths),
        desc="move val xml and image files",
        total=len(val_xml_paths),
    ):
        try:
            new_image_path = val_image_dir / image_path.name
            copy(image_path, new_image_path)
            new_xml_path = val_xml_dir / xml_path.name
            copy(xml_path, new_xml_path)
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")

    for xml_path, image_path in tqdm(
        zip(train_xml_paths, train_image_paths),
        desc="move train xml and image files",
        total=len(train_xml_paths),
    ):
        try:
            new_image_path = train_image_dir / image_path.name
            copy(image_path, new_image_path)
            new_xml_path = train_xml_dir / xml_path.name
            copy(xml_path, new_xml_path)
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")


# if __name__ == "__main__":
#     # 原本 xml 文件路径
#     xml_dirs = [
#         "../VOC/xmls/test2007",
#     ]
#     # 原本图片文件路径
#     image_dirs = [
#         "../VOC/images/test2007",
#     ]
#     # 采样后的路径, 包含 train 和 val 两个文件夹, 以及对应的 xmls 和 images 文件夹, 用来存放全部采样后的数据
#     sample_dir = "../VOC/test2007--sample--voc"
#     # 验证集占比
#     val_percent = 0.1
#     # 划分数据集时每个类别的最小数量, 如果数据集太少不一定能保证, 需要调整这个值
#     object_min_num = 10
#     # 随机种子, 保证可以复现, None 代表不设置
#     seed = None

#     sample_voc(xml_dirs, image_dirs, sample_dir, val_percent, object_min_num, seed)

if __name__ == "__main__":
    # 原本 xml 文件路径
    xml_dirs = [
        "C:/ml/code/dataset/CrowdHuman--person--filtered--voc-format/xmls",
        "C:/ml/code/dataset/coco--person--filtered--voc-format/xmls",
        "C:/ml/code/dataset/VOC--person--filtered--voc-format/xmls",
    ]
    # 原本图片文件路径
    image_dirs = [
        "C:/ml/code/dataset/CrowdHuman--person--filtered--voc-format/images",
        "C:/ml/code/dataset/coco--person--filtered--voc-format/images",
        "C:/ml/code/dataset/VOC--person--filtered--voc-format/images",
    ]
    # 采样后的路径, 包含 train 和 val 两个文件夹, 以及对应的 xmls 和 images 文件夹, 用来存放全部采样后的数据
    sample_dir = "C:/ml/code/dataset/person--sample"
    # 验证集占比
    val_percent = 0.1
    # 划分数据集时每个类别的最小数量, 如果数据集太少不一定能保证, 需要调整这个值
    object_min_num = 10
    # 随机种子, 保证可以复现, None 代表不设置
    seed = None

    sample_voc(xml_dirs, image_dirs, sample_dir, val_percent, object_min_num, seed)

