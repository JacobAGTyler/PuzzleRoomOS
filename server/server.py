from flask import Flask, render_template
from flask_restful import Api

from data.game_list import get_game_list, get_game, new_game
from server.GameResource import GameResource
from server.GamesResource import GamesResource
from server.AttemptResource import AttemptResource


def create_app():
    new_app = Flask('Puzzle Room OS', template_folder='server/templates', static_folder='server/static')
    api = Api(new_app)
    api.add_resource(GameResource, '/api/game/<string:game_id>')
    api.add_resource(AttemptResource, '/api/attempt')
    api.add_resource(GamesResource, '/api/games')

    @new_app.route('/')
    def index():
        return render_template('index.html', title='Puzzle Room OS')

    @new_app.route('/games')
    def games():
        games = get_game_list()
        return render_template('games.html', title='Puzzle Room OS', games=games)

    @new_app.route('/new-game/<game_config_code>')
    def add_new_game(game_config_code):
        return new_game(game_config_code)

    @new_app.route('/game/<game_id>')
    def view_game(game_id):
        game = get_game(game_id)
        # graph = build_graph(game)

        return render_template('game.html', title='Puzzle Room OS', game=game)

    @new_app.route('/play/<game_id>')
    def play_game(game_id):
        return render_template('play.html', title='Puzzle Room OS', game=get_game(game_id))

    return new_app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=80)
