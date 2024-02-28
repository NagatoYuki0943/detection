import numpy as np

#-----------------------------------------------------------#
#   计算宽高IOU
#-----------------------------------------------------------#
def wh_iou(wh1, wh2):
    """
    wh1 wh2全是真实框的宽高 [N,2] N代表个数, 2代表wh
    """
    # Returns the nxm IoU matrix. wh1 is nx2, wh2 is mx2
    wh1 = wh1[:, None]  # [N,2] => [N,1,2]  None扩展维度 中间插入维度   维度为1可以进行广播
    wh2 = wh2[None]     # [M,2] => [1,M,2]  最前面插入维度

    #-----------------------------------------------------------#
    #   找最小值，相当左上角重叠，找最小的右下角坐标，最后求乘积
    #-----------------------------------------------------------#
    inter = np.minimum(wh1, wh2).prod(2)  # [N,M]
    return inter / (wh1.prod(2) + wh2.prod(2) - inter)  # iou = inter / (area1 + area2 - inter)


#-----------------------------------------------------------#
#   计算kmeans
#-----------------------------------------------------------#
def k_means(boxes, k, dist=np.median):
    """
    yolo k-means methods
    refer: https://github.com/qqwweee/keras-yolo3/blob/master/kmeans.py
    Args:
        boxes: 需要聚类的bboxes [N,2] N代表个数, 2代表wh
        k: 簇数(聚成几类)
        dist: 更新簇坐标的方法(默认使用中位数，比均值效果略好)
    """
    # box个数
    box_number = boxes.shape[0]
    # 用来当做box聚类结果
    last_nearest = np.zeros((box_number,))
    # np.random.seed(0)  # 固定随机数种子

    #-----------------------------------------------------------#
    #   随机选择k个作为中心 init k clusters
    #   replace=False 数据不会有重复
    #-----------------------------------------------------------#
    clusters = boxes[np.random.choice(box_number, k, replace=False)]

    while True:
        #-----------------------------------------------------------#
        #   计算距离所有boxes和中心的距离
        #   1 - IOU 不使用欧式距离
        #-----------------------------------------------------------#
        distances = 1 - wh_iou(boxes, clusters)
        #-----------------------------------------------------------#
        #   找最近距离的索引,表示被划分到哪一个簇中了
        #-----------------------------------------------------------#
        current_nearest = np.argmin(distances, axis=1)
        #-----------------------------------------------------------#
        #   上一次聚类结果和这一次聚类结果完全相等,就暂计算
        #-----------------------------------------------------------#
        if (last_nearest == current_nearest).all():
            break  # clusters won't change
        #-----------------------------------------------------------#
        #   根据簇数进行更新
        #-----------------------------------------------------------#
        for cluster in range(k):
            # update clusters
            clusters[cluster] = dist(boxes[current_nearest == cluster], axis=0)

        # 存储聚类结果
        last_nearest = current_nearest

    return clusters
