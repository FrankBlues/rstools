# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:40:55 2020

@author: mlm
"""
import os
from .io_utils import write_json


def create_band_def_dict(b1, b2, b3, other_bands):
    """生成波段定义的字典结构,用于波段计算、波段组合等的输入, 如果输入的影像不是正确文件或者
    输入的波段索引不能被识别，直接退出程序.

    Args:
        b1, b2, b3 (str): 前3个波段,格式"image_file, band_index",其中前2个波段
            不能为空;
        other_bands (str): 其它波段,波段直接用';'分隔.

    """
    def parse_args(arg):
        """解析传入的波段参数,形式为'path,index'"""
        image, band_idx = [s.strip() for s in arg.split(',')]
        # 如果image不是文件或者波段索引转换为int出错,返回空值
        try:
            band_idx = int(band_idx)
        except ValueError:
            print("Error: Wrong input band index.")
            exit(1)
        if not os.path.isfile(image):
            print("Error: Current input file seems not a file.")
            exit(1)
        return [image, band_idx]

    null_values = ['None', 'none', '', ' ']
    layers = {}
    if b1 in null_values or b2 in null_values:
        raise ValueError("Band b1 and b2 cannot be empty.")
    layers['b1'] = parse_args(b1)
    layers['b2'] = parse_args(b2)

    if not b3 in null_values:
        layers['b3'] = parse_args(b3)
    else:  # 如果第三个波段为空,则不再进行下面的判断
        return layers
    
    if ';' in other_bands:    
        other_band_list = [s.strip() for s in other_bands.split(';')]
    else:  # 只有一个波段输入
        other_band_list = [other_bands.strip()]
        if other_band_list[0] in null_values:
            return layers
    idx = 4
    for b in other_band_list:
        layers['b' + str(idx)] = parse_args(b)
        idx += 1
    return layers


def create_band_def_json(b1, b2, b3, other_bands='',
                         out_config='/tmp/band_def.json'):
    layers = create_band_def_dict(b1, b2, b3, other_bands)
    print("Input layers is:\n{}".format(layers))
    write_json(out_config, layers)

