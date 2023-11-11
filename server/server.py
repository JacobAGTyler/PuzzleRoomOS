from flask import Flask, render_template
from flask_restful import Api

from data.game_list import get_game_list, get_game, get_game_config_list, get_game_config
from server.game_resource import GameResource
from server.games_resource import GamesResource
from server.attempt_resource import AttemptResource
from server.diagnostic_resource import DiagnosticResource


def create_app():
    new_app = Flask('Puzzle Room OS', template_folder='server/templates', static_folder='server/static')
    api = Api(new_app)
    api.add_resource(GameResource, '/api/game/<string:game_id>')
    api.add_resource(AttemptResource, '/api/attempt')
    api.add_resource(GamesResource, '/api/games')
    api.add_resource(DiagnosticResource, '/api/diagnostic')

    @new_app.route('/')
    def index():
        return render_template('index.html', title='Puzzle Room OS')

    @new_app.route('/game-config/<game_config_id>')
    def view_game_config(game_config_id):
        game_config = get_game_config(game_config_id)
        # graph = build_graph(game)

        return render_template('config.html', title='Puzzle Room OS', game_config=game_config)

    @new_app.route('/game-configs')
    def game_configs():
        game_config_list = get_game_config_list()
        return render_template('configs.html', title='Puzzle Room OS', game_configs=game_config_list)

    @new_app.route('/games')
    def games():
        game_list = get_game_list()
        return render_template('games.html', title='Puzzle Room OS', games=game_list)

    @new_app.route('/new-game/<game_config_id>')
    @new_app.route('/new-game')
    def add_new_game(game_config_id=None):
        return render_template('new-config.html', title='Puzzle Room OS', game_config_id=game_config_id)

    @new_app.route('/game/<game_id>')
    def view_game(game_id):
        game = get_game(game_id)
        # graph = build_graph(game)

        return render_template('game.html', title='Puzzle Room OS', game=game)

    @new_app.route('/play/<game_id>')
    def play_game(game_id):
        return render_template('play.html', title='Puzzle Room OS', game=get_game(game_id))

    @new_app.route('/diagnostic')
    def diagnostic():
        return render_template('diagnostic.html', title='Puzzle Room OS', games=get_game_list())

    return new_app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=80)
