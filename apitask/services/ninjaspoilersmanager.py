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
        """
        Manager class for all the ninja spoilers feature classes
        """
        response = {"headers": {
            'Access-Control-Allow-Origin': '*'
        }}
        print("Event object", self.event)
        resource = self.event.get("resource", "")
        http_method = self.event.get("httpMethod")
        if http_method in ["PUT", "POST"]:
            header = self.event.get("headers")
            for key in list(header.keys()):
                if key.lower() == "content-type":
                    content_type = header.get(key, "")
                    break
            print("Content-type", content_type)
            if content_type != "application/json":
                response["statusCode"] = 412
                data = {
                    "error": "Invalid content type. Use content type application/json"
                }
                response["body"] = json.dumps(data)
                return response
        try:
            if resource == Resources.CREATE_USER.value:
                manager_obj = NinjaSpoilersUsers()
                body = json.loads(self.event.get("body", {}))
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
                    if http_method == "GET":
                        data = manager_obj.load_game_state()
                        response["statusCode"] = 200
                    elif http_method == "PUT":
                        game_data = self.event.get("body")
                        if game_data:
                            game_data = json.loads(game_data)
                            data = manager_obj.save_game_state(game_data)
                            response["statusCode"] = 200
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
                    if http_method == "GET":
                        query_params = self.event.get("queryStringParameters", {})
                        if query_params:
                            page_no = query_params.get("pageNo")
                            item_count = query_params.get("itemCount")
                            data = manager_obj.get_friends(page_no, item_count)
                        else:
                            data = manager_obj.get_friends()
                        response["statusCode"] = 200
                    elif http_method == "PUT":
                        friends_data = self.event.get("body")
                        if friends_data:
                            friends_data = json.loads(friends_data)
                            data = manager_obj.update_friends(friends_data)
                            response["statusCode"] = 200
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
        except Exception as e:
            if "__module__" in dir(e):
                if e.__module__ == "CustomException":
                    response["statusCode"] = e.status
                    data = {"error": e.error_msg}
                    response["body"] = json.dumps(data)
                    return response
            raise
