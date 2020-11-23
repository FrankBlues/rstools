# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:25:48 2020

投影转换
@author: mlm
"""

from argparse import ArgumentParser
from rstools.warp import reproject_rio


if __name__ == '__main__':

    resampling_methods = ['nearest', 'bilinear', 'cubic', 'average',
                          'max', 'min', 'med']
    parse = ArgumentParser()
    parse.add_argument('--input_raster', required=True,
                       help="输入栅格数据")
    parse.add_argument('--output_raster', required=True,
                       help="输出栅格数据")
    parse.add_argument('--dst_crs', required=True, default='EPSG:4326',
                       help="目标坐标参考")
    parse.add_argument('--output_res', default=None,
                       help="采样后的分辨率,如果未指定则采用原始数据分辨率.")
    parse.add_argument('--resampling_method', default='nearest',
                       choices=resampling_methods,
                       help="重采样方法")
    parse.add_argument('--src_crs', default=None,
                       help="如果影像没有定义坐标参考,则采用此指定坐标参考")

    args = parse.parse_args()

    res = args.output_res
    res = float(res) if res is not None else None
    reproject_rio(args.input_raster, args.output_raster, args.dst_crs,
                  res, method=args.resampling_method,
                  src_crs=args.src_crs)
