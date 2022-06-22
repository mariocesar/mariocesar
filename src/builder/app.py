from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from yattag import Doc
from yattag.indentation import indent

from builder.pages import Page
from builder.utils import load_yaml, yaml2json


class XMLTextResponse(PlainTextResponse):
    media_type = "text/xml"


BASE_DIR = Path(__file__).parent.resolve()

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=(BASE_DIR / "../../public/static").resolve()),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.globals["yaml2json"] = yaml2json


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    page = Page.from_markdown(BASE_DIR / "../../README.md")
    return templates.TemplateResponse(
        "landing.jinja2",
        media_type="text/html",
        context={
            "site": {"url": "https://mariocesar.xyz"},
            "page": page,
            "request": request,
        },
    )


@app.get("/sitemap.xml", response_class=XMLTextResponse)
async def sitemap():
    doc, tag, text = Doc().tagtext()
    doc.asis('<?xml version="1.0" encoding="UTF-8"?>\n')
    sitemap = load_yaml(BASE_DIR / "data/sitemap.yml")

    with tag(
        "urlset",
        **{
            "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xmlns:xhtml": "http://www.w3.org/1999/xhtml",
        },
    ):
        for url in sitemap["urlset"]:
            with tag("url"):
                with tag("loc"):
                    text(url["loc"])
                with tag("lastmod"):
                    text(datetime.now().strftime("%Y-%m-%d"))

    return indent(doc.getvalue(), newline="\n")


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return """User-agent: *
Allow:

Sitemap: https://mariocesar.xyz/sitemap.xml
    """
