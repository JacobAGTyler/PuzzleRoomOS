import pytest
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from game.game import Game

from data.database import save_entity, get_engine, get_connection


class TestDatabase:

    def test_get_engine(self):
        result = get_engine()

        assert isinstance(result, Engine)
        assert result.url.database == 'puzzle_room_os'
        assert result.url.username == 'jacob'
        assert result.url.password == 'jacob'
        assert result.url.host == 'localhost'
        assert result.url.port == 5432

    def test_get_connection(self):
        engine = get_engine()
        result = get_connection(engine)

        assert isinstance(result, Session)
        assert result.bind == engine

    @pytest.mark.usefixtures('mock_engine')
    def test_save_entity(self, mock_engine, built_game: Game):
        session = Session(mock_engine)
        save_entity(built_game, session)

        assert True


