from pathlib import Path
import yaml


IMAGE_SUFFIX = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp")


def get_image_path(image_dir: str | Path, image_stem: str = ""):
    image_dir = Path(image_dir)
    if not image_dir.is_dir():
        raise NotADirectoryError(f"{image_dir} is not a directory")
    for image_suffix in IMAGE_SUFFIX:
        image_path = image_dir / (image_stem + image_suffix)
        if image_path.is_file():
            return image_path
    raise FileNotFoundError(f"No image {image_stem} file found in {image_dir}")


def read_yaml(yaml_path: str | Path) -> dict | list:
    yaml_path = Path(yaml_path)
    assert yaml_path.is_file(), f"{yaml_path} is not a file"
    with open(yaml_path, mode="r", encoding="utf-8") as f:
        data = yaml.full_load(f)
    return data


def load_id2name_from_yaml(yaml_path: str | Path) -> dict[int, str]:
    data = read_yaml(yaml_path)
    assert isinstance(data.get("names", None), dict), "names should be a dictionary"
    id2name = {i: name for i, name in data["names"].items()}
    return id2name


def load_name2id_from_yaml(yaml_path: str | Path) -> dict[str, int]:
    data = read_yaml(yaml_path)
    assert isinstance(data.get("names", None), dict), "names should be a dictionary"
    name2id = {name: i for i, name in data["names"].items()}
    return name2id


def load_ids_from_yaml(yaml_path: str | Path) -> list[int]:
    data = read_yaml(yaml_path)
    assert isinstance(data.get("names", None), dict), "names should be a dictionary"
    ids = [i for i in data["names"]]
    return ids


def load_names_from_yaml(yaml_path: str | Path) -> list[str]:
    data = read_yaml(yaml_path)
    assert isinstance(data.get("names", None), dict), "names should be a dictionary"
    names = [name for name in data["names"].values()]
    return names


def save_names_to_yaml(yaml_path: str | Path, names: list[str]):
    data = {"names": {i: name for i, name in enumerate(names)}}
    with open(yaml_path, mode="w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)


def save_id2names_and_path_to_yaml(
    yaml_path: str | Path,
    id2names: dict[int, str],
    path: str | Path = None,
    train_paths: list[str | Path] | str | Path = None,
    val_paths: list[str | Path] | str | Path = None,
):
    data = {}
    if path is not None:
        data["path"] = str(path)
    if train_paths is not None:
        train_paths = (
            train_paths
            if isinstance(train_paths, (list, tuple, set))
            else [train_paths]
        )
        data["train"] = [str(path) for path in train_paths]
    if val_paths is not None:
        val_paths = (
            val_paths if isinstance(val_paths, (list, tuple, set)) else [val_paths]
        )
        data["val"] = [str(path) for path in val_paths]
    data["names"] = id2names
    with open(yaml_path, mode="w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
