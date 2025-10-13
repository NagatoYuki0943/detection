from pathlib import Path


IMAGE_SUFFIX = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp")


def get_image_path(image_dir: str | Path, image_stem: str = ""):
    image_dir = Path(image_dir)
    if not image_dir.is_dir():
        raise NotADirectoryError(f"{image_dir} is not a directory")
    for image_suffix in IMAGE_SUFFIX:
        image_path = image_dir / (image_stem + image_suffix)
        if image_path.is_file():
            return image_path
    raise FileNotFoundError(f"No image file found in {image_dir}")
