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

**Purpose:** Nightly web scout that finds new AI, Claude Code, OpenClaw, and workflow automation developments — then logs them to `~/.hermes/memories/research-YYYY-MM-DD.md` (curated daily report) and `long-term-memory.md` under `## new_learnings` (URL-deduped per-topic log). Keeps your knowledge base fresh without manual browsing.

**Trigger phrases:** "research scout", "check for updates", "scout new AI stuff", "what's new in Claude", "run research scout", "evening research scout"  
**Also runs:** evening cron job (scheduled daily)

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
`~/.hermes/memories/research-YYYY-MM-DD.md` — 3–5 curated findings with source, points, and summary. See `references/output-format.md` for the canonical format used in this codebase — includes source priority order and browser-based research technique notes.

**Long-term memory** (secondary, for deduplicated per-topic tracking):  
`~/.openclaw/workspace/memory/long-term-memory.md` under `## new_learnings` — URL-deduped entries written automatically by the research_scout.py script.

---

## Sources & Techniques

**Priority order for evening scout (most reliable first):**

1. **Browser: Ars Technica AI section** (`https://arstechnica.com/ai/`) — reliably accessible, good AI/tech policy coverage. Use `browser_navigate` → `browser_snapshot` to read headlines.
2. **Browser: TechCrunch AI section** (`https://techcrunch.com/category/artificial-intelligence/`) — strong venture/product angle. Can also fetch via RSS: `https://techcrunch.com/category/artificial-intelligence/feed/`.
3. **Browser: Google News with `when:1d` filter** (`https://news.google.com/search?q=QUERY+when:1d&hl=en-US&gl=US&ceid=US:en`) — real-time, less bot-blocking than google.com search. Good for breaking stories.
4. **execute_code with urllib** — HN Algolia API (`https://hn.algolia.com/api/v1/search?query=TOPIC&tags=story`) and RSS feeds work well. Use `urllib.request` with Python, not `terminal curl | python3` — the security vet blocks pipe-to-interpreter patterns.

**HN Algolia API — Front Page (high-signal technical stories):**
```python
import urllib.request, json, ssl
url = 'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50'
req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-Scout/1.0'})
ctx = ssl.create_default_context()
with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
    data = json.loads(r.read().decode())
ai_kw = ['ai','llm','model','gpt','claude','gemini','anthropic','openai','neural','agent','gemma','deepseek','mistral']
for h in data.get('hits', []):
    title = h.get('title','').lower()
    if any(k in title for k in ai_kw):
        print(h.get('title'), h.get('points'), 'pts')
```

**HN Algolia API — Topic search:**
`https://hn.algolia.com/api/v1/search?query=TOPIC&tags=story&hitsPerPage=5`

**RSS feeds** — TechCrunch AI RSS worked via urllib. Ars Technica RSS also accessible. Try `urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})`.

**Avoid:** Piping `curl` output directly to `python3` — the security vet blocks this pattern. Use `execute_code` with urllib instead.

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

## ⚠️ Critical: Dual-Output Requirement

The `research_scout.py` script has **two separate output targets** — it does NOT automatically write the daily memory file:

1. **`~/.hermes/memories/research-YYYY-MM-DD.md`** — the daily scout report (primary for cron jobs). **The script does NOT write this.** You must write this file manually after running the script.
2. **`~/.openclaw/workspace/memory/long-term-memory.md` under `## new_learnings`** — URL-deduped per-topic log. Written automatically by the script.

**Cron job workflow (correct):**
```bash
# Step 1: Run scout script (writes to long-term-memory.md only)
python3 /Users/ktoclaw/.openclaw/workspace/scripts/research_scout.py

# Step 2: Manually write the daily memory file
# (use format from references/output-format.md)
```

Do NOT skip Step 2. The cron job deliverable is `~/.hermes/memories/research-YYYY-MM-DD.md`.

## Sources & Techniques

**Preferred: Browser-based Google News with `when:1d` filter (most reliable for fresh news)**
Navigate to:
```
https://news.google.com/search?q=QUERY+when:1d&hl=en-US&gl=US&ceid=US:en
```
Use browser_snapshot to read headlines, click into interesting links for details. The `when:1d` parameter restricts results to the past 24 hours.

**HN Algolia API — Front Page (for high-signal technical stories)**
```python
import urllib.request, json, ssl
url = 'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50'
req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-Scout/1.0'})
ctx = ssl.create_default_context()
with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
    data = json.loads(r.read().decode())
ai_kw = ['ai','llm','model','gpt','claude','gemini','anthropic','openai','neural','agent','gemma','deepseek','mistral']
for h in data.get('hits', []):
    title = h.get('title','').lower()
    if any(k in title for k in ai_kw):
        print(h.get('title'), h.get('points'), 'pts')
```

**HN Algolia API — Topic search**
`https://hn.algolia.com/api/v1/search?query=TOPIC&tags=story&hitsPerPage=5`

**Reddit** — `https://www.reddit.com/search.json?q=TOPIC&sort=new&limit=5&type=link`

**Avoid:** Piping `curl` output directly to `python3` — the security vet blocks this pattern. If you need XML parsing, download to a temp file first, then process separately.

## Notes

- Script deduplicates by URL — same link won't appear twice in long-term-memory.md
- Skips results with no URL or with clickbait-style titles (heuristic filter)
- Max 5 results per topic per run to avoid log bloat