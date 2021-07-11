"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

import decimal
from uuid import UUID


def convert_key_case_to_camel_case(key):
    """
    Convert snake case to camel case
    """
    # split underscore using split
    temp = key.split('_')
    res = temp[0] + ''.join(ele.title() for ele in temp[1:])
    return res


def replace_decimals(obj):
    """
    Convert all whole number decimals in `obj` to integers
    """
    if isinstance(obj, list):
        return [replace_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: replace_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else obj
    return obj


def convert_hex_to_uuid(hex_value):
    """
    Convert hex value string to valid UUID string
    """
    return str(UUID(hex_value))
