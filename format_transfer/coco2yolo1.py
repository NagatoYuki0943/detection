from ultralytics.data.converter import convert_coco


convert_coco(
    "../coco/annotations/",
    "../coco_converted_yolo/",
    False,
    False,
    True,
    False,
)
