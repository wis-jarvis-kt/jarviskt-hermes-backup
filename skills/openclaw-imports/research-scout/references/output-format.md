# Research Scout Output Format Reference

The canonical format for `~/.hermes/memories/research-YYYY-MM-DD.md`.

## Recommended Format (Evening Scout — 3 items)

```markdown
# Research Scout — YYYY-MM-DD

## 1. [HEADLINE]

**Source:** [Publication] / **Date:** [Relative date]

[2–3 sentence summary: what happened, key facts, context.]

Key angle: [One sentence on why this matters or where it's heading.]

**Tags:** #category #subcategory

---

## 2. [HEADLINE]
...
```

- **3 items** for evening/quick scouts; 5 items for morning/full-day research
- Each item: headline + source/date + prose summary + one-line significance + tags
- Horizontal rules (`---`) separate items
- Tags (e.g. `#AI #policy #infrastructure`) at bottom of each item for searchability
- Links are optional — include when article URL is stable and accessible

## Full Format (Major Developments — 5 items)

Adds a "Why it matters" block and source list footer:

```markdown
# Evening Research Scout — FULL DATE

## 1. [HEADLINE]
**Source:** [Publication], [Date]  
**Link:** [URL]

[Paragraph summary — what happened, key facts.]

**Why it matters:** [One sentence on significance / implications.]

---

*Scout time: [HH:MM] [TZ] | Sources: [comma-separated sources]*
```

## What to Capture vs. Skip

- **Capture:** genuine new capabilities, policy/regulatory developments, significant product announcements, surprising misuse cases, notable failures
- **Skip:** routine earnings, incremental updates, speculation without sources, duplicate stories already in long-term-memory
- Quality over quantity — if nothing significant found, write a brief note and date it
- **Avoid:** over-formatting with bullet lists inside items — prose paragraphs only

## Browser-Based Research Priority Order

1. **Ars Technica AI section** (`https://arstechnica.com/ai/`) — reliably accessible, good AI coverage
2. **TechCrunch AI section** (`https://techcrunch.com/category/artificial-intelligence/`) — strong venture/product angle
3. **Google News with `when:1d` filter** (`https://news.google.com/search?q=QUERY+when:1d`) — real-time, blocks less than google.com search
4. **HN Algolia API** — good for technical/developer-facing stories (use `execute_code` with urllib, not `terminal curl | python3`)
5. **RSS feeds** via `urllib.request` — TechCrunch RSS worked; Ars Technica feed also accessible

## Notes

- Script deduplicates by URL — same link won't appear twice in long-term-memory.md
- Skips results with no URL or with clickbait-style titles (heuristic filter)
- Max 5 results per topic per run to avoid log bloat