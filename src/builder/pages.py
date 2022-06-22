import html
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

from .markdown import md


@dataclass
class Page:
    path: Path
    title: str
    content: str
    url: str
    description: Optional[str] = None

    @classmethod
    def from_markdown(cls, path: Path):
        head, body = path.read_text().split("\n---\n", 1)
        meta = yaml.load(head, Loader=Loader)
        content = md.convert(body)
        title = meta.get("title", None)
        description = meta.get("description", None)

        return cls(path, title, content, url=path, description=description)


class Loader(yaml.SafeLoader):
    ...

    def construct_html_escape(self, node):
        value = self.construct_scalar(node)
        return html.escape(value)

    def construct_include(self, node):
        # TODO
        return self.construct_yaml_str(node)


Loader.add_constructor("!include", Loader.construct_html_escape)
Loader.add_constructor("!escape", Loader.construct_html_escape)
Loader.add_path_resolver("!str", ["meta"])


def load_yaml(path: Path):
    return yaml.load(path.open("rt"), Loader=Loader)
