"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

import unittest

from apitask.services import *


class TestNinjaSpoilerServices(unittest.TestCase):

    def test_create_user(self):
        user_obj = NinjaSpoilersUsers()
        resp = user_obj.create_user("Abishek")
        assert isinstance(resp, dict)

    def test_save_game_state(self):
        pass

    def test_load_game_state(self):
        pass


if __name__ == '__main__':
    unittest.main()
