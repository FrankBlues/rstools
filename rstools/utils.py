# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 11:17:31 2021

@author: mlm
"""
import rasterio

from .io_utils import check_parent_dir


def get_target_crs(in_raster, out_file):
    """根据影像投影类型及所在位置判断目标投影参数并写出到文件.

    Args:
        in_raster(str): 输入影像路径;
        out_file(str): 写出后的文件.

    """
    # 判断是地理坐标系或投影坐标系
    with rasterio.open(in_raster) as ds:
        if ds.crs is None:
            print("Unrecgonized sapcial reference system.")
            exit(1)

        if ds.crs.is_projected:
            target_crs = 'NULL'
        elif ds.crs.is_geographic:
            center_lon = (ds.bounds.left + ds.bounds.right)/2
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
                target_crs = 'World_Sinusoidal'

    print(f"Target spacial reference is {target_crs}.")
    check_parent_dir(out_file)
    with open(out_file, 'w') as projf:
        projf.write(target_crs)


if __name__ == '__main__':
    in_raster = r'E:\T50SKH_20210107T031121_TCI.jp2'

    out_file = 'd:/temp11/projection.txt'

    get_target_crs(in_raster, out_file)





