# -*- coding: utf-8 -*-
"""
Module for local reading and writing of data

"""

import json


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


def write_json(filename, data):
    """Write data to JSON file.

    Args:
        filename (str): Name of JSON file to write data to.
        data (list,tuple): Data to write to JSON file.

    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)
