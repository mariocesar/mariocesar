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
