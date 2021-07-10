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
        user_list = ["Abishek", "Suganya", "Sudhakar", "Sathish", "Bref", "Vishnu"]
        for user in user_list:
            resp = user_obj.create_user(user)
            assert isinstance(resp, dict)

    def test_save_game_state(self):
        save_game_state_obj = NinjaSpoilersUserGames("5dc50172-e18b-11eb-84da-3cf011dfc659")
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

    def test_update_friends(self):
        update_obj = NinjaSpoilersUserFriends("aec3d5c9-06f3-4c18-b723-4e933de58a5b")
        friends_data = {
            "friends": ["31896d4e-e179-11eb-84da-3cf011dfc659",
                        "35dc2198-e179-11eb-84da-3cf011dfc659",
                        "3b068aa0-e179-11eb-84da-3cf011dfc659",
                        "3dc9623a-e179-11eb-84da-3cf011dfc659"]
        }
        resp = update_obj.update_friends(friends_data)
        assert isinstance(resp, dict)

    def test_get_friends(self):
        get_obj = NinjaSpoilersUserFriends("aec3d5c9-06f3-4c18-b723-4e933de58a5b")
        resp = get_obj.get_friends()
        assert isinstance(resp, dict)


if __name__ == '__main__':
    unittest.main()
