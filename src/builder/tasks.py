import json
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Dict, List

from yattag import Doc
from yattag.indentation import indent

from .pages import Page, load_yaml


def yaml2json(path: str) -> str:
    return json.dumps(load_yaml((Path(__file__).parent / path).resolve()), indent=2)
