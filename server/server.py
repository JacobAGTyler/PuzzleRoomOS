from flask import Flask, render_template
from flask_restful import Api, Resource

from server.grapher import build_graph
from server.game_list import get_game_list, get_game, new_game


class GameResource(Resource):
    def get(self):
        return {'hello': 'world'}


def create_app():
    new_app = Flask('Puzzle Room OS', template_folder='server/templates', static_folder='server/static')
    api = Api(new_app)
    api.add_resource(GameResource, "/game/<string:game_id>")

    @new_app.route('/')
    def index():
        return render_template('index.html', title='Puzzle Room OS')

    @new_app.route('/games')
    def games():
        return get_game_list()

    @new_app.route('/new-game/<game_config_code>')
    def add_new_game(game_config_code):
        return new_game(game_config_code)

    @new_app.route('/game/<game_id>')
    def game(game_id):
        return get_game(game_id)

    @new_app.route('/hello/')
    @new_app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)

    return new_app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=80)
