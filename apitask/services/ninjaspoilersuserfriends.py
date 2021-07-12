"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from utility import HTTPError, HTTPUnProcessableEntity, replace_decimals
from constant import DYNAMO_DB_BATCH_COUNT

from .ninjaspoilersbase import NinjaSpoilers


class NinjaSpoilersUserFriends(NinjaSpoilers):
    """
    Update and retrieve friends details class
    """

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.aws_resource = self.get_aws_resource("dynamodb")
        self.validate_user_uuid_format(self.user_id)

    def update_friends(self, friends_data):
        """
        Updates user's friends detail to DB
        """
        if ["friends"] != sorted(friends_data):
            raise HTTPUnProcessableEntity(f"Invalid request. "
                                          f"Request body should contain only the following keys - "
                                          f"{','.join(['friends'])}")
        if not isinstance(friends_data.get("friends"), list):
            raise HTTPUnProcessableEntity(f"Invalid request. friends should be a list of id's")

        friends_id = friends_data.get("friends")
        for ids in friends_id:
            self.validate_user_uuid_format(ids, True)
        user_table = self.aws_resource.Table("Users")
        user_data = self.get_user_by_id(user_table, self.user_id)
        if not user_data:
            raise HTTPError(404, "DATA_NOT_FOUND")
        user_data = user_data[0]
        # friends_list = user_data.get("friendsList", [])
        # friends_list.extend(friends_data.get("friends"))
        friends_list = friends_data.get("friends")
        update_data = {
            ":friends_list": friends_list
        }
        user_data_update_statement = self.prepare_update_db_statement(list(update_data.keys()))
        user_table.update_item(
            Key={
                "userName": user_data.get("username")
            },
            UpdateExpression=user_data_update_statement,
            ExpressionAttributeValues=update_data
        )
        return {
            "message": "Friends list updated"
        }

    def get_friends(self):
        """
        Loads User friends game state and scores with Pagination of records
        """
        friends_details = []
        dynamo_resource = self.aws_resource
        user_table = dynamo_resource.Table("Users")
        user_data = self.get_user_by_id(user_table, self.user_id)
        if not user_data:
            raise HTTPError(404, "USER_DATA_NOT_FOUND")
        user_data = user_data[0]
        friends_list = user_data.get("friendsList", [])
        friends_data = []
        friends_data_not_found_list = []
        for ids in friends_list:
            data = self.get_user_by_id(user_table, ids)
            if data:
                friends_data.append(data[0])
            else:
                friends_data_not_found_list.append(ids)
        # if friends_data_not_found_list:
        #     raise HTTPUnProcessableEntity(f"No data found for the friends "
        #                                   f"ids-{','.join(friends_data_not_found_list)}")

        batch_friends_list = [friends_data[i:i + DYNAMO_DB_BATCH_COUNT]
                              for i in range(0, len(friends_data), DYNAMO_DB_BATCH_COUNT)]
        for ids in batch_friends_list:
            resp = dynamo_resource.batch_get_item(RequestItems={"Users": {
                "Keys": [{'userName': friend_id.get("username")} for friend_id in ids],
                "ProjectionExpression": "id, userName, highScore, createdAt"
            }
            })
            print("Response, resp")
            friends_details.extend(resp.get("Responses", {}).get("Users", []))
        friends_details = replace_decimals(friends_details)
        sorted_data = sorted(friends_details, key=lambda i: i['createdAt'])
        sorted_data = [{k: v for k, v in d.items() if k != 'createdAt'} for d in sorted_data]
        return {
            "friends": sorted_data
        }
