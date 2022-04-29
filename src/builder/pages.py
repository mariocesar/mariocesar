import html
import os
import re
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Generator, Iterator, List, Optional, Union

import yaml

from .jinja import env, md

ROOT_DIR = Path(os.getcwd())


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
        meta = yaml.safe_load(head)
        content = md.convert(body)
        title = meta.get("title", None)
        description = meta.get("description", None)

        return cls(path, title, content, url=path, description=description)


def consumer(func):
    @wraps(func)
    def wrapper(*args, **kw):
        gen = func(*args, **kw)
        next(gen)
        return gen

    return wrapper


def src(patterns: Union[str, List[str]]) -> Generator[Path, Path, None]:
    if isinstance(patterns, str):
        patterns = [patterns]

    print(f"{patterns=}")

    for pattern in patterns:
        yield from ROOT_DIR.glob(pattern)


def log(path: Path):
    print(f"{path=}")
    return path


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


def load(path: Path):
    return yaml.load(path.open("rt"), Loader=Loader)


def grep(match_pattern: str):
    match = re.compile(match_pattern).match

    def inner(path: Path):
        return not (match(str(path)) is None)

    return inner


def exhausts(generator: Iterator) -> None:
    for _ in generator:
        pass


def main_markdown():
    # md = Markdown(output_format="html5", extensions=[MarkdownExtension(), "meta"])
    source = Path("README.md").read_text()
    return md.convert(source)


def markdown_page(path: Path):
    content = md.convert(path.read_text())
    title = md.Meta.get("title", None)
    return Page(path=path, title=title, content=content)


def render(path: Union[Path, str], context: Dict[str, Any]):
    if isinstance(path, str):
        path = Path(path).resolve()

    return env.get_template(str(path.relative_to(ROOT_DIR))).render(context)


def out(page: Page, dst: Path):
    dst.write_text(page.content)


def main_pipeline():
    exhausts(
        map(
            print,
            map(render, map(log, src("pages/**/[!_]*.jinja2"))),
        )
    )
