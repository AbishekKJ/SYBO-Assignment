"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from ninjaspoilersbase import NinjaSpoilers
from uuid import UUID


class NinjaSpoilersUserGames(NinjaSpoilers):

    def __init__(self, user_id):
        self.user_id = user_id
        self.aws_resource = self.get_aws_resource("dynamodb")

    def save_game_state(self, game_data):
        user_table = self.aws_resource.Table("Users")
        games_table = self.aws_resource.Table("Games")
        game_id = self.get_random_id("game")
        user_data = user_table.get_item(Key={
            'id': UUID(self.user_id).hex,
        })
        user_data = user_data.get("Item")
        if user_data:
            updated_user_data = {}
            scores = user_data.get("scores")
            games_played = user_data.get("gamesPlayed")
            high_score = user_data.get("highScore")
            games_played.append({"gameId": game_id,
                                 "id": game_data.get("gamesPlayed")})
            if game_data.get("score") > high_score:
                high_score = game_data.get("score")
                updated_user_data["highScore"] = high_score
            scores.append(game_data.get("score"))

        updated_user_data.update({
            "scores": scores,
            "gamesPlayed": games_played

        })
        user_data_update_statement = self.prepare_update_db_statement(list(updated_user_data.keys()))
        user_table.update_item(
            Key={
                "id": UUID(self.user_id).hex
            },
            UpdateExpression=user_data_update_statement,
            ExpressionAttributeValues=updated_user_data
        )
        game_details = {
            "id": game_id,
            "usedId": UUID(self.user_id).hex,
            "score": game_data.get("score")
        }
        games_table.put_item(game_details)

    def load_game_state(self):
        user_table = self.aws_resource.Table("Users")
        user_data = user_table.get_item(Key={
            'id': UUID(self.user_id).hex,
        })
        user_data = user_data.get("Item")
        if user_data:
            return {"gamesPlayed": len(user_data.get("gamesPlayed")),
                    "score": user_data.get("highScore")}

