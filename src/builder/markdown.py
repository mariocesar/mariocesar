import html
import io
import os
import xml.etree.ElementTree as etree
from pathlib import Path
from typing import Any, Callable, Dict, Generator, Optional

import markdown
from markdown.inlinepatterns import LINK_RE, LinkInlineProcessor
from markdown.serializers import _escape_attrib_html

ROOT_DIR = Path(os.getcwd())

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
INDENT = "  "


def render_attrs(obj: Dict[str, str]) -> str:
    return " ".join(f'{key}="{_escape_attrib_html(value)}"' for key, value in obj.items())


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
