# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 18:15:43 2020

栅格计算，输入栅格数据的各个波段参与计算(b1, b2, b3, ..., bn, 从1开始).
@author: mlm
"""

from argparse import ArgumentParser

from rsgislib import imagecalc


if __name__ == '__main__':

    dtypes = ['undefined', 'int8', 'int16', 'int32', 'int64', 'uint8',
              'uint16', 'uint32', 'uint64', 'float32', 'float64']

    parse = ArgumentParser()

    parse.add_argument('--input_raster', required=True,
                       help="输入栅格数据")
    parse.add_argument('--output_raster', required=True,
                       help="输出栅格数据")
    parse.add_argument('--expression', required=True,
                       help="栅格计算表达式")
    parse.add_argument('--format', default='GTiff',
                       help="输出结果命名字段,默认GTiff")
    parse.add_argument('--dtype', default='uint8', choices=dtypes,
                       help="输出栅格类型")

    args = parse.parse_args()

    # 计算
    imagecalc.imageBandMath(args.input_raster, args.output_raster,
                            args.expression, args.format,
                            dtypes.index(args.dtype))
