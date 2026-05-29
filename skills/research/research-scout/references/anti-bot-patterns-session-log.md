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

### Key Learnings

- **The anti-bot trigger is the INDIRECT click path** (AI News homepage → heading link), not direct navigation to AI News article URLs. Both article pages loaded fine when navigated to directly.
- **Google News → original publication (TechCrunch, blog.google, Reuters) works reliably.** The failure mode is clicking links that point back to aggregators.
- **Always check the browser address bar URL** after any navigation — anti-bot redirects leave the URL in an unexpected state, but a correct article URL can be copied from the address bar.
- **Timestamps on Google News are relative** ("21 hours ago", "Yesterday") — article may actually be from the prior calendar day. Cross-reference with AI News homepage dates.
- **AI News homepage date reliably shows today's articles** in the top 2–3 headline slots (May 29 → "Anthropic releases Claude Opus 4.8" published today). Older articles (May 28, May 27) are still runnable if genuinely notable.

### URL Patterns

```
AI News direct article:   https://www.artificialintelligence-news.com/news/{slug}/
Google News search:       https://news.google.com/search?q={QUERY}&hl=en-US&gl=US&ceid=US:en
Google News article link: [varies — click to original source domain]
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
