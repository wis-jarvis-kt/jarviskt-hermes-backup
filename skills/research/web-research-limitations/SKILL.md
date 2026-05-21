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
- **Inform the user:** If a cron job fails due to these limitations, clearly communicate the reason for the failure and the observed anti-bot measures.
