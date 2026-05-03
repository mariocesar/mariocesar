from pathlib import Path

from .pages import Page


APP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = (APP_DIR / "../..").resolve()
CONTENT_DIR = ROOT_DIR / "content"
ARTICLES_DIR = CONTENT_DIR / "articles"


def load_homepage() -> Page:
    return Page.from_markdown(
        ROOT_DIR / "README.md",
        url="/",
        template="landing.jinja2",
    )


def load_articles() -> list[Page]:
    articles = [
        Page.from_markdown(
            path,
            url=f"/articles/{path.stem}/",
            template="article.jinja2",
        )
        for path in ARTICLES_DIR.glob("*.md")
    ]
    return sorted(articles, key=lambda page: page.lastmod, reverse=True)
