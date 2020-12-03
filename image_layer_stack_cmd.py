# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:55:26 2020
根据输入的波段定义配置文件进行波段重新组合.
@author: mlm
"""

from argparse import ArgumentParser

from cmd_util import trans_none
from rstools.raster_layer_manager import layer_stack_use_json


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--input_band_define', required=True,
                        help="输入的波段定义参数文件.")
    parser.add_argument('--output_raster', required=True,
                        help="波段组合后的栅格结果.")
    parser.add_argument('--out_format', default='GTiff',
                        help="输出栅格数据格式,默认GTiff.")
    parser.add_argument('--out_crs', default=None,
                        help="输出数据的投影, 默认None,采用与第一个波段一致的投影.")

    args = parser.parse_args()

    layer_stack_use_json(args.input_band_define, args.output_raster,
                         args.out_format, trans_none(args.out_crs))
