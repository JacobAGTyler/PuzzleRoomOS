from sqlalchemy.orm import Session

from tests.fixtures import mock_engine, built_game_config
from game.GameConfig import GameConfig

from data.database import save_entity


class TestDatabase:
    def test_save_entity(self, mock_engine, built_game_config: GameConfig):
        session = Session(mock_engine)
        save_entity(built_game_config, session)

        assert True


