[Ultralytics YOLOv5 - Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/yolov5/)

# 数据集

> 先要把数据集放入dataset中，修改data/目录下的yaml，调整为自己的数据集，需要调整路径，分类数，标签名

> yolo数据集格式(yolov5/v8的coco128和霹雳吧啦Wz的yolo3为例)
>
> txt内容，每一行都是 `3 0.933536 0.486124 0.030408 0.154487`
>
> 是 label 中心横坐标与图像宽度比值 中心纵坐标与图像高度比值 bbox宽度与图像宽度比值 bbox高度与图像宽高比值

```sh
#-------------------------------------------#
# 	yolov5 v8的格式
#-------------------------------------------#
yaml:
    path: ../datasets/coco128   # dataset root dir
    train: images/train         # train images (relative to 'path') 128 images
    val: images/val             # val images (relative to 'path') 128 images
    test: images/test           # test images (optional)

dir:
    datasets
    ├── coco128
        ├── images
        │   ├── train   # 训练图片
        │   ├── val     # 验证图片
        │   └── test    # 测试图片
        └── labels
            ├── train   # 训练标签txt
            ├── val     # 验证标签txt
            └── test    # 测试标签txt

#-------------------------------------------#
# 	yolov5 v8另的一种图片目录格式
#-------------------------------------------#
yaml:
    path: ../datasets/coco128   # dataset root dir
    train: train/images         # train images (relative to 'path')
    val: val/images             # val images (relative to 'path')
    test: test/images           # test images (optional)
dir:
    datasets
    ├── coco128
        ├── train
        │   ├── images  # 训练图片
        │   └── labels  # 训练标签txt
        ├── val
        │   ├── images  # 验证图片
        │   └── labels  # 验证标签txt
        └── test
            ├── images  # 测试图片
            └── labels  # 测试标签txt
```

> `data/class20.yaml`

```yaml
# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
# COCO128 dataset https://www.kaggle.com/ultralytics/coco128 (first 128 images from COCO train2017) by Ultralytics
# Example usage: python train.py --data coco128.yaml
# parent
# ├── yolov5
# └── datasets
#     └── yourname
#         └── images/
#             └── train2017/  存放训练图片
#             └── val2017/    存放验证图片
#         └── labels/
#             └── train2017/  存放训练标签  class x_center y_center width height
#             └── val2017/    存放验证标签


# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
path: ../datasets/classes20  # dataset root dir
train: images/train2017  # train images (relative to 'path') 128 images
val: images/val2017  # val images (relative to 'path') 128 images
test:  # test images (optional)

# Classes
names:
  0: aeroplane
  1: bicycle
  2: bird
  3: boat
  4: bottle
  5: bus
  6: car
  7: cat
  8: chair
  9: cow
  10: diningtable
  11: dog
  12: horse
  13: motorbike
  14: person
  15: pottedplant
  16: sheep
  17: sofa
  18: train
  19: tvmonitor
```

# 模型

# 下载权重

> 将下载好的权重放到`weights/`文件下下

### 预训练模型

| 模型                                                                                                                                            | 尺寸 （像素）   | mAPval 50-95  | mAPval 50     | 推理速度 CPU b1 （ms） | 推理速度 V100 b1 （ms） | 速度 V100 b32 （ms） | 参数量 (M) | FLOPs @640 (B) |
| --------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ------------- | ------------- | ---------------- | ----------------- | ---------------- | ------- | -------------- |
| [YOLOv5n](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n.pt)                                                            | 640       | 28.0          | 45.7          | **45**           | **6.3**           | **0.6**          | **1.9** | **4.5**        |
| [YOLOv5s](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt)                                                            | 640       | 37.4          | 56.8          | 98               | 6.4               | 0.9              | 7.2     | 16.5           |
| [YOLOv5m](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5m.pt)                                                            | 640       | 45.4          | 64.1          | 224              | 8.2               | 1.7              | 21.2    | 49.0           |
| [YOLOv5l](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5l.pt)                                                            | 640       | 49.0          | 67.3          | 430              | 10.1              | 2.7              | 46.5    | 109.1          |
| [YOLOv5x](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5x.pt)                                                            | 640       | 50.7          | 68.9          | 766              | 12.1              | 4.8              | 86.7    | 205.7          |
|                                                                                                                                               |           |               |               |                  |                   |                  |         |                |
| [YOLOv5n6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n6.pt)                                                          | 1280      | 36.0          | 54.4          | 153              | 8.1               | 2.1              | 3.2     | 4.6            |
| [YOLOv5s6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s6.pt)                                                          | 1280      | 44.8          | 63.7          | 385              | 8.2               | 3.6              | 12.6    | 16.8           |
| [YOLOv5m6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5m6.pt)                                                          | 1280      | 51.3          | 69.3          | 887              | 11.1              | 6.8              | 35.7    | 50.0           |
| [YOLOv5l6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5l6.pt)                                                          | 1280      | 53.7          | 71.3          | 1784             | 15.8              | 10.5             | 76.8    | 111.4          |
| [YOLOv5x6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5x6.pt) +[TTA](https://github.com/ultralytics/yolov5/issues/303) | 1280 1536 | 55.0 **55.8** | 72.7 **72.7** | 3136 -           | 26.2 -            | 19.4 -           | 140.7 - | 209.8 -        |

笔记

- 所有模型都使用默认配置，训练 300 epochs。n和s模型使用 [hyp.scratch-low.yaml](https://github.com/ultralytics/yolov5/blob/master/data/hyps/hyp.scratch-low.yaml) ，其他模型都使用 [hyp.scratch-high.yaml](https://github.com/ultralytics/yolov5/blob/master/data/hyps/hyp.scratch-high.yaml) 。
- **mAPval**在单模型单尺度上计算，数据集使用 [COCO val2017](http://cocodataset.org/) 。 复现命令 `python val.py --data coco.yaml --img 640 --conf 0.001 --iou 0.65`
- **推理速度**在 COCO val 图像总体时间上进行平均得到，测试环境使用[AWS p3.2xlarge](https://aws.amazon.com/ec2/instance-types/p3/)实例。 NMS 时间 (大约 1 ms/img) 不包括在内。 复现命令 `python val.py --data coco.yaml --img 640 --task speed --batch 1`
- **TTA** [测试时数据增强](https://github.com/ultralytics/yolov5/issues/303) 包括反射和尺度变换。 复现命令 `python val.py --data coco.yaml --img 1536 --iou 0.7 --augment`

# 显卡训练

> [yolov5——训练策略](https://blog.csdn.net/CharmsLUO/article/details/123577851)

> [Train Custom Data Tutorial ⭐ · Issue #12 · ultralytics/yolov5 (github.com)](https://github.com/ultralytics/yolov5/issues/12)

## 参数说明

```python
# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""
Train a YOLOv5 model on a custom dataset. Models and datasets download automatically from the latest YOLOv5 release.

Usage - Single-GPU training:
    $ python train.py --data coco128.yaml --weights yolov5s.pt --img 640  # from pretrained (recommended)
    $ python train.py --data coco128.yaml --weights '' --cfg yolov5s.yaml --img 640  # from scratch

Usage - Multi-GPU DDP training:
    $ python -m torch.distributed.run --nproc_per_node 4 --master_port 1 train.py --data coco128.yaml --weights yolov5s.pt --img 640 --device 0,1,2,3

Models:     https://github.com/ultralytics/yolov5/tree/master/models
Datasets:   https://github.com/ultralytics/yolov5/tree/master/data
Tutorial:   https://docs.ultralytics.com/yolov5/tutorials/train_custom_data
"""

def parse_opt(known=False):
    """
    Parse command-line arguments for YOLOv5 training, validation, and testing.

    Args:
        known (bool, optional): If True, parses known arguments, ignoring the unknown. Defaults to False.

    Returns:
        (argparse.Namespace): Parsed command-line arguments containing options for YOLOv5 execution.

    Example:
        ```python
        from ultralytics.yolo import parse_opt
        opt = parse_opt()
        print(opt)
        ```

    Links:
        - Models: https://github.com/ultralytics/yolov5/tree/master/models
        - Datasets: https://github.com/ultralytics/yolov5/tree/master/data
        - Tutorial: https://docs.ultralytics.com/yolov5/tutorials/train_custom_data
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str, default=ROOT / "yolov5s.pt", help="initial weights path")
    parser.add_argument("--cfg", type=str, default="", help="model.yaml path")
    parser.add_argument("--data", type=str, default=ROOT / "data/coco128.yaml", help="dataset.yaml path")
    parser.add_argument("--hyp", type=str, default=ROOT / "data/hyps/hyp.scratch-low.yaml", help="hyperparameters path")
    parser.add_argument("--epochs", type=int, default=100, help="total training epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="total batch size for all GPUs, -1 for autobatch")
    parser.add_argument("--imgsz", "--img", "--img-size", type=int, default=640, help="train, val image size (pixels)")
    parser.add_argument("--rect", action="store_true", help="rectangular training")
    parser.add_argument("--resume", nargs="?", const=True, default=False, help="resume most recent training")
    parser.add_argument("--nosave", action="store_true", help="only save final checkpoint")
    parser.add_argument("--noval", action="store_true", help="only validate final epoch")
    parser.add_argument("--noautoanchor", action="store_true", help="disable AutoAnchor")
    parser.add_argument("--noplots", action="store_true", help="save no plot files")
    parser.add_argument("--evolve", type=int, nargs="?", const=300, help="evolve hyperparameters for x generations")
    parser.add_argument(
        "--evolve_population", type=str, default=ROOT / "data/hyps", help="location for loading population"
    )
    parser.add_argument("--resume_evolve", type=str, default=None, help="resume evolve from last generation")
    parser.add_argument("--bucket", type=str, default="", help="gsutil bucket")
    parser.add_argument("--cache", type=str, nargs="?", const="ram", help="image --cache ram/disk")
    parser.add_argument("--image-weights", action="store_true", help="use weighted image selection for training")
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu")
    parser.add_argument("--multi-scale", action="store_true", help="vary img-size +/- 50%%")
    parser.add_argument("--single-cls", action="store_true", help="train multi-class data as single-class")
    parser.add_argument("--optimizer", type=str, choices=["SGD", "Adam", "AdamW"], default="SGD", help="optimizer")
    parser.add_argument("--sync-bn", action="store_true", help="use SyncBatchNorm, only available in DDP mode")
    parser.add_argument("--workers", type=int, default=8, help="max dataloader workers (per RANK in DDP mode)")
    parser.add_argument("--project", default=ROOT / "runs/train", help="save to project/name")
    parser.add_argument("--name", default="exp", help="save to project/name")
    parser.add_argument("--exist-ok", action="store_true", help="existing project/name ok, do not increment")
    parser.add_argument("--quad", action="store_true", help="quad dataloader")
    parser.add_argument("--cos-lr", action="store_true", help="cosine LR scheduler")
    parser.add_argument("--label-smoothing", type=float, default=0.0, help="Label smoothing epsilon")
    parser.add_argument("--patience", type=int, default=100, help="EarlyStopping patience (epochs without improvement)")
    parser.add_argument("--freeze", nargs="+", type=int, default=[0], help="Freeze layers: backbone=10, first3=0 1 2")
    parser.add_argument("--save-period", type=int, default=-1, help="Save checkpoint every x epochs (disabled if < 1)")
    parser.add_argument("--seed", type=int, default=0, help="Global training seed")
    parser.add_argument("--local_rank", type=int, default=-1, help="Automatic DDP Multi-GPU argument, do not modify")

    # Logger arguments
    parser.add_argument("--entity", default=None, help="Entity")
    parser.add_argument("--upload_dataset", nargs="?", const=True, default=False, help='Upload data, "val" option')
    parser.add_argument("--bbox_interval", type=int, default=-1, help="Set bounding-box image logging interval")
    parser.add_argument("--artifact_alias", type=str, default="latest", help="Version of dataset artifact to use")

    # NDJSON logging
    parser.add_argument("--ndjson-console", action="store_true", help="Log ndjson to console")
    parser.add_argument("--ndjson-file", action="store_true", help="Log ndjson to file")

    return parser.parse_known_args()[0] if known else parser.parse_args()
```

> `--rect` 使用长方形训练
>
> Setting "rect"=True allows you to train using rectangular images, not necessarily square ones. This allows for more efficient use of GPU memory as there's less need for padding spatial dimensions.
>
> [Custom input size: letterbox vs resizing · Issue #11350 ](https://github.com/ultralytics/yolov5/issues/11350)
>
> [About the rectangle training · Issue #4819](https://github.com/ultralytics/ultralytics/issues/4819)

> 学习率的调整在 `hyps`中调整
>
> `initial learning rate (SGD=1E-2, Adam=1E-3)`

## 单显卡训练

> `SGD`

```sh
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-low.yaml  --optimizer SGD --cos-lr --device 0 --cfg models/yolov5n.yaml --weights weights/yolov5n.pt --data data/coco128.yaml
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-low.yaml  --optimizer SGD --cos-lr --device 0 --cfg models/yolov5s.yaml --weights weights/yolov5s.pt --data data/coco128.yaml
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-high.yaml --optimizer SGD --cos-lr --device 0 --cfg models/yolov5m.yaml --weights weights/yolov5m.pt --data data/coco128.yaml
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-high.yaml --optimizer SGD --cos-lr --device 0 --cfg models/yolov5l.yaml --weights weights/yolov5l.pt --data data/coco128.yaml
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-high.yaml --optimizer SGD --cos-lr --device 0 --cfg models/yolov5x.yaml --weights weights/yolov5x.pt --data data/coco128.yaml
```

> `Adam` & `AdamW`

```sh
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-low-adam.yaml  --optimizer AdamW --cos-lr --device 0 --cfg models/yolov5n.yaml --weights weights/yolov5n.pt --data data/coco128.yaml
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-low-adam.yaml  --optimizer AdamW --cos-lr --device 0 --cfg models/yolov5s.yaml --weights weights/yolov5s.pt --data data/coco128.yaml
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-high-adam.yaml --optimizer AdamW --cos-lr --device 0 --cfg models/yolov5m.yaml --weights weights/yolov5m.pt --data data/coco128.yaml
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-high-adam.yaml --optimizer AdamW --cos-lr --device 0 --cfg models/yolov5l.yaml --weights weights/yolov5l.pt --data data/coco128.yaml
python train.py --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 --hyp data/hyps/hyp.scratch-high-adam.yaml --optimizer AdamW --cos-lr --device 0 --cfg models/yolov5x.yaml --weights weights/yolov5x.pt --data data/coco128.yaml
```

## 多显卡训练

- -m torch.distributed.launch pytorch启用多线程
- --nproc_per_node=8 8张显卡
- --device 0,1,2,3,4,5,6,7 8张显卡序号

```sh
python -m torch.distributed.launch --nproc_per_node=8 train.py --device 0,1,2,3,4,5,6,7 --sync-bn --img 640 --batch-size -1 --workers 8--epochs 300 --patience 0 \
--hyp data/hyps/hyp.scratch-low.yaml --optimizer SGD --cos-lr --cfg models/yolov5n.yaml --weights weights/yolov5n.pt --data data/coco128.yaml

python -m torch.distributed.launch --nproc_per_node=8 train.py --device 0,1,2,3,4,5,6,7 --sync-bn --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 \
--hyp data/hyps/hyp.scratch-low.yaml --optimizer SGD --cos-lr --cfg models/yolov5s.yaml --weights weights/yolov5s.pt --data data/coco128.yaml

python -m torch.distributed.launch --nproc_per_node=8 train.py --device 0,1,2,3,4,5,6,7 --sync-bn --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 \
--hyp data/hyps/hyp.scratch-high.yaml --optimizer SGD --cos-lr --cfg models/yolov5m.yaml --weights weights/yolov5m.pt --data data/coco128.yaml

python -m torch.distributed.launch --nproc_per_node=8 train.py --device 0,1,2,3,4,5,6,7 --sync-bn --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 \
--hyp data/hyps/hyp.scratch-high.yaml --optimizer SGD --cos-lr --cfg models/yolov5l.yaml --weights weights/yolov5l.pt --data data/coco128.yaml

python -m torch.distributed.launch --nproc_per_node=8 train.py --device 0,1,2,3,4,5,6,7 --sync-bn --img 640 --batch-size -1 --workers 8 --epochs 300 --patience 0 \
--hyp data/hyps/hyp.scratch-high.yaml --optimizer SGD --cos-lr --cfg models/yolov5x.yaml --weights weights/yolov5x.pt --data data/coco128.yaml
```

## **不需要在模型配置中显示更改类别数**

> 会自动将nc调整为数据集的类别数量

```sh
> python train.py --img 640 --batch-size -1 --epochs 300 --hyp data/hyps/hyp.scratch-low.yaml  --optimizer SGD --cos-lr --device 0 --weights weights/yolov5n.pt --cfg models/yolov5n.yaml --data data/classes20.yaml
train: weights=weights/yolov5n.pt, cfg=models/yolov5n.yaml, data=data/classes20.yaml, hyp=data/hyps/hyp.scratch-low.yaml, epochs=300, batch_size=-1, imgsz=640, rect=False, resume=False, nosave=False, noval=False, noautoanchor=False, noplots=False, evolve=None, bucket=, cache=None, image_weights=False, device=0, multi_scale=False, single_cls=False, optimizer=SGD, sync_bn=False, workers=8, project=runs\train, name=exp, exist_ok=False, quad=False, cos_lr=True, label_smoothing=0.0, patience=100, freeze=[0], save_period=-1, seed=0, local_rank=-1, entity=None, upload_dataset=False, bbox_interval=-1, artifact_alias=latest
remote: Enumerating objects: 10, done.
remote: Counting objects: 100% (10/10), done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 10 (delta 1), reused 4 (delta 0), pack-reused 0
Unpacking objects: 100% (10/10), 5.30 KiB | 246.00 KiB/s, done.
From https://github.com/ultralytics/yolov5
   b96f35c..b54fd0a  master     -> origin/master
 * [new branch]      dependabot/github_actions/actions/stale-8 -> origin/dependabot/github_actions/actions/stale-8
github:  YOLOv5 is out of date by 1 commit. Use 'git pull' or 'git clone https://github.com/ultralytics/yolov5' to update.
YOLOv5  v7.0-128-gb96f35c Python-3.10.9 torch-2.0.0+cu118 CUDA:0 (NVIDIA GeForce GTX 1080 Ti, 11264MiB)

hyperparameters: lr0=0.01, lrf=0.01, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, warmup_bias_lr=0.1, box=0.05, cls=0.5, cls_pw=1.0, obj=1.0, obj_pw=1.0, iou_t=0.2, anchor_t=4.0, fl_gamma=0.0, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, mosaic=1.0, mixup=0.0, copy_paste=0.0
ClearML: run 'pip install clearml' to automatically track, visualize and remotely train YOLOv5  in ClearML
Comet: run 'pip install comet_ml' to automatically track and visualize YOLOv5  runs in Comet
TensorBoard: Start with 'tensorboard --logdir runs\train', view at http://localhost:6006/
Overriding model.yaml nc=80 with nc=20 		# 这里自动覆盖了旧的类别数

                 from  n    params  module                                  arguments
  0                -1  1      1760  models.common.Conv                      [3, 16, 6, 2, 2]
  1                -1  1      4672  models.common.Conv                      [16, 32, 3, 2]
  2                -1  1      4800  models.common.C3                        [32, 32, 1]
  3                -1  1     18560  models.common.Conv                      [32, 64, 3, 2]
  4                -1  2     29184  models.common.C3                        [64, 64, 2]
  5                -1  1     73984  models.common.Conv                      [64, 128, 3, 2]
  6                -1  3    156928  models.common.C3                        [128, 128, 3]
  7                -1  1    295424  models.common.Conv                      [128, 256, 3, 2]
  8                -1  1    296448  models.common.C3                        [256, 256, 1]
  9                -1  1    164608  models.common.SPPF                      [256, 256, 5]
 10                -1  1     33024  models.common.Conv                      [256, 128, 1, 1]
 11                -1  1         0  torch.nn.modules.upsampling.Upsample    [None, 2, 'nearest']
 12           [-1, 6]  1         0  models.common.Concat                    [1]
 13                -1  1     90880  models.common.C3                        [256, 128, 1, False]
 14                -1  1      8320  models.common.Conv                      [128, 64, 1, 1]
 15                -1  1         0  torch.nn.modules.upsampling.Upsample    [None, 2, 'nearest']
 16           [-1, 4]  1         0  models.common.Concat                    [1]
 17                -1  1     22912  models.common.C3                        [128, 64, 1, False]
 18                -1  1     36992  models.common.Conv                      [64, 64, 3, 2]
 19          [-1, 14]  1         0  models.common.Concat                    [1]
 20                -1  1     74496  models.common.C3                        [128, 128, 1, False]
 21                -1  1    147712  models.common.Conv                      [128, 128, 3, 2]
 22          [-1, 10]  1         0  models.common.Concat                    [1]
 23                -1  1    296448  models.common.C3                        [256, 256, 1, False]
 24      [17, 20, 23]  1     33825  models.yolo.Detect                      [20, [[10, 13, 16, 30, 33, 23], [30, 61, 62, 45, 59, 119], [116, 90, 156, 198, 373, 326]], [64, 128, 256]]
YOLOv5n summary: 214 layers, 1790977 parameters, 1790977 gradients, 4.3 GFLOPs
```

> 自动调整 `nc` 的代码在 `models/yolo.py`

```python
        if nc and nc != self.yaml['nc']: # 使用data config中的names长度覆盖模型配置文件中的类别
            LOGGER.info(f"Overriding model.yaml nc={self.yaml['nc']} with nc={nc}")
            self.yaml['nc'] = nc  # override yaml value
```

## 训练时出现的问题

### reduce FPs | 解决特殊场景模型拍摄日常目标的FP数量过多

> [how to use Background images in training? · Issue #2844 · ultralytics/yolov5 (github.com)](https://github.com/ultralytics/yolov5/issues/2844)
>
> 在图片训练文件夹 `images/train` 中添加背景图片文件，比如coco或者voc数据集的一些照片
>
> 不需要添加空白label txt文件，添加了也不会出错
>
> `(if no objects in image, no `\*.txt` file is required).`
>
> [目标检测（降低误检测率及小目标检测系列笔记）](https://blog.csdn.net/weixin_44836143/article/details/105952819)

```sh
train: Scanning D:\code\datasets\classes20\labels\train... 5266 images, 1000 backgrounds, 0 corrupt: 100%|██████████|
train: New cache created: D:\code\datasets\classes20\labels\train.cache
val: Scanning D:\code\datasets\classes20\labels\val... 586 images, 0 backgrounds, 0 corrupt: 100%|██████████|
val: New cache created: D:\code\datasets\classes20\labels\val.cache
```

### 训练 `obj_loss` 增大

> [mAP is too low and val obj_loss is increasing while training is decreasing](https://github.com/ultralytics/yolov5/issues/7384)

> Dataset

- **Images per class.** ≥ 1500 images per class recommended

- **Instances per class.** ≥ 10000 instances (labeled objects) per class recommended

- **Image variety.** Must be representative of deployed environment. For real-world use cases we recommend images from different times of day, different seasons, different weather, different lighting, different angles, different sources (scraped online, collected locally, different cameras) etc.

    必须能够代表部署环境。 对于现实世界的用例，我们推荐来自一天中不同时间、不同季节、不同天气、不同照明、不同角度、不同来源（在线抓取、本地收集、不同相机）等的图像。

- **Label consistency.** All instances of all classes in all images must be labelled. Partial labelling will not work.

    所有图像中所有类的所有实例都必须被标记。 部分标签不起作用。

- **Label accuracy.** Labels must closely enclose each object. No space should exist between an object and it's bounding box. No objects should be missing a label.

    标签必须紧密包围每个对象。 对象与其边界框之间不应存在空间。 任何物品都不应缺少标签。

- **Background images.** Background images are images with no objects that are added to a dataset to reduce False Positives (FP). We recommend about 0-10% background images to help reduce FPs (COCO has 1000 background images for reference, 1% of the total). No labels are required for background images.

    背景图像是没有对象的图像，添加到数据集中以减少误报 (FP)。 我们建议使用大约 0-10% 的背景图片，以帮助降低 FP（COCO 有 1000 张背景图片可供参考，占总数的 1%）。 背景图像不需要标签

# export

## 参数说明

```python
# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""
Export a YOLOv5 PyTorch model to other formats. TensorFlow exports authored by https://github.com/zldrobit.

Format                      | `export.py --include`         | Model
---                         | ---                           | ---
PyTorch                     | -                             | yolov5s.pt
TorchScript                 | `torchscript`                 | yolov5s.torchscript
ONNX                        | `onnx`                        | yolov5s.onnx
OpenVINO                    | `openvino`                    | yolov5s_openvino_model/
TensorRT                    | `engine`                      | yolov5s.engine
CoreML                      | `coreml`                      | yolov5s.mlmodel
TensorFlow SavedModel       | `saved_model`                 | yolov5s_saved_model/
TensorFlow GraphDef         | `pb`                          | yolov5s.pb
TensorFlow Lite             | `tflite`                      | yolov5s.tflite
TensorFlow Edge TPU         | `edgetpu`                     | yolov5s_edgetpu.tflite
TensorFlow.js               | `tfjs`                        | yolov5s_web_model/
PaddlePaddle                | `paddle`                      | yolov5s_paddle_model/

Requirements:
    $ pip install -r requirements.txt coremltools onnx onnx-simplifier onnxruntime openvino-dev tensorflow-cpu  # CPU
    $ pip install -r requirements.txt coremltools onnx onnx-simplifier onnxruntime-gpu openvino-dev tensorflow  # GPU

Usage:
    $ python export.py --weights yolov5s.pt --include torchscript onnx openvino engine coreml tflite ...

Inference:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle

TensorFlow.js:
    $ cd .. && git clone https://github.com/zldrobit/tfjs-yolov5-example.git && cd tfjs-yolov5-example
    $ npm install
    $ ln -s ../../yolov5/yolov5s_web_model public/yolov5s_web_model
    $ npm start
"""

def parse_opt(known=False):
    """
    Parse command-line options for YOLOv5 model export configurations.

    Args:
        known (bool): If True, uses `argparse.ArgumentParser.parse_known_args`; otherwise, uses `argparse.ArgumentParser.parse_args`.
                      Default is False.

    Returns:
        argparse.Namespace: Object containing parsed command-line arguments.

    Example:
        ```python
        opts = parse_opt()
        print(opts.data)
        print(opts.weights)
        ```
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=ROOT / "data/coco128.yaml", help="dataset.yaml path")
    parser.add_argument("--weights", nargs="+", type=str, default=ROOT / "yolov5s.pt", help="model.pt path(s)")
    parser.add_argument("--imgsz", "--img", "--img-size", nargs="+", type=int, default=[640, 640], help="image (h, w)")
    parser.add_argument("--batch-size", type=int, default=1, help="batch size")
    parser.add_argument("--device", default="cpu", help="cuda device, i.e. 0 or 0,1,2,3 or cpu")
    parser.add_argument("--half", action="store_true", help="FP16 half-precision export")
    parser.add_argument("--inplace", action="store_true", help="set YOLOv5 Detect() inplace=True")
    parser.add_argument("--keras", action="store_true", help="TF: use Keras")
    parser.add_argument("--optimize", action="store_true", help="TorchScript: optimize for mobile")
    parser.add_argument("--int8", action="store_true", help="CoreML/TF/OpenVINO INT8 quantization")
    parser.add_argument("--per-tensor", action="store_true", help="TF per-tensor quantization")
    parser.add_argument("--dynamic", action="store_true", help="ONNX/TF/TensorRT: dynamic axes")
    parser.add_argument("--cache", type=str, default="", help="TensorRT: timing cache file path")
    parser.add_argument("--simplify", action="store_true", help="ONNX: simplify model")
    parser.add_argument("--mlmodel", action="store_true", help="CoreML: Export in *.mlmodel format")
    parser.add_argument("--opset", type=int, default=17, help="ONNX: opset version")
    parser.add_argument("--verbose", action="store_true", help="TensorRT: verbose log")
    parser.add_argument("--workspace", type=int, default=4, help="TensorRT: workspace size (GB)")
    parser.add_argument("--nms", action="store_true", help="TF: add NMS to model")
    parser.add_argument("--agnostic-nms", action="store_true", help="TF: add agnostic NMS to model")
    parser.add_argument("--topk-per-class", type=int, default=100, help="TF.js NMS: topk per class to keep")
    parser.add_argument("--topk-all", type=int, default=100, help="TF.js NMS: topk for all classes to keep")
    parser.add_argument("--iou-thres", type=float, default=0.45, help="TF.js NMS: IoU threshold")
    parser.add_argument("--conf-thres", type=float, default=0.25, help="TF.js NMS: confidence threshold")
    parser.add_argument(
        "--include",
        nargs="+",
        default=["torchscript"],
        help="torchscript, onnx, openvino, engine, coreml, saved_model, pb, tflite, edgetpu, tfjs, paddle",
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    print_args(vars(opt))
    return opt
```

> 导出路径和权重路径相同
>
> --include 后面写想导出的格式

## Example

### torchscript

```sh
python export.py --imgsz 640 --weights weights/yolov5s.pt --include torchscript --device 0
python export.py --imgsz 640 --weights weights/yolov5s.pt --include torchscript --device cpu --optimize # --optimize not compatible with cuda devices, i.e. use --device cpu
```

### onnx

> 注意:
>
> `onnxruntime` 和 `onnxruntime-gpu` 不要同时安装，否则使用 `gpu` 推理时速度会很慢，如果同时安装了2个包，要全部卸载，再安装 'onnxruntime-gpu' 才能使用gpu推理，否则gpu速度会很慢

```sh
python export.py --imgsz 640 --weights weights/yolov5s.pt --include onnx --simplify --device 0

python export.py --imgsz 640 --weights weights/yolov5s.pt --include onnx --simplify --device 0 --half      			# --half only compatible with GPU export, i.e. use --device 0

python export.py --imgsz 640 --weights weights/yolov5s.pt --include onnx --simplify --device cpu --dynamic 			# --dynamic only compatible with cpu

python export.py --imgsz 640 --weights weights/yolov5s.pt --include onnx --simplify --device cpu --half --dynamic	# 导出失败 --half not compatible with --dynamic
```

### opencv使用的onnx

> https://github.com/ultralytics/ultralytics/tree/main/examples/YOLOv8-OpenCV-ONNX-Python

```sh
python export.py --imgsz 640 --weights weights/yolov5s.pt --include onnx --simplify --device 0 --opset 12			# opset必须为12

python export.py --imgsz 640 --weights weights/yolov5s.pt --include onnx --simplify --device 0 --half --opset 12	# opset必须为12

# opencv不支持dynamic
```

### openvino

```sh
python export.py --imgsz 640 --weights weights/yolov5s.pt --include openvino --simplify --device cpu      # 可以用simplify的onnx
python export.py --imgsz 640 --weights weights/yolov5s.pt --include openvino --simplify --device 0 --half # openvino支持half,但是要使用cpu导出onnx的half会报错,所以要使用 --device 0, openvino导出和设备无关,不受影响,主要是导出onnx的问题

python export.py --imgsz 640 --weights weights/yolov5s.pt --include openvino --simplify --device cpu --int8 # 需要安装nncf
```

#### 通过openvino的`ovc`命令将onnx转换为openvino格式(支持**fp16**)

> https://docs.openvino.ai/archive/2023.2/openvino_docs_OV_Converter_UG_prepare_model_convert_model_MO_OVC_transition.html

```sh
ovc "onnx_path" --output_model "output_path" --compress_to_fp16

ovc "onnx_path" --output_model "output_path" --compress_to_fp16
```

### export failure  0.9s: DLL load failed while importing ie_api

> https://blog.csdn.net/qq_26815239/article/details/123047840
>
> 如果你使用的是 Python 3.8 或更高版本，并且是在Windows系统下通过pip安装的openvino，那么该错误的解决方案如下：

1. 进入目录 `your\env\site-packages\openvino\inference_engine`
2. 打开文件 `__init__.py`
3. 26行下添加一行

```python
        if os.path.isdir(lib_path):
            # On Windows, with Python >= 3.8, DLLs are no longer imported from the PATH.
            if (3, 8) <= sys.version_info:
                os.add_dll_directory(os.path.abspath(lib_path))
                os.environ['PATH'] = os.path.abspath(lib_path) + ';' + os.environ['PATH']	# 添加这一行
```

### tensorrt

```sh
python export.py --imgsz 640 --weights weights/yolov5s.pt --include engine --simplify --device 0 # 可以用simplify的onnx

python export.py --imgsz 640 --weights weights/yolov5s.pt --include engine --simplify --device 0 --half

python export.py --imgsz 640 --weights weights/yolov5s.pt --include engine --simplify --device 0 --dynamic --batch-size=16 	       # --dynamic model requires maximum --batch-size argument

python export.py --imgsz 640 --weights weights/yolov5s.pt --include engine --simplify --device 0 --half --dynamic --batch-size=16  # 导出失败 --half not compatible with --dynamic, i.e. use either --half or --dynamic but not both
```

# detect

## 参数说明

```python
# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources:
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/LNwODJXcvt4'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlpackage          # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
"""

def parse_opt():
    """
    Parse command-line arguments for YOLOv5 detection, allowing custom inference options and model configurations.

    Args:
        --weights (str | list[str], optional): Model path or Triton URL. Defaults to ROOT / 'yolov5s.pt'.
        --source (str, optional): File/dir/URL/glob/screen/0(webcam). Defaults to ROOT / 'data/images'.
        --data (str, optional): Dataset YAML path. Provides dataset configuration information.
        --imgsz (list[int], optional): Inference size (height, width). Defaults to [640].
        --conf-thres (float, optional): Confidence threshold. Defaults to 0.25.
        --iou-thres (float, optional): NMS IoU threshold. Defaults to 0.45.
        --max-det (int, optional): Maximum number of detections per image. Defaults to 1000.
        --device (str, optional): CUDA device, i.e., '0' or '0,1,2,3' or 'cpu'. Defaults to "".
        --view-img (bool, optional): Flag to display results. Defaults to False.
        --save-txt (bool, optional): Flag to save results to *.txt files. Defaults to False.
        --save-csv (bool, optional): Flag to save results in CSV format. Defaults to False.
        --save-conf (bool, optional): Flag to save confidences in labels saved via --save-txt. Defaults to False.
        --save-crop (bool, optional): Flag to save cropped prediction boxes. Defaults to False.
        --nosave (bool, optional): Flag to prevent saving images/videos. Defaults to False.
        --classes (list[int], optional): List of classes to filter results by, e.g., '--classes 0 2 3'. Defaults to None.
        --agnostic-nms (bool, optional): Flag for class-agnostic NMS. Defaults to False.
        --augment (bool, optional): Flag for augmented inference. Defaults to False.
        --visualize (bool, optional): Flag for visualizing features. Defaults to False.
        --update (bool, optional): Flag to update all models in the model directory. Defaults to False.
        --project (str, optional): Directory to save results. Defaults to ROOT / 'runs/detect'.
        --name (str, optional): Sub-directory name for saving results within --project. Defaults to 'exp'.
        --exist-ok (bool, optional): Flag to allow overwriting if the project/name already exists. Defaults to False.
        --line-thickness (int, optional): Thickness (in pixels) of bounding boxes. Defaults to 3.
        --hide-labels (bool, optional): Flag to hide labels in the output. Defaults to False.
        --hide-conf (bool, optional): Flag to hide confidences in the output. Defaults to False.
        --half (bool, optional): Flag to use FP16 half-precision inference. Defaults to False.
        --dnn (bool, optional): Flag to use OpenCV DNN for ONNX inference. Defaults to False.
        --vid-stride (int, optional): Video frame-rate stride, determining the number of frames to skip in between
            consecutive frames. Defaults to 1.

    Returns:
        argparse.Namespace: Parsed command-line arguments as an argparse.Namespace object.

    Example:
        ```python
        from ultralytics import YOLOv5
        args = YOLOv5.parse_opt()
        ```
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", nargs="+", type=str, default=ROOT / "yolov5s.pt", help="model path or triton URL")
    parser.add_argument("--source", type=str, default=ROOT / "data/images", help="file/dir/URL/glob/screen/0(webcam)")
    parser.add_argument("--data", type=str, default=ROOT / "data/coco128.yaml", help="(optional) dataset.yaml path")
    parser.add_argument("--imgsz", "--img", "--img-size", nargs="+", type=int, default=[640], help="inference size h,w")
    parser.add_argument("--conf-thres", type=float, default=0.25, help="confidence threshold")
    parser.add_argument("--iou-thres", type=float, default=0.45, help="NMS IoU threshold")
    parser.add_argument("--max-det", type=int, default=1000, help="maximum detections per image")
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu")
    parser.add_argument("--view-img", action="store_true", help="show results")
    parser.add_argument("--save-txt", action="store_true", help="save results to *.txt")
    parser.add_argument(
        "--save-format",
        type=int,
        default=0,
        help="whether to save boxes coordinates in YOLO format or Pascal-VOC format when save-txt is True, 0 for YOLO and 1 for Pascal-VOC",
    )
    parser.add_argument("--save-csv", action="store_true", help="save results in CSV format")
    parser.add_argument("--save-conf", action="store_true", help="save confidences in --save-txt labels")
    parser.add_argument("--save-crop", action="store_true", help="save cropped prediction boxes")
    parser.add_argument("--nosave", action="store_true", help="do not save images/videos")
    parser.add_argument("--classes", nargs="+", type=int, help="filter by class: --classes 0, or --classes 0 2 3")
    parser.add_argument("--agnostic-nms", action="store_true", help="class-agnostic NMS")
    parser.add_argument("--augment", action="store_true", help="augmented inference")
    parser.add_argument("--visualize", action="store_true", help="visualize features")
    parser.add_argument("--update", action="store_true", help="update all models")
    parser.add_argument("--project", default=ROOT / "runs/detect", help="save results to project/name")
    parser.add_argument("--name", default="exp", help="save results to project/name")
    parser.add_argument("--exist-ok", action="store_true", help="existing project/name ok, do not increment")
    parser.add_argument("--line-thickness", default=3, type=int, help="bounding box thickness (pixels)")
    parser.add_argument("--hide-labels", default=False, action="store_true", help="hide labels")
    parser.add_argument("--hide-conf", default=False, action="store_true", help="hide confidences")
    parser.add_argument("--half", action="store_true", help="use FP16 half-precision inference")
    parser.add_argument("--dnn", action="store_true", help="use OpenCV DNN for ONNX inference")
    parser.add_argument("--vid-stride", type=int, default=1, help="video frame-rate stride")
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt
```

> source后面可以放图片，视频或者文件夹路径，会保存到runs/detect目录下面

`python detect.py --weights 权重路径 --source 图片or视频or文件夹路径`

## Example

### torch

```sh
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.pt --source data/images/bus.jpg --device 0

python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.pt --source ../datasets/coco128/images/train2017 --device 0
```

### torchscript

```sh
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.torchscript --source data/images/bus.jpg --device 0

python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.torchscript --source ../datasets/coco128/images/train2017 --device 0
```

### onnx

> 注意:
>
> `onnxruntime` 和 `onnxruntime-gpu` 不要同时安装，否则使用 `gpu` 推理时速度会很慢，如果同时安装了2个包，要全部卸载，再安装 `onnxruntime-gpu` 才能使用gpu推理，否则gpu速度会很慢

```sh
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.onnx --source data/images/bus.jpg --device 0
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.onnx --source ../datasets/coco128/images/train2017 --device 0

python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.fp16.onnx --half --source data/images/bus.jpg --device 0				# fp16模型需要 --half
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.fp16.onnx --half --source ../datasets/coco128/images/train2017 --device 0

python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.fp16.onnx --half --source data/images/bus.jpg --device cpu				# gpu导出的fp16模型可以用cpu推理
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.fp16.onnx --half --source ../datasets/coco128/images/train2017 --device cpu

python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.cpu.dynamic.onnx --source data/images/bus.jpg --device 0				# 使用cpu导出的dynamic模型可以用gpu推理
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.cpu.dynamic.onnx --source ../datasets/coco128/images/train2017 --device 0
```

### openvino

> 注意：openvino没法使用cuda，但是使用 --device 0 会提高推理速度

```sh
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s_openvino_model --source data/images/bus.jpg --device cpu

python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s_openvino_model --source ../datasets/coco128/images/train2017 --device cpu
```

### tensorrt

```sh
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.engine --half --source data/images/bus.jpg --device 0					# fp32模型也能用 --half 推理
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.engine --half --source ../datasets/coco128/images/train2017 --device 0

python detect.py --imgsz 640 --save-txt --save-conf --save-crop --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.fp16.engine --half --source data/images/bus.jpg --device 0
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.fp16.engine --half --source ../datasets/coco128/images/train2017 --device 0

python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.fp32.dynamic.engine --half --source data/images/bus.jpg --device 0		 # fp32模型也能用 --half 推理
python detect.py --imgsz 640 --save-txt --save-conf --save-crop --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.fp32.dynamic.engine --half --source ../datasets/coco128/images/train2017 --device 0
```

# val

## 参数说明

```python
# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""
Validate a trained YOLOv5 detection model on a detection dataset.

Usage:
    $ python val.py --weights yolov5s.pt --data coco128.yaml --img 640

Usage - formats:
    $ python val.py --weights yolov5s.pt                 # PyTorch
                              yolov5s.torchscript        # TorchScript
                              yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                              yolov5s_openvino_model     # OpenVINO
                              yolov5s.engine             # TensorRT
                              yolov5s.mlpackage          # CoreML (macOS-only)
                              yolov5s_saved_model        # TensorFlow SavedModel
                              yolov5s.pb                 # TensorFlow GraphDef
                              yolov5s.tflite             # TensorFlow Lite
                              yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                              yolov5s_paddle_model       # PaddlePaddle
"""

def parse_opt():
    """
    Parse command-line options for configuring YOLOv5 model inference.

    Args:
        data (str, optional): Path to the dataset YAML file. Default is 'data/coco128.yaml'.
        weights (list[str], optional): List of paths to model weight files. Default is 'yolov5s.pt'.
        batch_size (int, optional): Batch size for inference. Default is 32.
        imgsz (int, optional): Inference image size in pixels. Default is 640.
        conf_thres (float, optional): Confidence threshold for predictions. Default is 0.001.
        iou_thres (float, optional): IoU threshold for Non-Max Suppression (NMS). Default is 0.6.
        max_det (int, optional): Maximum number of detections per image. Default is 300.
        task (str, optional): Task type - options are 'train', 'val', 'test', 'speed', or 'study'. Default is 'val'.
        device (str, optional): Device to run the model on. e.g., '0' or '0,1,2,3' or 'cpu'. Default is empty to let the system choose automatically.
        workers (int, optional): Maximum number of dataloader workers per rank in DDP mode. Default is 8.
        single_cls (bool, optional): If set, treats the dataset as a single-class dataset. Default is False.
        augment (bool, optional): If set, performs augmented inference. Default is False.
        verbose (bool, optional): If set, reports mAP by class. Default is False.
        save_txt (bool, optional): If set, saves results to *.txt files. Default is False.
        save_hybrid (bool, optional): If set, saves label+prediction hybrid results to *.txt files. Default is False.
        save_conf (bool, optional): If set, saves confidences in --save-txt labels. Default is False.
        save_json (bool, optional): If set, saves results to a COCO-JSON file. Default is False.
        project (str, optional): Project directory to save results to. Default is 'runs/val'.
        name (str, optional): Name of the directory to save results to. Default is 'exp'.
        exist_ok (bool, optional): If set, existing directory will not be incremented. Default is False.
        half (bool, optional): If set, uses FP16 half-precision inference. Default is False.
        dnn (bool, optional): If set, uses OpenCV DNN for ONNX inference. Default is False.

    Returns:
        argparse.Namespace: Parsed command-line options.

    Notes:
        - The '--data' parameter is checked to ensure it ends with 'coco.yaml' if '--save-json' is set.
        - The '--save-txt' option is set to True if '--save-hybrid' is enabled.
        - Args are printed using `print_args` to facilitate debugging.

    Example:
        To validate a trained YOLOv5 model on a COCO dataset:
        ```python
        $ python val.py --weights yolov5s.pt --data coco128.yaml --img 640
        ```
        Different model formats could be used instead of `yolov5s.pt`:
        ```python
        $ python val.py --weights yolov5s.pt yolov5s.torchscript yolov5s.onnx yolov5s_openvino_model yolov5s.engine
        ```
        Additional options include saving results in different formats, selecting devices, and more.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=ROOT / "data/coco128.yaml", help="dataset.yaml path")
    parser.add_argument("--weights", nargs="+", type=str, default=ROOT / "yolov5s.pt", help="model path(s)")
    parser.add_argument("--batch-size", type=int, default=32, help="batch size")
    parser.add_argument("--imgsz", "--img", "--img-size", type=int, default=640, help="inference size (pixels)")
    parser.add_argument("--conf-thres", type=float, default=0.001, help="confidence threshold")
    parser.add_argument("--iou-thres", type=float, default=0.6, help="NMS IoU threshold")
    parser.add_argument("--max-det", type=int, default=300, help="maximum detections per image")
    parser.add_argument("--task", default="val", help="train, val, test, speed or study")
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu")
    parser.add_argument("--workers", type=int, default=8, help="max dataloader workers (per RANK in DDP mode)")
    parser.add_argument("--single-cls", action="store_true", help="treat as single-class dataset")
    parser.add_argument("--augment", action="store_true", help="augmented inference")
    parser.add_argument("--verbose", action="store_true", help="report mAP by class")
    parser.add_argument("--save-txt", action="store_true", help="save results to *.txt")
    parser.add_argument("--save-hybrid", action="store_true", help="save label+prediction hybrid results to *.txt")
    parser.add_argument("--save-conf", action="store_true", help="save confidences in --save-txt labels")
    parser.add_argument("--save-json", action="store_true", help="save a COCO-JSON results file")
    parser.add_argument("--project", default=ROOT / "runs/val", help="save to project/name")
    parser.add_argument("--name", default="exp", help="save to project/name")
    parser.add_argument("--exist-ok", action="store_true", help="existing project/name ok, do not increment")
    parser.add_argument("--half", action="store_true", help="use FP16 half-precision inference")
    parser.add_argument("--dnn", action="store_true", help="use OpenCV DNN for ONNX inference")
    opt = parser.parse_args()
    opt.data = check_yaml(opt.data)  # check YAML
    opt.save_json |= opt.data.endswith("coco.yaml")
    opt.save_txt |= opt.save_hybrid
    print_args(vars(opt))
    return opt
```

## 问题

### default confidence threshold = 0.001

> [mAP bug at higher --conf · Issue #1466 · ultralytics/yolov5](https://github.com/ultralytics/yolov5/issues/1466)
>
> [Why does the confidence threshold of 0.001 in val.py result in good results? · Issue #11745 · ultralytics/yolov5](https://github.com/ultralytics/yolov5/issues/11745)

### 验证模型在自定义数据集上的效果 精度0.995

> https://www.jianshu.com/p/cfb01add61bd#1684051613808
>
> https://github.com/ultralytics/yolov5/issues/5508
>
> https://github.com/ultralytics/yolov5/issues/1563
>
> https://github.com/ultralytics/yolov5/pull/1646
>
> `--save-hybrid` 会合并已知的labels，导致得分很高

## Example

### torch

```sh
python val.py --imgsz 640 --save-txt --save-conf --save-json --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.pt --device 0
```

### torchscript

```sh
python val.py --imgsz 640 --save-txt --save-conf --save-json --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.torchscript --device 0
```

### onnx

> 注意:
>
> `onnxruntime` 和 `onnxruntime-gpu` 不要同时安装，否则使用 `gpu` 推理时速度会很慢，如果同时安装了2个包，要全部卸载，再安装 `onnxruntime-gpu` 才能使用gpu推理，否则gpu速度会很慢

```sh
python val.py --imgsz 640 --save-txt --save-conf --save-json --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.onnx --device 0

python val.py --imgsz 640 --save-txt --save-conf --save-json --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.onnx --device 0 --dnn
```

### openvino

> 注意：openvino没法使用cuda，但是使用 --device 0 会提高推理速度

```sh
python val.py --imgsz 640 --save-txt --save-conf --save-json --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s_openvino_model --device cpu
```

### tensorrt

```sh
python val.py --imgsz 640 --save-txt --save-conf --save-json --conf-thres 0.25 --iou-thres 0.6 --data data/coco128.yaml --weights weights/yolov5s.engine --device 0
```
