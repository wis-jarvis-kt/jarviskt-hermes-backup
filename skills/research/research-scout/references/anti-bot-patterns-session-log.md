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

### New Observations — 2026-05-31

| Action | URL/Element | Result | Diagnosis |
|--------|-------------|--------|-----------|
| Click AI News heading link from LATEST section — NBA AI article | `ref=e132` on "NBA plans AI system..." in LATEST section | `(empty page)`, `element_count: 0` | LATEST section heading links appear to have higher anti-bot hit rate than featured section links |
| Google News search for NBA AI → click Reuters result | Reuters link (`ref=e36`) in Google News results | DataDome device verification block | Reuters via Google News click is a CONFIRMED hard block (not occasional) |
| Navigate directly to Yahoo Sports NBA article URL | `sports.yahoo.com/nba/...` from Google News address bar URL | 404 page not found | Yahoo Sports article URLs expire/are restructured — do not rely on copied GN address bar URL |
| Navigate directly to FanSided NBA article URL | `fansided.com/2025/05/28/...` | 404 page not found | Same URL rot issue |
| Navigate directly to KTLA NBA article | `ktla.com/news/nba-...` | Cloudflare block | Local news sites also use Cloudflare |
| Navigate directly to LarryBrownSports | `larrybrownsports.com/nba-...` | Cloudflare block | Cloudflare is widespread across mid-tier sports media |
| Click AI News heading link — Google Pay UCP article | `ref=e121` from featured section | **Page loaded correctly** | Featured section heading links still have ~67% success rate |
| Click AI News heading link — OpenAI FGF article | `ref=e117` from featured section | `(empty page)`, `element_count: 0` | Same intermittent pattern confirmed |

### Key Learnings (Updated)

- **LATEST section heading links may have a higher anti-bot hit rate** than the main featured article heading links. Prefer the top 2–3 featured articles (large cards at top of page) before scrolling to LATEST.
- **Reuters via Google News is a hard block — do not retry.** DataDome on Reuters is a confirmed blocker in cron job context. When Reuters appears in Google News results, skip it and click through to a different outlet's link.
- **After DataDome/Cloudflare block, do NOT iterate through other news aggregator sites** — Yahoo Sports, FanSided, KTLA, LarryBrownSports all either 404 or Cloudflare-block in rapid succession. Instead: (a) stay on Google News results, (b) find a different non-Reuters/non-NYT outlet's link, (c) click through to that outlet's direct native domain.
- **Yahoo Sports and FanSided article URLs are not stable** — they return 404 when navigated to directly even hours after publication. Do not use copied Google News address bar URLs for these sites.
- **The anti-bot trigger is the INDIRECT click path** (AI News homepage → heading link), not direct navigation to AI News article URLs. Both article pages loaded fine when navigated to directly.
- **Heading-click anti-bot is INTERMITTENT on featured section links (~67% success).** LATEST section links appear worse. Always have direct URL fallback ready.
- **Viable workflow: click heading → if empty page, back to homepage and continue.** No need to immediately reach for direct URL on first failure — proceed to next article and use direct URL as rescue only if needed.
- **browser_snapshot(full=false) is sufficient for article reading** even on longer articles. The 132–142 element count captured full article text. Use full=true only when compact snapshot returns suspiciously little content.
- **Google News → original publication (TechCrunch, blog.google) works reliably for non-blocked outlets.** The failure mode is clicking links that point to Reuters, NYT, or other DataDome-protected domains.
- **Always check the browser address bar URL** after any navigation — anti-bot redirects leave the URL in an unexpected state, but a correct article URL can be copied from the address bar for non-aggregator sources.
- **Timestamps on Google News are relative** ("21 hours ago", "Yesterday") — article may actually be from the prior calendar day. Cross-reference with AI News homepage dates.
- **AI News homepage date reliably shows today's articles** in the top 2–3 headline slots. Older articles (May 28, May 27) are still runnable if genuinely notable.
- **Major news sites (NYT, CNBC, Reuters) block via DataDome/Cloudflare** when navigating through Google News click paths. Navigate directly to known article URLs or use a non-blocked outlet's Google News link.

### URL Patterns (Updated)

```
AI News direct article:   https://www.artificialintelligence-news.com/news/{slug}/
Google News search:       https://news.google.com/search?q={QUERY}&hl=en-US&gl=US&ceid=US:en
CNBC article URL format:  https://www.cnbc.com/YYYY/MM/DD/{slug}.html  (date in path)
```

### Quick Diagnosis Flow

```
Article title confirmed on AI News homepage
    ↓
browser_click on heading link ref
    ↓
browser_snapshot(full=true)
    ↓
[ element_count: 0 ] → empty page → STOP, don't retry
    ↓
Copy address bar URL OR search Google News for the story
    ↓
Navigate to original source domain directly
    ↓
browser_snapshot(full=true) → verify title
```
