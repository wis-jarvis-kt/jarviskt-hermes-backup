# Research-Scout Anti-Bot Knowledge Bank

## Session Log — 2026-05-29

### Observed Anti-Bot Patterns

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Click AI News article heading link from AINS homepage | `ref=e117` on "Anthropic releases Claude Opus 4.8" heading | `(empty page)`, `element_count: 0` | AI News heading links misbehave via direct click |
| Navigate back then re-click same ref | Same `ref=e117` after back() | Same failure | Click retry does NOT different resolve |
| Click Google News link to TechCrunch | `ref=e39` in Google News results | TechCrunch loaded correctly with full content | Google News → original source works |
| Navigate directly to AI News article URL | `https://www.artificialintelligence-news.com/news/google-pay-ai-agents-universal-commerce-protocol/` | Page loaded correctly, title matched | Direct URL works; anti-bot triggers are on link clicks |
| Navigate to AI News NBA article via direct URL | `https://www.artificialintelligence-news.com/news/nba-ai-out-of-bounds-calls/` | Page loaded correctly | Direct navigation reliable |
| Navigate to `blog.google/technology/秤/` | blog.google with Chinese characters | `net::ERR_TOO_MANY_REDIRECTS` | Non-ASCII characters in URL break navigation; use English path |
| Click Yahoo Sports article for NBA via Google News | Yahoo Sports link in Google News results | Reuters article loaded instead (redirect) | Some Google News aggregator links redirect; source URL in address bar is authoritative |

### New Observations — 2026-05-30

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Click AI News heading link — OpenAI FGF article | `ref=e122` on "Scaling safe enterprise AI..." | `(empty page)`, `element_count: 0` | Same heading-click anti-bot pattern as prior session |
| Click AI News heading link — Claude Opus 4.8 article | `ref=e119` | **Page loaded correctly with full article** | **Heading-click anti-bot is INTERMITTENT, not 100% — one heading click succeeded** |
| Click AI News heading link — Google Pay UCP article | `ref=e121` | **Page loaded correctly with full article** | Second intermittent success; confirms pattern is probabilistic, not systematic |
| Navigate directly to AI News article URL (after failed click) | `https://www.artificialintelligence-news.com/news/scaling-safe-enterprise-ai-openai-governance-frameworks/` | Page loaded correctly, title matched | Direct URL navigation is the reliable fallback after a failed heading click |
| Read all 3 articles successfully via heading clicks (with 1 failure → direct URL fallback) | AI News homepage → e117, e119, e121 | 2/3 heading clicks succeeded; 1 required direct URL fallback | Viable workflow: click heading → if empty, back to homepage → next article; or immediately use direct URL |
| browser_snapshot(full=false) on Claude Opus 4.8 article | After successful heading click | 132 elements, full article text readable | Compact snapshot is sufficient for article reading; full=true only needed if compact misses content |
| browser_snapshot(full=false) on Google Pay UCP article | After successful heading click | 142 elements, full article text readable | Same — compact snapshot captures full article body |
| Click NYT link via Google News | Google News → NYT article | DataDome block page | NYT via Google News click triggers DataDome |
| Navigate directly to CNBC article URL | `https://www.cnbc.com/2026/05/29/...` | "Not Found" (404) | CNBC article URLs include date in path; slug must be exact |
| Navigate to Invezz article | Invezz.com | Cloudflare block | Invezz uses Cloudflare; blocked in cron context |

### New Observations — 2026-06-01

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Click AI News heading link — Google Pay UCP | Featured section | Click "succeeded" — no error thrown — but `browser_snapshot` showed homepage with ref IDs unchanged. | Anti-bot intercepts silently; ref IDs refresh (new page context) but visible content stays homepage. |
| Click AI News heading link — NBA AI article | After scrolling to LATEST | Same: click registered, no error, snapshot showed homepage. | Same silent interception pattern. |
| Click AI News heading link — OpenAI FGF article | Featured section | `(empty page)`, `element_count: 0` | Classic anti-bot redirect. |
| After failed heading click, navigate directly to article URL | Direct URL `.../scaling-safe-enterprise-ai-openai-governance-frameworks/` | Page loaded correctly, full article readable | Direct URL is reliable fallback regardless of failure mode. |
| Google News search → TechCrunch result for Claude Opus 4.8 | `ref=e38` in Google News | **Page loaded correctly with full content** | Google News → TechCrunch works reliably; primary viable path. |
| browser_snapshot(full=false) sufficient for all 3 articles | OpenAI FGF, Google Pay UCP, NBA AI | 124–142 element count captured full article text across all three | Compact snapshot remains sufficient; full=true not needed. |

### New Silent Interception Failure Mode

Two distinct anti-bot failure modes now observed on AI News heading links:

1. **Silent interception** — click is consumed, ref IDs refresh (new page context), but content stays on homepage. `browser_snapshot` shows homepage, not the article. Distinct from empty-page redirect.
2. **Empty-page redirect** — `element_count: 0`, "(empty page)". Classic anti-bot redirect.

Both resolved by navigating directly to the original source domain.

### New Observations — 2026-06-02

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Google News "Anthropic IPO filing 2026" → click Reuters link | Reuters via Google News | DataDome device verification block | Reuters via Google News confirmed hard block — same pattern as prior sessions. |
| Navigate directly to TechCrunch Anthropic article | Direct URL `techcrunch.com/2026/06/01/anthropic-files-to-go-public/` | Page loaded correctly with full article | Direct navigation to TechCrunch bypasses anti-bot entirely. |
| Google News "AI technology June 2 2026" → click NVIDIA Newsroom | NVIDIA Newsroom link in Build/AI search | Page loaded correctly with full article | NVIDIA Newsroom accessible via Google News click path. |
| Google News "Microsoft Build AI announcements today" → click PCMag Australia | PCMag Australia link in live coverage search | Page loaded correctly with live blog content | PCMag Australia does not block via Google News click path. |
| Google News "AI technology June 2 2026" → click Mashable Microsoft Build | Mashable link in AI tech search | Page loaded correctly with article content | Mashable accessible via Google News click path. |
| Google News "Nvidia AI PC chip" → click Hawaii Tribune-Herald (reprint) | Hawaii Tribune-Herald Reuters wire article | Page loaded correctly with full Reuters content | Local wire-reprint papers block less than Reuters direct; rescue path for blocked wire stories. |
| Google News "China AI trade secret" → click Euronews | Euronews article on China AI IP rules | Page loaded correctly | Euronews accessible via Google News for policy/trade topics. |
| Politico via Google News (Florida/OpenAI story) | Politico link in AI tech search | Cloudflare challenge page, then block | Politico uses Cloudflare — same recovery pattern as other Cloudflare sites. |
| Click Reuters link from Google News results | Reuters in search listings | DataDome device check block | Confirmed hard block; skip Reuters, use local wire-reprint outlet or direct TechCrunch/VentureBeat. |
| Money Morning via Google News | Money Morning link in search | `(empty page)` anti-bot | Same pattern as Reuters. Treat as blocked aggregator. |

### New Observations — 2026-06-06

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Navigate directly to TechCrunch article URL (from listing) | `techcrunch.com/2026/06/06/google-will-pay-spacex-920m-per-month-for-compute/` | 404 page | TechCrunch article URLs are unstable — many return 404 even hours after publication |
| Navigate directly to The Verge AI section | `theverge.com/ai-artificial-intelligence` | Full article listing loaded cleanly, click-through to articles works | **The Verge is the most reliable primary source for AI news in cron jobs** — clean loads, stable URLs, working article click-through |
| Navigate to Google News RSS endpoint via browser_navigate | `news.google.com/rss/search?q=AI+technology+June+6+2026` | `lastBuildDate: Fri, 05 Jun 2026` — all items from prior day | **RSS endpoint is NOT a same-day scan** — server-side filters to previous day. Use the search page, not the RSS feed. |
| delegate_task with `web` toolset for AI news research | Subagent with web_search | Minimal output — subagent didn't fetch actual article content | delegate_task web searches are not a reliable substitute for direct browser reading |

**Key finding — The Verge replaces TechCrunch as primary AI news source:**
- TechCrunch listing pages are fine for headlines, but article URLs frequently 404
- The Verge AI section (`theverge.com/ai-artificial-intelligence`) loads cleanly with stable URLs and working article click-through
- For the research-scout workflow, use The Verge as primary and TechCrunch as secondary (with 404 caveat)

### Quick Diagnosis Flow

```
Article title confirmed on AI News homepage or Google News listing
    ↓
browser_click on link ref
    ↓
browser_snapshot(full=false):
   a. Article title confirmed → proceed to read
   b. Homepage content (refs match listing page) → silent interception → step 5
   c. element_count: 0 / (empty page) → anti-bot redirect → step 5
    ↓
Step 5: Navigate directly to the original source domain
    ↓
browser_snapshot(full=false) → verify title → read
```

### New Observations — 2026-06-07

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Navigate to TechCrunch AI listing page | `techcrunch.com/category/artificial-intelligence/` | Full article listing loaded cleanly with 10+ headlines | TechCrunch listing page loads reliably in cron jobs |
| Click TechCrunch article heading from listing page | `ref=e57` on "OpenAI unveils Lockdown Mode..." | **Article loaded correctly with full content** | Click-through from TechCrunch listing page WORKS — ref IDs point to the article |
| Click TechCrunch article heading from listing page (WWDC) | `ref=e59` on "What to expect from WWDC 2026..." | **Article loaded correctly with full content** | Second confirmed success via listing click-through |
| HN Algolia API via curl | `hn.algolia.com/api/v1/search?query=AI+OR+artificial+intelligence&hitsPerPage=8` | 400 error: "Unknown parameter: rows" | Parameter is `hitsPerPage`, not `rows` |
| HN Algolia API — correct parameter | `hn.algolia.com/api/v1/search?query=AI+OR+artificial+intelligence&tags=story&hitsPerPage=8` | Returned older/irrelevant HN posts | HN Algolia API search quality is poor for current AI news — not reliable as primary source |
| Google News search page via browser_navigate | `news.google.com/search?q=AI+artificial+intelligence` | Lead stories were 2–5 days old (IMDb, Guardian, AP) | Google News search page lead section is not a same-day AI news scan |

**Key clarification — TechCrunch URL stability:**
- Direct navigation to TechCrunch article URLs is unreliable (404).
- **Click-through from the TechCrunch AI listing page works reliably** — do NOT copy the URL from the address bar and re-navigate to it directly.

### New Observations — 2026-06-09 (Evening Scout)

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Navigate to TechCrunch homepage | `techcrunch.com/` | Rich snapshot with AI headlines — lead stories 15–17h old | TechCrunch homepage is a viable primary source — snapshot captures headline text directly without click-through |
| Navigate to The Verge article URL | Direct `theverge.com/ai-models/2026/6/9/apple-siri-wwdc-ai` | 404 page | The Verge article URLs also 404 on direct navigation |
| Navigate to The Verge AI section | `theverge.com/ai` | Timed out / no response | The Verge AI section is unreliable in this session — possibly load-dependent |
| Navigate to artificialintelligence.news | `artificialintelligence.news` | 404 page | AINS is offline or restructured — not a reliable source in current session |
| Navigate to Google News search page | `news.google.com/search?q=AI+technology+2026&hl=en-US&gl=US&ceid=US:en` | Loaded cleanly with headlines | Google News search page remains a reliable fallback listing source |

**Key finding — TechCrunch homepage snapshot IS the article:** Reading the TechCrunch homepage snapshot is sufficient to extract 3 article summaries without clicking through.

**Sites that 404 on direct article URL navigation (confirmed this session):**
- TechCrunch (`/YYYY/MM/DD/{slug}/` pattern)
- Business Insider
- The Verge
- Guardian

**Sites confirmed blocked in cron context (do not rely on):**
- artificialintelligence.news (404/offline) — as of 2026-06-09
- CNET search (empty results)
- Yahoo search (error page)
- Reuters/DataDome sites (hard block)

### New Observations — 2026-06-12 (Evening Scout)

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Navigate to The Verge AI section, click article heading | `ref=e66` on "Anthropic apologizes for invisible Claude Fable guardrails" | Click succeeded, article loaded | Click-through from The Verge AI listing page works reliably |
| Navigate directly to The Verge article URL | `theverge.com/anthropic-apologizes-invisible-claude-fable-guardrails` | 404 page | **The Verge article URLs 404 on direct navigation** — do NOT use direct article URLs |
| Navigate to artificialintelligence-news.com | `artificialintelligence-news.com` | Homepage loaded with cookie consent dialog | **AINS is back online** — `www.` prefix required, not `artificialintelligence.news` |
| Accept cookie consent on AINS | `ref=e3` "Accept" button | Dialog dismissed, article listings accessible | Handle cookie consent with browser_click before reading content |
| Click article heading from AINS homepage | `ref=e123` on "Visa ChatGPT integration enables AI agent retail purchasing" | `(empty page)` — anti-bot on heading click | Heading-click anti-bot on AINS confirmed — same silent interception pattern |
| Navigate directly to AINS article URL | `https://www.artificialintelligence-news.com/news/visa-chatgpt-integration-enables-ai-agent-retail-purchasing/` | **Page loaded correctly with full article** | **AINS direct article URLs are stable and reliable** — use direct navigation instead of heading click |
| Read AINS article via browser_snapshot(full=false) | After direct navigation | 138 elements, full article text readable | Compact snapshot sufficient for AI news articles |

**Key findings — 2026-06-12:**
- **The Verge article URLs 404 on direct navigation** — click-through from the listing page is the only reliable path.
- **AINS is back online** — `www.artificialintelligence-news.com` is accessible. Use the `www.` prefix.
- **AINS article URLs are stable via direct navigation** — the full slug path works. Heading click anti-bot still intercepts — navigate directly.
- **Cookie consent on AINS** — dismiss with `browser_click("Accept")` before reading content.

**Updated AINS research-scout workflow (2026-06-12):**
```
1. Navigate to www.artificialintelligence-news.com
2. browser_click "Accept" on cookie consent dialog
3. Read snapshot — identify top 3 articles by headline
4. For each article: navigate directly to https://www.artificialintelligence-news.com/news/{slug}/
5. browser_snapshot(full=false) — verify title, read article
6. Do NOT click heading links from the AINS homepage — anti-bot intercepts them
```

**Updated The Verge research-scout workflow (2026-06-12):**
```
1. Navigate to theverge.com/ai-artificial-intelligence
2. Read snapshot — identify top 3 articles by headline and recency
3. browser_click on article heading ref from the listing (NOT from any other page)
4. browser_snapshot(full=false) — verify title, read article
5. Do NOT use direct article URLs (theverge.com/{slug}) — they 404
```

### New Observations — 2026-06-13 (Evening Scout)

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Navigate to The Verge AI section, click SpaceX article heading | `ref=e22` on "SpaceX reportedly rented out Colossus 1..." | Click registered, no error, but snapshot still showed listing page | **New silent failure mode:** click consumed but page stays on listing — not empty, not homepage. Detect with `browser_console('window.location.href')`. |
| Navigate to AINS direct article URL (Siri AI slug) | `.../siri-ai-arrives-with-google-inside-and-much-of-the-world-is-locked-out/` | **Redirected to Luca Boschin VISUA CEO interview (Aug 2021)** — wrong article | **AINS slug URLs are not guaranteed stable** — slugs can resolve to unrelated content. Always verify title immediately after direct navigation. |
| Google News search for Anthropic Fable/Mythos export control | `news.google.com/search?q=Anthropic+Fable+Mythos+export+control+June+2026` | Loaded cleanly, 10+ sources (Reuters, CNBC, Business Insider, AP, Fortune, MarkTechPost) | **Google News is the reliable rescue** when all primary-source paths fail. |
| Google News search for SpaceX Colossus rental story | `news.google.com/search?q=SpaceX+Colossus+AI+data+center+rented+latency+June+2026` | Bloomberg lead, confirmatory sources (Stocktwits, IndexBox, Crypto Briefing) | Same — Google News delivers multi-source confirmation without needing original article. |
| AINS Visa ChatGPT article via direct URL | `.../visa-chatgpt-integration-enables-ai-agent-retail-purchasing/` | Page loaded correctly, 138 elements, title confirmed | AINS direct navigation works for stable slugs — the Siri redirect was an outlier. |

**Key findings — 2026-06-13:**
- **The Verge listing click-through can silently fail** — snapshot stays on listing page without error. Check `browser_console('window.location.href')` after any click — if URL unchanged, fall to Google News.
- **AINS slug URLs can redirect to unrelated content** — slugs are not permanent. Verify title on every direct navigation; if wrong, use Google News search instead.
- **Google News search is the universal rescue** — confirmed on two stories where primary methods both failed. Delivers multi-source confirmation with recency in a compact snapshot, no anti-bot issues.
- **3-source research-scout pattern (confirmed 2026-06-13):** (1) The Verge listing click-through for top stories, (2) AINS direct navigation for stories seen there, (3) Google News search for any story that both primary methods can't deliver — it replaces any broken path without retry loops.

**Universal rescue flow (2026-06-13 confirmed):**
```
Primary source click-through or direct navigation
  → browser_snapshot: title confirmed? → proceed.
  → title not confirmed? → browser_console('window.location.href').
  → URL unchanged (silent failure) or wrong article (slug redirect)? → Google News search for the topic.
  → Google News delivers multi-source snapshot → sufficient for summary, no further clicking needed.
```

### New Observations — 2026-06-14 (Evening Scout)

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|---------|-----------|
| Google News RSS via `curl` terminal | `https://news.google.com/rss/search?q=AI+technology+OR+LLM+OR+artificial+intelligence&hl=en-US&gl=US&ceid=US:en&tbs=qdr:d` | Full RSS XML with dozens of `<item>` elements returned. Titles, pubDates, and links all present. | **RSS via terminal WORKS in cron jobs** — reliable primary fetch method. Faster than browser navigation, zero anti-bot risk. |
| Google News RSS with `tbs=qdr:d` parameter | Same URL with `tbs=qdr:d` appended | Filters results to past 24 hours. PubDate analysis shows stories from the same day. | **`tbs=qdr:d` is the correct parameter for same-day scanning** — without it, results span multiple days. |
| Navigate to Politico article via Google News link | Politico.com link in Google News results | Cloudflare challenge, then access denied | Politico always blocked in cron jobs. Use Google News snippets or secondary coverage. |
| Navigate directly to Nature.com article URL | `nature.com/articles/s41586-026-00372-4` | 404 page | Nature article URLs are unpredictable; navigate via Google News or skip. |
| Navigate to The Hacker News article via direct URL | `thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding-agents-into-running-malicious-code.html` | 404 page | THN direct article URLs frequently 404 even for recent articles. Use Google News listing to find the article and click through from there. |
| Navigate to CyberPress article via direct URL | `cyberpress.org/new-agentjacking-attack-compromises-ai-coding-agents-for-code-execution/` | 404 page | CyberPress article URLs can 404 even when the article title appears in their own listing page. Use the listing page as entry point, not direct URL. |
| Google News search page for "agentjacking" | `news.google.com/search?q=%22agentjacking%22+AI+coding+agents+security` | Full listing with 5 sources (THN, Infosecurity Magazine, CyberPress, etc.) | Google News is the reliable index even when direct article URLs are broken. |
| Navigate to NDTV article via Google News link | NDTV.com link in Google News results | Access denied | NDTV blocked in cron jobs. Use alternative source. |

**Key findings — 2026-06-14:**
- **Google News RSS via terminal is a valid primary fetch** — the "RSS fails in cron jobs" note in SKILL.md was wrong. Use `curl` to get the RSS XML directly, parse titles and pubDates with grep. This is faster than browser navigation and has no anti-bot surface.
- **Direct article URLs for THN, CyberPress, Nature, Politico, NDTV are unreliable** — always use Google News as the index; find the article there and navigate to the source link only if the source is known to work (The Verge, TechCrunch listing page, AINS).
- **Google News search page `tbs=qdr:d` parameter limits to past 24 hours** — always include this when doing a same-day scan.
- **Research-scout workflow (updated 2026-06-14):** (1) `curl` Google News RSS with `tbs=qdr:d` for fast same-day headline scan, (2) Google News search page for clickable links to sources, (3) verify title after any navigation, (4) skip any site that triggers Cloudflare or access denied — Google News has alternative sources for every story.

### New Observations — 2026-06-14 (This Session)

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Navigate to TechCrunch AI category page | `techcrunch.com/category/artificial-intelligence/` | Full listing loaded: headlines, recency stamps (11h, 14h, 17h ago), author bylines | **TechCrunch listing page is reliable entry point** — all scout data available directly from snapshot without click-through |
| Direct TechCrunch article URL | `techcrunch.com/2026/06/14/...` | 404 — same-day articles 404 on direct navigation | Confirmed: TechCrunch article URLs unstable for direct nav |
| Click TechCrunch heading from listing | `ref=e57` on "As Anthropic suspends..." | Snapshot stayed on listing — click-through SILENTLY FAILED | **TechCrunch click-through can also silently fail** — do not rely on it |
| Google.com, Bing.com search | Direct search engine nav | Cloudflare challenge/CAPTCHA blocked | Never attempt direct search engine navigation in cron jobs |
| delegate_task `web` subagents for 3 TechCrunch articles | 3 parallel subagents | All returned empty/minimal — subagent web searches return no live content | **Confirmed: delegate_task `web` toolset does not fetch live article content in cron jobs** |
| Write scout from listing page headline data alone | Snapshot: title + author + recency + category tag | Sufficient to write 3-item scout summary without article body | **Minimal viable scout:** listing data × 3 = signal-quality output. Article body is optional. |

**Key additions (2026-06-14):**
- **TechCrunch: both direct URLs AND listing click-through fail.** Use listing snapshot as primary source — extract signal from headlines, skip article body.
- **delegate_task with `web` toolset confirmed unreliable** for live fetching in cron jobs — do not substitute for direct browser reading.
- **Minimal viable research scout:** headline + author + recency + category tag × 3 = sufficient. No article body required.

**Updated workflow (2026-06-14 final):**
```
1. curl Google News RSS with tbs=qdr:d  → fast same-day headline scan
2. Navigate TechCrunch AI listing → extract top 3 by headline + recency
3. Any article path fails? → Google News search page for the topic (universal rescue)
4. delegate_task web subagents → NOT a substitute for direct reading
5. Write ~/.hermes/memories/research-YYYY-MM-DD.md from listing/snapshot data
```

**Sites BLOCKED (never attempt):** Google.com, Bing.com, Politico, NDTV, Reuters/DataDome, Nature.com, THN direct URLs, CyberPress direct URLs.
**Sites RELIABLE:** TechCrunch listing (extract-only), The Verge listing+click, AINS direct URLs, Google News (search + RSS).
