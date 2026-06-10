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
- **2026-06-10:** Memory consolidation — pruned daily logs from June 1–3. Disk Space Watchdog now auto-cleans (every 24h, threshold 50GB).

## Victor Framework (Stock Investing)
- **Entry signal:** Current P/E < 90% of 5Y Avg P/E — OR — Current PEG < 90% of 5Y Avg PEG
- **Strong entry:** Both conditions met
- **PEG < 1:** Peter Lynch standalone bargain signal
- **CSP RED day:** VIX > 30 OR S&P drops > 1%
- **Key tickers:** NVDA, MSFT, GOOGL, META, AMZN, AAPL, TSLA, SHOP, BABA, PDD, SOXQ, AIQ

## Known Fixes
- SOUL.md path ref fixed: `memory/` → `~/.hermes/memories/` (2026-05-26)
- User follows AI agent/voice AI content on Instagram (OpenClaw, Grok, prompt engineering)
§
Disk Space Watchdog (job_id: 99ed63eabd51) — auto-cleanup script at ~/.hermes/scripts/disk_space_watchdog.sh. Runs every 24h (schedule updated from 60m). Threshold: 50GB free. Cleans: old cron output dirs, old session files, old daily memory logs (research/war-news/stock-radar/victor-study), old log files, sleepimage (>1GB). All items older than 7 days. Script bugfix: df -g on macOS puts Available in column 4, not 7.