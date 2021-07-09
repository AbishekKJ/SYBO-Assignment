"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

import random
import string
from abc import ABC

import boto3

from api_task.constant import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, random_key_length


def convert_key_case_to_camel_case(key):
    # split underscore using split
    temp = key.split('_')
    # joining result
    res = temp[0] + ''.join(ele.title() for ele in temp[1:])
    return res


class NinjaSpoilers(ABC):
    def __init__(self):
        pass

    @staticmethod
    def get_aws_resource(aws_resource):
        return boto3.resource(aws_resource,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region_name="us-east-1")

    @staticmethod
    def get_random_id(event_prefix):
        key_len = random_key_length - (len(event_prefix)+1)
        random_id = f"{event_prefix}_{''.join(random.choices(string.ascii_letters + string.digits, k=key_len))}"
        return random_id

    @staticmethod
    def prepare_update_db_statement(updated_key_list):
        statement = "SET"
        for key in updated_key_list:
            statement = f"{statement} {convert_key_case_to_camel_case(key)} = :{key},"
        return statement.rstrip(',')





