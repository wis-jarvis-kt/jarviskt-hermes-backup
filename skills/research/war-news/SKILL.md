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
| BBC Asia | `https://www.bbc.com/news/world/asia` | South China Sea, Taiwan (supplement with Google News) |
| Google News | `https://news.google.com/search?q=...` | Taiwan/SCS supplement — extract headline + byline, navigate to source directly |
| Institute for the Study of War | `https://understandingwar.org` | **Go-to for China/Taiwan**; no bot detection. See ISW URL Navigation note below. |

## Anti-Bot / Technical Notes

> **ISW URL navigation (2026-06-10):** ISW homepage clicks land on a `backgrounder/` summary page. Full reports are at `research/<region>/<slug>` paths. Navigate to the `research/` URL directly for complete text. The homepage now also has an "ISW TEAMS" section with clickable region cards (China & Taiwan, Russia & Ukraine, Middle East) — clicking these lands on a listing page; extract `research/` URLs via JS before navigating.

> **ISW Middle East reports (2026-06-10):** ISW publishes `iran-update-special-report-YYYY-MM-DD` at `understandingwar.org/research/middle-east/`. Go-to for in-depth Hormuz/Iran military-strategic coverage; supplement to BBC for the Iran strikes story.

> **ISW report URL patterns (2026-06-10):**
> - China/Taiwan: `understandingwar.org/research/china-taiwan/china-taiwan-update-<date>/`
> - Russia/Ukraine: `understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-<date>/`
> - Middle East/Iran: `understandingwar.org/research/middle-east/iran-update-special-report-<date>/`

- BBC RSS feeds work but provide only `<title>` + `<description>` — insufficient for detail. Use browser navigation for full articles.
- Google News RSS (`news.google.com/rss/search?q=...`) returns empty `<item>` lists in cron jobs — use browser nav instead.
- **Hard-blocked outlets** — do not attempt to browser_navigate directly to these; use Google News or BBC as intermediary:
  - **Reuters** — DataDome device-check iframe (blocks all direct nav; different mechanism from Cloudflare)
  - **SCMP** — returns 404 on many article URLs; use Taipei Times or other outlets instead
  - **The Diplomat** — Cloudflare challenge (different from DataDome; Google News signposting works)
  - **U.S. News & World Report** — `net::ERR_HTTP2_PROTOCOL_ERROR` on direct nav; Google News headline extraction works
  - **Google News JS href extraction unreliable** — the `WYjbwe` class-based JS approach does not reliably yield article links; URLs from Google News search results must be inferred from the visible text links or from page structure using broader selectors
- **Cookie dialog**: After navigating to BBC, an "Online Quality Survey" alertdialog appears. Press `Escape` once or twice to dismiss it, then proceed.
- **Click failures**: Interactive element refs from `browser_snapshot` (e.g. `@e88`) often error with "Could not compute box model." **Do NOT use `browser_click` on article links from a listing page.** Instead:
  1. Run the JS snippet (step 5 above) to extract `https://www.bbc.com/news/articles/<id>` URLs.
  2. Navigate directly with `browser_navigate(url)` to each article.
- **Google News article extraction**: Same pattern — don't try clicking results. Use `browser_console` JS to grab URLs, then navigate directly to source sites. If URL extraction fails, navigate to Google News and use the visible headline text to search the topic on a known-working outlet (Taipei Times, Al Jazeera).
- **Diplomatic exception — Iran World Cup (2026-06-07):** The US granted visas to Iran's football team for their World Cup match in Los Angeles on June 15, despite active reciprocal strikes between the US and Iran. This is the first time a host nation has received a team from a country it is at war with. If covering the Iran conflict, note this precedent — it signals selective humanitarian/diplomatic exemptions even during active hostilities.
- **BBC article text**: After navigating to an article, body content is in the `article` element's static text children of `main`. Use `browser_snapshot(full=false)` for the full article text; `browser_console` can be used for targeted DOM inspection.
- **Article count and batching**: A full six-article read (3 Europe + 3 Middle East) is safe for a cron job with no time pressure. If running in a time-constrained session, prioritize 2–3 most recent/relevant per region. Group browser_navigate calls by region to reduce session overhead.
- **URL typos in BBC section links**: Double-check URLs before navigating — a truncated URL (e.g. `/middle_ea`) silently yields a 404. Always spell-check: the Middle East section is `bbc.com/news/world/middle_east` (not `/middle_ea`).

## Session Observations (2026-06-04)

- Google News JS href extraction (the `WYjbwe` class) remains unreliable — verified still broken
- Reuters DataDome block confirmed still active
- SCMP 404s confirmed still active

## Session Observations (2026-06-05)

- ISW (Institute for the Study of War) confirmed fully accessible — no bot detection, substantive China/Taiwan analysis. Elevated to go-to fallback for SCS/Taiwan.
- The Diplomat: Cloudflare challenge page confirmed active (bot detection, not DataDome). Different mitigation path — use Google News signposting.
- U.S. News direct nav: `net::ERR_HTTP2_PROTOCOL_ERROR` — different failure from DataDome/Cloudflare. Google News headline + byline extraction works fine.
- Reuters DataDome confirmed distinct block mechanism from Cloudflare; distinguish in anti-bot notes.

## Session Observations (2026-06-07)

- ISW URL `www.` prefix confirmed broken; bare `understandingwar.org` is correct.
- ISW "Toplines" section is the primary quick-read section on full report pages — jump to it first.
- Iran ceasefire stall confirmed: US requested changes to terms; Iran said US keeps "changing its views and putting forward new or contradictory demands." Article captured both sides' positions.
- New diplomatic exception: US granted visas to Iran's World Cup football team (Los Angeles, June 15) despite active strikes — first such host-nation exception.
- Taipei Times URL inference still risky; correct IDs must be extracted from Google News snippets. Inferred URL `…/2000106928` returned 404 on 2026-06-07.
- All other anti-bot and navigation patterns from prior sessions hold.

## Session Observations (2026-06-08)

- Google News JS URL extraction: `Array.from(document.querySelectorAll('a[href*="/news/articles/"]')).map(a => a.href).filter((v,i,a) => a.indexOf(v) === i)` is the reliable pattern for both BBC section pages and Google News search results. Deduplicates with `indexOf` trick. Confirmed working on both.
- ISW China/Taiwan full report URL format: `understandingwar.org/research/china-taiwan/china-taiwan-update-<date>/` — the "Toplines" section at the top is the quick-read; full text follows below.

## Session Observations (2026-06-10)

- **ISW homepage navigation confirmed:** The ISW TEAMS section with region cards (CHINA & TAIWAN, RUSSIA & UKRAINE, MIDDLE EAST) is now the primary homepage entry point. From any listing page, extract `research/` URLs via JS (`Array.from(document.querySelectorAll('a[href*="/research/"]')).map(a => a.href).filter(...)`), then navigate directly to the full report. The homepage click lands on a listing page, not the full report.
- **ISW Middle East supplement:** ISW publishes same-day `iran-update-special-report-YYYY-MM-DD` reports under `understandingwar.org/research/middle-east/` that cover the Hormuz conflict in depth. These are a valuable supplement to BBC for the Iran strikes story — use when BBC article is thin or you want the military/strategic context.
- **Google News result display:** Each result now shows source name + relative time (e.g. "ISW — 4 days ago", "Reuters — 5 days ago") directly inline, above the headline. No need to click "More" for source/recency. Headlines and bylines are fully visible without expansion.
- **BBC article URL slug vs. heading mismatch:** The article URL slug does not always match the visible headline. The JS URL extraction is still the correct method — don't try to infer URLs from headline text. The content is what matters.
- All prior anti-bot patterns (Reuters/DataDome, SCMP/404, The Diplomat/Cloudflare, U.S. News/protocol error) remain confirmed active.

- `web-research-limitations/references/conflict-news-rss.md` — RSS feed URLs and keyword patterns for conflict filtering
- `web-research-limitations` — AI/tech research workflow (absorbed from archived `research-scout`; see `references/research-scout-anti-bot.md`)

## Support Files
- `references/outlet-notes.md` — outlet accessibility matrix, blocking mechanism reference (DataDome vs Cloudflare vs protocol error), Google News search URLs, ISW as go-to China/Taiwan fallback
