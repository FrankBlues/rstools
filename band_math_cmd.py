# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 14:05:58 2020

栅格计算，自定义参与计算的波段，保存在json配置文件中，输入表达式进行指定计算，波段名称必须与
配置文件中定义的名称一致(b1, b2, b3, ...).
@author: mlm
"""

from argparse import ArgumentParser

from rsgislib import imagecalc
from rsgislib.imagecalc import BandDefn

from rstools import io_utils


if __name__ == '__main__':

    dtypes = ['undefined', 'int8', 'int16', 'int32', 'int64', 'uint8',
              'uint16', 'uint32', 'uint64', 'float32', 'float64']

    parse = ArgumentParser()

    parse.add_argument('-i', '--input_json', required=True,
                       help="输入波段定义的json格式配置文件")
    parse.add_argument('-o', '--output_raster', required=True,
                       help="输出栅格数据")
    parse.add_argument('-e', '--expression', required=True,
                       help="栅格计算表达式")
    parse.add_argument('-f', '--format', default='GTiff',
                       help="输出结果命名字段,默认GTiff")
    parse.add_argument('-t', '--dtype', default='uint8', choices=dtypes,
                       help="输出栅格类型")

    args = parse.parse_args()

    # band define
    band_defn_dict = io_utils.read_json(args.input_json)

    band_defn_list = []
    for k, v in band_defn_dict.items():
        band_defn_list.append(BandDefn(k, v[0], v[1]))

    # 计算
    imagecalc.bandMath(args.output_raster, args.expression,
                       args.format, dtypes.index(args.dtype),
                       band_defn_list)
