import pytest

from game.puzzle import Puzzle

from tests.fixtures.puzzle_fixtures import puzzle_test_data
from tests.fixtures.database_fixtures import db_session


@pytest.mark.usefixtures('puzzle_test_data')
@pytest.mark.skip(reason="Strange Behaviour")
class TestPuzzle:
    @pytest.mark.usefixtures('db_session')
    def test_create_puzzle(self, puzzle_test_data, db_session):
        pz = Puzzle(**puzzle_test_data)
        assert pz is not None
        assert isinstance(pz, Puzzle)

    def test_get_puzzle_id(self, puzzle_test_data):
        pz = Puzzle(**puzzle_test_data)
        assert pz.get_puzzle_id() == 1

    def test_get_puzzle_reference(self, puzzle_test_data):
        pz = Puzzle(**puzzle_test_data)
        assert isinstance(pz, Puzzle)
        print(pz.__dict__)
        assert pz.get_puzzle_reference() == 'test_puzzle_1'

    def test_set_prerequisites(self, puzzle_test_data):
        pz = Puzzle(**puzzle_test_data)
        assert type(pz.prerequisites) is set

        test_set = {"test_puzzle_2", "test_puzzle_3"}
        pz.set_prerequisites(test_set)
        assert pz.__getattribute__('prerequisites') == test_set

        assert pz.get_prerequisites() is not None
        assert len(pz.get_prerequisites()) == 2
        assert "test_puzzle_2" in pz.get_prerequisites()

    def test_set_prerequisites_type_error(self, puzzle_test_data):
        pz = Puzzle(**puzzle_test_data)
        assert type(pz.get_prerequisites()) is set

        with pytest.raises(ValueError, match="Prerequisites must be a set"):
            pz.set_prerequisites("test_puzzle_2")

        assert pz.set_prerequisites(None) is None

    def test_add_first_prerequisite(self, puzzle_test_data):
        pz = Puzzle(**puzzle_test_data)
        assert pz.get_prerequisites() is None

        pz.add_prerequisite("test_puzzle_2")

        assert pz.get_prerequisites() is not None
        assert len(pz.get_prerequisites()) == 1
        assert "test_puzzle_2" in pz.get_prerequisites()

    def test_add_prerequisite(self, puzzle_test_data):
        pz = Puzzle(**puzzle_test_data)
        assert pz.get_prerequisites() is None

        pz.add_prerequisite("test_puzzle_2")

        assert pz.get_prerequisites() is not None
        assert len(pz.get_prerequisites()) == 1
        assert "test_puzzle_2" in pz.get_prerequisites()

        pz.add_prerequisite("test_puzzle_3")

        assert pz.get_prerequisites() is not None
        assert len(pz.get_prerequisites()) == 2
        assert "test_puzzle_3" in pz.get_prerequisites()

    def test_get_prerequisites(self, puzzle_test_data):
        pz = Puzzle(**puzzle_test_data)
        pz.set_prerequisites({"test_puzzle_2", "test_puzzle_3"})

        assert pz.get_prerequisites() is not None
        assert len(pz.get_prerequisites()) == 2
        assert "test_puzzle_2" in pz.get_prerequisites()

    def test_has_prerequisites(self, puzzle_test_data):
        pz = Puzzle(**puzzle_test_data)
        assert pz.has_prerequisites() is False

        pz.set_prerequisites({"test_puzzle_2", "test_puzzle_3"})
        assert pz.has_prerequisites() is True
