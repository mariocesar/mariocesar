import html
import io
import json
import re
import xml.etree.ElementTree as etree
from dataclasses import dataclass
from datetime import datetime
from functools import partial, wraps
from pathlib import Path
from textwrap import indent
from typing import Any, Callable, Dict, Generator, Iterator, List, Optional, Union

import jinja2
import markdown
import yaml
from markdown.inlinepatterns import LINK_RE, LinkInlineProcessor
from markdown.serializers import _escape_attrib_html
from yattag import Doc

RootDir = Path(__file__).parent

HTML_EMPTY = {
    "area",
    "base",
    "basefont",
    "br",
    "col",
    "frame",
    "hr",
    "img",
    "input",
    "isindex",
    "link",
    "meta",
    "param",
}

INLINE_ELEMENTS = {"span", "a", "em", "strong", "code"}
INDENT = "    "


class LinkProcessor(LinkInlineProcessor):
    def handleMatch(self, m, data):
        el, start, end = super().handleMatch(m, data)
        el: etree.Element

        if el is None:
            return el, start, end

        if el.attrib["href"].startswith("http"):
            el.set("rel", "noopener")
            el.set("target", "_blank")
        if "title" not in el.attrib:
            el.set("title", el.attrib.get("href"))

        return el, start, end


class MarkdownExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            LinkProcessor(LINK_RE, md), "link", 170
        )  # Replace builtin LinkProcessor


def write_html(
    *,
    tag: str,
    attrs=Optional[Dict[str, str]],
    text=Optional[str],
    tail=Optional[str],
    children=Generator[tuple, None, None],
    depth: int = 0,
    write: Callable[[str], Any] = print,
):
    tag = tag.lower()
    text = text.strip() if text else None
    tail = tail.strip() if tail else ""

    if tag not in INLINE_ELEMENTS:
        write(INDENT * depth)

    write(f"<{tag}")

    if attrs:
        write(" ")
        write(render_attrs(attrs))

    write(">")

    if tag not in INLINE_ELEMENTS and text is None:
        write("\n")
        write(INDENT * (depth + 1))

    if text:
        if tag not in INLINE_ELEMENTS:
            write(f"\n{INDENT * (depth + 1)}")

        if tag in {"script", "style"}:
            write(text)
        else:
            write(html.escape(text))

        if tail:
            write(f"</{tag}>")

        if tail == "" and tag not in INLINE_ELEMENTS:
            write(" ")
        elif len(tail) > 0:
            # Style Tweal. Avoids adding unnecessary space before punctuation.
            if not (tail[0] in {",", "."}):
                write(" ")

    for _tag, _attrs, _text, _tail, _children in children:
        if _tag not in INLINE_ELEMENTS:
            write("\n")

        write_html(
            tag=_tag,
            attrs=_attrs,
            text=_text,
            tail=_tail,
            children=_children,
            depth=depth + 1,
            write=write,
        )

        if _tag in INLINE_ELEMENTS:
            write(" ")

    if tag not in HTML_EMPTY:
        if tail:
            write(html.escape(tail))

        if tag not in INLINE_ELEMENTS:
            write("\n")
            write(INDENT * depth)

        if not tail:
            write(f"</{tag}>")


def to_html_string(element: etree.Element):
    out = io.StringIO()

    def iter_children(el: etree.Element):
        for child in el:
            children = iter_children(child) if child else []
            yield child.tag, dict(child.items()), child.text, child.tail, children

    write_html(
        tag=element.tag,
        attrs=dict(element.items()),
        text=element.text,
        tail=element.tail,
        children=iter_children(element),
        write=out.write,
    )

    return out.getvalue()


class Markdown(markdown.Markdown):
    doc_tag = "article"
    output_formats = {"html": to_html_string}


md = Markdown(
    output_format="html5",
    extensions=[MarkdownExtension(), "mdx_truly_sane_lists"],
)
md.stripTopLevelTags = False

loader = jinja2.FileSystemLoader(RootDir / "pages")
env = jinja2.Environment(loader=loader, auto_reload=False)
env.globals["markdown"] = md.convert


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

        return cls(path, title, content, description)


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
        yield from RootDir.glob(pattern)


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


def render_attrs(obj: Dict[str, str]) -> str:
    return " ".join(f'{key}="{_escape_attrib_html(value)}"' for key, value in obj.items())


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


def render(path: Page):
    return env.get_template(str(path.relative_to(RootDir / "pages"))).render()


def out(page: Page, dst: Path):
    dst.write_text(page.content)


def main_pipeline():
    exhausts(
        map(
            print,
            map(render, map(log, src("pages/**/[!_]*.jinja2"))),
        )
    )


def make_ld_json_script_tag(page: Page, data: Dict[str, Any]) -> str:
    out = io.StringIO()
    out.write('<script type="application/ld+json">\n')
    out.write(indent(json.dumps(data, indent="    "), "    "))
    out.write("\n    </script>")

    return out.getvalue()


get_schema_website = partial(
    make_ld_json_script_tag,
    data={
        "@context": "https://schema.org",
        "@type": "WebSite",
        "url": "https://mariocesar.xyz/",
        "abstract": "I’m a software developer here is my Personal site and Blog",
        "keywords": [
            "python",
            "bolivia",
            "santa cruz de la sierra",
            "mariocesar",
            "mariocesar_bo",
            "zapier",
            "software engineer",
        ],
        "mainEntity": {
            "@type": "Person",
            "@context": "http://schema.org",
            "familyName": "Señoranis Ayala",
            "givenName": "Mario César",
            "jobTitle": "Senior Software Engineer",
            "worksFor": {"@type": "Organization", "name": "Zapier"},
            "image": "https://mariocesar.xyz/mariocesar.jpg",
            "gender": "http://schema.org/Male",
            "sameAs": [
                "https://mariocesar.xyz/",
                "https://twitter.com/mariocesar_bo",
                "https://www.linkedin.com/in/mariocesar/",
                "https://facebook.com/mariocesar",
                "https://instagram.com/mariocesar_bo",
                "https://github.com/mariocesar",
                "https://joinclubhouse.com/@mariocesar",
            ],
        },
        "author": {
            "@type": "Person",
            "name": "Mario César Señoranis",
            "url": "https://mariocesar.xyz",
        },
        "publisher": {
            "@type": "Person",
            "name": "Mario César Señoranis",
            "url": "https://mariocesar.xyz",
        },
    },
)


def build_sitemaps_xml(pages: List[Page]) -> str:
    doc, tag, text = Doc().tagtext()
    doc.asis('<?xml version="1.0" encoding="UTF-8"?>\n')

    with tag("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"):
        for page in pages:
            with tag("url"):
                with tag("loc"):
                    text(f"https://mariocesar.xyz{page.url}")
                with tag("lastmod"):
                    text(datetime.now().strftime("%Y-%m-%d"))
                with tag("changefreq"):
                    text("daily")
                with tag("priority"):
                    text(1)

    return indent(doc.getvalue(), indentation="    ", newline="\n", indent_text=True)


def build_robots_txt(pages: List[Page]) -> str:
    return """
User-agent: *
Allow:

Sitemap: https://mariocesar.xyz/sitemap.xml
"""


def main_build():
    # Create directories
    Path("out/css").mkdir(parents=True, exist_ok=True)

    # Build Pages
    pages: List[Page] = []
    page = Page.from_markdown(Path("README.md"))
    page.path = Path("pages/index.jinja2")
    page.content = env.get_template("index.jinja2").render(
        {
            "page": page,
            "site": {"url": "https://mariocesar.xyz"},
            "get_schema_website": get_schema_website,
        }
    )
    page.url = "/"

    out(page, Path("out/index.html"))
    pages.append(page)

    # Post build pages
    Path("out/sitemap.xml").write_text(build_sitemaps_xml(pages))
    Path("out/robots.txt").write_text(build_robots_txt(pages))

    # Assets
    Path("out/mariocesar.jpg").write_bytes(Path("public/mariocesar.jpg").read_bytes())
    Path("out/css/main.css").write_text(Path("public/css/main.css").read_text())


if __name__ == "__main__":
    main_build()
