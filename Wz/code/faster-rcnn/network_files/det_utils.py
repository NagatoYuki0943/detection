import torch
import math
from typing import List, Tuple
from torch import Tensor

#---------------------------------------------------#
#   按照给定的batch_size_per_image, positive_fraction选择正负样本
#---------------------------------------------------#
class BalancedPositiveNegativeSampler(object):
    """
    This class samples batches, ensuring that they contain a fixed proportion of positives
    """

    def __init__(self, batch_size_per_image, positive_fraction):
        # type: (int, float) -> None
        """
        Arguments:
            batch_size_per_image (int): number of elements to be selected per image
            positive_fraction (float): percentage of positive elements per batch
        """
        self.batch_size_per_image = batch_size_per_image
        self.positive_fraction = positive_fraction

    def __call__(self, matched_idxs):
        # type: (List[Tensor]) -> Tuple[List[Tensor], List[Tensor]]
        """
        Arguments:
            matched idxs: list of tensors containing -1, 0 or positive values.
                Each tensor corresponds to a specific image.
                -1 values are ignored, 0 are considered as negatives and > 0 as
                positives.

        Returns:
            pos_idx (list[tensor])
            neg_idx (list[tensor])

        Returns two lists of binary masks for each image.
        The first list contains the positive elements that were selected,
        and the second list the negative example.
        """
        pos_idx = []
        neg_idx = []
        #---------------------------------------------------#
        #   遍历每张图像的matched_idxs
        #---------------------------------------------------#
        for matched_idxs_per_image in matched_idxs:
            #---------------------------------------------------#
            #   >= 1的为正样本, nonzero返回非零元素索引
            #---------------------------------------------------#
            # positive = torch.nonzero(matched_idxs_per_image >= 1).squeeze(1)
            positive = torch.where(torch.ge(matched_idxs_per_image, 1))[0]
            # = 0的为负样本
            # negative = torch.nonzero(matched_idxs_per_image == 0).squeeze(1)
            negative = torch.where(torch.eq(matched_idxs_per_image, 0))[0]

            #---------------------------------------------------#
            # 指定正样本的数量
            #---------------------------------------------------#
            num_pos = int(self.batch_size_per_image * self.positive_fraction)
            # protect against not enough positive examples
            # 如果正样本数量不够就直接采用所有正样本
            num_pos = min(positive.numel(), num_pos)
            # 指定负样本数量 = 总样本个数- 正样本个数
            num_neg = self.batch_size_per_image - num_pos
            # protect against not enough negative examples
            # 如果负样本数量不够就直接采用所有负样本
            num_neg = min(negative.numel(), num_neg)

            # randomly select positive and negative examples
            # Returns a random permutation of integers from 0 to n - 1. 随机排序数字,不重复
            # 随机选择指定数量的正负样本,取前n个作为索引
            perm1 = torch.randperm(positive.numel(), device=positive.device)[:num_pos]
            perm2 = torch.randperm(negative.numel(), device=negative.device)[:num_neg]

            #---------------------------------------------------#
            #   通过索引获取数据
            #---------------------------------------------------#
            pos_idx_per_image = positive[perm1]
            neg_idx_per_image = negative[perm2]

            #---------------------------------------------------#
            #   创建蒙版,正样本和负样本
            #---------------------------------------------------#
            pos_idx_per_image_mask = torch.zeros_like(
                matched_idxs_per_image, dtype=torch.uint8
            )
            neg_idx_per_image_mask = torch.zeros_like(
                matched_idxs_per_image, dtype=torch.uint8
            )
            #---------------------------------------------------#
            #   正样本对应位置全设为1,负样本也一样
            #---------------------------------------------------#
            pos_idx_per_image_mask[pos_idx_per_image] = 1
            neg_idx_per_image_mask[neg_idx_per_image] = 1

            pos_idx.append(pos_idx_per_image_mask)
            neg_idx.append(neg_idx_per_image_mask)

        return pos_idx, neg_idx


#---------------------------------------------------#
#   真实框求计算参数
#   真实框求相对于预测值的值(用来求loss)
#   中心参数 = (真实坐标 - 先验框坐标) / 先验框宽高
#   宽高参数 = ln(真实宽高 / 先验框宽高)
#   求出来的参数和预测结果进行loss计算
#---------------------------------------------------#
@torch.jit._script_if_tracing
def encode_boxes(reference_boxes, proposals, weights):
    # type: (torch.Tensor, torch.Tensor, torch.Tensor) -> torch.Tensor
    """
    Encode a set of proposals with respect to some
    reference boxes

    Arguments:
        reference_boxes (Tensor): reference boxes(gt)    先验框
        proposals (Tensor): boxes to be encoded(anchors) 预测框
        weights:
    """

    # perform some unpacking to make it JIT-fusion friendly
    wx = weights[0]
    wy = weights[1]
    ww = weights[2]
    wh = weights[3]

    # 先验框 左上右下坐标
    proposals_x1 = proposals[:, 0].unsqueeze(1)
    proposals_y1 = proposals[:, 1].unsqueeze(1)
    proposals_x2 = proposals[:, 2].unsqueeze(1)
    proposals_y2 = proposals[:, 3].unsqueeze(1)

    # 真实框 左上右下坐标
    reference_boxes_x1 = reference_boxes[:, 0].unsqueeze(1)
    reference_boxes_y1 = reference_boxes[:, 1].unsqueeze(1)
    reference_boxes_x2 = reference_boxes[:, 2].unsqueeze(1)
    reference_boxes_y2 = reference_boxes[:, 3].unsqueeze(1)

    # 左上右下坐标 -> 中心宽高
    ex_widths = proposals_x2 - proposals_x1
    ex_heights = proposals_y2 - proposals_y1
    # parse coordinate of center point
    ex_ctr_x = proposals_x1 + 0.5 * ex_widths
    ex_ctr_y = proposals_y1 + 0.5 * ex_heights

    gt_widths = reference_boxes_x2 - reference_boxes_x1
    gt_heights = reference_boxes_y2 - reference_boxes_y1
    gt_ctr_x = reference_boxes_x1 + 0.5 * gt_widths
    gt_ctr_y = reference_boxes_y1 + 0.5 * gt_heights

    #---------------------------------------------------#
    #   真实框求相对于预测值的值(用来求loss)
    #   中心参数 = (真实坐标 - 先验框坐标) / 先验框宽高
    #   宽高参数 = ln(真实宽高 / 先验框宽高)
    #   求出来的参数和预测结果进行loss计算
    #---------------------------------------------------#
    #            权重为1,不用管
    targets_dx = wx * (gt_ctr_x - ex_ctr_x) / ex_widths
    targets_dy = wy * (gt_ctr_y - ex_ctr_y) / ex_heights
    targets_dw = ww * torch.log(gt_widths / ex_widths)
    targets_dh = wh * torch.log(gt_heights / ex_heights)

    # 中心,宽高参数
    targets = torch.cat((targets_dx, targets_dy, targets_dw, targets_dh), dim=1)
    return targets

#---------------------------------------------------#
#   将预测的bbox regression参数应用到anchors上得到最终预测bbox坐标
#---------------------------------------------------#
class BoxCoder(object):
    """
    This class encodes and decodes a set of bounding boxes into
    the representation used for training the regressors.
    """

    def __init__(self, weights, bbox_xform_clip=math.log(1000. / 16)):
        # type: (Tuple[float, float, float, float], float) -> None
        """
        Arguments:
            weights (4-element tuple)
            bbox_xform_clip (float)
        """
        self.weights = weights
        self.bbox_xform_clip = bbox_xform_clip

    #---------------------------------------------------#
    #   结合anchors和与之对应的真实框gt计算regression参数
    #---------------------------------------------------#
    def encode(self, reference_boxes, proposals):
        # type: (List[Tensor], List[Tensor]) -> List[Tensor]
        """
        结合anchors和与之对应的gt计算regression参数
        Args:
            reference_boxes: List[Tensor] 每个proposal/anchor对应的gt_boxes
            proposals: List[Tensor] anchors/proposals

        Returns: regression parameters
        """
        #---------------------------------------------------#
        #   统计每张图像的anchors个数，方便后面拼接在一起处理后在分开
        #   reference_boxes和proposal数据结构相同
        #---------------------------------------------------#
        boxes_per_image = [len(b) for b in reference_boxes]
        reference_boxes = torch.cat(reference_boxes, dim=0)
        proposals = torch.cat(proposals, dim=0) # 在0维度上拼接

        #---------------------------------------------------#
        #   真实框回归参数
        #   x, y, w, h
        #---------------------------------------------------#
        targets = self.encode_single(reference_boxes, proposals)
        return targets.split(boxes_per_image, 0)


    def encode_single(self, reference_boxes, proposals):
        """
        Encode a set of proposals with respect to some
        reference boxes

        Arguments:
            reference_boxes (Tensor): reference boxes
            proposals (Tensor): boxes to be encoded
        """
        dtype = reference_boxes.dtype
        device = reference_boxes.device
        weights = torch.as_tensor(self.weights, dtype=dtype, device=device)
        targets = encode_boxes(reference_boxes, proposals, weights)

        return targets

    #---------------------------------------------------#
    #   将预测的bbox regression参数应用到anchors上得到最终预测bbox坐标
    #---------------------------------------------------#
    def decode(self, rel_codes, boxes):
        # type: (Tensor, List[Tensor]) -> Tensor
        """

        Args:
            rel_codes: bbox regression parameters
            boxes: anchors/proposals

        Returns:

        """
        assert isinstance(boxes, (list, tuple))
        assert isinstance(rel_codes, torch.Tensor)
        #---------------------------------------------------#
        #   统计每张图像的anchors个数，方便后面拼接在一起处理后在分开
        #---------------------------------------------------#
        boxes_per_image = [b.size(0) for b in boxes]
        concat_boxes = torch.cat(boxes, dim=0)

        # 求sum总数
        box_sum = 0
        for val in boxes_per_image:
            box_sum += val

        #---------------------------------------------------#
        #   将预测的bbox回归参数应用到对应anchors上得到预测bbox的坐标
        #---------------------------------------------------#
        pred_boxes = self.decode_single(
            rel_codes, concat_boxes
        )

        # 防止pred_boxes为空时导致reshape报错
        if box_sum > 0:
            pred_boxes = pred_boxes.reshape(box_sum, -1, 4) # [b, 4] -> [b, 1, 4]

        return pred_boxes


    #---------------------------------------------------#
    #   将预测的bbox回归参数应用到对应anchors上得到预测bbox的坐标
    #---------------------------------------------------#
    def decode_single(self, rel_codes, boxes):
        """
        From a set of original boxes and encoded relative box offsets,
        get the decoded boxes.

        Arguments:
            rel_codes (Tensor): encoded boxes (bbox regression parameters)
            boxes (Tensor): reference boxes (anchors/proposals)
        """
        boxes = boxes.to(rel_codes.dtype)

        # 先验框 xmin, ymin, xmax, ymax
        widths  = boxes[:, 2] - boxes[:, 0]    # anchor/proposal宽度
        heights = boxes[:, 3] - boxes[:, 1]    # anchor/proposal高度
        ctr_x   = boxes[:, 0] + 0.5 * widths   # anchor/proposal中心x坐标
        ctr_y   = boxes[:, 1] + 0.5 * heights  # anchor/proposal中心y坐标


        # 回归参数
        wx, wy, ww, wh = self.weights  # RPN中为[1,1,1,1], fastrcnn中为[10,10,5,5]
        dx = rel_codes[:, 0::4] / wx   # 预测anchors/proposals的中心坐标x回归参数   0::4 获取的是2个维度  0 获取的是1个维度
        dy = rel_codes[:, 1::4] / wy   # 预测anchors/proposals的中心坐标y回归参数
        dw = rel_codes[:, 2::4] / ww   # 预测anchors/proposals的宽度回归参数
        dh = rel_codes[:, 3::4] / wh   # 预测anchors/proposals的高度回归参数

        #---------------------------------------------------#
        #   clamp 限制数值上下限
        #   limit max value, prevent sending too large values into torch.exp()
        #   self.bbox_xform_clip=math.log(1000. / 16)   4.135
        #---------------------------------------------------#
        dw = torch.clamp(dw, max=self.bbox_xform_clip)
        dh = torch.clamp(dh, max=self.bbox_xform_clip)

        #---------------------------------------------------#
        #   预测值调整先验框
        #       中心调整: 原始坐标 + 预测结果 * 原始宽高 = 最终坐标
        #       宽高调整: 原始宽高 * e^预测结果 = 最终宽高
        #   None 增加1个维度
        #---------------------------------------------------#
        pred_ctr_x = dx * widths[:, None] + ctr_x[:, None]
        pred_ctr_y = dy * heights[:, None] + ctr_y[:, None]
        pred_w = torch.exp(dw) * widths[:, None]
        pred_h = torch.exp(dh) * heights[:, None]

        #---------------------------------------------------#
        #   调整后的参数转换为左上角右下角模式
        #---------------------------------------------------#
        # xmin
        pred_boxes1 = pred_ctr_x - torch.tensor(0.5, dtype=pred_ctr_x.dtype, device=pred_w.device) * pred_w # center_x - 0.5 * w
        # ymin
        pred_boxes2 = pred_ctr_y - torch.tensor(0.5, dtype=pred_ctr_y.dtype, device=pred_h.device) * pred_h # center_y - 0.5 * h
        # xmax
        pred_boxes3 = pred_ctr_x + torch.tensor(0.5, dtype=pred_ctr_x.dtype, device=pred_w.device) * pred_w # center_x + 0.5 * w
        # ymax
        pred_boxes4 = pred_ctr_y + torch.tensor(0.5, dtype=pred_ctr_y.dtype, device=pred_h.device) * pred_h # center_y + 0.5 * h

        #   先用stack拼接增加一个维度,再用flatten展平,不如直接用cat
        pred_boxes = torch.stack((pred_boxes1, pred_boxes2, pred_boxes3, pred_boxes4), dim=2).flatten(1)
        return pred_boxes

#---------------------------------------------------#
#   计算每个anchors与gt匹配iou最大的索引（如果iou<0.3索引置为-1，0.3<iou<0.7索引为-2）
#---------------------------------------------------#
class Matcher(object):
    BELOW_LOW_THRESHOLD = -1
    BETWEEN_THRESHOLDS = -2

    __annotations__ = {
        'BELOW_LOW_THRESHOLD': int,
        'BETWEEN_THRESHOLDS': int,
    }

    def __init__(self, high_threshold, low_threshold, allow_low_quality_matches=False):
        # type: (float, float, bool) -> None
        """
        Args:
            high_threshold (float): quality values greater than or equal to
                this value are candidate matches.
            low_threshold (float): a lower quality threshold used to stratify
                matches into three levels:
                1) matches >= high_threshold
                2) BETWEEN_THRESHOLDS matches in [low_threshold, high_threshold)
                3) BELOW_LOW_THRESHOLD matches in [0, low_threshold)
            allow_low_quality_matches (bool): if True, produce additional matches
                for predictions that have only low-quality match candidates. See
                set_low_quality_matches_ for more details.
        """
        self.BELOW_LOW_THRESHOLD = -1
        self.BETWEEN_THRESHOLDS = -2
        assert low_threshold <= high_threshold
        self.high_threshold = high_threshold  # 0.7
        self.low_threshold = low_threshold    # 0.3
        self.allow_low_quality_matches = allow_low_quality_matches

    def __call__(self, match_quality_matrix):
        """
        计算anchors与每个gtboxes匹配的iou最大值，并记录索引，
        iou<low_threshold索引值为-1， low_threshold<=iou<high_threshold索引值为-2
        Args:
            match_quality_matrix (Tensor[float]): an MxN tensor, containing the  anchors与真实bbox的iou信息,是一个矩阵,代表每一个真实框和预测框的交并比
            pairwise quality between M ground-truth elements and N predicted elements.

        Returns:
            matches (Tensor[int64]): an N tensor where N[i] is a matched gt in
            [0, M - 1] or a negative value indicating that prediction i could not
            be matched.
        """
        if match_quality_matrix.numel() == 0:
            # empty targets or proposals not supported during training
            if match_quality_matrix.shape[0] == 0:
                raise ValueError(
                    "No ground-truth boxes available for one of the images "
                    "during training")
            else:
                raise ValueError(
                    "No proposal boxes available for one of the images "
                    "during training")

        #---------------------------------------------------#
        # match_quality_matrix is M (gt) x N (predicted)  0:真实框 1:预测框 4*6
        # Max over gt elements (dim 0) to find best gt candidate for each prediction
        # M x N 的每一列代表一个anchors与所有gt的匹配iou值
        # matched_vals代表每列的最大值，即每个anchors与所有gt匹配的最大iou值
        # matches对应最大值所在的索引
        #---------------------------------------------------#
        matched_vals, matches = match_quality_matrix.max(dim=0)  # 维度0上求最大值(真实框), 对预测框找iou最大的真实框 返回dim=1长度的个值 [[值,下标],...]
        if self.allow_low_quality_matches:
            all_matches = matches.clone()   # clone() 不能用等号,等号是引用
        else:
            all_matches = None

        #---------------------------------------------------#
        #   Assign candidate matches with low quality to negative (unassigned) values
        #   计算iou小于low_threshold的索引
        #---------------------------------------------------#
        below_low_threshold = matched_vals < self.low_threshold # 返回True, False列表
        # 计算iou在low_threshold与high_threshold之间的索引值
        between_thresholds = (matched_vals >= self.low_threshold) & (
            matched_vals < self.high_threshold
        )

        #---------------------------------------------------#
        #   iou小于low_threshold的matches索引置为-1
        #---------------------------------------------------#
        matches[below_low_threshold] = self.BELOW_LOW_THRESHOLD  # -1

        #---------------------------------------------------#
        #   iou在[low_threshold, high_threshold]之间的matches索引置为-2
        #---------------------------------------------------#
        matches[between_thresholds] = self.BETWEEN_THRESHOLDS    # -2

        #---------------------------------------------------#
        #   iou在大于0.7的部分没做任何操作
        #---------------------------------------------------#

        #---------------------------------------------------#
        #   是否启用最低正样本匹配,没有任何框的iou大于0.7,就选择最大iou的框为正样本
        #---------------------------------------------------#
        if self.allow_low_quality_matches:
            assert all_matches is not None
            self.set_low_quality_matches_(matches, all_matches, match_quality_matrix)

        return matches

    #---------------------------------------------------#
    #   没有任何框的iou大于0.7,就选择最大iou的框为正样本
    #   在维度1上取最大值,相当于对真实框找所有预测框中iou最大的值
    #---------------------------------------------------#
    def set_low_quality_matches_(self, matches, all_matches, match_quality_matrix):
        """
        Produce additional matches for predictions that have only low-quality matches.
        Specifically, for each ground-truth find the set of predictions that have
        maximum overlap with it (including ties); for each prediction in that set, if
        it is unmatched, then match it to the ground-truth with which it has the highest
        quality value.
        """
        # For each gt, find the prediction with which it has highest quality
        # 对于每个gt boxes寻找与其iou最大的anchor，
        # highest_quality_foreach_gt为匹配到的最大iou值
        highest_quality_foreach_gt, _ = match_quality_matrix.max(dim=1)  # 在维度1上取最大值,相当于对真实框找所有预测框中iou最大的值 长度为真实框个数

        #---------------------------------------------------#
        #   寻找每个gt boxes与其iou最大的anchor索引，一个gt匹配到的最大iou可能有多个anchor
        #   Find highest quality match available, even if it is low, including ties
        #---------------------------------------------------#
        # gt_pred_pairs_of_highest_quality = torch.nonzero(
        #     match_quality_matrix == highest_quality_foreach_gt[:, None]
        # )
        gt_pred_pairs_of_highest_quality = torch.where(
            torch.eq(match_quality_matrix, highest_quality_foreach_gt[:, None])
        )
        # Example gt_pred_pairs_of_highest_quality:
        #   tensor([[    0, 39796],
        #           [    1, 32055],
        #           [    1, 32070],
        #           [    2, 39190],
        #           [    2, 40255],
        #           [    3, 40390],
        #           [    3, 41455],
        #           [    4, 45470],
        #           [    5, 45325],
        #           [    5, 46390]])
        # Each row is a (gt index, prediction index)
        # Note how gt items 1, 2, 3, and 5 each have two ties

        #---------------------------------------------------#
        #   gt_pred_pairs_of_highest_quality[:, 0]代表是对应的gt index(不需要)
        #---------------------------------------------------#
        # pre_inds_to_update = gt_pred_pairs_of_highest_quality[:, 1]
        pre_inds_to_update = gt_pred_pairs_of_highest_quality[1]
        #---------------------------------------------------#
        #   保留该anchor匹配gt最大iou的索引，即使iou低于设定的阈值
        #---------------------------------------------------#
        matches[pre_inds_to_update] = all_matches[pre_inds_to_update]

#----------------------------------------------------#
#   计算边界框损失信息
#----------------------------------------------------#
def smooth_l1_loss(input, target, beta: float = 1. / 9, size_average: bool = True):
    """
    very similar to the smooth_l1_loss from pytorch, but with
    the extra beta parameter
    """
    # n对应公式中的x
    n = torch.abs(input - target)
    # cond = n < beta
    cond = torch.lt(n, beta)

    # where 用来判断cond绝对值是否大于0
    loss = torch.where(cond, 0.5 * n ** 2 / beta, n - 0.5 * beta)

    # 返回平均损失还是损失和
    if size_average:
        return loss.mean()
    return loss.sum()
