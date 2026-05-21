# 数据集类型转换工具

代码介绍

`fetch_voc.py` 获取 voc 格式的 xml 标注中的类别和数量

`fetch_yolo.py` 获取 yolo 格式的 txt 标注中的类别和数量

`filter_voc.py` 实现 voc 格式的 xml 标注的类别过滤以及类别重命名操作

`filter_yolo.py` 实现 yolo 格式的 txt 标注的类别过滤以及类别重命名操作

`sample_voc.py` 实现 voc 格式的数据集的随机采样, 划分训练集和验证集

`sample_yolo.py` 实现 yolo 格式的数据集的随机采样, 划分训练集和验证集

`voc2yolo.py` 实现 voc 格式数据集到 yolo 格式的转换

`yolo2voc.py` 实现 yolo 格式数据集到 voc 格式的转换

# 依赖库

```txt
tqdm
PyYAML
```

# voc 和 yolo 标注格式差异

下面的2个标注是同一张图片的标注, 相对来说 voc 的标注更容易理解, 包含了图片宽高, 每个 box 框的类别名称和左上角和右下角的绝对坐标。

voc 格式

```xml
<annotation>
    <folder>test2007</folder>
    <filename>000001.xml</filename>
    <path>D:\code\datasets\VOC\xmls\test2007\000001.xml</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>353</width>
        <height>500</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>dog</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>47</xmin>
            <ymin>239</ymin>
            <xmax>194</xmax>
            <ymax>370</ymax>
        </bndbox>
    </object>
    <object>
        <name>person</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>7</xmin>
            <ymin>11</ymin>
            <xmax>351</xmax>
            <ymax>497</ymax>
        </bndbox>
    </object>
</annotation>
```

yolo 格式

> 每一行为一个 box 框
>
> 5个数字的含义为 `class center_x center_y width height`
>
> `class` 代表类别 id，还需要额外的文件表示 id 到真是类别的映射
>
> 其中 `center_x center_y width height` 都是相对值, 除以了宽高

```txt
11 0.3413597733711048 0.609 0.4164305949008499 0.262
14 0.5070821529745042 0.508 0.9745042492917847 0.972
```

相比 yolo 格式, voc 格式的标注共容易让人理解，建议使用 xml 格式进行标注，后续转换为 yolo 格式

# 使用方式

这里假设使用 voc 格式的标注作为标准，最终转换为的标注类型为 yolo 格式。

## 1. 获取已有标注的类型

使用 `fetch_voc.py` 脚本获取已有标注的类型，查看标注的数量，每个类别的数量，并生一个可以用于 ultralytics 库训练的 yaml 文件

要修改 `fetch_voc.py`  中 xml 文件所在的目录路径和用于保存的 yaml 文件路径

```python
if __name__ == "__main__":
    # xml 文件所在的目录, 支持多个目录
    xml_dirs = [
        "../VOC/xmls/test2007",
    ]
    # 生成的类别 yaml 文件
    yaml_path = "../VOC/data.yaml"

    fetch_voc(xml_dirs, yaml_path)
```

执行脚本如下

```powershell
Fetch VOC ...
xml_dirs: ['../VOC/xmls/test2007']
output_yaml_path: ../VOC/data.yaml
check val xml files: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4952/4952 [00:00<00:00, 10662.07it/s]
total 4952 xml files, 12032 objects
object counts:
    aeroplane: 285
    bicycle: 337
    bird: 459
    boat: 263
    bottle: 469
    bus: 213
    car: 1201
    cat: 358
    chair: 756
    cow: 244
    diningtable: 206
    dog: 489
    horse: 348
    motorbike: 325
    person: 4528
    pottedplant: 480
    sheep: 242
    sofa: 239
    train: 282
    tvmonitor: 308
save yaml config to: ..\VOC\data.yaml
```

生成的 yaml 文件，包含 names 和 id 的映射和统计信息，值得注意的是，这个文件里面只有 names, 缺少指定的训练和验证的图片的路径，这个后续会介绍

```yaml
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
statistics:
  total_files: 4952
  total_objects: 12032
  counts:
    aeroplane: 285
    bicycle: 337
    bird: 459
    boat: 263
    bottle: 469
    bus: 213
    car: 1201
    cat: 358
    chair: 756
    cow: 244
    diningtable: 206
    dog: 489
    horse: 348
    motorbike: 325
    person: 4528
    pottedplant: 480
    sheep: 242
    sofa: 239
    train: 282
    tvmonitor: 308
```

## 2. 过滤数据（重命名类别，可选）

过滤数据的目的是将已有的数据中不需要的数据过滤掉, 并且将原本的数据集中的类别改名, 比如将 cat、dog 等全部改为 pet 类别。

要修改 `filter_voc.py`  中原本 xml 和图片路径、新的保存路径、步骤1生成的 yaml 文件路径、保留的类别名称（以下示例使用前一半的类别）、类别的重映射（可选, 下面使用和原本类别的名称）。

```python
if __name__ == "__main__":
    # 原本 xml 文件路径, 支持多个目录
    xml_dirs = [
        "../VOC/xmls/test2007",
    ]
    # 原本图片文件路径, 支持多个目录, 但是要和 xml_dirs 一一匹配
    image_dirs = [
        "../VOC/images/test2007",
    ]
    # 过滤后的 xmls 和 images 的存放路径, 里面会有 xmls 和 images 文件夹, 用来存放全部过滤后的数据
    filtered_save_dir = "../VOC/test2007--filtered--voc-format"
    # 对应的 yaml 文件路径(不是必须, 当前主要目的是获取类别名称)
    yaml_path = "../VOC/data.yaml"

    names = load_names_from_yaml(yaml_path)

    # 保留的类别名, 这里保留前一半类别
    keep_names = names[: len(names) // 2]

    # 类别的重映射
    name_remap = {i: i for i in keep_names}

    filter_voc(xml_dirs, image_dirs, filtered_save_dir, keep_names, name_remap)
```

执行脚本如下

```powershell
> python filter_voc.py 
Filter VOC dataset by keep_names...
xml_dirs: ['../VOC/xmls/test2007']
image_dirs: ['../VOC/images/test2007']
filtered_save_dir: ../VOC/test2007--filtered--voc-format
keep_names: ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow']
name_remap: {'aeroplane': 'aeroplane', 'bicycle': 'bicycle', 'bird': 'bird', 'boat': 'boat', 'bottle': 'bottle', 'bus': 'bus', 'car': 'car', 'cat': 'cat', 'chair': 'chair', 'cow': 'cow'}
filter xml files: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4952/4952 [00:18<00:00, 273.10it/s]
total 4952 xml files, total 12032 objects, filtered 2729 xml files, filtered 4585 objects.
object counts:
    aeroplane: 285
    bicycle: 337
    bird: 459
    boat: 263
    bottle: 469
    bus: 213
    car: 1201
    cat: 358
    chair: 756
    cow: 244
save yaml config to ..\VOC\test2007--filtered--voc-format\filtered.yaml
```

执行完成后保存的文件夹结构为

```yaml
test2007--filtered
├─images           # 过滤后的图片
├─xmls             # 过滤后的 xml 文件
└─data.yaml        # 生成的配置文件
```

下面是生成的 yaml 文件，包含 name 和统计信息，值得注意的是，这个文件里面只有 names，缺少指定的训练和验证的图片的路径, 这个后续会介绍

```yaml
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
statistics:
  total_files: 4952
  total_objects: 12032
  filtered_files: 2729
  filtered_objects: 4585
  filtered_counts:
    aeroplane: 285
    bicycle: 337
    bird: 459
    boat: 263
    bottle: 469
    bus: 213
    car: 1201
    cat: 358
    chair: 756
    cow: 244
```

## 3. 划分为训练集和测试集（可选）

要修改 `sample_voc.py`  中的原本 xml 文件路径、原本图片文件路径、保存划分后数据集的路径、验证集占比(可选)、划分数据集时每个类别的最小数量(可选)、随机种子(可选)

```python
#     sample_voc(xml_dirs, image_dirs, sample_dir, val_percent, object_min_num, seed)
if __name__ == "__main__":
    # 原本 xml 文件路径
    xml_dirs = [
        "../VOC/test2007--filtered--voc-format/xmls",
    ]
    # 原本图片文件路径
    image_dirs = [
        "../VOC/test2007--filtered--voc-format/images",
    ]
    # 采样后的路径, 包含 train 和 val 两个文件夹, 以及对应的 xmls 和 images 文件夹, 用来存放全部采样后的数据
    sample_dir = "../VOC/test2007--filtered--voc-format--sample--voc"
    # 验证集占比
    val_percent = 0.1
    # 划分数据集时每个类别的最小数量, 如果数据集太少不一定能保证, 需要调整这个值
    object_min_num = 10
    # 随机种子, 保证可以复现, None 代表不设置
    seed = None

    sample_voc(
        xml_dirs, image_dirs, sample_dir, val_percent, object_min_num, seed
    )
```

执行脚本如下

```powershell
> python sample_voc.py
Sample VOC dataset...
xml_dirs: ['../VOC/test2007--filtered--voc-format/xmls']
image_dirs: ['../VOC/test2007--filtered--voc-format/images']
sample_dir: ../VOC/test2007--filtered--voc-format--sample--voc
val_percent: 0.1
object_min_num: 10
seed: None
Save val images to ..\VOC\test2007--filtered--voc-format--sample--voc\val\images
Save val xmls to ..\VOC\test2007--filtered--voc-format--sample--voc\val\xmls
Save train images to ..\VOC\test2007--filtered--voc-format--sample--voc\train\images
Save train xmls to ..\VOC\test2007--filtered--voc-format--sample--voc\train\xmls
sample iteration 1 ...
check val xml files: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 273/273 [00:00<00:00, 9790.73it/s]
val total 273 xml files, 475 objects
val object counts:
    aeroplane: 31
    bicycle: 28
    bird: 65
    boat: 30
    bottle: 37
    bus: 37
    car: 133
    cat: 37
    chair: 53
    cow: 24
check train xml files: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2456/2456 [00:00<00:00, 9201.03it/s] 
train total 2456 xml files, 4110 objects
train object counts:
    aeroplane: 254
    bicycle: 309
    bird: 394
    boat: 233
    bottle: 432
    bus: 176
    car: 1068
    cat: 321
    chair: 703
    cow: 220
save yaml config to ..\VOC\test2007--filtered--voc-format--sample--voc\data.yaml
move val xml and image files: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 273/273 [00:00<00:00, 1034.08it/s] 
move train xml and image files: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2456/2456 [00:04<00:00, 590.89it/s]
```

移动后的文件夹格式如下, 含义如注释所示

```txt
test2007--filtered--voc-format--sample--voc
├─train
│  ├─images    # 训练图片
│  └─xmls      # 训练标签, 需要转换为 yolo 格式
└─val
│  ├─images    # 验证图片
│  └─xmls      # 验证标签, 需要转换为 yolo 格式
└─data.yaml    # 新生成的 config
```

同时会生成 data.yaml，包含名称和统计数据，这个配置可以用来训练模型，但是还需要后面的步骤将 voc 格式的注释转换为 yolo 格式的注释

> train 和 val 中只填写了 image 的路径，而没有 labels 的路径，是因为 ultralytics 库会自动根据这个路径查找标签路径，具体查找方式是将路径中最后面的 images 替换为 labels，labels 路径就是存放标签的路径，labels 文件夹会在第四步生成

实际训练时要将 path 路径改为真实路径

```yaml
path: test2007--filtered--voc-format--sample--voc
train:
- train/images
val:
- val/images
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
statistics:
  train_files: 2456
  train_objects: 4110
  train_counts:
    aeroplane: 254
    bicycle: 309
    bird: 394
    boat: 233
    bottle: 432
    bus: 176
    car: 1068
    cat: 321
    chair: 703
    cow: 220
  val_files: 273
  val_objects: 475
  val_counts:
    aeroplane: 31
    bicycle: 28
    bird: 65
    boat: 30
    bottle: 37
    bus: 37
    car: 133
    cat: 37
    chair: 53
    cow: 24
```

## 4. 将 xml 转换为 yolo 格式

上面我们将数据集划分为了测试集和验证集，因此需要执行2次格式转换

修改原本的 xml 文件夹、原本图片文件夹（用于获取图片宽高，xml中的宽高可能不正确）、新的 txt 文件夹、yaml 配置文件路径

```python
if __name__ == "__main__":
    # 原本的 xml 文件夹
    xml_dirs = [
        "../VOC/test2007--filtered--voc-format--sample--voc/train/xmls",
    ]
    # 原本图片文件夹
    image_dirs = [
        "../VOC/test2007--filtered--voc-format--sample--voc/train/images",
    ]
    # 新的 txt 文件夹, 会将全部的转换后的 txt 文件放到这个文件夹下
    new_txt_dir = "../VOC/test2007--filtered--voc-format--sample--voc/train/labels"
    # yaml 配置路径
    yaml_path = "../VOC/test2007--filtered--voc-format--sample--voc/data.yaml"
    name2id = load_name2id_from_yaml(yaml_path)
    # 新的图片文件夹, 会把全部图片放在这个文件夹下, 如果为 None 则不复制图片
    new_image_dir = None

    voc2yolo(xml_dirs, image_dirs, new_txt_dir, name2id, new_image_dir)
```

执行脚本如下

```powershell
> python voc2yolo.py
Converting VOC to YOLO...
xml_dirs: ['../VOC/test2007--filtered--voc-format--sample--voc/train/xmls']
image_dirs: ['../VOC/test2007--filtered--voc-format--sample--voc/train/images']
new_txt_dir: ../VOC/test2007--filtered--voc-format--sample--voc/train/labels
new_image_dir: None
name2id: {'aeroplane': 0, 'bicycle': 1, 'bird': 2, 'boat': 3, 'bottle': 4, 'bus': 5, 'car': 6, 'cat': 7, 'chair': 8, 'cow': 9}
convert xml to txt: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2456/2456 [00:01<00:00, 1384.02it/s]
```

调整验证集式

```python
if __name__ == "__main__":
    # 原本的 xml 文件夹
    xml_dirs = [
        "../VOC/test2007--filtered--voc-format--sample--voc/val/xmls",
    ]
    # 原本图片文件夹
    image_dirs = [
        "../VOC/test2007--filtered--voc-format--sample--voc/val/images",
    ]
    # 新的 txt 文件夹
    new_txt_dir = "../VOC/test2007--filtered--voc-format--sample--voc/val/labels"
    # yaml 配置
    yaml_path = "../VOC/test2007--filtered--voc-format--sample--voc/data.yaml"
    name2id = load_name2id_from_yaml(yaml_path)
    # 新的图片文件夹, 如果为 None 则不复制图片
    new_image_dir = None

    voc2yolo(xml_dirs, image_dirs, new_txt_dir, name2id, new_image_dir)
```

执行脚本如下

```powershell
> python voc2yolo.py
Converting VOC to YOLO...
xml_dirs: ['../VOC/test2007--filtered--voc-format--sample--voc/val/xmls']
image_dirs: ['../VOC/test2007--filtered--voc-format--sample--voc/val/images']
new_txt_dir: ../VOC/test2007--filtered--voc-format--sample--voc/val/labels
new_image_dir: None
name2id: {'aeroplane': 0, 'bicycle': 1, 'bird': 2, 'boat': 3, 'bottle': 4, 'bus': 5, 'car': 6, 'cat': 7, 'chair': 8, 'cow': 9}
convert xml to txt: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 273/273 [00:00<00:00, 816.69it/s]
```

最终生成的文件夹格式如下，这个文件夹就能够拿来训练模型了

```txt
test2007--filtered--sample--voc
├─train
│  ├─images    # 训练图片
│  ├─labels    # 训练标签, yolo 格式
│  └─xmls      # 训练标签, 需要转换为 yolo 格式
└─val
│  ├─images    # 验证图片
│  ├─labels    # 验证标签, yolo 格式
│  └─xmls      # 验证标签, 需要转换为 yolo 格式
└─data.yaml    # 生成的 config
```

data.yaml 在这个步骤并没有改变，还是第3步的生成的

> train 和 val 中只填写了 image 的路径，而没有 labels 的路径，是因为 ultralytics 库会自动根据这个路径查找标签路径，具体查找方式是将路径中最后面的 images 替换为 labels，labels 路径就是存放标签的路径

> 如果不执行上面的第三步，就不会有 train 和 val 文件夹的内容，需要自己添加，只需要填写对应的 images 路径即可

实际训练时要将 path 路径改为真实路径

```yaml
path: test2007--filtered--voc-format--sample--voc
train:
- train/images
val:
- val/images
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
statistics:
  train_files: 2456
  train_objects: 4110
  train_counts:
    aeroplane: 254
    bicycle: 309
    bird: 394
    boat: 233
    bottle: 432
    bus: 176
    car: 1068
    cat: 321
    chair: 703
    cow: 220
  val_files: 273
  val_objects: 475
  val_counts:
    aeroplane: 31
    bicycle: 28
    bird: 65
    boat: 30
    bottle: 37
    bus: 37
    car: 133
    cat: 37
    chair: 53
    cow: 24
```

# 路径注意事项

注意最终的图片文件夹路径中一定有 images，txt 文件夹中的路径一定有 labels，下面的2种路径是正确的

## 路径方式1

```
VOC
├─train
│  ├─images    # 训练图片
│  ├─labels    # 训练标签, yolo 格式
└─val
   ├─images    # 验证图片
   ├─labels    # 验证标签, yolo 格式
```

对应的 yaml

```yaml
train:
- VOC\train\images
val:
- VOC\val\images
```

## 路径方式2

```txt
VOC
├─images
│  ├─train    # 训练图片
│  ├─val      # 验证图片
└─labels
   ├─train    # 训练标签
   ├─val      # 验证标签
```

对应的 yaml

```yaml
train:
- VOC\images\train
val:
- VOC\images\val
```

# 合并不同的数据集

建议的步骤是，分别对不同的数据集执行上面的 1、2 两步，然后获得不同数据集过滤得到的数据集和配置文件，之后需要手动合并数据集的图片和 xml 文件夹

配置文件是否需要合并取决于是否使用划分训练集和验证集的功能，如果使用这个功能，则不需要手动合并配置文件，因为划分训练集和验证集的功能会生成新的配置文件，否则就需要手动合并配置文件，合并方式如下

比如数据集A的配置如下

```yaml
names:
  0: aeroplane
  1: bicycle
  2: bird
```

比如数据集B的配置如下

```yaml
names:
  0: boat
  1: bottle
  2: bus
```

手动合并后的数据集如下，names 的顺序无所谓，只要数字连续递增即可

```yaml
names:
  0: aeroplane
  1: bicycle
  2: bird
  3: boat
  4: bottle
  5: bus
```

然后拿合并好的图片、xml、配置文件执行后面的3、4步骤即可（或者拿合并好的数据再从1开始跑也可以，这样就不需要手动合并配置了）

