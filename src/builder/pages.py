import html
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Optional

import yaml

from .markdown import md


@dataclass
class Page:
    path: Path
    title: Optional[str]
    content: str
    url: str
    description: Optional[str] = None
    date: Optional[date] = None
    updated: Optional[date] = None
    summary: Optional[str] = None
    template: str = "page.jinja2"

    @property
    def lastmod(self) -> date:
        return self.updated or self.date or date.fromtimestamp(
            self.path.stat().st_mtime
        )

    @classmethod
    def from_markdown(
        cls,
        path: Path,
        *,
        url: Optional[str] = None,
        template: str = "page.jinja2",
    ):
        head, body = path.read_text().split("\n---\n", 1)
        meta = yaml.load(head, Loader=YamlLoader)
        md.reset()
        content = strip_document_wrapper(md.convert(body))

        return cls(
            path=path,
            title=meta.get("title"),
            content=content,
            url=url or str(path),
            description=meta.get("description"),
            date=parse_date(meta.get("date")),
            updated=parse_date(meta.get("updated")),
            summary=meta.get("summary"),
            template=template,
        )


def parse_date(value: Any) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def strip_document_wrapper(content: str) -> str:
    content = content.strip()
    if content.startswith("<div>") and content.endswith("</div>"):
        return content[5:-6].strip()
    return content


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
