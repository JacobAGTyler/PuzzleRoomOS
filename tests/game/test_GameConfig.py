import pytest

from fastjsonschema.exceptions import JsonSchemaValueException
from game.GameConfig import GameConfig, import_game_config


class TestGameConfig:
    def test_init(self):
        gc = GameConfig('test_reference', 'test_name', 'test_version')

        assert gc.config_reference == 'test_reference'
        assert gc.name == 'test_name'
        assert gc.version == 'test_version'

        assert isinstance(gc, GameConfig)


class TestImportGameConfig:
    fixture_path = 'tests/fixtures/config/'

    @pytest.fixture
    def mock_config_reference(self):
        return "test-game-config"

    def test_game_config_init(self, mock_config_reference, monkeypatch):
        monkeypatch.setattr('utilities.config.base_path', self.fixture_path)
        game_config = import_game_config(mock_config_reference, 0)
        assert isinstance(game_config.pop(), GameConfig)

    def test_game_config_init_fail_reference(self):
        with pytest.raises(FileNotFoundError, match="Config file not found:"):
            _ = import_game_config("not-a-config", 0)

    def test_game_config_init_fail_schema(self, monkeypatch):
        monkeypatch.setattr('utilities.config.base_path', self.fixture_path)
        with pytest.raises(JsonSchemaValueException):
            _ = import_game_config("invalid-game-config", 0)