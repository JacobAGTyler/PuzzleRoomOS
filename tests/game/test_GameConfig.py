import pytest

from fastjsonschema.exceptions import JsonSchemaValueException
from game.GameConfig import GameConfig, import_game_config


class TestGameConfig:
    def test_init(self):
        gc = GameConfig('test_reference', 'test_name', 'test_version')
        assert isinstance(gc, GameConfig)

    def test_get_reference(self):
        gc = GameConfig('test_reference', 'test_name', 'test_version')
        assert gc.get_reference() == 'test_reference'

    def test_get_name(self):
        gc = GameConfig('test_reference', 'test_name', 'test_version')
        assert gc.get_name() == 'test_name'

    def test_get_version(self):
        gc = GameConfig('test_reference', 'test_name', 'test_version')
        assert gc.get_version() == 'test_version'


class TestImportGameConfig:
    fixture_path = 'tests/fixtures/config/'

    @pytest.fixture
    def mock_config_reference(self) -> str:
        return "test-game-config"

    def test_game_config_init(self, mock_config_reference, monkeypatch):
        monkeypatch.setattr('utilities.config.base_path', self.fixture_path)
        game_config = import_game_config(mock_config_reference)
        assert isinstance(game_config, GameConfig)

        assert game_config.get_reference() == mock_config_reference
        assert game_config._name == 'test_game'
        assert game_config._version == '1.0.0'
        assert game_config.description == 'Test game'
        assert game_config.author == 'Jacob Tyler'
        assert game_config.author_url == 'https://jacob.tyler'
        assert game_config.game_license == 'https://opensource.org/licenses/MIT'
        assert game_config.game_url == 'https://test.com'

        assert game_config.get_puzzle_configs()[0].get_reference() == 'Test Puzzle A'

    def test_game_config_init_parameters(self, mock_config_reference, monkeypatch):
        monkeypatch.setattr('utilities.config.base_path', self.fixture_path)
        game_config = import_game_config(mock_config_reference)
        assert isinstance(game_config, GameConfig)

        assert game_config.parameters is not None
        assert game_config.parameters['test_parameter'] == 'test_value'

    def test_game_config_init_fail_reference(self):
        with pytest.raises(FileNotFoundError, match="Config file not found:"):
            _ = import_game_config("not-a-config")

    def test_game_config_init_fail_schema(self, monkeypatch):
        monkeypatch.setattr('utilities.config.base_path', self.fixture_path)
        with pytest.raises(JsonSchemaValueException):
            _ = import_game_config("invalid-game-config")
