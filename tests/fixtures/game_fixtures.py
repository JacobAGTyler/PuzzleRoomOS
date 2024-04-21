import uuid

import pytest

from sqlalchemy.orm.collections import __set
from sqlalchemy.orm.attributes import InstrumentedAttribute

from unittest.mock import Mock
from game.puzzle import Puzzle
from game.game import Game
from game.game_config import GameConfig

from tests.fixtures.puzzle_fixtures import pc1, pc2, pc3, pc4, pc5, built_puzzle

m_game_config = Mock(spec=GameConfig)


def p_list() -> list[Puzzle]:
    return [
        Mock(
            spec=Puzzle,
            _puzzle_reference="puzzle_1",
            _puzzle_id="11111111-1111-1111-1111-111111111111",
            _puzzle_config=pc1,
            _prerequisites=None,
            has_prerequisites=lambda: False,
            get_prerequisites=lambda: set(),
            get_puzzle_ref=lambda: "puzzle_1",
        ),
        Mock(
            spec=Puzzle,
            _puzzle_reference="puzzle_2",
            _puzzle_id="22222222-2222-2222-2222-222222222222",
            _puzzle_config=pc2,
            _prerequisites=None,
            has_prerequisites=lambda: False,
            get_prerequisites=lambda: set(),
            get_puzzle_ref=lambda: "puzzle_2",
        ),
        Mock(
            spec=Puzzle,
            _puzzle_reference="puzzle_3",
            _puzzle_id="33333333-3333-3333-3333-333333333333",
            _puzzle_config=pc3,
            _prerequisites=['puzzle_1', 'puzzle_2'],
            has_prerequisites=lambda: True,
            get_prerequisites=lambda: ['puzzle_1', 'puzzle_2'],
            get_puzzle_ref=lambda: "puzzle_3",
        ),
        Mock(
            spec=Puzzle,
            _puzzle_reference="puzzle_2",
            _puzzle_id="44444444-4444-4444-4444-444444444444",
            _puzzle_config=pc4,
            _prerequisites=['puzzle_3'],
            has_prerequisites=lambda: True,
            get_prerequisites=lambda: ['puzzle_3'],
            get_puzzle_ref=lambda: "puzzle_4",
        )
    ]


@pytest.fixture
def mock_game_config(monkeypatch):
    # monkeypatch.setattr(
    #     'sqlalchemy.orm.attributes.InstrumentedAttribute.__set__',
    #     Mock(spec=InstrumentedAttribute.__set__)
    # )
    return m_game_config


@pytest.fixture
def built_game_config() -> GameConfig:
    return GameConfig('test_reference', 'test_name', 'test_version')


@pytest.fixture
def mock_puzzle_list(monkeypatch):
    monkeypatch.setattr('sqlalchemy.orm.collections.__set', Mock(spec=__set))
    return p_list()


@pytest.fixture
def mock_game(monkeypatch):
    monkeypatch.setattr(
        'sqlalchemy.orm.attributes.InstrumentedAttribute.__set__',
        Mock(spec=InstrumentedAttribute.__set__)
    )
    return Mock(spec=Game, _puzzles=set(), get_puzzles=lambda: set())


@pytest.fixture
def built_game(monkeypatch, mock_game_config) -> Game:
    monkeypatch.setattr(
        'sqlalchemy.orm.attributes.InstrumentedAttribute.__set__',
        Mock(spec=InstrumentedAttribute.__set__)
    )
    monkeypatch.setattr('sqlalchemy.orm.collections.__set', Mock(spec=__set))
    gm = Game("game_reference", mock_game_config)

    for p in p_list():
        gm.add_puzzle(p)

    return gm


@pytest.fixture
def mock_puzzle(monkeypatch):
    monkeypatch.setattr('sqlalchemy.orm.collections.__set', Mock(spec=__set))

    return Mock(
        spec=Puzzle,
        _puzzle_reference="puzzle_5",
        _puzzle_id="11111111-1111-1111-1111-111111111111",
        _puzzle_config=pc5,
        _prerequisites=['puzzle_4'],
        has_prerequisites=lambda: True,
        get_prerequisites=lambda: ['puzzle_4'],
        get_puzzle_id=lambda: "puzzle_5",
    )
