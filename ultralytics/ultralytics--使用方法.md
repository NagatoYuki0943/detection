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

# Load a YOLO model from a pretrained weights file
model = YOLO("yolo26n.pt")

# Run the model in MODE using custom ARGS
MODE = "predict"
ARGS = {"source": "image.jpg", "imgsz": 640}
getattr(model, MODE)(**ARGS)
```

- 说明：
  - `TASK`（可选）是以下之一（[detect](https://docs.ultralytics.com/zh/tasks/detect), [segment](https://docs.ultralytics.com/zh/tasks/segment), [classify](https://docs.ultralytics.com/zh/tasks/classify), [pose](https://docs.ultralytics.com/zh/tasks/pose), [obb](https://docs.ultralytics.com/zh/tasks/obb)）
  - `MODE`（必选）是以下之一（[train](https://docs.ultralytics.com/zh/modes/train), [val](https://docs.ultralytics.com/zh/modes/val), [predict](https://docs.ultralytics.com/zh/modes/predict), [export](https://docs.ultralytics.com/zh/modes/export), [track](https://docs.ultralytics.com/zh/modes/track), [benchmark](https://docs.ultralytics.com/zh/modes/benchmark)）
  - `ARGS` (optional) are `arg=value` pairs like `imgsz=640` that override defaults.

默认的 `ARG` 值在此页面定义，并来自 `cfg/default.yaml` [文件](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/default.yaml)。

## 任务

- Ultralytics YOLO 模型可以执行多种计算机视觉任务，包括：
  - **Detect**（检测）：[目标检测](https://docs.ultralytics.com/tasks/detect) 用于识别图像或视频中的对象并进行定位。
  - **Segment**（分割）：[实例分割](https://docs.ultralytics.com/tasks/segment) 将图像或视频划分为对应不同对象或类别的区域。
  - **Classify**（分类）：[图像分类](https://docs.ultralytics.com/tasks/classify) 预测输入图像的类别标签。
  - **Pose**（姿态）：[姿态估计](https://docs.ultralytics.com/tasks/pose) 在图像或视频中识别对象并估计其关键点。
  - **OBB**（旋转框）：[旋转边界框](https://docs.ultralytics.com/tasks/obb) 使用旋转后的边界框，适用于卫星图像或医学图像。

| 参数   | 默认值     | 描述                                                         |
| :----- | :--------- | :----------------------------------------------------------- |
| `task` | `'detect'` | 指定 YOLO 任务：`detect` 用于 [目标检测](https://www.ultralytics.com/glossary/object-detection)，`segment` 用于分割，`classify` 用于分类，`pose` 用于姿态估计，`obb` 用于旋转边界框。每个任务都针对图像和视频分析中的特定输出和问题进行了定制。 |

## 模式

Ultralytics YOLO 模型在不同模式下运行，每种模式专为模型生命周期的特定阶段而设计：

- **Train**（训练）：在自定义数据集上训练 YOLO 模型。
- **Val**（验证）：验证训练好的 YOLO 模型。
- **Predict**（预测）：使用训练好的 YOLO 模型对新图像或视频进行预测。
- **Export**（导出）：导出 YOLO 模型以进行部署。
- **Track**（追踪）：使用 YOLO 模型进行实时对象追踪。
- **Benchmark**（基准测试）：对 YOLO 导出模型（ONNX、TensorRT 等）的速度和精度进行基准测试。

| 参数   | 默认值    | 描述                                                         |
| :----- | :-------- | :----------------------------------------------------------- |
| `mode` | `'train'` | 指定 YOLO 模型的运行模式：`train` 用于模型训练，`val` 用于验证，`predict` 用于推理，`export` 用于转换为部署格式，`track` 用于对象追踪，`benchmark` 用于性能评估。每种模式都支持从开发到部署的不同阶段。 |

## 训练设置

...

## 预测设置

...

## 验证设置

...

## 导出设置

...

## 解决方案设置

Ultralytics 解决方案配置设置提供了灵活性，可针对目标检测计数、热图创建、健身追踪、数据分析、区域追踪、队列管理和基于区域的计数等任务自定义模型。这些选项支持轻松调整，以获得针对特定需求量身定制的准确且有用的结果。

| 数                | 类型              | 默认值                       | 描述                                                         |
| :---------------- | :---------------- | :--------------------------- | :----------------------------------------------------------- |
| `model`           | `str`             | `None`                       | Ultralytics YOLO 模型文件的路径。                            |
| `region`          | `list`            | `'[(20, 400), (1260, 400)]'` | 定义计数区域的点列表。                                       |
| `show_in`         | `bool`            | `True`                       | 用于控制是否在视频流中显示进入计数的标志。                   |
| `show_out`        | `bool`            | `True`                       | 用于控制是否在视频流中显示离开计数的标志。                   |
| `analytics_type`  | `str`             | `'line'`                     | 图表类型，例如 `line`（折线图）、`bar`（柱状图）、`area`（面积图）或 `pie`（饼图）。 |
| `colormap`        | `int`             | `cv2.COLORMAP_DEEPGREEN`     | 用于热图的配色方案。                                         |
| `json_file`       | `str`             | `None`                       | 包含所有停车坐标数据的 JSON 文件路径。                       |
| `up_angle`        | `float`           | `145.0`                      | “向上”姿势的角度阈值。                                       |
| `kpts`            | `list[int]`       | `'[6, 8, 10]'`               | 用于监控健身训练的三个关键点索引列表。这些关键点对应于身体关节或部位，例如肩部、肘部和腕部，适用于俯卧撑、引体向上、深蹲和腹部训练等动作。 |
| `down_angle`      | `int`             | `90`                         | “向下”姿势的角度阈值。                                       |
| `blur_ratio`      | `float`           | `0.5`                        | 调节模糊强度百分比，取值范围为 `0.1 - 1.0`。                 |
| `crop_dir`        | `str`             | `'cropped-detections'`       | 用于存储裁剪后的检测结果的目录名称。                         |
| `records`         | `int`             | `5`                          | 触发带有安全警报系统的电子邮件所需的总检测计数。             |
| `vision_point`    | `tuple[int, int]` | `(20, 20)`                   | 使用 VisionEye 解决方案追踪对象并绘制路径的点。              |
| `source`          | `str`             | `None`                       | 输入源（视频、RTSP 等）的路径。仅可用于解决方案命令行界面 (CLI)。 |
| `figsize`         | `tuple[int, int]` | `(12.8, 7.2)`                | 用于分析图表（如热图或统计图）的图形大小。                   |
| `fps`             | `float`           | `30.0`                       | 用于速度计算的每秒帧数。                                     |
| `max_hist`        | `int`             | `5`                          | 用于速度/方向计算时，每个对象最大追踪的历史点数。            |
| `meter_per_pixel` | `float`           | `0.05`                       | 用于将像素距离转换为现实世界单位的比例因子。                 |
| `max_speed`       | `int`             | `120`                        | 视觉叠加层中的最高速度限制（用于警报）。                     |
| `data`            | `str`             | `'images'`                   | 用于相似度搜索的图像目录路径。                               |

## 数据增强设置

...

## 日志记录、检查点和绘图设置

...

# 数据集

先要把数据集放入dataset中，修改data/目录下的yaml，调整为自己的数据集，需要调整路径，分类数，标签名

txt内容，每一行都是 `3 0.933536 0.486124 0.030408 0.154487`，`class center_x center_y width height`

label 中心横坐标与图像宽度比值 中心纵坐标与图像高度比值 bbox宽度与图像宽度比值 bbox高度与图像宽高比值

```sh
#-------------------------------------------#
#     yolov5 11的格式
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
#     yolov5 11另的一种图片目录格式
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

所有的 yolo26 预训练模型都可以在此找到。检测、分割和姿态模型在 [COCO](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/datasets/coco.yaml) 数据集上进行预训练，而分类模型在 [ImageNet](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/datasets/ImageNet.yaml) 数据集上进行预训练。

在首次使用时，[模型](https://github.com/ultralytics/ultralytics/tree/main/ultralytics/models) 会自动从最新的 Ultralytics [发布版本](https://github.com/ultralytics/assets/releases)中下载。

| Model                                                        | size (pixels) | mAPval 50-95 | mAPval 50-95(e2e) | Speed CPU ONNX (ms) | Speed T4 TensorRT10 (ms) | params (M) | FLOPs (B) |
| ------------------------------------------------------------ | ------------- | ------------ | ----------------- | ------------------- | ------------------------ | ---------- | --------- |
| [YOLO26n](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26n.pt) | 640           | 40.9         | 40.1              | 38.9 ± 0.7          | 1.7 ± 0.0                | 2.4        | 5.4       |
| [YOLO26s](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt) | 640           | 48.6         | 47.8              | 87.2 ± 0.9          | 2.5 ± 0.0                | 9.5        | 20.7      |
| [YOLO26m](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26m.pt) | 640           | 53.1         | 52.5              | 220.0 ± 1.4         | 4.7 ± 0.1                | 20.4       | 68.2      |
| [YOLO26l](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26l.pt) | 640           | 55.0         | 54.4              | 286.2 ± 2.0         | 6.2 ± 0.2                | 24.8       | 86.4      |
| [YOLO26x](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26x.pt) | 640           | 57.5         | 56.9              | 525.8 ± 4.0         | 11.8 ± 0.2               | 55.7       | 193.9     |

*参数和 FLOPs 数值是针对 `model.fuse()` 之后融合模型的，该操作会合并 Conv 和 BatchNorm 层并移除辅助的一对多检测头。预训练检查点保留了完整的训练架构，因此可能显示更高的计数值。*



# [命令行界面](https://docs.ultralytics.com/zh/usage/cli/)

## 语法

```sh
yolo TASK MODE ARGS
```

说明：

- `TASK`（可选）是 [detect, segment, classify, pose, obb] 之一
- `MODE`（必选）是 [train, val, predict, export, track, benchmark] 之一
- `ARGS`（可选）是任意数量的自定义 `arg=value` 对（例如 `imgsz=320`），用于覆盖默认设置。

在完整的 [配置指南](https://docs.ultralytics.com/zh/usage/cfg) 中或通过 `yolo cfg` 查看所有 ARGS。

说明：

- `TASK`（可选）是 `[detect, segment, classify, pose, obb]` 之一。如果不明确指定，YOLO 将尝试根据模型类型推断 `TASK`。
- `MODE`（必选）是 `[train, val, predict, export, track, benchmark]` 之一
- `ARGS`（可选）是任意数量的自定义 `arg=value` 对（例如 `imgsz=320`），用于覆盖默认设置。有关可用 `ARGS` 的完整列表，请参阅 [配置](https://docs.ultralytics.com/zh/usage/cfg) 页面和 `default.yaml`。

> 参数必须以 `arg=val` 对，用等号分隔 `=` 签名，并用空格分隔对。不要使用 `--` 参数前缀或逗号 `,` 在参数之间。
>
> - `yolo predict model=yolo26n.pt imgsz=640 conf=0.25`  ✅
> - `yolo predict model yolo26n.pt imgsz 640 conf 0.25`  ❌
> - `yolo predict --model yolo26n.pt --imgsz 640 --conf 0.25`  ❌

## 训练

在 COCO8 数据集上训练 YOLO 100 个 epoch，图像尺寸为 640。有关可用参数的完整列表，请参阅 [配置](https://docs.ultralytics.com/zh/usage/cfg) 页面。

```sh
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640
```

恢复中断的训练会话：

```sh
yolo detect train resume model=last.pt
```

## 验证

验证训练后的模型在 COCO8 数据集上的 [accuracy](https://www.ultralytics.com/glossary/accuracy)。不需要参数，因为 `model` 会保留其训练 `data` 和参数作为模型属性。

```sh
yolo detect val model=yolo26n.pt
```

验证自定义训练的模型：

```sh
yolo detect val model=path/to/best.pt
```

## 预测

使用训练好的模型来运行图像预测。

使用官方yolo26n模型进行预测：

```sh
yolo detect predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'
```

使用自定义模型进行预测：

```sh
yolo detect predict model=path/to/best.pt source='https://ultralytics.com/images/bus.jpg'
```

## 导出

将模型导出为不同的格式，如 ONNX 或 CoreML。

```sh
yolo export model=yolo26n.pt format=onnx
```

将自定义训练的模型导出为 ONNX 格式：

```
yolo export model=path/to/best.pt format=onnx
```

## 覆盖默认参数

通过在 CLI 中以 `arg=value` 的键值对形式传递参数，可以覆盖默认参数。

训练一个检测模型，进行 10 个 epoch，学习率为 0.01：

```sh
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=10 lr0=0.01
```

使用预训练的分割模型对 YouTube 视频进行预测，图像尺寸为 320：

```sh
yolo segment predict model=yolo26n-seg.pt source='https://youtu.be/LNwODJXcvt4' imgsz=320
```

验证一个预训练检测模型，batch size 为 1，图像尺寸为 640：

```sh
yolo detect val model=yolo26n.pt data=coco8.yaml batch=1 imgsz=640
```

## 覆盖默认配置文件

覆盖 `default.yaml` 通过传递一个新文件来完全替换配置文件。 `cfg` 参数，例如 `cfg=custom.yaml`.

为此，首先创建一份副本 `default.yaml` 在您当前的工作目录中使用 `yolo copy-cfg` 命令，它会创建一个 `default_copy.yaml` 文件。

然后，你可以将此文件作为 `cfg=default_copy.yaml` 传递，并附带任何附加参数，例如本例中的 `imgsz=320`：

```sh
yolo copy-cfg
yolo cfg=default_copy.yaml imgsz=320
```

## 解决方案命令

Ultralytics 通过 CLI 为常见的计算机视觉应用提供了开箱即用的解决方案。`yolo solutions` 命令涵盖了目标计数、裁剪、模糊处理、锻炼监控、热图、实例分割、VisionEye、速度估计、队列管理、分析、Streamlit 推理和基于区域的跟踪——请参阅 [Solutions](https://docs.ultralytics.com/zh/solutions) 页面获取完整目录。运行 `yolo solutions help` 以列出所有受支持的解决方案及其参数。

统计视频或直播流中的物体数量：

```sh
yolo solutions count show=True
yolo solutions count source="path/to/video.mp4" # specify video file path
```

裁剪检测到的目标并将其保存到磁盘：

```sh
yolo solutions crop show=True
yolo solutions crop source="path/to/video.mp4" # specify video file path
yolo solutions crop classes="[0, 2]"           # crop only selected classes
```

为了隐私保护或突出其他区域，模糊视频中检测到的目标：

```sh
yolo solutions blur show=True
yolo solutions blur source="path/to/video.mp4" # specify video file path
yolo solutions blur classes="[0, 5]"           # blur only selected classes
```

使用姿态模型监控健身锻炼：

```sh
yolo solutions workout show=True
yolo solutions workout source="path/to/video.mp4" # specify video file path

# Use keypoints for ab-workouts
yolo solutions workout kpts="[5, 11, 13]" # left side
yolo solutions workout kpts="[6, 12, 14]" # right side
```

生成显示目标密度和运动模式的热图：

```sh
yolo solutions heatmap show=True
yolo solutions heatmap source="path/to/video.mp4"                                # specify video file path
yolo solutions heatmap colormap=cv2.COLORMAP_INFERNO                             # customize colormap
yolo solutions heatmap region="[(20, 400), (1080, 400), (1080, 360), (20, 360)]" # restrict heatmap to a region
```

在视频上运行带有跟踪功能的实例分割：

```sh
yolo solutions isegment show=True
yolo solutions isegment source="path/to/video.mp4" # specify video file path
yolo solutions isegment classes="[0, 5]"           # segment only selected classes
```

使用 VisionEye 绘制目标到观察者的视线：

```sh
yolo solutions visioneye show=True
yolo solutions visioneye source="path/to/video.mp4" # specify video file path
yolo solutions visioneye classes="[0, 5]"           # monitor only selected classes
```

估计视频中移动目标的速度：

```sh
yolo solutions speed show=True
yolo solutions speed source="path/to/video.mp4" # specify video file path
yolo solutions speed meter_per_pixel=0.05       # set scale for real-world units
```

统计指定队列或区域内的目标数量：

```sh
yolo solutions queue show=True
yolo solutions queue source="path/to/video.mp4"                                # specify video file path
yolo solutions queue region="[(20, 400), (1080, 400), (1080, 360), (20, 360)]" # configure queue coordinates
```

根据跟踪到的检测结果生成分析图表（折线图、柱状图、面积图或饼图）：

```sh
yolo solutions analytics show=True
yolo solutions analytics source="path/to/video.mp4" # specify video file path
yolo solutions analytics analytics_type="pie" show=True
yolo solutions analytics analytics_type="bar" show=True
yolo solutions analytics analytics_type="area" show=True
```

使用 Streamlit 在 Web 浏览器中执行目标检测、实例分割或姿态估计：

```sh
yolo solutions inference
yolo solutions inference model="path/to/model.pt" # use custom model
```

仅跟踪指定多边形区域内的目标：

```sh
yolo solutions trackzone show=True
yolo solutions trackzone source="path/to/video.mp4"                                  # specify video file path
yolo solutions trackzone region="[(150, 150), (1130, 150), (1130, 570), (150, 570)]" # configure zone coordinates
```

结合目标检测运行安全报警监控：

```sh
yolo solutions security show=True
yolo solutions security source="path/to/video.mp4" # specify video file path
```

使用预定义区域监控停车场占用情况：

```sh
yolo solutions parking source="path/to/video.mp4" json_file="bounding_boxes.json" # requires pre-built JSON
yolo solutions parking source="path/to/video.mp4" json_file="bounding_boxes.json" model="yolo26n.pt"
```

查看可用解决方案及其选项：

```sh
yolo solutions help
```

有关 Ultralytics 解决方案的更多信息，请访问 [Solutions](https://docs.ultralytics.com/zh/solutions) 页面。

# [训练](https://docs.ultralytics.com/zh/modes/train/)

## 使用示例

### **单 GPU 和 CPU 训练示例**

设备是自动确定的。如果有 GPU 可用，则将使用 GPU（默认 CUDA 设备 0），否则将在 CPU 上开始训练。

在 COCO8 数据集上训练 YOLO26n，时长 100 个 [epoch](https://www.ultralytics.com/glossary/epoch)，图像尺寸为 640。训练设备可以使用 `device` 参数指定。如果未传递参数，且可用时将默认使用 GPU `device=0`；否则将使用 `device='cpu'`。有关训练参数的完整列表，请参见下方的“参数”部分。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.yaml")  # build a new model from YAML
model = YOLO("yolo26n.pt")  # load a pretrained model (recommended for training)
model = YOLO("yolo26n.yaml").load("yolo26n.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data="coco8.yaml", epochs=100, imgsz=640)
```

> CLI

```sh
# Build a new model from YAML and start training from scratch
yolo detect train data=coco8.yaml model=yolo26n.yaml epochs=100 imgsz=640

# Start training from a pretrained *.pt model
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640

# Build a new model from YAML, transfer pretrained weights to it and start training
yolo detect train data=coco8.yaml model=yolo26n.yaml pretrained=yolo26n.pt epochs=100 imgsz=640
```

### 多 GPU 训练

多 GPU 训练通过将训练负载分配到多个 GPU 上，实现了对现有硬件资源更高效的利用。此功能可通过 Python API 和命令行界面使用。要启用多 GPU 训练，请指定你希望使用的 GPU 设备 ID。

若要使用 CUDA 设备 0 和 1 这 2 个 GPU 进行训练，请使用以下命令。根据需要扩展到更多 GPU。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # load a pretrained model (recommended for training)

# Train the model with 2 GPUs
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=[0, 1])

# Train the model with the two most idle GPUs
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=[-1, -1])
```

> CLI

```sh
# Start training from a pretrained *.pt model using GPUs 0 and 1
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640 device=0,1

# Use the two most idle GPUs
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640 device=-1,-1
```

> **使用自定义代码进行多 GPU 训练**
>
> 当你指定多个设备（例如 `device=[0, 1]`）时，Ultralytics 会在内部启动一个新的训练器实例，并在底层执行 `torch.distributed.run`。这对于标准的 CLI 使用和未经修改的 Python 脚本可以无缝运行。
>
> 但是，如果你的脚本包含自定义组件（例如自定义训练器、验证器、数据集或增强流水线），这些对象无法自动序列化并传输到 DDP 子进程中。在这种情况下，你必须使用 `torch.distributed.run` 直接启动你的脚本：
>
> ```sh
> python -m torch.distributed.run --nproc_per_node 2 your_training_script.py
> ```

AMD GPU 训练使用带有标准 `device=0` 或 `device=cuda:0` 语法的 PyTorch ROCm 构建版本。有关安装以及当前 MIGraphX、DirectML 和 Ryzen AI NPU 支持状态，请参见 [AMD integration guide](https://docs.ultralytics.com/zh/integrations/amd)。

Intel GPU 训练使用 `device=xpu:0`，或者在使用提供 XCCL 的 PyTorch 构建版本时使用多个 XPU ID。

### 空闲 GPU 训练

空闲 GPU 训练能够自动选择多 GPU 系统中利用率最低的 GPU，从而在无需手动选择的情况下优化资源使用。此功能根据利用率指标和 VRAM 可用性来识别可用 GPU。

> 要自动选择并使用最空闲的 GPU 进行训练，请使用 `-1` 设备参数。这在共享计算环境或多用户服务器中特别有用。
>

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # load a pretrained model (recommended for training)

# Train using the single most idle GPU
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=-1)

# Train using the two most idle GPUs
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=[-1, -1])
```

> CLI

```shell
# Start training using the single most idle GPU
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640 device=-1

# Start training using the two most idle GPUs
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640 device=-1,-1
```

自动选择算法会优先考虑具有以下特征的 GPU：

1. 较低的当前利用率百分比
2. 较高的可用内存（空闲 VRAM）
3. 较低的温度和功耗

此功能在共享计算环境或跨不同模型运行多个训练作业时特别有价值。它会自动适应不断变化的系统条件，确保在无需人工干预的情况下实现最佳的资源分配。

### Apple Silicon MPS 训练

随着 Ultralytics YOLO 模型对 Apple Silicon 芯片的支持，现在可以在利用强大的 Metal Performance Shaders (MPS) 框架的设备上训练你的模型。MPS 提供了一种在 Apple 自研芯片上执行计算和图像处理任务的高性能方式。

要启用在 Apple Silicon 芯片上的训练，你应在启动训练过程时将 'mps' 指定为你的设备。以下是你在 Python 和命令行中如何进行此操作的示例：

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # load a pretrained model (recommended for training)

# Train the model with MPS
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device="mps")
```

> CLI

```shell
# Start training from a pretrained *.pt model using MPS
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640 device=mps
```

### 恢复中断的训练

在使用深度学习模型时，从先前保存的状态恢复训练是一项至关重要的功能。这在各种场景下都很方便，例如训练过程意外中断时，或者你希望用新数据或更多的 epoch 继续训练模型时。

当恢复训练时，Ultralytics YOLO 会加载最后保存的模型权重，并恢复优化器状态、[学习率](https://www.ultralytics.com/glossary/learning-rate)调度器以及 epoch 编号。这使你能够从上次中断的地方无缝继续训练过程。

您可以通过设置以下参数，在 Ultralytics YOLO 中轻松恢复训练 `resume` 参数为 `True` 在调用 `train` 方法时，并指定包含部分训练模型权重的 `.pt` 文件的路径。

以下是如何使用 Python 和命令行恢复中断训练的示例：

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

通过设置 `resume=True`，`train` 函数将从上次中断的地方继续训练，使用存储在 'path/to/last.pt' 文件中的状态。如果省略 `resume` 参数或将其设置为 `False`，`train` 函数将开启一个新的训练会话。

请记住，检查点默认在每个 epoch 结束时保存，或者使用 `save_period` 参数以固定间隔保存，因此你必须至少完成 1 个 epoch 才能恢复训练运行。

### MuSGD 优化器

在 YOLO26 中，**MuSGD** 是一种混合优化器，它将标准 **SGD** 更新与 **Muon 风格的正交化更新**相结合。

它**推荐用于较长的 YOLO26 训练运行和较大的数据集**，在这种情况下，正交化的 Muon 更新可以帮助稳定优化过程。

只有 2D 线性权重和 4D 卷积滤波器（重塑为 2D）与 SGD 一起接收 Muon 风格的更新，而所有其他参数（例如批归一化权重和偏置项）则保留在标准 SGD 上。

当使用 `optimizer=auto` 时，Ultralytics 会自动为较长的训练运行（通常当迭代次数 > 10000 时）选择 **MuSGD**。对于较短的运行，训练器会回退到 **AdamW**。

使用示例：

```sh
yolo train model=yolo26n.pt data=coco8.yaml optimizer=MuSGD
```

请参阅 `ultralytics/optim/muon.py` 中的实现，以及 `BaseTrainer.build_optimizer` 中的优化器自动选择逻辑。

## 参数

YOLO 模型的训练设置包含训练过程中使用的各种超参数和配置。这些设置会影响模型的性能、速度和 [准确率](https://www.ultralytics.com/glossary/accuracy)。关键训练设置包括批次大小、学习率、动量和权重衰减。此外，优化器、[损失函数](https://www.ultralytics.com/glossary/loss-function)和训练数据集组成的选择也会影响训练过程。仔细调整和实验这些设置对于优化性能至关重要。

| 参数              | 类型                     | 默认值   | 描述                                                         |
| :---------------- | :----------------------- | :------- | :----------------------------------------------------------- |
| `model`           | `str`                    | `None`   | 指定用于训练的模型文件。接受 `.pt` 预训练模型或 `.yaml` 配置文件的路径。这对于定义模型结构或初始化权重至关重要。 |
| `data`            | `str`                    | `None`   | 数据集配置文件的路径（例如 `coco8.yaml`）。该文件包含特定于数据集的参数，包括训练和 [验证数据](https://www.ultralytics.com/glossary/validation-data)的路径、类别名称以及类别数量。 |
| `epochs`          | `int`                    | `100`    | 总训练 epoch 数。每个 [epoch](https://www.ultralytics.com/glossary/epoch) 代表对整个数据集的一次完整遍历。调整此值会影响训练持续时间和模型性能。 |
| `time`            | `float`                  | `None`   | 以小时为单位的最长训练时间。如果设置，它将覆盖 `epochs` 参数，允许训练在指定持续时间后自动停止。这对于有时间限制的训练场景非常有用。 |
| `patience`        | `int`                    | `100`    | 在验证指标没有改善的情况下等待的 epoch 数，之后将提前停止训练。通过在性能停滞时停止训练，有助于防止 [过拟合](https://www.ultralytics.com/glossary/overfitting)。 |
| `batch`           | `int` 或 `float`         | `16`     | [Batch size](https://www.ultralytics.com/glossary/batch-size)，具有三种模式：设置为整数（例如 `batch=16`）、用于 60% GPU 内存利用率的自动模式（`batch=-1`），或带有指定利用率分数的自动模式（`batch=0.70`）。 |
| `imgsz`           | `int`                    | `640`    | 训练的目标图像尺寸。图像被调整为边长等于指定值的正方形（如果 `rect=False`），这保留了 YOLO 模型的长宽比，但 RT-DETR 不会。这会影响模型 [准确率](https://www.ultralytics.com/glossary/accuracy) 和计算复杂度。 |
| `save`            | `bool`                   | `True`   | 启用保存训练检查点和最终模型权重。这对于恢复训练或 [模型部署](https://www.ultralytics.com/glossary/model-deployment) 非常有用。 |
| `save_period`     | `int`                    | `-1`     | 保存模型检查点的频率，以 epoch 为单位。值为 -1 会禁用此功能。这对于在长时间训练期间保存中间模型非常有用。 |
| `cache`           | `bool`                   | `False`  | 启用将数据集图像缓存到内存（`True`/`ram`）、磁盘（`disk`）或禁用缓存（`False`）。通过减少磁盘 I/O 来提高训练速度，但会以增加内存使用量为代价。 |
| `device`          | `int` 或 `str` 或 `list` | `None`   | 指定用于训练的计算设备：单个 GPU（`device=0`）、多个 GPU（`device=[0,1]`）、CPU（`device=cpu`）、适用于 Apple 芯片的 MPS（`device=mps`）、华为昇腾 NPU（`device=npu:0` 或 `device=npu:0,1`），或者自动选择空闲 GPU（`device=-1`）或多个空闲 GPU（`device=[-1,-1]`）。 |
| `workers`         | `int`                    | `8`      | 用于数据加载的工作线程数（如果是多 GPU 训练，则为每个 `RANK` 分配的线程数）。影响数据预处理和输入模型的速度，在多 GPU 设置中特别有用。 |
| `project`         | `str`                    | `None`   | 保存训练输出的项目目录名称。允许对不同的实验进行有组织的存储。 |
| `name`            | `str`                    | `None`   | 训练运行的名称。用于在项目文件夹内创建子目录，存储训练日志和输出。 |
| `exist_ok`        | `bool`                   | `False`  | 如果为 True，则允许覆盖现有的项目/名称目录。这对于迭代实验非常有用，无需手动清除之前的输出。 |
| `save_dir`        | `str`                    | `None`   | 指定保存运行输出的确切目录，覆盖 `project`/`name` 组合。该路径按原样使用，不会自动递增，因此连续运行会重复使用同一个目录。 |
| `pretrained`      | `bool` 或 `str`          | `True`   | 确定是否从预训练权重开始训练。可以是布尔值，也可以是权重加载的字符串路径。`pretrained=False` 将从随机初始化的权重开始训练，同时保留模型架构。 |
| `optimizer`       | `str`                    | `'auto'` | 训练所选的优化器。选项包括 `SGD`、`MuSGD`、`Adam`、`Adamax`、`AdamW`、`NAdam`、`RAdam`、`RMSProp`，或用于基于模型配置自动选择的 `auto`。影响收敛速度和稳定性。 |
| `seed`            | `int`                    | `0`      | 设置训练的随机种子，确保在相同配置下的运行结果具有可重复性。 |
| `deterministic`   | `bool`                   | `True`   | 强制使用确定性算法，确保可重复性，但由于对非确定性算法的限制，可能会影响性能和速度。 |
| `verbose`         | `bool`                   | `True`   | 在训练期间启用详细输出，在控制台中显示进度条、每个 epoch 的指标以及其他训练信息。 |
| `single_cls`      | `bool`                   | `False`  | 在训练期间将多类别数据集中的所有类别视为单个类别。适用于二分类任务或专注于对象是否存在而非分类的情况。 |
| `classes`         | `list[int]`              | `None`   | 指定要训练的类别 ID 列表。有助于在训练期间过滤掉其他类别，仅关注特定类别。 |
| `rect`            | `bool`                   | `False`  | 启用最小填充策略——批次中的图像会被最小程度地填充以达到统一大小，最长边等于 `imgsz`。这可以提高效率和速度，但可能会影响模型精度。 |
| `multi_scale`     | `float`                  | `0.0`    | 每批次随机改变 `imgsz`，变化范围为 +/- `multi_scale`（例如 `0.25` -> `0.75x` 到 `1.25x`），并四舍五入到模型步长的倍数；`0.0` 表示禁用多尺度训练。 |
| `cos_lr`          | `bool`                   | `False`  | 使用余弦 [学习率](https://www.ultralytics.com/glossary/learning-rate) 调度器，使学习率随 epoch 变化遵循余弦曲线。有助于管理学习率以获得更好的收敛效果。 |
| `close_mosaic`    | `int`                    | `10`     | 在最后 N 个 epoch 禁用马赛克 [数据增强](https://www.ultralytics.com/glossary/data-augmentation)，以便在完成前稳定训练。设置为 0 则禁用此功能。 |
| `resume`          | `bool`                   | `False`  | 从上一个保存的检查点恢复训练。自动加载模型权重、优化器状态和 epoch 计数，无缝继续训练。 |
| `amp`             | `bool`                   | `True`   | 启用自动 [混合精度](https://www.ultralytics.com/glossary/mixed-precision) (AMP) 训练，在对精度影响极小的情况下减少内存使用并可能加快训练速度。 |
| `fraction`        | `float`                  | `1.0`    | 指定用于训练的数据集比例。允许在完整数据集的子集上进行训练，适用于实验或资源受限的情况。 |
| `profile`         | `bool`                   | `False`  | 在训练期间启用 ONNX 和 TensorRT 速度分析，有助于优化模型部署。 |
| `freeze`          | `int` 或 `list`          | `None`   | 冻结模型的前 N 层或按索引指定的层，从而减少可训练参数的数量。适用于微调或 [迁移学习](https://www.ultralytics.com/glossary/transfer-learning)。 |
| `lr0`             | `float`                  | `0.01`   | 初始学习率（例如 `SGD=1E-2`，`Adam=1E-3`）。调整此值对于优化过程至关重要，它会影响模型权重的更新速度。 |
| `lrf`             | `float`                  | `0.01`   | 最终学习率占初始学习率的比例 = (`lr0 * lrf`)，与调度器结合使用以随时间调整学习率。 |
| `momentum`        | `float`                  | `0.937`  | SGD 的动量因子或 [Adam 优化器](https://www.ultralytics.com/glossary/adam-optimizer) 的 beta1，影响在当前更新中纳入过去梯度的程度。 |
| `weight_decay`    | `float`                  | `0.0005` | L2 [正则化](https://www.ultralytics.com/glossary/regularization) 项，通过惩罚过大的权重来防止过拟合。 |
| `warmup_epochs`   | `float`                  | `3.0`    | 学习率预热的 epoch 数，将学习率从一个较小的值逐渐提高到初始学习率，以便在早期稳定训练。 |
| `warmup_momentum` | `float`                  | `0.8`    | 预热阶段的初始动量，在预热期间逐渐调整到设定的动量值。       |
| `warmup_bias_lr`  | `float`                  | `0.1`    | 预热阶段偏置参数的学习率，有助于在初始 epoch 中稳定模型训练。 |
| `distill_model`   | `str`                    | `None`   | 指向用于知识蒸馏的教师模型检查点（例如 `yolo26x.pt`）的路径。设置后，学生模型将通过冻结的教师模型引导的额外蒸馏损失进行训练。 |
| `dis`             | `float`                  | `6.0`    | 添加到标准检测损失中的蒸馏损失权重。较高的值会增加教师特征引导的影响力。 |
| `box`             | `float`                  | `7.5`    | [损失函数](https://www.ultralytics.com/glossary/loss-function) 中框损失组件的权重，影响预测 [边界框](https://www.ultralytics.com/glossary/bounding-box) 坐标的准确性权重。 |
| `cls`             | `float`                  | `0.5`    | 总损失函数中分类损失的权重，影响正确分类预测相对于其他组件的重要性。 |
| `cls_pw`          | `float`                  | `0.0`    | 用于处理类别不平衡的类别加权幂指数，采用类别频率的倒数。`0.0` 禁用类别加权，`1.0` 应用完全倒数频率加权。0 到 1 之间的值提供部分加权。 |
| `dfl`             | `float`                  | `1.5`    | 分布焦点损失 (DFL) 的权重，这是一种用于回归边界框边缘距离的边界框定位项。 |
| `pose`            | `float`                  | `12.0`   | 针对姿态估计模型训练中的姿态损失权重，影响对关键点预测准确性的重视程度。 |
| `kobj`            | `float`                  | `1.0`    | 姿态估计模型中关键点目标性损失的权重，平衡检测置信度和姿态准确性。 |
| `rle`             | `float`                  | `1.0`    | 姿态估计模型中残差对数似然估计损失的权重，影响关键点定位的精度。 |
| `angle`           | `float`                  | `1.0`    | obb 模型中角度损失的权重，影响旋转边界框角度预测的精度。     |
| `nbs`             | `int`                    | `64`     | 用于损失归一化的标称批次大小。                               |
| `overlap_mask`    | `bool`                   | `True`   | 确定训练时是否应将对象掩码合并为单个掩码，还是为每个对象保持独立。如果重叠，在合并期间较小的掩码会覆盖在较大的掩码之上。 |
| `mask_ratio`      | `int`                    | `4`      | 分割掩码的下采样比率，影响训练期间所用掩码的分辨率。         |
| `dropout`         | `float`                  | `0.0`    | 分类任务中用于正则化的 Dropout 率，通过在训练期间随机省略单元来防止过拟合。 |
| `val`             | `bool`                   | `True`   | 在训练期间启用验证，允许在单独的数据集上定期评估模型性能。   |
| `plots`           | `bool`                   | `True`   | 生成并保存训练和验证指标的绘图以及预测示例，从而提供关于模型性能和学习进度的视觉见解。 |
| `compile`         | `bool` 或 `str`          | `False`  | 启用 PyTorch 2.x 的 `torch.compile` 图编译，后台使用 `backend='inductor'`。接受 `True` -> `"default"`，`False` -> 禁用，或字符串模式如 `"default"`、`"reduce-overhead"`、`"max-autotune-no-cudagraphs"`。如果不支持，将回退到 eager 模式并发出警告。 |
| `channels_last`   | `bool`                   | `False`  | 在训练期间为卷积使用 channels_last (NHWC) 内存格式，以此加速 CUDA Tensor Core GPU，且不改变结果。在 CPU 和 MPS 上会自动忽略，因为它们无法从中获得收益。 |
| `max_det`         | `int`                    | `300`    | 指定在训练验证阶段保留的对象最大数量。                       |

> 关于批次大小设置的说明
>
> `batch` 参数可以通过三种方式配置：
>
> - **固定 [批次大小](https://www.ultralytics.com/glossary/batch-size)**：设置一个整数值（例如 `batch=16`），直接指定每个批次的图像数量。
> - **自动模式（60% GPU 内存）**：使用 `batch=-1` 自动调整批次大小，以利用大约 60% 的 CUDA 内存。
> - **带利用率分数的自动模式**：设置一个分数（例如 `batch=0.70`），根据指定的 GPU 内存使用比例来调整批次大小。
> - **OOM 自动重试**：如果第一个 epoch 期间发生 CUDA 内存溢出错误，训练器会自动将批次大小减半并重试（最多 3 次）。这仅适用于单 GPU 训练；多 GPU (DDP) 训练将立即引发错误。

>`rect = True` 使用长方形训练
>
>Setting "rect"=True allows you to train using rectangular images, not necessarily square ones. This allows for more efficient use of GPU memory as there's less need for padding spatial dimensions.
>
>[Custom input size: letterbox vs resizing · Issue #11350 ](https://github.com/ultralytics/yolov5/issues/11350)
>
>[About the rectangle training · Issue #4819](https://github.com/ultralytics/ultralytics/issues/4819)

### 增强设置和超参数

增强技术对于通过在 [训练数据](https://www.ultralytics.com/glossary/training-data) 中引入变异性来提高 YOLO 模型的稳健性和性能至关重要，有助于模型更好地推广到未见数据。

下表概述了每个增强参数的目的和效果：

| 参数                                                         | 类型    | 默认值        | 支持的任务                                     | 范围          | 描述                                                         |
| :----------------------------------------------------------- | :------ | :------------ | :--------------------------------------------- | :------------ | :----------------------------------------------------------- |
| [`hsv_h`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#hue-adjustment-hsv_h) | `float` | `0.015`       | `detect`, `segment`, `pose`, `obb`, `classify` | `0.0 - 1.0`   | 通过色轮的一小部分调整图像的色调，引入颜色变异性。有助于模型在不同光照条件下实现泛化。 |
| [`hsv_s`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#saturation-adjustment-hsv_s) | `float` | `0.7`         | `detect`, `segment`, `pose`, `obb`, `classify` | `0.0 - 1.0`   | 通过一小部分比例改变图像的饱和度，影响颜色的强度。适用于模拟不同的环境条件。 |
| [`hsv_v`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#brightness-adjustment-hsv_v) | `float` | `0.4`         | `detect`, `segment`, `pose`, `obb`, `classify` | `0.0 - 1.0`   | 通过一小部分比例修改图像的值（亮度），帮助模型在各种光照条件下表现良好。 |
| [`degrees`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#rotation-degrees) | `float` | `0`           | `detect`, `segment`, `pose`, `obb`             | `0.0 - 180`   | 在指定的度数范围内随机旋转图像，提高模型识别不同朝向物体的能力。 |
| [`translate`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#translation-translate) | `float` | `0.1`         | `detect`, `segment`, `pose`, `obb`             | `0.0 - 1.0`   | 按图像尺寸的一定比例水平和垂直平移图像，有助于学习检测部分可见的物体。 |
| [`scale`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#scale-scale) | `float` | `0.5`         | `detect`, `segment`, `pose`, `obb`, `classify` | `0 - 1`       | 通过增益因子缩放图像，模拟相机与物体距离不同的情况。         |
| [`shear`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#shear-shear) | `float` | `0`           | `detect`, `segment`, `pose`, `obb`             | `-180 - +180` | 按指定角度对图像进行剪切，模拟从不同角度观察物体的效果。     |
| [`perspective`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#perspective-perspective) | `float` | `0`           | `detect`, `segment`, `pose`, `obb`             | `0.0 - 0.001` | 对图像应用随机透视变换，增强模型在3D空间中理解物体的能力。   |
| [`flipud`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#flip-up-down-flipud) | `float` | `0`           | `detect`, `segment`, `pose`, `obb`, `classify` | `0.0 - 1.0`   | 以指定的概率将图像上下翻转，在不影响物体特性的前提下增加数据变体。 |
| [`fliplr`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#flip-left-right-fliplr) | `float` | `0.5`         | `detect`, `segment`, `pose`, `obb`, `classify` | `0.0 - 1.0`   | 以指定的概率将图像左右翻转，有助于学习对称物体并增加数据集的多样性。 |
| [`bgr`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#bgr-channel-swap-bgr) | `float` | `0`           | `detect`, `segment`, `pose`, `obb`             | `0.0 - 1.0`   | 以指定的概率将图像通道从 RGB 翻转为 BGR，有助于增强对错误通道排序的鲁棒性。 |
| [`mosaic`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#mosaic-mosaic) | `float` | `1`           | `detect`, `segment`, `pose`, `obb`             | `0.0 - 1.0`   | 将四张训练图像组合成一张，模拟不同的场景构成和物体交互。对于复杂场景理解非常有效。 |
| [`mixup`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#mixup-mixup) | `float` | `0`           | `detect`, `segment`, `pose`, `obb`             | `0.0 - 1.0`   | 混合两张图像及其标签，创建一个复合图像。通过引入标签噪声和视觉变体，提高模型的泛化能力。 |
| [`cutmix`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#cutmix-cutmix) | `float` | `0`           | `detect`, `segment`, `pose`, `obb`             | `0.0 - 1.0`   | 结合两张图像的部分内容，在保持不同区域的同时创建一个部分混合图像。通过创建遮挡场景来增强模型的鲁棒性。 |
| [`copy_paste`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#copy-paste-copy_paste) | `float` | `0`           | `segment`                                      | `0.0 - 1.0`   | 在图像之间复制和粘贴物体，以增加物体实例。                   |
| [`copy_paste_mode`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#copy-paste-mode-copy_paste_mode) | `str`   | `flip`        | `segment`                                      | -             | 指定使用的 `copy-paste` 策略。选项包括 `'flip'` 和 `'mixup'`。 |
| [`auto_augment`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#auto-augment-auto_augment) | `str`   | `randaugment` | `classify`                                     | -             | 应用预定义的增强策略（`'randaugment'`、`'autoaugment'` 或 `'augmix'`），通过视觉多样性来提升模型性能。 |
| [`erasing`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#random-erasing-erasing) | `float` | `0.4`         | `classify`                                     | `0.0 - 1.0`   | 在训练期间随机擦除图像区域，鼓励模型关注不太明显的特征。     |
| [`augmentations`](https://docs.ultralytics.com/zh/guides/yolo-data-augmentation#custom-albumentations-transforms-augmentations) | `list`  | `None`        | `detect`, `segment`, `pose`, `obb`             | -             | 用于高级数据增强的自定义 Albumentations 转换（仅限 Python API）。接受转换对象列表以满足特定的增强需求。 |

这些设置可以根据数据集和当前任务的具体要求进行调整。尝试不同的数值有助于找到实现最佳模型性能的最佳增强策略。

> 有关训练增强操作的更多信息，请参阅 [参考部分](https://docs.ultralytics.com/reference/data/augment)。

## Example

py

```python
from pathlib import Path
from ultralytics import YOLO, settings


settings.update(
    {
        "tensorboard": True,
        "datasets_dir": "datasets",
        "weights_dir": "weights",
        "runs_dir": "runs",
    }
)


yaml_path = Path("ultralytics/cfg/models/11/yolo26n.yaml").resolve()
model_path = Path("weights/yolo26n.pt").resolve()
data_path = Path("datasets/coco/coco.yaml").resolve()
project = "coco"
name = "yolo26n/train"

print(f"{yaml_path} is exists: {yaml_path.exists()}")
print(f"{model_path} is exists: {model_path.exists()}")
print(f"{data_path} is exists: {data_path.exists()}")


# Load a model
# model = YOLO(yaml_path, task="detect")  # build a new model from YAML
model = YOLO(model_path, task="detect")  # load a pretrained model (recommended for training)
# model = YOLO(yaml_path, task="detect").load(model_path)  # build from YAML and transfer weights


# Train the model
results = model.train(
    data=data_path,
    epochs=100,
    time=None,
    patience=100,
    batch=-1,
    imgsz=640,
    save=True,
    save_period=-1,
    cache=False,
    device=0,
    workers=8,
    project=project,
    name=name,
    exist_ok=False,
    pretrained=True,
    optimizer="auto",
    seed=0,
    deterministic=True,
    verbose=True,
    single_cls=False,
    classes=None,  # list[int] | None, 指定要训练的类 ID 列表。可用于在训练期间过滤掉并仅关注某些类。
    rect=False,
    multi_scale=0.0,
    cos_lr=True,
    close_mosaic=10,
    resume=False,
    amp=True,  # 会在脚本执行目录下载一个小模型用来检查 amp 是否可用
    fraction=1.0,
    profile=False,
    freeze=None,
    lr0=0.01,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3,
    warmup_momentum=0.8,
    warmup_bias_lr=0.1,
    val=True,
    plots=False,
    compile=False,
    max_det=300,
    # below are image enhance hyperparameters
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=0.0,
    translate=0.1,
    scale=0.5,
    shear=0.0,
    perspective=0.0,
    flipud=0.0,
    fliplr=0.5,
    bgr=0.0,
    mosaic=1.0,
    mixup=0.0,
    cutmix=0.0,
    copy_paste=0.0,
    copy_paste_mode="flip",
    auto_augment="randaugment",
    erasing=0.4,
    augmentations="",
    cfg=None,
)
```

cmd

```sh
# Build a new model from YAML and start training from scratch
yolo detect train data=coco8.yaml model=yolo26n.yaml epochs=100 imgsz=640 project=coco8 name=yolo26n/train

# Start training from a pretrained *.pt model
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640 project=coco8 name=yolo26n/train

# Build a new model from YAML, transfer pretrained weights to it and start training
yolo detect train data=coco8.yaml model=yolo26n.yaml pretrained=yolo26n.pt epochs=100 imgsz=640 project=coco8 name=yolo26n/train
```

> `Multi-GPU Training`

```sh
# Start training from a pretrained *.pt model using GPUs 0 and 1
yolo detect train data=coco8.yaml model=yolo26n.pt epochs=100 imgsz=640 device=0,1 project=coco8 name=yolo26n/train
```

> `auto optimizer`

```sh
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=ultralytics/cfg/models/11/yolo26n.yaml pretrained=weights/yolo26n.pt data=ultralytics/datasets/coco8.yaml project=coco8 name=yolo26n/train

#                                                                                                                                model可以直接设置为pt
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=weights/yolo26n.pt data=ultralytics/cfg/datasets/coco8.yaml project=coco8 name=yolo26n/train

#                                                        rtdetr 训练轮数更少
yolo detect train imgsz=640 batch=-1 workers=8 epochs=100 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=ultralytics/cfg/models/rt-detr/rtdetr-x.yaml pretrained=weights/rtdetr-x.pt data=ultralytics/cfg/datasets/coco8.yaml project=coco8 name=yolo26n/train

#                                                        rtdetr 训练轮数更少                                                       model可以直接设置为pt
yolo detect train imgsz=640 batch=-1 workers=8 epochs=100 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=weights/rtdetr-x.pt data=ultralytics/cfg/datasets/coco8.yaml project=coco8 name=yolo26n/train
```

> `resume`

```sh
#                                                                                                                                model=最后的pt
yolo detect train imgsz=640 batch=-1 workers=8 epochs=300 patience=0 close_mosaic=10 fraction=1.0 cos_lr=True device=0 model=weights/last.pt data=ultralytics/cfg/datasets/coco8.yaml resume=True exist_ok=True project=coco8 name=yolo26n/train
```

## **不需要在模型配置中显示更改类别数**

> 会自动将nc调整为数据集的类别数量

```sh
> yolo detect train imgsz=640 batch=-1 epochs=300 optimizer=SGD lr0=0.01 cos_lr=True device=0 pretrained=weights/yolo26n.pt model=ultralytics/models/11/yolo26n.yaml data=ultralytics/datasets/classes20.yaml

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
yolo26n summary: 225 layers, 3157200 parameters, 3157184 gradients, 8.9 GFLOPs

Transferred 355/355 items from pretrained weights
Ultralytics yolo26.0.58  Python-3.10.9 torch-2.0.0+cu118 CUDA:0 (NVIDIA GeForce GTX 1080 Ti, 11264MiB)
yolo\engine\trainer: detect, train, model=ultralytics/models/11/yolo26n.yaml, data=ultralytics/datasets/classes20.yaml, epochs=300, patience=50, batch=-1, imgsz=640, save=True, save_period=-1, cache=False, device=0, workers=8, project=None, name=None, exist_ok=False, pretrained=weights/yolo26n.pt, optimizer=SGD, verbose=True, seed=0, deterministic=True, single_cls=False, image_weights=False, rect=False, cos_lr=True, close_mosaic=10, resume=False, amp=True, overlap_mask=True, mask_ratio=4, dropout=0.0, val=True, split=val, save_json=False, save_hybrid=False, conf=None, iou=0.7, max_det=300, half=False, dnn=False, plots=True, source=None, show=False, save_txt=False, save_conf=False, save_crop=False, hide_labels=False, hide_conf=False, vid_stride=1, line_thickness=3, visualize=False, augment=False, agnostic_nms=False, classes=None, retina_masks=False, boxes=True, format=torchscript, keras=False, optimize=False, int8=False, dynamic=False, simplify=False, opset=None, workspace=4, nms=False, lr0=0.01, lrf=0.01, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, warmup_bias_lr=0.1, box=7.5, cls=0.5, dfl=1.5, fl_gamma=0.0, label_smoothing=0.0, nbs=64, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.1, scale=0.5, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, mosaic=1.0, mixup=0.0, copy_paste=0.0, cfg=None, v5loader=False, tracker=botsort.yaml, save_dir=d:\code\ultralytics\runs\detect\train2
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
yolo26n summary: 225 layers, 3014748 parameters, 3014732 gradients, 8.2 GFLOPs

Transferred 319/355 items from pretrained weights
TensorBoard: Start with 'tensorboard --logdir d:\code\ultralytics\runs\detect\train', view at http://localhost:6006/
AMP: running Automatic Mixed Precision (AMP) checks with yolo26n...
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

在 COCO8 数据集上验证已训练的 YOLO26n 模型[准确率](https://www.ultralytics.com/glossary/accuracy)。不需要任何参数，因为 `model` 会将其训练 `data` 和参数保留为模型属性。请参阅下方的参数部分获取验证参数的完整列表。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # load an official model
model = YOLO("path/to/best.pt")  # load a custom model

# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.box.map  # map50-95
metrics.box.map50  # map50
metrics.box.map75  # map75
metrics.box.maps  # a list containing mAP50-95 for each category
metrics.box.image_metrics  # per-image metrics dictionary with precision, recall, F1, TP, FP, and FN
```

> CLI

```sh
yolo detect val model=yolo26n.pt      # val official model
yolo detect val model=path/to/best.pt # val custom model
```

## 参数

在验证 YOLO 模型时，可以微调多个参数以优化评估过程。这些参数控制输入图像尺寸、批处理和性能阈值等方面。

下方是每个参数的详细分解，帮助你有效地自定义验证设置。

| 参数           | 类型            | 默认值  | 描述                                                         |
| :------------- | :-------------- | :------ | :----------------------------------------------------------- |
| `data`         | `str`           | `None`  | 指定数据集配置文件的路径（例如 `coco8.yaml`）。此文件应包含 [validation data](https://www.ultralytics.com/glossary/validation-data) 的路径。 |
| `imgsz`        | `int`           | `640`   | 定义输入图像的大小。所有图像在处理前都会调整为此尺寸。较大的尺寸可能会提高小对象的精度，但会增加计算时间。 |
| `batch`        | `int`           | `16`    | 设置每批图像的数量。更高的值更有效地利用 GPU 显存，但需要更多的 VRAM。请根据可用的硬件资源进行调整。 |
| `save_json`    | `bool`          | `False` | 如果为 `True`，则将结果保存为 JSON 文件，以便进行进一步分析、与其他工具集成或提交给 COCO 等评估服务器。 |
| `conf`         | `float`         | `0.001` | 设置检测的最低置信度阈值。较低的值会增加召回率，但可能会引入更多误报。在 [validation](https://docs.ultralytics.com/modes/val) 期间使用，以计算精度-召回率曲线。对于 OBB 验证，默认为 `0.01` 以减少内存使用。 |
| `iou`          | `float`         | `0.7`   | 设置 [Intersection Over Union](https://www.ultralytics.com/glossary/intersection-over-union-iou) 阈值，用于 [Non-Maximum Suppression](https://www.ultralytics.com/glossary/non-maximum-suppression-nms)。控制重复检测的消除。 |
| `max_det`      | `int`           | `300`   | 限制每张图像的最大检测数。在密集场景中非常有用，可以防止过多的检测并管理计算资源。 |
| `quantize`     | `int` 或 `str`  | `None`  | 验证精度：`16`/`"fp16"` 可在支持的 GPU 上启用 FP16 验证；`32`/`"fp32"`/未设置则为 FP32。INT8/PTQ 量化在 [export](https://docs.ultralytics.com/zh/modes/export#quantization-options) 期间进行配置，并在验证导出模型时使用。取代了已弃用的 `half` 标志。 |
| `device`       | `str`           | `None`  | 指定验证设备（`cpu`、`cuda:0`、`npu`、`npu:0` 等）。当为 `None` 时，自动选择最佳可用设备。多个 CUDA 设备可以用逗号分隔指定。 |
| `dnn`          | `bool`          | `False` | 如果为 `True`，则使用 [OpenCV](https://www.ultralytics.com/glossary/opencv) DNN 模块进行 ONNX 模型推理，提供了一种替代 [PyTorch](https://www.ultralytics.com/glossary/pytorch) 推理方法的方式。 |
| `plots`        | `bool`          | `True`  | 设为 `True` 时，会生成并保存预测结果与真值对比的图表、混淆矩阵以及 PR 曲线，用于直观评估模型性能。 |
| `classes`      | `list[int]`     | `None`  | 指定需要评估的类别 ID 列表。这在评估过程中过滤并仅关注特定类别时非常有用。 |
| `rect`         | `bool`          | `True`  | 如果设为 `True`，将使用矩形推理进行批处理，减少填充（padding），通过按图像原始长宽比进行处理，从而可能提高速度和效率。 |
| `split`        | `str`           | `'val'` | 确定用于验证的数据集拆分（`val`、`test` 或 `train`）。允许你灵活选择数据片段进行性能评估。 |
| `project`      | `str`           | `None`  | 保存验证输出的项目目录名称。有助于整理来自不同实验或模型的结果。 |
| `name`         | `str`           | `None`  | 验证运行的名称。用于在项目文件夹内创建子目录，存储验证日志和输出。 |
| `verbose`      | `bool`          | `True`  | 如果设为 `True`，会在验证过程中显示详细信息，包括各类的指标、批处理进度以及额外的调试信息。 |
| `save_txt`     | `bool`          | `False` | 如果设为 `True`，将以文本文件形式保存检测结果（每张图像一个文件），便于进一步分析、自定义后处理或与其他系统集成。 |
| `save_conf`    | `bool`          | `False` | 如果设为 `True`，在启用 `save_txt` 时会在保存的文本文件中包含置信度值，从而为分析和过滤提供更详细的输出。 |
| `workers`      | `int`           | `8`     | 用于数据加载的工作线程数。更高的数值可以加快数据预处理速度，但可能会增加 CPU 使用率。设为 0 表示使用主线程，在某些环境中可能更稳定。 |
| `augment`      | `bool`          | `False` | 在验证期间启用测试时增强（TTA），通过对输入的转换版本运行推理，以牺牲推理速度为代价，潜在地提高检测准确率。 |
| `agnostic_nms` | `bool`          | `False` | 启用类无关的 [Non-Maximum Suppression](https://www.ultralytics.com/glossary/non-maximum-suppression-nms)，无论其预测类别如何，都会合并重叠的框。这对于以实例为核心的应用非常有用。对于端到端模型（YOLO26、YOLOv10），这仅防止同一检测结果出现多个类别标签（IoU=1.0 重复），而不会在不同框之间执行基于 IoU 阈值的抑制。 |
| `single_cls`   | `bool`          | `False` | 在验证过程中将所有类别视为单一类别。对于评估二分类任务的模型性能，或者当类别区分并不重要时非常有用。 |
| `visualize`    | `bool`          | `False` | 为每张图像可视化真值（ground truths）、真阳性、假阳性及假阴性。有助于调试和模型解释。 |
| `show_labels`  | `bool`          | `True`  | 当 `visualize=True` 时，在验证可视化中显示类别标签。设为 `False` 可获得更清晰的匹配项和错误查看效果。 |
| `show_conf`    | `bool`          | `True`  | 当 `visualize=True` 时，在验证可视化中显示置信度分数。设为 `False` 可获得更清晰的匹配项和错误查看效果。 |
| `compile`      | `bool` 或 `str` | `False` | 启用 PyTorch 2.x 的 `torch.compile` 图编译，后台使用 `backend='inductor'`。接受 `True` -> `"default"`，`False` -> 禁用，或字符串模式如 `"default"`、`"reduce-overhead"`、`"max-autotune-no-cudagraphs"`。如果不支持，将回退到 eager 模式并发出警告。 |
| `end2end`      | `bool`          | `None`  | 覆盖支持无 NMS 推理（YOLO26、YOLOv10）的 YOLO 模型中的端到端模式。将其设为 `False`，允许你使用传统的 NMS 流水线运行验证，同时还可以使用 `iou` 参数。 |

这些设置中的每一项在验证过程中都发挥着至关重要的作用，实现了对 YOLO 模型可定制且高效的评估。根据你的具体需求和资源调整这些参数，有助于在准确性和性能之间取得最佳平衡。

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

py

```python
from pathlib import Path
from ultralytics import YOLO, settings
from ultralytics.utils.metrics import DetMetrics
import pandas as pd


settings.update(
    {
        "tensorboard": True,
        "datasets_dir": "datasets",
        "weights_dir": "weights",
        "runs_dir": "runs",
    }
)


model_path = Path("weights/yolo26n.pt").resolve()
data_path = Path("datasets/coco/coco.yaml").resolve()
project = "coco"
name = "yolo26n/val"


print(f"{model_path} is exists: {model_path.exists()}")
print(f"{data_path} is exists: {data_path.exists()}")


model = YOLO(model_path, task="detect")

metrics: DetMetrics = model.val(
    data=data_path,
    imgsz=640,
    batch=1,
    save_json=False,
    conf=0.001,
    iou=0.7,
    max_det=300,
    device=0,
    dnn=False,
    plots=True,
    classes=None,  # list[int] | None, 指定要训练的类 ID 列表。可用于在评估期间过滤并仅关注某些类。
    rect=True,
    split="val",
    project=project,
    name=name,
    verbose=True,
    save_txt=False,
    save_conf=False,
    workers=8,
    augment=False,
    agnostic_nms=False,
    single_cls=False,
    visualize=False,
    compile=False,
    end2end=None,
)

# attrs
print(f"metrics attrs: {[i for i in dir(metrics) if not i.startswith('__')]}\n")
print(f"metrics.box attrs: {[i for i in dir(metrics.box) if not i.startswith('__')]}\n")

print(f"map\n:{metrics.box.map}\n")  # mAP50-95
print(f"map50\n:{metrics.box.map50}\n")  # mAP50
print(f"map75\n:{metrics.box.map75}\n")  # mAP75
print(f"maps\n:{metrics.box.maps}\n")  # list of mAP50-95 for each category
# per-image metrics dictionary with precision, recall, F1, TP, FP, and FN
print(f"image_metrics\n:{metrics.box.image_metrics}\n")

# confusion_matrix: polars.DataFrame
metrics_df: pd.DataFrame = metrics.to_df().to_pandas()
metrics_df_save_path = metrics.save_dir / "metrics.csv"
metrics_df.to_csv(metrics_df_save_path, index=False)
print(f"metrics_df saved to {metrics_df_save_path}")
```

cmd

```sh
yolo detect val imgsz=640 save_json=True save_txt=True save_conf=True conf=0.25 iou=0.7 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo26n.pt device=0 project=coco8 name=yolo26n/val
```

## 验证原理

代码主要在

验证基类 https://github.com/ultralytics/ultralytics/blob/main/ultralytics/engine/validator.py

目标检测具体实现 https://github.com/ultralytics/ultralytics/blob/main/ultralytics/models/yolo/detect/val.py

### 流程

```sh
DetectionValidator()
  └─ __call__(model=...)
       ├─ AutoBackend / DataLoader 初始化
       ├─ 准备 model
       ├─ 准备 data / dataloader
       ├─ model.eval()
       ├─ warmup
       ├─ init_metrics()            # DetMetrics 准备
       ├─ for batch in dataloader:
       │    ├─ preprocess()         # 图像归一化、移到设备
       │    ├─ model()              # 推理
       │    ├─ loss()               # 计算（训练时）
       │    ├─ postprocess()        # NMS，得到 bboxes/conf/cls
       │    │    ├─ NMS
       │    └─ update_metrics()     # 匹配真值，累积 tp/conf
       │         ├─ _prepare_batch()    # 取出当前图的 GT（xywh → xyxy，映射到图像尺寸）
       │         ├─ _prepare_pred()     # 如果是单类别模式，就把所有预测类别都当成 0 类。
       │         ├─ _process_batch()
       │         │    ├─ box_iou()            # 计算 IoU 矩阵 [M_true, N_pred]
       │         │    └─ match_predictions()  # 计算 TP [N_pred, 10]
       │         └─ update_stats(tp, target_cls, conf, ...)
       ├─ gather_stats()            # DDP 汇总
       ├─ get_stats()               # 获取最终指标
       │    └─ process()            # 计算最终指标
       ├─ finalize_metrics()        # 记录速度、混淆矩阵
       ├── save_json / eval_json
       └── return stats
```

### match_predictions：TP 多 IOU 阈值匹配

这是最关键的一步，输出形状是 (N_pred, 10)，对应 10 个 IoU 阈值（0.50 到 0.95，步长 0.05）：

对每个 IoU 阈值 t：

1. 只保留类别匹配的 IoU 值（wrong class → 0）
2. 找所有 iou >= t 的 (gt, pred) 配对
3. 默认使用贪心匹配：按 IoU 降序排序，每个 GT 和每个预测最多匹配一次。
   若 use_scipy=True，则使用匈牙利算法（linear_sum_assignment）做最优匹配。
4. 只有类别一致且 IoU ≥ 阈值 才算 True Positive。

返回 correct 矩阵，形状为 [N_pred, 10]（N_pred 个预测，10 个 IoU 阈值，0.50 到 0.95），表示该预测在每个阈值下是否为 TP。

类别错误或者 IOU 不达标都是 False

注意: 这里只记录了每个预测框在不同的 IOU 下是否匹配上了真实框，没有记录对应的真实框，因为不需要，真实类别、预测类别和预测分数在 update_stats 中记录了

### update_stats

最终 stats 里积累了每张图的数据：

| 字段       | 含义                                   |
| ---------- | -------------------------------------- |
| tp         | 每个预测框在 10 个 IoU 阈值下是否为 TP |
| target_cls | 当前图片所有 GT 类别                   |
| target_img | 当前图片出现过哪些类别                 |
| conf       | 每个预测框的置信度                     |
| pred_cls   | 每个预测框的预测类别                   |
| im_name    | 图片名                                 |

### process

1. 收集所有图片的预测结果
2. 按 confidence 从高到低排序(这里不考虑类别)
3. 对每个类别分别统计 TP / FP
4. 得到 Precision-Recall 曲线
5. 对 PR 曲线积分得到 AP
6. 对类别取平均得到 mAP
7. 对 10 个 IoU 阈值取平均得到 mAP50-95
8. 计算 Percision / Recall



#### 计算 Precision-Recall 曲线举例

假设 `car` 类有 3 个真实目标：

```
GT car 数量 n_l = 3
```

模型预测了 5 个 car 框，按 conf 降序：

| 排名 | conf | tp@0.5 |
| ---- | ---- | ------ |
| 1    | 0.95 | True   |
| 2    | 0.88 | False  |
| 3    | 0.70 | True   |
| 4    | 0.40 | True   |
| 5    | 0.20 | False  |

然后累计：

| 截断到哪个 conf | TP 累计 | FP 累计 | Precision    | Recall       |
| --------------- | ------- | ------- | ------------ | ------------ |
| ≥ 0.95          | 1       | 0       | 1 / 1 = 1.00 | 1 / 3 = 0.33 |
| ≥ 0.88          | 1       | 1       | 1 / 2 = 0.50 | 1 / 3 = 0.33 |
| ≥ 0.70          | 2       | 1       | 2 / 3 = 0.67 | 2 / 3 = 0.67 |
| ≥ 0.40          | 3       | 1       | 3 / 4 = 0.75 | 3 / 3 = 1.00 |
| ≥ 0.20          | 3       | 2       | 3 / 5 = 0.60 | 3 / 3 = 1.00 |

这条表就形成了一条 **Precision-Recall 曲线**。

然后 AP 就是这条 PR 曲线下面的面积。

10个 IOU 阈值就是用不同的阈值来判断是否是 TP 的方法，会按照上面的方式计算10次。

#### `conf` 作用

`conf`**不会直接当成权重参与。**

也就是说，不是这样：

```
AP = 某种 tp * conf 的加权平均
```

不是。

`conf` 的作用主要是：

```
决定预测框排序
决定不同 confidence threshold 下的 P/R 点
```

所以 AP 评估的是：

> 模型能不能把正确的框排在错误的框前面。

如果一个模型的分数校准不准，比如它总是把数值压得很低：

```
0.31, 0.28, 0.25
```

但排序完全正确，那么 AP 可能依然不错。

如果另一个模型数值看起来很自信：

```
0.99, 0.98, 0.97
```

但高分里面一堆 FP，那 AP 会很难看。

所以 **AP 更关心 ranking，不太关心 confidence 的绝对值校准**。这就是为什么只看 `conf=0.9` 这种绝对值有时候很迷惑。

默认 detect val 通常很低，比如 `0.001`，目的就是尽量保留候选框，让 mAP 评估可以扫完整的 PR 曲线。

如果你把验证时的 `conf` 设得很高，比如：

```
yolo val conf=0.5
```

那很多低分预测会提前被过滤掉。

后果是：

```
Recall 可能上不去
mAP 可能下降
```

所以做标准 mAP 评估时，一般不要把 `conf` 设太高。

#### 计算 Precision 和 Recall

预测是否正确按照 IOU=0.5 的结果判断

1. 按 conf 从高到低排序

2. 每个类别单独累计 TP / FP

3. 得到 precision / recall 曲线

4. 用 IoU=0.5 那一列构造 P-Confidence / R-Confidence 曲线

5. 算 F1-Confidence 曲线
   $$
   F1 = \frac {2 \times P \times R}{(P + R)}
   $$
   F1 是 Precision 和 Recall 的调和平均，倾向于惩罚那种“一个高一个低”的情况。

   比如：

   | Precision | Recall | F1   |
   | --------- | ------ | ---- |
   | 0.95      | 0.20   | 0.33 |
   | 0.60      | 0.60   | 0.60 |
   | 0.40      | 0.90   | 0.55 |

   所以 F1 最大的点通常是一个折中点。

6. 找平均 F1 最大的 confidence 阈值

   a. 对所有类别的 F1 按类别求平均
   b. 对平均 F1 曲线做平滑
   c. 找到平均 F1 最大的位置 i
   d. 取这个 confidence 阈值下所有类别的 P/R/F1

7. 取该阈值下每个类别的 P / R

8. 对类别求平均

9. 最终得到类别平均 Precision / Recall

用一个小例子理解

假设某个类别在不同 confidence 阈值下结果是：

| conf 阈值 | Precision | Recall | F1   |
| --------- | --------- | ------ | ---- |
| 0.90      | 1.00      | 0.20   | 0.33 |
| 0.70      | 0.85      | 0.50   | 0.63 |
| 0.50      | 0.72      | 0.75   | 0.73 |
| 0.30      | 0.50      | 0.90   | 0.64 |
| 0.10      | 0.30      | 0.98   | 0.46 |

如果 F1 最大在 `conf=0.50`，那这个类别最终汇总用的就是：

```
Precision = 0.72
Recall    = 0.75
```

不是：

```
所有 Precision 的平均
所有 Recall 的平均
PR 曲线面积
conf=0.001 时的 P/R
```

### 总结

detect val 里的最终 `Precision` 和 `Recall` 是基于 IoU=0.5 的 TP/FP 统计，在使所有类别平均 F1 最大的 confidence 阈值处取得的类别平均 Precision 和 Recall。

而 `mAP50` / `mAP50-95` 才是对 PR 曲线做积分得到的 AP/mAP。

 `P/R` 是一个“最佳 F1 点”，`mAP` 是整条曲线的综合表现。



# [预测](https://docs.ultralytics.com/zh/modes/predict/)

## 使用示例

Ultralytics YOLO 模型在进行推理时返回一个 Python `Results` 对象列表，或者当传入 `stream=True` 时，返回一个内存高效的 Python `Results` 对象生成器：

> 设置 `stream=False` 时返回列表

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # pretrained YOLO26n model

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

> 设置 `stream=True` 时返回生成器

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # pretrained YOLO26n model

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

YOLO26 可以处理不同类型的推理输入源，如下表所示。输入源包括静态图像、视频流和多种数据格式。下表还标注了每个源是否可以使用 `stream=True` 参数以流式模式运行 ✅。流式模式对于处理视频或实时流非常有益，因为它会创建一个结果生成器，而不是将所有帧加载到内存中。

> 在处理长视频或大型数据集时，请使用 `stream=True` 以高效管理内存。当 `stream=False` 时，所有帧或数据点的结果都会存储在内存中，这可能会迅速堆积并导致大输入下的内存不足错误。相比之下，`stream=True` 利用生成器，仅将当前帧或数据点的结果保存在内存中，从而显著降低内存消耗并防止内存不足问题。

| 来源                                                  | 示例                                       | 类型            | 注意事项                                                     |
| :---------------------------------------------------- | :----------------------------------------- | :-------------- | :----------------------------------------------------------- |
| image                                                 | `'image.jpg'`                              | `str` 或 `Path` | 单张图像文件。                                               |
| URL                                                   | `'https://ultralytics.com/images/bus.jpg'` | `str`           | 图像的 URL 地址。                                            |
| screenshot                                            | `'screen'`                                 | `str`           | 截取屏幕画面。                                               |
| PIL                                                   | `Image.open('image.jpg')`                  | `PIL.Image`     | 带 RGB 通道的 HWC 格式。                                     |
| [OpenCV](https://www.ultralytics.com/glossary/opencv) | `cv2.imread('image.jpg')`                  | `np.ndarray`    | 带 BGR 通道的 HWC 格式 `uint8 (0-255)`。                     |
| NumPy                                                 | `np.zeros((640,1280,3))`                   | `np.ndarray`    | 带 BGR 通道的 HWC 格式 `uint8 (0-255)`。                     |
| torch                                                 | `torch.zeros(16,3,320,640)`                | `torch.Tensor`  | 带 RGB 通道的 BCHW 格式 `float32 (0.0-1.0)`。                |
| CSV                                                   | `'sources.csv'`                            | `str` 或 `Path` | 包含图像、视频或目录路径的 CSV 文件。                        |
| video ✅                                               | `'video.mp4'`                              | `str` 或 `Path` | MP4、AVI 等格式的视频文件。                                  |
| directory ✅                                           | `'path/'`                                  | `str` 或 `Path` | 包含图像或视频的目录路径。                                   |
| glob ✅                                                | `'path/*.jpg'`                             | `str`           | 用于匹配多个文件的 Glob 模式。使用 `*` 字符作为通配符。      |
| YouTube ✅                                             | `'https://youtu.be/LNwODJXcvt4'`           | `str`           | YouTube 视频的 URL。                                         |
| stream ✅                                              | `'rtsp://example.com/media.mp4'`           | `str`           | 用于 RTSP、RTMP、TCP 等流媒体协议的 URL 或 IP 地址。         |
| multi-stream ✅                                        | `'list.streams'`                           | `str` 或 `Path` | `*.streams` 文本文件，每行一个流 URL，例如 8 个流将以 8 的批处理大小运行。 |
| webcam ✅                                              | `0`                                        | `int`           | 已连接摄像头设备的索引，用于运行推理。                       |

以下是使用每种来源类型的代码示例：

图像

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Define path to the image file
source = "path/to/image.jpg"

# Run inference on the source
results = model(source)  # list of Results objects
```

截图

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Define current screenshot as source
source = "screen"

# Run inference on the source
results = model(source)  # list of Results objects
```
URL

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Define remote image or video URL
source = "https://ultralytics.com/images/bus.jpg"

# Run inference on the source
results = model(source)  # list of Results objects
```

PIL

```python
from PIL import Image

from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Open an image using PIL
source = Image.open("path/to/image.jpg")

# Run inference on the source
results = model(source)  # list of Results objects
```

OpenCV

```python
import cv2

from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Read an image using OpenCV
source = cv2.imread("path/to/image.jpg")

# Run inference on the source
results = model(source)  # list of Results objects
```

numpy

```python
import numpy as np

from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Create a random numpy array of HWC shape (640, 640, 3) with values in range [0, 255] and type uint8
source = np.random.randint(low=0, high=255, size=(640, 640, 3), dtype="uint8")

# Run inference on the source
results = model(source)  # list of Results objects
```

torch

```python
import torch

from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Create a random torch tensor of BCHW shape (1, 3, 640, 640) with values in range [0, 1] and type float32
source = torch.rand(1, 3, 640, 640, dtype=torch.float32)

# Run inference on the source
results = model(source)  # list of Results objects
```

CSV

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Define a path to a CSV file with images, URLs, videos and directories
source = "path/to/file.csv"

# Run inference on the source
results = model(source)  # list of Results objects
```

视频

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Define path to video file
source = "path/to/video.mp4"

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

目录

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Define path to directory containing images and videos for inference
source = "path/to/dir"

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

Glob

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

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

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Define source as YouTube video URL
source = "https://youtu.be/LNwODJXcvt4"

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

流

> 使用流模式通过 RTSP、RTMP、TCP 或 IP 地址协议对实时视频流运行推理。如果提供单个流，模型将以 1 的[批处理大小](https://www.ultralytics.com/glossary/batch-size)运行推理。对于多个流，可以使用 `.streams` 文本文件来执行批处理推理，其中批处理大小由提供的流数量决定（例如，8 个流的批处理大小为 8）。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Single stream with batch-size 1 inference
source = "rtsp://example.com/media.mp4"  # RTSP, RTMP, TCP, or IP streaming address

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects
```

多流

> 若要同时处理多个视频流，请使用一个 `.streams` 文本文件，并在其中按行写入每个源。模型将运行批处理推理，其中批大小等于流的数量。此设置可实现多个数据源的并发高效处理。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

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

> 文件中的每一行代表一个流媒体源，让你能够同时监控并对多个视频流执行推理。

网络摄像头

> 你可以通过将特定摄像头设备的索引传递给 `source`，来对该连接的摄像头运行推理。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Run inference on the source
results = model(source=0, stream=True)  # generator of Results objects
```


## 推理参数

`model.predict()` 接受多个参数，这些参数可以在推理时传入以覆盖默认设置：

### 固定尺寸 vs 最小矩形 (`rect`)

默认情况下，predict 使用 **`rect=True`**，这会在可能的情况下启用 **最小矩形** 填充。图像被缩放以适合 `imgsz`，并仅填充到最近的步幅倍数，因此最终张量可能比 `imgsz` **小**。最小矩形填充仅在 **批次中所有图像具有相同形状** 且后端支持（PyTorch `.pt` 或动态 ONNX / Triton）时使用。否则，图像将被填充到 **完整** 的 `imgsz` 目标尺寸。

使用 **`rect=False`** 可始终填充到完整的 `imgsz` 目标。当你需要固定的输入尺寸以匹配导出的模型（ONNX、TensorRT 等）时，建议使用此项。

**整数与元组 `imgsz`**

- **整数** `imgsz=640` 在步幅取整后会成为正方形目标 `(640, 640)`。
- **元组** `imgsz=(384, 672)` 会设置一个矩形目标。在使用 `rect=True` 和 `auto=True` 时，实际张量可能比此目标更小。

**训练 vs 预测/导出**

训练仅接受单个整数 `imgsz`（`[h, w]` 列表会被强制转换为最大值）。Predict 和 export 接受整数或 `(height, width)` 元组。

> python

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Run inference on 'bus.jpg' with arguments
model.predict("https://ultralytics.com/images/bus.jpg", save=True, imgsz=320, conf=0.25)
```

> CLI

```SH
# Run inference on 'bus.jpg'
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'
```

推理参数：

| 参数            | 类型                     | 默认值  | 描述                                                         |
| :-------------- | :----------------------- | :------ | :----------------------------------------------------------- |
| `source`        | `str` 或 `int` 或 `None` | `None`  | 指定推理的数据源。可以是图像路径、视频文件、目录、URL 或实时流的设备 ID。如果省略，将记录警告，模型将回退到内置的演示资源（`ultralytics/assets`，或用于 OBB 的演示 URL）。支持多种格式和来源，能够在 [不同类型的输入](https://docs.ultralytics.com/modes/predict#inference-sources) 间灵活应用。 |
| `conf`          | `float`                  | `0.25`  | 设置检测的最低置信度阈值。置信度低于此阈值的检测对象将被忽略。调整此值有助于减少误报。 |
| `iou`           | `float`                  | `0.7`   | [Intersection Over Union](https://www.ultralytics.com/glossary/intersection-over-union-iou) (IoU) 非极大值抑制 (NMS) 阈值。较低的值通过消除重叠框来减少检测数量，有助于减少重复项。 |
| `imgsz`         | `int` 或 `tuple`         | `640`   | Letterbox 目标。整数给出方形 `N×N`；元组给出 `(height, width)`。设置 `rect=True` 时，由于最小矩形填充，实际张量可能小于此目标。使用 `rect=False` 可获得固定大小。请参阅 [Fixed shape vs minimum rectangle](https://docs.ultralytics.com/modes/predict#fixed-shape-vs-minimum-rectangle-rect)。 |
| `rect`          | `bool`                   | `True`  | 如果为 `True`，则在可能时使用最小矩形填充（相同形状的批次和支持的后端）。如果为 `False`，则始终填充至完整的 `imgsz`。请参阅 [Fixed shape vs minimum rectangle](https://docs.ultralytics.com/modes/predict#fixed-shape-vs-minimum-rectangle-rect)。 |
| `quantize`      | `int` 或 `str`           | `None`  | 推理精度：`16`/`"fp16"` 可在支持的 GPU 上启用 FP16 推理；`32`/`"fp32"`/未设置则为 FP32。INT8/PTQ 量化在 [export](https://docs.ultralytics.com/zh/modes/export#quantization-options) 期间进行配置，并在加载导出模型时使用。取代了已弃用的 `half` 标志。 |
| `device`        | `str`                    | `None`  | 指定推理设备（例如 `cpu`、`cuda:0`、`0`、`npu` 或 `npu:0`）。允许你选择在 CPU、特定 GPU、华为昇腾 NPU 或其他计算设备上执行模型。 |
| `batch`         | `int`                    | `1`     | 指定推理的批次大小（仅在源为 [目录、视频文件或 `.txt` 文件](https://docs.ultralytics.com/modes/predict#inference-sources) 时有效）。较大的批次大小可以提供更高的吞吐量，缩短推理所需的总时间。 |
| `max_det`       | `int`                    | `300`   | 每张图像允许的最大检测数。限制模型在单次推理中可检测的对象总数，防止在密集场景中输出过多结果。 |
| `vid_stride`    | `int`                    | `1`     | 视频输入的帧步长。允许跳过视频中的帧以加快处理速度，代价是牺牲时间分辨率。值为 1 处理每一帧，更高的值会跳过帧。 |
| `stream_buffer` | `bool`                   | `False` | 确定是否为视频流排队传入的帧。如果为 `False`，则丢弃旧帧以适应新帧（针对实时应用程序进行优化）。如果为 `True`，则将新帧排入缓冲区，确保不跳过任何帧，但如果推理 FPS 低于流 FPS，则会导致延迟。 |
| `visualize`     | `bool`                   | `False` | 在推理期间激活模型特征可视化，深入了解模型正在“看到”什么。这对于调试和模型解释非常有用。 |
| `augment`       | `bool`                   | `False` | 启用测试时增强 (TTA) 进行预测，可能会提高检测的稳健性，但会以牺牲推理速度为代价。 |
| `agnostic_nms`  | `bool`                   | `False` | 启用类别无关的非极大值抑制 (NMS)，它会合并不同类别的重叠框。在类别重叠常见的多类检测场景中非常有用。对于端到端模型（YOLO26、YOLOv10），这仅防止相同的检测以多个类别标签出现（IoU=1.0 重复），并且不会在不同框之间执行基于 IoU 阈值的抑制。 |
| `classes`       | `list[int]`              | `None`  | 将预测过滤为一组类别 ID。仅返回属于指定类别的检测结果。在多类检测任务中专注于相关对象非常有用。 |
| `retina_masks`  | `bool`                   | `False` | 返回高分辨率分割掩码。如果启用，返回的掩码 (`masks.data`) 将匹配原始图像大小。如果禁用，它们将具有推理期间使用的图像大小。 |
| `embed`         | `list[int]`              | `None`  | 指定用于提取特征向量或 [embeddings](https://www.ultralytics.com/glossary/embeddings) 的层。使用 `model.embed(source)` 获取倒数第二层的嵌入，或使用 `model.predict(source, embed=[layer])` 来选择特定层。这对于聚类或相似度搜索等下游任务非常有用。 |
| `project`       | `str`                    | `None`  | 如果启用了 `save`，预测输出将保存到的项目目录名称。          |
| `name`          | `str`                    | `None`  | 预测运行名称。用于在项目文件夹内创建一个子目录，如果启用了 `save`，预测输出将存储在该子目录中。 |
| `stream`        | `bool`                   | `False` | 通过返回 Results 对象的生成器而不是一次将所有帧加载到内存中，为长视频或大量图像启用内存高效处理。 |
| `verbose`       | `bool`                   | `True`  | 控制是否在终端中显示详细的推理日志，提供关于预测过程的实时反馈。 |
| `compile`       | `bool` 或 `str`          | `False` | 启用 PyTorch 2.x 的 `torch.compile` 图编译，后台使用 `backend='inductor'`。接受 `True` -> `"default"`，`False` -> 禁用，或字符串模式如 `"default"`、`"reduce-overhead"`、`"max-autotune-no-cudagraphs"`。如果不支持，将回退到 eager 模式并发出警告。 |
| `channels_last` | `bool`                   | `False` | 在推理期间为卷积使用 channels_last (NHWC) 内存格式，以此加速 CUDA Tensor Core GPU，且不改变结果。仅适用于原生 PyTorch 模型；对于 CPU、MPS 以及 TensorRT 和 ONNX 等导出格式将被忽略。 |
| `end2end`       | `bool`                   | `None`  | 覆盖支持免 NMS 推理的 YOLO 模型（YOLO26、YOLOv10）中的端到端模式。将其设置为 `False`，你可以使用传统的 NMS 管道运行预测，此外还可以利用 `iou` 参数。有关详细信息，请参阅 [End-to-End Detection guide](https://docs.ultralytics.com/zh/guides/end2end-detection)。 |

可视化参数：

| 参数          | 类型          | 默认值          | 描述                                                         |
| :------------ | :------------ | :-------------- | :----------------------------------------------------------- |
| `show`        | `bool`        | `False`         | 如果为 `True`，则在窗口中显示标注后的图像或视频。这对于开发或测试过程中的即时视觉反馈非常有用。 |
| `save`        | `bool`        | `False or True` | 启用将带注释的图像或视频保存到文件。对于文档记录、进一步分析或分享结果非常有用。使用 CLI 时默认为 True，在 Python 中使用时默认为 False。 |
| `save_frames` | `bool`        | `False`         | 处理视频时，将单个帧保存为图像。对于提取特定帧或进行详细的逐帧分析非常有用。 |
| `save_txt`    | `bool`        | `False`         | 以 `[class] [x_center] [y_center] [width] [height] [confidence]` 格式将检测结果保存在文本文件中。对于与其他分析工具集成非常有用。 |
| `save_conf`   | `bool`        | `False`         | 在保存的文本文件中包含置信度分数。增强了可用于后续处理和分析的详细信息。 |
| `save_crop`   | `bool`        | `False`         | 保存检测对象的裁剪图像。对于数据集增强、分析或创建针对特定对象的聚焦数据集非常有用。 |
| `show_labels` | `bool`        | `True`          | 在视觉输出中显示每次检测的标签。提供对检测到对象的即时理解。 |
| `show_conf`   | `bool`        | `True`          | 在标签旁显示每次检测的置信度得分。让你深入了解模型对每次检测的确定性。 |
| `show_boxes`  | `bool`        | `True`          | 在检测到的对象周围绘制边界框。对于图像或视频帧中对象的视觉识别和定位至关重要。 |
| `line_width`  | `int or None` | `None`          | 指定边界框的线条宽度。如果为 `None`，则线条宽度会根据图像尺寸自动调整。提供用于清晰度的视觉自定义功能。 |

## 图像和视频格式

YOLO26 支持多种图像和视频格式，具体见 [ultralytics/data/utils.py](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/data/utils.py)。请参阅下表了解有效的后缀和预测命令示例。

### 图像

下表包含有效的 Ultralytics 图像格式。

> HEIC/HEIF 格式需要 `pi-heif`，它会在首次使用时自动安装。AVIF 由 Pillow 原生支持。

| 图像后缀 | 预测命令示例                     | 参考                                                         |
| :------- | :------------------------------- | :----------------------------------------------------------- |
| `.avif`  | `yolo predict source=image.avif` | [AV1 图像文件格式](https://en.wikipedia.org/wiki/AVIF)       |
| `.bmp`   | `yolo predict source=image.bmp`  | [微软 BMP 文件格式](https://en.wikipedia.org/wiki/BMP_file_format) |
| `.dng`   | `yolo predict source=image.dng`  | [Adobe DNG](https://en.wikipedia.org/wiki/Digital_Negative)  |
| `.heic`  | `yolo predict source=image.heic` | [高效图像格式](https://en.wikipedia.org/wiki/HEIF)           |
| `.heif`  | `yolo predict source=image.heif` | [高效图像格式](https://en.wikipedia.org/wiki/HEIF)           |
| `.jp2`   | `yolo predict source=image.jp2`  | [JPEG 2000](https://en.wikipedia.org/wiki/JPEG_2000)         |
| `.jpeg`  | `yolo predict source=image.jpeg` | [JPEG](https://en.wikipedia.org/wiki/JPEG)                   |
| `.jpg`   | `yolo predict source=image.jpg`  | [JPEG](https://en.wikipedia.org/wiki/JPEG)                   |
| `.mpo`   | `yolo predict source=image.mpo`  | [多重图像对象](https://fileinfo.com/extension/mpo)           |
| `.png`   | `yolo predict source=image.png`  | [可移植网络图形](https://en.wikipedia.org/wiki/PNG)          |
| `.tif`   | `yolo predict source=image.tif`  | [标签图像文件格式](https://en.wikipedia.org/wiki/TIFF)       |
| `.tiff`  | `yolo predict source=image.tiff` | [标签图像文件格式](https://en.wikipedia.org/wiki/TIFF)       |
| `.webp`  | `yolo predict source=image.webp` | [WebP](https://en.wikipedia.org/wiki/WebP)                   |

### 视频

下表包含有效的 Ultralytics 视频格式。

| 视频后缀 | 预测命令示例                     | 参考                                                         |
| :------- | :------------------------------- | :----------------------------------------------------------- |
| `.asf`   | `yolo predict source=video.asf`  | [高级系统格式](https://en.wikipedia.org/wiki/Advanced_Systems_Format) |
| `.avi`   | `yolo predict source=video.avi`  | [音频视频交错格式](https://en.wikipedia.org/wiki/Audio_Video_Interleave) |
| `.gif`   | `yolo predict source=video.gif`  | [图形交换格式](https://en.wikipedia.org/wiki/GIF)            |
| `.m4v`   | `yolo predict source=video.m4v`  | [MPEG-4 第 14 部分](https://en.wikipedia.org/wiki/M4V)       |
| `.mkv`   | `yolo predict source=video.mkv`  | [Matroska](https://en.wikipedia.org/wiki/Matroska)           |
| `.mov`   | `yolo predict source=video.mov`  | [QuickTime 文件格式](https://en.wikipedia.org/wiki/QuickTime_File_Format) |
| `.mp4`   | `yolo predict source=video.mp4`  | [MPEG-4 第 14 部分 - 维基百科](https://en.wikipedia.org/wiki/MPEG-4_Part_14) |
| `.mpeg`  | `yolo predict source=video.mpeg` | [MPEG-1 第 2 部分](https://en.wikipedia.org/wiki/MPEG-1)     |
| `.mpg`   | `yolo predict source=video.mpg`  | [MPEG-1 第 2 部分](https://en.wikipedia.org/wiki/MPEG-1)     |
| `.ts`    | `yolo predict source=video.ts`   | [MPEG 传输流](https://en.wikipedia.org/wiki/MPEG_transport_stream) |
| `.wmv`   | `yolo predict source=video.wmv`  | [Windows 媒体视频](https://en.wikipedia.org/wiki/Windows_Media_Video) |
| `.webm`  | `yolo predict source=video.webm` | [WebM 项目](https://en.wikipedia.org/wiki/WebM)              |

## 处理结果

所有 Ultralytics `predict()` 调用都将返回一个 `Results` 对象列表：

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

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

| 属性            | 类型                     | 描述                                                   |
| :-------------- | :----------------------- | :----------------------------------------------------- |
| `orig_img`      | `np.ndarray`             | 作为 NumPy 数组的原始图像。                            |
| `orig_shape`    | `tuple`                  | 以 (高度, 宽度) 格式表示的原始图像形状。               |
| `boxes`         | `Boxes, optional`        | 包含检测边界框的 Boxes 对象。                          |
| `masks`         | `Masks, optional`        | 包含检测掩膜的 Masks 对象。                            |
| `probs`         | `Probs, optional`        | 包含分类任务中每个类别概率的 Probs 对象。              |
| `keypoints`     | `Keypoints, optional`    | 包含每个对象检测到的关键点的 Keypoints 对象。          |
| `obb`           | `OBB, optional`          | 包含旋转边界框的 OBB 对象。                            |
| `semantic_mask` | `SemanticMask, optional` | 包含密集逐像素类地图的 SemanticMask 对象。             |
| `speed`         | `dict`                   | 预处理、推理和后处理速度的字典，单位为每张图像毫秒数。 |
| `names`         | `dict`                   | 将类别索引映射到类别名称的字典。                       |
| `path`          | `str`                    | 图像文件的路径。                                       |
| `save_dir`      | `str, optional`          | 保存结果的目录。                                       |

### 各任务的结果

下方填充哪些字段取决于你的模型任务 — 如果你还没选定任务，请[比较检测、分割、分类、姿态、OBB、语义分割和深度估计](https://docs.ultralytics.com/zh/tasks)。每次预测都会为每张图像或每帧返回一个 `Results` 对象。上述通用字段始终可用，而特定于任务的预测数据则存储在下方的字段中。坐标、置信度和概率张量默认为 `torch.float32`，除非使用了半精度，此时为 `torch.float16`。执行 `result.numpy()` 后，张量将变为匹配 NumPy 数据类型的 NumPy 数组。实例掩码是 `torch.uint8` 二进制张量，而语义掩码则会根据类别数量使用最小的实用整数数据类型：`torch.uint8`、`torch.int16` 或 `torch.int32`。

> 检测

| 属性                | 类型            | 形状      | 描述                                               |
| :------------------ | :-------------- | :-------- | :------------------------------------------------- |
| `result.boxes`      | `Boxes`         | `(N)`     | 检测框。                                           |
| `result.boxes.data` | `torch.float32` | `(N,6/7)` | 原始 `[x1,y1,x2,y2,conf,cls]`，外加可选的追踪 ID。 |
| `result.boxes.xyxy` | `torch.float32` | `(N,4)`   | `xyxy` 像素框。                                    |
| `result.boxes.conf` | `torch.float32` | `(N,)`    | 置信度得分。                                       |
| `result.boxes.cls`  | `torch.float32` | `(N,)`    | 类别 ID；转换为 `int` 即可获取名称。               |

> 分割

| 属性                | 类型          | 形状          | 描述                          |
| :------------------ | :------------ | :------------ | :---------------------------- |
| `result.boxes`      | `Boxes`       | `(N)`         | 实例框/类别/置信度。          |
| `result.masks`      | `Masks`       | `(N)`         | 实例掩膜。                    |
| `result.masks.data` | `torch.uint8` | `(N,H,W)`     | 二进制掩膜，值为 `0` 或 `1`。 |
| `result.masks.xy`   | `np.float32`  | `list[(P,2)]` | 像素多边形。                  |
| `result.masks.xyn`  | `np.float32`  | `list[(P,2)]` | 归一化多边形。                |

> 语义

| 属性                        | 类型                                      | 形状    | 描述                                    |
| :-------------------------- | :---------------------------------------- | :------ | :-------------------------------------- |
| `result.semantic_mask`      | `SemanticMask`                            | `(H,W)` | 密集类地图。                            |
| `result.semantic_mask.data` | `torch.uint8` `torch.int16` `torch.int32` | `(H,W)` | 逐像素类 ID，数据类型根据类别数量选择。 |
| `result.masks`              | -                                         | -       | 无实例掩膜。                            |
| `result.boxes`              | -                                         | -       | 无实例框/置信度。                       |

> 分类

| 属性                    | 类型            | 形状    | 描述             |
| :---------------------- | :-------------- | :------ | :--------------- |
| `result.probs`          | `Probs`         | `(C,)`  | 类别概率。       |
| `result.probs.data`     | `torch.float32` | `(C,)`  | 每个类别的概率。 |
| `result.probs.top1`     | `int`           | `()`    | 首选类别 ID。    |
| `result.probs.top1conf` | `torch.float32` | `()`    | 首选置信度。     |
| `result.probs.top5`     | `list[int]`     | `(<=5)` | 前 5 个类别 ID。 |

> 姿态

| 属性                    | 类型            | 形状        | 描述                            |
| :---------------------- | :-------------- | :---------- | :------------------------------ |
| `result.boxes`          | `Boxes`         | `(N)`       | 实例框。                        |
| `result.keypoints`      | `Keypoints`     | `(N)`       | 关键点。                        |
| `result.keypoints.data` | `torch.float32` | `(N,K,2/3)` | `x,y` 外加可选的可见性/置信度。 |
| `result.keypoints.xy`   | `torch.float32` | `(N,K,2)`   | 像素关键点。                    |
| `result.keypoints.xyn`  | `torch.float32` | `(N,K,2)`   | 归一化关键点。                  |

> OBB

| 属性                  | 类型            | 形状      | 描述                          |
| :-------------------- | :-------------- | :-------- | :---------------------------- |
| `result.obb`          | `OBB`           | `(N)`     | 旋转边界框。                  |
| `result.obb.data`     | `torch.float32` | `(N,7/8)` | 包含置信度/类别的原始旋转框。 |
| `result.obb.xywhr`    | `torch.float32` | `(N,5)`   | `xywhr` 旋转框。              |
| `result.obb.xyxyxyxy` | `torch.float32` | `(N,4,2)` | 四个角点。                    |
| `result.obb.conf`     | `torch.float32` | `(N,)`    | 置信度得分。                  |

`Results` 对象具有以下方法：

| 方法          | 返回类型               | 描述                                                         |
| :------------ | :--------------------- | :----------------------------------------------------------- |
| `update()`    | `None`                 | 使用框、掩码、概率、obb、关键点或语义掩码等新数据更新 Results 对象。 |
| `cpu()`       | `Results`              | 返回一个将所有张量移至 CPU 内存的 Results 对象副本。         |
| `numpy()`     | `Results`              | 返回一个将所有张量转换为 NumPy 数组的 Results 对象副本。     |
| `cuda()`      | `Results`              | 返回一个将所有张量移至 GPU 内存的 Results 对象副本。         |
| `to()`        | `Results`              | 返回一个将张量移至指定设备和数据类型的 Results 对象副本。    |
| `new()`       | `Results`              | 创建一个具有相同图像、路径、名称和速度属性的新 Results 对象。 |
| `plot()`      | `np.ndarray`           | 在输入 BGR 图像上绘制检测结果并返回带标注的图像。            |
| `show()`      | `None`                 | 显示带有标注推理结果的图像。                                 |
| `save()`      | `str`                  | 将带标注的推理结果图像保存到文件并返回文件名。               |
| `verbose()`   | `str`                  | 返回每个任务的日志字符串，详述检测和分类结果。               |
| `save_txt()`  | `str`                  | 将检测结果保存到文本文件并返回保存文件的路径。               |
| `save_crop()` | `None`                 | 将裁剪后的检测图像保存到指定目录。                           |
| `summary()`   | `List[Dict[str, Any]]` | 将推理结果转换为带有可选归一化的摘要字典。                   |
| `to_df()`     | `DataFrame`            | 将检测结果转换为 Polars DataFrame。                          |
| `to_csv()`    | `str`                  | 将检测结果转换为 CSV 格式。                                  |
| `to_json()`   | `str`                  | 将检测结果转换为 JSON 格式。                                 |

有关更多详细信息，请参阅 [`Results` 类文档](https://docs.ultralytics.com/reference/engine/results)。

### 框

`Boxes` 对象可用于索引、操作和将边界框转换为不同格式。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.boxes)  # print the Boxes object containing the detection bounding boxes
```

这是 `Boxes` 类方法和属性表，包括它们的名称、类型和描述：

| 名称      | 类型                  | 描述                                         |
| :-------- | :-------------------- | :------------------------------------------- |
| `cpu()`   | 方法                  | 将对象移动到 CPU 内存。                      |
| `numpy()` | 方法                  | 将对象转换为 NumPy 数组。                    |
| `cuda()`  | 方法                  | 将对象移动到 CUDA 内存。                     |
| `to()`    | 方法                  | 将对象移动到指定设备。                       |
| `xyxy`    | 属性 (`torch.Tensor`) | 以 xyxy 格式返回边界框。                     |
| `conf`    | 属性 (`torch.Tensor`) | 返回边界框的置信度值。                       |
| `cls`     | 属性 (`torch.Tensor`) | 返回边界框的类别值。                         |
| `id`      | 属性 (`torch.Tensor`) | 返回边界框的跟踪 ID（如果可用）。            |
| `xywh`    | 属性 (`torch.Tensor`) | 以 xywh 格式返回边界框。                     |
| `xyxyn`   | 属性 (`torch.Tensor`) | 以原始图像大小归一化的 xyxy 格式返回边界框。 |
| `xywhn`   | 属性 (`torch.Tensor`) | 以原始图像大小归一化的 xywh 格式返回边界框。 |

有关更多详细信息，请参阅 [`Boxes` 类文档](https://docs.ultralytics.com/reference/engine/results#ultralytics.engine.results.Boxes)。

### 掩码

`Masks` 对象可用于索引、操作并将掩码转换为分割区域。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n-seg Segment model
model = YOLO("yolo26n-seg.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.masks)  # print the Masks object containing the detected instance masks
```

这是 `Masks` 类方法和属性表，包括它们的名称、类型和描述：

| 名称      | 类型                      | 描述                                                         |
| :-------- | :------------------------ | :----------------------------------------------------------- |
| `data`    | 属性 (`torch.Tensor`)     | `torch.uint8` 二进制掩码张量，形状为 `(N,H,W)`，数值为 `0` 或 `1`。 |
| `cpu()`   | 方法                      | 在 CPU 内存上返回掩码张量。                                  |
| `numpy()` | 方法                      | 以 NumPy 数组形式返回掩码张量。                              |
| `cuda()`  | 方法                      | 在 GPU 内存上返回掩码张量。                                  |
| `to()`    | 方法                      | 以指定设备和数据类型返回掩码张量。                           |
| `xyn`     | 属性 (`list[np.ndarray]`) | 归一化掩码多边形列表。                                       |
| `xy`      | 属性 (`list[np.ndarray]`) | 像素坐标下的掩码多边形列表。                                 |

有关更多详细信息，请参阅 [`Masks` 类文档](https://docs.ultralytics.com/reference/engine/results#ultralytics.engine.results.Masks)。

### 语义掩码

`SemanticMask` 为语义分割结果存储一张密集类映射图。与 `Masks` 不同，它不为每个对象包含一个二进制掩码，也不提供多边形辅助工具。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n-sem Semantic model
model = YOLO("yolo26n-sem.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.semantic_mask.data)  # print the H x W class-ID map
```

| 名称      | 类型                  | 描述                                                         |
| :-------- | :-------------------- | :----------------------------------------------------------- |
| `data`    | 属性 (`torch.Tensor`) | 形状为 `(H,W)` 的类 ID 映射图。数据类型为 `torch.uint8`、`torch.int16` 或 `torch.int32`，具体取决于类别数量。 |
| `shape`   | 属性 (`tuple`)        | 类映射图的形状，通常与 `result.orig_shape` 匹配。            |
| `cpu()`   | 方法                  | 在 CPU 内存上返回语义掩码张量。                              |
| `numpy()` | 方法                  | 以 NumPy 数组形式返回语义掩码张量。                          |
| `cuda()`  | 方法                  | 在 GPU 内存上返回语义掩码张量。                              |
| `to()`    | 方法                  | 以指定设备和数据类型返回语义掩码张量。                       |

### 关键点

`Keypoints` 对象可用于索引、操作和归一化坐标。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n-pose Pose model
model = YOLO("yolo26n-pose.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.keypoints)  # print the Keypoints object containing the detected keypoints
```

这是 `Keypoints` 类方法和属性表，包括它们的名称、类型和描述：

| 名称      | 类型                  | 描述                                            |
| :-------- | :-------------------- | :---------------------------------------------- |
| `cpu()`   | 方法                  | 在 CPU 内存上返回关键点张量。                   |
| `numpy()` | 方法                  | 以 NumPy 数组形式返回关键点张量。               |
| `cuda()`  | 方法                  | 在 GPU 内存上返回关键点张量。                   |
| `to()`    | 方法                  | 返回具有指定设备和数据类型的关键点张量。        |
| `xyn`     | 属性 (`torch.Tensor`) | 以张量表示的归一化关键点列表。                  |
| `xy`      | 属性 (`torch.Tensor`) | 以张量表示的像素坐标关键点列表。                |
| `conf`    | 属性 (`torch.Tensor`) | 返回关键点的置信度值（若可用），否则返回 None。 |

有关更多详情，请参阅 [`Keypoints` 类文档](https://docs.ultralytics.com/reference/engine/results#ultralytics.engine.results.Keypoints)。

### Probs

`Probs` 对象可用于获取 `top1` 和 `top5` 分类索引及得分。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n-cls Classify model
model = YOLO("yolo26n-cls.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/bus.jpg")  # results list

# View results
for r in results:
    print(r.probs)  # print the Probs object containing the detected class probabilities
```

下表总结了 `Probs` 类的方法和属性：

| 名称       | 类型                  | 描述                                          |
| :--------- | :-------------------- | :-------------------------------------------- |
| `cpu()`    | 方法                  | 返回 CPU 内存中 probs 张量的副本。            |
| `numpy()`  | 方法                  | 返回作为 NumPy 数组的 probs 张量副本。        |
| `cuda()`   | 方法                  | 返回 GPU 内存中 probs 张量的副本。            |
| `to()`     | 方法                  | 返回具有指定设备和数据类型的 probs 张量副本。 |
| `top1`     | 属性 (`int`)          | Top 1 类别的索引。                            |
| `top5`     | 属性 (`list[int]`)    | Top 5 类别的索引。                            |
| `top1conf` | 属性 (`torch.Tensor`) | Top 1 类别的置信度。                          |
| `top5conf` | 属性 (`torch.Tensor`) | Top 5 类别的置信度。                          |

有关更多详情，请参阅 [`Probs` 类文档](https://docs.ultralytics.com/reference/engine/results#ultralytics.engine.results.Probs)。

### OBB

`OBB` 对象可用于索引、操作并将旋转边界框转换为不同格式。

```python
from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n-obb.pt")

# Run inference on an image
results = model("https://ultralytics.com/images/boats.jpg")  # results list

# View results
for r in results:
    print(r.obb)  # print the OBB object containing the oriented detection bounding boxes
```

下表列出了 `OBB` 类的方法和属性，包括它们的名称、类型和描述：

| 名称        | 类型                  | 描述                                         |
| :---------- | :-------------------- | :------------------------------------------- |
| `cpu()`     | 方法                  | 将对象移动到 CPU 内存。                      |
| `numpy()`   | 方法                  | 将对象转换为 NumPy 数组。                    |
| `cuda()`    | 方法                  | 将对象移动到 CUDA 内存。                     |
| `to()`      | 方法                  | 将对象移动到指定设备。                       |
| `conf`      | 属性 (`torch.Tensor`) | 返回边界框的置信度值。                       |
| `cls`       | 属性 (`torch.Tensor`) | 返回边界框的类别值。                         |
| `id`        | 属性 (`torch.Tensor`) | 返回边界框的跟踪 ID（如果可用）。            |
| `xyxy`      | 属性 (`torch.Tensor`) | 以 xyxy 格式返回水平框。                     |
| `xywhr`     | 属性 (`torch.Tensor`) | 以 xywhr 格式返回旋转框。                    |
| `xyxyxyxy`  | 属性 (`torch.Tensor`) | 以 xyxyxyxy 格式返回旋转框。                 |
| `xyxyxyxyn` | 属性 (`torch.Tensor`) | 以图像尺寸归一化的 xyxyxyxy 格式返回旋转框。 |

有关更多详情，请参阅 [`OBB` 类文档](https://docs.ultralytics.com/reference/engine/results#ultralytics.engine.results.OBB)。

## 结果绘图

字段 `plot()` 方法在 `Results` 对象通过将检测到的对象（例如边界框、掩码、关键点和概率）叠加到原始图像上，从而方便预测的可视化。此方法将带注释的图像作为 NumPy 数组返回，从而可以轻松显示或保存。

```python
from PIL import Image

from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("yolo26n.pt")

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

`plot()` 方法支持各种参数以自定义输出：

| 参数         | 类型                        | 描述                                                      | 默认值            |
| :----------- | :-------------------------- | :-------------------------------------------------------- | :---------------- |
| `conf`       | `bool`                      | 包含检测置信度分数。                                      | `True`            |
| `line_width` | `float`                     | 边界框的线宽。如果为 `None`，则随图像大小缩放。           | `None`            |
| `font_size`  | `float`                     | 文本字体大小。如果为 `None`，则随图像大小缩放。           | `None`            |
| `font`       | `str`                       | 文本标注的字体名称。                                      | `'Arial.ttf'`     |
| `pil`        | `bool`                      | 以 PIL Image 对象形式返回图像。                           | `False`           |
| `img`        | `np.ndarray | torch.Tensor` | 替代图像。张量必须是连续的 HWC BGR uint8。                | `None`            |
| `kpt_radius` | `int`                       | 绘制关键点的半径。                                        | `5`               |
| `kpt_line`   | `bool`                      | 用线条连接关键点。                                        | `True`            |
| `labels`     | `bool`                      | 在标注中包含类标签。                                      | `True`            |
| `boxes`      | `bool`                      | 在图像上叠加边界框。                                      | `True`            |
| `masks`      | `bool`                      | 在图像上叠加掩码。                                        | `True`            |
| `probs`      | `bool`                      | 包含分类概率。                                            | `True`            |
| `show`       | `bool`                      | 使用默认图像查看器直接显示标注后的图像。                  | `False`           |
| `save`       | `bool`                      | 将标注后的图像保存到 `filename` 指定的文件中。            | `False`           |
| `filename`   | `str`                       | 如果 `save` 为 `True`，则为保存标注图像的文件路径和名称。 | `None`            |
| `color_mode` | `str`                       | 指定颜色模式，例如 'instance' 或 'class'。                | `'class'`         |
| `txt_color`  | `tuple[int, int, int]`      | 用于边界框和图像分类标签的 BGR 文本颜色。                 | `(255, 255, 255)` |

## 线程安全推理

当你在不同线程中并行运行多个 YOLO 模型时，确保推理过程中的线程安全至关重要。线程安全推理保证了每个线程的预测是隔离的，且互不干扰，从而避免竞态条件并确保输出的一致性和可靠性。

在多线程应用程序中使用 YOLO 模型时，务必为每个线程实例化单独的模型对象，或采用线程本地存储以防止冲突：

```python
from threading import Thread

from ultralytics import YOLO

def thread_safe_predict(model, image_path):
    """Performs thread-safe prediction on an image using a locally instantiated YOLO model."""
    model = YOLO(model)
    results = model.predict(image_path)
    # Process results

# Starting threads that each have their own model instance
Thread(target=thread_safe_predict, args=("yolo26n.pt", "image1.jpg")).start()
Thread(target=thread_safe_predict, args=("yolo26n.pt", "image2.jpg")).start()
```

有关 YOLO 模型线程安全推理的深入了解及分步说明，请参阅我们的 [YOLO 线程安全推理指南](https://docs.ultralytics.com/zh/guides/yolo-thread-safe-inference)。本指南将为你提供避开常见陷阱并确保多线程推理平稳运行所需的所有必要信息。

## 流媒体源 `for`-循环

这是一个使用 OpenCV (`cv2`) 和 YOLO 对视频帧进行推理的 Python 脚本。该脚本假设你已经安装了必要的包（`opencv-python` 和 `ultralytics`）。

```python
import cv2

from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolo26n.pt")

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

> python

```python
from pathlib import Path
from ultralytics import YOLO, settings
from ultralytics.engine.results import Results


settings.update(
    {
        "tensorboard": True,
        "datasets_dir": "datasets",
        "weights_dir": "weights",
        "runs_dir": "runs",
    }
)


model_path = Path("weights/yolo26n.pt").resolve()
source = Path("datasets/coco/images/val2017/000000000139.jpg").resolve()
source = Path("datasets/coco/images/val2017/").resolve()
project = "coco"
name = "yolo26n/predict"

print(f"{model_path} is exists: {model_path.exists()}")
print(f"{source} is exists: {source.exists()}")


model = YOLO(model_path, task="detect")

results = model(
    source,
    conf=0.25,
    iou=0.7,
    imgsz=640,
    rect=True,
    device=0,
    batch=1,
    max_det=300,
    vid_stride=1,
    stream_buffer=False,
    visualize=False,
    augment=False,
    agnostic_nms=False,
    classes=None,  # list[int] | None, 将预测结果筛选到一组类别 ID。只会返回属于指定类别的检测结果。这对于专注于多类别检测任务中的相关对象非常有用。
    retina_masks=False,
    embed=None,
    project=project,
    name=name,
    stream=True,
    verbose=True,
    compile=False,
    end2end=None,
    # below are visualize parameters
    show=False,
    save=True,
    save_frames=False,
    save_txt=True,
    save_conf=False,
    save_crop=False,
    show_labels=True,
    show_conf=True,
    show_boxes=True,
    line_width=None,
)

result: Results
for result in results:
    result.orig_img
    result.orig_shape
    result.names
    boxes = result.boxes  # Boxes object for bounding box outputs
    boxes.id
    boxes.cls
    boxes.conf
    boxes.xyxy
    boxes.xyxyn
    boxes.xywh
    boxes.xywhn
    result.masks  # Masks object for segmentation masks outputs
    result.keypoints  # Keypoints object for pose outputs
    result.probs  # Probs object for classification outputs
    result.obb  # Oriented boxes object for OBB outputs
    result.path  # Path to the input image file.
    result.save_dir  # Directory to save results.
    # result.show()  # display to screen
    # result.save(filename="result.jpg")  # Save annotated inference results image to file.
    # result.save_txt(txt_file="result.txt", save_conf=False)  # Save detection results to a text file.
    # result.save_crop(save_dir="crops", file_name="im.jpg")  # Save cropped detection images to specified directory.
```

> CLI

```sh
yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.7 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo26n.pt source=ultralytics/assets/bus.jpg device=0 project=coco8 name=yolo26n/predict

yolo detect predict imgsz=640 save=True save_txt=True save_conf=True save_crop=True conf=0.25 iou=0.7 data=ultralytics/cfg/datasets/coco8.yaml model=weights/yolo26n.pt source=../datasets/coco8/images/train2017 device=0 project=coco8 name=yolo26n/predict
```

### yolo-world

> python

```python
# https://docs.ultralytics.com/zh/models/yolo-world/

from pathlib import Path
from ultralytics import YOLOWorld
from ultralytics.engine.results import Results


model_path = Path("weights/yolov8x-worldv2.pt").resolve()
source = Path("datasets/coco/images/val2017/000000000139.jpg").resolve()
source = Path("datasets/coco/images/val2017/").resolve()
project = "coco"
name = "yolo-world/yolov8x-worldv2/predict"

print(f"{model_path} is exists: {model_path.exists()}")
print(f"{source} is exists: {source.exists()}")


model = YOLOWorld(model_path)

# prompt based (optional)
# names = ["person", "car", "bus", "black cat", "white dog walking"]
# model.set_classes(names)

results = model(
    source,
    conf=0.25,
    iou=0.7,
    imgsz=640,
    rect=True,
    device=0,
    batch=1,
    max_det=300,
    vid_stride=1,
    stream_buffer=False,
    visualize=False,
    augment=False,
    agnostic_nms=False,
    classes=None,  # list[int] | None, 将预测结果筛选到一组类别 ID。只会返回属于指定类别的检测结果。这对于专注于多类别检测任务中的相关对象非常有用。
    retina_masks=False,
    embed=None,
    project=project,
    name=name,
    stream=True,
    verbose=True,
    compile=False,
    end2end=None,
    # below are visualize parameters
    show=False,
    save=True,
    save_frames=False,
    save_txt=True,
    save_conf=False,
    save_crop=False,
    show_labels=True,
    show_conf=True,
    show_boxes=True,
    line_width=None,
)

result: Results
for result in results:
    result.orig_img
    result.orig_shape
    result.names
    boxes = result.boxes  # Boxes object for bounding box outputs
    boxes.id
    boxes.cls
    boxes.conf
    boxes.xyxy
    boxes.xyxyn
    boxes.xywh
    boxes.xywhn
    result.masks  # Masks object for segmentation masks outputs
    result.keypoints  # Keypoints object for pose outputs
    result.probs  # Probs object for classification outputs
    result.obb  # Oriented boxes object for OBB outputs
    result.path  # Path to the input image file.
    result.save_dir  # Directory to save results.
    # result.show()  # display to screen
    # result.save(filename="result.jpg")  # Save annotated inference results image to file.
    # result.save_txt(txt_file="result.txt", save_conf=False)  # Save detection results to a text file.
    # result.save_crop(save_dir="crops", file_name="im.jpg")  # Save cropped detection images to specified directory.
```

### yoloe

> python

```python
# https://docs.ultralytics.com/zh/models/yoloe/

from pathlib import Path
from ultralytics import YOLOE
from ultralytics.engine.results import Results


use_prompt = False  # prompt based (optional)

if use_prompt:
    # 文本/视觉提示模型
    model_path = Path("weights/yoloe-26x-seg.pt").resolve()
    name = "yoloe/yoloe-26x-seg/predict"
else:
    # 无提示词模型
    model_path = Path("weights/yoloe-26x-seg-pf.pt").resolve()
    name = "yoloe/yoloe-26x-seg-pf/predict"
source = Path("datasets/coco/images/val2017/000000000139.jpg").resolve()
source = Path("datasets/coco/images/val2017/").resolve()
project = "coco"


print(f"{model_path} is exists: {model_path.exists()}")
print(f"{source} is exists: {source.exists()}")


model = YOLOE(model_path, task="segment")

# prompt based (optional)
if use_prompt:
    names = ["person", "car", "bus", "black cat", "white dog walking"]
    model.set_classes(names, model.get_text_pe(names))

results = model(
    source,
    conf=0.25,
    iou=0.7,
    imgsz=640,
    rect=True,
    device=0,
    batch=1,
    max_det=300,
    vid_stride=1,
    stream_buffer=False,
    visualize=False,
    augment=False,
    agnostic_nms=False,
    classes=None,  # list[int] | None, 将预测结果筛选到一组类别 ID。只会返回属于指定类别的检测结果。这对于专注于多类别检测任务中的相关对象非常有用。
    retina_masks=False,
    embed=None,
    project=project,
    name=name,
    stream=True,
    verbose=True,
    compile=False,
    end2end=None,
    # below are visualize parameters
    show=False,
    save=True,
    save_frames=False,
    save_txt=True,
    save_conf=False,
    save_crop=False,
    show_labels=True,
    show_conf=True,
    show_boxes=True,
    line_width=None,
)

result: Results
for result in results:
    result.orig_img
    result.orig_shape
    result.names
    boxes = result.boxes  # Boxes object for bounding box outputs
    boxes.id
    boxes.cls
    boxes.conf
    boxes.xyxy
    boxes.xyxyn
    boxes.xywh
    boxes.xywhn
    result.masks  # Masks object for segmentation masks outputs
    result.keypoints  # Keypoints object for pose outputs
    result.probs  # Probs object for classification outputs
    result.obb  # Oriented boxes object for OBB outputs
    result.path  # Path to the input image file.
    result.save_dir  # Directory to save results.
    # result.show()  # display to screen
    # result.save(filename="result.jpg")  # Save annotated inference results image to file.
    # result.save_txt(txt_file="result.txt", save_conf=False)  # Save detection results to a text file.
    # result.save_crop(save_dir="crops", file_name="im.jpg")  # Save cropped detection images to specified directory.
```

# [导出](https://docs.ultralytics.com/zh/modes/export/)

## 使用示例

将 YOLO26n 模型导出为其他格式（如 ONNX 或 TensorRT）。请参阅下方的“参数”部分以获取完整的导出参数列表。

> python

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # load an official model
model = YOLO("path/to/best.pt")  # load a custom-trained model

# Export the model
model.export(format="onnx")
```

> CLI

```sh
yolo export model=yolo26n.pt format=onnx      # export official model
yolo export model=path/to/best.pt format=onnx # export custom-trained model
```

## 参数

此表格详细说明了将 YOLO 模型导出为不同格式时可用的配置和选项。这些设置对于优化导出模型的性能、大小以及在各种平台和环境下的兼容性至关重要。正确的配置可确保模型能够以最佳效率准备好在预期的应用程序中进行部署。

| 参数        | 类型              | 默认值          | 描述                                                         |
| :---------- | :---------------- | :-------------- | :----------------------------------------------------------- |
| `format`    | `str`             | `'torchscript'` | 导出模型的目标格式，例如 `'onnx'`、`'torchscript'`、`'engine'` (TensorRT) 等。每种格式都能实现与不同 [部署环境](https://docs.ultralytics.com/modes/export) 的兼容性。 |
| `imgsz`     | `int` 或 `tuple`  | `640`           | 模型输入所需的图像尺寸。对于正方形图像，可以是一个整数（例如 `640` 表示 640×640），也可以是一个元组 `(height, width)` 以指定具体尺寸。 |
| `keras`     | `bool`            | `False`         | 启用导出为 [TensorFlow](https://www.ultralytics.com/glossary/tensorflow) SavedModel 的 Keras 格式，提供与 TensorFlow 服务和 API 的兼容性。 |
| `optimize`  | `bool`            | `False`         | 为 DEEPX 启用更高的编译器优化，在增加编译时间的同时减少推理延迟。 |
| `quantize`  | `int` 或 `str`    | `None`          | 量化精度：`16`（FP16，可减小模型大小并提升在支持硬件上的推理速度）或 `8`（INT8/PTQ，在[准确率](https://www.ultralytics.com/glossary/accuracy)损失极小的情况下进一步压缩模型，主要用于[边缘设备](https://www.ultralytics.com/blog/understanding-the-real-world-applications-of-edge-ai)；需要校准 `data`/`fraction`）；`32`/未设置则为 FP32。支持混合权重/激活精度的导出格式也接受 `'w8a8'`/`'w16a16'`/`'w8a16'`/`'w8a32'` 表示法。取代了已弃用的 `half`/`int8` 标志（`half=True` → `16`，`int8=True` → `8`，仍可使用但会触发弃用警告）。仅允许使用目标格式支持的精度（见下文）。 |
| `dynamic`   | `bool`            | `False`         | 允许 TorchScript、ONNX、OpenVINO、TensorRT 和 CoreML 导出采用动态输入尺寸，增强了处理不同图像尺寸时的灵活性。 |
| `simplify`  | `bool`            | `True`          | 使用 `onnxslim` 简化导出生成的中间 ONNX 图（参阅 [Export Formats](https://docs.ultralytics.com/modes/export)），这可能会提升性能并增强与推理引擎的兼容性。 |
| `opset`     | `int`             | `None`          | 为构建 ONNX 图的导出指定 ONNX opset 版本（参阅 [Export Formats](https://docs.ultralytics.com/modes/export)），以确保与不同的 [ONNX](https://docs.ultralytics.com/integrations/onnx) 解析器和运行时兼容。如果未设置，将使用支持的最新版本。 |
| `workspace` | `float` 或 `None` | `None`          | 设置 [TensorRT](https://docs.ultralytics.com/integrations/tensorrt) 优化的最大工作空间大小（单位为 GiB），以平衡内存使用和性能。使用 `None` 可由 TensorRT 自动分配，最高可达设备上限。 |
| `nms`       | `bool`            | `False`         | 在支持的情况下（参见 [Export Formats](https://docs.ultralytics.com/modes/export)）为导出模型添加非极大值抑制 (NMS)，从而提高检测后处理效率。这不适用于 end2end 模型。对于 CoreML，仅支持检测模型。 |
| `batch`     | `int`             | `1`             | 指定导出模型的批量推理大小，即导出模型在 `predict` 模式下将同时处理的最大图像数量。对于 Edge TPU 导出，此值会自动设为 1。 |
| `device`    | `str`             | `None`          | 指定导出的设备：GPU (`device=0`)、CPU (`device=cpu`)、适用于 Apple 芯片的 MPS (`device=mps`)、华为昇腾 NPU (`device=npu` 或 `device=npu:0`)，或者适用于 NVIDIA Jetson 的 DLA (`device=dla:0` 或 `device=dla:1`)。TensorRT 导出会自动使用 GPU，但 TensorRT 11.0 不支持 DLA。 |
| `data`      | `str`             | `None`          | 指向 [dataset](https://docs.ultralytics.com/datasets) 配置文件的路径，对于 INT8 量化校准至关重要。如果在启用 INT8 时未指定，Ultralytics 会在需要时选择特定于任务的校准数据集，或者回退到模型任务的默认数据集。 |
| `fraction`  | `float`           | `1.0`           | 指定用于 INT8 量化校准的数据集比例。允许在完整数据集的一个子集上进行校准，这对实验或资源受限时非常有用。如果启用 INT8 但未指定，将使用完整数据集。 |
| `end2end`   | `bool`            | `None`          | 覆盖支持无 NMS 推理（YOLO26、YOLOv10）的 YOLO 模型中的端到端模式。将其设为 `False`，允许你导出这些模型，以使其兼容传统的基于 NMS 的后处理流水线。详情请参阅 [端到端检测指南](https://docs.ultralytics.com/zh/guides/end2end-detection)。 |

调整这些参数可以自定义导出过程，以满足特定要求，例如部署环境、硬件限制和性能目标。选择合适的格式和设置对于在模型大小、速度和 [accuracy](https://www.ultralytics.com/glossary/accuracy) 之间实现最佳平衡至关重要。

## 导出格式

下表列出了可用的 YOLO26 导出格式。你可以使用 `format` 参数导出为任何格式，例如 `format='onnx'` 或 `format='engine'`。你可以直接在导出的模型上进行预测或验证，例如 `yolo predict model=yolo26n.onnx`。导出完成后会显示模型的使用示例。模型也可以直接在 [Ultralytics Platform](https://docs.ultralytics.com/zh/platform/train/models#export-model) 上从浏览器中导出，无需任何本地设置。

| 格式                                                         | `format` 参数 | 模型                        | 元数据 | 参数                                                         |
| :----------------------------------------------------------- | :------------ | :-------------------------- | :----- | :----------------------------------------------------------- |
| [PyTorch](https://pytorch.org/)                              | -             | `yolo26n.pt`                | ✅      | -                                                            |
| [TorchScript](https://docs.ultralytics.com/zh/integrations/torchscript) | `torchscript` | `yolo26n.torchscript`       | ✅      | `imgsz`, `quantize`, `dynamic`, `nms`, `batch`, `device`     |
| [ONNX](https://docs.ultralytics.com/zh/integrations/onnx)    | `onnx`        | `yolo26n.onnx`              | ✅      | `imgsz`, `quantize`, `dynamic`, `simplify`, `opset`, `nms`, `batch`, `data`, `fraction`, `device` |
| [OpenVINO](https://docs.ultralytics.com/zh/integrations/openvino) | `openvino`    | `yolo26n_openvino_model/`   | ✅      | `imgsz`, `quantize`, `dynamic`, `nms`, `batch`, `data`, `fraction`, `device` |
| [TensorRT](https://docs.ultralytics.com/zh/integrations/tensorrt) | `engine`      | `yolo26n.engine`            | ✅      | `imgsz`, `quantize`, `dynamic`, `simplify`, `opset`, `workspace`, `nms`, `batch`, `data`, `fraction`, `device` |
| [CoreML](https://docs.ultralytics.com/zh/integrations/coreml) | `coreml`      | `yolo26n.mlpackage`         | ✅      | `imgsz`, `dynamic`, `quantize`, `nms`, `batch`, `device`     |
| [TF SavedModel](https://docs.ultralytics.com/zh/integrations/tf-savedmodel) | `saved_model` | `yolo26n_saved_model/`      | ✅      | `imgsz`, `keras`, `quantize`, `opset`, `nms`, `batch`, `data`, `fraction`, `device` |
| [TF GraphDef](https://docs.ultralytics.com/zh/integrations/tf-graphdef) | `pb`          | `yolo26n.pb`                | ❌      | `imgsz`, `opset`, `batch`, `device`                          |
| [TF Edge TPU](https://docs.ultralytics.com/zh/integrations/edge-tpu) | `edgetpu`     | `yolo26n_edgetpu.tflite`    | ✅      | `imgsz`, `quantize`, `opset`, `data`, `fraction`, `device`   |
| [PaddlePaddle](https://docs.ultralytics.com/zh/integrations/paddlepaddle) | `paddle`      | `yolo26n_paddle_model/`     | ✅      | `imgsz`, `batch`, `device`                                   |
| [MNN](https://docs.ultralytics.com/zh/integrations/mnn)      | `mnn`         | `yolo26n.mnn`               | ✅      | `imgsz`, `batch`, `dynamic`, `quantize`, `simplify`, `opset`, `nms`, `device` |
| [NCNN](https://docs.ultralytics.com/zh/integrations/ncnn)    | `ncnn`        | `yolo26n_ncnn_model/`       | ✅      | `imgsz`, `quantize`, `batch`, `device`                       |
| [IMX500](https://docs.ultralytics.com/zh/integrations/sony-imx500) | `imx`         | `yolo26n_imx_model/`        | ✅      | `imgsz`, `quantize`, `data`, `fraction`, `nms`, `device`     |
| [RKNN](https://docs.ultralytics.com/zh/integrations/rockchip-rknn) | `rknn`        | `yolo26n_rknn_model/`       | ✅      | `imgsz`, `batch`, `name`, `quantize`, `simplify`, `opset`, `data`, `fraction`, `device` |
| [ExecuTorch](https://docs.ultralytics.com/zh/integrations/executorch) | `executorch`  | `yolo26n_executorch_model/` | ✅      | `imgsz`, `batch`, `device`                                   |
| [Axelera](https://docs.ultralytics.com/zh/integrations/axelera) | `axelera`     | `yolo26n_axelera_model/`    | ✅      | `imgsz`, `batch`, `quantize`, `data`, `fraction`, `device`   |
| [DEEPX](https://docs.ultralytics.com/zh/integrations/deepx)  | `deepx`       | `yolo26n_deepx_model/`      | ✅      | `imgsz`, `quantize`, `simplify`, `opset`, `data`, `optimize`, `device` |
| [Qualcomm QNN](https://docs.ultralytics.com/zh/integrations/qnn) | `qnn`         | `yolo26n_qnn.onnx`          | ✅      | `imgsz`, `batch`, `name`, `quantize`, `simplify`, `opset`, `data`, `fraction`, `device` |
| [LiteRT](https://docs.ultralytics.com/zh/integrations/litert) | `litert`      | `yolo26n.tflite`            | ✅      | `imgsz`, `quantize`, `batch`, `data`, `fraction`, `device`   |
| [Hailo](https://docs.ultralytics.com/zh/integrations/hailo)  | `hailo`       | `yolo26n_hailo_model/`      | ✅      | `imgsz`, `name`, `quantize`, `data`, `fraction`, `simplify`, `conf`, `iou` |
| [Huawei Ascend](https://docs.ultralytics.com/zh/integrations/ascend) | `ascend`      | `yolo26n_ascend_model/`     | ✅      | `imgsz`, `batch`, `name`, `quantize`, `opset`, `simplify`, `nms` |

## 量化选项

使用 `quantize` 参数来指定导出精度。字符串值不区分大小写，Ultralytics 会在导出前将接受的别名规范化：

| 请求值                             | 规范化值  | 含义                                                         |
| :--------------------------------- | :-------- | :----------------------------------------------------------- |
| `8`, `"8"`, `"int8"`, `"w8a8"`     | `8`       | INT8 权重和激活                                              |
| `16`, `"16"`, `"fp16"`, `"w16a16"` | `16`      | FP16 权重和激活                                              |
| `32`, `"32"`, `"fp32"`, `"w32a32"` | `32`      | FP32 导出；与未设置时相同，但 CoreML NMS ML Programs 默认为 FP16 |
| `"w8a16"`                          | `"w8a16"` | INT8 权重和 16 位激活（FP16；LiteRT 上为 INT16）             |
| `"w8a32"`                          | `"w8a32"` | INT8 权重和 FP32 激活（LiteRT 动态 INT8，无需校准）          |

旧版的 `half=True` 和 `int8=True` 标志仍然被接受，但会触发弃用警告并转发至 `quantize=16` 和 `quantize=8`。

并非所有导出格式都支持每种精度。明确的 `quantize` 请求要么生成该精度，要么在导出前失败：

| 格式          | FP32 (`32`/未设置) | FP16 (`16`)  | INT8 (`8`) | W8A16 (`"w8a16"`) | 注意事项                                                     |
| :------------ | :----------------- | :----------- | :--------- | :---------------- | :----------------------------------------------------------- |
| PyTorch       | ✅                  | 不适用       | 不适用     | 不适用            | 原生训练/检查点格式。                                        |
| TorchScript   | ✅                  | ✅ 仅限 GPU   | ❌          | ❌                 | FP16 TorchScript 导出需要 `device=0`；CPU 导出则为 FP32。    |
| ONNX          | ✅                  | ✅            | ✅          | ❌                 | INT8 使用 ONNX Runtime 静态量化和校准数据。                  |
| OpenVINO      | ✅                  | ✅            | ✅          | ❌                 | INT8 使用 NNCF 训练后量化。                                  |
| TensorRT      | ✅                  | ✅            | ✅          | ❌                 | INT8 需要具有代表性的校准数据。                              |
| CoreML        | ✅¹                 | ✅            | ✅          | ✅                 | CoreML INT8 是权重量化；W8A16 使用 INT8 权重和 FP16 激活。¹未设置的 NMS ML Programs 默认为 FP16。 |
| TF SavedModel | ✅                  | ❌            | ✅          | ❌                 | INT8 导出使用 TensorFlow 校准。                              |
| TF GraphDef   | ✅                  | ❌            | ❌          | ❌                 | 无导出时的精度转换。                                         |
| Edge TPU      | ❌                  | ❌            | ✅ 自动     | ❌                 | Edge TPU 需要 INT8；未设置时会自动启用。                     |
| PaddlePaddle  | ✅                  | ❌            | ❌          | ❌                 | 无导出时的精度转换。                                         |
| MNN           | ✅                  | ✅            | ✅          | ❌                 | INT8 是通过 MNN 转换进行的权重量化。                         |
| NCNN          | ✅                  | ✅            | ❌          | ❌                 | 移动端/嵌入式运行时格式。                                    |
| IMX500        | ❌                  | ❌            | ✅ 自动     | ✅                 | IMX500 需要量化；未设置时会自动启用 INT8。                   |
| RKNN          | ❌                  | ✅ 视芯片而定 | ✅          | ❌                 | RK3588/RK3576/RK3566/RK3568/RK3562/RK2118/RV1126B 支持 FP16 或 INT8；RV1103/RV1106 变体仅支持 INT8。 |
| ExecuTorch    | ✅                  | ❌            | ❌          | ❌                 | 无导出时的精度转换。                                         |
| Axelera       | ❌                  | ❌            | ✅ 自动     | ❌                 | Axelera 导出需要 INT8；未设置时会自动启用。                  |
| DEEPX         | ❌                  | ❌            | ✅ 自动     | ❌                 | DEEPX 导出需要 INT8；未设置时会自动启用。                    |
| Qualcomm QNN  | ❌                  | ❌            | ❌          | ✅ 自动            | QNN HTP 导出固定为 INT8 权重和 16 位激活。                   |
| LiteRT        | ✅                  | ❌            | ✅          | ✅                 | 静态 INT8 (`8`) 和 `"w8a16"`（int8 权重 + **int16** 激活）使用校准数据；也支持 `"w8a32"` 动态 INT8（无需校准）。`quantize=16` 不是一种单独的导出方式；FP32 模型在运行时通过 GPU 委托以 FP16 运行。 |
| 华为昇腾      | ❌                  | ✅ 自动       | ❌          | ❌                 | 昇腾 AI 核心卷积仅接受 FP16/INT8 输入，因此 ATC 会编译 FP16；未设置时会自动启用。 |

对于 INT8 和 W8A16 导出，请通过 `data` 提供具有代表性的校准数据，例如 `data="coco8.yaml"`，除非目标集成文档说明了默认或自动启用行为。LiteRT `"w8a32"`（动态 INT8）方案无需校准数据。

## Example

> 注意:
>
> `onnxruntime` 和 `onnxruntime-gpu` 不要同时安装，否则使用 `gpu` 推理时速度会很慢，如果同时安装了2个包，要全部卸载，再安装`onnxruntime-gpu` 才能使用gpu推理，否则gpu速度会很慢

py

```py
from pathlib import Path
from ultralytics import YOLO, settings


settings.update(
    {
        "tensorboard": True,
        "datasets_dir": "datasets",
        "weights_dir": "weights",
        "runs_dir": "runs",
    }
)


model_path = Path("weights/yolo26n.pt").resolve()
data_path = Path("datasets/coco/coco.yaml").resolve()

print(f"{model_path} is exists: {model_path.exists()}")
print(f"{data_path} is exists: {data_path.exists()}")
model_path = str(model_path)
data_path = str(data_path)

# Load a model
model = YOLO(model_path, task="detect")


export_type = "onnx"
imgsz = [640, 640]
quantize = 16
dynamic = False
nms = False
batch = 1


# Export the model
if export_type == "torchscript":
    model.export(
        format="torchscript",
        quantize=quantize,
        imgsz=imgsz,
        dynamic=dynamic,
        optimize=True,
        nms=nms,
        batch=batch,
        device="cpu",
    )
elif export_type == "onnx":
    model.export(
        format="onnx",
        quantize=quantize,
        imgsz=imgsz,
        dynamic=dynamic,
        simplify=True,
        opset=None,
        nms=nms,
        batch=batch,
        data=data_path,
        device="cpu",
    )
elif export_type == "openvino":
    model.export(
        format="openvino",
        quantize=quantize,
        imgsz=imgsz,
        dynamic=dynamic,
        nms=nms,
        batch=batch,
        data=data_path,
        fraction=0.1,
        device="cpu",
    )
elif export_type == "tensorrt":
    model.export(
        format="tensorrt",
        quantize=quantize,
        imgsz=imgsz,
        dynamic=dynamic,
        simplify=True,
        workspace=None,
        nms=nms,
        batch=batch,
        data=data_path,
        fraction=0.1,
        device=0,
    )
elif export_type == "ncnn":
    model.export(
        format="ncnn",
        quantize=quantize,
        imgsz=imgsz,
        batch=batch,
        device="cpu",
    )
elif export_type == "saved_model":
    model.export(
        format="saved_model",
        quantize=quantize,
        imgsz=imgsz,
        keras=True,
        nms=nms,
        batch=batch,
        data=data_path,
        fraction=0.1,
        device="cpu",
    )
elif export_type == "litert":
    model.export(
        format="litert",
        quantize=quantize,
        imgsz=imgsz,
        nms=nms,
        batch=batch,
        data=data_path,
        fraction=0.1,
        device="cpu",
    )
else:
    print("Unsupported export type")

print("Model exported successfully")
```

cmd

```sh
yolo detect export imgsz=640 model=weights/yolo26n.pt format=onnx simplify=True device=0 project=coco8
```

# [跟踪](https://docs.ultralytics.com/zh/modes/track/)

## 可用的追踪器

Ultralytics YOLO 内置了六种跟踪器。通过将对应的 YAML 配置文件传递给 `tracker` 参数即可启用。

| 跟踪器                                                       | 配置文件          | 运动模型                 | 外观 / ReID        | 摄像机运动补偿           | 遮挡处理                                  |
| :----------------------------------------------------------- | :---------------- | :----------------------- | :----------------- | :----------------------- | :---------------------------------------- |
| **[BoT-SORT](https://docs.ultralytics.com/zh/modes/track#bot-sort)** | `botsort.yaml`    | 线性卡尔曼滤波           | 可选 (`with_reid`) | 是 (sparseOptFlow / ECC) | 跟踪缓冲区 + ReID 重绑定                  |
| **[ByteTrack](https://docs.ultralytics.com/zh/modes/track#bytetrack)** | `bytetrack.yaml`  | 线性卡尔曼滤波           | 无                 | 否                       | 两阶段低置信度救援                        |
| **[OC-SORT](https://docs.ultralytics.com/zh/modes/track#oc-sort)** | `ocsort.yaml`     | 以观察为中心的卡尔曼滤波 | 无                 | 否                       | ORU、OCM、从最后一次观察进行 OCR 重新更新 |
| **[Deep OC-SORT](https://docs.ultralytics.com/zh/modes/track#deep-oc-sort)** | `deepocsort.yaml` | 以观察为中心的卡尔曼滤波 | 可选 (`with_reid`) | 可选 (`gmc_method`)      | OC-SORT + 自适应外观 EMA                  |
| **[FastTracker](https://docs.ultralytics.com/zh/modes/track#fasttracker)** | `fasttrack.yaml`  | 线性卡尔曼滤波 + 回滚    | 无                 | 否                       | 卡尔曼回滚 + 遮挡时的 bbox 放大           |
| **[TrackTrack](https://docs.ultralytics.com/zh/modes/track#tracktrack)** | `tracktrack.yaml` | 线性卡尔曼滤波 (NSA)     | 可选 (HMIoU 后备)  | 是 (sparseOptFlow / ECC) | 迭代多线索关联 + TAI                      |

默认追踪器是 BoT-SORT。

### 我应该使用哪个跟踪器？

使用此流程来选择起点：

1. **需要最快、最简单的基准？** → **ByteTrack**（无 ReID，无摄像机运动补偿，开销最小）。
2. **手持、无人机或移动摄像机拍摄的素材？** → **BoT-SORT**（默认；增加了摄像机运动补偿和可选的 ReID）。
3. **非线性运动（体育、舞蹈、突变转向）且无需 ReID？** → **OC-SORT**（以观察为中心的校正，无需外观成本）。
4. **主要问题是 ID 交换的拥挤移动摄像机场景？** → **Deep OC-SORT** 或 **TrackTrack**（两者均增加了自适应外观融合；TrackTrack 还增加了多线索关联和重复 ID 抑制）。
5. **实时频繁的部分重叠，没有 ReID 预算？** → **FastTracker**（带有卡尔曼回滚的遮挡感知 ByteTrack 变体）。

## 跟踪器

将跟踪器配置文件名传递给 `tracker=` 即可。所有其他代码保持不变。

> python

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

results = model.track(source="path/to/video.mp4", tracker="bytetrack.yaml")
results = model.track(source="path/to/video.mp4", tracker="ocsort.yaml")
results = model.track(source="path/to/video.mp4", tracker="tracktrack.yaml")
```

> CLI

```sh
yolo track model=yolo26n.pt source="path/to/video.mp4" tracker="bytetrack.yaml"
```

## 配置

### 追踪参数

跟踪配置与 Predict 模式共享属性，例如 `conf`、`iou` 和 `show`。如需更多配置，请参阅 [Predict](https://docs.ultralytics.com/zh/modes/predict#inference-arguments) 模型页面。

> python

```sh
from ultralytics import YOLO

# Configure the tracking parameters and run the tracker
model = YOLO("yolo26n.pt")
results = model.track(source="https://youtu.be/LNwODJXcvt4", conf=0.1, iou=0.7, show=True)
```

> CLI

```sh
# Configure tracking parameters and run the tracker using the command line interface
yolo track model=yolo26n.pt source="https://youtu.be/LNwODJXcvt4" conf=0.1 iou=0.7 show
```

### 自定义跟踪器配置

Ultralytics还允许您使用修改后的跟踪器配置文件。为此，只需从[ultralytics/cfg/trackers](https://github.com/ultralytics/ultralytics/tree/main/ultralytics/cfg/trackers)复制一个跟踪器配置文件（例如`custom_tracker.yaml`），并根据您的需求修改任何配置（除了`tracker_type`）。

> python

```python
from ultralytics import YOLO

# Load the model and run the tracker with a custom configuration file
model = YOLO("yolo26n.pt")
results = model.track(source="https://youtu.be/LNwODJXcvt4", tracker="custom_tracker.yaml")
```

> CLI

```sh
# Load the model and run the tracker with a custom configuration file using the command line interface
yolo track model=yolo26n.pt source="https://youtu.be/LNwODJXcvt4" tracker='custom_tracker.yaml'
```

### 共享跟踪器参数

以下参数是大多数跟踪器 YAML 文件通用的；并非每个参数都会出现在所有配置中：

> 跟踪器阈值信息
>
> 如果检测结果的置信度分数低于 `track_high_thresh`，跟踪器将不会更新该目标，从而导致没有活跃的跟踪轨道。

| 参数                | 有效值或范围                                                 | 描述                                                         |
| :------------------ | :----------------------------------------------------------- | :----------------------------------------------------------- |
| `tracker_type`      | `botsort`, `bytetrack`, `ocsort`, `deepocsort`, `fasttrack`, `tracktrack` | 指定跟踪器类型。                                             |
| `track_high_thresh` | `0.0-1.0`                                                    | 第一次关联的阈值。影响将检测结果匹配到现有跟踪轨道的置信度。 |
| `track_low_thresh`  | `0.0-1.0`                                                    | 对低置信度检测结果进行第二次关联的阈值。对于 OC-SORT 和 Deep OC-SORT，此项仅在 `use_byte: True` 时生效。 |
| `new_track_thresh`  | `0.0-1.0`                                                    | 如果检测结果无法与任何现有轨道匹配，则用于初始化新轨道的阈值。 |
| `track_buffer`      | `>=0`                                                        | 丢失轨道被保留存活的帧数，超过后将被移除。数值越大，对遮挡的容忍度越高。 |
| `match_thresh`      | `0.0-1.0`                                                    | 匹配轨道的阈值。数值越高，匹配越宽松。                       |
| `fuse_score`        | `True`, `False`                                              | 是否在匹配前将置信度分数与 IoU 距离进行融合。                |
| `gmc_method`        | `sparseOptFlow`, `orb`, `sift`, `ecc`, `none`                | 全局运动补偿方法。有助于考虑摄像机运动。                     |
| `proximity_thresh`  | `0.0-1.0`                                                    | 有效的 ReID 匹配所需的最小 IoU。确保在使用外观线索之前空间上足够接近。 |
| `appearance_thresh` | `0.0-1.0`                                                    | ReID 所需的最小外观相似度。                                  |
| `with_reid`         | `True`, `False`                                              | 启用基于外观的匹配，以便在遮挡情况下获得更好的跟踪效果。BoT-SORT、Deep OC-SORT 和 TrackTrack 支持此功能。 |
| `model`             | `auto` 或指向导出文件的路径                                  | ReID 模型。`auto` 在可用时使用原生 YOLO 主干特征；否则回退到 `yolo26n-cls.pt`。对于自定义编码器，请传入 `.torchscript`, `.onnx`, `.engine`, `.openvino`, …… 文件。 |

#### 追踪器特定参数

每种算法在共享参数之外还公开了额外的调节旋钮。请查看下文针对各追踪器的说明和调优建议，或直接参考配置文件：

- [`botsort.yaml`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/botsort.yaml)
- [`bytetrack.yaml`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/bytetrack.yaml)
- [`ocsort.yaml`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/ocsort.yaml)
- [`deepocsort.yaml`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/deepocsort.yaml)
- [`fasttrack.yaml`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/fasttrack.yaml)
- [`tracktrack.yaml`](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/tracktrack.yaml)

### 启用重识别 (ReID)

ReID 默认处于禁用状态以尽量减少开销。如需启用，请在追踪器配置文件中设置 `with_reid: True`。

**ReID 模型选项：**

- **`model: auto`** — 使用原生 YOLO 检测器特征，仅增加极小的开销。当你需要在不大幅影响性能的前提下使用部分 ReID 功能时，这是理想选择。如果检测器未公开兼容的特征，系统将回退至 `yolo26n-cls.pt`。
- **已导出 ReID 模型** — 将 `model:` 指向一个已导出的文件（`.torchscript`、`.onnx`、`.engine`、`.openvino` 等），可以在增加每次裁剪额外前向传播开销的情况下获得更具区分度的嵌入特征。编码器通过 `AutoBackend` 加载，因此 Ultralytics 支持的任何导出格式均可在无需更改代码的情况下使用。

每个模型大小都有现成的 ONNX 编码器发布。将 `model:` 设置为这些名称之一，文件会在追踪器首次运行时自动下载（方式与获取 YOLO 权重相同）——无需手动导出或下载步骤：

```python
# In your tracker config (e.g. tracktrack.yaml)
with_reid: True
model: yolo26n-reid.onnx # downloaded on first use; swap n→s/m/l/x for a larger encoder
```

| 模型                                                         | 大小 (像素) | 参数 (百万) | FLOPs (十亿) |
| :----------------------------------------------------------- | :---------- | :---------- | :----------- |
| [YOLO26n-reid.onnx](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26n-reid.onnx) | 448         | 2.8         | 2.0          |
| [YOLO26s-reid.onnx](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s-reid.onnx) | 448         | 7.5         | 6.6          |
| [YOLO26m-reid.onnx](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26m-reid.onnx) | 448         | 12.4        | 20.1         |
| [YOLO26l-reid.onnx](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26l-reid.onnx) | 448         | 15.3        | 25.2         |
| [YOLO26x-reid.onnx](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26x-reid.onnx) | 448         | 32.7        | 55.9         |

> ReID 仅用于追踪
>
> 目前仅提供用于追踪器外观分支的 ONNX ReID 编码器。ReID 的 `train`、`val` 和 `predict` 模式，以及专用的 ReID 导出方案，目前仍在开发中。

若要通过单独的分类模型获得更好的性能，请将其导出到更快的后端，例如 TensorRT：

> **将 ReID 模型导出为 TensorRT**

```python
from torch import nn

from ultralytics import YOLO

# Load the classification model
model = YOLO("yolo26n-cls.pt")

# Add average pooling layer
head = model.model.model[-1]
pool = nn.Sequential(nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten(start_dim=1))
pool.f, pool.i = head.f, head.i
model.model.model[-1] = pool

# Export to TensorRT
model.export(format="engine", quantize=16, dynamic=True, batch=32)
```

导出后，在你的追踪器配置中指向该 TensorRT 模型路径。

## 追踪器详情

展开下方各部分的详情，了解每个追踪器的设计、特定参数及调优技巧。

#### BoT-SORT

[BoT-SORT](https://github.com/NirAharon/BoT-SORT) (Aharon 等人，2022) 是默认的追踪器。它在 ByteTrack 的基础上增加了摄像机运动补偿和可选的 ReID 功能：

- **摄像机运动补偿 (CMC)：** 在 IoU 匹配之前，将每帧估计的仿射变换（默认使用稀疏光流；也可使用 ORB / ECC）应用于卡尔曼状态。
- **可选 ReID：** 外观嵌入可以融合到代价矩阵中。默认禁用；可通过 `with_reid: True` 启用。

**最适用于：** 通用追踪场景，尤其是运动的摄像机。仅当外貌相似的人群导致 ID 交换时才添加 ReID。

**BoT-SORT 特定参数：**

| 参数                | 有效值或范围                                  | 描述                                                         |
| :------------------ | :-------------------------------------------- | :----------------------------------------------------------- |
| `gmc_method`        | `sparseOptFlow`, `orb`, `sift`, `ecc`, `none` | 摄像机运动补偿后端。`sparseOptFlow` 为默认值。`none` 表示禁用 CMC。 |
| `with_reid`         | `True`, `False`                               | 启用基于外观的匹配。默认关闭。                               |
| `model`             | `auto` 或 ReID 模型路径                       | ReID 模型。`auto` 在可用时使用原生 YOLO 特征；否则传入 `.torchscript` / `.onnx` / `.engine` 路径。 |
| `proximity_thresh`  | `0.0-1.0`                                     | 考虑外观特征之前的最小 IoU。                                 |
| `appearance_thresh` | `0.0-1.0`                                     | ReID 匹配所需的最小余弦相似度。调高此值可减少身份 ID 交换。  |

**调优技巧：**

- **静态摄像机：** 设置 `gmc_method: none` 可节省每帧几毫秒的耗时。
- **剧烈摄像机运动：** 保留 `sparseOptFlow`；`ecc` 更准确但速度较慢。
- **外貌相似人群：** 开启 `with_reid: True` 并调高 `appearance_thresh`（例如 `0.85+`）。

#### ByteTrack

[ByteTrack](https://github.com/FoundationVision/ByteTrack) (Zhang 等人，ECCV 2022) 是轻量级的基准追踪器。它使用线性卡尔曼 + IoU 配合两阶段关联：

- **第一阶段：** 将高置信度检测结果与活跃轨迹进行匹配。
- **第二阶段：** 将未匹配的轨迹与低置信度检测结果重新匹配，从而恢复短暂部分遮挡下的轨迹。

该算法没有外观模型，也没有摄像机运动补偿。

**最适用于：** 检测器开销占据主导地位且你需要最低追踪器开销的静态或近乎静态的摄像机场景。

**ByteTrack 特定参数：** 除 [共享追踪器参数](https://docs.ultralytics.com/zh/modes/track#shared-tracker-arguments) 外无其他参数。

**调优技巧：**

- **噪声检测器：** 降低 `track_low_thresh` 以使第二阶段拥有更多候选框。
- **高召回率检测器：** 调高 `track_high_thresh` 以减少碎片化 ID。
- **频繁 ID 闪烁：** 调高 `track_buffer` 以保留短暂丢失的轨迹。

#### OC-SORT

[OC-SORT](https://arxiv.org/abs/2203.14360) (Cao 等人，CVPR 2023) 是 SORT 的观测中心化扩展。它保留了 SORT 的轻量级设计（无外观特征），并增加了三项校正：

- **观测中心化重更新 (ORU)：** 在上一次观测和当前检测之间重放虚拟轨迹，重新运行卡尔曼更新以修复漂移的速度。
- **观测中心化动量 (OCM)：** 通过速度一致性项对向错误方向移动的检测结果进行惩罚。
- **观测中心化恢复 (OCR)：** 使用未匹配检测结果的最后一次观测而非预测状态，将其与最近丢失的轨迹重新比对。

**最适用于：** 无需 ReID 模型开销的非线性运动场景。

**OC-SORT 特定参数：**

| 参数       | 有效值或范围    | 描述                                                         |
| :--------- | :-------------- | :----------------------------------------------------------- |
| `delta_t`  | `>=1`           | OCM 中用于计算速度方向的时间窗口（帧数）。较大的值会产生更平滑的结果。 |
| `inertia`  | `0.0-1.0`       | 速度一致性代价的权重。较高的值会惩罚剧烈的方向改变。         |
| `use_byte` | `True`, `False` | 启用一种针对低置信度检测结果的 ByteTrack 式第二轮关联。      |

**调优技巧：**

- **非线性运动：** 调高 `inertia`（例如 `0.3-0.4`）。
- **稀疏检测：** 启用 `use_byte: True`。
- **长时间遮挡：** 调高 `track_buffer` 以便 OCR 有更多丢失的轨迹可供重新绑定。

#### Deep OC-SORT

[Deep OC-SORT](https://arxiv.org/abs/2302.11813) 通过外观信息和摄像机运动补偿增强了 OC-SORT：

- **自适应外观融合：** 检测嵌入被融合到代价矩阵中，其权重由检测置信度和重叠度进行调节。
- **动态外观 EMA：** 轨迹嵌入使用 EMA 进行更新，其平滑因子会根据检测置信度进行自适应调整。
- **摄像机运动补偿：** 卡尔曼状态通过稀疏光流、ORB 或 ECC 在帧间进行扭曲变形。

**最适用于：** 人群密集或摄像机移动的场景，这些场景下外观差异小但空间靠近的目标常发生 ID 交换。

**Deep OC-SORT 特定参数：**

| 参数                | 有效值或范围                                  | 描述                                                         |
| :------------------ | :-------------------------------------------- | :----------------------------------------------------------- |
| `with_reid`         | `True`, `False`                               | 启用基于外观的匹配。默认关闭。                               |
| `model`             | `auto`，已导出的 ReID 模型文件                | ReID 模型。`auto` 会重用原生 YOLO 特征；否则传入已导出的文件路径（`.torchscript`、`.onnx`、`.engine` 等）。 |
| `proximity_thresh`  | `0.0-1.0`                                     | 考虑外观特征之前的最小 IoU。                                 |
| `appearance_thresh` | `0.0-1.0`                                     | ReID 匹配所需的最小余弦相似度。                              |
| `alpha_fixed_emb`   | `0.0-1.0`                                     | 轨迹嵌入更新的基础 EMA 因子。较高的值会使旧的嵌入特征保留更长时间。 |
| `gmc_method`        | `sparseOptFlow`, `orb`, `sift`, `ecc`, `none` | 全局运动补偿方法。                                           |
| `delta_t`           | `>=1`                                         | OCM 中用于计算速度方向的时间窗口（帧数）（继承自 OC-SORT）。 |
| `inertia`           | `0.0-1.0`                                     | 速度一致性代价的权重（继承自 OC-SORT）。                     |
| `use_byte`          | `True`, `False`                               | 启用一种针对低置信度检测结果的 ByteTrack 式第二轮关联（继承自 OC-SORT）。 |

**调优技巧：**

- **人群 ID 交换：** 调高 `appearance_thresh`（例如 `0.92-0.95`）并调低 `alpha_fixed_emb`，使嵌入特征更新得更慢。
- **移动摄像机：** 设置 `gmc_method: sparseOptFlow`（Deep OC-SORT 默认为 `none`）。
- **更低延迟：** 仅保留运动 + CMC 功能时，保持 `with_reid: False`（默认）；仅当 ID 交换成为主要的错误原因时才启用 ReID。

#### FastTracker

[FastTracker](https://arxiv.org/abs/2508.14370) 是一种具有遮挡感知能力的 ByteTrack 变体，不含外观模型：

- **遮挡检测：** 当被其他活跃轨迹覆盖的程度超过 `occ_cover_thresh` 时，将轨迹标记为遮挡。
- **遮挡时的卡尔曼回滚：** 使用环形缓冲历史记录将卡尔曼状态回滚至遮挡前的帧。
- **运动阻尼与搜索区域扩大：** 遮挡时减小速度并扩大预测的 bbox。
- **初始 IoU 抑制：** 防止在活跃轨迹之上生成新的轨迹。

**最适用于：** 具有频繁目标间重叠（人群、队列、体育）的实时纯检测追踪流水线。

**FastTracker 特定参数：**

| 参数                        | 有效值或范围 | 描述                                                         |
| :-------------------------- | :----------- | :----------------------------------------------------------- |
| `reset_velocity_offset_occ` | `>=0`        | 发生遮挡时恢复卡尔曼速度所回溯的历史帧数。                   |
| `reset_pos_offset_occ`      | `>=0`        | 发生遮挡时恢复卡尔曼位置所回溯的历史帧数。                   |
| `enlarge_bbox_occ`          | `>=1.0`      | 遮挡时应用于预测 bbox 的高度缩放比例（宽度通过 XYAH 长宽比缩放）。 |
| `dampen_motion_occ`         | `0.0-1.0`    | 遮挡期间的速度乘数。较低的值会使轨迹在遮挡期间“减速”。       |
| `active_occ_to_lost_thresh` | `>=1`        | 活跃轨迹在被移至丢失状态前允许的最大连续遮挡帧数。           |
| `occ_cover_thresh`          | `0.0-1.0`    | 一个轨迹区域被另一个活跃轨迹所覆盖的比例，用于判定遮挡。     |
| `occ_reappear_window`       | `>=0`        | 最近被遮挡的丢失轨迹仍可被优先重新发现的帧数。               |
| `init_iou_suppress`         | `0.0-1.0`    | 如果新轨迹与任何活跃轨迹的 IoU 超过此值，则抑制新轨迹的初始化。设置为 `1.0` 可禁用。 |

**调优技巧：**

- **频繁部分遮挡：** 降低 `occ_cover_thresh`（例如 `0.5-0.6`）。
- **重叠处的重复 ID：** 降低 `init_iou_suppress`（例如 `0.5`）。
- **长期遮挡：** 同时提高 `occ_reappear_window` 和 `track_buffer`。
- **快速移动目标：** 提高 `dampen_motion_occ`（接近 `1.0`）并降低 `enlarge_bbox_occ`。

#### TrackTrack

[TrackTrack](https://openaccess.thecvf.com/content/CVPR2025/papers/Shim_Focusing_on_Tracks_for_Online_Multi-Object_Tracking_CVPR_2025_paper.pdf) (Shim 等人，CVPR 2025) 通过多线索迭代关联，从每个轨迹的角度进行推理：

- **基于轨迹视角的关联 (TPA)：** 结合了 HMIoU、余弦 ReID 距离、置信度投影距离和角点角度距离。分配过程通过放宽阈值进行迭代求解。
- **轨迹感知初始化 (TAI)：** 在创建新 ID 之前抑制重复生成。

**最适合：** 频繁遮挡且重复 ID 成为问题的拥挤场景。

**TrackTrack 特有参数：**

| 参数             | 有效值或范围                                  | 描述                                                         |
| :--------------- | :-------------------------------------------- | :----------------------------------------------------------- |
| `iou_weight`     | `0.0-1.0`                                     | 多线索成本矩阵中 HMIoU 距离的权重。                          |
| `reid_weight`    | `0.0-1.0`                                     | 余弦 ReID 距离的权重。如果禁用 ReID，则回退到 HMIoU。        |
| `conf_weight`    | `0.0-1.0`                                     | 置信度投影距离的权重。                                       |
| `angle_weight`   | `0.0-1.0`                                     | 角点角度距离的权重。                                         |
| `penalty_p`      | `0.0-1.0`                                     | 低置信度检测的成本惩罚。                                     |
| `penalty_q`      | `0.0-1.0`                                     | 通过二次 NMS 恢复的检测的成本惩罚。                          |
| `reduce_step`    | `0.0-1.0`                                     | 每次迭代的匹配阈值放宽幅度。                                 |
| `tai_thr`        | `0.0-1.0`                                     | 轨迹感知初始化 NMS 的 IoU 阈值。                             |
| `min_track_len`  | `>=0`                                         | 确认新轨迹之前所需的最少成功更新次数。                       |
| `lost_match_thr` | `0.0-1.0`                                     | 用于放宽丢失重新绑定步骤的成本门限；`0` 表示禁用。           |
| `with_reid`      | `True`, `False`                               | 启用余弦 ReID 外观匹配（使用原生 YOLO 特征）。默认关闭。     |
| `model`          | `auto`，ReID 文件                             | ReID 模型；`auto` 使用原生 YOLO 特征，否则使用导出的 ReID 文件。 |
| `gmc_method`     | `sparseOptFlow`, `orb`, `sift`, `ecc`, `none` | 全局运动补偿方法。                                           |

**调优技巧：**

- **拥挤行人：** 降低 `tai_thr`（例如 `0.45`）以抑制更多重复生成；提高 `track_buffer` 以应对更长的遮挡。
- **快速相机运动：** 保持启用 `gmc_method: sparseOptFlow`。
- **小型/快速物体：** 适当提高 `angle_weight` 并降低 `min_track_len`。
- **仅在需要时启用 ReID：** 它会增加推理成本；对于短时间遮挡，默认的多线索成本通常就足够了。

## Example

```python
# https://docs.ultralytics.com/zh/models/yolo-world/

from pathlib import Path
from ultralytics import YOLOWorld, settings
from ultralytics.engine.results import Results


settings.update(
    {
        "tensorboard": True,
        "datasets_dir": "datasets",
        "weights_dir": "weights",
        "runs_dir": "runs",
    }
)


model_path = Path("weights/yolov8x-worldv2.pt").resolve()
source = Path("datasets/videoss/traffic monitor.mp4").resolve()
project = "traffic monitor"
name = "yolov8x-worldv2/track"

print(f"{model_path} is exists: {model_path.exists()}")
print(f"{source} is exists: {source.exists()}")


model = YOLOWorld(model_path)

# prompt based (optional)
# names = ["person", "car", "bus"]
# model.set_classes(names)

results = model.track(
    source,
    conf=0.25,
    iou=0.7,
    imgsz=640,
    rect=True,
    device=0,
    batch=1,
    max_det=300,
    vid_stride=1,
    stream_buffer=False,
    visualize=False,
    augment=False,
    agnostic_nms=False,
    classes=None,  # list[int] | None, 将预测结果筛选到一组类别 ID。只会返回属于指定类别的检测结果。这对于专注于多类别检测任务中的相关对象非常有用。
    retina_masks=False,
    embed=None,
    project=project,
    name=name,
    stream=True,
    verbose=True,
    compile=False,
    end2end=None,
    # below are visualize parameters
    show=True,
    save=True,
    save_frames=False,
    save_txt=False,
    save_conf=False,
    save_crop=False,
    show_labels=True,
    show_conf=True,
    show_boxes=True,
    line_width=None,
    # tracking parameters
    tracker="botsort.yaml",
)

result: Results
for result in results:
    result.orig_img
    result.orig_shape
    result.names
    boxes = result.boxes  # Boxes object for bounding box outputs
    boxes.id
    boxes.cls
    boxes.conf
    boxes.xyxy
    boxes.xyxyn
    boxes.xywh
    boxes.xywhn
    result.masks  # Masks object for segmentation masks outputs
    result.keypoints  # Keypoints object for pose outputs
    result.probs  # Probs object for classification outputs
    result.obb  # Oriented boxes object for OBB outputs
    result.path  # Path to the input image file.
    result.save_dir  # Directory to save results.
    # result.show()  # display to screen
    # result.save(filename="result.jpg")  # Save annotated inference results image to file.
    # result.save_txt(txt_file="result.txt", save_conf=False)  # Save detection results to a text file.
    # result.save_crop(save_dir="crops", file_name="im.jpg")  # Save cropped detection images to specified directory.
```

# yolo special commands

## yolo help

```sh
> yolo help
    Arguments received: ['yolo', 'help']. Ultralytics 'yolo' commands use the following syntax:

        yolo TASK MODE ARGS

        Where   TASK (optional) is one of ['classify', 'detect', 'pose', 'segment', 'obb']
                MODE (required) is one of ['predict', 'track', 'benchmark', 'train', 'val', 'export']
                ARGS (optional) are any number of custom 'arg=value' pairs like 'imgsz=320' that override defaults.
                    See all ARGS at https://docs.ultralytics.com/usage/cfg or with 'yolo cfg'

    1. Train a detection model for 10 epochs with an initial learning_rate of 0.01
        yolo train data=coco8.yaml model=yolo26n.pt epochs=10 lr0=0.01

    2. Predict a YouTube video using a pretrained segmentation model at image size 320:
        yolo predict model=yolo26n-seg.pt source='https://youtu.be/LNwODJXcvt4' imgsz=320

    3. Validate a pretrained detection model at batch-size 1 and image size 640:
        yolo val model=yolo26n.pt data=coco8.yaml batch=1 imgsz=640

    4. Export a YOLO26n classification model to ONNX format at image size 224 by 128 (no TASK required)
        yolo export model=yolo26n-cls.pt format=onnx imgsz=224,128

    5. Ultralytics solutions usage
        yolo solutions count or any of ['crop', 'blur', 'workout', 'heatmap', 'isegment', 'visioneye', 'speed', 'queue', 'analytics', 'inference', 'trackzone'] source="path/to/videos.mp4"

    6. Run special commands:
        yolo help
        yolo checks
        yolo version
        yolo settings
        yolo copy-cfg
        yolo cfg
        yolo solutions help

    Docs: https://docs.ultralytics.com
    Solutions: https://docs.ultralytics.com/solutions/
    Community: https://community.ultralytics.com
    GitHub: https://github.com/ultralytics/ultralytics
```

## yolo checks

```sh
> yolo checks
Ultralytics 8.4.19 🚀 Python-3.12.12 torch-2.10.0+cu128 CUDA:0 (NVIDIA GeForce RTX 3090, 24124MiB)
Setup complete ✅ (32 CPUs, 93.9 GB RAM, 596.4/983.3 GB disk)

OS                     Linux-5.15.0-140-generic-x86_64-with-glibc2.31
Environment            Linux
Python                 3.12.12
Install                git
Path                   /home/spepc/lihongtu/dl/train/ultralytics--git/ultralytics
RAM                    93.90 GB
Disk                   596.4/983.3 GB
CPU                    13th Gen Intel Core i9-13900K
CPU count              32
GPU                    NVIDIA GeForce RTX 3090, 24124MiB
GPU count              1
CUDA                   12.8

numpy                  ✅ 2.4.2>=1.23.0
matplotlib             ✅ 3.10.8>=3.3.0
opencv-python          ✅ 4.13.0.92>=4.6.0
pillow                 ✅ 12.1.1>=7.1.2
pyyaml                 ✅ 6.0.3>=5.3.1
requests               ✅ 2.32.5>=2.23.0
scipy                  ✅ 1.17.1>=1.4.1
torch                  ✅ 2.10.0>=1.8.0
torch                  ✅ 2.10.0!=2.4.0,>=1.8.0; sys_platform == "win32"
torchvision            ✅ 0.25.0>=0.9.0
psutil                 ✅ 7.2.2>=5.8.0
polars                 ✅ 1.38.1>=0.20.0
ultralytics-thop       ✅ 2.0.18>=2.0.18
```

## yolo version

```sh
> yolo version
8.4.19
```

## yolo settings

```sh
> yolo settings
JSONDict("/home/spepc/.config/Ultralytics/settings.json"):
{
  "settings_version": "0.0.6",
  "datasets_dir": "/home/spepc/lihongtu/dl/train/datasets",
  "weights_dir": "/home/spepc/lihongtu/dl/train/ultralytics--git/weights",
  "runs_dir": "./runs",
  "uuid": "0c48beeafa6ec3f635c3da340286bca7125f47463a2826e1a8efb51a62bce090",
  "sync": true,
  "api_key": "",
  "openai_api_key": "",
  "clearml": true,
  "comet": true,
  "dvc": true,
  "hub": true,
  "mlflow": true,
  "neptune": true,
  "raytune": true,
  "tensorboard": true,
  "wandb": false,
  "vscode_msg": true,
  "openvino_msg": true
}
💡 Learn more about Ultralytics Settings at https://docs.ultralytics.com/quickstart/#ultralytics-settings
```

## yolo copy-cfg

```sh
> yolo copy-cfg
D:\ml\code\yolo26-ultralytics\ultralytics\cfg\default.yaml copied to D:\ml\code\yolo26-ultralytics\default_copy.yaml
Example YOLO command with this new custom cfg:
    yolo cfg='D:\ml\code\yolo26-ultralytics\default_copy.yaml' imgsz=320 batch=8
```

## yolo cfg

```sh
> yolo cfg
Printing '/home/spepc/lihongtu/dl/train/ultralytics--git/ultralytics/cfg/default.yaml'

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
freeze: null
multi_scale: 0.0
compile: false
overlap_mask: true
mask_ratio: 4
dropout: 0.0
val: true
split: val
save_json: false
conf: null
iou: 0.7
max_det: 300
half: false
dnn: false
plots: true
end2end: null
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
simplify: true
opset: null
workspace: null
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
rle: 1.0
angle: 1.0
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
cutmix: 0.0
copy_paste: 0.0
copy_paste_mode: flip
auto_augment: randaugment
erasing: 0.4
cfg: null
tracker: botsort.yaml
```

