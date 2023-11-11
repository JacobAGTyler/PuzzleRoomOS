from typing import Union

from sqlalchemy.orm.session import Session

from data.database import retrieve_entity, get_connection, get_engine
from game.game_config import GameConfig, import_game_config

from game.puzzle_config import PuzzleConfig
from game.game import Game
from game.puzzle import Puzzle


def make_new_game(game_config_code: Union[int, str], session: Session = get_connection(get_engine())) -> Game:
    if type(game_config_code) == str:
        game_config: GameConfig = import_game_config(game_config_code)
    else:
        game_config: GameConfig = retrieve_entity(game_config_code, GameConfig, session)

    game = Game(game_config.get_reference(), game_config)

    puzzle_config: PuzzleConfig
    for puzzle_config in game_config.get_puzzle_configs():
        puzzle = Puzzle(puzzle_config=puzzle_config, puzzle_reference=puzzle_config.get_reference())
        game.add_puzzle(puzzle)

    return game
