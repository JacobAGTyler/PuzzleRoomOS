from typing import Optional

from flask import request
from flask_restful import Resource
from data.game_list import get_game
from game.game import Game
from data.database import get_connection, get_engine

from listener.game_handler import GameHandler


class GameResource(Resource):
    def __init__(self):
        self.game: Optional[Game] = None
        self.handler: Optional[GameHandler] = None

    def get(self, game_id: str):
        self.game = get_game(game_id)

        return self.game.to_dict()

    def put(self, game_id: str):
        session = get_connection(get_engine())
        self.game = get_game(game_id, session)
        self.handler = GameHandler(self.game, session)

        game_data: dict = request.json

        if 'started' in game_data.keys() and game_data['started'] is True:
            self.handler.start_game()

        if 'ended' in game_data.keys() and game_data['ended'] is True:
            self.handler.end_game()

        return self.game.to_dict()
