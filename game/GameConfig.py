import os.path
import yaml
import json
import fastjsonschema

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Table
from typing import Optional

from game.PuzzleConfig import PuzzleConfig
from data import mapper_registry

base_path = 'config/'


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
            puzzles: Optional[list[dict]] = None
    ):
        self.config_reference = config_reference

        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.author_url = author_url
        self.game_license = game_license
        self.game_url = game_url

        self.puzzles = []

        if puzzles is not None:
            for puzzle in puzzles:
                self.puzzles.append(PuzzleConfig(puzzle))

        super().__init__()


def import_game_config(config_reference: str, instance: int = None) -> set[GameConfig]:
    config_path = f'{base_path}{config_reference}.yaml'

    if not os.path.exists(config_path):
        raise FileNotFoundError(f'Config file not found: {config_path}')

    with open(config_path, 'r') as f:
        config_set = yaml.safe_load(f)

    with open('game/game-config-schema.json', 'r') as schema_file:
        validate_schema = fastjsonschema.compile(json.load(schema_file))

    validate_schema(config_set)

    def map_config(config: dict) -> GameConfig:
        return GameConfig(
            config_reference=config_reference,
            name=config['name'],
            version=config['version'],
            description=config['description'],
            author=config['author'],
            author_url=config['authorURL'],
            game_license=config['gameLicense'],
            game_url=config['gameURL'],
            puzzles=config['puzzles']
        )

    imported_configs = set()

    if instance is None:
        for config_instance in config_set['instances']:
            imported_configs.add(map_config(config_instance))
    else:
        imported_configs.add(map_config(config_set[instance]))

    return imported_configs


game_config_table = Table(
    'game_config',
    mapper_registry.metadata,

    Column('game_config_id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('version', String(255)),
    Column('description', String(255)),
    Column('author', String(255)),
    Column('author_url', String(255)),
    Column('game_license', String(255)),
    Column('game_url', String(255)),
)

mapper_registry.map_imperatively(GameConfig, game_config_table, properties={
    'games': relationship('Game', back_populates="game_config")
})