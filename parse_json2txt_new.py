# -*- coding: utf-8 -*-
import os
import json

from argparse import ArgumentParser


def write_txt(out_file, content):
    with open(out_file, 'w') as fw:
        fw.write(content.encode('utf-8'))


def parse_params(input_json_file,
                 out_img_path='/tmp/img_path.txt',
                 out_max_zoom='/tmp/max_zoom.txt',
                 out_min_zoom='/tmp/min_zoom.txt',
                 ):
    """解析json参数,写出需要的参数到txt文件"""
    with open(input_json_file) as j:
        params_list = json.load(j)
        if len(params_list) > 1:
            print("Sorry, Only support 1 image currently!")
            exit(1)
        params = params_list[0]
        zoom_level = params['zoom']
        minmax_level = zoom_level.strip().split('-')
        try:
            print(params['img_path'])
            write_txt(out_img_path, params['img_path'])
            write_txt(out_max_zoom, minmax_level[1])
            write_txt(out_min_zoom, minmax_level[0])
        except KeyError:
            print("Some parameters do not exist. exit!")
            exit(1)


if __name__ == '__main__':

    # input_json_file = r'D:\temp11\params3.json'
    # parse_params(input_json_file, 'c:/tmp/img_path.txt', 'c:/tmp/max_zoom.txt', 'c:/tmp/min_zoom.txt',)
    
    parser = ArgumentParser()

    parser.add_argument('--input_json_file', required=True, help="json参数文件地址")
    parser.add_argument('--out_img_path', default="/tmp/img_path.txt",
                        help="输出img_path参数文件")
    parser.add_argument('--out_max_zoom', default="/tmp/max_zoom.txt",
                        help="输出最大切片级别参数文件")
    parser.add_argument('--out_min_zoom', default="/tmp/min_zoom.txt",
                        help="输出最小切片级别参数文件")

    args = parser.parse_args()
    
    parse_params(args.input_json_file, args.out_img_path, args.out_max_zoom,
                 args.out_min_zoom)
