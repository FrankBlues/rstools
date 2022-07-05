# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:09:22 2022
根据输入影像范围生成对应的网格，默认网格大小10000*10000当前影像像素，
范围缓存5%。
@author: menglimeng
"""
import os
from math import ceil
from argparse import ArgumentParser

from osgeo import gdal
from osgeo import ogr


def extent2grid(outputGridfn,xmin,xmax,ymin,ymax,gridHeight,gridWidth, SpatialReference=None):
    """Generate grid(shapefile)"""
    xmin = float(xmin)
    xmax = float(xmax)
    ymin = float(ymin)
    ymax = float(ymax)
    gridWidth = float(gridWidth)
    gridHeight = float(gridHeight)

    # get rows
    rows = ceil((ymax-ymin)/gridHeight)
    # get columns
    cols = ceil((xmax-xmin)/gridWidth)

    # start grid cell envelope
    ringXleftOrigin = xmin
    ringXrightOrigin = xmin + gridWidth
    ringYtopOrigin = ymax
    ringYbottomOrigin = ymax-gridHeight

    # create output file
    outDriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(outputGridfn):
        os.remove(outputGridfn)
    outDataSource = outDriver.CreateDataSource(outputGridfn)
    outLayer = outDataSource.CreateLayer(outputGridfn,SpatialReference, geom_type=ogr.wkbPolygon)
    outLayer.CreateField(ogr.FieldDefn('NewMapNo',ogr.OFTString))
    featureDefn = outLayer.GetLayerDefn()

    # create grid cells
    countcols = 0
    while countcols < cols:
        countcols += 1

        # reset envelope for rows
        ringYtop = ringYtopOrigin
        ringYbottom =ringYbottomOrigin
        countrows = 0

        while countrows < rows:
            countrows += 1
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)

            # add new geom to layer
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(poly)
            outFeature.SetField("NewMapNo", f"grid_{countcols:04d}_{countrows:04d}")
            outLayer.CreateFeature(outFeature)
            outFeature.Destroy

            # new envelope for next poly
            ringYtop = ringYtop - gridHeight
            ringYbottom = ringYbottom - gridHeight

        # new envelope for next poly
        ringXleftOrigin = ringXleftOrigin + gridWidth
        ringXrightOrigin = ringXrightOrigin + gridWidth

    # Close DataSources
    outDataSource.Destroy()


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--ref_raster', required=True, help="参考DOM")
    parser.add_argument('--out_shp', required=True, help="输出shp")
    parser.add_argument('--grid_width_pixel', default='10000', help="网格宽")
    parser.add_argument('--grid_height_pixel', default='10000', help="网格高")
    
    options = parser.parse_args()
    output_shp = options.out_shp
    
    ds = gdal.Open(options.ref_raster)
    # SpatialReference
    sr = ds.GetSpatialRef()
    
    # extent
    geotransform = ds.GetGeoTransform()
    xmin, res_x, _, ymax, _, res_y = geotransform
    
    cols, rows = (ds.RasterXSize, ds.RasterYSize)
    
    buffer_x = cols * res_x * 0.05
    buffer_y = abs(rows * res_y * 0.05)
    
    xmin, xmax = (xmin-buffer_x, xmin + cols * res_x * 1.05)
    ymin, ymax = (ymax + rows * res_y * 1.05, ymax + buffer_y)

    # grid width and height
    gridHeight, gridWidth = (int(options.grid_width_pixel) * res_x, 
                             abs(int(options.grid_height_pixel) * res_y))
    
    # 检查/创建输出文件所在目录
    dirname = os.path.dirname(options.out_shp)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    extent2grid(output_shp, xmin, xmax, ymin, ymax, gridHeight, gridWidth, sr)

    # 检查结果文件是否生成
    # check_file_exist(options.out_shp)