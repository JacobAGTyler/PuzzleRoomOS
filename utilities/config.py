import json
import os.path
import fastjsonschema
import yaml

from enum import Enum

base_path = f'config{os.path.sep}'
setup_config = f'{base_path}setup.yaml'


class ConfigType(Enum):
    GAME = 'GAME'
    DEVICE = 'DEVICE'
    INTERFACE = 'INTERFACE'


def import_config(config_reference: str, config_type: ConfigType) -> dict:
    config_path = f'{base_path}{config_type.value.lower()}{os.path.sep}{config_reference}.yaml'

    if not os.path.exists(config_path):
        raise FileNotFoundError(f'Config file not found: {config_path}')

    with open(config_path, 'r') as f:
        config_set = yaml.safe_load(f)

    if config_type == ConfigType.GAME:
        schema_path = f'game{os.path.sep}game-config-schema.json'
    elif config_type in [ConfigType.DEVICE, config_type.INTERFACE]:
        schema_path = f'listener{os.path.sep}{config_type.value.lower()}-config-schema.json'

    with open(schema_path, 'r') as schema_file:
        validate_schema = fastjsonschema.compile(json.load(schema_file))

    validate_schema(config_set)

    return config_set


class Setup:
    def __init__(self):
        self._config = None

        if os.path.exists(setup_config):
            with open(setup_config, 'r') as f:
                self._config = yaml.safe_load(f)

        fastjsonschema.compile(json.load(open('setup-schema.json', 'r')))(self._config)

        self.kafka_bootstrap_servers = self._config['kafka']['bootstrap_servers']
