"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

import unittest

from services.ninjaspoilersusergames import NinjaSpoilersUserGames
from services.ninjaspoilersusers import NinjaSpoilersUsers
from services.ninjaspoilersuserfriends import NinjaSpoilersUserFriends


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
            resp = user_obj.create_user(user)
            assert isinstance(resp, dict)

    def test_save_game_state(self):
        """
        Test Save Game state
        """
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
        """
        Test Load Game state
        """
        load_game_state_obj = NinjaSpoilersUserGames("5dc50172-e18b-11eb-84da-3cf011dfc659")
        resp = load_game_state_obj.load_game_state()
        assert isinstance(resp, dict)

    def test_update_friends(self):
        """
        Test Update Friends
        """
        update_obj = NinjaSpoilersUserFriends("5dc50172-e18b-11eb-84da-3cf011dfc659")
        friends_data = {
            "friends": ["5f3b4a0c-e18b-11eb-84da-3cf011dfc659",
                        "5f3b4a0d-e18b-11eb-84da-3cf011dfc659",
                        "5f3b4a0e-e18b-11eb-84da-3cf011dfc659",
                        "5fe9ad40-e18b-11eb-84da-3cf011dfc659",
                        "5fe9ad41-e18b-11eb-84da-3cf011dfc659"]
        }
        resp = update_obj.update_friends(friends_data)
        assert isinstance(resp, dict)

    def test_get_friends(self):
        """
        Test Get Friends
        """
        get_obj = NinjaSpoilersUserFriends("5dc50172-e18b-11eb-84da-3cf011dfc659")
        resp = get_obj.get_friends()
        assert isinstance(resp, dict)


if __name__ == '__main__':
    unittest.main()
