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
3. **Scan headlines** for 3 notable AI/tech developments. Click article links with `browser_click` on the heading link (not the image or sub-link).
4. **Verify page title after each navigation** — if the title doesn't match the expected article, the link may have been redirected by anti-bot protection. Use Google News search as fallback.
5. **Read each article** via `browser_snapshot(full=true)` — capture title, source date, key points, and "why it matters" takeaway.
6. **If an article link misbehaves** (wrong page, redirect, anti-bot), use Google News search for that topic instead: `https://news.google.com/search?q=TOPIC&hl=en-US&gl=US&ceid=US:en`
7. **Write findings** to `~/.hermes/memories/research-YYYY-MM-DD.md` with frontmatter header:

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

## Verified Working Sources (cron job context)

| Source | URL | Notes |
|---|---|---|
| AI News | `https://www.artificialintelligence-news.com/` | Reliable, no anti-bot. Accept cookie dialog first. |
| Google News Search | `https://news.google.com/search?q=QUERY&hl=en-US&gl=US&ceid=US:en` | Lightweight, rarely blocked. |

## Anti-Bot Patterns to Avoid

- **Google News RSS** (`news.google.com/rss/search?q=...`) — returns zero `<item>` elements in cron job context. Use browser navigation instead.
- **Google News direct article URLs** from AI News listing — can redirect unexpectedly to a different article on the same domain. Always verify page title after navigation; if wrong, fall back to Google News search.
- **Bing.com** — triggers Cloudflare human verification in cron jobs.
- **Clicking image links or sub-links** — click the article heading link, not attached images or category tags, to avoid anti-bot traps on secondary elements.

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