"""Filter yolo dataset"""

from pathlib import Path
from shutil import copy
import traceback
import yaml
from tqdm import tqdm
from collections import Counter
from functions import get_image_path, load_id2name_from_yaml


def filter_yolo(
    txt_dirs: str | Path | list[str | Path],
    image_dirs: str | Path | list[str | Path],
    filtered_save_dir: str | Path,
    keep_ids: list[int],
    id_remap: dict[int, int] | None = None,
) -> None:
    """Filter YOLO dataset by keep_ids

    Args:
        txt_dirs (str | Path | list[str | Path]): 已有 YOLO 格式的 txt 文件的目录
        image_dirs (str | Path | list[str | Path]): 已有图片目录
        filtered_save_dir (str | Path): 过滤后的 YOLO 格式的 txt 文件和图片存放目录, 里面会有 txts 和 images 文件夹
        keep_ids (list[int]): 需要保留的类别 id list
        id_remap (dict[int, int] | None): 类别 id 映射表, 若为 None, 则不进行映射
    """
    print(
        "Filter YOLO dataset by keep_ids...\n"
        f"txt_dirs: {txt_dirs}\n"
        f"image_dirs: {image_dirs}\n"
        f"filtered_save_dir: {filtered_save_dir}\n"
        f"keep_ids: {keep_ids}\n"
        f"id_remap: {id_remap}"
    )

    assert len(keep_ids) > 0

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

    filtered_save_dir = Path(filtered_save_dir)
    new_txt_dir = filtered_save_dir / "txts"
    new_txt_dir.mkdir(exist_ok=True, parents=True)
    new_image_dir = filtered_save_dir / "images"
    new_image_dir.mkdir(exist_ok=True, parents=True)
    new_yaml_path = filtered_save_dir / "data.yaml"

    if id_remap:
        new_ids = [id_remap.get(i, i) for i in keep_ids]
    else:
        new_ids = keep_ids
    new_names = sorted([id2name[i] for i in new_ids])
    data = {
        "names": {i: name for i, name in enumerate(new_names)},
    }

    i = 0
    j = 0
    new_ids = []
    txt_path: Path
    image_path: Path
    for txt_path, image_path in tqdm(
        zip(txt_paths, image_paths), desc="filter txt files", total=len(txt_paths)
    ):
        try:
            class_exists = False
            lines = []
            with open(txt_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    _line = line.rstrip().split(" ")
                    if len(_line) != 5:
                        continue
                    j += 1
                    _id = int(_line[0])
                    if _id not in keep_ids:
                        continue
                    # id 映射
                    new_id = id_remap.get(_id, _id) if id_remap else _id
                    new_ids.append(new_id)
                    _line = [str(new_id)] + _line[1:]
                    lines.append(_line)
                    class_exists = True

            if not class_exists:
                continue

            new_txt_path = new_txt_dir / txt_path.name
            with open(new_txt_path, "w", encoding="utf-8") as f:
                for line in lines:
                    f.write(" ".join(line) + "\n")

            new_image_path = new_image_dir / image_path.name
            copy(image_path, new_image_path)

            i += 1
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception:
            print(f"Error: {traceback.format_exc()}")

    print(
        f"total {len(txt_paths)} txt files, total {j} objects, filtered {i} txt files, filtered {len(new_ids)} objects."
    )
    counters = dict(sorted(Counter(new_ids).items(), key=lambda x: x[0]))
    print("object counts:")
    for _id, count in counters.items():
        print(f"    {_id}: {count}")

    data.update(
        {
            "statistics": {
                "total_files": len(txt_paths),
                "total_objects": j,
                "filtered_files": i,
                "filtered_objects": len(new_ids),
                "filtered_counts": counters,
            }
        }
    )
    with open(new_yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"save yaml config to {new_yaml_path}")


if __name__ == "__main__":
    # 原本 txt 文件路径, 支持多个目录
    txt_dirs = [
        "../VOC/labels/test2007",
    ]
    # 原本图片文件路径, 支持多个目录, 但是要和 txt_dirs 一一匹配
    image_dirs = [
        "../VOC/images/test2007",
    ]
    # 过滤后的 xmls 和 images 的存放路径, 里面会有 xmls 和 images 文件夹, 用来存放全部过滤后的数据
    filtered_save_dir = "../VOC/test2007--filtered--yolo-format"
    # 对应的 yaml 文件路径(不是必须, 当前主要目的是获取类别名称)
    yaml_path = "../VOC/VOC.yaml"

    id2name = load_id2name_from_yaml(yaml_path)
    ids = sorted(id2name.keys())

    # 保留的类别 id, 这里保留前一半类别
    keep_ids = ids[: len(ids) // 2]

    # id 的重映射
    id_remap = {i: i for i in keep_ids}

    filter_yolo(txt_dirs, image_dirs, filtered_save_dir, keep_ids, id_remap)
