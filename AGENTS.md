# AGENTS.md

This repo powers `mariocesar.xyz`, a small code-owned static site generated from
Markdown, Jinja templates, and Python. Keep it boring in production and pleasant
to write in.

## North Star

- Production is static HTML in `out/`.
- Simplicity wins over framework features.
- The homepage intentionally comes from `README.md`.
- Articles live in `content/articles/`.
- Content is edited in Git. Do not introduce a CMS, database, auth flow, or
  runtime server unless explicitly requested.

## Project Shape

- `src/builder/build.py`: static site builder entrypoint.
- `src/builder/content.py`: loads homepage and article Markdown.
- `src/builder/pages.py`: page dataclass, front matter parsing, Markdown render.
- `src/builder/markdown.py`: custom Markdown renderer and link processing.
- `src/builder/serve.py`: local dev server with rebuild and browser reload.
- `src/builder/templates/`: Jinja page templates.
- `src/builder/data/schema_website.yml`: homepage WebSite/Person JSON-LD data.
- `content/articles/*.md`: article source files.
- `public/`: static assets copied directly to `out/`.
- `tests/test_builder.py`: focused build/content/SEO regression tests.
- `vercel.json` and `scripts/vercel-build.sh`: Vercel static deploy setup.

## Commands

Use these from the repo root:

```sh
uv sync
uv run pytest
just build
just serve
bash scripts/vercel-build.sh
```

In sandboxed Codex sessions, prefer:

```sh
UV_CACHE_DIR=/tmp/uv-cache uv run pytest
UV_CACHE_DIR=/tmp/uv-cache just build
```

`just serve` builds the site, serves `out/` at `http://127.0.0.1:8000`, watches
`README.md`, `content/`, `public/`, and `src/builder/`, then rebuilds and reloads
the browser on changes.

## Build Rules

- Do not reintroduce the old FastAPI/Uvicorn + `wget --mirror` build pipeline.
- The canonical build path is `python -m builder.build`.
- `out/` is generated output and is ignored. Do not edit generated files.
- Static assets in `public/` are copied directly to `out/`.
- `llms.txt` and `llm.txt` are generated from `README.md`.

## Article Conventions

Articles must use YAML front matter:

```yaml
---
title: Example Article
description: One sentence for search/share previews.
summary: One sentence for article cards and RSS.
date: 2026-05-03
updated: 2026-05-03
---
```

Guidelines:

- Use lowercase kebab-case filenames, for example
  `content/articles/django-admin-actions-should-be-forms.md`.
- Keep article titles concrete and searchable.
- Write for technical readers: useful, direct, low fluff.
- FAQ sections are welcome when they answer real implementation questions.
- If an article is meaningfully changed, update `updated`.
- If the edit is cosmetic only, do not change `updated`.

## SEO Requirements

Keep these intact:

- Every HTML page has one canonical URL.
- Sitemaps use absolute canonical URLs.
- Sitemap `lastmod` comes from `updated`, then `date`, then file mtime.
- RSS uses absolute canonical URLs and meaningful `pubDate`.
- Article pages include Open Graph, Twitter card metadata, and Article JSON-LD.
- Homepage includes WebSite/Person JSON-LD from `schema_website.yml`.
- `robots.txt` references both:
  - `https://mariocesar.xyz/sitemap.xml`
  - `https://mariocesar.xyz/articles/rss.xml`
- Vercel serves `/llms.txt` and `/llm.txt` as
  `text/markdown; charset=utf-8`.

When adding templates or page types, update tests for generated metadata.

## Deploy Notes

The site deploys to Vercel. GitHub Pages deployment is intentionally disabled.

`vercel.json` intentionally includes:

```json
"framework": null
```

This prevents Vercel from auto-detecting the repo as a Python backend app and
looking for an `app.py`/`main.py` web entrypoint.

Vercel build:

```sh
bash scripts/vercel-build.sh
```

Vercel output directory:

```text
out
```

Do not add GitHub Pages deploy workflows or `actions/deploy-pages` back unless the
user explicitly asks to restore GitHub Pages.

## Dependency Policy

Runtime dependencies should stay small:

- `jinja2`
- `markdown`
- `mdx-truly-sane-lists`
- `pyyaml`

Development dependency:

- `pytest`

Do not add a web framework, JavaScript build step, CSS pipeline, CMS, database, or
watcher dependency unless the user explicitly asks and the tradeoff is clear.

## Verification Checklist

Before finishing a code/content change, run:

```sh
UV_CACHE_DIR=/tmp/uv-cache uv run pytest
UV_CACHE_DIR=/tmp/uv-cache just build
git diff --check
```

For Vercel changes, also run:

```sh
bash scripts/vercel-build.sh
python3 -m json.tool vercel.json
```

Useful generated files to inspect:

- `out/index.html`
- `out/articles/index.html`
- `out/articles/rss.xml`
- `out/sitemap.xml`
- `out/robots.txt`

## Editing Guidance

- Use `apply_patch` for manual edits.
- Keep generated HTML out of source changes.
- Keep content and builder behavior in sync through tests.
- Preserve user edits in a dirty worktree; do not revert unrelated changes.
- Prefer small, explicit Python functions over clever shell.
- Keep copy human first; SEO should clarify, not pad.
