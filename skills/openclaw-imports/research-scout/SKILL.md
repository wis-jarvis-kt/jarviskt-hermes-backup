---
name: research-scout
description: Nightly web scout for AI, Claude Code, OpenClaw, and workflow automation developments. Logs findings to memory files.
tags: []
trigger_phrases:
  - research scout
  - check for updates
  - scout new AI stuff
  - what's new in Claude
  - run research scout
---

# research-scout

**Purpose:** Nightly web scout that finds new AI, Claude Code, OpenClaw, and workflow automation updates — then logs them to `~/.hermes/memories/research-YYYY-MM-DD.md` (class-level findings) and `long-term-memory.md` under `## new_learnings` (per-topic findings). Keeps your knowledge base fresh without manual browsing.

**Trigger phrases:** "research scout", "check for updates", "scout new AI stuff", "what's new in Claude", "run research scout"  
**Also runs:** nightly cron (configured via Hermes cronjob, not crontab)

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

## Output Targets

**Daily memory file** (primary for cron jobs):  
`~/.hermes/memories/research-YYYY-MM-DD.md` — 3–5 curated findings with source, points, and summary. Format:

```markdown
### 1. Local Video Indexing with Gemma4-31B on MacBook
- **Title:** Indexing a year of video locally on a 2021 MacBook with Gemma4-31B (50GB swap)
- **Summary:** ...one line description...
- **Source:** HN / simbastack.com | 236 pts
- **URL:** https://...
```

**Long-term memory** (secondary, for deduplicated per-topic tracking):  
`~/.openclaw/workspace/memory/long-term-memory.md` under `## new_learnings` — URL-deduped entries from research_scout.py runs.

---

## Sources

- **Brave Search API** (requires `BRAVE_API_KEY` env var; falls back to HN-only if unset)
- **Hacker News Algolia API** — `https://hn.algolia.com/api/v1/search?query=TOPIC&tags=story&hitsPerPage=5`
- **Reddit** — `https://www.reddit.com/search.json?q=TOPIC&sort=new&limit=5&type=link`

**Finding AI/Tech stories from HN front page** (when doing manual scout):

```python
import urllib.request, json, ssl
url = 'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50'
req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-Scout/1.0'})
ctx = ssl.create_default_context()
with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
    data = json.loads(r.read().decode())
# Filter AI-relevant stories
ai_kw = ['ai','llm','model','gpt','claude','gemini','anthropic','openai','neural','agent','gemma','deepseek','mistral']
for h in data.get('hits', []):
    title = h.get('title','').lower()
    if any(k in title for k in ai_kw):
        print(h.get('title'), h.get('points'), 'pts')
```

---

## Notes

- Script deduplicates by URL — same link won't appear twice
- Skips results with no URL or with clickbait-style titles (heuristic filter)
- Max 5 results per topic per run to avoid log bloat
- When run as cron job, save findings to `~/.hermes/memories/research-YYYY-MM-DD.md` — the script itself writes to long-term-memory.md via the `## new_learnings` mechanism