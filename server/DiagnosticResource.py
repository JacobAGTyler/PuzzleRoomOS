from flask import request
from flask_restful import Resource
from listener.DiagnosticHandler import DiagnosticHandler


class DiagnosticResource(Resource):
    def __init__(self):
        self.handler: DiagnosticHandler = DiagnosticHandler()

    def post(self):
        if not request.is_json:
            diagnostic_data: dict = request.form
        else:
            diagnostic_data: dict = request.json

        if diagnostic_data is None:
            return {'message': 'No trigger data provided'}, 400

        if 'trigger_text' not in diagnostic_data.keys():
            return {'message': 'No trigger text provided'}, 400

        game_key = diagnostic_data['game_id'] if 'game_id' in diagnostic_data.keys() else None

        result = self.handler.make_diagnostic(
            trigger_text=diagnostic_data['trigger_text'],
            game_key=game_key
        )

        if not result:
            return {'message': 'Attempt not published'}, 500

        return {'message': 'Attempt published'}, 200
