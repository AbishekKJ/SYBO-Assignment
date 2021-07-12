"""
Project: NinjaSpoilers
Author: Abishek KJ
Date: 09-Jul-2021
"""

from utility import HTTPError, HTTPUnProcessableEntity, replace_decimals
from .ninjaspoilersbase import NinjaSpoilers


class NinjaSpoilersUserGames(NinjaSpoilers):
    """
    Load and Save game state class for user
    """
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.aws_resource = self.get_aws_resource("dynamodb")
        self.validate_user_uuid_format(self.user_id)

    def save_game_state(self, game_data):
        """
        Save user game state to db
        """
        if ["gamesPlayed", "score"] != sorted(game_data):
            raise HTTPUnProcessableEntity(f"Invalid request. Request body should contain only the following keys - "
                                          f"{','.join(['gamesPlayed', 'score'])}")
        if not isinstance(game_data.get("gamesPlayed"), int):
            raise HTTPUnProcessableEntity(f"gamesPlayed should be integer")
        if not isinstance(game_data.get("score"), int):
            raise HTTPUnProcessableEntity(f"score should be integer")

        user_table = self.aws_resource.Table("Users")
        games_table = self.aws_resource.Table("Games")
        high_score_table = self.aws_resource.Table("HighScore")
        user_data = self.get_user_by_id(user_table, self.user_id)
        if not user_data:
            raise HTTPError(404, "DATA_NOT_FOUND")
        user_data = user_data[0]
        updated_user_data = {}
        scores = user_data.get("scores")
        games_played = user_data.get("gamesPlayed")
        high_score = user_data.get("highScore")
        if len(games_played) < game_data.get("gamesPlayed"):
            game_id = self.get_random_id("game")
            games_played.append({"gameId": game_id,
                                "id": game_data.get("gamesPlayed")})
            updated_user_data[":games_played"] = games_played
            scores.append(game_data.get("score"))
            updated_user_data[":scores"] = scores
        else:
            game_index = {games_played[i].get("id"): i for i in range(0, len(games_played))}
            scores[game_index.get(game_data.get("gamesPlayed"))] = game_data.get("score")
            updated_user_data[":scores"] = scores
        if high_score:
            if game_data.get("score") > high_score:
                high_score = game_data.get("score")
                updated_user_data[":high_score"] = high_score
        else:
            high_score = game_data.get("score")
            updated_user_data[":high_score"] = high_score
        user_data_update_statement = self.prepare_update_db_statement(list(updated_user_data.keys()))
        user_table.update_item(
            Key={
                "username": user_data.get("username")
            },
            UpdateExpression=user_data_update_statement,
            ExpressionAttributeValues=updated_user_data
        )
        # Update Games and HighScore table as this is future implementations
        if ":games_played" in updated_user_data:
            game_details = {
                "id": game_id,
                "usedId": self.user_id,
                "score": game_data.get("score")
            }
            games_table.put_item(Item=game_details)

        if ":highScore" in updated_user_data:
            high_score_details = {
                "id": self.user_id,
                "score": game_data.get("score")
            }
            high_score_table.put_item(Item=high_score_details)

        return {"message": "Data updated successfully"}

    def load_game_state(self):
        """
        Load user game state from db
        """
        user_table = self.aws_resource.Table("Users")
        user_data = self.get_user_by_id(user_table, self.user_id)
        if not user_data:
            raise HTTPError(404, "USER_DATA_NOT_FOUND")
        user_data = user_data[0]
        return {"gamesPlayed": len(user_data.get("gamesPlayed")),
                "score": replace_decimals(user_data.get("highScore"))}

