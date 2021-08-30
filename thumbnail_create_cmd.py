# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 17:45:28 2021

遥感影像缩略图生产,预处理采用2%线性拉伸及自动gamma校正,缩略图保持原来长宽比,短边为指定像素大小.
@author: mlm
"""
from argparse import ArgumentParser

from rstools.thumbnail import create_thumbnail_rs


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-ir', '--input_raster', required=True,
                       help="输入栅格数据")
    parser.add_argument('-o', '--output_file', required=True,
                       help="输出缩略图")
    parser.add_argument('-s', '--size', default='500',  # type=float,
                       help="缩略图短边像素大小")

    args = parser.parse_args()

    create_thumbnail_rs(args.input_raster, args.output_file,
                        int(args.size))
