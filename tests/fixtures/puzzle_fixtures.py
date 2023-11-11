import pytest

from sqlalchemy.orm.collections import __set
from sqlalchemy.orm.attributes import InstrumentedAttribute

from unittest.mock import Mock

from game.puzzle import Puzzle
from game.puzzle_config import PuzzleConfig

pc1 = Mock(spec=PuzzleConfig)
pc2 = Mock(spec=PuzzleConfig)
pc3 = Mock(spec=PuzzleConfig)
pc4 = Mock(spec=PuzzleConfig)
pc5 = Mock(spec=PuzzleConfig)

pc_real = PuzzleConfig(
    puzzle_reference='Test Puzzle 1',
    puzzle_code='TestPuzzleCode1',
    definition={
        'name': 'Test Definition Name 1',
        'puzzleCode': '8D75398A',
        'solutionType': 'CODEWORD'
    },
    setup={
        'prerequisites': [
            'A7FEA899',
            '2B3E4F5F',
            '955ABA37',
            '18963568B',
            '171A790C'],
        'interfaceMapping': [
            'Key1'
        ]
    }
)


@pytest.fixture
def built_puzzle_config() -> PuzzleConfig:
    return pc_real


p_1_data = {
    'puzzle_reference': 'test_puzzle_1',
    'puzzle_config': pc_real,
    'solved': False,
    'solve_time': None,
    'data': None,
    'prerequisites': None,
    'solutions': {'test_solution_1', 'test_solution_2'},
    'triggers': {'test_trigger_1', 'test_trigger_2'},
}

p_1 = Puzzle(**p_1_data)


@pytest.fixture
def built_puzzle(monkeypatch):
    monkeypatch.setattr(
        'sqlalchemy.orm.attributes.InstrumentedAttribute.__set__',
        Mock(spec=InstrumentedAttribute.__set__)
    )
    monkeypatch.setattr('sqlalchemy.orm.collections.__set', Mock(spec=__set))
    return p_1


@pytest.fixture
def puzzle_test_data(monkeypatch):
    # monkeypatch.setattr(
    #     'sqlalchemy.orm.attributes.InstrumentedAttribute.__set__',
    #     Mock(spec=InstrumentedAttribute.__set__)
    # )
    # monkeypatch.setattr('sqlalchemy.orm.collections.__set', Mock(spec=__set))
    return p_1_data
