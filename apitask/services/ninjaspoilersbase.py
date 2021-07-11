"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from abc import ABC
from uuid import uuid1

import boto3

from ..utility import convert_key_case_to_camel_case


class NinjaSpoilers(ABC):
    def __init__(self):
        pass

    @staticmethod
    def get_aws_resource(aws_resource):
        return boto3.resource(aws_resource)

    @staticmethod
    def get_random_id(event_prefix):
        random_id = f"{event_prefix}_{uuid1().hex}"
        return random_id

    @staticmethod
    def prepare_update_db_statement(updated_key_list):
        statement = "SET"
        updated_key_list = [key.lstrip(":") for key in updated_key_list]
        for key in updated_key_list:
            statement = f"{statement} {convert_key_case_to_camel_case(key)} = :{key},"
        return statement.rstrip(',')
