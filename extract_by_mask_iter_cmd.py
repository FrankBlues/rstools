# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:53:57 2020

对输入栅格和矢量数据计算交集，循环裁切栅格.
@author: mlm
"""

from argparse import ArgumentParser

from rstools.crop import crop


if __name__ == '__main__':
    parse = ArgumentParser()

    parse.add_argument('--input_mask', required=True,
                       help="输入矢量掩膜数据")
    parse.add_argument('--input_raster', required=True,
                       help="输入栅格数据")
    parse.add_argument('--output_dir', required=True,
                       help="输出栅格目录,不存在则创建")
    parse.add_argument('--name_field', required=True,
                       help="输出结果命名字段")
    parse.add_argument('--nodata', default='0',  # type=float,
                       help="空值,默认0")

    args = parse.parse_args()
    crop(args.input_raster, args.input_mask, args.output_dir,
         args.name_field, nodata=float(args.nodata))
