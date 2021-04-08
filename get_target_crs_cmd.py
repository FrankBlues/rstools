# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 15:20:37 2021
根据影像投影类型及位置判断目标投影类型并写出到指定文件里.
如果是投影坐标系 写出NULL;
如果是地理坐标系 首先计算影像中央经线，然后根据经线判断目标投影;
对于中国区域(东经73.5-136.5),采用高斯2000投影（3度带）；
73.5-76.5  EPSG:4534
76.5-79.5 EPSG:4535
79.5-82.5 EPSG:4536
......
133.5-136.5:EPSG:4554

其它区域选 World_Sinusoidal投影.

Usage:
>>> python get_target_crs_cmd.py -i t_14.tif -o D:\projection.txt

@author: mlm
"""

from argparse import ArgumentParser
from rstools.utils import get_target_crs


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-i', '--input_raster', required=True,
                        help="输入栅格数据")
    parser.add_argument('-o', '--output_file', required=True,
                        default='projection.txt',
                        help="输出栅格数据")

    args = parser.parse_args()

    get_target_crs(args.input_raster, args.output_file)
