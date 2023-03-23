from flask import render_template
from sqlalchemy import select, Row
from sqlalchemy.orm import Session

from data.database import get_connection, get_engine, retrieve_entity, retrieve_all
from game.Game import Game
from listener.Event import Event
from game.Puzzle import Puzzle
from game.GameConfig import GameConfig, import_game_config

engine = get_engine()


def get_game_list():
    session = get_connection(engine)
    games = retrieve_all(Game, session)

    return render_template('games.html', title='Puzzle Room OS', games=games)


def get_game(game_id: str, session: Session = get_connection(engine)) -> Game:
    statement = select(Game)\
        .where(Game.game_id == game_id)\
        .join(Event, isouter=True).add_columns(Event)\
        .join(GameConfig).add_columns(GameConfig)\
        .join(Game.puzzles, isouter=True).add_columns(Puzzle)
    result: Row = session.execute(statement).first()

    print(result)

    return result.__getitem__(0)


def get_current_game() -> Game:
    session = get_connection(engine)
    statement = select(Game).order_by('end_time DESC').where(Game.ended is False).limit(1)
    result: Row = session.execute(statement).first()

    return result.__getitem__(0)


def new_game(game_config_code: str):
    game_config_code = game_config_code.replace('/', '').replace('\\', '').strip()
    game_config = import_game_config(game_config_code)

    game = Game(game_config_code, game_config)


