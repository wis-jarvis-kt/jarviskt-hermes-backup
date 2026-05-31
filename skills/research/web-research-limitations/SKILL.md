---
name: web-research-limitations
category: research
description: Documents observed limitations and pitfalls when performing general web research (e.g., news, company performance) using browser tools in a cron job environment.
---

## Observed Limitations and Pitfalls for Web Research in Cron Jobs

When running as a scheduled cron job, direct web browsing using the `browser_navigate`, `browser_type`, and `browser_press` tools for general web research (e.g., finding recent news, company performance, or market reports) frequently encounters anti-bot measures. These measures can include:

- **CAPTCHAs:** Preventing automated access.
- **IP address blocking/rate limiting:** Blocking access from perceived bot traffic.
- **Page timeouts:** The page failing to load or timing out before content is accessible.

These issues make it unreliable to use the `browser` toolset for broad, unstructured web research in an autonomous cron job context. Attempts to navigate to popular search engines (like Google) or news sites (like Forbes) often result in immediate blocking or timeouts.

### Guidance

- **AI News direct navigation works when link-clicking fails:** Article heading links on `artificialintelligence-news.com` listing pages frequently resolve to an empty page via browser click (anti-bot on indirect click path). However, navigating directly to the article's canonical URL (e.g., `https://www.artificialintelligence-news.com/news/{slug}/`) loads reliably. After clicking from the homepage, check the URL — if it redirected to an empty page, copy the slug from the address bar and navigate directly to the intended article URL. AI News article URLs follow the pattern `/news/{slug}/` making them predictable. See `research-scout` skill for full rescue flow. If a task requires fetching unstructured information from the open web (e.g., "recent news for X," "top companies in Y sector"), assume the `browser` tools will be unreliable in a cron job.
- **Prefer specialized tools or APIs:** If specific data sources (e.g., arXiv, Polymarket, or a structured API) are available and can be accessed without browser interaction (e.g., via `terminal` with `curl` or a Python library), these should be prioritized.
- **Use Google News RSS as a lightweight workaround:** For batch news scanning (earnings, price moves, headlines across multiple companies), Google News RSS works reliably in cron jobs:
  ```
  curl -s "https://news.google.com/rss/search?q={COMPANY}+stock&hl=en-US&gl=US&ceid=US:en"
  ```
  Use `grep -o '<title>[^<]*</title>' | head -N` to extract headlines fast. This is much faster than browser navigation and avoids anti-bot blocking. Limitation: only titles + snippets, not full articles.
- **Google News via browser_navigate — WORKS WELL in cron jobs:**  \
Navigate to `https://news.google.com/search?q=QUERY&hl=en-US&gl=US&ceid=US:en`. The search results page is lightweight and rarely blocked. Click through to individual articles for detail. Tested successfully on 2026-05-23 for AI research scout. Caveats: some paywalled sites (NYT) show only a block page; some sites (Forbes) return 404 on article URLs even when linked from Google News — for those, rely on secondary sources.

**Article URL gotcha:** Google News links to articles via the Google News redirect (e.g., `https://news.google.com/articles/...`). When clicking through from the Google News listing page, use the actual article link in the snapshot (ref=ex), not any Google redirect URL. Direct source links from the listing are more stable than the `?url=...` redirect pattern.

**RSS feed endpoint — FAILS in cron jobs:** The Google News RSS endpoint (`https://news.google.com/rss/search?q=...`) returns only the RSS channel metadata (title, generator, copyright header) with zero `<item>` elements in a cron job context. This appears to be server-side filtering based on user-agent or lack of session cookies. Do not rely on RSS parsing as a lightweight news fetch in cron jobs — use browser_navigate to the Google News search page instead.

- **BBC homepage + section pages via browser_navigate — WORKS in cron jobs:** Navigating to `https://www.bbc.com/news/world/europe`, `https://www.bbc.com/news/world/middle_east`, and `https://www.bbc.com/news/world/asia` produced clean snapshots with lead headlines. The homepage and section listing pages are lightweight and load reliably without anti-bot blocking. Article click-through from listings sometimes fails to load new content (the snapshot stays on the same page), but navigating directly to section URLs bypasses this. Sufficient for a news radar/summary task. Tested 2026-05-30. Limitation: no full article body via this approach — use for headlines and top-level developments only.

### Support Files
- `references/conflict-news-rss.md` — BBC + CNBC RSS feed URLs, grep filter patterns for conflict topics (Ukraine, Middle East, South China Sea), and usage examples. Maintained with verified working sources from 2026-05-27.

### Verified working news sources in cron job browser context:
- `www.artificialintelligence-news.com` — loads reliably, no anti-bot blocking observed. Good for AI/tech news. Accepts cookie consent dialog (handle with browser_click on "Accept" button before reading content).
- Google News search results pages (e.g., `https://news.google.com/search?q=AI+breakthrough&hl=en-US&gl=US&ceid=US:en`) — lightweight, rarely blocked.

**BBC World News RSS (verified working in cron jobs — preferred for general news radar):**
```
curl -s "https://feeds.bbci.co.uk/news/world/rss.xml" | grep -A 3 "<item>" | head -N   # top N headlines
curl -s "https://feeds.bbci.co.uk/news/world/europe/rss.xml" | grep -A 3 "<item>" | head -N
curl -s "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml" | grep -A 3 "<item>" | head -N
curl -s "https://feeds.bbci.co.uk/news/world/asia/rss.xml" | grep -A 3 "<item>" | head -N
curl -s "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml" | grep -A 3 "<item>" | head -N
```
- Sections: europe, us_and_canada, middle_east, asia, africa, latin_america. Combine with `grep -iE "keyword1|keyword2"` to filter by topic across feeds.
- **Caveat:** BBC RSS gives only titles + short descriptions (no body). Fully sufficient for a news radar/summary task.
- BBC RSS successfully fetched Ukraine, Middle East, Asia, and US/Canada headlines on 2026-05-27. Tested in cron job context with no anti-bot blocking.

**CNBC RSS (verified working, good for business/finance-adjacent conflict news):**
```
curl -s "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114" | grep -A 3 "<item>" | head -N
```
- CNBC RSS includes wire stories on US/Iran strikes, Strait of Hormuz threats, and Taiwan chip sector news — useful for conflict intelligence that has market dimensions. Available at `/id/100003114/device/rss/rss.html` (US top news) or `/id/10000664/device/rss/rss.html` (full site).

**Combining RSS sources for multi-topic conflict news:**
For a "war news summary" covering Ukraine + Middle East + South China Sea/Taiwan:
1. Run 2–3 `curl` calls in parallel across BBC section feeds + CNBC RSS.
2. Pipe through `grep -iE` to extract relevant items.
3. BBC Middle East RSS alone surfaced: Israel/Gaza strike, Lebanon strikes, US/Iran strikes, Iran internet restoration.
4. BBC Europe RSS surfaced: Russia/GCHQ warnings, EU mediator search.
5. For Taiwan/South China Sea specifically — BBC Asia RSS had **no** direct military escalation headlines today; chip-sector news (Nvidia $150B, SK Hynix/Micron $1T market cap) dominated instead.
6. Aggregate and write directly to `~/.hermes/memories/war-news-YYYY-MM-DD.md`.

**RSS feed endpoint — FAILS in cron jobs:** The Google News RSS endpoint (`https://news.google.com/rss/search?q=...`) returns only the RSS channel metadata (title, generator, copyright header) with zero `<item>` elements in a cron job context. This appears to be server-side filtering based on user-agent or lack of session cookies. Do not rely on RSS parsing as a lightweight news fetch in cron jobs — use browser_navigate to the Google News search page instead.

**Wikipedia navigation — unreliable for live news (2026-05-27 observation):**
- Wikipedia article pages (e.g. `en.wikipedia.org/wiki/Russo-Ukrainian_war`) are very long (15,000+ line snapshots) and often time out or produce truncated snapshots.
- The article map/caption showed territorial control as of April 2026 — useful for context, not current events.
- **Do not use Wikipedia as a live news feed** for war news; use it for background/background context only.
- Wikipedia was tested on 2026-05-27 as an alternative to blocked search engines and returned only static background content.

---

## Google News Browser Navigation — Conflict/War News (tested 2026-05-31)

**Primary method for multi-topic conflict news:** Navigate to `https://news.google.com/search?q=TOPIC+May+2026&hl=en-US&gl=US&ceid=US:en`, read the snapshot for headlines, click through for detail.

**Verified working topics (2026-05-31):**
```
Ukraine Russia war    → https://news.google.com/search?q=Ukraine+Russia+war+May+2026
Israel Gaza war       → https://news.google.com/search?q=Israel+Gaza+war+May+2026
South China Sea Taiwan→ https://news.google.com/search?q=South+China+Sea+Taiwan+May+2026
```

**What works:** Google News search result pages load cleanly with 0 anti-bot blocking. Headlines give source, recency (e.g. "11 hours ago", "Yesterday"), and publication — sufficient to identify the top 1-2 stories per topic. Snapshot is compact (~235 elements max) and fast.

**Click-through failure patterns — do NOT rely on clicking Google News article links:**
| Source | Pattern |
|--------|---------|
| Reuters | DataDome device check blocks browser nav to native URL |
| BBC | 500 Internal Server Error on article URLs |
| CNN | "Uh-oh! no page here" error on article URLs |
| Al Jazeera | Heading click sometimes triggers anti-bot (ISW articles reliable) |
| CNBC | Paywall/block page on article URLs |
| ISW (Institute for the Study of War) | Heading clicks work ~67% of the time — proceed to next if it fails |

**Rescue pattern when click-through fails:** Read the Google News snapshot (headline + source + recency) — that data is sufficient for a conflict news summary. Full article body is not required. Al Jazeera and ISW articles reliably load via heading click; use those for casualty figures and territorial data.

**Best practice for war news summary:**
1. Navigate Google News search page per topic → read snapshot for top story selection
2. Note headline, source, and recency from the listing — don't rely on click-through for body text
3. If article detail is needed (e.g. casualty figures, territorial gains), use Al Jazeera or ISW articles that reliably load via heading click
4. Format summary directly from Google News snapshot data — no file writes until the final output

**Session log (2026-05-31):** Successfully produced full war news summary covering Ukraine-Russia, Israel-Gaza, and South China Sea/Taiwan using this method. No RSS, no delegate_task subagents — just browser_navigate + snapshot reading.

---

## Use delegate_task subagents with `web` toolset for multi-sector research (RECOMMENDED)

### Batch by Sector, Not by Company — delegate_task Wave Pattern

For structured multi-company research (5 sectors × 5 companies = 25 tickers), batch by **sector** into waves of ≤ 3 tasks. Each subagent handles one sector's worth of companies in a single call — far more efficient than one subagent per company.

`max_concurrent_children = 3` is the hard limit. Plan waves accordingly:

```
Wave 1 (3 sectors): AI/ML, Semiconductors, Cloud
Wave 2 (2 sectors): E-Commerce, Cybersecurity
```

Each subagent prompt should:
- State all 5 companies explicitly in the prompt
- Ask for a concise bullet summary per company, not raw JSON
- Include "Focus on what's NEW since [prior study date]" to avoid duplicating yesterday's data

After all waves return, **always check existing memory files first** before launching searches:
1. Read `stock-radar-YYYY-MM-DD.md` for today's P/E, PEG, and entry signals
2. Read `research-YYYY-MM-DD.md` for today's news developments
3. Read the prior `victor-study-YYYY-MM-DD.md` for carryover company context
4. Supplement with subagent searches only for gaps — don't re-fetch what already exists

Validated: 2026-05-29 session ran 3 waves (3+3+3 tasks) for Victor Study with no anti-bot failures.

- **Inform the user:** If a cron job fails due to these limitations, clearly communicate the reason for the failure and the observed anti-bot measures.
