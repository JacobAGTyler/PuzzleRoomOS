from flask_restful import Resource
from server.game_list import get_game


class GameResource(Resource):
    def __init__(self):
        self.game = None

    def get(self, game_id: str):
        self.game = get_game(game_id)

        return self.game.to_dict()
