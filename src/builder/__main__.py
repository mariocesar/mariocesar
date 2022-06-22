from pathlib import Path
from typing import List

import click

from builder.pages import Page, out, render
from builder.tasks import build_robots_txt, build_sitemaps_xml, get_schema_website


@click.group()
def cli():
    ...


@cli.command()
def serve():
    ...


@cli.command()
def build():
    """Build website"""
    # Create directories
    Path("out/css").mkdir(parents=True, exist_ok=True)

    # Build Pages
    pages: List[Page] = []
    page = Page.from_markdown(Path("README.md"))
    page.path = Path("pages/index.jinja2")
    page.content = render(
        "index.jinja2",
        {
            "page": page,
            "site": {"url": "https://mariocesar.xyz"},
            "get_schema_website": get_schema_website,
        },
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
    cli()
