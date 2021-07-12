"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from enum import Enum


class Resources(Enum):
    CREATE_USER = "/ninjaSpoilers/api/v1/user"
    LOAD_SAVE_GAME_STATE = "/ninjaSpoilers/api/v1/user/{userId}/state"
    UPDATE_GET_FRIENDS = "/ninjaSpoilers/api/v1/user/{userId}/friends"


dynamo_db_batch_count = 100
