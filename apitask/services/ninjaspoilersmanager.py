"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

import json
from services.ninjaspoilersusergames import NinjaSpoilersUserGames
from services.ninjaspoilersusers import NinjaSpoilersUsers
from services.ninjaspoilersuserfriends import NinjaSpoilersUserFriends
from constant import Resources


class NinjaSpoilersManager:

    def __init__(self, event, context):
        self.event = event
        self.context = context

    def run(self):
        response = {"headers": {
            'Access-Control-Allow-Origin': '*'
        }}
        resource = self.event.get("resource", "")
        print("Event", self.event)
        if resource == Resources.CREATE_USER.value:
            manager_obj = NinjaSpoilersUsers()
            body = self.event.get("body", {})
            name = body.get("name", "")
            if name:
                data = manager_obj.create_user(name)
                response["statusCode"] = 200
            else:
                response["statusCode"] = 422
                data = {
                    "error": "Name should be valid"
                }
            response["body"] = json.dumps(data)
            return response
        elif resource == Resources.LOAD_SAVE_GAME_STATE.value:
            path_parameters = self.event.get("pathParameters")
            if path_parameters:
                user_id = path_parameters.get("userId")
                manager_obj = NinjaSpoilersUserGames(user_id)
                http_method = self.event.get("httpMethod")
                if http_method == "GET":
                    data = manager_obj.load_game_state()
                elif http_method == "PUT":
                    game_data = self.event.get("body")
                    if game_data:
                        data = manager_obj.save_game_state(game_data)
                    else:
                        response["statusCode"] = 422
                        data = {
                            "error": "Request body cannot be empty"
                        }
            else:
                response["statusCode"] = 422
                data = {
                    "error": "User id should be valid"
                }
            response["body"] = json.dumps(data)
            return response
        elif resource == Resources.UPDATE_GET_FRIENDS.value:
            path_parameters = self.event.get("pathParameters")
            if path_parameters:
                user_id = path_parameters.get("userId")
                manager_obj = NinjaSpoilersUserFriends(user_id)
                http_method = self.event.get("httpMethod")
                if http_method == "GET":
                    data = manager_obj.get_friends()
                elif http_method == "PUT":
                    friends_data = self.event.get("body")
                    if friends_data:
                        data = manager_obj.update_friends(friends_data)
                    else:
                        response["statusCode"] = 422
                        data = {
                            "error": "Request body cannot be empty"
                        }
            else:
                response["statusCode"] = 422
                data = {
                    "error": "User id should be valid"
                }
            response["body"] = json.dumps(data)
            return response
