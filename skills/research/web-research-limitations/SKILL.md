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

- **AI News direct navigation works when link-clicking fails:** Article heading links on `www.artificialintelligence-news.com` listing pages frequently resolve to an empty page via browser click (anti-bot on indirect click path). However, navigating directly to the article's canonical URL (e.g., `https://www.artificialintelligence-news.com/news/{slug}/`) loads reliably. After clicking from the homepage, check the URL — if it redirected to an empty page, copy the slug from the address bar and navigate directly to the intended article URL. AI News article URLs follow the pattern `/news/{slug}/` making them predictable. See `research-scout` skill for full rescue flow. If a task requires fetching unstructured information from the open web (e.g., "recent news for X," "top companies in Y sector"), assume the `browser` tools will be unreliable in a cron job.
- **Cookie consent on AINS:** Always `browser_click("Accept")` on the cookie dialog before reading content on `www.artificialintelligence-news.com`.
- **Prefer specialized tools or APIs:** If specific data sources (e.g., arXiv, Polymarket, or a structured API) are available and can be accessed without browser interaction (e.g., via `terminal` with `curl` or a Python library), these should be prioritized.
- **Use Google News RSS as a lightweight workaround:** For batch news scanning (earnings, price moves, headlines across multiple companies), Google News RSS works reliably in cron jobs:
  ```
  curl -s "https://news.google.com/rss/search?q={COMPANY}+stock&hl=en-US&gl=US&ceid=US:en"
  ```
  Use `grep -o '<title>[^<]*</title>' | head -N` to extract headlines fast. This is much faster than browser navigation and avoids anti-bot blocking. Limitation: only titles + snippets, not full articles.
- **Google News via browser_navigate — WORKS WELL in cron jobs:**  \
Navigate to `https://news.google.com/search?q=QUERY&hl=en-US&gl=US&ceid=US:en`. The search results page is lightweight and rarely blocked. Click through to individual articles for detail. Tested successfully on 2026-05-23 for AI research scout. Caveats: some paywalled sites (NYT) show only a block page; some sites (Forbes) return 404 on article URLs even when linked from Google News — for those, rely on secondary sources.

**Article URL gotcha:** Google News links to articles via the Google News redirect (e.g., `https://news.google.com/articles/...`). When clicking through from the Google News listing page, use the actual article link in the snapshot (ref=ex), not any Google redirect URL. Direct source links from the listing are more stable than the `?url=...` redirect pattern.

**Google News RSS endpoint — WORKS in cron jobs (corrected 2026-06-14):** Confirmed: `https://news.google.com/rss/search?q=AI+artificial+intelligence&hl=en-US&gl=US&ceid=US:en` returns a full feed with dozens of `<item>` elements in cron job context. Use `curl` via terminal tool to get the raw RSS XML, then parse titles and pubDates with grep. This is faster than browser navigation and avoids anti-bot blocking. Limitation: only titles + snippets, not full articles. For full article content, navigate to the source link from each item. The earlier "FAILS in cron jobs" warning in this document was incorrect — RSS is a valid primary fetch method.

- **BBC homepage + section pages via browser_navigate — WORKS in cron jobs:** Navigating to `https://www.bbc.com/news/world/europe`, `https://www.bbc.com/news/world/middle_east`, and `https://www.bbc.com/news/world/asia` produced clean snapshots with lead headlines. The homepage and section listing pages are lightweight and load reliably without anti-bot blocking. Article click-through from listings sometimes fails to load new content (the snapshot stays on the same page), but navigating directly to section URLs bypasses this. Sufficient for a news radar/summary task. Tested 2026-05-30. Limitation: no full article body via this approach — use for headlines and top-level developments only.

### Support Files
- `references/conflict-news-rss.md` — BBC + CNBC RSS feed URLs, grep filter patterns for conflict topics (Ukraine, Middle East, South China Sea), and usage examples. Maintained with verified working sources from 2026-05-27.
- `references/pubmed-eutils-api.md` — PubMed EUtils API: curl-based search and abstract fetch, query syntax, verified queries for health research fact-checking. Use when verifying medical/scientific claims from social media.
- `references/banking-login-research.md` — Anti-bot patterns for banking website login research. Documents that major bank websites (HLB tested) use JS SPA routing that makes automated login impossible in cron job environment. Includes workaround: manual browser access required.

**Verified working news sources in cron job browser context (updated 2026-06-14):**
- `theverge.com/ai-artificial-intelligence` — reliable primary source for AI news; clean loads, working listing click-through. **Caveat: listing click-through can silently fail** — click consumed but snapshot stays on listing page. Verify title after click; if wrong, fall back to Google News.
- `www.artificialintelligence-news.com` — reliable secondary source. Cookie consent required (`browser_click("Accept")`). Direct article URLs (`/news/{slug}/`) work but **slugs can redirect to wrong content** — always verify title after navigation. Heading click anti-bot confirmed — do not click, navigate directly.
- Google News search (`news.google.com/search?q=...`) — **universal rescue path** when primary sources fail. Delivers multi-source confirmation with recency stamps without needing original article. Tested reliably for Anthropic export control and SpaceX Colossus stories (2026-06-13).
- TechCrunch AI listing — click-through from listing page works; direct article URLs 404. Use listing page as entry point only.
- **Google News RSS** — works via `curl` in terminal. Fast, no anti-bot. Returns full `<item>` list with titles, links, and pubDates. Use as primary scan before browser navigation.
- **Politico.com** — **always blocked** by Cloudflare in cron jobs. Do not attempt to navigate directly; the Cloudflare challenge cannot be bypassed. For Politico stories, rely on Google News snippets or secondary coverage.
- **Nature.com** — article pages frequently 404 or show cookie walls. The Nature URL structure is unpredictable; navigate via Google News link or skip to secondary source.
- **The Hacker News** — direct article URLs (`thehackernews.com/YYYY/MM/...`) frequently 404. Use Google News search results listing to find the article and click through from there, or use CyberPress as an aggregator that reliably indexes THN content.
- **CyberPress.org** — reliable aggregator for security/AI news; direct article URLs may 404 even when the article title appears in listings. Use listing page as entry point.
- **NDTV.com** — access denied in cron jobs. Skip; use alternative source.

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

**Google News RSS endpoint — WORKS in cron jobs (corrected 2026-06-14):** Confirmed: `https://news.google.com/rss/search?q=AI+artificial+intelligence&hl=en-US&gl=US&ceid=US:en` returns a full feed with dozens of `<item>` elements in cron job context. Use `curl` via terminal tool to get the raw RSS XML, then parse titles and pubDates with grep. This is faster than browser navigation and avoids anti-bot blocking. Limitation: only titles + snippets, not full articles. For full article content, navigate to the source link from each item. The earlier "FAILS in cron jobs" warning in this document was incorrect — RSS is a valid primary fetch method.

**Wikipedia for company/sector research (2026-06-10):**
- Wikipedia sector pages (e.g. `en.wikipedia.org/wiki/Semiconductor_industry`) load cleanly and are useful for **identifying top companies by sector** — the "Largest companies" subsection gives ranked lists with market context.
- Wikipedia article pages for individual companies (e.g. `en.wikipedia.org/wiki/NVIDIA`) are **404-prone on direct navigation** and often produce enormous snapshots (3,000+ elements) that are impractical for live research.
- **Best use:** Navigate to the sector overview page → find the company list → use that as a checklist to compile notes from existing knowledge or follow up with targeted searches. Do not attempt to read full company articles via browser_snapshot.
- Wikipedia was tested 2026-06-10 for semiconductor industry research — sector overview page loaded; individual company articles not attempted due to known 404/size issues.

**delegate_task subagents with `web` toolset — returns training data, not live web content (2026-06-12):**
- When subagents using the `web` toolset complete successfully, the summary field may contain **training-data knowledge** (e.g. approximate market cap figures, general company descriptions from model knowledge) rather than live web search results.
- Root cause: The `web_search` tool call executes successfully (returns `status: ok`) but the subagent's summary synthesis falls back to model knowledge when real-time results are unavailable or blocked.
- **Additional failure mode (2026-06-12):** Subagents may fail with `max_iterations` exit reason — the model keeps calling web_search until iteration limit, generating a trace of tool calls but no aggregated result.
- **Reliable pattern for multi-sector research:** Before launching subagents, read existing knowledge files (`victor-study-YYYY-MM-DD.md`, `research-YYYY-MM-DD.md`, `stock-radar-YYYY-MM-DD.md`) — they contain already-fetched data. Use subagents **only to supplement gaps**, not to re-fetch what's already there.
- Confirmed failures (2026-06-12): AI/ML subagent returned tool-call traces; Cybersecurity subagent returned training-data summaries; Cloud subagent hit max_iterations; Semiconductors subagent returned model knowledge instead of live news.
- **Better alternative for live company news:** Use the research-scout workflow (The Verge AI, AINS, Google News browser_navigate) for individual companies, or accept that today's knowledge files carry yesterday's news and update only what changed.

**Bing.com search triggers Cloudflare CAPTCHA in cron jobs:**
- Navigating to `https://www.bing.com/search?q=...` in a cron job context produces a Cloudflare human-verification challenge (`"Please solve the challenge below to continue"`). The challenge cannot be solved programmatically in this environment.
- **Do NOT use `browser_navigate` to Bing for research in cron jobs.** Google News search pages (`https://news.google.com/search?q=...`) work reliably; Bing does not.
- Confirmed 2026-06-12: `browser_navigate` to Bing search for "NVIDIA NVDA news June 2026" triggered Cloudflare challenge; Google News search pages did not.

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

---

## Research Scout (Evening AI/Tech) — Specific Cron Job

> **Absorbed from `research-scout` (archived 2026-06-02).** The research-scout skill was merged into this umbrella on 2026-06-16. Its unique content (evening scan workflow, save format, verified working sources table) is preserved here as a labeled subsection.

A specific recurring task: run an evening scan of AI/tech developments and save a brief report to `~/.hermes/memories/research-YYYY-MM-DD.md`.

> This is one application of the general anti-bot patterns and source guidance above. For ad-hoc one-shot research, prefer `delegate_task` subagents with the `web` toolset instead of this scheduled skill.

### Verified Working Sources (cron job context)

> Absorbed from `research-scout` — table of verified working sources for the evening scan.

| Source | URL | Notes |
|---|---|---|
| AI News | `https://www.artificialintelligence-news.com/` | Reliable, no anti-bot. Accept cookie dialog first. |
| Google News Search | `https://news.google.com/search?q=QUERY&hl=en-US&gl=US&ceid=US:en` | Lightweight, rarely blocked. |

### Fastest Workflow: Google News RSS + terminal
### Fastest Workflow: Google News RSS + terminal

1. **First: scan via RSS** — Run in terminal:
   ```
   curl -sL "https://news.google.com/rss/search?q=AI+technology+OR+LLM+OR+artificial+intelligence&hl=en-US&gl=US&ceid=US:en&tbs=qdr:d"
   ```
   The `tbs=qdr:d` parameter limits results to past 24 hours. Pipe through `grep -E '<title>|<pubDate>'` to extract headlines and dates. This is the fastest way to get a same-day headline scan with zero anti-bot risk.
   
2. **Cross-reference** — Navigate to `https://news.google.com/search?q=AI+artificial+intelligence&hl=en-US&gl=US&ceid=US:en&tbs=qdr:d` to see the same results in browser form with clickable links.

3. **Article detail** — For top stories, navigate to the source link from the RSS item (the `link` element contains the actual article URL). If that site is blocked (Politico, NDTV, Nature), skip to a secondary source that Google News also indexed.

4. **Verify page title after each navigation** — if the title doesn't match the expected article, the link may have been redirected by anti-bot protection. Use another source instead.

```markdown
# AI/Tech Research Scout — YYYY-MM-DD

## Evening Scan: 3 Notable Developments

---

### 1. [Headline]

**Source:** ... — YYYY-MM-DD
**Category:** ...

**Summary:**
...

**Key points:**
- ...

**Why it matters:** ...
```

8. **Verify the file** by reading back the first few lines (check line count and last entry's "Why it matters" is present).

### Save Format

Use this exact header format so future agents can parse it:

```
# AI/Tech Research Scout — {date}

## 1. [Headline]
- **Source:** Source Name (Date)
- **Summary:** 2-sentence summary
- **URL:** url

## 2. [Headline]
- **Source:** Source Name (Date)
- **Summary:** 2-sentence summary
- **URL:** url

## 3. [Headline]
- **Source:** Source Name (Date)
- **Summary:** 2-sentence summary
- **URL:** url

---
*Scout run: {date} morning/evening*
```

Keep entries concise — the goal is signal, not summaries. Each entry should be immediately useful to someone scanning for what's new.

### Support Files
- `references/research-scout-anti-bot.md` — session-tested anti-bot patterns, URL workarounds, and rescue flow for the research-scout workflow. Updated after each scout run that encounters blocking.
