from flask import render_template

from data.database import get_connection, get_engine, retrieve_entity, retrieve_all
from game.Game import Game

engine = get_engine()


def get_game_list():
    session = get_connection(engine)
    games = retrieve_all(Game, session)

    return render_template('games.html', title='Puzzle Room OS', games=games)


def get_game(game_id):
    session = get_connection(engine)
    game: Game = retrieve_entity(game_id, Game, session)

    return render_template('game.html', title='Puzzle Room OS', game=game)

