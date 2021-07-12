"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

import unittest

from services.ninjaspoilersusergames import NinjaSpoilersUserGames
from services.ninjaspoilersusers import NinjaSpoilersUsers
from services.ninjaspoilersuserfriends import NinjaSpoilersUserFriends
from utility import HTTPUnProcessableEntity, HTTPError


class TestNinjaSpoilerServices(unittest.TestCase):
    """
    Unit test class for the api functions
    """

    def test_create_user(self):
        """
        Test Create user
        """
        user_obj = NinjaSpoilersUsers()
        user_list = ["Abishek", "Suganya", "Sudhakar", "Sathish", "Bref", "Vishnu"]
        for user in user_list:
            resp = user_obj.create_user({"name": user})
            assert isinstance(resp, dict)

    def test_get_all_users(self):
        """
        Test Create user
        """
        user_obj = NinjaSpoilersUsers()
        resp = user_obj.get_users()
        assert isinstance(resp, dict)

    def test_save_game_state(self):
        """
        Test Save Game state
        """
        save_game_state_obj = NinjaSpoilersUserGames("bb333e0d-e30b-11eb-8366-61eeb2b58c4c")
        score = 395
        for i in range(1, 2):
            score = score + 1
            game_data = {
                "gamesPlayed": i,
                "score": score
            }
            save_game_state_obj.save_game_state(game_data)

    def test_load_game_state(self):
        """
        Test Load Game state
        """
        load_game_state_obj = NinjaSpoilersUserGames("bb333e0d-e30b-11eb-8366-61eeb2b58c4c")
        resp = load_game_state_obj.load_game_state()
        assert isinstance(resp, dict)

    def test_update_friends(self):
        """
        Test Update Friends
        """
        update_obj = NinjaSpoilersUserFriends("bb333e0d-e30b-11eb-8366-61eeb2b58c4c")
        friends_data = {
            "friends": ["2cff1c23-e30c-11eb-a07a-61eeb2b58c4c",
                        "3957e152-e30c-11eb-9baf-61eeb2b58c4c",
                        "40e7dab7-e30c-11eb-a187-61eeb2b58c4c"
                        ]
        }
        resp = update_obj.update_friends(friends_data)
        assert isinstance(resp, dict)

    def test_get_friends(self):
        """
        Test Get Friends
        """
        get_obj = NinjaSpoilersUserFriends("bb333e0d-e30b-11eb-8366-61eeb2b58c4c")
        resp = get_obj.get_friends()
        assert isinstance(resp, dict)

    def test_create_user_error_validations(self):
        """
        Test Create user error validations
        """
        with self.assertRaises(HTTPUnProcessableEntity):
            user_obj = NinjaSpoilersUsers()
            resp = user_obj.create_user({"name": "Abishek"})

        with self.assertRaises(HTTPUnProcessableEntity):
            user_obj = NinjaSpoilersUsers()
            resp = user_obj.create_user({"names": "Abishek"})

        with self.assertRaises(HTTPUnProcessableEntity):
            user_obj = NinjaSpoilersUsers()
            resp = user_obj.create_user({"name": ""})

    def test_user_games_validations(self):
        """
        Test Create user games error validations
        """
        with self.assertRaises(HTTPUnProcessableEntity):
            user_obj = NinjaSpoilersUserGames("bb333e0d-e30b-11eb-8366-61eeb2b58c4c")
            resp = user_obj.save_game_state({})

        with self.assertRaises(HTTPUnProcessableEntity):
            user_obj = NinjaSpoilersUserGames("bb333e0d-e30b-11eb-8366-61eeb2b58c4c")
            resp = user_obj.save_game_state({"gamesPlayed": "",
                                             "score": 1})

        with self.assertRaises(HTTPUnProcessableEntity):
            user_obj = NinjaSpoilersUserGames("bb333e0d-e30b-11eb-8366-61eeb2b58c4c")
            resp = user_obj.save_game_state({"gamesPlayed": 1,
                                             "score": ""})

        with self.assertRaises(HTTPError):
            user_obj = NinjaSpoilersUserGames("bb333e0d-e30b-11eb-8366-61eeb2b57c4c")
            resp = user_obj.save_game_state({"gamesPlayed": 1,
                                             "score": 4})

    def test_user_friends_validations(self):
        """
        Test Create user friends error validations
        """
        with self.assertRaises(HTTPUnProcessableEntity):
            user_obj = NinjaSpoilersUserFriends("bb333e0d-e30b-11eb-8366-61eeb2b58c4c")
            friends_data = {
                "friendss": ["2cff1c23-e30c-11eb-a07a-61eeb2b58c4c"]
            }
            resp = user_obj.update_friends(friends_data)


if __name__ == '__main__':
    unittest.main()
