# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 11:17:31 2021

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
import os
from osgeo import gdal
from argparse import ArgumentParser

def check_parent_dir(file_name):
    """检查文件父目录是否存在,如果不存在则创建."""
    path = os.path.dirname(file_name)
    if not os.path.exists(path) and path.strip():
        try:
            os.makedirs(path)
        except FileExistsError:
            print("WARNING: Directory already exists")

def get_target_crs(in_raster, out_file):
    """根据影像投影类型及所在位置判断目标投影参数并写出到文件.

    Args:
        in_raster(str): 输入影像路径;
        out_file(str): 写出后的文件.

    """
    # 判断是地理坐标系或投影坐标系
    ds = gdal.Open(in_raster)
    
    sr = ds.GetSpatialRef()
    if sr is None:
        print("Unrecgonized sapcial reference system.")
        exit(1)
    if sr.IsProjected():
        target_crs = 'NULL'
    elif sr.IsGeographic():
        trans = ds.GetGeoTransform()
        center_lon = trans[0] + trans[1] * ds.RasterXSize / 2
        # 东经73.5-136.5
        epsg_code = 4534
        step = 0
        for lon in range(73, 134, 3):
            if center_lon >= lon + 0.5 and center_lon < lon + 3.5:
                target_crs = f'EPSG:{epsg_code+step}'
            else:
                step += 1
        # 其它区域
        if center_lon < 73.5 or center_lon >= 136.5:
            target_crs = 'PROJCS[\\"World_Sinusoidal\\",GEOGCS[\\"GCS_WGS_1984\\",DATUM[\\"WGS_1984\\",SPHEROID[\\"WGS_1984\\",6378137,298.257223563]],PRIMEM[\\"Greenwich\\",0],UNIT[\\"Degree\\",0.017453292519943295]],PROJECTION[\\"Sinusoidal\\"],PARAMETER[\\"False_Easting\\",0],PARAMETER[\\"False_Northing\\",0],PARAMETER[\\"Central_Meridian\\",0],UNIT[\\"Meter\\",1],AUTHORITY[\\"EPSG\\",\\"54008\\"]]'

    print(f"Target spacial reference is {target_crs}.")
    check_parent_dir(out_file)
    with open(out_file, 'w') as projf:
        projf.write(target_crs)


if __name__ == '__main__':
    # in_raster = r'E:\T50SKH_20210107T031121_TCI.jp2'
    # in_raster = r'E:\S2\label\S2B_MSIL1C_20210701T030549_N0301_R075_T50SMJ_20210701T051355_14.jpg'
    # in_raster = r'd:\temp11\P_GZ_test4_2019_0615_Level_18.tif'
    # in_raster = r'd:\temp11\natural_earth_shaded_relief1.tif'
    # out_file = 'd:/temp11/projection.txt'
    # get_target_crs(in_raster, out_file)

    parser = ArgumentParser()

    parser.add_argument('-i', '--input_raster', required=True,
                        help="输入栅格数据")
    parser.add_argument('-o', '--output_file', required=True,
                        default='projection.txt',
                        help="输出栅格数据")

    args = parser.parse_args()

    get_target_crs(args.input_raster, args.output_file)




