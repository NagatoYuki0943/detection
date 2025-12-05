import json
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm


def write_txt(save_path: str | Path, image_info: dict, objects: list[dict]):
    """生成并保存 yolo 格式的 txt 文件

    Args:
        save_path (str | Path): txt 文件保存路径
        image_info (dict): 包含图片信息的字典
        objects (list[dict]): 包含物体信息的列表，每个元素是一个字典，包含 "name", "xmin", "ymin", "xmax", "ymax" 五个键值
    """

    width = image_info["width"]
    height = image_info["height"]

    str_list = []
    # Objects
    for obj in objects:
        _id = obj["cat_id"]
        xmin = obj["xmin"]
        ymin = obj["ymin"]
        xmax = obj["xmax"]
        ymax = obj["ymax"]
        cx = (xmin + xmax) / 2 / width
        cy = (ymin + ymax) / 2 / height
        w = (xmax - xmin) / width
        h = (ymax - ymin) / height
        str_list.append(f"{_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

    # Save txt file
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("\n".join(str_list))


def coco91_to_coco80_class() -> list[int]:
    """Convert 91-index COCO class IDs to 80-index COCO class IDs.

    Returns:
        (list[int]): A list of 91 class IDs where the index represents the 80-index class ID and the value is the
            corresponding 91-index class ID.
    """
    return [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        None,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        None,
        24,
        25,
        None,
        None,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        None,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        None,
        60,
        None,
        None,
        61,
        None,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        None,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        None,
    ]


def coco80_to_coco91_class() -> list[int]:
    r"""Convert 80-index (val2014) to 91-index (paper).

    Returns:
        (list[int]): A list of 80 class IDs where each value is the corresponding 91-index class ID.

    Examples:
        >>> import numpy as np
        >>> a = np.loadtxt("data/coco.names", dtype="str", delimiter="\n")
        >>> b = np.loadtxt("data/coco_paper.names", dtype="str", delimiter="\n")

        Convert the darknet to COCO format
        >>> x1 = [list(a[i] == b).index(True) + 1 for i in range(80)]

        Convert the COCO to darknet format
        >>> x2 = [list(b[i] == a).index(True) if any(b[i] == a) else None for i in range(91)]

    References:
        https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/
    """
    return [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        27,
        28,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
        63,
        64,
        65,
        67,
        70,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        84,
        85,
        86,
        87,
        88,
        89,
        90,
    ]


def coco2yolo(
    json_file: str | Path,
    save_dir: str | Path,
    cls91to80: bool = False,
    ignore_crowd: bool = True,
):
    """
    将 COCO JSON 标注转换为 YOLO TXT 格式。

    Args:
        json_file (str | Path): COCO 格式的 JSON 文件路径
        save_dir (str | Path): TXT 保存目录
        cls91to80 (bool): 是否将 91-index 类别 ID 转换为 80-index 类别 ID, 默认为 False
        ignore_crowd (bool): 是否忽略 iscrowd=1 的标注，默认忽略
    """
    print(
        "Converting COCO to...\n"
        f"json_file: {json_file}\n"
        f"save_dir: {save_dir}"
    )

    json_path = Path(json_file)
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading COCO annotations from {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 构建 image_id 到 image info 的映射
    images_dict = {img["id"]: img for img in data["images"]}

    # 2. 构建 image_id 到 annotations 的映射
    annotations_dict = defaultdict(list)
    for ann in data["annotations"]:
        annotations_dict[ann["image_id"]].append(ann)

    print(f"Converting to VOC format into {save_dir}...")

    coco80 = coco91_to_coco80_class()

    # 遍历所有图片进行转换
    for img_id, img_info in tqdm(images_dict.items(), desc="Converting"):
        filename = img_info["file_name"]

        # 对应的 txt 文件名
        txt_filename = Path(filename).with_suffix(".txt").name
        save_path = save_dir / txt_filename

        # 获取该图片下的所有标注
        anns = annotations_dict.get(img_id, [])
        objects = []

        for ann in anns:
            # 过滤掉 iscrowd 标注 (通常用于实例分割中的密集人群，不做目标检测训练)
            if ignore_crowd and ann.get("iscrowd", 0) == 1:
                continue

            cat_id = ann["category_id"]
            if cls91to80:
                # 之所以要 coco 的 id 是从 1 开始的
                cat_id = coco80[cat_id - 1]

            # COCO bbox 格式: [x_min, y_min, width, height]
            bbox = ann["bbox"]
            x_min, y_min, w, h = bbox

            # VOC bbox 格式: [x_min, y_min, x_max, y_max]
            x_max = x_min + w
            y_max = y_min + h

            # 简单的越界修正（虽然 COCO 通常是准的）
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(img_info["width"], x_max)
            y_max = min(img_info["height"], y_max)

            objects.append(
                {
                    "cat_id": cat_id,
                    "xmin": x_min,
                    "ymin": y_min,
                    "xmax": x_max,
                    "ymax": y_max,
                }
            )

        # 即使没有物体（objects为空），有些场景也需要生成空的 xml，或者选择跳过
        # 这里选择：只有当有有效物体时才写入，或者图片本身在 JSON 里
        write_txt(save_path, img_info, objects)

    print(f"Conversion completed. XMLs saved to {save_dir}")


if __name__ == "__main__":
    # 1. COCO JSON 文件路径
    coco_json_path = "../coco/annotations/instances_val2017.json"

    # 2. XML 保存路径
    txt_save_path = "../coco_converted_yolo/labels/val2017-1"

    coco2yolo(coco_json_path, txt_save_path, True)
