# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 16:43:08 2020

栅格数据重采样
@author: mlm
"""

from argparse import ArgumentParser
from rstools.warp import resample


if __name__ == '__main__':

    resampling_methods = ['nearest', 'bilinear', 'cubic', 'average',
                          'max', 'min', 'med']
    parse = ArgumentParser()
    parse.add_argument('-i', '--input_raster', required=True,
                       help="需要进行重采样的栅格数据")
    parse.add_argument('-o', '--output_raster', required=True,
                       help="重采样后的栅格数据")
    parse.add_argument('-r', '--output_res', required=True,
                       help="采样后的分辨率")
    parse.add_argument('-m', '--resampling_method', default='bilinear',
                       choices=resampling_methods,
                       help="重采样方法")

    args = parse.parse_args()

    resample(args.input_raster, args.output_raster, float(args.output_res),
             method=args.resampling_method)
