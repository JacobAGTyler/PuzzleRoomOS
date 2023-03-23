from typing import Optional

from flask import request
from flask_restful import Resource

from data.game_list import get_game_list
from listener.GameHandler import make_new_game_handler, GameHandler


class GamesResource(Resource):
    def __init__(self):
        self.handler: Optional[GameHandler] = None

    @staticmethod
    def get():
        return [game.to_dict() for game in get_game_list()]

    def post(self):
        game_data: dict = request.json

        if 'game_config_code' in game_data.keys() and type(game_data['game_config_code']) is str:
            game_config_code = game_data['game_config_code']
        elif 'game_config_id' in game_data.keys() and type(game_data['game_config_id']) is int:
            game_config_code = game_data['game_config_id']
        else:
            return {'error': 'game_config_code or game_config_id must be provided'}, 400

        self.handler = make_new_game_handler(game_config_code=game_config_code)
        self.handler.new_game()

        return self.handler.game.to_dict()
