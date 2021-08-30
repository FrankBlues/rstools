# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 17:38:37 2021

@author: mlm
"""
import numpy as np
from PIL import Image as Pil

class pilImage(object):
    """利用PIL显示、保存图像或缩略图.

    Attributes:
        data (numpy ndarray or list): 单通道二维数组或列表形式的RGB数组[R,G,B].
        img (pil image object): PIL对象

    """
    def __init__(self, data):
        """利用数组构建PIL Image对象.

        Args:
            data (numpy ndarray or list): 单通道二维数组或列表形式的RGB数组[R,G,B].

        Raises:
            ValueError: If input format wrong.
        """

        self.data = data
        if isinstance(data, list):
            if len(data) == 3:
                R = Pil.fromarray(np.asanyarray(data[0]), 'L')
                G = Pil.fromarray(np.asanyarray(data[1]), 'L')
                B = Pil.fromarray(np.asanyarray(data[2]), 'L')
                self.img = Pil.merge("RGB", (R, G, B))
        elif isinstance(data, np.ndarray):
            if data.ndim == 2:
                self.img = Pil.fromarray(np.asanyarray(data), 'L')
        else:
            raise ValueError('Wrong input format,please input either numpy \
                              ndarray or RGB list of ndarray.')

    def show(self):
        """Show image."""
        self.img.show()

    def save(self, location):
        """Save image.

        Args:
            location (str): The target image file.
        """
        self.img.save(location, "JPEG")

    def thumbnail(self, size=(1024, 1024)):
        """Construct a thumbnail object.

        Args:
            size (tuple): Size of the thumbnail, default (1024, 1024).
        """
        self.img.thumbnail(size)

    def showThumb(self, size=(1024, 1024)):
        """Show thumbnail."""
        self.thumbnail(size)
        self.show()

    def saveThumb(self, location, size=(1024, 1024)):
        """Save thumbnail."""
        self.thumbnail(size)
        self.save(location)


def gamma(image, gamma=1.0):
    """ Apply gamma correction to the channels of the image.

    Note:
        Only apply to 8 bit unsighn image.

    Args:
        image (numpy ndarray): The image array.
        gamma (float): The gamma value.

    Returns:
        Numpy ndarray: Gamma corrected image array.

    Raises:
        ValueError: If gamma value less than 0 or is nan.

    """
    if gamma <= 0 or np.isnan(gamma):
        raise ValueError("gamma must be greater than 0")
    if image.dtype != 'uint8':
        raise ValueError("data type must be uint8")

    norm = image/256.
    norm **= 1.0 / gamma
    return (norm * 255).astype('uint8')


def aoto_gamma(image, mean_v=0.45, nodata=None):
    """自动获取gamma值,"""
    dims = image.shape
    if len(dims) > 2 or image.dtype != 'uint8':
        raise ValueError()
    img = image[::2, ::2].astype('float32')
    if nodata is not None:
        img[img == nodata] = np.nan
    gammav = np.log10(mean_v)/np.log10(np.nanmean(img)/256)
    return 1/gammav


def bytscl(argArry, maxValue=None, minValue=None, nodata=None, top=255):
    """将原数组指定范围(minValue ≤ x ≤ maxValue)数据拉伸至指定整型范围(0 ≤ x ≤ Top),
    输出数组类型为无符号8位整型数组.

    Note:
        Dtype of the output array is uint8.

    Args:
        argArry (numpy ndarray): 输入数组.
        maxValue (float): 最大值.默认为输入数组最大值.
        minValue (float): 最小值.默认为输入数组最大值.
        nodata (float or None): 空值，默认None，计算时排除.
        top (float): 输出数组最大值，默认255.

    Returns:
        Numpy ndarray: 线性拉伸后的数组.

    Raises:
        ValueError: If the maxValue less than or equal to the minValue.

    """
    mask = (argArry == nodata)
    retArry = np.ma.masked_where(mask, argArry)

    if maxValue is None:
        maxValue = np.ma.max(retArry)
    if minValue is None:
        minValue = np.ma.min(retArry)

    if maxValue <= minValue:
        raise ValueError("Max value must be greater than min value! ")

    retArry = (retArry - minValue) * float(top) / (maxValue - minValue)

    retArry[argArry < minValue] = 0
    retArry[argArry > maxValue] = top
    retArry = np.ma.filled(retArry, 0)
    return retArry.astype('uint8')


def percentile_v(argArry, percent=2, leftPercent=None,
                 rightPercent=None, nodata=None):
    if percent is not None:
        leftPercent = percent
        rightPercent = percent
    elif (leftPercent is None or rightPercent is None):
        raise ValueError('Wrong parameter! Both left and right percent '
                         'should be set.')

    if len(argArry.shape) == 2:
        _arr = argArry[::2, ::2]
        retArry = _arr[_arr != nodata]
    else:
        retArry = argArry[argArry != nodata]

    minValue = np.percentile(retArry, leftPercent, interpolation="nearest")
    maxValue = np.percentile(retArry, 100 - rightPercent,
                             interpolation="nearest")
    
    return maxValue, minValue


def linear_stretch(argArry, percent=2, leftPercent=None,
                   rightPercent=None, nodata=None):
    """指定百分比对数据进行线性拉伸处理.

    Args:
        argArry (numpy ndarray): 输入图像数组.
        percent (float): 最大最小部分不参与拉伸的百分比.
        leftPercent (float):  左侧（小）不参与拉伸的百分比.
        rightPercent (float):  右侧（大）不参与拉伸的百分比.
        nodata (same as input array): 空值，默认None，计算时排除.

    Returns:
        numpy ndarray: 拉伸后八位无符号整型数组(0-255).

    Raises:
        ValueError: If only one of the leftPercent or the rightPercent is set.

    """
    maxValue, minValue = percentile_v(argArry, percent, leftPercent,
                                      rightPercent, nodata)
    return bytscl(argArry, maxValue=maxValue, minValue=minValue, nodata=nodata)
