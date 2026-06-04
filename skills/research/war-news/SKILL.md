---
name: war-news
description: "Daily geopolitical conflict news summary: Ukraine, Middle East, South China Sea, Taiwan Strait. Produces war-news-YYYY-MM-DD.md."
version: 1.0.0
---

# War News Summary

Run a daily scan of geopolitical conflict news and save a brief report to `~/.hermes/memories/war-news-YYYY-MM-DD.md`.

## Workflow

1. **Check today's date** via `terminal("date +%Y-%m-%d")`
2. **Navigate to BBC section pages** (reliable, no anti-bot):
   - Ukraine/Russia: `https://www.bbc.com/news/world/europe`
   - Middle East: `https://www.bbc.com/news/world/middle_east`
   - South China Sea/Taiwan: `https://www.bbc.com/news/world/asia`
3. **Dismiss the "Online Quality Survey" alertdialog** if it appears (it contains an iframe). Press `Escape` once or twice — do NOT try to click inside the iframe. Then proceed to scrape headlines.
4. **Scan headlines** for conflict-relevant stories using `browser_snapshot(full=false)`.
5. **Get article URLs** via `browser_console` — the interactive click refs often fail. Run:
   ```javascript
   Array.from(document.querySelectorAll('a[href*="/news/articles/"]'))
     .map(a => a.href).filter((v,i,a) => a.indexOf(v) === i)
   ```
   Deduplicate the results, then open relevant articles directly via `browser_navigate(url)` using the `https://www.bbc.com/news/articles/<id>` URLs. Do NOT rely on clickable refs from the snapshot — they frequently error with "Could not compute box model."
6. **Read article content** via `browser_snapshot(full=false)` on each article page. The body text is in the `article` element's static text children; use `browser_console` to inspect if needed.
7. **For Taiwan/South China Sea**, supplement BBC Asia with a Google News search:
   `https://news.google.com/search?q=south+china+sea+taiwan+strait+2026&hl=en-US&gl=US&ceid=US:en`
   Extract URLs from Google News results using the same JS snippet above, then navigate directly to source articles (SCMP, Taipei Times, Reuters, Al Jazeera, etc.).
8. **Write findings** to `~/.hermes/memories/war-news-YYYY-MM-DD.md` with this format:

```markdown
# War News Summary — YYYY-MM-DD

---

## [Conflict Region]

### [Headline]

**Source:** [Outlet] — YYYY-MM-DD
**Category:** [Conflict Region]

**Summary:**
...

**Key points:**
- ...

**Why it matters:** ...
```

8. **Verify** by reading back the first few lines.

## Verified Sources (cron job context)

| Source | URL | Notes |
|--------|-----|-------|
| BBC World Europe | `https://www.bbc.com/news/world/europe` | Ukraine/Russia — reliable, no anti-bot |
| BBC Middle East | `https://www.bbc.com/news/world/middle_east` | Israel, Iran, Gaza |
| BBC Asia | `https://www.bbc.com/news/world/asia` | South China Sea, Taiwan |
| Google News | `https://news.google.com/search?q=...` | Fallback supplement |

## Anti-Bot / Technical Notes

- BBC RSS feeds work but provide only `<title>` + `<description>` — insufficient for detail. Use browser navigation for full articles.
- Google News RSS (`news.google.com/rss/search?q=...`) returns empty `<item>` lists in cron jobs — use browser nav instead.
- **Hard-blocked outlets** — do not attempt to browser_navigate directly to these; use Google News or BBC as intermediary:
  - **Reuters** — DataDome device-check iframe blocks all direct navigations
  - **SCMP** — returns 404 on many article URLs; use Taipei Times or other outlets instead
  - **Google News JS href extraction unreliable** — the ` WYjbwe` class-based JS approach does not reliably yield article links; URLs from Google News search results must be inferred from the visible text links or from page structure using broader selectors
- **Cookie dialog**: After navigating to BBC, an "Online Quality Survey" alertdialog appears. Press `Escape` once or twice to dismiss it, then proceed.
- **Click failures**: Interactive element refs from `browser_snapshot` (e.g. `@e88`) often error with "Could not compute box model." **Do NOT use `browser_click` on article links from a listing page.** Instead:
  1. Run the JS snippet (step 5 above) to extract `https://www.bbc.com/news/articles/<id>` URLs.
  2. Navigate directly with `browser_navigate(url)` to each article.
- **Google News article extraction**: Same pattern — don't try clicking results. Use `browser_console` JS to grab URLs, then navigate directly to source sites. If URL extraction fails, navigate to Google News and use the visible headline text to search the topic on a known-working outlet (Taipei Times, Al Jazeera).
- **BBC article text**: After navigating to an article, body content is in the `article` element's static text children of `main`. Use `browser_snapshot(full=false)` for the full article text; `browser_console` can be used for targeted DOM inspection.
- **Article count and batching**: A full six-article read (3 Europe + 3 Middle East) is safe for a cron job with no time pressure. If running in a time-constrained session, prioritize 2–3 most recent/relevant per region. Group browser_navigate calls by region to reduce session overhead.
- **URL typos in BBC section links**: Double-check URLs before navigating — a truncated URL (e.g. `/middle_ea`) silently yields a 404. Always spell-check: the Middle East section is `bbc.com/news/world/middle_east` (not `/middle_ea`).

## Session Observations (2026-06-04)

- Google News JS href extraction (the `WYjbwe` class) remains unreliable — verified still broken
- Reuters DataDome block confirmed still active
- SCMP 404s confirmed still active
- **Taipei Times URL form**: Article IDs appear in Google News preview snippets as full URLs. Extract from there rather than inferring. The pattern is `https://www.taipeitimes.com/News/taiwan/archives/YYYY/MM/DD/NumericID`. DO NOT use `/news/detail/<code>` form — these are section index pages, not article pages.

- `web-research-limitations/references/conflict-news-rss.md` — RSS feed URLs and keyword patterns for conflict filtering
- `research-scout` — AI/tech research (separate from conflict news)

## Support Files
- `references/outlet-notes.md` — outlet accessibility matrix, hard-blocked sites (Reuters DataDome, SCMP 404s), Google News search URLs, and BBC Asia coverage gaps for Taiwan/SCS
