# 安装

## pip 安装

```sh
# Install the ultralytics package from PyPI
pip install ultralytics
```

## git clone

```sh
# Clone the ultralytics repository
git clone https://github.com/ultralytics/ultralytics

# Navigate to the cloned directory
cd ultralytics

# Install the package in editable mode for development
pip install -v -e .
# "-v" 指详细说明，或更多的输出
# "-e" 表示在可编辑模式下安装项目，因此对代码所做的任何本地修改都会生效，从而无需重新安装。
```

# [配置](https://docs.ultralytics.com/zh/usage/cfg/)

YOLO 设置和超参数在模型的性能、速度和 [准确性](https://www.ultralytics.com/glossary/accuracy) 方面起着关键作用。这些设置会影响模型在各个阶段的行为，包括训练、验证和预测。

Ultralytics 命令使用以下语法：

> CLI

```sh
yolo TASK MODE ARGS
```

> python

```python
from ultralytics import YOLO

# Load a YOLO model from a pre-trained weights file
model = YOLO("yolo11n.pt")

# Run MODE mode using the custom arguments ARGS (guess TASK)
model.MODE(ARGS)
```

其中：

- `TASK` （可选）是以下之一（[detect](https://docs.ultralytics.com/zh/tasks/detect/), [分割](https://docs.ultralytics.com/zh/tasks/segment/), [分类](https://docs.ultralytics.com/zh/tasks/classify/), [姿势估计](https://docs.ultralytics.com/zh/tasks/pose/), [旋转框检测](https://docs.ultralytics.com/zh/tasks/obb/))
- `MODE` （必需）是以下之一（[train](https://docs.ultralytics.com/zh/modes/train/), [val](https://docs.ultralytics.com/zh/modes/val/), [预测](https://docs.ultralytics.com/zh/modes/predict/), [导出](https://docs.ultralytics.com/zh/modes/export/), [追踪](https://docs.ultralytics.com/zh/modes/track/), [基准测试](https://docs.ultralytics.com/zh/modes/benchmark/))
- `ARGS` （可选）是 `arg=value` 键值对，例如 `imgsz=640` 用于覆盖默认值。

默认值 `ARG` 值在此页面上定义，并且来自 `cfg/defaults.yaml` [文件](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/default.yaml).

## 任务

Ultralytics YOLO 模型可以执行各种计算机视觉任务，包括：

- **检测**: [物体检测](https://docs.ultralytics.com/zh/tasks/detect/) 识别并定位图像或视频中的物体。
- **分割**：[实例分割](https://docs.ultralytics.com/zh/tasks/segment/)将图像或视频划分为对应于不同对象或类别的区域。
- **分类**: [图像分类](https://docs.ultralytics.com/zh/tasks/classify/) 预测输入图像的类别标签。
- **姿势估计**[姿势估计 ](https://docs.ultralytics.com/zh/tasks/pose/)：[姿势估计 可以](https://docs.ultralytics.com/zh/tasks/pose/)识别图像或视频中的物体并估计其关键点。
- **旋转框检测**:[定向边界框](https://docs.ultralytics.com/zh/tasks/obb/)使用旋转边界框，适用于卫星或医学图像。

| 参数   | 默认值     | 描述                                                         |
| :----- | :--------- | :----------------------------------------------------------- |
| `task` | `'detect'` | 指定 YOLO 任务： `detect` 用于 [对象检测](https://www.ultralytics.com/glossary/object-detection), `segment` 用于分割， `classify` 用于分类， `pose` 用于姿势估计 ，以及 `obb` 用于定向边界框。每项任务都针对图像和视频分析中的特定输出和问题量身定制。 |

## 模式

Ultralytics YOLO 模型以不同的模式运行，每种模式都专为模型生命周期的特定阶段而设计：

- **训练**：在自定义数据集上训练 YOLO 模型。
- **Val**：验证已训练的 YOLO 模型。
- **预测**：使用训练好的 YOLO 模型对新图像或视频进行预测。
- **导出**：导出 YOLO 模型以进行部署。
- **跟踪**：使用 YOLO 模型实时跟踪对象。
- **基准测试**: 对 YOLO 导出（ONNX、TensorRT 等）的速度和准确性进行基准测试。

| 参数   | 默认值    | 描述                                                         |
| :----- | :-------- | :----------------------------------------------------------- |
| `mode` | `'train'` | 指定 YOLO 模型的运行模式： `train` 用于模型训练， `val` 用于验证， `predict` 用于推理， `export` 用于转换为部署格式， `track` 用于对象跟踪，以及 `benchmark` 用于性能评估。每种模式都支持从开发到部署的不同阶段。 |

## 训练设置

...

## 预测设置

...

## 验证设置

...

## 导出设置

...

## 解决方案设置

Ultralytics Solutions 配置设置提供了灵活性，可以自定义模型以执行对象计数、热图创建、锻炼跟踪、数据分析、区域跟踪、队列管理和基于区域的计数等任务。这些选项允许轻松调整，以获得根据特定需求量身定制的准确且有用的结果。

| 参数              | 类型                  | 默认值                       | 描述                                                         |
| :---------------- | :-------------------- | :--------------------------- | :----------------------------------------------------------- |
| `model`           | `str`                 | `None`                       | Ultralytics YOLO 模型文件的路径。                            |
| `region`          | `list`                | `'[(20, 400), (1260, 400)]'` | 定义计数区域的点列表。                                       |
| `show_in`         | `bool`                | `True`                       | 控制是否在视频流上显示进入计数的标志。                       |
| `show_out`        | `bool`                | `True`                       | 控制是否在视频流上显示离开计数的标志。                       |
| `analytics_type`  | `str`                 | `line`                       | 图形类型，即 `line`, `bar`, `area`或 `pie`.                  |
| `colormap`        | `int`                 | `cv2.COLORMAP_JET`           | 用于热图的颜色映射。                                         |
| `json_file`       | `str`                 | `None`                       | 包含所有停车坐标数据的 JSON 文件路径。                       |
| `up_angle`        | `float`               | `145.0`                      | 向上 "姿势估计角度阈值。                                     |
| `kpts`            | `list[int, int, int]` | `'[6, 8, 10]'`               | 用于监控锻炼的关键点列表。这些关键点对应于身体关节或部位，例如肩部、肘部和腕部，适用于俯卧撑、引体向上、深蹲、腹部锻炼等运动。 |
| `down_angle`      | `float`               | `90.0`                       | 下 "姿势估计角度阈值。                                       |
| `blur_ratio`      | `float`               | `0.5`                        | 调整模糊强度的百分比，取值范围为 `0.1 - 1.0`.                |
| `crop_dir`        | `str`                 | `'cropped-detections'`       | 用于存储裁剪检测结果的目录名。                               |
| `records`         | `int`                 | `5`                          | 触发带有安全警报系统的电子邮件的总检测计数。                 |
| `vision_point`    | `tuple[int, int]`     | `(20, 20)`                   | 视觉将跟踪对象并使用 VisionEye 解决方案绘制路径的点。        |
| `source`          | `str`                 | `None`                       | 输入源（视频、RTSP 等）的路径。仅适用于 Solutions 命令行界面 (CLI)。 |
| `figsize`         | `tuple[int, int]`     | `(12.8, 7.2)`                | 用于分析图表（如热图或图形）的图形大小。                     |
| `fps`             | `float`               | `30.0`                       | 用于速度计算的每秒帧数。                                     |
| `max_hist`        | `int`                 | `5`                          | 用于速度/方向计算的每个对象要跟踪的最大历史点数。            |
| `meter_per_pixel` | `float`               | `0.05`                       | 用于将像素距离转换为真实世界单位的比例因子。                 |
| `max_speed`       | `int`                 | `120`                        | 视觉叠加中的最大速度限制（用于警报）。                       |
| `data`            | `str`                 | `'images'`                   | 用于相似性搜索的图像目录的路径。                             |

## 数据增强设置

...

## 日志记录、检查点和绘图设置

...

# 数据集

先要把数据集放入dataset中，修改data/目录下的yaml，调整为自己的数据集，需要调整路径，分类数，标签名

yolo数据集格式(yolov5/v8的coco8和霹雳吧啦Wz的yolo3为例)

txt内容，每一行都是 `3 0.933536 0.486124 0.030408 0.154487`，`class center_x center_y width height`

label 中心横坐标与图像宽度比值 中心纵坐标与图像高度比值 bbox宽度与图像宽度比值 bbox高度与图像宽高比值

```sh
#-------------------------------------------#
#     yolov5 v8的格式
#-------------------------------------------#
yaml:
    path: coco8                 # dataset root dir
    train: images/train         # train images (relative to 'path') 128 images
    val: images/val             # val images (relative to 'path') 128 images
    test: images/test           # test images (optional)

dir:
    datasets
    ├── coco8
        ├── images
        │   ├── train   # 训练图片
        │   ├── val     # 验证图片
        │   └── test    # 测试图片
        └── labels
            ├── train   # 训练标签txt
            ├── val     # 验证标签txt
            └── test    # 测试标签txt

#-------------------------------------------#
#     yolov5 v8另的一种图片目录格式
#-------------------------------------------#
yaml:
    path: coco8                 # dataset root dir
    train: train/images         # train images (relative to 'path')
    val: val/images             # val images (relative to 'path')
    test: test/images           # test images (optional)

dir:
    datasets
    ├── coco8
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

`ultralytics/cfg/datasets/VOC.yaml`

```yaml
# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# PASCAL VOC dataset http://host.robots.ox.ac.uk/pascal/VOC by University of Oxford
# Documentation: # Documentation: https://docs.ultralytics.com/datasets/detect/voc/
# Example usage: yolo train data=VOC.yaml
# parent
# ├── ultralytics
# └── datasets
#     └── VOC ← downloads here (2.8 GB)
#         └── images/
#             └── train2012/  存放训练图片
#             └── train2007/  存放训练图片
#             └── val2012/    存放训练图片
#             └── val2017/    存放训练图片
#             └── test2007/   存放验证/测试图片
#         └── labels/
#             └── train2012/  存放训练标签  class center_x center_y width height
#             └── train2007/  存放训练标签
#             └── val2012/    存放训练标签
#             └── val2017/    存放训练标签
#             └── test2007/   存放验证/测试标签

# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
path: VOC
train: # train images (relative to 'path') 16551 images
  - images/train2012
  - images/train2007
  - images/val2012
  - images/val2007
val: # val images (relative to 'path') 4952 images
  - images/test2007
test: # test images (optional)
  - images/test2007

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

# 下载权重

> 将下载好的权重放到`weights/`文件下下

## 模型

所有的 YOLOv8 预训练模型都可以在此找到。检测、分割和姿态模型在 [COCO](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/datasets/coco.yaml) 数据集上进行预训练，而分类模型在 [ImageNet](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/datasets/ImageNet.yaml) 数据集上进行预训练。

在首次使用时，[模型](https://github.com/ultralytics/ultralytics/tree/main/ultralytics/models) 会自动从最新的 Ultralytics [发布版本](https://github.com/ultralytics/assets/releases)中下载。

| 模型                                                         | 尺寸 （像素） | mAPval 50-95 | 推理速度 CPU ONNX (ms) | 推理速度 A100 TensorRT (ms) | 参数量 (M) | FLOPs (B) |
| ------------------------------------------------------------ | ------------- | ------------ | ---------------------- | --------------------------- | ---------- | --------- |
| [yolo11n](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolo11n.pt) | 640           | 37.3         | 80.4                   | 0.99                        | 3.2        | 8.7       |
| [yolo11n](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolo11n.pt) | 640           | 44.9         | 128.4                  | 1.20                        | 11.2       | 28.6      |
| [YOLOv8m](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt) | 640           | 50.2         | 234.7                  | 1.83                        | 25.9       | 78.9      |
| [YOLOv8l](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt) | 640           | 52.9         | 375.2                  | 2.39                        | 43.7       | 165.2     |
| [YOLOv8x](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt) | 640           | 53.9         | 479.1                  | 3.53                        | 68.2       | 257.8     |

- **mAPval** 结果都在 [COCO val2017](http://cocodataset.org/) 数据集上，使用单模型单尺度测试得到。
  复现命令 `yolo val detect data=coco.yaml device=0`
- **推理速度**使用 COCO 验证集图片推理时间进行平均得到，测试环境使用 [Amazon EC2 P4d](https://aws.amazon.com/ec2/instance-types/p4/) 实例。
  复现命令 `yolo val detect data=coco8.yaml batch=1 device=0|cpu`

# [命令行界面](https://docs.ultralytics.com/zh/usage/cli/)

## 语法

```sh
yolo TASK MODE ARGS
```

其中：

- `TASK` （可选）是以下之一 `[detect, segment, classify, pose, obb]`。如果未明确传递，YOLO 将尝试推断 `TASK` 。
- `MODE` （必需）是以下之一 `[train, val, predict, export, track, benchmark]`
- `ARGS` （可选）是任意数量的自定义 `arg=value` 键值对，例如 `imgsz=320` ，用于覆盖默认值。 有关可用 `ARGS`，请参阅 [配置](https://docs.ultralytics.com/zh/usage/cfg/) 页面和 `defaults.yaml`.

在完整版中查看所有 ARGS [配置指南](https://docs.ultralytics.com/zh/usage/cfg/) 或使用 `yolo cfg`.

> 参数必须以 `arg=val` 对，用等号分隔 `=` 签名，并用空格分隔对。不要使用 `--` 参数前缀或逗号 `,` 在参数之间。
>
> - `yolo predict model=yolo11n.pt imgsz=640 conf=0.25`  ✅
> - `yolo predict model yolo11n.pt imgsz 640 conf 0.25`  ❌
> - `yolo predict --model yolo11n.pt --imgsz 640 --conf 0.25`  ❌

## 训练

在 COCO8 数据集上训练 YOLO，图像大小为 640，训练 100 个 epoch。有关可用参数的完整列表，请参见[配置](https://docs.ultralytics.com/zh/usage/cfg/)页面。

```sh
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640
```

恢复中断的训练会话：

```sh
yolo detect train resume model=last.pt
```

## 验证

验证 [准确性](https://www.ultralytics.com/glossary/accuracy) 在 COCO8 数据集上训练模型的。由于 `model` 保留其训练 `data` 和参数作为模型属性，因此无需任何参数。

```sh
yolo detect val model=yolo11n.pt
```

验证自定义训练的模型：

```sh
yolo detect val model=path/to/best.pt
```

## 预测

使用训练好的模型来运行图像预测。

使用官方YOLO11n模型进行预测：

```sh
yolo detect predict model=yolo11n.pt source='https://ultralytics.com/images/bus.jpg'
```

使用自定义模型进行预测：

```sh
yolo detect predict model=path/to/best.pt source='https://ultralytics.com/images/bus.jpg'
```

## 导出

将官方 YOLO11n 模型导出为 ONNX 格式：

```sh
yolo export model=yolo11n.pt format=onnx
```

将自定义训练的模型导出为 ONNX 格式：

```
yolo export model=path/to/best.pt format=onnx
```

## 覆盖默认参数

通过在 CLI 中传递参数来覆盖默认参数，例如 `arg=value` 键值对的形式传递参数来覆盖默认参数。

训练一个检测模型 10 个 epochs，学习率为 0.01：

```sh
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=10 lr0=0.01
```

使用预训练的分割模型在YouTube视频上以320的图像尺寸进行预测：

```sh
yolo segment predict model=yolo11n-seg.pt source='https://youtu.be/LNwODJXcvt4' imgsz=320
```

使用 1 的批量大小和 640 的图像大小验证预训练的检测模型：

```sh
yolo detect val model=yolo11n.pt data=coco8.yaml batch=1 imgsz=640
```

## 覆盖默认配置文件

覆盖 `default.yaml` 通过传递一个新文件来完全替换配置文件。 `cfg` 参数，例如 `cfg=custom.yaml`.

为此，首先创建一份副本 `default.yaml` 在您当前的工作目录中使用 `yolo copy-cfg` 命令，它会创建一个 `default_copy.yaml` 文件。

然后，您可以将此文件作为以下内容传递： `cfg=default_copy.yaml` 以及任何其他参数，例如 `imgsz=320` 在此示例中：

```sh
yolo copy-cfg
yolo cfg=default_copy.yaml imgsz=320
```

## 解决方案命令

Ultralytics 通过 CLI 为常见的计算机视觉应用提供即用型解决方案。这些解决方案简化了对象计数、锻炼监控和队列管理等复杂任务的实施。

统计视频或直播流中的物体数量：

```sh
yolo solutions count show=True
yolo solutions count source="path/to/video.mp4" # specify video file path
```

使用姿势模型监控锻炼练习：

```sh
yolo solutions workout show=True
yolo solutions workout source="path/to/video.mp4" # specify video file path

# Use keypoints for ab-workouts
yolo solutions workout kpts=[5, 11, 13] # left side
yolo solutions workout kpts=[6, 12, 14] # right side
```

统计指定队列或区域中的物体数量：

```sh
yolo solutions queue show=True
yolo solutions queue source="path/to/video.mp4"                                # specify video file path
yolo solutions queue region="[(20, 400), (1080, 400), (1080, 360), (20, 360)]" # configure queue coordinates
```

使用 Streamlit 在 Web 浏览器中执行对象检测、实例分割或姿势估计：

```sh
yolo solutions inference
yolo solutions inference model="path/to/model.pt" # use custom model
```

查看可用的解决方案及其选项：

```sh
yolo solutions help
```

# [训练](https://docs.ultralytics.com/zh/modes/train/)

## 使用示例

### **单 GPU 和 CPU 训练示例**

设备是自动确定的。如果有 GPU 可用，则将使用 GPU（默认 CUDA 设备 0），否则将在 CPU 上开始训练。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.yaml")  # build a new model from YAML
model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)
model = YOLO("yolo11n.yaml").load("yolo11n.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data="coco8.yaml", epochs=100, imgsz=640)
```

```python
from ultralytics import YOLO

# yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10
# fraction=1.0 cos_lr=True device=0 model=weights/yolo11n.pt data=ultralytics/cfg/datasets/coco8.yaml

# 加载一个模型
model = YOLO('weights/yolo11n.pt')  # 加载预训练模型（推荐用于训练）

# 训练模型
results = model.train(
    imgsz=640,
    batch=-1,
    workers=8,
    epochs=300,
    patience=0,
    close_mosaic=10,
    fraction=1.0,
    cos_lr=True,
    device=0,
    data='ultralytics/cfg/datasets/coco8.yaml',
)

print(results)
```

> CLI

```sh
# Build a new model from YAML and start training from scratch
yolo detect train data=coco8.yaml model=yolo11n.yaml epochs=100 imgsz=640

# Start training from a pretrained *.pt model
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640

# Build a new model from YAML, transfer pretrained weights to it and start training
yolo detect train data=coco8.yaml model=yolo11n.yaml pretrained=yolo11n.pt epochs=100 imgsz=640
```

### 多 GPU 训练

通过将训练负载分配到多个 GPU 上，多 GPU 训练可以更有效地利用可用的硬件资源。此功能可通过 python API 和命令行界面使用。要启用多 GPU 训练，请指定您希望使用的 GPU 设备 ID。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)

# Train the model with 2 GPUs
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=[0, 1])

# Train the model with the two most idle GPUs
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=[-1, -1])
```

> CLI

```sh
# Start training from a pretrained *.pt model using GPUs 0 and 1
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640 device=0,1

# Use the two most idle GPUs
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640 device=-1,-1
```

### 空闲 GPU 训练

空闲 GPU 训练支持自动选择多 GPU 系统中利用率最低的 GPU，从而优化资源使用，而无需手动选择 GPU。此功能根据利用率指标和 VRAM 可用性识别可用的 GPU。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)

# Train using the single most idle GPU
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=-1)

# Train using the two most idle GPUs
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=[-1, -1])
```

> CLI

```shell
# Start training using the single most idle GPU
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640 device=-1

# Start training using the two most idle GPUs
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640 device=-1,-1
```

### Apple Silicon MPS 训练

通过 Ultralytics YOLO 模型中集成的对 Apple 芯片的支持，现在可以在利用强大的 Metal Performance Shaders (MPS) 框架的设备上训练您的模型。MPS 提供了一种在 Apple 的定制芯片上执行计算和图像处理任务的高性能方法。

为了在 Apple 芯片上启用训练，您应该在启动训练过程时将 'mps' 指定为您的设备。以下是如何在 python 中以及通过命令行执行此操作的示例：

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)

# Train the model with MPS
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device="mps")
```

> CLI

```shell
# Start training from a pretrained *.pt model using MPS
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640 device=mps
```

### 恢复中断的训练

从先前保存的状态恢复训练是使用深度学习模型时的一项关键功能。这在各种情况下都非常有用，例如当训练过程意外中断时，或者当您希望使用新数据或更多 epoch 继续训练模型时。

当训练恢复时，Ultralytics YOLO 会从上次保存的模型加载权重，还会恢复优化器状态、[学习率](https://www.ultralytics.com/glossary/learning-rate)调度器和 epoch 编号。这使您可以从中断的地方无缝地继续训练过程。

您可以通过设置以下参数，在 Ultralytics YOLO 中轻松恢复训练 `resume` 参数为 `True` 在调用 `train` 方法时，并指定包含部分训练模型权重的 `.pt` 文件的路径。

以下是如何使用 python 和通过命令行恢复中断训练的示例：

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("path/to/last.pt")  # load a partially trained model

# Resume training
results = model.train(resume=True)
```

> CLI

```sh
# Resume an interrupted training
yolo train resume model=path/to/last.pt
```

通过设置`resume=True`，`train`函数将从'path/to/last.pt'文件中存储的状态继续训练。如果省略`resume`参数或将其设置为`False`，`train`函数将启动新的训练会话。

请记住，默认情况下，检查点会在每个时期结束时保存，或者使用`save_period`参数以固定间隔保存，因此您必须至少完成1个时期才能恢复训练运行。

通过设置 `resume=True`， `train` 函数将从上次停止的地方继续训练，使用存储在 'path\/to\/last.pt' 文件中的状态。如果省略 `resume` 参数或将其设置为 `False`， `train` ，该函数将启动新的训练会话。

请记住，默认情况下，检查点会在每个 epoch 结束时保存，或者使用 `save_period` 参数按固定间隔保存，因此您必须至少完成 1 个 epoch 才能恢复训练运行。

## 训练设置

YOLO 模型的训练设置包括训练过程中使用的各种超参数和配置。这些设置会影响模型的性能、速度和[准确性](https://www.ultralytics.com/glossary/accuracy)。关键训练设置包括批量大小、学习率、动量和权重衰减。此外，优化器的选择、[损失函数](https://www.ultralytics.com/glossary/loss-function)和训练数据集组成会影响训练过程。仔细调整和试验这些设置对于优化性能至关重要。

| 参数              | 类型                     | 默认值   | 描述                                                         |
| :---------------- | :----------------------- | :------- | :----------------------------------------------------------- |
| `model`           | `str`                    | `None`   | 指定用于训练的模型文件。接受指向 `.pt` 预训练模型或 `.yaml` 配置文件的路径。对于定义模型结构或初始化权重至关重要。 |
| `data`            | `str`                    | `None`   | 数据集配置文件的路径（例如， `coco8.yaml`）。此文件包含数据集特定的参数，包括训练和 [验证数据的路径](https://www.ultralytics.com/glossary/validation-data)，类别名称和类别数量。 |
| `epochs`          | `int`                    | `100`    | 训练的总轮数。每个[epoch](https://www.ultralytics.com/glossary/epoch)代表对整个数据集的一次完整遍历。调整此值会影响训练时长和模型性能。 |
| `time`            | `float`                  | `None`   | 最长训练时间（以小时为单位）。如果设置此参数，它将覆盖 `epochs` 参数，允许训练在指定时长后自动停止。适用于时间受限的训练场景。 |
| `patience`        | `int`                    | `100`    | 在验证指标没有改善的情况下，等待多少个epoch后提前停止训练。通过在性能停滞时停止训练，有助于防止[过拟合](https://www.ultralytics.com/glossary/overfitting)。 |
| `batch`           | `int` 或 `float`         | `16`     | [批次大小](https://www.ultralytics.com/glossary/batch-size)，具有三种模式：设置为整数（例如， `batch=16`），自动模式，GPU 内存利用率为 60%（`batch=-1`），或具有指定利用率分数的自动模式（`batch=0.70`）。 |
| `imgsz`           | `int` 或 `list`          | `640`    | 训练的目标图像大小。所有图像在输入模型之前都会调整为此尺寸。影响模型的[准确性](https://www.ultralytics.com/glossary/accuracy)和计算复杂度。 |
| `save`            | `bool`                   | `True`   | 启用保存训练检查点和最终模型权重。可用于恢复训练或[模型部署](https://www.ultralytics.com/glossary/model-deployment)。 |
| `save_period`     | `int`                    | `-1`     | 保存模型检查点的频率，以 epoch 为单位指定。值为 -1 时禁用此功能。适用于在长时间训练期间保存临时模型。 |
| `cache`           | `bool`                   | `False`  | 启用在内存中缓存数据集图像（`True`/`ram`），在磁盘上缓存（`disk`），或禁用缓存（`False`）。通过减少磁盘 I/O 来提高训练速度，但会增加内存使用量。 |
| `device`          | `int` 或 `str` 或 `list` | `None`   | 指定用于训练的计算设备：单个 GPU（`device=0`），多个 GPU（`device=[0,1]`），CPU（`device=cpu`），适用于 Apple 芯片的 MPS（`device=mps`），或自动选择最空闲的 GPU（`device=-1`）或多个空闲 GPU （`device=[-1,-1]`) |
| `workers`         | `int`                    | `8`      | 用于数据加载的工作线程数（每个 `RANK` ，如果是多 GPU 训练）。影响数据预处理和输入模型的速度，在多 GPU 设置中尤其有用。 |
| `project`         | `str`                    | `None`   | 项目目录的名称，训练输出保存在此目录中。允许有组织地存储不同的实验。 |
| `name`            | `str`                    | `None`   | 训练运行的名称。用于在项目文件夹中创建一个子目录，训练日志和输出存储在该子目录中。 |
| `exist_ok`        | `bool`                   | `False`  | 如果为 True，则允许覆盖现有的 project/name 目录。适用于迭代实验，无需手动清除之前的输出。 |
| `pretrained`      | `bool` 或 `str`          | `True`   | 确定是否从预训练模型开始训练。可以是一个布尔值，也可以是加载权重的特定模型的字符串路径。增强训练效率和模型性能。 |
| `optimizer`       | `str`                    | `'auto'` | 训练优化器的选择。选项包括 `SGD`, `Adam`, `AdamW`, `NAdam`, `RAdam`, `RMSProp` 等等，或者 `auto` 用于基于模型配置自动选择。影响收敛速度和稳定性。 |
| `seed`            | `int`                    | `0`      | 设置训练的随机种子，确保在相同配置下运行结果的可重复性。     |
| `deterministic`   | `bool`                   | `True`   | 强制使用确定性算法，确保可重复性，但由于限制了非确定性算法，可能会影响性能和速度。 |
| `single_cls`      | `bool`                   | `False`  | 在多类别数据集中，将所有类别视为单个类别进行训练。适用于二元分类任务或侧重于对象是否存在而非分类时。 |
| `classes`         | `list[int]`              | `None`   | 指定要训练的类 ID 列表。可用于在训练期间过滤掉并仅关注某些类。 |
| `rect`            | `bool`                   | `False`  | 启用矩形训练，优化批次组合以实现最小填充。可以提高效率和速度，但可能会影响模型准确性。 |
| `multi_scale`     | `bool`                   | `False`  | 通过增加/减少来启用多尺度训练 `imgsz` 高达 `0.5` 在训练期间。训练模型，使其在多次迭代中更加准确 `imgsz` 在推理过程中。 |
| `cos_lr`          | `bool`                   | `False`  | 使用余弦[学习率](https://www.ultralytics.com/glossary/learning-rate)调度器，在 epochs 上按照余弦曲线调整学习率。有助于管理学习率，从而实现更好的收敛。 |
| `close_mosaic`    | `int`                    | `10`     | 在最后 N 个 epochs 中禁用 mosaic [数据增强](https://www.ultralytics.com/glossary/data-augmentation)，以在完成前稳定训练。设置为 0 可禁用此功能。 |
| `resume`          | `bool`                   | `False`  | 从上次保存的检查点恢复训练。自动加载模型权重、优化器状态和 epoch 计数，无缝继续训练。 |
| `amp`             | `bool`                   | `True`   | 启用自动[混合精度](https://www.ultralytics.com/glossary/mixed-precision)（AMP）训练，减少内存使用，并可能在对准确性影响最小的情况下加快训练速度。 |
| `fraction`        | `float`                  | `1.0`    | 指定用于训练的数据集比例。允许在完整数据集的子集上进行训练，这在实验或资源有限时非常有用。 |
| `profile`         | `bool`                   | `False`  | 在训练期间启用 ONNX 和 TensorRT 速度的分析，有助于优化模型部署。 |
| `freeze`          | `int` 或 `list`          | `None`   | 冻结模型的前 N 层或按索引指定的层，从而减少可训练参数的数量。适用于微调或[迁移学习](https://www.ultralytics.com/glossary/transfer-learning)。 |
| `lr0`             | `float`                  | `0.01`   | 初始学习率（即 `SGD=1E-2`, `Adam=1E-3`)。调整此值对于优化过程至关重要，它会影响模型权重更新的速度。 |
| `lrf`             | `float`                  | `0.01`   | 最终学习率作为初始速率的一部分 = (`lr0 * lrf`），与调度器结合使用以随时间调整学习率。 |
| `momentum`        | `float`                  | `0.937`  | SGD 的动量因子或 [Adam 优化器](https://www.ultralytics.com/glossary/adam-optimizer)的 beta1，影响当前更新中过去梯度的合并。 |
| `weight_decay`    | `float`                  | `0.0005` | L2 [正则化](https://www.ultralytics.com/glossary/regularization)项，惩罚大权重以防止过拟合。 |
| `warmup_epochs`   | `float`                  | `3.0`    | 学习率预热的 epochs 数，将学习率从低值逐渐增加到初始学习率，以在早期稳定训练。 |
| `warmup_momentum` | `float`                  | `0.8`    | 预热阶段的初始动量，在预热期间逐渐调整到设定的动量。         |
| `warmup_bias_lr`  | `float`                  | `0.1`    | 预热阶段偏差参数的学习率，有助于稳定初始 epochs 中的模型训练。 |
| `box`             | `float`                  | `7.5`    | [损失函数](https://www.ultralytics.com/glossary/loss-function)中框损失分量的权重，影响对准确预测[边界框](https://www.ultralytics.com/glossary/bounding-box)坐标的重视程度。 |
| `cls`             | `float`                  | `0.5`    | 分类损失在总损失函数中的权重，影响正确类别预测相对于其他成分的重要性。 |
| `dfl`             | `float`                  | `1.5`    | 分布焦点损失的权重，在某些 YOLO 版本中用于细粒度分类。       |
| `pose`            | `float`                  | `12.0`   | 为姿势估计 训练的模型中姿势估计 损失的权重，影响对准确预测姿势估计 关键点的重视程度。 |
| `kobj`            | `float`                  | `2.0`    | 关键点对象性损失在姿势估计 模型中的权重，兼顾检测可信度和姿势估计 精度。 |
| `nbs`             | `int`                    | `64`     | 用于损失归一化的标称批量大小。                               |
| `overlap_mask`    | `bool`                   | `True`   | 确定是否应将对象掩码合并为单个掩码以进行训练，还是为每个对象保持分离。如果发生重叠，则在合并期间，较小的掩码会覆盖在较大的掩码之上。 |
| `mask_ratio`      | `int`                    | `4`      | 分割掩码的下采样率，影响训练期间使用的掩码分辨率。           |
| `dropout`         | `float`                  | `0.0`    | 分类任务中用于正则化的 Dropout 率，通过在训练期间随机省略单元来防止过拟合。 |
| `val`             | `bool`                   | `True`   | 在训练期间启用验证，从而可以定期评估模型在单独数据集上的性能。 |
| `plots`           | `bool`                   | `False`  | 生成并保存训练和验证指标的图表，以及预测示例，从而提供对模型性能和学习进度的可视化见解。 |

> 关于批量大小设置的说明
>
> 字段 `batch` 参数可以通过三种方式配置：
>
> - **固定 [批量大小](https://www.ultralytics.com/glossary/batch-size)**：设置一个整数值（例如， `batch=16`），直接指定每个批次的图像数量。
> - **自动模式（60% GPU 内存）**：使用 `batch=-1` 自动调整批量大小，以达到大约 60% 的 CUDA 内存利用率。
> - **具有利用率分数的自动模式**：设置一个分数值（例如， `batch=0.70`），以根据指定的 GPU 内存使用率分数调整批量大小。

>`rect = True` 使用长方形训练
>
>Setting "rect"=True allows you to train using rectangular images, not necessarily square ones. This allows for more efficient use of GPU memory as there's less need for padding spatial dimensions.
>
>[Custom input size: letterbox vs resizing · Issue #11350 ](https://github.com/ultralytics/yolov5/issues/11350)
>
>[About the rectangle training · Issue #4819](https://github.com/ultralytics/ultralytics/issues/4819)

### 增强设置和超参数

数据增强技术对于提高 YOLO 模型的鲁棒性和性能至关重要，它通过在[训练数据](https://www.ultralytics.com/glossary/training-data)中引入变异性，帮助模型更好地泛化到未见过的数据。下表概述了每个数据增强参数的目的和效果：

| 参数                                                         | 类型    | 默认值        | 范围          | 描述                                                         |
| :----------------------------------------------------------- | :------ | :------------ | :------------ | :----------------------------------------------------------- |
| [`hsv_h`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#hue-adjustment-hsv_h) | `float` | `0.015`       | `0.0 - 1.0`   | 通过色轮的一小部分调整图像的色调，从而引入颜色变化。帮助模型在不同的光照条件下进行泛化。 |
| [`hsv_s`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#saturation-adjustment-hsv_s) | `float` | `0.7`         | `0.0 - 1.0`   | 通过一小部分改变图像的饱和度，从而影响颜色的强度。可用于模拟不同的环境条件。 |
| [`hsv_v`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#brightness-adjustment-hsv_v) | `float` | `0.4`         | `0.0 - 1.0`   | 通过一小部分修改图像的明度（亮度），帮助模型在各种光照条件下表现良好。 |
| [`degrees`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#rotation-degrees) | `float` | `0.0`         | `0.0 - 180`   | 在指定的角度范围内随机旋转图像，提高模型识别各种方向物体的能力。 |
| [`translate`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#translation-translate) | `float` | `0.1`         | `0.0 - 1.0`   | 通过图像尺寸的一小部分在水平和垂直方向上平移图像，帮助学习检测部分可见的物体。 |
| [`scale`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#scale-scale) | `float` | `0.5`         | `>=0.0`       | 通过增益因子缩放图像，模拟物体与相机的不同距离。             |
| [`shear`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#shear-shear) | `float` | `0.0`         | `-180 - +180` | 按指定的角度错切图像，模仿从不同角度观察物体的效果。         |
| [`perspective`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#perspective-perspective) | `float` | `0.0`         | `0.0 - 0.001` | 对图像应用随机透视变换，增强模型理解 3D 空间中物体的能力。   |
| [`flipud`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#flip-up-down-flipud) | `float` | `0.0`         | `0.0 - 1.0`   | 以指定的概率将图像上下翻转，增加数据变化，而不影响物体的特征。 |
| [`fliplr`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#flip-left-right-fliplr) | `float` | `0.5`         | `0.0 - 1.0`   | 以指定的概率将图像左右翻转，有助于学习对称物体并增加数据集的多样性。 |
| [`bgr`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#bgr-channel-swap-bgr) | `float` | `0.0`         | `0.0 - 1.0`   | 以指定的概率将图像通道从 RGB 翻转到 BGR，有助于提高对不正确通道排序的鲁棒性。 |
| [`mosaic`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#mosaic-mosaic) | `float` | `1.0`         | `0.0 - 1.0`   | 将四个训练图像组合成一个，模拟不同的场景组成和物体交互。对于复杂的场景理解非常有效。 |
| [`mixup`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#mixup-mixup) | `float` | `0.0`         | `0.0 - 1.0`   | 混合两个图像及其标签，创建一个合成图像。通过引入标签噪声和视觉变化，增强模型的泛化能力。 |
| [`cutmix`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#cutmix-cutmix) | `float` | `0.0`         | `0.0 - 1.0`   | 组合两张图像的部分区域，创建局部混合，同时保持清晰的区域。通过创建遮挡场景来增强模型的鲁棒性。 |
| [`copy_paste`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#copy-paste-copy_paste) | `float` | `0.0`         | `0.0 - 1.0`   | *仅分割*。在图像中复制和粘贴对象，以增加对象实例。           |
| [`copy_paste_mode`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#copy-paste-mode-copy_paste_mode) | `str`   | `flip`        | -             | *仅分割*。指定了 `copy-paste` 要使用的策略。选项包括 `'flip'` 和 `'mixup'`. |
| [`auto_augment`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#auto-augment-auto_augment) | `str`   | `randaugment` | -             | *仅分类*。应用预定义的增强策略（`'randaugment'`, `'autoaugment'`或 `'augmix'`）通过视觉多样性来增强模型性能。 |
| [`erasing`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation/#random-erasing-erasing) | `float` | `0.4`         | `0.0 - 0.9`   | *仅分类*。在训练过程中随机擦除图像的区域，以鼓励模型关注不那么明显的特征。 |

## example

```sh
# Build a new model from YAML and start training from scratch
yolo detect train data=coco8.yaml model=yolo11n.yaml epochs=100 imgsz=640 project=myproject

# Start training from a pretrained *.pt model
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640 project=myproject

# Build a new model from YAML, transfer pretrained weights to it and start training
yolo detect train data=coco8.yaml model=yolo11n.yaml pretrained=yolo11n.pt epochs=100 imgsz=640 project=myproject
```

> `Multi-GPU Training`

```sh
# Start training from a pretrained *.pt model using GPUs 0 and 1
yolo detect train data=coco8.yaml model=yolo11n.pt epochs=100 imgsz=640 device=0,1 project=myproject
```

> `auto optimizer`

```sh
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=ultralytics/cfg/models/v8/yolo11n.yaml pretrained=weights/yolo11n.pt data=ultralytics/datasets/coco8.yaml project=myproject

#                                                                                                                                model可以直接设置为pt
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=weights/yolo11n.pt data=ultralytics/cfg/datasets/coco8.yaml project=myproject

#                                                        rtdetr 训练轮数更少
yolo detect train imgsz=640 batch=-1 workers=8 epochs=100 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=ultralytics/cfg/models/rt-detr/rtdetr-x.yaml pretrained=weights/rtdetr-x.pt data=ultralytics/cfg/datasets/coco8.yaml project=myproject

#                                                        rtdetr 训练轮数更少                                                       model可以直接设置为pt
yolo detect train imgsz=640 batch=-1 workers=8 epochs=100 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=weights/rtdetr-x.pt data=ultralytics/cfg/datasets/coco8.yaml project=myproject
```

> `SGD`

```sh
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 optimizer=SGD lr0=0.01 cos_lr=True device=0 model=ultralytics/cfg/models/v8/yolo11n.yaml pretrained=weights/yolo11n.pt data=ultralytics/cfg/datasets/coco8.yaml project=myproject

#                                                                                                                                                       model可以直接设置为pt
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 optimizer=SGD lr0=0.01 cos_lr=True device=0 model=weights/yolo11n.pt data=ultralytics/cfg/datasets/coco8.yaml project=myproject
```

> `Adam`

```sh
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 optimizer=AdamW lr0=0.001 cos_lr=True device=0 model=ultralytics/cfg/models/v8/yolo11n.yaml pretrained=weights/yolo11n.pt data=ultralytics/cfg/datasets/coco8.yaml project=myproject

#                                                                                                                                                          model可以直接设置为pt
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 optimizer=AdamW lr0=0.001 cos_lr=True device=0 model=weights/yolo11n.pt data=ultralytics/cfg/datasets/coco8.yaml project=myproject
```

> `resume`

```sh
#                                                                                                                                model=最后的pt
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=weights/last.pt data=ultralytics/cfg/datasets/coco8.yaml resume=True exist_ok=True project=myproject
```

## **不需要在模型配置中显示更改类别数**

> 会自动将nc调整为数据集的类别数量

```sh
> yolo detect train imgsz=640 batch=-1 epochs=300 optimizer=SGD lr0=0.01 cos_lr=True device=0 pretrained=weights/yolo11n.pt model=ultralytics/models/v8/yolo11n.yaml data=ultralytics/datasets/classes20.yaml

                   from  n    params  module                                       arguments
  0                  -1  1       464  ultralytics.nn.modules.Conv                  [3, 16, 3, 2]
  1                  -1  1      4672  ultralytics.nn.modules.Conv                  [16, 32, 3, 2]
  2                  -1  1      7360  ultralytics.nn.modules.C2f                   [32, 32, 1, True]
  3                  -1  1     18560  ultralytics.nn.modules.Conv                  [32, 64, 3, 2]
  4                  -1  2     49664  ultralytics.nn.modules.C2f                   [64, 64, 2, True]
  5                  -1  1     73984  ultralytics.nn.modules.Conv                  [64, 128, 3, 2]
  6                  -1  2    197632  ultralytics.nn.modules.C2f                   [128, 128, 2, True]
  7                  -1  1    295424  ultralytics.nn.modules.Conv                  [128, 256, 3, 2]
  8                  -1  1    460288  ultralytics.nn.modules.C2f                   [256, 256, 1, True]
  9                  -1  1    164608  ultralytics.nn.modules.SPPF                  [256, 256, 5]
 10                  -1  1         0  torch.nn.modules.upsampling.Upsample         [None, 2, 'nearest']
 11             [-1, 6]  1         0  ultralytics.nn.modules.Concat                [1]
 12                  -1  1    148224  ultralytics.nn.modules.C2f                   [384, 128, 1]
 13                  -1  1         0  torch.nn.modules.upsampling.Upsample         [None, 2, 'nearest']
 14             [-1, 4]  1         0  ultralytics.nn.modules.Concat                [1]
 15                  -1  1     37248  ultralytics.nn.modules.C2f                   [192, 64, 1]
 16                  -1  1     36992  ultralytics.nn.modules.Conv                  [64, 64, 3, 2]
 17            [-1, 12]  1         0  ultralytics.nn.modules.Concat                [1]
 18                  -1  1    123648  ultralytics.nn.modules.C2f                   [192, 128, 1]
 19                  -1  1    147712  ultralytics.nn.modules.Conv                  [128, 128, 3, 2]
 20             [-1, 9]  1         0  ultralytics.nn.modules.Concat                [1]
 21                  -1  1    493056  ultralytics.nn.modules.C2f                   [384, 256, 1]
 22        [15, 18, 21]  1    897664  ultralytics.nn.modules.Detect                [80, [64, 128, 256]]
yolo11n summary: 225 layers, 3157200 parameters, 3157184 gradients, 8.9 GFLOPs

Transferred 355/355 items from pretrained weights
Ultralytics YOLOv8.0.58  Python-3.10.9 torch-2.0.0+cu118 CUDA:0 (NVIDIA GeForce GTX 1080 Ti, 11264MiB)
yolo\engine\trainer: detect, train, model=ultralytics/models/v8/yolo11n.yaml, data=ultralytics/datasets/classes20.yaml, epochs=300, patience=50, batch=-1, imgsz=640, save=True, save_period=-1, cache=False, device=0, workers=8, project=None, name=None, exist_ok=False, pretrained=weights/yolo11n.pt, optimizer=SGD, verbose=True, seed=0, deterministic=True, single_cls=False, image_weights=False, rect=False, cos_lr=True, close_mosaic=10, resume=False, amp=True, overlap_mask=True, mask_ratio=4, dropout=0.0, val=True, split=val, save_json=False, save_hybrid=False, conf=None, iou=0.7, max_det=300, half=False, dnn=False, plots=True, source=None, show=False, save_txt=False, save_conf=False, save_crop=False, hide_labels=False, hide_conf=False, vid_stride=1, line_thickness=3, visualize=False, augment=False, agnostic_nms=False, classes=None, retina_masks=False, boxes=True, format=torchscript, keras=False, optimize=False, int8=False, dynamic=False, simplify=False, opset=None, workspace=4, nms=False, lr0=0.01, lrf=0.01, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, warmup_bias_lr=0.1, box=7.5, cls=0.5, dfl=1.5, fl_gamma=0.0, label_smoothing=0.0, nbs=64, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, mosaic=1.0, mixup=0.0, copy_paste=0.0, cfg=None, v5loader=False, tracker=botsort.yaml, save_dir=d:\code\ultralytics\runs\detect\train2
Overriding model.yaml nc=80 with nc=20        # 这里自动覆盖了旧的类别数

                   from  n    params  module                                       arguments
  0                  -1  1       464  ultralytics.nn.modules.Conv                  [3, 16, 3, 2]
  1                  -1  1      4672  ultralytics.nn.modules.Conv                  [16, 32, 3, 2]
  2                  -1  1      7360  ultralytics.nn.modules.C2f                   [32, 32, 1, True]
  3                  -1  1     18560  ultralytics.nn.modules.Conv                  [32, 64, 3, 2]
  4                  -1  2     49664  ultralytics.nn.modules.C2f                   [64, 64, 2, True]
  5                  -1  1     73984  ultralytics.nn.modules.Conv                  [64, 128, 3, 2]
  6                  -1  2    197632  ultralytics.nn.modules.C2f                   [128, 128, 2, True]
  7                  -1  1    295424  ultralytics.nn.modules.Conv                  [128, 256, 3, 2]
  8                  -1  1    460288  ultralytics.nn.modules.C2f                   [256, 256, 1, True]
  9                  -1  1    164608  ultralytics.nn.modules.SPPF                  [256, 256, 5]
 10                  -1  1         0  torch.nn.modules.upsampling.Upsample         [None, 2, 'nearest']
 11             [-1, 6]  1         0  ultralytics.nn.modules.Concat                [1]
 12                  -1  1    148224  ultralytics.nn.modules.C2f                   [384, 128, 1]
 13                  -1  1         0  torch.nn.modules.upsampling.Upsample         [None, 2, 'nearest']
 14             [-1, 4]  1         0  ultralytics.nn.modules.Concat                [1]
 15                  -1  1     37248  ultralytics.nn.modules.C2f                   [192, 64, 1]
 16                  -1  1     36992  ultralytics.nn.modules.Conv                  [64, 64, 3, 2]
 17            [-1, 12]  1         0  ultralytics.nn.modules.Concat                [1]
 18                  -1  1    123648  ultralytics.nn.modules.C2f                   [192, 128, 1]
 19                  -1  1    147712  ultralytics.nn.modules.Conv                  [128, 128, 3, 2]
 20             [-1, 9]  1         0  ultralytics.nn.modules.Concat                [1]
 21                  -1  1    493056  ultralytics.nn.modules.C2f                   [384, 256, 1]
 22        [15, 18, 21]  1    755212  ultralytics.nn.modules.Detect                [20, [64, 128, 256]]
yolo11n summary: 225 layers, 3014748 parameters, 3014732 gradients, 8.2 GFLOPs

Transferred 319/355 items from pretrained weights
TensorBoard: Start with 'tensorboard --logdir d:\code\ultralytics\runs\detect\train', view at http://localhost:6006/
AMP: running Automatic Mixed Precision (AMP) checks with yolo11n...
AMP: checks passed
AutoBatch: Computing optimal batch size for imgsz=640
AutoBatch: CUDA:0 (NVIDIA GeForce GTX 1080 Ti) 11.00G total, 0.10G reserved, 0.07G allocated, 10.83G free
      Params      GFLOPs  GPU_mem (GB)  forward (ms) backward (ms)                   input                  output
     3014748       8.215         0.210         28.59         17.95        (1, 3, 640, 640)                    list
     3014748       16.43         0.296         13.96         21.27        (2, 3, 640, 640)                    list
     3014748       32.86         0.581         12.96         20.99        (4, 3, 640, 640)                    list
     3014748       65.72         1.065         20.27          28.6        (8, 3, 640, 640)                    list
     3014748       131.4         2.334         34.56         48.56       (16, 3, 640, 640)                    list
AutoBatch: Using batch-size 50 for CUDA:0 7.30G/11.00G (66%)
optimizer: SGD(lr=0.01) with parameter groups 57 weight(decay=0.0), 64 weight(decay=0.000390625), 63 bias
train: Scanning D:\code\datasets\classes20\labels\train.cache... 5266 images, 0 backgrounds, 0 corrupt: 100%|██████████
val: Scanning D:\code\datasets\classes20\labels\val.cache... 586 images, 0 backgrounds, 0 corrupt: 100%|██████████| 586
Plotting labels to d:\code\ultralytics\runs\detect\train\labels.jpg...
Image sizes 640 train, 640 val
Using 8 dataloader workers
Logging results to d:\code\ultralytics\runs\detect\train
Starting training for 300 epochs...
```

> 自动调整 `nc` 的代码在 `ultralytics/nn/task.py`

```python
        ch = self.yaml['ch'] = self.yaml.get('ch', ch)  # input channels
        if nc and nc != self.yaml['nc']:    # 使用data config中的names长度覆盖模型配置文件中的类别
            LOGGER.info(f"Overriding model.yaml nc={self.yaml['nc']} with nc={nc}")
            self.yaml['nc'] = nc  # override yaml value
```

## 训练时出现的问题

### 训练 `obj_loss` 增大 | reduce FPs | 解决特殊场景模型拍摄日常目标的FP数量过多

> [how to use Background images in training? · Issue #2844 · ultralytics/yolov5 (github.com)](https://github.com/ultralytics/yolov5/issues/2844)
>
> 在图片训练文件夹 `images/train` 中添加背景图片文件，比如coco或者voc数据集的一些照片
>
> 不需要添加空白label txt文件，添加了也不会出错
>
> `(if no objects in image, no `*.txt` file is required).`
>
> [目标检测（降低误检测率及小目标检测系列笔记）](https://blog.csdn.net/weixin_44836143/article/details/105952819)

```sh
train: Scanning D:\code\datasets\classes20\labels\train... 5266 images, 1000 backgrounds, 0 corrupt: 100%|██████████|
train: New cache created: D:\code\datasets\classes20\labels\train.cache
val: Scanning D:\code\datasets\classes20\labels\val... 586 images, 0 backgrounds, 0 corrupt: 100%|██████████|
val: New cache created: D:\code\datasets\classes20\labels\val.cache
```

# [验证](https://docs.ultralytics.com/zh/modes/val/)

## 使用示例

在 coco8 数据集上验证训练过的 yolo11n 模型的准确性。由于 `model` 保留了其训练的 `data` 和参数作为模型属性，因此无需传递任何参数。有关完整的导出参数列表，请参阅下面的参数部分。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load an official model
model = YOLO("path/to/best.pt")  # load a custom model

# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.box.map  # map50-95
metrics.box.map50  # map50
metrics.box.map75  # map75
metrics.box.maps  # a list contains map50-95 of each category
```

> CLI

```sh
yolo detect val model=yolo11n.pt      # val official model
yolo detect val model=path/to/best.pt # val custom model
```

## 参数

在验证 YOLO 模型时，可以微调多个参数以优化评估过程。这些参数控制着输入图像大小、批量处理和性能阈值等方面。以下是每个参数的详细分解，旨在帮助您有效地自定义验证设置。

| 参数           | 类型        | 默认值  | 描述                                                         |
| :------------- | :---------- | :------ | :----------------------------------------------------------- |
| `data`         | `str`       | `None`  | 指定数据集配置文件（例如， `coco8.yaml`）的路径。 此文件包含指向 [验证数据的路径](https://www.ultralytics.com/glossary/validation-data)，类别名称和类别数量。 |
| `imgsz`        | `int`       | `640`   | 定义输入图像的大小。所有图像在处理前都会调整为此尺寸。较大的尺寸可能会提高小目标的准确性，但会增加计算时间。 |
| `batch`        | `int`       | `16`    | 设置每个批次的图像数量。较高的值能更有效地利用 GPU 内存，但需要更多的 VRAM。根据可用的硬件资源进行调整。 |
| `save_json`    | `bool`      | `False` | 可视化参数： `True`，将结果保存到 JSON 文件中，以便进一步分析、与其他工具集成或提交到 COCO 等评估服务器。 |
| `conf`         | `float`     | `0.001` | 设置检测的最小置信度阈值。较低的值会提高召回率，但也可能引入更多的假阳性。在[验证](https://docs.ultralytics.com/zh/modes/val/)期间用于计算精确率-召回率曲线。 |
| `iou`          | `float`     | `0.7`   | 设置[交并比（Intersection Over Union）](https://www.ultralytics.com/glossary/intersection-over-union-iou)阈值，用于[非极大值抑制（Non-Maximum Suppression）](https://www.ultralytics.com/glossary/non-maximum-suppression-nms)。控制重复检测的消除。 |
| `max_det`      | `int`       | `300`   | 限制每幏图像的最大检测数量。在密集场景中非常有用，可防止过度检测和管理计算资源。 |
| `half`         | `bool`      | `True`  | 启用半[精度](https://www.ultralytics.com/glossary/precision) (FP16) 计算，从而减少内存使用量，并可能在对[准确性](https://www.ultralytics.com/glossary/accuracy)影响最小的情况下提高速度。 |
| `device`       | `str`       | `None`  | 指定验证的设备（`cpu`, `cuda:0`，等等）。当 `None`，自动选择最佳可用设备。多个 CUDA 设备可以用逗号分隔指定。 |
| `dnn`          | `bool`      | `False` | 可视化参数： `True`，使用 [OpenCV](https://www.ultralytics.com/glossary/opencv) DNN 模块进行 ONNX 模型推理，从而提供了一种替代 [PyTorch](https://www.ultralytics.com/glossary/pytorch) 推理方法。 |
| `plots`        | `bool`      | `False` | 当设置为 `True`，生成并保存预测与真实值的对比图、混淆矩阵和 PR 曲线，以便对模型性能进行可视化评估。 |
| `classes`      | `list[int]` | `None`  | 指定要训练的类 ID 列表。可用于在评估期间过滤并仅关注某些类。 |
| `rect`         | `bool`      | `True`  | 可视化参数： `True`，使用矩形推理进行批处理，减少填充，并通过以原始宽高比处理图像来潜在地提高速度和效率。 |
| `split`        | `str`       | `'val'` | 确定用于验证的数据集分割（`val`, `test`或 `train`）。 允许灵活选择数据段进行性能评估。 |
| `project`      | `str`       | `None`  | 用于保存验证输出的项目目录的名称。有助于组织来自不同实验或模型的结果。 |
| `name`         | `str`       | `None`  | 验证运行的名称。用于在项目文件夹中创建一个子目录，用于存储验证日志和输出。 |
| `verbose`      | `bool`      | `False` | 可视化参数： `True`，在验证过程中显示详细信息，包括每个类别的指标、批次进度和其他调试信息。 |
| `save_txt`     | `bool`      | `False` | 可视化参数： `True`，将检测结果保存在文本文件中，每个图像对应一个文件，可用于进一步分析、自定义后处理或与其他系统集成。 |
| `save_conf`    | `bool`      | `False` | 可视化参数： `True`，在保存的文本文件中包含置信度值，当 `save_txt` 已启用，提供更详细的输出以供分析和过滤。 |
| `workers`      | `int`       | `8`     | 用于数据加载的工作线程数。较高的值可以加快数据预处理速度，但可能会增加 CPU 使用率。设置为 0 使用主线程，这在某些环境中可能更稳定。 |
| `augment`      | `bool`      | `False` | 启用测试时增强（TTA），通过对输入的转换版本运行推理，从而可能提高检测精度，但会牺牲推理速度。 |
| `agnostic_nms` | `bool`      | `False` | 启用与类别无关的 [非极大值抑制](https://www.ultralytics.com/glossary/non-maximum-suppression-nms)，它合并重叠的框，而不管其预测的类别如何。对于以实例为中心的应用程序很有用。 |
| `single_cls`   | `bool`      | `False` | 在验证期间将所有类别视为单一类别。这对于评估二元检测任务中的模型性能或类别区分并不重要时非常有用。 |
| `visualize`    | `bool`      | `False` | 可视化每张图像的真值、真正例、假正例和假反例。 有助于调试和模型解释。 |

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
> `savehybrid` 会合并已知的labels，导致得分很高

## Example

### torch

```sh
yolo detect val imgsz=640 save_json=True save_txt=True save_conf=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.pt device=0 project=myproject
```

### torchscript

```sh
yolo detect val imgsz=640 save_json=True save_txt=True save_conf=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.torchscript device=0 project=myproject
```

### onnx

> 注意:
>
> `onnxruntime` 和 `onnxruntime-gpu` 不要同时安装，否则使用 `gpu` 推理时速度会很慢，如果同时安装了2个包，要全部卸载，再安装 `onnxruntime-gpu` 才能使用gpu推理，否则gpu速度会很慢

```sh
yolo detect val imgsz=640 save_json=True save_txt=True save_conf=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.onnx device=0 project=myproject
```

### openvino

> 注意：openvino没法使用cuda，但是使用 --device 0 会提高推理速度

```sh
yolo detect val imgsz=640 save_json=True save_txt=True save_conf=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n_openvnio_model device=cpu project=myproject
```

### tensorrt

```sh
yolo detect val imgsz=640 save_json=True save_txt=True save_conf=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.onnx device=0 half=True project=myproject
```

# [预测](https://docs.ultralytics.com/zh/modes/predict/)

## 使用示例

Ultralytics YOLO 模型在进行推理时返回一个 Python `Results` 对象列表，或者当传入 `stream=True` 时，返回一个内存高效的 Python `Results` 对象生成器：

> 使用 `stream=False` 返回列表

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # pretrained YOLO11n model

# Run batched inference on a list of images
results = model(["image1.jpg", "image2.jpg"])  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk
```

> 使用 `stream=True` 返回生成器

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # pretrained YOLO11n model

# Run batched inference on a list of images
results = model(["image1.jpg", "image2.jpg"], stream=True)  # return a generator of Results objects

# Process results generator
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk
```

## 推理来源

如下表所示，YOLO11 可以处理不同类型的输入源以进行推理。这些源包括静态图像、视频流和各种数据格式。该表还指示了每个源是否可以在流模式下与参数一起使用 `stream=True` ✅。流模式有利于处理视频或直播流，因为它会创建一个结果生成器，而不是将所有帧加载到内存中。

> 使用 `stream=True` 用于处理长视频或大型数据集，以有效管理内存。当 `stream=False`时，所有帧或数据点的结果都存储在内存中，这会迅速累积，并导致大型输入出现内存不足错误。相反， `stream=True` 采用生成器，仅将当前帧或数据点的结果保存在内存中，从而显著降低内存消耗并防止内存溢出问题。

| 来源                                                  | 示例                                       | 类型            | 备注                                                         |
| :---------------------------------------------------- | :----------------------------------------- | :-------------- | :----------------------------------------------------------- |
| 图像                                                  | `'image.jpg'`                              | `str` 或 `Path` | 单个图像文件。                                               |
| URL                                                   | `'https://ultralytics.com/images/bus.jpg'` | `str`           | 图像的URL。                                                  |
| 截图                                                  | `'screen'`                                 | `str`           | 截取屏幕截图。                                               |
| PIL                                                   | `Image.open('image.jpg')`                  | `PIL.Image`     | 具有RGB通道的HWC格式。                                       |
| [OpenCV](https://www.ultralytics.com/glossary/opencv) | `cv2.imread('image.jpg')`                  | `np.ndarray`    | 具有BGR通道的HWC格式 `uint8 (0-255)`.                        |
| numpy                                                 | `np.zeros((640,1280,3))`                   | `np.ndarray`    | 具有BGR通道的HWC格式 `uint8 (0-255)`.                        |
| torch                                                 | `torch.zeros(16,3,320,640)`                | `torch.Tensor`  | 具有RGB通道的BCHW格式 `float32 (0.0-1.0)`.                   |
| CSV                                                   | `'sources.csv'`                            | `str` 或 `Path` | 包含图像、视频或目录路径的CSV文件。                          |
| 视频 ✅                                                | `'video.mp4'`                              | `str` 或 `Path` | MP4、AVI等格式的视频文件。                                   |
| 目录 ✅                                                | `'path/'`                                  | `str` 或 `Path` | 包含图像或视频的目录的路径。                                 |
| glob ✅                                                | `'path/*.jpg'`                             | `str`           | 用于匹配多个文件的Glob模式。使用 `*` 字符作为通配符。        |
| YouTube ✅                                             | `'https://youtu.be/LNwODJXcvt4'`           | `str`           | YouTube视频的URL。                                           |
| 流 ✅                                                  | `'rtsp://example.com/media.mp4'`           | `str`           | 用于流媒体协议的URL，例如RTSP、RTMP、TCP或IP地址。           |
| 多流 ✅                                                | `'list.streams'`                           | `str` 或 `Path` | `*.streams` 包含每行一个流 URL 的文本文件，例如，8 个流将以 batch-size 8 运行。 |
| 网络摄像头 ✅                                          | `0`                                        | `int`           | 用于运行推理的已连接摄像头设备的索引。                       |

以下是使用每种来源类型的代码示例：

图像

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Define path to the image file
source = "path/to/image.jpg"

# Run inference on the source
results = model(source)  # list of Results objects
```

截图

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Define current screenshot as source
source = "screen"

# Run inference on the source
results = model(source)  # list of Results objects
```
URL

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Define remote image or video URL
source = "https://ultralytics.com/images/bus.jpg"

# Run inference on the source
results = model(source)  # list of Results objects
```

PIL

```python
from PIL import Image

from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Open an image using PIL
source = Image.open("path/to/image.jpg")

# Run inference on the source
results = model(source)  # list of Results objects
```

OpenCV

```python
import cv2

from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Read an image using OpenCV
source = cv2.imread("path/to/image.jpg")

# Run inference on the source
results = model(source)  # list of Results objects
```

numpy

```python
import numpy as np

from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Create a random numpy array of HWC shape (640, 640, 3) with values in range [0, 255] and type uint8
source = np.random.randint(low=0, high=255, size=(640, 640, 3), dtype="uint8")

# Run inference on the source
results = model(source)  # list of Results objects
```

torch

```python
import torch

from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Create a random torch tensor of BCHW shape (1, 3, 640, 640) with values in range [0, 1] and type float32
source = torch.rand(1, 3, 640, 640, dtype=torch.float32)

# Run inference on the source
results = model(source)  # list of Results objects
```

CSV

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Define a path to a CSV file with images, URLs, videos and directories
source = "path/to/file.csv"

# Run inference on the source
results = model(source)  # list of Results objects
```

视频

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Define path to video file
source = "path/to/video.mp4"

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

目录下

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Define path to directory containing images and videos for inference
source = "path/to/dir"

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

glob

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Define a glob search for all JPG files in a directory
source = "path/to/dir/*.jpg"

# OR define a recursive glob search for all JPG files including subdirectories
source = "path/to/dir/**/*.jpg"

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

YouTube

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Define source as YouTube video URL
source = "https://youtu.be/LNwODJXcvt4"

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

流

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Single stream with batch-size 1 inference
source = "rtsp://example.com/media.mp4"  # RTSP, RTMP, TCP, or IP streaming address

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

多流

> 要同时处理多个视频流，请使用包含流媒体源的 `.streams` 文本文件。模型将运行批量推理，其中批量大小等于流的数量。此设置可以高效地并发处理多个源。

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Multiple streams with batched inference (e.g., batch-size 8 for 8 streams)
source = "path/to/list.streams"  # *.streams text file with one streaming address per line

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

> 示例 `.streams` 文本文件：

```
rtsp://example.com/media1.mp4
rtsp://example.com/media2.mp4
rtmp://example2.com/live
tcp://192.168.1.100:554
...
```

> 文件中的每一行代表一个流媒体源，允许您同时监控多个视频流并对其执行推理。

网络摄像头

> 您可以通过将特定摄像头的索引传递给 `source`.

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Run inference on the source
results = model(source=0, stream=True)  # generator of Results objects
```


## 推理参数

`model.predict()` 在推理时接受多个参数，可以用来覆盖默认值：

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Run inference on 'bus.jpg' with arguments
model.predict("https://ultralytics.com/images/bus.jpg", save=True, imgsz=320, conf=0.5)
```

推理参数：

| 参数            | 类型             | 默认值                 | 描述                                                         |
| :-------------- | :--------------- | :--------------------- | :----------------------------------------------------------- |
| `source`        | `str`            | `'ultralytics/assets'` | 指定推理的数据源。可以是图像路径、视频文件、目录、URL 或实时馈送的设备 ID。 支持多种格式和来源，从而可以在[不同类型的输入](https://docs.ultralytics.com/zh/modes/predict/#inference-sources)上灵活应用。 |
| `conf`          | `float`          | `0.25`                 | 设置检测的最小置信度阈值。 将忽略置信度低于此阈值的检测到的对象。 调整此值有助于减少误报。 |
| `iou`           | `float`          | `0.7`                  | 用于非极大值抑制 (NMS) 的 [Intersection Over Union](https://www.ultralytics.com/glossary/intersection-over-union-iou) (IoU) 阈值。较低的值会通过消除重叠的框来减少检测结果，这对于减少重复项很有用。 |
| `imgsz`         | `int` 或 `tuple` | `640`                  | 定义推理的图像大小。可以是一个整数 `640` 表示正方形调整大小，也可以是 (height, width) 元组。适当的大小调整可以提高检测 [准确性](https://www.ultralytics.com/glossary/accuracy) 和处理速度。 |
| `rect`          | `bool`           | `True`                 | 如果启用，则对图像较短的一边进行最小填充，直到可以被步长整除，以提高推理速度。如果禁用，则在推理期间将图像填充为正方形。 |
| `half`          | `bool`           | `False`                | 启用半[精度](https://www.ultralytics.com/glossary/precision) (FP16) 推理，这可以加快在支持的 GPU 上的模型推理速度，同时对准确性的影响极小。 |
| `device`        | `str`            | `None`                 | 指定用于推理的设备（例如， `cpu`, `cuda:0` 或 `0`）。允许用户在 CPU、特定 GPU 或其他计算设备之间进行选择，以执行模型。 |
| `batch`         | `int`            | `1`                    | 指定推理的批处理大小（仅在源为以下情况时有效： [目录、视频文件或 `.txt` 文件](https://docs.ultralytics.com/zh/modes/predict/#inference-sources))。更大的批处理大小可以提供更高的吞吐量，从而缩短推理所需的总时间。 |
| `max_det`       | `int`            | `300`                  | 每张图像允许的最大检测数量。限制模型在单次推理中可以检测到的对象总数，防止在密集场景中产生过多的输出。 |
| `vid_stride`    | `int`            | `1`                    | 视频输入的帧步长。允许跳过视频中的帧，以加快处理速度，但会降低时间分辨率。值为 1 时处理每一帧，值越高跳过的帧越多。 |
| `stream_buffer` | `bool`           | `False`                | 确定是否为视频流排队传入帧。如果 `False`，旧帧会被丢弃以适应新帧（针对实时应用进行了优化）。如果 `True`，在缓冲区中对新帧进行排队，确保不跳过任何帧，但如果推理 FPS 低于流 FPS，则会导致延迟。 |
| `visualize`     | `bool`           | `False`                | 激活推理期间模型特征的可视化，从而深入了解模型正在“看到”的内容。这对于调试和模型解释非常有用。 |
| `augment`       | `bool`           | `False`                | 启用测试时增强 (TTA) 进行预测，可能会提高检测的鲁棒性，但会降低推理速度。 |
| `agnostic_nms`  | `bool`           | `False`                | 启用与类别无关的非极大值抑制 (NMS)，它会合并不同类别的重叠框。在类别重叠很常见的多类别检测场景中非常有用。 |
| `classes`       | `list[int]`      | `None`                 | 将预测结果筛选到一组类别 ID。只会返回属于指定类别的检测结果。这对于专注于多类别检测任务中的相关对象非常有用。 |
| `retina_masks`  | `bool`           | `False`                | 返回高分辨率分割掩码。返回的掩码（`masks.data`）如果启用，将与原始图像大小匹配。如果禁用，它们将具有推理期间使用的图像大小。 |
| `embed`         | `list[int]`      | `None`                 | 指定从中提取特征向量或 [embeddings](https://www.ultralytics.com/glossary/embeddings) 的层。对于诸如聚类或相似性搜索之类的下游任务非常有用。 |
| `project`       | `str`            | `None`                 | 如果 `save` 已启用，则为保存预测输出的项目目录的名称。       |
| `name`          | `str`            | `None`                 | 预测运行的名称。用于在项目文件夹中创建一个子目录，如果 `save` 已启用，则为保存预测输出的项目目录的名称。 |
| `stream`        | `bool`           | `False`                | 通过返回 Results 对象的生成器而不是一次将所有帧加载到内存中，从而为长视频或大量图像启用内存高效处理。 |
| `verbose`       | `bool`           | `True`                 | 控制是否在终端中显示详细的推理日志，从而提供有关预测过程的实时反馈。 |

可视化参数：

| 参数          | 类型          | 默认值          | 描述                                                         |
| :------------ | :------------ | :-------------- | :----------------------------------------------------------- |
| `show`        | `bool`        | `False`         | 可视化参数： `True`，则在窗口中显示带注释的图像或视频。这对于开发或测试期间的即时视觉反馈非常有用。 |
| `save`        | `bool`        | `False or True` | 启用将带注释的图像或视频保存到文件。这对于文档编制、进一步分析或共享结果非常有用。使用 CLI 时默认为 True，在 python 中使用时默认为 False。 |
| `save_frames` | `bool`        | `False`         | 处理视频时，将各个帧另存为图像。这对于提取特定帧或进行详细的逐帧分析非常有用。 |
| `save_txt`    | `bool`        | `False`         | 以文本文件格式保存检测结果，格式如下： `[class] [x_center] [y_center] [width] [height] [confidence]`。 有助于与其他分析工具集成。 |
| `save_conf`   | `bool`        | `False`         | 在保存的文本文件中包含置信度分数。 增强了可用于后处理和分析的细节。 |
| `save_crop`   | `bool`        | `False`         | 保存检测到的裁剪图像。 有助于数据集增强、分析或为特定对象创建重点数据集。 |
| `show_labels` | `bool`        | `True`          | 在可视化输出中显示每个检测的标签。 能够立即理解检测到的对象。 |
| `show_conf`   | `bool`        | `True`          | 在标签旁边显示每个检测的置信度分数。 可以深入了解模型对每次检测的确定性。 |
| `show_boxes`  | `bool`        | `True`          | 在检测到的对象周围绘制边界框。 这对于在图像或视频帧中以可视方式识别和定位对象至关重要。 |
| `line_width`  | `None or int` | `None`          | 指定边界框的线条宽度。 如果 `None`，则线条宽度会根据图像大小自动调整。 提供视觉自定义以提高清晰度。 |

## 图像和视频格式

YOLO11 支持各种图像和视频格式，如 [ultralytics/data/utils.py](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/data/utils.py) 中所指定。请参见下表，了解有效的后缀和示例预测命令。

### 图像

下表包含有效的 Ultralytics 图像格式。

| 图像后缀 | 示例预测命令                     | 参考                                                         |
| :------- | :------------------------------- | :----------------------------------------------------------- |
| `.bmp`   | `yolo predict source=image.bmp`  | [Microsoft BMP 文件格式](https://en.wikipedia.org/wiki/BMP_file_format) |
| `.dng`   | `yolo predict source=image.dng`  | [Adobe DNG](https://en.wikipedia.org/wiki/Digital_Negative)  |
| `.jpeg`  | `yolo predict source=image.jpeg` | [JPEG](https://en.wikipedia.org/wiki/JPEG)                   |
| `.jpg`   | `yolo predict source=image.jpg`  | [JPEG](https://en.wikipedia.org/wiki/JPEG)                   |
| `.mpo`   | `yolo predict source=image.mpo`  | [多图片对象](https://fileinfo.com/extension/mpo)             |
| `.png`   | `yolo predict source=image.png`  | [便携式网络图形](https://en.wikipedia.org/wiki/PNG)          |
| `.tif`   | `yolo predict source=image.tif`  | [标签图像文件格式](https://en.wikipedia.org/wiki/TIFF)       |
| `.tiff`  | `yolo predict source=image.tiff` | [标签图像文件格式](https://en.wikipedia.org/wiki/TIFF)       |
| `.webp`  | `yolo predict source=image.webp` | [WebP](https://en.wikipedia.org/wiki/WebP)                   |
| `.pfm`   | `yolo predict source=image.pfm`  | [便携式浮点图](https://en.wikipedia.org/wiki/Netpbm#File_formats) |
| `.HEIC`  | `yolo predict source=image.HEIC` | [高效率图像格式](https://en.wikipedia.org/wiki/HEIF)         |

### 视频

下表包含有效的 Ultralytics 视频格式。

| 视频后缀 | 示例预测命令                     | 参考                                                         |
| :------- | :------------------------------- | :----------------------------------------------------------- |
| `.asf`   | `yolo predict source=video.asf`  | [高级系统格式](https://en.wikipedia.org/wiki/Advanced_Systems_Format) |
| `.avi`   | `yolo predict source=video.avi`  | [音视频交错格式](https://en.wikipedia.org/wiki/Audio_Video_Interleave) |
| `.gif`   | `yolo predict source=video.gif`  | [图像互换格式](https://en.wikipedia.org/wiki/GIF)            |
| `.m4v`   | `yolo predict source=video.m4v`  | [MPEG-4 Part 14](https://en.wikipedia.org/wiki/M4V)          |
| `.mkv`   | `yolo predict source=video.mkv`  | [Matroska](https://en.wikipedia.org/wiki/Matroska)           |
| `.mov`   | `yolo predict source=video.mov`  | [QuickTime 文件格式](https://en.wikipedia.org/wiki/QuickTime_File_Format) |
| `.mp4`   | `yolo predict source=video.mp4`  | [MPEG-4 Part 14 - 维基百科](https://en.wikipedia.org/wiki/MPEG-4_Part_14) |
| `.mpeg`  | `yolo predict source=video.mpeg` | [MPEG-1 Part 2](https://en.wikipedia.org/wiki/MPEG-1)        |
| `.mpg`   | `yolo predict source=video.mpg`  | [MPEG-1 Part 2](https://en.wikipedia.org/wiki/MPEG-1)        |
| `.ts`    | `yolo predict source=video.ts`   | [MPEG 传输流](https://en.wikipedia.org/wiki/MPEG_transport_stream) |
| `.wmv`   | `yolo predict source=video.wmv`  | [Windows Media 视频](https://en.wikipedia.org/wiki/Windows_Media_Video) |
| `.webm`  | `yolo predict source=video.webm` | [WebM 项目](https://en.wikipedia.org/wiki/WebM)              |

## 处理结果

所有 Ultralytics `predict()` 调用将返回一个 `Results` 对象列表：

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")
results = model(
    [
        "https://ultralytics.com/images/bus.jpg",
        "https://ultralytics.com/images/zidane.jpg",
    ]
)  # batch inference
```

`Results` 对象具有以下属性：

| 属性         | 类型                  | 描述                                                        |
| :----------- | :-------------------- | :---------------------------------------------------------- |
| `orig_img`   | `np.ndarray`          | 原始图像，以 numpy 数组形式呈现。                           |
| `orig_shape` | `tuple`               | 原始图像的形状，格式为（高度，宽度）。                      |
| `boxes`      | `Boxes, optional`     | 一个 Boxes 对象，包含检测到的边界框。                       |
| `masks`      | `Masks, optional`     | 一个 Masks 对象，包含检测到的掩码。                         |
| `probs`      | `Probs, optional`     | 一个 Probs 对象，包含分类任务中每个类别的概率。             |
| `keypoints`  | `Keypoints, optional` | 一个 Keypoints 对象，包含每个对象检测到的关键点。           |
| `obb`        | `OBB, optional`       | 旋转框检测 对象，包含定向边界框。                           |
| `speed`      | `dict`                | 一个字典，包含预处理、推理和后处理的速度，单位为毫秒/图像。 |
| `names`      | `dict`                | 一个将类索引映射到类名称的字典。                            |
| `path`       | `str`                 | 图像文件的路径。                                            |
| `save_dir`   | `str, optional`       | 用于保存结果的目录。                                        |

`Results` 对象具有以下方法：

| 方法          | 返回类型               | 描述                                                         |
| :------------ | :--------------------- | :----------------------------------------------------------- |
| `update()`    | `None`                 | 用新的检测数据（方框、遮罩、问题、旋转框检测、关键点）更新结果对象。 |
| `cpu()`       | `Results`              | 返回 Results 对象的副本，其中所有 tensor 都已移动到 CPU 内存。 |
| `numpy()`     | `Results`              | 返回 Results 对象的副本，其中所有 tensor 都已转换为 numpy 数组。 |
| `cuda()`      | `Results`              | 返回 Results 对象的副本，其中所有 tensor 都已移动到 GPU 内存。 |
| `to()`        | `Results`              | 返回 Results 对象的副本，其中 tensor 已移动到指定的设备和数据类型。 |
| `new()`       | `Results`              | 创建一个新的 Results 对象，该对象具有相同的图像、路径、名称和速度属性。 |
| `plot()`      | `np.ndarray`           | 在输入的 RGB 图像上绘制检测结果，并返回带注释的图像。        |
| `show()`      | `None`                 | 显示带有注释的推理结果的图像。                               |
| `save()`      | `str`                  | 将带注释的推理结果图像保存到文件并返回文件名。               |
| `verbose()`   | `str`                  | 返回每个任务的日志字符串，详细说明检测和分类结果。           |
| `save_txt()`  | `str`                  | 将检测结果保存到文本文件，并返回保存文件的路径。             |
| `save_crop()` | `None`                 | 将裁剪的检测图像保存到指定目录。                             |
| `summary()`   | `List[Dict[str, Any]]` | 将推理结果转换为汇总字典，可以选择进行归一化。               |
| `to_df()`     | `DataFrame`            | 将检测结果转换为 Pandas DataFrame。                          |
| `to_csv()`    | `str`                  | 将检测结果转换为 CSV 格式。                                  |
| `to_xml()`    | `str`                  | 将检测结果转换为 XML 格式。                                  |
| `to_html()`   | `str`                  | 将检测结果转换为 HTML 格式。                                 |
| `to_json()`   | `str`                  | 将检测结果转换为 JSON 格式。                                 |
| `to_sql()`    | `None`                 | 将检测结果转换为 SQL 兼容格式并保存到数据库。                |

有关更多详细信息，请参见 [`Results` 类文档](https://docs.ultralytics.com/zh/reference/engine/results/).

### 边界框

`Boxes` 对象可用于索引、操作和将边界框转换为不同的格式。

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.boxes)  # print the Boxes object containing the detection bounding boxes
```

以下是 `Boxes` 类的方法和属性表，包括它们的名称、类型和描述：

| 名称      | 类型                  | 描述                                           |
| :-------- | :-------------------- | :--------------------------------------------- |
| `cpu()`   | 方法                  | 将对象移动到 CPU 内存。                        |
| `numpy()` | 方法                  | 将对象转换为 numpy 数组。                      |
| `cuda()`  | 方法                  | 将对象移动到 CUDA 内存。                       |
| `to()`    | 方法                  | 将对象移动到指定的设备。                       |
| `xyxy`    | 属性 (`torch.Tensor`) | 以 xyxy 格式返回边界框。                       |
| `conf`    | 属性 (`torch.Tensor`) | 返回边界框的置信度值。                         |
| `cls`     | 属性 (`torch.Tensor`) | 返回边界框的类别值。                           |
| `id`      | 属性 (`torch.Tensor`) | 返回边界框的跟踪 ID（如果可用）。              |
| `xywh`    | 属性 (`torch.Tensor`) | 以 xywh 格式返回边界框。                       |
| `xyxyn`   | 属性 (`torch.Tensor`) | 返回以原始图像大小归一化的 xyxy 格式的边界框。 |
| `xywhn`   | 属性 (`torch.Tensor`) | 返回以原始图像大小归一化的 xywh 格式的边界框。 |

有关更多详细信息，请参见 [`Boxes` 类文档](https://docs.ultralytics.com/zh/reference/engine/results/#ultralytics.engine.results.Boxes).

### 掩码

`Masks` 对象可用于索引、操作和将掩码转换为分割。

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n-seg Segment model
model = YOLO("yolo11n-seg.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.masks)  # print the Masks object containing the detected instance masks
```

以下是 `Masks` 类的方法和属性表，包括它们的名称、类型和描述：

| 名称      | 类型                  | 描述                                      |
| :-------- | :-------------------- | :---------------------------------------- |
| `cpu()`   | 方法                  | 返回 CPU 内存上的掩码 tensor。            |
| `numpy()` | 方法                  | 返回作为 numpy 数组的掩码 tensor。        |
| `cuda()`  | 方法                  | 返回 GPU 内存上的掩码 tensor。            |
| `to()`    | 方法                  | 返回具有指定设备和数据类型的掩码 tensor。 |
| `xyn`     | 属性 (`torch.Tensor`) | 表示为 tensor 的归一化分割列表。          |
| `xy`      | 属性 (`torch.Tensor`) | 表示为 tensor 的像素坐标中的分割列表。    |

有关更多详细信息，请参见 [`Masks` 类文档](https://docs.ultralytics.com/zh/reference/engine/results/#ultralytics.engine.results.Masks).

### 关键点

`Keypoints` 对象可用于索引、操作和归一化坐标。

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n-pose Pose model
model = YOLO("yolo11n-pose.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.keypoints)  # print the Keypoints object containing the detected keypoints
```

以下是 `Keypoints` 类的方法和属性表，包括它们的名称、类型和描述：

| 名称      | 类型                  | 描述                                              |
| :-------- | :-------------------- | :------------------------------------------------ |
| `cpu()`   | 方法                  | 返回 CPU 内存上的关键点 tensor。                  |
| `numpy()` | 方法                  | 返回作为 numpy 数组的关键点 tensor。              |
| `cuda()`  | 方法                  | 返回 GPU 内存上的关键点 tensor。                  |
| `to()`    | 方法                  | 返回具有指定设备和数据类型的关键点 tensor。       |
| `xyn`     | 属性 (`torch.Tensor`) | 表示为 tensor 的归一化关键点列表。                |
| `xy`      | 属性 (`torch.Tensor`) | 表示为 tensor 的像素坐标中的关键点列表。          |
| `conf`    | 属性 (`torch.Tensor`) | 如果可用，则返回关键点的置信度值，否则返回 None。 |

有关更多详细信息，请参见 [`Keypoints` 类文档](https://docs.ultralytics.com/zh/reference/engine/results/#ultralytics.engine.results.Keypoints).

### 概率

`Probs` 对象可用于索引、获取 `top1` 和 `top5` 分类的索引和分数。

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n-cls Classify model
model = YOLO("yolo11n-cls.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.probs)  # print the Probs object containing the detected class probabilities
```

下表总结了以下方法的属性： `Probs` 函数：

| 名称       | 类型                  | 描述                                             |
| :--------- | :-------------------- | :----------------------------------------------- |
| `cpu()`    | 方法                  | 返回 CPU 内存中 probs tensor 的副本。            |
| `numpy()`  | 方法                  | 返回 probs tensor 作为 numpy 数组的副本。        |
| `cuda()`   | 方法                  | 返回 GPU 内存中 probs tensor 的副本。            |
| `to()`     | 方法                  | 返回具有指定设备和数据类型的 probs tensor 副本。 |
| `top1`     | 属性 (`int`)          | 排名第一的类别的索引。                           |
| `top5`     | 属性 (`list[int]`)    | 排名前 5 的类别的索引。                          |
| `top1conf` | 属性 (`torch.Tensor`) | 排名第一的类别的置信度。                         |
| `top5conf` | 属性 (`torch.Tensor`) | 排名前 5 的类别的置信度。                        |

有关更多详细信息，请参见 [`Probs` 类文档](https://docs.ultralytics.com/zh/reference/engine/results/#ultralytics.engine.results.Probs).

### 旋转框检测

`OBB` 对象可用于索引、操作和转换有向边界框为不同的格式。

```python
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n-obb.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/boats.jpg")  # results list

# View results
for r in results:
    print(r.obb)  # print the OBB object containing the oriented detection bounding boxes
```

以下是 `OBB` 类的方法和属性表，包括它们的名称、类型和描述：

| 名称        | 类型                  | 描述                                           |
| :---------- | :-------------------- | :--------------------------------------------- |
| `cpu()`     | 方法                  | 将对象移动到 CPU 内存。                        |
| `numpy()`   | 方法                  | 将对象转换为 numpy 数组。                      |
| `cuda()`    | 方法                  | 将对象移动到 CUDA 内存。                       |
| `to()`      | 方法                  | 将对象移动到指定的设备。                       |
| `conf`      | 属性 (`torch.Tensor`) | 返回边界框的置信度值。                         |
| `cls`       | 属性 (`torch.Tensor`) | 返回边界框的类别值。                           |
| `id`        | 属性 (`torch.Tensor`) | 返回边界框的跟踪 ID（如果可用）。              |
| `xyxy`      | 属性 (`torch.Tensor`) | 以 xyxy 格式返回水平框。                       |
| `xywhr`     | 属性 (`torch.Tensor`) | 以 xywhr 格式返回旋转框。                      |
| `xyxyxyxy`  | 属性 (`torch.Tensor`) | 以 xyxyxyxy 格式返回旋转框。                   |
| `xyxyxyxyn` | 属性 (`torch.Tensor`) | 返回由图像大小归一化的 xyxyxyxy 格式的旋转框。 |

有关更多详细信息，请参见 [`OBB` 类文档](https://docs.ultralytics.com/zh/reference/engine/results/#ultralytics.engine.results.OBB).

## 结果绘图

字段 `plot()` 方法在 `Results` 对象通过将检测到的对象（例如边界框、掩码、关键点和概率）叠加到原始图像上，从而方便预测的可视化。此方法将带注释的图像作为 NumPy 数组返回，从而可以轻松显示或保存。

```python
from PIL import Image

from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Run inference on 'bus.jpg'
results = model(["https://ultralytics.com/images/bus.jpg", "https://ultralytics.com/images/zidane.jpg"])  # results list

# Visualize the results
for i, r in enumerate(results):
    # Plot results image
    im_bgr = r.plot()  # BGR-order numpy array
    im_rgb = Image.fromarray(im_bgr[..., ::-1])  # RGB-order PIL image

    # Show results to screen (in supported environments)
    r.show()

    # Save results to disk
    r.save(filename=f"results{i}.jpg")
```

### `plot()` 方法参数

字段 `plot()` 方法支持各种参数来自定义输出：

| 参数         | 类型                   | 描述                                                         | 默认值            |
| :----------- | :--------------------- | :----------------------------------------------------------- | :---------------- |
| `conf`       | `bool`                 | 包括检测置信度分数。                                         | `True`            |
| `line_width` | `float`                | 边界框的线条宽度。如果图像大小为，则缩放 `None`.             | `None`            |
| `font_size`  | `float`                | 文本字体大小。如果图像大小为，则缩放 `None`.                 | `None`            |
| `font`       | `str`                  | 文本注释的字体名称。                                         | `'Arial.ttf'`     |
| `pil`        | `bool`                 | 将图像作为 PIL 图像对象返回。                                | `False`           |
| `img`        | `np.ndarray`           | 用于绘制图像的替代图像。如果未提供，则使用原始图像。 `None`. | `None`            |
| `im_gpu`     | `torch.Tensor`         | 用于更快进行掩码绘制的 GPU 加速图像。形状：(1, 3, 640, 640)。 | `None`            |
| `kpt_radius` | `int`                  | 绘制的关键点半径。                                           | `5`               |
| `kpt_line`   | `bool`                 | 用线条连接关键点。                                           | `True`            |
| `labels`     | `bool`                 | 在注释中包含类别标签。                                       | `True`            |
| `boxes`      | `bool`                 | 在图像上叠加边界框。                                         | `True`            |
| `masks`      | `bool`                 | 在图像上叠加掩码。                                           | `True`            |
| `probs`      | `bool`                 | 包含分类概率。                                               | `True`            |
| `show`       | `bool`                 | 使用默认图像查看器直接显示带注释的图像。                     | `False`           |
| `save`       | `bool`                 | 将带注释的图像保存到指定的文件中。 `filename`.               | `False`           |
| `filename`   | `str`                  | 如果指定了 ，则为保存带注释图像的文件的路径和名称。 `save` 是 `True`. | `None`            |
| `color_mode` | `str`                  | 指定颜色模式，例如“instance”或“class”。                      | `'class'`         |
| `txt_color`  | `tuple[int, int, int]` | 用于边界框和图像分类标签的 RGB 文本颜色。                    | `(255, 255, 255)` |

## 线程安全推理

当您在不同线程中并行运行多个 YOLO 模型时，确保推理过程中的线程安全至关重要。线程安全推理保证每个线程的预测都是隔离的，不会相互干扰，从而避免竞争条件，并确保输出的一致性和可靠性。

在多线程应用程序中使用 YOLO 模型时，为每个线程实例化单独的模型对象或采用线程局部存储以防止冲突非常重要：

```python
from threading import Thread

from ultralytics import YOLO


def thread_safe_predict(model, image_path):
    """Performs thread-safe prediction on an image using a locally instantiated YOLO model."""
    model = YOLO(model)
    results = model.predict(image_path)
    # Process results


# Starting threads that each have their own model instance
Thread(target=thread_safe_predict, args=("yolo11n.pt", "image1.jpg")).start()
Thread(target=thread_safe_predict, args=("yolo11n.pt", "image2.jpg")).start()
```

要深入了解 YOLO 模型的线程安全推理以及分步说明，请参阅我们的 [YOLO 线程安全推理指南](https://docs.ultralytics.com/zh/guides/yolo-thread-safe-inference/)。本指南将为您提供避免常见陷阱并确保多线程推理顺利运行所需的所有信息。

## 流媒体源 `for`-循环

这是一个使用 OpenCV (`cv2`) 和 YOLO 运行视频帧推理的 python 脚本。此脚本假定您已安装必要的软件包 (`opencv-python` 和 `ultralytics`）。

```python
import cv2

from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolo11n.pt")

# Open the video file
video_path = "path/to/your/video/file.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLO Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
```

## Example

### torch

```sh
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.pt source=ultralytics/assets/bus.jpg device=0 project=myproject

yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.pt source=../datasets/coco8/images/train2017 device=0 project=myproject
```

### torchscript

```sh
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.torchscript source=ultralytics/assets/bus.jpg device=0 project=myproject

yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.torchscript source=../datasets/coco8/images/train2017 device=0 project=myproject
```

### onnx

> 注意:
>
> `onnxruntime` 和 `onnxruntime-gpu` 不要同时安装，否则使用 `gpu` 推理时速度会很慢，如果同时安装了2个包，要全部卸载，再安装 `onnxruntime-gpu` 才能使用gpu推理，否则gpu速度会很慢

```sh
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.onnx source=ultralytics/assets/bus.jpg device=0 project=myproject
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.onnx source=../datasets/coco8/images/train2017 device=0 project=myproject

yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.fp16.onnx half=True source=ultralytics/assets/bus.jpg device=0 project=myproject           # fp16模型需要 half=True
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.fp16.onnx half=True source=../datasets/coco8/images/train2017 device=0 project=myproject

yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.cpu.dynamic.onnx source=ultralytics/assets/bus.jpg device=0 project=myproject              # 使用cpu导出的dynamic模型可以用gpu推理
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.cpu.dynamic.onnx source=../datasets/coco8/images/train2017 device=0 project=myproject
```

### openvino

> 注意：openvino没法使用cuda，但是使用 `device=0` 会提高推理速度

```sh
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n_openvino_model source=ultralytics/assets/bus.jpg device=cpu project=myproject

yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n_openvino_model source=../datasets/coco8/images/train2017 device=cpu project=myproject
```

### tensorrt

```sh
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.engine half=True source=ultralytics/assets/bus.jpg device=0 project=myproject                          # fp32模型也能用 --half 推理
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.engine half=True source=../datasets/coco8/images/train2017 device=0 project=myproject

yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.fp16.engine half=True source=ultralytics/assets/bus.jpg device=0 project=myproject
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.fp16.engine half=True source=../datasets/coco8/images/train2017 device=0 project=myproject

yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.fp32.dynamic.engine half=True source=ultralytics/assets/bus.jpg device=0 project=myproject             # fp32模型也能用 --half 推理
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.6 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo11n.fp32.dynamic.engine half=True source=../datasets/coco8/images/train2017 device=0 project=myproject
```

# [导出](https://docs.ultralytics.com/zh/modes/export/)

## 使用示例

将 YOLO11n 模型导出为其他格式，如 ONNX 或 TensorRT。有关导出参数的完整列表，请参见下面的“参数”部分。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load an official model
model = YOLO("path/to/best.pt")  # load a custom trained model

# Export the model
model.export(format="onnx")
```

> CLI

```sh
yolo export model=yolo11n.pt format=onnx      # export official model
yolo export model=path/to/best.pt format=onnx # export custom trained model
```

## 参数

此表详细说明了将 YOLO 模型导出为不同格式的配置和选项。这些设置对于优化导出模型的性能、大小以及在各种平台和环境中的兼容性至关重要。正确的配置可确保模型已准备好部署在预期应用中，并具有最佳效率。

| 参数        | 类型              | 默认值          | 描述                                                         |
| :---------- | :---------------- | :-------------- | :----------------------------------------------------------- |
| `format`    | `str`             | `'torchscript'` | 导出模型的目标格式，例如 `'onnx'`, `'torchscript'`, `'engine'` （TensorRT）等。每种格式都支持与不同的 [部署环境](https://docs.ultralytics.com/zh/modes/export/). |
| `imgsz`     | `int` 或 `tuple`  | `640`           | 模型输入所需的图像大小。可以是正方形图像的整数（例如， `640` 对于 640x640）或元组 `(height, width)` 用于指定特定维度。 |
| `keras`     | `bool`            | `False`         | 启用导出为 Keras 格式，用于 [TensorFlow](https://www.ultralytics.com/glossary/tensorflow) SavedModel，提供与 TensorFlow serving 和 API 的兼容性。 |
| `optimize`  | `bool`            | `False`         | 导出到 TorchScript 时，应用针对移动设备的优化，可能会减小模型大小并提高 [推理](https://docs.ultralytics.com/zh/modes/predict/) 性能。与 NCNN 格式或 CUDA 设备不兼容。 |
| `half`      | `bool`            | `False`         | 启用 FP16（半精度）量化，从而减小模型大小并可能加快受支持硬件上的推理速度。与 ONNX 的 INT8 量化或仅 CPU 导出不兼容。 |
| `int8`      | `bool`            | `False`         | 激活 INT8 量化，进一步压缩模型并加速推理，同时最大限度地减少[精度](https://www.ultralytics.com/glossary/accuracy)损失，主要用于[边缘设备](https://www.ultralytics.com/blog/understanding-the-real-world-applications-of-edge-ai)。与 TensorRT 结合使用时，执行训练后量化 (PTQ)。 |
| `dynamic`   | `bool`            | `False`         | 允许 ONNX、TensorRT 和 OpenVINO 导出使用动态输入大小，从而提高处理不同图像尺寸的灵活性。自动设置为 `True` 当将TensorRT与INT8一起使用时。 |
| `simplify`  | `bool`            | `True`          | 使用以下方式简化 ONNX 导出的模型图 `onnxslim`，从而可能提高性能以及与推理引擎的兼容性。 |
| `opset`     | `int`             | `None`          | 指定 [ONNX](https://docs.ultralytics.com/zh/integrations/onnx/) opset 版本，以与不同的 [ONNX](https://docs.ultralytics.com/zh/integrations/onnx/) 解析器和运行时兼容。如果未设置，则使用最新支持的版本。 |
| `workspace` | `float` 或 `None` | `None`          | 设置最大工作区大小，单位为GiB，用于 [TensorRT](https://docs.ultralytics.com/zh/integrations/tensorrt/) 优化，平衡内存使用和性能。使用 `None` 用于 TensorRT 自动分配，最高可达设备最大值。 |
| `nms`       | `bool`            | `False`         | 如果支持，则将非极大值抑制 (NMS) 添加到导出的模型（请参阅[导出格式](https://docs.ultralytics.com/zh/modes/export/)），从而提高检测后处理效率。不适用于 end2end 模型。 |
| `batch`     | `int`             | `1`             | 指定导出模型批量推理大小，或导出模型将并发处理的最大图像数量，单位为。 `predict` 模式。对于 Edge TPU 导出，此项会自动设置为 1。 |
| `device`    | `str`             | `None`          | 指定导出设备：GPU (`device=0`），CPU（`device=cpu`），适用于 Apple 芯片的 MPS（`device=mps`）或适用于 NVIDIA Jetson 的 DLA（`device=dla:0` 或 `device=dla:1`)。TensorRT 导出自动使用 GPU。 |
| `data`      | `str`             | `'coco8.yaml'`  | 路径指向 [数据集](https://docs.ultralytics.com/zh/datasets/) 配置文件（默认： `coco8.yaml`)，这对于 INT8 量化校准至关重要。如果启用 INT8 但未指定，则将分配默认数据集。 |
| `fraction`  | `float`           | `1.0`           | 指定用于 INT8 量化校准的数据集比例。允许在完整数据集的子集上进行校准，这对于实验或资源有限时非常有用。如果未在使用 INT8 启用时指定，则将使用完整数据集。 |

## 导出格式

YOLOv8 可用的导出格式如下表所示。您可以使用 `format` 参数，即 `format='onnx'` 或 `format='engine'`.

下表列出了可用的 YOLO11 导出格式。您可以使用 `format` 参数导出为任何格式，例如 `format='onnx'` 或 `format='engine'`。您可以直接在导出的模型上进行预测或验证，例如 `yolo predict model=yolo11n.onnx`。导出完成后，将显示您的模型的使用示例。

| 格式                                                         | `format` 参数 | 模型                      | 元数据 | 参数                                                         |
| :----------------------------------------------------------- | :------------ | :------------------------ | :----- | :----------------------------------------------------------- |
| [PyTorch](https://pytorch.org/)                              | -             | `yolo11n.pt`              | ✅      | -                                                            |
| [TorchScript](https://docs.ultralytics.com/zh/integrations/torchscript/) | `torchscript` | `yolo11n.torchscript`     | ✅      | `imgsz`, `half`, `dynamic`, `optimize`, `nms`, `batch`, `device` |
| [ONNX](https://docs.ultralytics.com/zh/integrations/onnx/)   | `onnx`        | `yolo11n.onnx`            | ✅      | `imgsz`, `half`, `dynamic`, `simplify`, `opset`, `nms`, `batch`, `device` |
| [OpenVINO](https://docs.ultralytics.com/zh/integrations/openvino/) | `openvino`    | `yolo11n_openvino_model/` | ✅      | `imgsz`, `half`, `dynamic`, `int8`, `nms`, `batch`, `data`, `fraction`, `device` |
| [TensorRT](https://docs.ultralytics.com/zh/integrations/tensorrt/) | `engine`      | `yolo11n.engine`          | ✅      | `imgsz`, `half`, `dynamic`, `simplify`, `workspace`, `int8`, `nms`, `batch`, `data`, `fraction`, `device` |
| [CoreML](https://docs.ultralytics.com/zh/integrations/coreml/) | `coreml`      | `yolo11n.mlpackage`       | ✅      | `imgsz`, `half`, `int8`, `nms`, `batch`, `device`            |
| [TF SavedModel](https://docs.ultralytics.com/zh/integrations/tf-savedmodel/) | `saved_model` | `yolo11n_saved_model/`    | ✅      | `imgsz`, `keras`, `int8`, `nms`, `batch`, `device`           |
| [TF GraphDef](https://docs.ultralytics.com/zh/integrations/tf-graphdef/) | `pb`          | `yolo11n.pb`              | ❌      | `imgsz`, `batch`, `device`                                   |
| [TF Lite](https://docs.ultralytics.com/zh/integrations/tflite/) | `tflite`      | `yolo11n.tflite`          | ✅      | `imgsz`, `half`, `int8`, `nms`, `batch`, `data`, `fraction`, `device` |
| [TF Edge TPU](https://docs.ultralytics.com/zh/integrations/edge-tpu/) | `edgetpu`     | `yolo11n_edgetpu.tflite`  | ✅      | `imgsz`, `device`                                            |
| [TF.js](https://docs.ultralytics.com/zh/integrations/tfjs/)  | `tfjs`        | `yolo11n_web_model/`      | ✅      | `imgsz`, `half`, `int8`, `nms`, `batch`, `device`            |
| [PaddlePaddle](https://docs.ultralytics.com/zh/integrations/paddlepaddle/) | `paddle`      | `yolo11n_paddle_model/`   | ✅      | `imgsz`, `batch`, `device`                                   |
| [MNN](https://docs.ultralytics.com/zh/integrations/mnn/)     | `mnn`         | `yolo11n.mnn`             | ✅      | `imgsz`, `batch`, `int8`, `half`, `device`                   |
| [NCNN](https://docs.ultralytics.com/zh/integrations/ncnn/)   | `ncnn`        | `yolo11n_ncnn_model/`     | ✅      | `imgsz`, `half`, `batch`, `device`                           |
| [IMX500](https://docs.ultralytics.com/zh/integrations/sony-imx500/) | `imx`         | `yolo11n_imx_model/`      | ✅      | `imgsz`, `int8`, `data`, `fraction`, `device`                |
| [RKNN](https://docs.ultralytics.com/zh/integrations/rockchip-rknn/) | `rknn`        | `yolo11n_rknn_model/`     | ✅      | `imgsz`, `batch`, `name`, `device`                           |

## Example

### torchscript

```sh
yolo detect export imgsz=640 model=weights/yolo11n.pt format=torchscript device=0 project=myproject
yolo detect export imgsz=640 model=weights/yolo11n.pt format=torchscript device=cpu optimize=True project=myproject # optimize not compatible with cuda devices, i.e. use device=cpu
```

### onnx

> 注意:
>
> `onnxruntime` 和 `onnxruntime-gpu` 不要同时安装，否则使用 `gpu` 推理时速度会很慢，如果同时安装了2个包，要全部卸载，再安装`onnxruntime-gpu` 才能使用gpu推理，否则gpu速度会很慢

```sh
yolo detect export imgsz=640 model=weights/yolo11n.pt format=onnx simplify=True device=0 project=myproject

yolo detect export imgsz=640 model=weights/yolo11n.pt format=onnx simplify=True device=0 half=True project=myproject                # half=True only compatible with GPU export, i.e. use device=0

yolo detect export imgsz=640 model=weights/yolo11n.pt format=onnx simplify=True device=cpu dynamic=True project=myproject

yolo detect export imgsz=640 model=weights/yolo11n.pt format=onnx simplify=True device=cpu half=True dynamic=True project=myproject  # 导出失败 half=True not compatible with dynamic=True, i.e. use only one.
```

### opencv使用的onnx

> https://github.com/ultralytics/ultralytics/tree/main/examples/YOLOv8-OpenCV-ONNX-Python

```sh
yolo detect export imgsz=640 model=weights/yolo11n.pt format=onnx simplify=True device=0 opset=12 project=myproject             # opset必须为12

yolo detect export imgsz=640 model=weights/yolo11n.pt format=onnx simplify=True device=0 half=True opset=12 project=myproject   # opset必须为12

# opencv不支持dynamic
```

### openvino

```sh
yolo detect export imgsz=640 model=weights/yolo11n.pt format=openvino device=cpu project=myproject

yolo detect export imgsz=640 model=weights/yolo11n.pt format=openvino device=cpu half=True project=myproject

yolo task =detect export imgsz=640 model=weights/yolo11n.pt format=openvino device=cpu int8=True data=ultralytics/cfg/datasets/coco8.yaml project=myproject # INT8 export requires a data argument for calibration
```

#### 通过openvino的`ovc`命令将onnx转换为openvino格式(支持**fp16**)

> https://docs.openvino.ai/archive/2023.2/openvino_docs_OV_Converter_UG_prepare_model_convert_model_MO_OVC_transition.html

```sh
ovc "onnx_path" --output_model "output_path" --compress_to_fp16

ovc "onnx_path" --output_model "output_path" --compress_to_fp16
```

### tensorrt

```sh
yolo detect export imgsz=640 model=weights/yolo11n.pt format=engine simplify=True device=0 project=myproject # 可以用simplify的onnx

yolo detect export imgsz=640 model=weights/yolo11n.pt format=engine simplify=True device=0 half=True project=myproject
```

### ncnn

```sh
yolo detect export imgsz=640 model=weights/yolo11n.pt format=ncnn simplify=True device=0 project=myproject # 可以用simplify的onnx

yolo detect export imgsz=640 model=weights/yolo11n.pt format=ncnn simplify=True device=0 half=True project=myproject
```

# [跟踪](https://docs.ultralytics.com/zh/modes/track/)

## 可用的追踪器

Ultralytics YOLO 支持以下跟踪算法。可以通过传递相关的 YAML 配置文件（例如 `tracker=tracker_type.yaml`:

- [BoT-SORT](https://github.com/NirAharon/BoT-SORT) - 使用 `botsort.yaml` 来启用此跟踪器。
- [ByteTrack](https://github.com/FoundationVision/ByteTrack) - 使用 `bytetrack.yaml` 来启用此跟踪器。

默认跟踪器是 BoT-SORT。

## 追踪

要在视频流中运行跟踪器，请使用训练有素的 Detect、Segment 或姿势姿势估计 模型，如 YOLO11n、YOLO11n-seg 和 YOLO11n-姿势估计。

> python

```python
from ultralytics import YOLO

# Load an official or custom model
model = YOLO("yolo11n.pt")  # Load an official Detect model
model = YOLO("yolo11n-seg.pt")  # Load an official Segment model
model = YOLO("yolo11n-pose.pt")  # Load an official Pose model
model = YOLO("path/to/best.pt")  # Load a custom trained model

# Perform tracking with the model
results = model.track("https://youtu.be/LNwODJXcvt4", show=True)  # Tracking with default tracker
results = model.track("https://youtu.be/LNwODJXcvt4", show=True, tracker="bytetrack.yaml")  # with ByteTrack
```

> CLI

```sh
# Perform tracking with various models using the command line interface
yolo track model=yolo11n.pt source="https://youtu.be/LNwODJXcvt4"      # Official Detect model
yolo track model=yolo11n-seg.pt source="https://youtu.be/LNwODJXcvt4"  # Official Segment model
yolo track model=yolo11n-pose.pt source="https://youtu.be/LNwODJXcvt4" # Official Pose model
yolo track model=path/to/best.pt source="https://youtu.be/LNwODJXcvt4" # Custom trained model

# Track using ByteTrack tracker
yolo track model=path/to/best.pt tracker="bytetrack.yaml"
```

从上述用法中可以看出，在视频或流媒体源上运行的所有 Detect、Segment 和姿势估计 模型都可以进行跟踪。

## 配置

### 追踪参数

跟踪配置与 Predict 模式共享属性，例如 `conf`, `iou`和 `show`。有关更多配置，请参阅 [预测](https://docs.ultralytics.com/zh/modes/predict/#inference-arguments) 模型页面。

> python

```sh
from ultralytics import YOLO

# Configure the tracking parameters and run the tracker
model = YOLO("yolo11n.pt")
results = model.track(source="https://youtu.be/LNwODJXcvt4", conf=0.3, iou=0.5, show=True)
```

> CLI

```sh
# Configure tracking parameters and run the tracker using the command line interface
yolo track model=yolo11n.pt source="https://youtu.be/LNwODJXcvt4" conf=0.3, iou=0.5 show
```

### 选择追踪器

Ultralytics 还允许您使用修改后的跟踪器配置文件。为此，只需复制一个跟踪器配置文件（例如， `custom_tracker.yaml`），从 [ultralytics/cfg/trackers](https://github.com/ultralytics/ultralytics/tree/main/ultralytics/cfg/trackers) 并根据您的需求修改任何配置（除了 `tracker_type`）。

> python

```python
from ultralytics import YOLO

# Load the model and run the tracker with a custom configuration file
model = YOLO("yolo11n.pt")
results = model.track(source="https://youtu.be/LNwODJXcvt4", tracker="custom_tracker.yaml")
```

> CLI

```sh
# Load the model and run the tracker with a custom configuration file using the command line interface
yolo track model=yolo11n.pt source="https://youtu.be/LNwODJXcvt4" tracker='custom_tracker.yaml'
```

有关每个参数的详细说明，请参阅[追踪器参数](https://docs.ultralytics.com/zh/modes/track/#tracker-arguments)部分。

### 跟踪器参数

可以通过编辑特定于每种跟踪算法的 YAML 配置文件来微调某些跟踪行为。这些文件定义了阈值、缓冲区和匹配逻辑等参数：

- [`botsort.yaml`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/botsort.yaml)
- [`bytetrack.yaml`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/bytetrack.yaml)

下表提供了每个参数的描述：

> 跟踪器阈值信息
>
> 如果目标置信度得分较低，即低于 [`track_high_thresh`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/bytetrack.yaml#L5)，则不会成功返回和更新任何轨迹。

| **参数**            | **有效值或范围**                              | **描述**                                                     |
| :------------------ | :-------------------------------------------- | :----------------------------------------------------------- |
| `tracker_type`      | `botsort`, `bytetrack`                        | 指定跟踪器类型。选项包括 `botsort` 或 `bytetrack`.           |
| `track_high_thresh` | `0.0-1.0`                                     | 跟踪期间第一次关联使用的阈值。 影响检测与现有轨迹匹配的置信度。 |
| `track_low_thresh`  | `0.0-1.0`                                     | 跟踪期间第二次关联使用的阈值。 在第一次关联失败时使用，具有更宽松的标准。 |
| `new_track_thresh`  | `0.0-1.0`                                     | 如果检测结果与现有跟踪不匹配，则使用此阈值初始化新跟踪。用于控制何时认为新对象出现。 |
| `track_buffer`      | `>=0`                                         | 用于指示在移除丢失的跟踪之前应保持活动状态的帧数的缓冲区。值越高，对遮挡的容忍度越高。 |
| `match_thresh`      | `0.0-1.0`                                     | 匹配轨迹的阈值。 值越高，匹配越宽松。                        |
| `fuse_score`        | `True`, `False`                               | 确定在匹配之前是否将置信度分数与 IoU 距离融合。有助于在关联时平衡空间和置信度信息。 |
| `gmc_method`        | `orb`, `sift`, `ecc`, `sparseOptFlow`, `None` | 用于全局运动补偿的方法。有助于解决摄像机移动问题，从而改善跟踪效果。 |
| `proximity_thresh`  | `0.0-1.0`                                     | 与 ReID（重新识别）有效匹配所需的最小 IoU。确保空间上的接近性，然后再使用外观线索。 |
| `appearance_thresh` | `0.0-1.0`                                     | ReID 所需的最小外观相似度。设置两个检测结果在视觉上必须有多相似才能被链接。 |
| `with_reid`         | `True`, `False`                               | 指示是否使用 ReID。启用基于外观的匹配，以便在遮挡情况下更好地进行跟踪。仅 BoTSORT 支持。 |
| `model`             | `auto`, `yolo11[nsmlx]-cls.pt`                | 指定要使用的模型。默认为 `auto`，如果检测器是 YOLO，则使用原生特征，否则使用 `yolo11n-cls.pt`. |

### 启用 Re-Identification (ReID)

默认情况下，ReID 处于关闭状态，以最大限度地减少性能开销。 启用它很简单，只需设置 `with_reid: True` 在 [跟踪器配置](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/botsort.yaml)。您还可以自定义 `model` 用于 ReID，允许您根据用例权衡准确性和速度：

- **原生功能 (`model: auto`)**：这利用了 YOLO 检测器的直接特征来进行 ReID，增加的开销极少。当您需要某种程度的 ReID 但不会显著影响性能时，这是理想的选择。如果检测器不支持本机特征，它会自动退回使用“”。 `yolo11n-cls.pt`.
- **YOLO 分类模型**：您可以明确设置分类模型（例如，“”）。 `yolo11n-cls.pt`）用于 ReID 特征提取。这提供了更具区分性的嵌入，但由于额外的推理步骤而引入了额外的延迟。

为了获得更好的性能，尤其是在为 ReID 使用单独的分类模型时，您可以将其导出到更快的后端，如 TensorRT：

**导出 ReID 模型到 TensorRT**

```python
from torch import nn

from ultralytics import YOLO

# Load the classification model
model = YOLO("yolo11n-cls.pt")

# Add average pooling layer
head = model.model.model[-1]
pool = nn.Sequential(nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten(start_dim=1))
pool.f, pool.i = head.f, head.i
model.model.model[-1] = pool

# Export to TensorRT
model.export(format="engine", half=True, dynamic=True, batch=32)
```

导出后，您可以在跟踪器配置中指向 TensorRT 模型路径，它将用于跟踪期间的 ReID。

## Python 示例

### 持久化跟踪循环

这是一个使用 python 脚本， [OpenCV](https://www.ultralytics.com/glossary/opencv) (`cv2`）和 YOLO11 在视频帧上运行对象跟踪。此脚本仍然假定您已经安装了必要的软件包（`opencv-python` 和 `ultralytics`）。 `persist=True` 参数告诉跟踪器，当前图像或帧是序列中的下一个，并期望当前图像中存在来自前一个图像的跟踪。

**使用跟踪的流式 for 循环**

```python
import cv2

from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("yolo11n.pt")

# Open the video file
video_path = "path/to/video.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO11 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLO11 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
```

请注意从 `model(frame)` 到 `model.track(frame)`的更改，它启用了对象跟踪而不是简单的检测。这个修改后的脚本将在视频的每一帧上运行跟踪器，可视化结果，并在一个窗口中显示它们。可以通过按 'q' 键退出循环。

### 随时间绘制轨迹

可视化连续帧上的对象轨迹可以为深入了解视频中检测到的对象的运动模式和行为提供有价值的信息。使用 Ultralytics YOLO11，绘制这些轨迹是一个无缝且高效的过程。

在下面的示例中，我们将演示如何利用 YOLO11 的跟踪功能来绘制检测到的对象在多个视频帧中的移动。此脚本涉及打开一个视频文件，逐帧读取它，并利用 YOLO 模型来识别和跟踪各种对象。通过保留检测到的边界框的中心点并将它们连接起来，我们可以绘制表示被跟踪对象所遵循的路径的线条。

```python
from collections import defaultdict

import cv2
import numpy as np

from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("yolo11n.pt")

# Open the video file
video_path = "path/to/video.mp4"
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO11 tracking on the frame, persisting tracks between frames
        result = model.track(frame, persist=True)[0]

        # Get the boxes and track IDs
        if result.boxes and result.boxes.is_track:
            boxes = result.boxes.xywh.cpu()
            track_ids = result.boxes.id.int().cpu().tolist()

            # Visualize the result on the frame
            frame = result.plot()

            # Plot the tracks
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                if len(track) > 30:  # retain 30 tracks for 30 frames
                    track.pop(0)

                # Draw the tracking lines
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

        # Display the annotated frame
        cv2.imshow("YOLO11 Tracking", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
```

### 多线程跟踪

多线程跟踪提供了同时在多个视频流上运行对象跟踪的能力。这在处理多个视频输入（例如来自多个监控摄像头）时特别有用，在这些情况下，并发处理可以大大提高效率和性能。

在提供的 python 脚本中，我们利用 python 的 `threading` 模块来并发运行跟踪器的多个实例。每个线程负责在一个视频文件上运行跟踪器，并且所有线程在后台同时运行。

为了确保每个线程都收到正确的参数（视频文件、要使用的模型和文件索引），我们定义了一个函数 `run_tracker_in_thread` ，它接受这些参数并包含主跟踪循环。此函数逐帧读取视频，运行跟踪器，并显示结果。

本例中使用了两个不同的模型： `yolo11n.pt` 和 `yolo11n-seg.pt`，每个模型跟踪不同视频文件中的对象。视频文件在 `SOURCES`.

字段 `daemon=True` 参数中指定。 `threading.Thread` 这意味着一旦主程序结束，这些线程将立即关闭。然后我们使用以下代码启动线程： `start()` 并使用 `join()` 来使主线程等待，直到两个跟踪器线程都完成。

最后，在所有线程完成其任务后，使用以下代码关闭显示结果的窗口： `cv2.destroyAllWindows()`.

```python
import threading

import cv2

from ultralytics import YOLO

# Define model names and video sources
MODEL_NAMES = ["yolo11n.pt", "yolo11n-seg.pt"]
SOURCES = ["path/to/video.mp4", "0"]  # local video, 0 for webcam


def run_tracker_in_thread(model_name, filename):
    """
    Run YOLO tracker in its own thread for concurrent processing.

    Args:
        model_name (str): The YOLO11 model object.
        filename (str): The path to the video file or the identifier for the webcam/external camera source.
    """
    model = YOLO(model_name)
    results = model.track(filename, save=True, stream=True)
    for r in results:
        pass


# Create and start tracker threads using a for loop
tracker_threads = []
for video_file, model_name in zip(SOURCES, MODEL_NAMES):
    thread = threading.Thread(target=run_tracker_in_thread, args=(model_name, video_file), daemon=True)
    tracker_threads.append(thread)
    thread.start()

# Wait for all tracker threads to finish
for thread in tracker_threads:
    thread.join()

# Clean up and close windows
cv2.destroyAllWindows()
```

# yolo special commands

## yolo help

```sh
> yolo help

    Arguments received: ['yolo', 'help']. Ultralytics 'yolo' commands use the following syntax:

        yolo TASK MODE ARGS

        Where   TASK (optional) is one of ('detect', 'segment', 'classify', 'pose')
                MODE (required) is one of ('train', 'val', 'predict', 'export', 'track', 'benchmark')
                ARGS (optional) are any number of custom 'arg=value' pairs like 'imgsz=320' that override defaults.
                    See all ARGS at https://docs.ultralytics.com/usage/cfg or with 'yolo cfg'

    1. Train a detection model for 10 epochs with an initial learning_rate of 0.01
        yolo train data=coco8.yaml model=yolo11n.pt epochs=10 lr0=0.01

    2. Predict a YouTube video using a pretrained segmentation model at image size 320:
        yolo predict model=yolo11n-seg.pt source='https://youtu.be/LNwODJXcvt4' imgsz=320

    3. Val a pretrained detection model at batch-size 1 and image size 640:
        yolo val model=yolo11n.pt data=coco8.yaml batch=1 imgsz=640

    4. Export a yolo11n classification model to ONNX format at image size 224 by 128 (no TASK required)
        yolo export model=yolo11n-cls.pt format=onnx imgsz=224,128

    5. Run special commands:
        yolo help
        yolo checks
        yolo version
        yolo settings
        yolo copy-cfg
        yolo cfg

    Docs: https://docs.ultralytics.com
    Community: https://community.ultralytics.com
    GitHub: https://github.com/ultralytics/ultralytics
```

## yolo checks

```sh
> yolo checks
Ultralytics YOLOv8.0.195  Python-3.11.4 torch-2.1.0+cu121 CUDA:0 (NVIDIA GeForce GTX 1080 Ti, 11264MiB)
Setup complete  (16 CPUs, 31.9 GB RAM, 152.1/200.0 GB disk)

OS                  Windows-10-10.0.19044-SP0
Environment         Windows
Python              3.11.4
Install             git
RAM                 31.91 GB
CPU                 Intel Core(TM) i7-10700 2.90GHz
CUDA                12.1

matplotlib           3.8.0>=3.3.0
numpy                1.26.0>=1.22.2
opencv-python        4.8.1.78>=4.6.0
pillow               10.0.1>=7.1.2
pyyaml               6.0.1>=5.3.1
requests             2.31.0>=2.23.0
scipy                1.10.1>=1.4.1
torch                2.1.0+cu121>=1.8.0
torchvision          0.16.0+cu121>=0.9.0
tqdm                 4.66.1>=4.64.0
pandas               2.1.1>=1.1.4
seaborn              0.13.0>=0.11.0
psutil               5.9.5
py-cpuinfo           9.0.0
thop                 0.1.1-2209072238>=0.1.1
```

## yolo version

```sh
> yolo version
8.0.195
```

## yolo settings

```sh
> yolo settings
 Learn about settings at https://docs.ultralytics.com/quickstart/#ultralytics-settings
Printing 'C:\Users\Administrator\AppData\Roaming\Ultralytics\settings.yaml'

settings_version: 0.0.4
datasets_dir: D:\ml\code\datasets
weights_dir: d:\ml\code\yolov8-ultralytics\weights
runs_dir: d:\ml\code\yolov8-ultralytics\runs
uuid: 062fa24c9a04873db7e870e2df7f4297a2745f5a740d9e7bd868b5884cf0b91a
sync: true
api_key: ''
clearml: true
comet: true
dvc: true
hub: true
mlflow: true
neptune: true
raytune: true
tensorboard: true
wandb: true
```

## yolo copy-cfg

```sh
> yolo copy-cfg
D:\ml\code\yolov8-ultralytics\ultralytics\cfg\default.yaml copied to D:\ml\code\yolov8-ultralytics\default_copy.yaml
Example YOLO command with this new custom cfg:
    yolo cfg='D:\ml\code\yolov8-ultralytics\default_copy.yaml' imgsz=320 batch=8
```

## yolo cfg

```sh
Printing 'C:\Users\Administrator\Desktop\self\yolov8-ultralytics\ultralytics\cfg\default.yaml'

task: detect
mode: train
model: null
data: null
epochs: 100
time: null
patience: 100
batch: 16
imgsz: 640
save: true
save_period: -1
cache: false
device: null
workers: 8
project: null
name: null
exist_ok: false
pretrained: true
optimizer: auto
verbose: true
seed: 0
deterministic: true
single_cls: false
rect: false
cos_lr: false
close_mosaic: 10
resume: false
amp: true
fraction: 1.0
profile: false
freeze: None
multi_scale: false
overlap_mask: true
mask_ratio: 4
dropout: 0.0
val: true
split: val
save_json: false
save_hybrid: false
conf: null
iou: 0.7
max_det: 300
half: false
dnn: false
plots: true
source: null
vid_stride: 1
stream_buffer: false
visualize: false
augment: false
agnostic_nms: false
classes: null
retina_masks: false
embed: null
show: false
save_frames: false
save_txt: false
save_conf: false
save_crop: false
show_labels: true
show_conf: true
show_boxes: true
line_width: null
format: torchscript
keras: false
optimize: false
int8: false
dynamic: false
simplify: false
opset: null
workspace: 4
nms: false
lr0: 0.01
lrf: 0.01
momentum: 0.937
weight_decay: 0.0005
warmup_epochs: 3.0
warmup_momentum: 0.8
warmup_bias_lr: 0.1
box: 7.5
cls: 0.5
dfl: 1.5
pose: 12.0
kobj: 1.0
label_smoothing: 0.0
nbs: 64
hsv_h: 0.015
hsv_s: 0.7
hsv_v: 0.4
degrees: 0.0
translate: 0.1
scale: 0.5
shear: 0.0
perspective: 0.0
flipud: 0.0
fliplr: 0.5
bgr: 0.0
mosaic: 1.0
mixup: 0.0
copy_paste: 0.0
auto_augment: randaugment
erasing: 0.4
crop_fraction: 1.0
cfg: null
tracker: botsort.yaml
```

