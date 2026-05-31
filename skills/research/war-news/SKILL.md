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
3. **Accept cookie consent** if dialog appears (click "Accept" or "Reject" as offered).
4. **Scan headlines** for conflict-relevant stories — use `browser_snapshot(full=false)` on each section page.
5. **Click through** to 2–3 relevant articles for detail. Verify title after each navigation.
6. **If BBC sections lack fresh conflict coverage**, supplement with:
   - Google News search: `https://news.google.com/search?q=ukraine+russia+war&hl=en-US&gl=US&ceid=US:en`
   - Google News search: `https://news.google.com/search?q=israel+gaza+iran&hl=en-US&gl=US&ceid=US:en`
7. **Write findings** to `~/.hermes/memories/war-news-YYYY-MM-DD.md` with this format:

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
| BBC World Europe | `https://www.bbci.co.uk/news/world/europe` | Ukraine/Russia — reliable, no anti-bot |
| BBC Middle East | `https://www.bbc.com/news/world/middle_east` | Israel, Iran, Gaza |
| BBC Asia | `https://www.bbc.com/news/world/asia` | South China Sea, Taiwan |
| Google News | `https://news.google.com/search?q=...` | Fallback supplement |

## Anti-Bot Notes

- BBC RSS feeds work but provide only `<title>` + `<description>` — insufficient for detail. Use browser navigation for full articles.
- Google News RSS (`news.google.com/rss/search?q=...`) returns empty `<item>` lists in cron jobs — use browser nav instead.
- Reuters via Google News is a *confirmed hard block* — navigate directly to Reuters or find alternative outlet.

## Related Skills

- `web-research-limitations/references/conflict-news-rss.md` — RSS feed URLs and keyword patterns for conflict filtering
- `research-scout` — AI/tech research (separate from conflict news)
