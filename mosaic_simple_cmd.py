# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:42:39 2020

@author: mlm
"""
import os
from argparse import ArgumentParser
from rstools.mosaic import mosaic_simple
from rstools.io_utils import read_list

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--mosaic_list_file', required=True,
                       help="输入栅格数据列表")
    parser.add_argument('--output_raster', required=True,
                       help="输出栅格数据")
    parser.add_argument('--output_res', default=None,
                       help="分辨率,如果未指定则采用原始数据分辨率.")
    parser.add_argument('--nodata_value', default=None,
                       help="空值,默认None,采取原数据空值.")
    parser.add_argument('--crs', default=None,
                       help="数据坐标参考,适用于原数据不含坐标参考,需要手动指定的情况,"
                       "默认None,采用数据本身坐标参考.")

    args = parser.parse_args()

    input_rasters = read_list(args.mosaic_list_file)
    # print(input_rasters)
    # input_rasters = map(os.path.normpath, input_rasters)
    
    res = args.output_res
    res = float(res) if res is not None else None
    mosaic_simple(input_rasters, args.output_raster,
                  res=res,
                  nodata=args.nodata_value,
                  crs=args.crs)
