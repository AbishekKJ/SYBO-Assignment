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
from utility import HTTPError, HTTPPreConditionFailed


class NinjaSpoilersManager:
    """
    Manager class for all ninja services
    """

    def __init__(self, event, context):
        self.event = event
        self.context = context

    @staticmethod
    def validate_pagination_query_parameter(page_no, item_count):
        try:
            page_no = int(page_no)
            item_count = int(item_count)
        except ValueError:
            raise HTTPPreConditionFailed("Pagination Query params should be integer")
        except TypeError:
            raise HTTPPreConditionFailed("Pagination Query params should be integer")
        else:
            return page_no, item_count

    @staticmethod
    def validate_content_type_body(body, header):
        """
        Validate the body and header of the request
        """
        data = {}
        if not body:
            data = {
                "statusCode": 412,
                "error": "Request body cannot be empty"
            }
            return data
        for key in list(header.keys()):
            if key.lower() == "content-type":
                content_type = header.get(key, "")
                break
        print("Content-type", content_type)
        if content_type != "application/json":
            data = {
                "statusCode": 412,
                "error": "Invalid content type. Use content type application/json"
            }
        return data

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
        path_parameters = self.event.get("pathParameters")
        body = self.event.get("body", "")
        header = self.event.get("headers")
        try:
            if http_method in ["PUT", "POST"]:
                data = self.validate_content_type_body(body, header)
                if len(data):
                    raise HTTPPreConditionFailed(data.get("error"))
            if resource == Resources.CREATE_USER.value:
                manager_obj = NinjaSpoilersUsers()
                userdata = json.loads(body)
                data = manager_obj.create_user(userdata)
                response["body"] = json.dumps(data)
            elif resource == Resources.GET_ALL_USERS.value:
                manager_obj = NinjaSpoilersUsers()
                query_params = self.event.get("queryStringParameters", {})
                if query_params:
                    page_no = query_params.get("page")
                    item_count = query_params.get("perPage")
                    page_no, item_count = self.validate_pagination_query_parameter(page_no, item_count)
                    data = manager_obj.get_users(page_no, item_count)
                else:
                    data = manager_obj.get_users()
                response["body"] = json.dumps(data)
            elif resource == Resources.LOAD_SAVE_GAME_STATE.value:
                if path_parameters:
                    user_id = path_parameters.get("userId")
                    manager_obj = NinjaSpoilersUserGames(user_id)
                    if http_method == "GET":
                        data = manager_obj.load_game_state()
                    elif http_method == "PUT":
                        game_data = json.loads(body)
                        data = manager_obj.save_game_state(game_data)
                else:
                    raise HTTPError(400, "Bad request")
            elif resource == Resources.UPDATE_GET_FRIENDS.value:
                if path_parameters:
                    user_id = path_parameters.get("userId")
                    manager_obj = NinjaSpoilersUserFriends(user_id)
                    if http_method == "GET":
                        data = manager_obj.get_friends()
                    elif http_method == "PUT":
                        friends_data = json.loads(body)
                        data = manager_obj.update_friends(friends_data)
                else:
                    raise HTTPError(400, "Bad request")
        except Exception as e:
            if "__module__" in dir(e):
                if e.__module__ == "CustomException":
                    response["statusCode"] = e.status
                    data = {"error": e.error_msg}
                    response["body"] = json.dumps(data)
                    return response
            raise
        else:
            response["statusCode"] = 200
            response["body"] = json.dumps(data)
            return response
