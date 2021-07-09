"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from enum import Enum


class Resources(Enum):
    CREATE_USER = "/user"
    LOAD_SAVE_GAME_STATE = "/user/{userid}/state"
    UPDATE_GET_FRIENDS = "/user/{userid}/friends"


random_key_length = 20
