# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 18:15:43 2020

栅格计算，输入的栅格数据整体参与计算(b1).
@author: mlm
"""

from argparse import ArgumentParser

from rsgislib import imagecalc


if __name__ == '__main__':

    dtypes = ['undefined', 'int8', 'int16', 'int32', 'int64', 'uint8',
              'uint16', 'uint32', 'uint64', 'float32', 'float64']

    parse = ArgumentParser()

    parse.add_argument('-i', '--input_raster', required=True,
                       help="输入栅格数据")
    parse.add_argument('-o', '--output_raster', required=True,
                       help="输出栅格数据")
    parse.add_argument('-e', '--expression', required=True,
                       help="栅格计算表达式")
    parse.add_argument('-f', '--format', default='GTiff',
                       help="输出结果命名字段,默认GTiff")
    parse.add_argument('-t', '--dtype', default='uint8', choices=dtypes,
                       help="输出栅格类型")

    args = parse.parse_args()

    # 计算
    imagecalc.imageMath(args.input_raster, args.output_raster,
                        args.expression, args.format, dtypes.index(args.dtype))
