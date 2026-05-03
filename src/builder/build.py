from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .content import APP_DIR, ROOT_DIR, load_articles, load_homepage
from .pages import Page
from .utils import yaml2json


SITE_URL = "https://mariocesar.xyz"
PUBLIC_DIR = ROOT_DIR / "public"
OUT_DIR = ROOT_DIR / "out"


@dataclass(frozen=True)
class Site:
    url: str = SITE_URL
    title: str = "Mario-César Señoranis"
    description: str = "Software developer & CTO in Santa Cruz, Bolivia."


def build(out_dir: Path = OUT_DIR) -> None:
    site = Site()
    homepage = load_homepage()
    articles = load_articles()
    pages = [
        homepage,
        Page(
            path=ROOT_DIR / "content" / "articles",
            title="Articles",
            description="Articles and notes by Mario-César Señoranis.",
            content="",
            url="/articles/",
            template="articles.jinja2",
        ),
        *articles,
    ]

    reset_out_dir(out_dir)
    copy_public(out_dir)

    env = template_environment()
    render_page(env, out_dir, homepage, site=site, articles=articles)
    render_page(env, out_dir, pages[1], site=site, articles=articles)
    for article in articles:
        render_page(env, out_dir, article, site=site, articles=articles)

    llms_content = (ROOT_DIR / "README.md").read_text()
    write_text(out_dir / "llms.txt", llms_content)
    write_text(out_dir / "llm.txt", llms_content)
    write_text(out_dir / "robots.txt", robots_txt())
    write_xml(out_dir / "sitemap.xml", sitemap_xml(site, pages))
    write_xml(out_dir / "articles" / "rss.xml", rss_xml(site, articles))


def template_environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader(APP_DIR / "templates"),
        autoescape=select_autoescape(("html", "xml", "jinja2")),
    )
    env.globals["yaml2json"] = yaml2json
    env.globals["display_date"] = display_date
    return env


def render_page(
    env: Environment,
    out_dir: Path,
    page: Page,
    *,
    site: Site,
    articles: list[Page],
) -> None:
    template = env.get_template(page.template)
    html = template.render(site=site, page=page, articles=articles)
    write_text(output_path(out_dir, page.url), html)


def output_path(out_dir: Path, url: str) -> Path:
    if url == "/":
        return out_dir / "index.html"
    return out_dir / url.strip("/") / "index.html"


def reset_out_dir(out_dir: Path) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)


def copy_public(out_dir: Path) -> None:
    for path in PUBLIC_DIR.iterdir():
        destination = out_dir / path.name
        if path.is_dir():
            shutil.copytree(path, destination)
        else:
            shutil.copy2(path, destination)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_xml(path: Path, content: str) -> None:
    write_text(path, content)


def absolute_url(site: Site, url: str) -> str:
    return f"{site.url}{url}"


def sitemap_xml(site: Site, pages: list[Page]) -> str:
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
    for page in pages:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = absolute_url(site, page.url)
        ET.SubElement(url, "lastmod").text = page.lastmod.isoformat()
    return xml_document(urlset)


def rss_xml(site: Site, articles: list[Page]) -> str:
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = f"{site.title} Articles"
    ET.SubElement(channel, "link").text = absolute_url(site, "/articles/")
    ET.SubElement(channel, "description").text = (
        "Articles and notes by Mario-César Señoranis."
    )
    ET.SubElement(channel, "language").text = "en"

    for article in articles:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = article.title
        ET.SubElement(item, "link").text = absolute_url(site, article.url)
        ET.SubElement(item, "guid", isPermaLink="true").text = absolute_url(
            site,
            article.url,
        )
        ET.SubElement(item, "description").text = (
            article.summary or article.description or ""
        )
        pub_date = datetime.combine(
            article.lastmod,
            datetime.min.time(),
            tzinfo=timezone.utc,
        )
        ET.SubElement(item, "pubDate").text = format_datetime(pub_date)

    return xml_document(rss)


def display_date(value) -> str:
    return value.strftime("%b %d, %Y").replace(" 0", " ")


def robots_txt() -> str:
    return """User-agent: *
Allow:

Sitemap: https://mariocesar.xyz/sitemap.xml
"""


def xml_document(root: ET.Element) -> str:
    ET.indent(root)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        root,
        encoding="unicode",
        short_empty_elements=False,
    )


def main() -> None:
    build()


if __name__ == "__main__":
    main()
