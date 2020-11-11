# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 19:05:09 2020

栅格裁切相关工具
@author: mlm
"""
import os
import multiprocessing

import numpy as np

from rtree import index
import geopandas as gpd
import rasterio
import rasterio.mask


def extract_by_mask_rio_ds(features, raster_dataset, out, nodata=0,
                           formats='GTiff', compress='lzw'):
    """基于矢量掩膜数据对栅格数据集进行裁切.

    Note:
        需要保持矢量和栅格数据投影一致.

    Args:
        features (iterable object): a GeoJSON-like dict or an object that
          implements the Python geo interface protocol(such as Shapely);
        raster_dataset (rasterio dataset): The raster dataset;
        out (str): 输出栅格;
        formats (str): 输出栅格格式(GDAL支持类型),默认'GTiff';
        nodata (float): 空值, 默认0.

    Returns:
        str: The output raster filename.
        None: If error happens.

    Raises:
        ValueError: If input shapes do not overlap raster.

    """
    # 判段输出路径
    h, t = os.path.split(out)
    if (not h == '') and (not os.path.isdir(h)):
        os.makedirs(h)

    out_meta = raster_dataset.meta.copy()

    try:
        out_image, out_transform = rasterio.mask.mask(
                raster_dataset,
                features,
                crop=True,
                nodata=nodata)
        out_meta.update({"driver": formats,
                         "nodata": nodata,
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform,
                         "compress": compress,
                         })
    except ValueError:  # ValueError: Input shapes do not overlap raster.
        return  # do nothing
    # 全部为空值则不进行输出
    if not np.all(out_image == nodata):
        with rasterio.open(out, "w", **out_meta) as dest:
            dest.write(out_image)
    return out


def extract_by_mask(input_shp, raster, out, nodata=0,
                    formats='GTiff', compress='lzw'):
    """基于上一个函数的,直接输入栅格数据."""
    from shapely.geometry import mapping
    features = read_vector_file(input_shp)
    fea2map = [mapping(features.geometry[i]) for i in range(
               features.geometry.count())]
    with rasterio.open(raster) as ds:
        extract_by_mask_rio_ds(fea2map, ds, out, formats=formats,
                               nodata=nodata, compress=compress)


def extract_by_mask_rio(features, raster, out, nodata=0,
                        formats='GTiff', compress='lzw'):
    """基于上一个函数的,直接输入栅格数据."""
    with rasterio.open(raster) as ds:
        extract_by_mask_rio_ds(features, ds, out, nodata=nodata,
                               formats=formats, compress=compress)


def read_vector_file(input_shp):
    """利用geopandas读矢量数据,返回pandas结构数据."""
    return gpd.read_file(input_shp)


def get_intersect_ids(geometries, bounds):
    """利用空间索引, 计算与目标区域相交的几何ID.

    Args:
        geometries (iterable):要建立空间索引的几何集;
        bounds (tuple):目标几何范围(left bottom right top).

    Returns:
        list: 与目标区域相交的几何所在原几何集的ID列表.

    """
    # 建立分幅数据的空间索引
    idx = index.Index()
    for i, g in enumerate(geometries):
        idx.insert(i, g.bounds)

    # 根据栅格数据四至范围找到相交的分幅
    return list(idx.intersection(tuple(bounds)))


def crop(input_image, input_shp, out_dir, name_field, nodata=0):
    """读取输入矢量数据, 找出与栅格交集, 循环裁切栅格数据, 输出tif格式数据,输出数
    据采用指定字段命名.

    Args:
        input_image (str): 输入栅格数据;
        input_shp (str): 输入矢量数据;
        out_dir (str): 输出目录;
        name_field (str): 输出数据命名字段;
        nodata (float): 空值, 默认0.

    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    data = read_vector_file(input_shp)
    with rasterio.open(input_image) as ds:
        ids = get_intersect_ids(data.geometry, tuple(ds.bounds))
        # 循环裁切
        for i in ids:
            output_name = data.loc[i, name_field] + '.tif'
            out_file = os.path.join(out_dir, output_name)
            extract_by_mask_rio_ds([data.geometry[i]], ds, out_file,
                                   nodata=0, compress=None)


def crop_parallel(input_image, input_shp, out_dir, name_field, nodata=0):
    """测试并行处理."""
    data = read_vector_file(input_shp)
    with rasterio.open(input_image) as ds:
        ids = get_intersect_ids(data.geometry, tuple(ds.bounds))

    # an iterable of [(1,2), (3, 4)] results in [func(1,2), func(3,4)].
    iter_params = [([data.geometry[i]], input_image,
                    os.path.join(out_dir, data.loc[i, name_field] + '.tif'),
                    nodata) for i in ids]
    # processes=3
    with multiprocessing.Pool() as pool:
        pool.starmap(extract_by_mask_rio, iter_params)
