# coding:utf-8
import os
from PIL import Image

# bmp 转换为jpg
def ToJpg(file_path, imageFormat):
    for fileName in os.listdir(file_path):

        # 查看结尾类型
        if fileName.endwith(imageFormat):
            # print(fileName)
            newFileName = fileName.split(".")[0]+".jpg"
            print(newFileName)
            img = Image.open(file_path+"/"+fileName)
            img.save(file_path+"/"+newFileName)


# 删除原来的位图
def deleteImages(file_path, imageFormat):
    command = "del "+file_path+"/*."+imageFormat
    os.system(command)


def main():
    file_path = "./VOCdevkit/VOC2007/JPEGImages"
    ToJpg(file_path, "bmp")
    #deleteImages(file_path, "bmp")


if __name__ == '__main__':
    main()