import io
import json
from datetime import datetime
from functools import partial
from typing import Any, Dict, List

from yattag import Doc
from yattag.indentation import indent

from .pages import Page


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
