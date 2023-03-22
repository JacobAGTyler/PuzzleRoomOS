from flask import render_template

from data.database import get_connection, get_engine, retrieve_entity, retrieve_all
from game.Game import Game
from game.GameConfig import GameConfig, import_game_config

engine = get_engine()


def get_game_list():
    session = get_connection(engine)
    games = retrieve_all(Game, session)

    return render_template('games.html', title='Puzzle Room OS', games=games)


def get_game(game_id):
    session = get_connection(engine)
    game: Game = retrieve_entity(game_id, Game, session)

    return render_template('game.html', title='Puzzle Room OS', game=game)


def new_game(game_config_code: str):
    game_config_code = game_config_code.replace('/', '').replace('\\', '').strip()
    game_config = import_game_config(game_config_code)

    game = Game(game_config_code, game_config)


