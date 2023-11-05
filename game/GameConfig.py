from typing import Optional

from game.PuzzleConfig import PuzzleConfig
from utilities.config import ConfigType, import_config


class GameConfig:
    def __init__(
            self,
            config_reference: str,
            name: str,
            version: str,
            description: Optional[str] = None,
            author: Optional[str] = None,
            author_url: Optional[str] = None,
            game_license: Optional[str] = None,
            game_url: Optional[str] = None,
            puzzles: Optional[list[dict]] = None,
            parameters: Optional[dict] = None,
            duration_minutes: Optional[int] = 55
    ):
        self.config_reference = config_reference

        self._name = name
        self._version = version
        self.description = description
        self.author = author
        self.author_url = author_url
        self.game_license = game_license
        self.game_url = game_url
        self.duration_minutes = duration_minutes
        self.parameters = parameters

        self.puzzle_configs: Optional[list[PuzzleConfig]] = []

        if puzzles is not None:
            for puzzle in puzzles:
                definition = puzzle['definition']
                puzzle_config = PuzzleConfig(
                    puzzle_reference=definition['name'],
                    definition=definition,
                    setup=puzzle['setup'],
                )
                self.puzzle_configs.append(puzzle_config)

    def get_reference(self) -> str:
        return self.config_reference

    def get_name(self) -> str:
        return self._name

    def get_puzzle_configs(self) -> list[PuzzleConfig]:
        return self.puzzle_configs

    def get_version(self) -> str:
        return self._version


def import_game_config(config_reference: str) -> GameConfig:
    config = import_config(config_reference=config_reference, config_type=ConfigType.GAME)

    parameters = None
    if 'parameters' in config.keys():
        parameters = config['parameters']

    return GameConfig(
        config_reference=config_reference,
        name=config['name'],
        version=config['version'],
        description=config['description'],
        author=config['author'],
        author_url=config['authorURL'],
        game_license=config['gameLicense'],
        game_url=config['gameURL'],
        puzzles=config['puzzles'],
        parameters=parameters,
    )
