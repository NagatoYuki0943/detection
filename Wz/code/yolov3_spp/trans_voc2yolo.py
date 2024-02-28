"""
���ű����������ܣ�
1.��voc���ݼ���ע��Ϣ(.xml)תΪyolo��ע��ʽ(.txt)������ͼ���ļ����Ƶ���Ӧ�ļ���
2.����json��ǩ�ļ������ɶ�Ӧnames��ǩ(my_data_label.names)
"""
import os
from tqdm import tqdm
from lxml import etree
import json
import shutil


# voc���ݼ���Ŀ¼�Լ��汾
voc_root = "/data/VOCdevkit"
voc_version = "VOC2012"

# ת����ѵ�����Լ���֤����Ӧtxt�ļ�
train_txt = "train.txt"
val_txt = "val.txt"

# ת������ļ�����Ŀ¼
save_file_root = "./my_yolo_dataset"

# label��ǩ��Ӧjson�ļ�
label_json_path = './data/pascal_voc_classes.json'

# ƴ�ӳ�voc��imagesĿ¼��xmlĿ¼��txtĿ¼
voc_images_path = os.path.join(voc_root, voc_version, "JPEGImages")
voc_xml_path = os.path.join(voc_root, voc_version, "Annotations")
train_txt_path = os.path.join(voc_root, voc_version, "ImageSets", "Main", train_txt)
val_txt_path = os.path.join(voc_root, voc_version, "ImageSets", "Main", val_txt)

# ����ļ�/�ļ��ж��Ƿ����
assert os.path.exists(voc_images_path), "VOC images path not exist..."
assert os.path.exists(voc_xml_path), "VOC xml path not exist..."
assert os.path.exists(train_txt_path), "VOC train txt file not exist..."
assert os.path.exists(val_txt_path), "VOC val txt file not exist..."
assert os.path.exists(label_json_path), "label_json_path does not exist..."
if os.path.exists(save_file_root) is False:
    os.makedirs(save_file_root)


def parse_xml_to_dict(xml):
    """
    ��xml�ļ��������ֵ���ʽ���ο�tensorflow��recursive_parse_xml_to_dict
    Args��
        xml: xml tree obtained by parsing XML file contents using lxml.etree

    Returns:
        Python dictionary holding XML contents.
    """

    if len(xml) == 0:  # �������ײ㣬ֱ�ӷ���tag��Ӧ����Ϣ
        return {xml.tag: xml.text}

    result = {}
    for child in xml:
        child_result = parse_xml_to_dict(child)  # �ݹ������ǩ��Ϣ
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:  # ��Ϊobject�����ж����������Ҫ�����б���
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}


def translate_info(file_names: list, save_root: str, class_dict: dict, train_val='train'):
    """
    ����Ӧxml�ļ���ϢתΪyolo��ʹ�õ�txt�ļ���Ϣ
    :param file_names:
    :param save_root:
    :param class_dict:
    :param train_val:
    :return:
    """
    save_txt_path = os.path.join(save_root, train_val, "labels")
    if os.path.exists(save_txt_path) is False:
        os.makedirs(save_txt_path)
    save_images_path = os.path.join(save_root, train_val, "images")
    if os.path.exists(save_images_path) is False:
        os.makedirs(save_images_path)

    for file in tqdm(file_names, desc="translate {} file...".format(train_val)):
        # �����ͼ���ļ��Ƿ����
        img_path = os.path.join(voc_images_path, file + ".jpg")
        assert os.path.exists(img_path), "file:{} not exist...".format(img_path)

        # ���xml�ļ��Ƿ����
        xml_path = os.path.join(voc_xml_path, file + ".xml")
        assert os.path.exists(xml_path), "file:{} not exist...".format(xml_path)

        # read xml
        with open(xml_path) as fid:
            xml_str = fid.read()
        xml = etree.fromstring(xml_str)
        data = parse_xml_to_dict(xml)["annotation"]
        img_height = int(data["size"]["height"])
        img_width = int(data["size"]["width"])

        # write object info into txt
        assert "object" in data.keys(), "file: '{}' lack of object key.".format(xml_path)
        if len(data["object"]) == 0:
            # ���xml�ļ���û��Ŀ���ֱ�Ӻ��Ը�����
            print("Warning: in '{}' xml, there are no objects.".format(xml_path))
            continue

        with open(os.path.join(save_txt_path, file + ".txt"), "w") as f:
            for index, obj in enumerate(data["object"]):
                # ��ȡÿ��object��box��Ϣ
                xmin = float(obj["bndbox"]["xmin"])
                xmax = float(obj["bndbox"]["xmax"])
                ymin = float(obj["bndbox"]["ymin"])
                ymax = float(obj["bndbox"]["ymax"])
                class_name = obj["name"]
                class_index = class_dict[class_name] - 1  # Ŀ��id��0��ʼ

                # ��һ��������ݣ��еı�ע��Ϣ�п�����w��hΪ0����������������ݻᵼ�¼���ع�lossΪnan
                if xmax <= xmin or ymax <= ymin:
                    print("Warning: in '{}' xml, there are some bbox w/h <=0".format(xml_path))
                    continue

                # ��box��Ϣת����yolo��ʽ
                xcenter = xmin + (xmax - xmin) / 2
                ycenter = ymin + (ymax - ymin) / 2
                w = xmax - xmin
                h = ymax - ymin

                # ��������ת������꣬����6λС��
                xcenter = round(xcenter / img_width, 6)
                ycenter = round(ycenter / img_height, 6)
                w = round(w / img_width, 6)
                h = round(h / img_height, 6)

                info = [str(i) for i in [class_index, xcenter, ycenter, w, h]]

                if index == 0:
                    f.write(" ".join(info))
                else:
                    f.write("\n" + " ".join(info))

        # copy image into save_images_path
        path_copy_to = os.path.join(save_images_path, img_path.split(os.sep)[-1])
        if os.path.exists(path_copy_to) is False:
            shutil.copyfile(img_path, path_copy_to)


def create_class_names(class_dict: dict):
    keys = class_dict.keys()
    with open("./data/my_data_label.names", "w") as w:
        for index, k in enumerate(keys):
            if index + 1 == len(keys):
                w.write(k)
            else:
                w.write(k + "\n")


def main():
    # read class_indict
    json_file = open(label_json_path, 'r')
    class_dict = json.load(json_file)

    # ��ȡtrain.txt�е���������Ϣ��ɾ������
    with open(train_txt_path, "r") as r:
        train_file_names = [i for i in r.read().splitlines() if len(i.strip()) > 0]
    # voc��Ϣתyolo������ͼ���ļ����Ƶ���Ӧ�ļ���
    translate_info(train_file_names, save_file_root, class_dict, "train")

    # ��ȡval.txt�е���������Ϣ��ɾ������
    with open(val_txt_path, "r") as r:
        val_file_names = [i for i in r.read().splitlines() if len(i.strip()) > 0]
    # voc��Ϣתyolo������ͼ���ļ����Ƶ���Ӧ�ļ���
    translate_info(val_file_names, save_file_root, class_dict, "val")

    # ����my_data_label.names�ļ�
    create_class_names(class_dict)


if __name__ == "__main__":
    main()
