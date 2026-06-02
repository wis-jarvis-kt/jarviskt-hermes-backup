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
| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Google News "AI technology June 2 2026" → click NVIDIA Newsroom | NVIDIA Newsroom link in Build/AI search | Page loaded correctly with full article | NVIDIA Newsroom accessible via Google News click path. |
| Google News "Microsoft Build AI announcements today" → click PCMag Australia | PCMag Australia link in live coverage search | Page loaded correctly with live blog content | PCMag Australia does not block via Google News click path. |
| Google News "AI technology June 2 2026" → click Mashable Microsoft Build | Mashable link in AI tech search | Page loaded correctly with article content | Mashable accessible via Google News click path. |
| Google News "Nvidia AI PC chip" → click Hawaii Tribune-Herald (reprint) | Hawaii Tribune-Herald Reuters wire article | Page loaded correctly with full Reuters content | Local wire-reprint papers block less than Reuters direct; rescue path for blocked wire stories. |
| Google News "China AI trade secret" → click Euronews | Euronews article on China AI IP rules | Page loaded correctly | Euronews accessible via Google News for policy/trade topics. |
| Politico via Google News (Florida/OpenAI story) | Politico link in AI tech search | Cloudflare challenge page, then block | Politico uses Cloudflare — same recovery pattern as other Cloudflare sites (back out, navigate direct). |
| Click Reuters link from Google News results | Reuters in search listings | DataDome device check block | Confirmed hard block; skip Reuters, use local wire-reprint outlet or direct TechCrunch/VentureBeat. |

### New Observations — 2026-06-02

- **Local wire-reprint papers (e.g. Hawaii Tribune-Herald) are accessible via Google News** — they reprint Reuters wire stories and are blocked less often than the original. Useful rescue path when Reuters is directly blocked. Direct navigation works.
- **Euronews is accessible via Google News click paths** for policy/trade topics (China AI IP, EU tech regulation). Not systematically blocked like Reuters/DataDome sites.
- **Cloudflare challenge pages — recovery pattern:** After a Cloudflare challenge clears (user/script exits the page), `browser_back()` often recovers to the correct final URL. The URL bar shows the intended destination even during the challenge. Quick redirect cycle clears the session.
- **Money Morning is anti-bot blocked via Google News click path** — same `(empty page)` pattern as Reuters. Treat it like other blocked aggregators.
- **TechCrunch, NVIDIA Newsroom, PCMag Australia, and Mashable are accessible via Google News click paths** — no anti-bot blocking observed on these outlets.
- **Direct navigation to TechCrunch and Money Morning works reliably** — bypasses anti-bot on the click path.
- **Google News → original source click path is reliable for non-blocked outlets** (TechCrunch, NVIDIA, PCMag, Mashable). Failure modes remain: Reuters (DataDome), Money Morning (anti-bot), and generic `(empty page)` on some outlets.
- **browser_snapshot(full=false) is sufficient for live blogs and longer-form articles** — PCMag Australia live blog returned 73 elements with full content visible.
- **Always verify the article title after navigation** — when anti-bot redirect occurs, `browser_snapshot` returns homepage content with ref IDs matching the homepage, not an empty page. Both empty-page and homepage-return are anti-bot signals.
- **LATEST section heading links may have a higher anti-bot hit rate** than the main featured article heading links. Prefer the top 2–3 featured articles (large cards at top of page) before scrolling to LATEST.
- **Reuters via Google News is a hard block — do not retry.** DataDome on Reuters is a confirmed blocker. When Reuters appears in Google News results, skip it and click through to a different outlet's link.
- **After DataDome/Cloudflare block, do NOT iterate through other news aggregator sites** — stay on Google News results, find a different non-blocked outlet's link.
- **Yahoo Sports and FanSided article URLs are not stable** — they return 404 when navigated to directly even hours after publication. Do not use copied Google News address bar URLs for these sites.
- **The anti-bot trigger is the INDIRECT click path** (AI News homepage → heading link), not direct navigation to AI News article URLs. Both article pages loaded fine when navigated to directly.
- **Heading-click anti-bot is INTERMITTENT on featured section links (~67% success).** LATEST section links appear worse. Always have direct URL fallback ready.
- **browser_snapshot(full=false) is sufficient for article reading** even on longer articles. The 132–142 element count captured full article text. Use full=true only when compact snapshot returns suspiciously little content.
- **Always check the browser address bar URL** after any navigation — anti-bot redirects leave the URL in an unexpected state.
- **Timestamps on Google News are relative** ("21 hours ago", "Yesterday") — article may actually be from the prior calendar day. Cross-reference with AI News homepage dates.
- **AI News homepage date reliably shows today's articles** in the top 2–3 headline slots.
- **Major news sites (NYT, CNBC, Reuters) block via DataDome/Cloudflare** when navigating through Google News click paths. Navigate directly to known article URLs or use a non-blocked outlet's Google News link.

### URL Patterns (Updated)

```
AI News direct article:    https://www.artificialintelligence-news.com/news/{slug}/
Google News search:        https://news.google.com/search?q={QUERY}&hl=en-US&gl=US&ceid=US:en
CNBC article URL format:   https://www.cnbc.com/YYYY/MM/DD/{slug}.html  (date in path)
TechCrunch direct:         https://techcrunch.com/YYYY/MM/DD/{slug}/
NVIDIA Newsroom direct:    https://blogs.nvidia.com/blog/{slug}/
Hawaii Tribune-Herald:     https://www.hawaiitribune-herald.com/YYYY/MM/DD/{slug}/
```

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