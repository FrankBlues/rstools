# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:25:48 2020

投影转换
Usage:
>>> python reproject_cmd.py -i D:\g_tiles\t_14.tif -o D:\g_tiles\t_14_prj.tif -dc EPSG:4326 
@author: mlm
"""

from argparse import ArgumentParser
from rstools.warp import reproject_rio

from cmd_util import trans_numbers


if __name__ == '__main__':

    resampling_methods = ['nearest', 'bilinear', 'cubic', 'average',
                          'max', 'min', 'med']
    parse = ArgumentParser()
    parse.add_argument('-i', '--input_raster', required=True,
                       help="输入栅格数据")
    parse.add_argument('-o', '--output_raster', required=True,
                       help="输出栅格数据")
    parse.add_argument('-dc', '--dst_crs', default='EPSG:4326',
                       help="目标坐标参考")
    parse.add_argument('-r', '--output_res', default=None,
                       help="采样后的分辨率,如果未指定则采用原始数据分辨率.")
    parse.add_argument('-m', '--resampling_method', default='nearest',
                       choices=resampling_methods,
                       help="重采样方法")
    parse.add_argument('-sc', '--src_crs', default=None,
                       help="如果影像没有定义坐标参考,则采用此指定坐标参考")

    args = parse.parse_args()

    res = trans_numbers(args.output_res)
    reproject_rio(args.input_raster, args.output_raster, args.dst_crs,
                  resample_method=args.resampling_method,
                  resolution=res,
                  src_crs=args.src_crs)
