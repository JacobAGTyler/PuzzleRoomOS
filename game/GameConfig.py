import os.path
import yaml
import json
import fastjsonschema

from game.PuzzleConfig import PuzzleConfig

base_path = 'config/'

with open('game/game-config-schema.json', 'r') as schema_file:
    validate_schema = fastjsonschema.compile(json.load(schema_file))


class GameConfig:
    def __init__(self, config_reference: str, instance: int):
        self.config_reference = config_reference
        config_path = f'{base_path}{config_reference}.yaml'

        if not os.path.exists(config_path):
            raise FileNotFoundError(f'Config file not found: {config_path}')

        with open(config_path, 'r') as f:
            config_set = yaml.safe_load(f)

        validate_schema(config_set)

        self._config = config_set[instance]

        self.name = self._config['name']
        self.version = self._config['version']
        self.description = self._config['description']
        self.author = self._config['author']
        self.author_url = self._config['authorURL']
        self.game_license = self._config['gameLicense']
        self.game_url = self._config['gameURL']

        self.puzzles = []

        for puzzle in self._config['puzzles']:
            self.puzzles.append(PuzzleConfig(puzzle))
