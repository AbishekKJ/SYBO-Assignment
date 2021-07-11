"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from ..services import NinjaSpoilers
from uuid import uuid1
from datetime import datetime


class NinjaSpoilersUsers(NinjaSpoilers):

    def __init__(self):
        self.aws_resource = self.get_aws_resource("dynamodb")

    def create_user(self, name):
        table = self.aws_resource.Table("Users")
        user_id = str(uuid1())
        user_data = {
            "id": user_id,
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "scores": [],
            "gamesPlayed": [],
            "friendsList": [],
            "highScore": 0
        }
        table.put_item(Item=user_data)
        return {"id": user_id, "name": name}
