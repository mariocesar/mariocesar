import html
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
        meta = yaml.load(head, Loader=YamlLoader)
        content = md.convert(body).strip("<div>").rstrip("</div>")
        title = meta.get("title", None)
        description = meta.get("description", None)

        return cls(path, title, content, url=path, description=description)


class YamlLoader(yaml.SafeLoader):
    ...

    def construct_html_escape(self, node):
        value = self.construct_scalar(node)
        return html.escape(value)

    def construct_include(self, node):
        # TODO
        return self.construct_yaml_str(node)


YamlLoader.add_constructor("!include", YamlLoader.construct_html_escape)
YamlLoader.add_constructor("!escape", YamlLoader.construct_html_escape)
YamlLoader.add_path_resolver("!str", ["meta"])
