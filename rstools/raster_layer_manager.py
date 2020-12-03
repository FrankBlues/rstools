# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 14:44:51 2020

@author: mlm
"""
import os
import rasterio

from .io_utils import check_parent_dir, read_json


def get_raster_arr(in_r, index):
    """获取栅格指定波段的数组."""
    with rasterio.open(in_r) as ds:
        return ds.read(index)


def layer_stack(layer_dict, out_raster, out_format='GTiff', out_crs=None):
    """进行波段组合.
        1. 以输入的第一个波段为基准判断数组大小是否一致;
        2. 按顺序进行组合.

    Args:
        layer_dict (dict): 输入波段字典,{'b1', ['path/image.tif', 1]};
        out_raster (str): 输出栅格数据;
        out_format (str): 输出栅格数据格式, 默认'GTiff';
        out_crs (str or CRS object): 输出数据投影,默认None,采用第一个输入数据投影.

    """
    n_layer = len(layer_dict)
    if n_layer <= 1:  # 至少2个及以上做波段组合
        print("Seems no need to stack, should input at least 1 layer, "
              "return None.")
        return
    with rasterio.open(layer_dict['b1'][0]) as src:
        meta = src.meta.copy()
        data_shape = (src.height, src.width)

    for k in layer_dict:
        if k != 'b1':
            ds = rasterio.open(layer_dict[k][0])
            if ds.height != data_shape[0] or ds.width != data_shape[1]:
                raise ValueError("Shapes of inputs do not have the same shape.")
            ds.close()

    crs = meta.get('crs') if out_crs is None else out_crs
    meta.update({'driver': out_format,
                 'count': n_layer,
                 'crs': crs})
    check_parent_dir(out_raster)
    with rasterio.open(out_raster, 'w', **meta) as dst:
        i = 1
        for k, v in layer_dict.items():
            dst.write(get_raster_arr(v[0], v[1]), i)
            i += 1
    return out_raster


def layer_stack_use_json(layers_json, out_raster, out_format='GTiff',
                         out_crs=None):
    """从配置文件中获取波段定义后进行波段组合."""
    layer_stack(read_json(layers_json), out_raster, out_format=out_format,
                out_crs=out_crs)

