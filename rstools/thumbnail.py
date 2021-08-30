# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 17:35:24 2021

@author: mlm
"""
import rasterio

from .io_utils import check_parent_dir
from .image_utils import pilImage, bytscl, percentile_v
from .image_utils import aoto_gamma, gamma, linear_stretch


def pre_process_thumbs(r_arr, g_arr, b_arr, nodata=None):
    """输入原始RGB值,返回2%线性拉伸及自动gamma校正后的RGB值."""
    # 计算线性拉伸最大最小值,采用2%拉伸
    r_p_max, r_p_min = percentile_v(r_arr, nodata=nodata)
    g_p_max, g_p_min = percentile_v(g_arr, nodata=nodata)
    b_p_max, b_p_min = percentile_v(b_arr, nodata=nodata)
    # 如果2%处数值相等,极有可能是nodata
    if r_p_max == g_p_max == b_p_max and nodata is None:
        print("The max value may be the nodata value")
        nodata = r_p_max
        r_p_max, r_p_min = percentile_v(r_arr, nodata=nodata)
        g_p_max, g_p_min = percentile_v(g_arr, nodata=nodata)
        b_p_max, b_p_min = percentile_v(b_arr, nodata=nodata)
    elif r_p_min == g_p_min == b_p_min and nodata is None:
        print("The min value may be the nodata value")
        nodata = r_p_min
        r_p_max, r_p_min = percentile_v(r_arr, nodata=nodata)
        g_p_max, g_p_min = percentile_v(g_arr, nodata=nodata)
        b_p_max, b_p_min = percentile_v(b_arr, nodata=nodata)
    # 线性拉伸
    stretched_r = bytscl(r_arr, r_p_max, r_p_min, nodata)
    stretched_g = bytscl(g_arr, g_p_max, g_p_min, nodata)
    stretched_b = bytscl(b_arr, b_p_max, b_p_min, nodata)

    # 计算gamma校正用到的gamma值
    gamma_v_r = aoto_gamma(stretched_r, nodata=nodata)
    gamma_v_g = aoto_gamma(stretched_g, nodata=nodata)
    gamma_v_b = aoto_gamma(stretched_b, nodata=nodata)
    g = (gamma_v_r + gamma_v_g + gamma_v_b) / 3
    print(f"Use gamma value: {g:.3f}")
    return [gamma(stretched_r, g), gamma(stretched_g, g),
            gamma(stretched_b, g)]


def create_thumbnail_rs(image, out_thumbs='thumbs.png', size=500):
    """遥感影像缩略图生产, 预处理采用2%线性拉伸及自动gamma校正, 缩略图保持原来长宽比,
    短边为指定像素大小.
        * 单波段: 灰度图;
        * 3波段: 默认采用1、2、3波段作为RGB波段;
        * 4波段及以上: 默认采用3、2、1波段作为RGB波段;
    """
    check_parent_dir(out_thumbs)
    with rasterio.open(image) as src:
        meta = src.meta.copy()
        width, height = meta['width'], meta['height']
        nodata = meta['nodata']
        bands = meta['count']
        # 短边等于size
        ratio = height / width
        if width > height:
            size1 = size
            size0 = int(size / ratio)
        else:
            size0 = size
            size1 = int(size * ratio)
        # 如果数据过大时,比如大于10倍size, 读取view的最大尺寸
        x_view_size, y_view_size = size1 * 10, size0 * 10
        if bands == 1:
            if height > x_view_size or width > y_view_size:
                print("The input data too large, read view of the data array.")
                data_array = src.read(1, out_shape=(x_view_size, y_view_size))
            else:
                data_array = src.read(1)
            print("Pre-processing the bands data..")
            stretched = linear_stretch(data_array, 2, nodata=nodata)
            gamma_trans = gamma(stretched, aoto_gamma(stretched, nodata=nodata))
            print("Creating thumbnails..")
            IMG = pilImage(gamma_trans)
            IMG.saveThumb(out_thumbs, (size0, size1))
        elif bands == 3:
            print("Use band_1, band_2, band_3 as the RGB bands respectly.")
            if height > x_view_size or width > y_view_size:
                print("The input data too large, read view of the data array.")
                r = src.read(1, out_shape=(x_view_size, y_view_size))
                g = src.read(2, out_shape=(x_view_size, y_view_size))
                b = src.read(3, out_shape=(x_view_size, y_view_size))
            else:
                r, g, b = src.read(1), src.read(2), src.read(3)
            rgb_list = pre_process_thumbs(r, g, b, nodata)
            IMG = pilImage(rgb_list)
            IMG.saveThumb(out_thumbs, (size0, size1))
        elif bands > 3:
            print("Use band_3, band_2, band_1 as the RGB bands respectly.")
            if height > x_view_size or width > y_view_size:
                print("The input data too large, read view of the data array.")
                r = src.read(3, out_shape=(x_view_size, y_view_size))
                g = src.read(2, out_shape=(x_view_size, y_view_size))
                b = src.read(1, out_shape=(x_view_size, y_view_size))
            else:
                r, g, b = src.read(1), src.read(2), src.read(3)
            print("Pre-processing the bands data..")
            rgb_list = pre_process_thumbs(r, g, b, nodata)
            print("Creating thumbnails..")
            IMG = pilImage(rgb_list)
            IMG.saveThumb(out_thumbs, (size0, size1))

