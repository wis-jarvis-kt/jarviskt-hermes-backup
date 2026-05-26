---
name: research-scout
description: "Recurring evening AI/tech research scout: find 3 notable developments, save to ~/.hermes/memories/research-YYYY-MM-DD.md. For one-shot or ad-hoc research, prefer delegate_task subagents with the `web` toolset."
version: 1.0.0
---

# Research Scout

Run a recurring evening scan of AI/tech developments and save a brief report to `~/.hermes/memories/research-YYYY-MM-DD.md`.

## Workflow

1. **Navigate** to `https://www.artificialintelligence-news.com/` — loads reliably in cron jobs (no anti-bot blocking observed).
2. **Accept cookie consent** if dialog appears: `browser_click(ref=e3)` on "Accept".
3. **Scan headlines** for 3 notable AI/tech developments. Click through with `browser_click` on article links from the listing page.
4. **Read each article** via `browser_snapshot(full=true)` — capture title, source date, key points, and "why it matters" takeaway.
5. **Write findings** to `~/.hermes/memories/research-YYYY-MM-DD.md` with frontmatter header:

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

6. **Verify the file** was written by reading back the first few lines.

## Verified Working Sources (cron job context)

| Source | URL | Notes |
|---|---|---|
| AI News | `https://www.artificialintelligence-news.com/` | Reliable, no anti-bot. Accept cookie dialog first. |
| Google News Search | `https://news.google.com/search?q=QUERY&hl=en-US&gl=US&ceid=US:en` | Lightweight, rarely blocked. |

## Anti-Bot Patterns to Avoid

- **Google News RSS** (`news.google.com/rss/search?q=...`) — returns zero `<item>` elements in cron job context. Use browser navigation instead.
- **Google News direct article URLs** from listing — can redirect unexpectedly. Always verify page title after navigation.
- **Bing.com** — triggers Cloudflare human verification in cron jobs.

## Save Format

Use this exact header format so future agents can parse it:

```
# AI/Tech Research Scout — {date}

## Evening Scan: 3 Notable Developments
```

Each entry must include: source + date, category, summary, key points, and "why it matters."

## Related Skills

- `web-research-limitations` — anti-bot patterns, delegate_task subagent workflow for multi-sector research
- `arxiv` — academic paper discovery
- `polymarket` — market-sentiment research
- `blogwatcher` — recurring blog/RSS monitoring