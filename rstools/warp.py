# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 16:36:31 2020

@author: mlm
"""
import logging

import rasterio
from rasterio import Affine
from rasterio.warp import reproject, Resampling, calculate_default_transform

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


RESAMPLE_METHODS = {'nearest': Resampling.nearest,
                    'bilinear': Resampling.bilinear,
                    'cubic': Resampling.cubic, 'lanczos': Resampling.lanczos,
                    'cubic_spline': Resampling.cubic_spline,
                    'average': Resampling.average, 'mode': Resampling.mode,
                    'max': Resampling.max, 'min': Resampling.min,
                    'med': Resampling.med, 'q1': Resampling.q1,
                    'q3': Resampling.q3,
                    }

def resample(srcfile, dstfile, new_res, width=0, height=0,
             method=Resampling.bilinear):
    """用rasterio reproject做栅格数据重采样.

    Note:
        暂时不扩充输入行列数及xy方向分辨率不同的情况，需要再扩充.
        
    Args:
        srcfile (str): 输入栅格数据.
        dstfile (str): 重采样后栅格数据.
        new_res (float): 重采样分辨率.
        width, height (int): 数据列数及行数，默认自动计算.
        resampling method (rasterio Resampleing method): One of the following:
            Resampling.nearest,
            Resampling.bilinear,
            Resampling.cubic,
            Resampling.cubic_spline,
            Resampling.lanczos,
            Resampling.average,
            Resampling.mode,
            Resampling.max (GDAL >= 2.2),
            Resampling.min (GDAL >= 2.2),
            Resampling.med (GDAL >= 2.2),
            Resampling.q1 (GDAL >= 2.2),
            Resampling.q3 (GDAL >= 2.2)

    """

    if isinstance(method, str):
        method = RESAMPLE_METHODS.get(method)
    with rasterio.open(srcfile) as src:
        meta = src.meta.copy()
        res = src.res[0]
        logger.info("Source res: {0}, Output res: {1}.".format(res, new_res))
        
        ratio = res*1./new_res
        # new transform
        aff = src.transform

        newaff = Affine(new_res, aff.b, aff.c,
                        aff.d, -new_res, aff.f)

        if width == 0 or height == 0:
            width = int(src.width * ratio)
            height = int(src.height * ratio)
        logger.info("Output data width:{0}, hei"
                    "ght: {1}.".format(width, height))
        meta.update({
                'transform': newaff,
                'width': width,
                'height': height
                })
        logger.info("Resampling data...")
        with rasterio.open(dstfile, 'w', **meta) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=aff,
                    src_crs=src.crs,
                    dst_transform=newaff,
                    dst_crs=src.crs,
                    resampling=method)


def reproject_rio(infile, outfile, dst_crs='EPSG:4326',
                  resample_method=Resampling.nearest,
                  resolution=None, src_crs=None):
    """ Reproject data using rasterio , See
    https://rasterio.readthedocs.io/en/latest/topics/reproject.html

    Args:
        infile (str): Input raster file.
        outfile (str): Reprojected outfile.
        dst_crs : Coordinate spacial reference supported by rasterio,
                default 'EPSG:4326'
        resample_method: Resample method ,defalt Resampling.nearest.
        resolution (float): Resolution of projected raster,default None which
                means same as input.

    """
    if isinstance(resample_method, str):
        resample_method = RESAMPLE_METHODS.get(resample_method)
    with rasterio.open(infile) as src:
        crs = src.crs
        if crs is None:  # 原始数据中没有投影
            print("Origin image has not built-in projection.")
            if src_crs:  # 采用指定的投影参考
                crs = src_crs
            else:
                raise ValueError("Source image hasn't a projection define,"
                                 "Please check it or designate one.")
                return

        if resolution is not None:
            trans, width, height = calculate_default_transform(
                    crs, dst_crs, src.width,
                    src.height, resolution=resolution, *src.bounds)
        else:
            trans, width, height = calculate_default_transform(
                crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'driver': 'GTIFF',
            'crs': dst_crs,
            'transform': trans,
            'width': width,
            'height': height
        })

        with rasterio.open(outfile, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=crs,
                    dst_transform=trans,
                    dst_crs=dst_crs,
                    resampling=resample_method)
