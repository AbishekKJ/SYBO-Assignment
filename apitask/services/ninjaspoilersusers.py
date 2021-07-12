"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

import re
from uuid import uuid1
from datetime import datetime

from utility import HTTPUnProcessableEntity
from .ninjaspoilersbase import NinjaSpoilers


class NinjaSpoilersUsers(NinjaSpoilers):
    """"""
    def __init__(self):
        self.aws_resource = self.get_aws_resource("dynamodb")

    def create_user(self, name):
        if not name.isalnum():
            raise HTTPUnProcessableEntity("name should be alphanumeric")
        user_table = self.aws_resource.Table("Users")
        user_data = user_table.get_item(Key={
           "username": name
        })
        user_data = user_data.get("Item", {})
        if user_data:
            raise HTTPUnProcessableEntity("name already taken")
        user_id = str(uuid1())
        user_data = {
            "id": user_id,
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": name,
            "scores": [],
            "gamesPlayed": [],
            "friendsList": [],
            "highScore": 0
        }
        user_table.put_item(Item=user_data)
        return {"id": user_id, "name": name}
