"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from ninjaspoilersbase import NinjaSpoilers
from uuid import uuid4
from datetime import datetime


class NinjaSpoilersUsers(NinjaSpoilers):

    def __init__(self):
        self.aws_resource = self.get_aws_resource("dynamodb")

    def create_user(self, name):
        table = self.aws_resource.Table("Users")
        user_id = uuid4()
        user_data = {
            "id": user_id.hex,
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "scores": [],
            "gamesPlayed": [],
            "friendsList": [],
            "highScore": ""
        }
        table.put_item(Item=user_data)
        return {"id": user_id, "name": name}
