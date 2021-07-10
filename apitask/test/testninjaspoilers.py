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
        save_game_state_obj = NinjaSpoilersUserGames("aec3d5c9-06f3-4c18-b723-4e933de58a5b")
        score = 395
        for i in range(1, 100):
            score = score + 1
            game_data = {
                "gamesPlayed": i,
                "score": score
            }
            save_game_state_obj.save_game_state(game_data)

    def test_load_game_state(self):
        load_game_state_obj = NinjaSpoilersUserGames("aec3d5c9-06f3-4c18-b723-4e933de58a5b")
        resp = load_game_state_obj.load_game_state()
        assert isinstance(resp, dict)


if __name__ == '__main__':
    unittest.main()
