# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 15:55:37 2020

@author: mlm
"""

from argparse import ArgumentParser

from rstools.config_tool import create_band_def_json


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--b1', required=True,
                        help="第一个波段,格式为'image_file,band_index'.")
    parser.add_argument('--b2', required=True,
                        help="第二个波段.")
    parser.add_argument('--b3', default='',
                        help="第三个波段,为' '、''、none、None时表示为空.")
    parser.add_argument('--other_bands', default='',
                        help="其它波段,如果有多个时用';'隔开.")
    parser.add_argument('--out_config', default='/tmp/band_def.json',
                        help="输出波段定义的配置文件.")

    args = parser.parse_args()

    create_band_def_json(args.b1, args.b2, args.b3, args.other_bands,
                         args.out_config)
