# Research Scout Output Format Reference

The canonical format for `~/.hermes/memories/research-YYYY-MM-DD.md` as established 2026-05-23.

## File Structure

```markdown
# Evening Research Scout — [FULL DATE]

## 1. [HEADLINE]
**Source:** [Publication], [Date]  
**Link:** [URL]

[Paragraph summary — what happened, key facts.]

**Why it matters:** [One sentence on significance / implications.]

---

## 2. [HEADLINE]
...

---
*Scout time: [HH:MM] [TZ] | Sources: [comma-separated sources]*
```

## Rules
- 3 items per scout (evening) or 5 items (morning/full-day)
- Each item: headline + source + link + what happened + why it matters
- Separate items with `---` (horizontal rule)
- Close with scout time + source list
- No bullet lists inside items — prose paragraphs only
- Links are optional but preferred; use when article URL is stable

## What to Capture vs. Skip
- Capture: genuine new capabilities, policy/regulatory developments, significant product announcements, surprising misuse cases
- Skip: routine company earnings, incremental product updates, speculation without sources
- Quality over quantity — if nothing significant found, write a brief note and date it

## Skills to Check Before Running
- `web-research-limitations` — for known anti-bot pitfalls per platform
- `blogwatcher` — for RSS-based sources that bypass browser blocking