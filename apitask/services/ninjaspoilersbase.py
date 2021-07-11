"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from abc import ABC
from uuid import uuid1, UUID

import boto3

from utility import convert_key_case_to_camel_case, HTTPUnProcessableEntity


class NinjaSpoilers(ABC):
    def __init__(self):
        pass

    @staticmethod
    def get_aws_resource(aws_resource):
        """
        Returns AWS resource connection object
        """
        return boto3.resource(aws_resource)

    @staticmethod
    def get_random_id(event_prefix):
        """
        Generates random id for unique key
        """
        random_id = f"{event_prefix}_{uuid1().hex}"
        return random_id

    @staticmethod
    def prepare_update_db_statement(updated_key_list):
        """
        Prepares the set expression statement for the keys passed
        """
        statement = "SET"
        updated_key_list = [key.lstrip(":") for key in updated_key_list]
        for key in updated_key_list:
            statement = f"{statement} {convert_key_case_to_camel_case(key)} = :{key},"
        return statement.rstrip(',')

    @staticmethod
    def validate_user_uuid_format(user_id, user_friends=False):
        """
        Validate the uuid1 format for the id's passed
        """
        try:
            UUID(user_id)
        except ValueError:
            if user_friends:
                message = "Incorrect UUID in friendsId"
            else:
                message = "Incorrect UUID in UserId"
        raise HTTPUnProcessableEntity(message)
