import pytest

from unittest.mock import Mock
from game.Puzzle import Puzzle
from game.Game import Game
from game.GameConfig import GameConfig

m_game_config = Mock(spec=GameConfig)


def p_list() -> list[Puzzle]:
    return [
        Mock(spec=Puzzle, _puzzle_id="puzzle_1", _prerequisites=None, has_prerequisites=lambda: False,
             get_prerequisites=lambda: set(), get_puzzle_id=lambda: "puzzle_1"),
        Mock(spec=Puzzle, _puzzle_id="puzzle_2", _prerequisites=None, has_prerequisites=lambda: False,
             get_prerequisites=lambda: set(), get_puzzle_id=lambda: "puzzle_2"),
        Mock(spec=Puzzle, _puzzle_id="puzzle_3", _prerequisites=['puzzle_1', 'puzzle_2'],
             has_prerequisites=lambda: True, get_prerequisites=lambda: ['puzzle_1', 'puzzle_2'],
             get_puzzle_id=lambda: "puzzle_3"),
        Mock(spec=Puzzle, _puzzle_id="puzzle_4", _prerequisites=['puzzle_3'], has_prerequisites=lambda: True,
             get_prerequisites=lambda: ['puzzle_3'], get_puzzle_id=lambda: "puzzle_4")
    ]


@pytest.fixture
def mock_game_config():
    return m_game_config


@pytest.fixture
def mock_puzzle_list():
    return p_list()


@pytest.fixture
def mock_game():
    return Mock(spec=Game, _puzzles=set(), get_puzzles=lambda: set())


@pytest.fixture
def built_game():
    gm = Game("game_reference", m_game_config)

    for p in p_list():
        gm.add_puzzle(p)

    return gm


@pytest.fixture
def mock_puzzle():
    return Mock(spec=Puzzle, _puzzle_id="puzzle_5", _prerequisites=['puzzle_4'], has_prerequisites=lambda: True,
                get_prerequisites=lambda: ['puzzle_4'], get_puzzle_id=lambda: "puzzle_5")
