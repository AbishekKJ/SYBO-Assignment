"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 10-Jul-2021
"""


class HTTPError(Exception):
    """
    Generic exception
    """
    __module__ = "CustomException"

    def __init__(self, status_code, error_msg):
        super().__init__()
        self.status = status_code
        self.error_msg = error_msg


class HTTPPreConditionFailed(Exception):
    """
    Custom exception to raise pre condition failed
    """
    __module__ = "CustomException"

    def __init__(self, error_msg):
        super().__init__()
        self.status = 412
        self.error_msg = error_msg


class HTTPUnProcessableEntity(Exception):
    """
    Custom exception to raise un processable entity
    """
    __module__ = "CustomException"

    def __init__(self, error_msg):
        super().__init__()
        self.status = 422
        self.error_msg = error_msg
