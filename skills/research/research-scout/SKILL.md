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
3. **Scan headlines** for 3 notable AI/tech developments. Prioritise articles with today's date. Click article links with `browser_click` on the heading link (not the image or sub-link).
4. **Verify page title after each navigation** — if the title doesn't match the expected article, the link may have been redirected by anti-bot protection. Use Google News search as fallback.
5. **Read each article** via `browser_snapshot(full=true)` — capture title, source date, key points, and "why it matters" takeaway.
6. **If an article link misbehaves** (wrong page, redirect, anti-bot), use Google News search for that topic: `https://news.google.com/search?q=TOPIC&hl=en-US&gl=US&ceid=US:en`
7. **After `browser_back()` — always take a fresh snapshot before clicking.** Ref IDs from a pre-`back()` snapshot are stale and will produce `Unknown ref` errors or wrong elements. Call `browser_snapshot(full=false)` to get current IDs before every subsequent click on a previously-seen page.
8. **If fewer than 3 articles with today's date appear on the homepage**, scroll down the "LATEST" section. If still insufficient, use Google News (`https://news.google.com/search?q=AI+technology&hl=en-US&gl=US&ceid=US:en`) to find supplementary stories — click through to source articles rather than reading in Google's aggregator. Prioritise developments that are genuinely new (not dated several days prior) even if the primary source is not the AI News homepage.
9. **Write findings** to `~/.hermes/memories/research-YYYY-MM-DD.md` with frontmatter header:

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

10. **Verify the file** by reading back the first few lines (check line count and last entry's "Why it matters" is present).

## Verified Working Sources (cron job context)

| Source | URL | Notes |
|---|---|---|
| AI News | `https://www.artificialintelligence-news.com/` | Reliable, no anti-bot. Accept cookie dialog first. |
| Google News Search | `https://news.google.com/search?q=QUERY&hl=en-US&gl=US&ceid=US:en` | Lightweight, rarely blocked. |

## Anti-Bot Patterns to Avoid

- **Google News RSS** (`news.google.com/rss/search?q=...`) — returns zero `<item>` elements in cron job context. Use browser navigation instead.
- **Google News direct article URLs from AI News listing** — can redirect unexpectedly to an empty page or a different article on the same domain. Always verify page title after navigation; if wrong, fall back to Google News search for the original source publication.
- **Bing.com** — triggers Cloudflare human verification in cron jobs.
- **Clicking image links or sub-links** — click the article heading link, not attached images or category tags, to avoid anti-bot traps on secondary elements.
- **AI News article heading links** — when you land on an AI News article listing and click the heading link, it may resolve to an empty `(empty page)`. **Fallback: copy the article's canonical URL from the browser address bar after navigation (which resolves correctly), or find the article via Google News search and click through to the original source publication (TechCrunch, blog.google, Reuters, etc.) rather than the aggregator link.**
- **Google News links pointing back to AI News** — these also frequently misbehave (land on empty page). When researching via Google News, click through to the original article source on its native domain, not the AI News mirror.
- **`(empty page)` on snapshot after click** — if `browser_snapshot(full=true)` returns `(empty page)` with `element_count: 0`, the link triggered an anti-bot redirect. Do NOT retry the click. Instead: (a) note the story from Google News results, (b) navigate directly to the original source URL, (c) verify with snapshot. Never use browser back and re-click the same link — it will fail again.

## Rescue Pattern (Empty Page After Click)

```
1. browser_snapshot(full=true) → element_count: 0 → empty page detected
2. Do NOT retry the click or use browser_back() yet
3. Check the current URL in browser address bar — it may have redirected
4. If redirected to AI News or unknown domain → use Google News search for
   the story and navigate directly to the original source (TechCrunch,
   blog.google, Reuters, etc.)
5. browser_snapshot(full=true) to verify correct article loaded
6. Proceed with reading
```

## Save Format

Use this exact header format so future agents can parse it:

```
# AI/Tech Research Scout — {date}

## Evening Scan: 3 Notable Developments
```

Each entry must include: source + date, category, summary, key points, and "why it matters."

## Support Files

- `references/anti-bot-patterns-session-log.md` — session-tested anti-bot patterns, URL workarounds, and rescue flow. Updated after each scout run that encounters blocking.

## Related Skills

- `web-research-limitations` — anti-bot patterns, delegate_task subagent workflow for multi-sector research
- `arxiv` — academic paper discovery
- `polymarket` — market-sentiment research
- `blogwatcher` — recurring blog/RSS monitoring