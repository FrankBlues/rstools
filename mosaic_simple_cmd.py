# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:42:39 2020

Usage:
>>> python mosaic_simple_cmd.py -i D:\g_terrain\14 -o D:\g_terrain\t_14.tif -c 'EPSG:3857 -f 'png'
@author: mlm
"""
import os
from argparse import ArgumentParser

from rstools.mosaic import mosaic_simple
from rstools.io_utils import read_list, get_image_file
from cmd_util import trans_numbers, trans_none


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-i', '--input_rasters', required=True,
                        help="输入栅格数据列表,可以是一个txt格式文本文件,每一行一个记录,"
                        "或者指定文件夹,将合并该文件夹下所有指定格式的数据.")
    parser.add_argument('-o', '--output_raster', required=True,
                        help="输出栅格数据")
    parser.add_argument('-r', '--output_res', default=None,
                        help="分辨率,如果未指定则采用原始数据分辨率.")
    parser.add_argument('-n', '--nodata_value', default=None,
                        help="空值,默认None,采取原数据空值.")
    parser.add_argument('-c', '--crs', default=None,
                        help="数据坐标参考,适用于原数据不含坐标参考,需要手动指定的情况,"
                        "默认None,采用数据本身坐标参考.")
    parser.add_argument('-f', '--format', default="tif",
                        help="文件格式,如果input_rasters是一个文件目录,检索该目录下"
                        "所有以该格式为后缀的文件,默认tif.")

    args = parser.parse_args()

    input_arg = args.input_rasters
    if input_arg.endswith('.txt'):  # 指定栅格列表在文本文件里
        print("Read input rasters from a text file.")
        input_rasters = read_list(input_arg)
    elif os.path.isdir(input_arg):
        print("List all raster files inside the input directory.")
        input_rasters = get_image_file(input_arg, [args.format])
    else:
        print("Unrecognized param 'input_rasters'.")
        exit(1)

    res = trans_numbers(args.output_res)
    nodata = trans_numbers(args.nodata_value)
    mosaic_simple(input_rasters, args.output_raster,
                  res=res,
                  nodata=nodata,
                  crs=trans_none(args.crs))
