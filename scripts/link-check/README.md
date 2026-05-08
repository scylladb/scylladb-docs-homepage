# Docs link check

Weekly automated link check across the ScyllaDB documentation ecosystem. Runs every Monday at 08:00 UTC (and on demand)
from [`.github/workflows/docs-link-check.yaml`](../../.github/workflows/docs-link-check.yaml).

The workflow runs one parallel job per site listed in [`sites.yml`](sites.yml).
Each job crawls only its own site, opens its own GitHub issue if it finds new broken links, and skips links already
reported in another open issue **for that same site**.

## How it works

The actual link checking is done by [lychee](https://github.com/lycheeverse/lychee), a fast Rust link checker.
lychee is not a spider (it does not follow links recursively), so the workflow first expands each site's sitemap
into a list of page URLs, then asks lychee to crawl each page and verify the links it contains.

For each site, a job:

1. Expands its sitemap into a flat list of page URLs (`urls.txt`) using [`expand_sitemaps.py`](expand_sitemaps.py).
2. Runs lychee with `--files-from urls.txt`, writing `lychee-report.json`.
3. Fetches its own open `link-check:<slug>` issues via `gh issue list`, writing `open-issues.json`.
4. Runs [`process.py`](process.py), which subtracts already-reported `(page, url)` pairs from the lychee findings and
   renders `issue-body.md` if anything new is left.
5. Opens a GitHub issue labelled `link-check` and `link-check:<slug>` if `process.py` produced a body.

Jobs run with `fail-fast: false`, so one slow or failing site does not block the others.

## Usage

### Add or remove a site

Edit [`sites.yml`](sites.yml) and add an entry:

```yaml
- name: Display name shown in the issue
  slug: short-stable-id            # used in the per-site label
  url: https://example.scylladb.com/stable/sitemap.xml
```

Notes:

- Use the **sitemap URL** when the site has one. lychee is not a spider, so it requires one input URL per page.
  Without a sitemap, point `url` at the homepage and lychee will check whatever links the homepage contains.
- `slug` becomes the per-site label `link-check:<slug>`. Renaming a slug orphans existing issues from the new label,
  so prefer not to.

### Exclude a URL or host

Add a regex to `lychee.toml` under `exclude`:

```toml
exclude = [
  # Skip a single URL
  "^https://example\\.com/known-broken/page$",
  # Skip every URL on a host
  "^https://flaky\\.example\\.com/",
  # Skip GitHub's anonymous-rate-limited search endpoint
  "^https://github\\.com/search\\?",
]
```

The pattern is anchored as a regex match against the full URL.
After editing, re-run the workflow (or run locally; see below) to confirm the exclusion is applied.

### Fix a broken link

1. Open the issue and fix the link in the upstream doc.
2. Close the issue. The next weekly run will not re-report links that are now working.

If you only fixed *some* of the links in the issue, closing it is still the right move. The remaining broken links
leave the "already reported" set, and the next run opens a fresh issue listing only those, without the noise of the
ones you fixed.

### Suppress an issue temporarily

Leave the GitHub issue open and do nothing.
Future runs will *not* re-report the same `(page, url)` pairs because the workflow reads its own open issues to
deduplicate.

If a link in the issue starts working again, future runs simply won't include it; if a *new* broken link appears for
the same site, a separate issue is opened.

### Trigger a run from the UI

Actions tab → **Docs / Link check** → **Run workflow** on `main`.

The dispatch dialog has an optional **slug** input. Leave it blank to run every site (same as the weekly schedule),
or enter a single slug from `sites.yml` (e.g. `python-driver`) to run just that one site. Useful when you've fixed
something on one docs site and want to confirm before next Monday. Unknown slugs fail the matrix-build job with a
list of valid slugs.

### Run a single site locally

Useful for testing a config tweak before pushing.

```sh
# Install lychee: https://github.com/lycheeverse/lychee#installation
pip install pyyaml

SITE_URL="https://python-driver.docs.scylladb.com/stable/sitemap.xml"
SITE_NAME="Python Driver"

python scripts/link-check/expand_sitemaps.py "$SITE_URL" \
  > scripts/link-check/urls.txt

# A GitHub token (PAT or `gh auth token`) avoids github.com rate-limit
# stalls on docs that link to many GitHub pages.
GITHUB_TOKEN=$(gh auth token) lychee \
  --config scripts/link-check/lychee.toml \
  --format json \
  --output scripts/link-check/lychee-report.json \
  --files-from scripts/link-check/urls.txt

# Optional: simulate dedupe against this site's existing open issues.
gh issue list --label "link-check:python-driver" --state open \
  --json body --limit 100 \
  > scripts/link-check/open-issues.json

SITE_NAME="$SITE_NAME" SITE_URL="$SITE_URL" \
  python scripts/link-check/process.py

cat scripts/link-check/issue-body.md
```

To audit page counts across every site without running lychee, run `python scripts/link-check/expand_sitemaps.py` with
no arguments.

### Filter issues with `gh`

```sh
# Every link-check issue (any site, any state)
gh issue list --label link-check

# Only the Python driver's open issues
gh issue list --label link-check:python-driver --state open

# All slugs currently in use
gh label list --search link-check:
```

## Reference

### Files

| File                  | Purpose                                                     |
| --------------------- | ----------------------------------------------------------- |
| `sites.yml`           | List of sites with `name`, `slug`, and `url` (sitemap)      |
| `lychee.toml`         | Lychee runtime configuration                                |
| `expand_sitemaps.py`  | Expands sitemap(s) into a flat list of page URLs            |
| `process.py`          | Subtracts already-reported links and renders the issue body |
| `README.md`           | This file                                                   |

These are produced at runtime and ignored via `.gitignore`:

- `urls.txt`: page URLs from the sitemap (one per line)
- `lychee-report.json`: raw lychee output
- `open-issues.json`: bodies of this site's open issues
- `issue-body.md`: rendered body of the new issue

For full lychee tuning options, see the [lychee configuration reference][lychee-config].

[lychee-config]: https://github.com/lycheeverse/lychee/blob/master/lychee.example.toml

### Labels

| Label                       | Meaning                                                    |
| --------------------------- | ---------------------------------------------------------- |
| `link-check`                | Applied to every issue opened by this workflow             |
| `link-check:<slug>`         | Per-site label, where `<slug>` matches `sites.yml`         |
