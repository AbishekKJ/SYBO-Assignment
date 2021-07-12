"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from .ninjaspoilersbase import NinjaSpoilers

from utility import HTTPError, HTTPUnProcessableEntity, replace_decimals
from constant import DYNAMO_DB_BATCH_COUNT


class NinjaSpoilersUserFriends(NinjaSpoilers):

    def __init__(self, user_id):
        self.user_id = user_id
        self.aws_resource = self.get_aws_resource("dynamodb")
        self.validate_user_uuid_format(self.user_id)

    def update_friends(self, friends_data):
        """
        Updates user's friends detail to DB
        """
        if ["friends"] != sorted(friends_data):
            raise HTTPUnProcessableEntity(f"Invalid request. Request body should contain only the following keys - "
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
                "username": user_data.get("username")
            },
            UpdateExpression=user_data_update_statement,
            ExpressionAttributeValues=update_data
        )
        return {
            "message": "Friends list updated"
        }

    def get_friends(self, page_no=1, item_count=10):
        """
        Loads User friends game state and scores with Pagination of records
        """
        friends_data = []
        dynamo_resource = self.aws_resource
        user_table = dynamo_resource.Table("Users")
        user_data = self.get_user_by_id(user_table, self.user_id)
        if not user_data:
            raise HTTPError(404, "USER_DATA_NOT_FOUND")
        user_data = user_data[0]
        friends_list = user_data.get("friendsList", [])
        batch_friends_list = [friends_list[i:i + dynamo_db_batch_count] for i in range(0, len(friends_list),
                                                                                       dynamo_db_batch_count)]
        for ids in batch_friends_list:
            resp = dynamo_resource.batch_get_item(RequestItems={"Users": {
                "Keys": [{'id': friend_id} for friend_id in ids],
                "ProjectionExpression": "id, #name, highScore, createdAt",
                "ExpressionAttributeNames": {'#name': 'name'}
            }
            })
            friends_data.extend(resp.get("Responses", {}).get("Users", []))
        friends_data = replace_decimals(friends_data)
        sorted_data = sorted(friends_data, key=lambda i: i['createdAt'])
        start_range = (page_no - 1) * item_count
        end_range = page_no * item_count
        return {
            "friends": sorted_data[start_range:end_range]
        }
