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

### Key Learnings (Updated)

- **The anti-bot trigger is the INDIRECT click path** (AI News homepage → heading link), not direct navigation to AI News article URLs. Both article pages loaded fine when navigated to directly.
- **Heading-click anti-bot is INTERMITTENT.** Two heading clicks succeeded (Claude Opus 4.8, Google Pay UCP) while one failed (OpenAI FGF). The pattern is probabilistic (~67% success in this session), not systematic. Always have direct URL fallback ready.
- **Viable workflow: click heading → if empty page, back to homepage and continue.** No need to immediately reach for direct URL on first failure — proceed to next article and use direct URL as the rescue only if needed.
- **browser_snapshot(full=false) is sufficient for article reading** even on longer articles. The 132–142 element count captured full article text. Use full=true only when compact snapshot returns suspiciously little content.
- **Google News → original publication (TechCrunch, blog.google, Reuters) works reliably.** The failure mode is clicking links that point back to aggregators.
- **Always check the browser address bar URL** after any navigation — anti-bot redirects leave the URL in an unexpected state, but a correct article URL can be copied from the address bar.
- **Timestamps on Google News are relative** ("21 hours ago", "Yesterday") — article may actually be from the prior calendar day. Cross-reference with AI News homepage dates.
- **AI News homepage date reliably shows today's articles** in the top 2–3 headline slots. Older articles (May 28, May 27) are still runnable if genuinely notable.
- **Major news sites (NYT, CNBC) block via DataDome/Cloudflare** when navigating through Google News click paths. Navigate directly to known article URLs or use the article's direct domain link.

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
