#!/usr/bin/env python3
"""Second-opinion verifier for lychee failures.

Lychee can't retry on 4xx, and two upstream hosts misbehave for the kind
of traffic lychee sends:

  - github.com sometimes 404s as anti-abuse to repeated calls.
  - university.scylladb.com sits behind Cloudflare and rejects lychee's
    custom UA from Actions IPs.

For each URL that lychee marked as failed, we re-check it directly with
urllib + a browser-like User-Agent + retries with backoff. URLs that
respond acceptably are removed from the report before process.py turns
the rest into a GitHub issue.
"""

import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

REPORT_FILE = Path(__file__).parent / "lychee-report.json"

# Browser-like UA so Cloudflare-protected hosts don't reject us out of
# hand for looking like a generic bot.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Hosts where lychee's "broken" verdict is unreliable and worth a second
# look. Keep this conservative — every host added here costs time.
FLAKY_HOST_SUFFIXES = (
    "github.com",
    "university.scylladb.com",
)

# Wait times between successive attempts. 4 attempts total (initial +
# three retries), capped under a minute per URL.
BACKOFFS = (5, 15, 30)

# Statuses we accept as "the link works". Mirrors lychee.toml's accept
# list (200-299, 403, 429) plus 3xx (urllib follows redirects, but
# include for safety).
ACCEPTED = set(range(200, 300)) | {301, 302, 303, 307, 308, 403, 429}


def is_flaky(url):
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return False
    return any(host == s or host.endswith("." + s) for s in FLAKY_HOST_SUFFIXES)


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

    all_urls = {
        e["url"]
        for entries in fail_map.values()
        for e in entries
        if e.get("url")
    }
    targets = sorted(u for u in all_urls if is_flaky(u))
    if not targets:
        print(
            f"verify: 0 of {len(all_urls)} failed URL(s) on flaky hosts; "
            f"nothing to re-verify."
        )
        return

    print(f"verify: re-checking {len(targets)} URL(s) on flaky hosts...")
    rescued = {u for u in targets if verify(u)}
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
