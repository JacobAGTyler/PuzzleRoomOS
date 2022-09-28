from flask import Flask
from flask_restful import Api, Resource


class Game(Resource):
    def get(self):
        return {'hello': 'world'}


def create_app():
    app = Flask('Puzzle Room OS')
    api = Api(app)
    api.add_resource(Game, "/game")

    @app.route('/')
    def index():
        return 'Test world'

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=80)
