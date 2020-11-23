# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:42:39 2020

@author: mlm
"""

from argparse import ArgumentParser
from rstools.mosaic import mosaic_simple


if __name__ == '__main__':

    parse = ArgumentParser()
    parse.add_argument('--input_rasters', required=True,
                       help="输入栅格数据列表")
    parse.add_argument('--output_raster', required=True,
                       help="输出栅格数据")
    parse.add_argument('--output_res', default=None,
                       help="分辨率,如果未指定则采用原始数据分辨率.")
    parse.add_argument('--nodata_value', default=None,
                       help="空值,默认None,采取原数据空值.")
    parse.add_argument('--crs', default=None,
                       help="数据坐标参考,适用于原数据不含坐标参考,需要手动指定的情况,"
                       "默认None,采用数据本身坐标参考.")

    args = parse.parse_args()

    res = args.output_res
    res = float(res) if res is not None else None
    mosaic_simple(args.input_rasters, args.output_raster,
                  res=res,
                  nodata=args.nodata_value,
                  crs=args.crs)
