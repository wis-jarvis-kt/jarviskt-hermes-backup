# Memory — Hermes Operations

## User (Master KT)
- **Timezone:** GMT+8
- **Name:** Wis (formerly Jarvis, since ~2026-04)
- **Speaks:** English only
- **Platforms:** CLI (primary), WhatsApp (2 groups), likely Telegram
- **Style:** outcome-only — no steps, no tool output, no process. Just the result. If uncertain, state plainly and ask.
- **Group chats:** stay silent unless @mentioned or name "Wis" is used
- **WhatsApp groups:** 120363423080731840 (stocks), 120363145668140275 (unknown) — both free_response mode
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

## Active Cron Workflows
- **research-scout:** Nightly AI/tech/news scout → `research-YYYY-MM-DD.md`
- **stock-radar:** Daily stock analysis via Victor framework → `stock-radar-YYYY-MM-DD.md`
- **victor-study:** Weekly sector deep-dives → `victor-study-YYYY-MM-DD.md`
- **war-news:** Daily conflict news → `war-news-YYYY-MM-DD.md`

## Victor Framework (Stock Investing)
- **Entry signal:** Current P/E < 90% of 5Y Avg P/E — OR — Current PEG < 90% of 5Y Avg PEG
- **Strong entry:** Both conditions met
- **PEG < 1:** Peter Lynch standalone bargain signal
- **CSP RED day:** VIX > 30 OR S&P drops > 1%
- **Key tickers:** NVDA, MSFT, GOOGL, META, AMZN, AAPL, TSLA, SHOP, BABA, PDD, SOXQ, AIQ

## Known Fixes
- SOUL.md path ref fixed: `memory/` → `~/.hermes/memories/` (2026-05-26)
- User follows AI agent/voice AI content on Instagram (OpenClaw, Grok, prompt engineering)
