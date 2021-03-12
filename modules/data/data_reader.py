"""Read token from file"""
from ruamel.yaml import YAML
from pathlib import Path

config_map = YAML().load(Path('config/settings.yaml'))