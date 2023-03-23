from typing import Optional

from flask import request
from flask_restful import Resource
from listener.AttemptHandler import AttemptHandler


class AttemptResource(Resource):
    def __init__(self):
        self.handler: AttemptHandler = AttemptHandler()

    def post(self):
        if not request.is_json:
            attempt_data: dict = request.form
        else:
            attempt_data: dict = request.json

        if attempt_data is None:
            return {'message': 'No attempt data provided'}, 400

        if 'attempt_text' not in attempt_data.keys():
            return {'message': 'No attempt text provided'}, 400

        game_key = attempt_data['game_id'] if 'game_id' in attempt_data.keys() else None

        result = self.handler.make_attempt(
            attempt_text=attempt_data['attempt_text'],
            game_key=game_key
        )

        if not result:
            return {'message': 'Attempt not published'}, 500

        return {'message': 'Attempt published'}, 200
