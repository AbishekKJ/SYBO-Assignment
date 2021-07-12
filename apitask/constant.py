"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from enum import Enum


class Resources(Enum):
    """
    Resource path values
    """
    CREATE_USER = "/ninjaSpoilers/api/v1/user"
    GET_ALL_USERS = "/ninjaSpoilers/api/v1/users"
    LOAD_SAVE_GAME_STATE = "/ninjaSpoilers/api/v1/user/{userId}/state"
    UPDATE_GET_FRIENDS = "/ninjaSpoilers/api/v1/user/{userId}/friends"


DYNAMO_DB_BATCH_COUNT = 100
