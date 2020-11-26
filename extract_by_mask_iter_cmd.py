# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:53:57 2020

对输入栅格和矢量数据计算交集，循环裁切栅格.
@author: mlm
"""

from argparse import ArgumentParser

from rstools.crop import crop
from cmd_util import trans_numbers

if __name__ == '__main__':
    parse = ArgumentParser()

    parse.add_argument('-im', '--input_mask', required=True,
                       help="输入矢量掩膜数据")
    parse.add_argument('-ir', '--input_raster', required=True,
                       help="输入栅格数据")
    parse.add_argument('-o', '--output_dir', required=True,
                       help="输出栅格目录,不存在则创建")
    parse.add_argument('-na', '--name_field', required=True,
                       help="输出结果命名字段")
    parse.add_argument('n', '--nodata', default='0',  # type=float,
                       help="空值,默认0")

    args = parse.parse_args()
    crop(args.input_raster, args.input_mask, args.output_dir,
         args.name_field, nodata=trans_numbers(args.nodata))
