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

- **Avoid direct web browsing for general research in cron jobs:** If a task requires fetching unstructured information from the open web (e.g., "recent news for X," "top companies in Y sector"), assume the `browser` tools will be unreliable in a cron job.
- **Prefer specialized tools or APIs:** If specific data sources (e.g., arXiv, Polymarket, or a structured API) are available and can be accessed without browser interaction (e.g., via `terminal` with `curl` or a Python library), these should be prioritized.
- **Use Google News RSS as a lightweight workaround:** For batch news scanning (earnings, price moves, headlines across multiple companies), Google News RSS works reliably in cron jobs:
  ```
  curl -s "https://news.google.com/rss/search?q={COMPANY}+stock&hl=en-US&gl=US&ceid=US:en"
  ```
  Use `grep -o '<title>[^<]*</title>' | head -N` to extract headlines fast. This is much faster than browser navigation and avoids anti-bot blocking. Limitation: only titles + snippets, not full articles.
- **Google News via browser_navigate — WORKS WELL in cron jobs:**  \
Navigate to `https://news.google.com/search?q=QUERY&hl=en-US&gl=US&ceid=US:en`. The search results page is lightweight and rarely blocked. Click through to individual articles for detail. Tested successfully on 2026-05-23 for AI research scout. Caveats: some paywalled sites (NYT) show only a block page; some sites (Forbes) return 404 on article URLs even when linked from Google News — for those, rely on secondary sources.

**Article URL gotcha:** Google News links to articles via the Google News redirect (e.g., `https://news.google.com/articles/...`). When clicking through from the Google News listing page, use the actual article link in the snapshot (ref=ex), not any Google redirect URL. Direct source links from the listing are more stable than the `?url=...` redirect pattern.

**Bing.com** — displays a Cloudflare human verification challenge (checkbox "Verify you are human") before returning search results. Avoid in cron jobs.

**Use delegate_task subagents with `web` toolset for multi-sector research (RECOMMENDED):** For structured company/sector research (top 5 companies by market cap, recent news, valuations), spawn delegate_task subagents with the `web` toolset. Each subagent independently searches and returns structured JSON. This approach is reliable, parallelizable, and bypasses anti-bot blocking because each subagent runs in its own context with fresh tool state.

  Example workflow for "Victor Company Study" (5 sectors × 5 companies):
  1. Run up to 3 subagents in parallel (the default `max_concurrent_children` limit).
  2. Prompt each subagent to return raw JSON only — no preamble, no markdown.
  3. Merge results, then run a second wave for remaining sectors if needed.
  4. Compile findings into `~/.hermes/memories/victor-study-YYYY-MM-DD.md`.

  ```python
  # Wave 1: 3 sectors
  delegate_task(tasks=[
    {"goal": "Return JSON array of top 5 AI/ML companies...", "toolsets": ["web"]},
    {"goal": "Return JSON array of top 5 Semiconductors...", "toolsets": ["web"]},
    {"goal": "Return JSON array of top 5 Cloud companies...", "toolsets": ["web"]},
  ])
  # Wave 2: remaining 2 sectors
  delegate_task(tasks=[
    {"goal": "Return JSON array of top 5 E-commerce...", "toolsets": ["web"]},
    {"goal": "Return JSON array of top 5 Cybersecurity...", "toolsets": ["web"]},
  ])
  ```

  This subagent approach was validated on 2026-05-22 for Victor Company Study — all 5 sectors returned good data with no anti-bot failures.

- **Inform the user:** If a cron job fails due to these limitations, clearly communicate the reason for the failure and the observed anti-bot measures.
