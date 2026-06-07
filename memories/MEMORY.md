# Memory — Hermes Operations

## User (Master KT)
- **Timezone:** GMT+8
- **Name:** Wis (formerly Jarvis, since ~2026-04)
- **Speaks:** English only
- **Platforms:** CLI (primary), WhatsApp (2 groups), likely Telegram
- **Style:** outcome-only — no steps, no tool output, no process. Just the result. If uncertain, state plainly and ask.
- **Group chats:** stay silent unless @mentioned or name "Wis" is used
- **WhatsApp groups:** 120363423080731840 (stocks), 120363145668140275 (unknown), 120363408633392803 (unknown) — all free_response mode
- **Short factual questions:** answer directly, no explanation of how

## Environment
- **Hermes home:** `~/.hermes/` — config.yaml, SOUL.md, sessions/, memories/, skills/, cron/
- **Agent codebase:** `~/.hermes/hermes-agent/` (git checkout)
- **Skills:** `~/.hermes/skills/` (user), `~/.hermes/hermes-agent/skills/` (built-in)
- **Memory:** `~/.hermes/memories/MEMORY.md` + daily logs
- **Logs:** `~/.hermes/logs/` — agent.log, gateway.log, errors.log
- **Sessions DB:** `~/.hermes/state.db` (SQLite FTS5)

## Conventions
- Session files: `session_YYYYMMDD_HHMMSS_*.json` or `session_cron_HASH_*.json`
- Cron output: `~/.hermes/cron/output/<job_id>/<timestamp>.md`
- Skill format: `SKILL.md` + YAML frontmatter
- Stuck gaps: document in `~/.hermes/memories/YYYY-MM-DD.md` under `## 🔧 Stuck & Learned`

## Skill Locations (non-obvious)
- `openclaw/openclaw-stock-analysis-victor-framework` is ARCHIVED — its content was absorbed into `openclaw/stock-analysis-victor-framework` (canonical: Victor Entry Signals + Stock Radar + Weekly Victor Study)
- Active openclaw skills live in `~/.hermes/skills/openclaw/<skill-name>/` subdirectories
- gbrain MCP server (3 skills: gbrain-brain-ops, gbrain-enrich, gbrain-signal-detector) — disconnected since OpenClaw migration. See `openclaw/openclaw-imports/references/gbrain-mcp-setup.md` for reconnection steps.

## Active Cron Workflows
- **research-scout:** Nightly AI/tech/news scout → `research-YYYY-MM-DD.md`
- **stock-radar:** Daily stock analysis via Victor framework → `stock-radar-YYYY-MM-DD.md`
- **victor-study:** Weekly sector deep-dives → `victor-study-YYYY-MM-DD.md`
- **war-news:** Daily conflict news → `war-news-YYYY-MM-DD.md`
- **hermes-self-improve-2am:** Auto-review of SOUL.md, config.yaml, skills for outdated info
- **hermes-backup-daily:** Daily backup of memories and config

## Recent Key Events
- **2026-06-07:** Memory consolidation run — sessions auto_prune=false (needs manual cleanup or config change). 3 stale session files identified (>7 days, from May 30): session_cron_72fa7cab90b2, session_cron_c5eefc0f6d98, session_cron_cc617d7fd4df. Memory files all within 7 days (oldest: May 31). SOUL.md and config.yaml reviewed — no updates needed.
- **2026-06-06:** Memory consolidation run — pruned sessions and memories older than 7 days. USER.md restored after accidental deletion.
- **AVGO Q2 FY2026 earnings June 3:** Stock +11.1% June 2 on AI data center/edge network platform announcements. Analysts focused on custom ASIC (XPU) demand from hyperscalers. PT range $1,100–$1,800.
- **PANW Q1 FY2026 earnings June 2:** NATO partnership announced; BTIG Bullish initiation PT $216; GlobalProtect VPN CVE-2026-0257 auth bypass under active exploit (patched).
- **MSFT Build 2026 (June 2):** 7 major AI announcements — first advanced reasoning AI model, Project Solara (OS for AI agents), Execution Containers (security layer for AI agents on Windows).
- **GOOGL:** Gemini Spark (agentic AI assistant) launching; Gemini 3 intensifying compute race; Apple/Samsung partnership rumored for Gemini powering Siri/iPhone AI.

## Victor Framework (Stock Investing)
- **Entry signal:** Current P/E < 90% of 5Y Avg P/E — OR — Current PEG < 90% of 5Y Avg PEG
- **Strong entry:** Both conditions met
- **PEG < 1:** Peter Lynch standalone bargain signal
- **CSP RED day:** VIX > 30 OR S&P drops > 1%
- **Key tickers:** NVDA, MSFT, GOOGL, META, AMZN, AAPL, TSLA, SHOP, BABA, PDD, SOXQ, AIQ

## Known Fixes
- SOUL.md path ref fixed: `memory/` → `~/.hermes/memories/` (2026-05-26)
- User follows AI agent/voice AI content on Instagram (OpenClaw, Grok, prompt engineering)
