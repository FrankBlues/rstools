# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:34:43 2020

@author: DELL
"""

import rasterio
from rasterio.merge import merge


def merge_rio(src_datasets_to_mosaic, output, res=None, nodata=None,
              crs=None):
    """Merge raster datasets to one raster using rasterio.

    Args:
        src_datasets_to_mosaic (list): List of rasterio datasets.
        output (str): Output raster file.
        res (float): Resolution of output raster.
        nodata (float): Nodata value of output raster.

    Usage:
        >>> src_files_to_mosaic = [rasterio.open(f) for f in rfiles]
        >>> merge_rio(src_files_to_mosaic, output, res=10)

    """
    mosaic, out_trans = merge(src_datasets_to_mosaic, res=res, nodata=nodata)

    try:
        src = src_datasets_to_mosaic[0]
        out_meta = src.meta.copy()
        out_meta.update({
                "driver": "GTiff",
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": out_trans,
                "crs": src.crs if (crs is None) else crs,
                "nodata": nodata
                })

        with rasterio.open(output, 'w', **out_meta) as dst:
            dst.write(mosaic)
    finally:
        src.close()
        del mosaic
        del src_datasets_to_mosaic


def mosaic_simple(in_rasters, output, res=None, nodata=None, crs=None):
    """指定需要镶嵌的栅格文件列表,进行简单镶嵌."""
    try:
        raster_datasets = [rasterio.open(f) for f in in_rasters]
    except Exception:  # 遇到错误文件逐步打开
        raster_datasets = []
        for f in in_rasters:
            try:
                ds = rasterio.open(f)
            except Exception as e:
                print('Current file cannot be open, the file is: {}.'.format(f))
                print('Error message is: {}'.format(e))
                continue
            raster_datasets.append(ds)

    merge_rio(raster_datasets, output, res=None, nodata=None, crs=None)