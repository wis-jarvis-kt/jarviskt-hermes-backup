# consolidate-memory

**Purpose:** Consolidate recent conversation logs and daily memory files into structured, searchable memory files. Keeps short-term context rolling and promotes important facts to long-term storage.

**Trigger phrases:** "consolidate memory", "update memory", "memory housekeeping"  
**Also runs:** nightly cron (suggested: 02:00 local)

---

## Memory File Structure

| File | Purpose | Retention |
|------|---------|-----------|
| `memory/recent-memory.md` | Rolling 48hr log of events, decisions, facts | Auto-pruned after 48hrs |
| `memory/long-term-memory.md` | Distilled facts, confirmed patterns, important context | Permanent (manual curation) |
| `memory/project-memory.md` | Active project states, open tasks, blockers | Updated per project activity |

---

## How to Run

```bash
# Dry run — show what would change, don't write
python3 /Users/ktoclaw/.openclaw/workspace/scripts/consolidate_memory.py --dry-run

# Full consolidation (prune recent, promote to long-term)
python3 /Users/ktoclaw/.openclaw/workspace/scripts/consolidate_memory.py

# Promote specific item from recent to long-term manually:
# Edit recent-memory.md, prefix the line with [PROMOTE] then re-run
python3 /Users/ktoclaw/.openclaw/workspace/scripts/consolidate_memory.py --promote-flagged
```

---

## Steps (what the script does)

1. **Read** all `memory/YYYY-MM-DD.md` daily files from the last 48 hours
2. **Parse** entries for facts, decisions, and project updates
3. **Append** new entries to `recent-memory.md` (deduplicated)
4. **Prune** `recent-memory.md` entries older than 48 hours
5. **Promote** items flagged `[PROMOTE]` or scoring high relevance → `long-term-memory.md`
6. **Update** `project-memory.md` with any project-related context found
7. **Print** a summary: N added, N pruned, N promoted

---

## recent-memory.md Format

```markdown
## [2026-03-24 08:30 GMT+8]
- KT asked about Instagram extractors → working approach: instaloader via python3 -c
- Deployed 3 new skills: consolidate-memory, research-scout, instagram-extractor
```

## long-term-memory.md Format

```markdown
## facts
- KT prefers concise bullet responses on WhatsApp
- instaloader works for public Instagram posts (single + carousel)

## new_learnings
<!-- research-scout appends here -->
- [2026-03-24] Claude Code 4 supports extended thinking | https://... | Significant context window bump

## patterns
- HLA portal uses Playwright; always login fresh per session
```

## project-memory.md Format

```markdown
## active_projects
### HLA Annual Statements
- Status: complete for 2025 season
- Script: hla_annual_stmt_correct.py
- Last run: 2026-03-20

### Skills Development
- Status: active
- Notes: 4 new skills added 2026-03-24
```

---

## Notes

- Script is safe to re-run multiple times (idempotent for deduplication)
- Does NOT delete daily `YYYY-MM-DD.md` files — those are raw logs
- `[PROMOTE]` flag can be added manually to any `recent-memory.md` entry
- If `long-term-memory.md` doesn't exist, script creates it with correct headings
