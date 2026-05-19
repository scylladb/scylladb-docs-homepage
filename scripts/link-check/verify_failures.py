#!/usr/bin/env python3
"""Second-opinion verifier for lychee failures.

Lychee can't retry on 4xx, and several hosts (github.com,
Cloudflare-fronted *.scylladb.com properties, etc.) return
false positive 404 due to bot protection measures.
For each URL that lychee marked as failed, we re-check it directly with
urllib + a browser-like User-Agent + retries with backoff. URLs that
respond acceptably are removed from the report before process.py turns
the rest into a GitHub issue.
"""

import concurrent.futures
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

REPORT_FILE = Path(__file__).parent / "lychee-report.json"

# Browser-like UA so Cloudflare-protected hosts don't reject us out of
# hand for looking like a generic bot.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Wait times between successive attempts. 4 attempts total (initial +
# three retries), capped under a minute per URL.
BACKOFFS = (5, 15, 30)

# Statuses we accept as "the link works". Mirrors lychee.toml's accept
# list (200-299, 403, 429) plus 3xx (urllib follows redirects, but
# include for safety).
ACCEPTED = set(range(200, 300)) | {301, 302, 303, 307, 308, 403, 429}

# Cap parallel verifications. Lychee was already polite; this is a
# small follow-up burst per site, so a modest pool is plenty.
MAX_WORKERS = 8


def verify(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for wait in [0, *BACKOFFS]:
        if wait:
            time.sleep(wait)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status in ACCEPTED:
                    return True
        except urllib.error.HTTPError as e:
            if e.code in ACCEPTED:
                return True
        except Exception:
            pass
    return False


def main():
    if not REPORT_FILE.exists():
        return
    text = REPORT_FILE.read_text().strip()
    if not text:
        return
    report = json.loads(text)
    key = "fail_map" if "fail_map" in report else "error_map"
    fail_map = report.get(key) or {}
    if not fail_map:
        return

    all_urls = sorted({
        e["url"]
        for entries in fail_map.values()
        for e in entries
        if e.get("url")
    })
    if not all_urls:
        return

    print(
        f"verify: re-checking {len(all_urls)} failed URL(s) with "
        f"{MAX_WORKERS} workers..."
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        results = dict(zip(all_urls, ex.map(verify, all_urls)))
    rescued = {url for url, ok in results.items() if ok}

    if not rescued:
        print("verify: no false positives; all failures confirmed.")
        return

    print(f"verify: rescued {len(rescued)} false positive(s):")
    for u in sorted(rescued):
        print(f"  {u}")

    new_fail_map = {}
    for source, entries in fail_map.items():
        kept = [e for e in entries if e.get("url") not in rescued]
        if kept:
            new_fail_map[source] = kept
    report[key] = new_fail_map
    REPORT_FILE.write_text(json.dumps(report))


if __name__ == "__main__":
    main()
