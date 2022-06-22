import json
from pathlib import Path

import yaml

from .pages import YamlLoader


def yaml2json(path: str) -> str:
    return json.dumps(load_yaml((Path(__file__).parent / path).resolve()), indent=2)


def load_yaml(path: Path):
    return yaml.load(path.open("rt"), Loader=YamlLoader)
