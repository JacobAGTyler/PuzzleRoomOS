import pytest

from fastjsonschema.exceptions import JsonSchemaValueException
from game.GameConfig import GameConfig


class TestGameConfig:
    fixture_path = 'tests/fixtures/config/'

    @pytest.fixture
    def mock_config_reference(self):
        return "test-game-config"

    def test_game_config_init(self, mock_config_reference, monkeypatch):
        monkeypatch.setattr('game.GameConfig.base_path', self.fixture_path)
        game_config = GameConfig(mock_config_reference, 0)
        assert isinstance(game_config, GameConfig)

    def test_game_config_init_fail_reference(self):
        with pytest.raises(FileNotFoundError, match="Config file not found:"):
            _ = GameConfig("not-a-config", 0)

    def test_game_config_init_fail_schema(self, monkeypatch):
        monkeypatch.setattr('game.GameConfig.base_path', self.fixture_path)
        with pytest.raises(JsonSchemaValueException):
            _ = GameConfig("invalid-game-config", 0)
