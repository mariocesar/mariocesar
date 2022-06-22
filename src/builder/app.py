from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from builder.pages import Page
from builder.tasks import build_robots_txt, build_sitemaps_xml, yaml2json

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
