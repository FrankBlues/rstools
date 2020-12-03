# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:08:49 2020

命令行工具
@author: mlm
"""


def trans_none(value):
    """处理前端传过来的字符型空值, 如果参数为字符型None/none, 转换为python语言中的None值."""
    if value in ['None', 'none', '']:
        value = None
    return value


def trans_numbers(value):
    """处理前端传过来的字符型数字,如果参数为字符型None/none, 转换为python语言中的None值,
    否则转换为float型"""
    v = trans_none(value)
    if v is not None:
        v = float(v)
    return v
