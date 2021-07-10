"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 10-Jul-2021
"""


class HTTPError(Exception):

    def __init__(self, status_code, error_msg):
        self.status = status_code
        self.error_msg = error_msg


class HTTPPreConditionFailed(Exception):

    def __init__(self, error_msg):
        self.status = 412
        self.error_msg = error_msg


class HTTPUnProcessableEntity(Exception):

    def __init__(self, error_msg):
        self.status = 422
        self.error_msg = error_msg
