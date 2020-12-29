# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 17:56:28 2020

@author: mlm
"""
from argparse import ArgumentParser
import xml.etree.ElementTree as ET

import rasterio
import rasterio.warp

from rtree import index

from io_utils import get_image_file


def build_index(ref_doms):
    """利用输入的数据建立空间索引(RTREE)."""
    # idx = index.Rtree('d:/rtree')
    idx = index.Index()
    for i, r in enumerate(ref_doms):
        print(r)
        ds = rasterio.open(r)
        bound = ds.bounds
        print(bound)
        trans_bd = rasterio.warp.transform_bounds('EPSG:4326', 'EPSG:4326',
                                                  bound.left, bound.bottom,
                                                  bound.right, bound.top)
        print(trans_bd)
        idx.insert(i, tuple(ds.bounds))
    return idx


def get_bounds_from_xml(input_file):
    """从元数据中获取范围(left, bottom, right, top)."""
    meta_xml = input_file.replace('.tiff', '.xml')
    tree = ET.parse(meta_xml)
    root = tree.getroot()
    def get_coordinate(pos):
        """lambda x: float(root.find(x).text)"""
        return float(root.find(pos).text)

    lats = list(map(get_coordinate, ['TopLeftLatitude', 'TopRightLatitude',
                                     'BottomRightLatitude', 'BottomLeftLatitude']))
    lons = list(map(get_coordinate, ['TopLeftLongitude', 'TopRightLongitude',
                                     'BottomRightLongitude', 'BottomLeftLongitude']))

    return (min(lons), min(lats), max(lons), max(lats))


def get_intersect_files(ref_doms, in_r):
    """"""
    # ref_doms = get_image_file(ref_dom_dir)
    idx = build_index(ref_doms)
    bound = get_bounds_from_xml(in_r)
    return list(idx.intersection(bound, objects="raw"))  # , objects="raw"


if __name__ == '__main__':
    ref_dom_dir = r'D:\temp\reference-dom'
    in_r = r'D:\work\data\影像样例\GF2\GF2_PMS1_E108.9_N34.2_20181026_L1A0003549596\GF2_PMS1_E108.9_N34.2_20181026_L1A0003549596-MSS1.tiff'
    import time
    start_time = time.time()
    
    ref_doms = get_image_file(ref_dom_dir)
    
    # idx = build_index(ref_doms)
    idx = index.Rtree(r'd:/rtree/rtree')
    bound = get_bounds_from_xml(in_r)
    idxs = list(idx.intersection(bound))
    print([ref_doms[i] for i in idxs])
    print(time.time() - start_time)

    # parser = ArgumentParser()

    # parser.add_argument('--ref_dom_dir', required=True,
    #                    help="参考文件目录")
    # parser.add_argument('--input_raster', required=True,
    #                    help="输入栅格文件")

    # args = parser.parse_args()

    # ref_doms = get_image_file(args.ref_dom_dir)
    # dom_idx = get_intersect_files(ref_doms, args.input_raster)

    # print([ref_doms[i] for i in dom_idx])





