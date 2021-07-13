"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from uuid import uuid1
from datetime import datetime
from collections import OrderedDict

from utility import HTTPUnProcessableEntity, replace_decimals
from .ninjaspoilersbase import NinjaSpoilers


class NinjaSpoilersUsers(NinjaSpoilers):
    """
    Create user class
    """

    def __init__(self):
        super().__init__()
        self.aws_resource = self.get_aws_resource("dynamodb")

    def create_user(self, name_data):
        """
        Create user method
        """
        if ["name"] != sorted(name_data):
            raise HTTPUnProcessableEntity(f"Invalid request. "
                                          f"Request body should contain only the following keys - "
                                          f"{','.join(['name'])}")
        name = name_data.get("name", "")
        if not name.isalnum():
            raise HTTPUnProcessableEntity("name should be alphanumeric")
        if len(name) > 20:
            raise HTTPUnProcessableEntity("name can be maximum of 20 characters")
        user_table = self.aws_resource.Table("Users")
        user_data = user_table.get_item(Key={
            "userName": name
        })
        user_data = user_data.get("Item", {})
        if user_data:
            raise HTTPUnProcessableEntity("name already taken")
        user_id = str(uuid1())
        user_data = {
            "id": user_id,
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "userName": name,
            "scores": [],
            "gamesPlayed": [],
            "friendsList": [],
            "highScore": 0
        }
        user_table.put_item(Item=user_data)
        return {"id": user_id, "name": name}

    def get_users(self, page_no=None, item_count=None):
        user_table = self.aws_resource.Table("Users")
        response = user_table.scan()
        data = response['Items']
        sorted_data = sorted(data, key=lambda k: k['createdAt'])
        display_list = ["id", "userName"]
        sorted_data = [{k: v for k, v in d.items() if k in display_list} for d in sorted_data]
        sorted_data = replace_decimals(sorted_data)
        order_data_list = []
        for i in sorted_data:
            order_data = OrderedDict()
            order_data['id'] = i.get("id")
            order_data['name'] = i.get("userName")
            order_data_list.append(order_data)
        if page_no and item_count:
            start_range = (page_no - 1) * item_count
            end_range = page_no * item_count
            return {
                "users": order_data_list[start_range:end_range],
                "totalCount": len(order_data_list)
            }
        else:
            return {
                "users": order_data_list
            }
