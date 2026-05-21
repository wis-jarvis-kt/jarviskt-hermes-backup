# research-scout

**Purpose:** Nightly web scout that finds new AI, Claude Code, OpenClaw, and workflow automation updates — then logs them to `long-term-memory.md` under `## new_learnings`. Keeps your knowledge base fresh without manual browsing.

**Trigger phrases:** "research scout", "check for updates", "scout new AI stuff", "what's new in Claude"  
**Also runs:** nightly cron (suggested: 03:00 local)

---

## How to Run

```bash
# Default topics (Claude Code, OpenClaw, AI agents, workflow automation)
python3 /Users/ktoclaw/.openclaw/workspace/scripts/research_scout.py

# Custom topics
python3 /Users/ktoclaw/.openclaw/workspace/scripts/research_scout.py "Claude 4" "MCP tools" "LangGraph"

# Dry run — print findings without writing to memory
python3 /Users/ktoclaw/.openclaw/workspace/scripts/research_scout.py --dry-run

# Promote staged new_learnings to confirmed patterns (run weekly)
python3 /Users/ktoclaw/.openclaw/workspace/scripts/research_scout.py --promote
```

---

## Sources

- **Brave Search API** (via OpenClaw `web_search` tool or direct API call)
- **Hacker News** — `https://hn.algolia.com/api/v1/search?query=TOPIC&tags=story&hitsPerPage=5`
- **Reddit** — `https://www.reddit.com/search.json?q=TOPIC&sort=new&limit=5`

---

## Output Format (appended to long-term-memory.md)

```markdown
## new_learnings

<!-- scout:2026-03-24T03:00:00+08:00 -->
- [2026-03-24] Claude Code adds persistent memory hooks | https://anthropic.com/... | New feature for session continuity
- [2026-03-24] OpenClaw 2.3 skill hot-reload | https://clawhub.com/... | Skills reload without gateway restart
- [2026-03-24] MCP sampling now stable | https://news.ycombinator.com/... | HN discussion on MCP protocol maturity
```

---

## Weekly Promotion (--promote flag)

Moves entries from `## new_learnings` that are >7 days old into `## patterns` or `## facts` in `long-term-memory.md`, then clears the staging area.

```markdown
## patterns
- Claude Code works best with explicit file context (learned from multiple sessions)

## facts  
- MCP sampling is now stable as of 2026-03 (confirmed via HN + official docs)
```

---

## Cron Setup (suggested)

```bash
# Edit crontab:  crontab -e
# 3AM nightly research scout
0 3 * * * /usr/bin/python3 /Users/ktoclaw/.openclaw/workspace/scripts/research_scout.py >> /Users/ktoclaw/.openclaw/workspace/memory/scout.log 2>&1

# Sunday 4AM: promote staged learnings
0 4 * * 0 /usr/bin/python3 /Users/ktoclaw/.openclaw/workspace/scripts/research_scout.py --promote >> /Users/ktoclaw/.openclaw/workspace/memory/scout.log 2>&1
```

---

## Notes

- Script deduplicates by URL — same link won't appear twice
- Skips results with no URL or with clickbait-style titles (heuristic filter)
- Max 5 results per topic per run to avoid log bloat
- Set `BRAVE_API_KEY` env var for web search; falls back to HN-only if unset
