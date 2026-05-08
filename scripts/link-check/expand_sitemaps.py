#!/usr/bin/env python3
"""Expand sitemap URL(s) into a flat list of page URLs, one per line on stdout.

Modes:
  python expand_sitemaps.py <URL>   expand one sitemap (used by the matrix workflow)
  python expand_sitemaps.py         expand every site in sites.yml (local use)

Non-XML URLs are passed through unchanged. See README.md for why this exists.
"""

import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
CONFIG_FILE = ROOT / "sites.yml"

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
USER_AGENT = (
    "scylladb-docs-link-check "
    "(+https://github.com/scylladb/scylladb-docs-homepage)"
)


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _normalize(url):
    """Some sitemaps emit scheme-less URLs (e.g. `developers.scylladb.com/...`).
    Prepend `https://` so lychee crawls the right host over TLS instead of
    defaulting to plain HTTP."""
    url = url.strip()
    if url and not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def expand_sitemap(url):
    """Return all page URLs in a sitemap, recursing into sitemap indexes."""
    root = ET.fromstring(fetch(url))
    tag = root.tag.split("}", 1)[-1]
    if tag == "sitemapindex":
        urls = []
        for loc in root.findall("sm:sitemap/sm:loc", SITEMAP_NS):
            urls.extend(expand_sitemap(_normalize(loc.text)))
        return urls
    if tag == "urlset":
        return [
            _normalize(loc.text)
            for loc in root.findall("sm:url/sm:loc", SITEMAP_NS)
        ]
    print(f"warning: unrecognized sitemap root <{tag}> at {url}", file=sys.stderr)
    return []


def expand_site(url):
    if url.lower().endswith(".xml"):
        return expand_sitemap(url)
    return [url]


def main():
    if len(sys.argv) > 1:
        # Single-URL mode: expand the given URL and print page URLs.
        for url in expand_site(sys.argv[1]):
            print(url)
        return
    # All-sites mode (local convenience).
    cfg = yaml.safe_load(CONFIG_FILE.read_text())
    for site in cfg["sites"]:
        urls = expand_site(site["url"])
        print(f"# {site['name']}: {len(urls)} page(s)", file=sys.stderr)
        for url in urls:
            print(url)


if __name__ == "__main__":
    main()
