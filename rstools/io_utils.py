# -*- coding: utf-8 -*-
"""
Module for local reading and writing of data

"""
import os
from pathlib import Path
import json


def check_file_exist(file_name):
    """判断文件是否已经存在"""
    if os.path.isfile(file_name):
        return True
    else:
        return False


def check_parent_dir(file_name):
    """检查文件父目录是否存在,如果不存在则创建."""
    path = os.path.dirname(file_name)
    if not os.path.exists(path) and path.strip():
        try:
            os.makedirs(path)
        except FileExistsError:
            print("WARNING: Directory already exists")


def read_json(filename):
    """Read data from JSON file.

    Args:
        filename (str): Name of JSON file to be read.

    Returns:
        dict: Data stored in JSON file.

    """
    with open(filename, 'r') as file:
        return json.load(file)


def write_text(filename, data, add=False):
    """Write image data to text file.

    Args:
        filename (str): Name of text file to write data to.
        data (numpy ndarray): Image data to write to file.
        add (bool): Whether or not to append to existing file or not.
                Default is ``False``.

    """
    write_type = 'a' if add else 'w'
    with open(filename, write_type) as file:
        file.write(data)


def write_list(contents, out_file):
    """将列表中内容写进文本文件,每行对应列表中的一项.
    
    Args:
        contents (list):列表.
    
    """
    if check_file_exist(out_file):
        os.remove(out_file)
    check_parent_dir(out_file)
    with open(out_file, 'a') as f:
        for line in contents:
            f.write(line + '\n')


def read_list(list_file):
    """从文本文件读取每一行作为列表一项."""
    with open(list_file) as f:
        lines = f.readlines()
        return [l.rstrip('\n') for l in lines]


def write_json(filename, data):
    """Write data to JSON file.

    Args:
        filename (str): Name of JSON file to write data to.
        data (list,tuple): Data to write to JSON file.

    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


def get_image_file(path,
                   extensions=['tif', 'img', 'tiff', 'TIF', 'IMG', 'TIFF']):
    """List all files within a directory with the given extensions."""
    img_files = []
    for ext in extensions:
        file_found = Path(path).glob('**/*.{}'.format(ext))
        for f in file_found:
            f_str = str(f)
            if f_str not in img_files:
                img_files.append(f_str)
    return img_files
