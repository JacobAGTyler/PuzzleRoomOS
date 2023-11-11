from sqlalchemy import select, Row
from sqlalchemy.orm import Session

from data.database import get_connection, get_engine, retrieve_entity, retrieve_all
from game.game import Game
from listener.game_event import GameEvent
from game.puzzle import Puzzle
from game.game_config import GameConfig, import_game_config

engine = get_engine()


def get_game_list(session: Session = get_connection(engine)) -> list[Game]:
    games: list[Game] = []
    row: Row
    for row in retrieve_all(Game, session):
        game = row.__getitem__(0)
        games.append(game)

    return games


def get_game_config_list(session: Session = get_connection(engine)) -> list[GameConfig]:
    game_configs: list[GameConfig] = []
    row: Row
    for row in retrieve_all(GameConfig, session):
        game_config = row.__getitem__(0)
        game_configs.append(game_config)

    return game_configs


def get_game(game_id: str, session: Session = get_connection(engine)) -> Game:
    statement = select(Game)\
        .where(Game.game_id == game_id)\
        .join(GameEvent, isouter=True).add_columns(GameEvent)\
        .join(GameConfig).add_columns(GameConfig)\
        .join(Game.puzzles, isouter=True).add_columns(Puzzle)
    result: Row = session.execute(statement).first()

    return result.__getitem__(0)


def get_game_config(game_config_id: str, session: Session = get_connection(engine)) -> GameConfig:
    statement = select(GameConfig)\
        .where(GameConfig.game_config_id == game_config_id)
    result: Row = session.execute(statement).first()

    return result.__getitem__(0)


def get_current_game() -> Game:
    session = get_connection(engine)
    statement = select(Game).where(Game.ended is False).limit(1)
    result: Row = session.execute(statement).first()

    return result.__getitem__(0)


def new_game(game_config_code: str):
    game_config_code = game_config_code.replace('/', '').replace('\\', '').strip()
    game_config = import_game_config(game_config_code)

    game = Game(game_config_code, game_config)


