import xml.etree.ElementTree as ET

from builder.build import Site, build, rss_xml, sitemap_xml
from builder.content import load_articles, load_homepage


def test_readme_renders_as_homepage():
    page = load_homepage()

    assert page.url == "/"
    assert "Hello, I&#x27;m Mario-César Señoranis" in page.content
    assert 'rel="noopener"' in page.content


def test_articles_load_with_metadata_sorted_newest_first():
    articles = load_articles()

    assert [article.url for article in articles] == [
        "/articles/static-websites-are-enough/",
        "/articles/readme-as-homepage/",
    ]
    assert articles[0].summary


def test_sitemap_uses_content_dates():
    articles = load_articles()
    xml = sitemap_xml(Site(), articles)
    root = ET.fromstring(xml)

    lastmods = [
        element.text
        for element in root.findall(
            "{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
            "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod"
        )
    ]
    assert "2026-05-03" in lastmods
    assert "2026-05-02" in lastmods


def test_rss_includes_articles():
    articles = load_articles()
    xml = rss_xml(Site(), articles)
    root = ET.fromstring(xml)

    titles = [element.text for element in root.findall("./channel/item/title")]
    assert "Static Websites Are Usually Enough" in titles
    assert "README as Homepage" in titles


def test_static_build_writes_expected_files(tmp_path):
    build(tmp_path)

    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "articles" / "index.html").exists()
    assert (tmp_path / "articles" / "rss.xml").exists()
    assert (tmp_path / "sitemap.xml").exists()
    assert (tmp_path / "static" / "css" / "main.css").exists()

    homepage = (tmp_path / "index.html").read_text()
    assert "Articles" in homepage
    assert "/articles/static-websites-are-enough/" in homepage
