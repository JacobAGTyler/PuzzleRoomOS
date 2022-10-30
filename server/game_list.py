from flask import render_template
from sqlalchemy import select
from sqlalchemy.engine.row import Row

from data.database import get_connection, get_engine
from game.Game import Game

engine = get_engine()


def get_game_list():
    session = get_connection(engine)

    statement = select(Game)
    result = session.execute(statement).all()

    return render_template('games.html', title='Puzzle Room OS', result=result)


def get_game(game_id):
    session = get_connection(engine)

    statement = select(Game).where(Game.game_id == game_id)
    result: Row = session.execute(statement).first()
    game: Game = result.__getitem__(0)

    return render_template('game.html', title='Puzzle Room OS', game=game)

