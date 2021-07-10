"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from apitask.services import NinjaSpoilers
from uuid import UUID

from apitask.utility.exception import HTTPError
from apitask.constant import dynamo_db_batch_count


class NinjaSpoilersUserFriends(NinjaSpoilers):

    def __init__(self, user_id):
        self.user_id = user_id
        self.aws_resource = self.get_aws_resource("dynamodb")

    def update_friends(self, friends_data):
        user_table = self.aws_resource.Table("Users")
        user_data = user_table.get_item(Key={
            'id': UUID(self.user_id).hex,
        })
        user_data = user_data.get("Item")
        if not user_data:
            raise HTTPError(404, "DATA_NOT_FOUND")
        if user_data:
            friends_list = user_data.get("friendsList", [])
            friends_list.extend([UUID(i).hex for i in friends_data.get("friends")])
            update_data = {
                ":friends_list": friends_list
            }
            user_data_update_statement = self.prepare_update_db_statement(list(update_data.keys()))
            user_table.update_item(
                Key={
                    "id": UUID(self.user_id).hex
                },
                UpdateExpression=user_data_update_statement,
                ExpressionAttributeValues=update_data
            )
            return {
                "message": "Friends list updated"
            }

    def get_friends(self, page_no=1, item_count=10):
        friends_data = []
        dynamo_resource = self.aws_resource
        user_table = dynamo_resource.Table("Users")
        user_data = user_table.get_item(Key={
            'id': UUID(self.user_id).hex,
        })
        user_data = user_data.get("Item")
        if not user_data:
            raise HTTPError(404, "USER_DATA_NOT_FOUND")
        if user_data:
            friends_list = user_data.get("friendsList", [])
            batch_friends_list = [friends_list[i:i + dynamo_db_batch_count] for i in range(0, len(friends_list),
                                                                                           dynamo_db_batch_count)]
            for ids in batch_friends_list:
                resp = dynamo_resource.batch_get_item(RequestItems={"Users": {
                    "Keys": [{'id': friend_id} for friend_id in ids]
                }
                })
                friends_data.append(resp.get("Responses"))
