from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from yattag import Doc
from yattag.indentation import indent

from builder.pages import Page
from builder.utils import load_yaml, yaml2json


class XMLTextResponse(PlainTextResponse):
    media_type = "text/xml"


class FaviconResponse(FileResponse):
    media_type = "image/x-icon"


APP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = (APP_DIR / "../..").resolve()
DATA_DIR = (APP_DIR / "data").resolve()
PUBLIC_DIR = (ROOT_DIR / "public").resolve()
STATIC_DIR = (PUBLIC_DIR / "static").resolve()


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


@app.get("/favicon.ico", response_class=FaviconResponse)
async def favicon():
    return FaviconResponse((PUBLIC_DIR / "favicon.ico").resolve())


templates = Jinja2Templates(directory=APP_DIR / "templates")
templates.env.globals["yaml2json"] = yaml2json


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    page = Page.from_markdown(ROOT_DIR / "README.md")
    return templates.TemplateResponse(
        "landing.jinja2",
        media_type="text/html",
        context={
            "site": {"url": "https://mariocesar.xyz"},
            "page": page,
            "request": request,
        },
    )


@app.get("/llms.txt", response_class=HTMLResponse)
async def llms(request: Request):
    page = (ROOT_DIR / "README.md").read_text()
    return PlainTextResponse(content=page, media_type="text/plain")


@app.get("/sitemap.xml", response_class=XMLTextResponse)
async def sitemap():
    doc, tag, text = Doc().tagtext()
    doc.asis('<?xml version="1.0" encoding="UTF-8"?>\n')
    sitemap = load_yaml(DATA_DIR / "sitemap.yml")

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
