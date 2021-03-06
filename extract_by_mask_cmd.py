# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:08:49 2020

掩膜提取, 利用输入矢量数据裁切栅格数据.
@author: mlm
"""
from argparse import ArgumentParser

from rstools.crop import extract_by_mask
from cmd_util import trans_numbers

if __name__ == '__main__':
    parse = ArgumentParser()

    parse.add_argument('-im', '--input_mask', required=True,
                       help="输入矢量掩膜数据")
    parse.add_argument('-ir', '--input_raster', required=True,
                       help="输入栅格数据")
    parse.add_argument('-o', '--output_file', required=True,
                       help="输出栅格数据")
    parse.add_argument('-n', '--nodata', default='0',  # type=float,
                       help="空值,默认0")
    parse.add_argument('-f', '--format', default='GTiff',
                       help="输出栅格格式(GDAL支持类型),默认'GTiff'")
    parse.add_argument('-c', '--compress', default=None,
                       help="输出数据压缩方式, 默认无压缩")

    args = parse.parse_args()

    extract_by_mask(args.input_mask, args.input_raster,
                    args.output_file, nodata=trans_numbers(args.nodata),
                    formats=args.format, compress=args.compress)
