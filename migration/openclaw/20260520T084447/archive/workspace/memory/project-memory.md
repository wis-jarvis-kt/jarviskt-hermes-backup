# project-memory.md
_Active projects, states, and blockers._

## active_projects

## completed_projects


### Noted [2026-03-24 08:40 GMT+8]
- Master KT added me to "Conversion Codex Chatbot" group (later renamed "Conversion Codex Project")
- Demo 2: Roofing company — upload photo → finds similar past projects with match %
- Build steps: Drop files in /data → Claude Code builds ingestion + chat UI automatically
- Key insight: Skill = clear communication + deep process understanding, not coding

### Noted [2026-03-25 03:30 GMT+8]
- AOAI transcripts Days 1-4
- EMC preview transcription (KT's own webinar style)
- Was on free tier — KT linked billing account "GOO KAH THART - Jarvis" to Jarvis Project
- Location: `scripts/webinar_analyzer.py`
- Video split script: uses ffmpeg to split large videos into 800MB chunks
- `skills/consolidate-memory/` — nightly memory consolidation
- `skills/research-scout/` — nightly web research + new_learnings section
- `skills/instagram-extractor/` — uses instaloader to extract carousel posts without login
- `DWOHj6-jesF` — .claude folder setup (10 slides): agents, commands, hooks, rules, skills, settings.json, CLAUDE.md

### Noted [2026-03-26 03:30 GMT+8]
- **Frontend/Backend:** Next.js 16 + React 19 + Supabase + Tailwind 4 + TypeScript
- **Transcription:** AssemblyAI / Whisper
- SAME Supabase project — Phase 2 adds new tables, does NOT modify Phase 1 files
- GitHub OAuth (wis-jarvis-kt) — not the account that owns the Supabase project
- Vercel/edge function deploy — requires Supabase PAT
- KT asked to provide it in Conversion Codex Project WhatsApp group
- Missing: `advanced-conversion.md` (VERSION.md entries #6 and #7 both point to self-referential-pain.md — likely a copy-paste error during initial build)

### Noted [2026-03-27 03:30 GMT+8]
- No major project updates or decisions in this session

### Noted [2026-03-30 03:30 GMT+8]
- Added exception: scheduled cron tasks (e.g. SELF_IMPROVE_NIGHTLY at 2AM) always run regardless of quiet hours

### Noted [2026-03-31 03:30 GMT+8]
- Added exception: scheduled cron tasks (e.g. SELF_IMPROVE_NIGHTLY at 2AM) always run regardless of quiet hours
- **HEARTBEAT.md** — Task 4 still blocked (billing), no changes needed

### Noted [2026-03-31 03:30 GMT+8]
- Added exception: scheduled cron tasks (e.g. SELF_IMPROVE_NIGHTLY at 2AM) always run regardless of quiet hours
- **HEARTBEAT.md** — Task 4 still blocked (billing), no changes needed

### Noted [2026-04-01 03:30 GMT+8]
- **HEARTBEAT.md** — Task 4 still blocked (billing), no changes needed
- **HEARTBEAT.md** — Task 4 still blocked (billing), no changes needed
- Cause: `--prod` flag created new deployment URL but alias `conversion-codex-dashboard.vercel.app` still pointed at old build
- Fix: Manually re-pointed alias to correct deployment
- Cause: Supabase edge functions terminate as soon as the outer function returns — background tasks are killed
- Populate brain_content table with actual conversion scripts
- Updated "Current Projects" date from 2026-03-31 → 2026-04-01

### Noted [2026-04-01 03:30 GMT+8]
- **HEARTBEAT.md** — Task 4 still blocked (billing), no changes needed
- **HEARTBEAT.md** — Task 4 still blocked (billing), no changes needed
- Cause: `--prod` flag created new deployment URL but alias `conversion-codex-dashboard.vercel.app` still pointed at old build
- Fix: Manually re-pointed alias to correct deployment
- Cause: Supabase edge functions terminate as soon as the outer function returns — background tasks are killed
- Populate brain_content table with actual conversion scripts
- Updated "Current Projects" date from 2026-03-31 → 2026-04-01

### Noted [2026-04-02 03:30 GMT+8]
- Updated "Current Projects" date from 2026-03-31 → 2026-04-01
- Published "Jarvis Access" OAuth app to Production in Google Cloud Console (project: jarvis-access-488903)
- Task 4 (photo beautify): updated status — removed stale "billing email" root cause (billing was fixed 2026-03-24), simplified to "wait for KT explicit confirmation"

### Noted [2026-04-03 03:30 GMT+8]
- Task 4 (photo beautify): updated status — removed stale "billing email" root cause (billing was fixed 2026-03-24), simplified to "wait for KT explicit confirmation"
- Task 4 (photo beautify): updated status — removed stale "billing email" root cause (billing was fixed 2026-03-24), simplified to "wait for KT explicit confirmation"
- Surrender Value: **RM 36,474.46** (projected)
- Surrender Value: **RM 61,683.45** (projected)
- `buildSystemPrompt` rewritten to use actual brain content (not placeholder)
- WhatsApp section: Replaced incorrect "creds.json corruption" description with correct rule — 499 = normal keep-alive restart, do NOT alert KT. Only alert if gateway fails to reconnect >5 min.
- Current Projects: Updated Conversion Codex status to reflect CCS Brain integration complete (2026-04-02)
- 2026-04-01 entry: Cleaned up WhatsApp 499 description to reflect corrected understanding

### Noted [2026-04-04 03:30 GMT+8]
- WhatsApp section: Replaced incorrect "creds.json corruption" description with correct rule — 499 = normal keep-alive restart, do NOT alert KT. Only alert if gateway fails to reconnect >5 min.
- Current Projects: Updated Conversion Codex status to reflect CCS Brain integration complete (2026-04-02)
- 2026-04-01 entry: Cleaned up WhatsApp 499 description to reflect corrected understanding
- HEARTBEAT.md — Minor: Task 2 backup size figure noted as potentially stale (last known 2026-03-16).

### Noted [2026-04-04 03:34 GMT+8]
- WhatsApp section: Replaced incorrect "creds.json corruption" description with correct rule — 499 = normal keep-alive restart, do NOT alert KT. Only alert if gateway fails to reconnect >5 min.
- Current Projects: Updated Conversion Codex status to reflect CCS Brain integration complete (2026-04-02)
- 2026-04-01 entry: Cleaned up WhatsApp 499 description to reflect corrected understanding
- HEARTBEAT.md — Minor: Task 2 backup size figure noted as potentially stale (last known 2026-03-16).

### Noted [2026-04-05 03:30 GMT+8]
- HEARTBEAT.md — Minor: Task 2 backup size figure noted as potentially stale (last known 2026-03-16).

### Noted [2026-04-06 03:30 GMT+8]
- Change made: Removed stale `~55.7 MB as of 2026-03-16` anchor from HEARTBEAT.md GitHub backup-size task and replaced it with a freshness rule to avoid outdated alerts.

### Noted [2026-04-06 03:30 GMT+8]
- Change made: Removed stale `~55.7 MB as of 2026-03-16` anchor from HEARTBEAT.md GitHub backup-size task and replaced it with a freshness rule to avoid outdated alerts.

### Noted [2026-04-15 03:30 GMT+8]
- Trigger: Nightly cron backup completed (01:00:22), heartbeat fired
- MEMORY.md was 30KB (target: <20KB). Removed stale: Apple ID recovery (resolved), Hume AI free-credit trivia. Updated project timestamp.

### Noted [2026-04-15 03:30 GMT+8]
- Trigger: Nightly cron backup completed (01:00:22), heartbeat fired
- MEMORY.md was 30KB (target: <20KB). Removed stale: Apple ID recovery (resolved), Hume AI free-credit trivia. Updated project timestamp.

### Noted [2026-04-16 03:30 GMT+8]
- Trigger: Nightly cron backup completed (01:00:22), heartbeat fired
- MEMORY.md was 30KB (target: <20KB). Removed stale: Apple ID recovery (resolved), Hume AI free-credit trivia. Updated project timestamp.
- Deal Hunter Skill, Itinerary Builder, Models configured, Webinar Brain Updates, New Tools/APIs, Google Security, Skills Built → consolidated into "Archived Reference Notes" section
- Japan Trip Planning, Smart Home, Conversion Codex Project Group, Gemini Embedding → condensed to brief notes
- Conversion Codex Full Project Map (56 lines) → compressed to 9-line summary
- Removed "Archived Reference Notes" section (10 lines — pointers to skills/docs, not critical for session bootstrap)

### Noted [2026-04-16 03:30 GMT+8]
- Trigger: Nightly cron backup completed (01:00:22), heartbeat fired
- MEMORY.md was 30KB (target: <20KB). Removed stale: Apple ID recovery (resolved), Hume AI free-credit trivia. Updated project timestamp.
- Deal Hunter Skill, Itinerary Builder, Models configured, Webinar Brain Updates, New Tools/APIs, Google Security, Skills Built → consolidated into "Archived Reference Notes" section
- Japan Trip Planning, Smart Home, Conversion Codex Project Group, Gemini Embedding → condensed to brief notes
- Conversion Codex Full Project Map (56 lines) → compressed to 9-line summary
- Removed "Archived Reference Notes" section (10 lines — pointers to skills/docs, not critical for session bootstrap)

### Noted [2026-04-17 03:30 GMT+8]
- Removed "Archived Reference Notes" section (10 lines — pointers to skills/docs, not critical for session bootstrap)

### Noted [2026-04-17 03:33 GMT+8]
- Removed "Archived Reference Notes" section (10 lines — pointers to skills/docs, not critical for session bootstrap)

### Noted [2026-04-18 03:30 GMT+8]
- OAUTH_REFRESH_DAILY cron job (35081fea) **deleted** — was useless
- HEARTBEAT.md Task 5 updated to show it's non-functional with strikethrough note

### Noted [2026-04-18 03:32 GMT+8]
- OAUTH_REFRESH_DAILY cron job (35081fea) **deleted** — was useless
- HEARTBEAT.md Task 5 updated to show it's non-functional with strikethrough note

### Noted [2026-04-25 03:30 GMT+8]
- WhatsApp notification to Master KT: **FAILED** (no HTTP API available in this cron context; WhatsApp is WebSocket-gateway only, no direct send endpoint accessible from exec context)

### Noted [2026-04-25 03:33 GMT+8]
- WhatsApp notification to Master KT: **FAILED** (no HTTP API available in this cron context; WhatsApp is WebSocket-gateway only, no direct send endpoint accessible from exec context)

### Noted [2026-04-27 03:30 GMT+8]
- No new tasks, rules, or system changes this session
- HEARTBEAT.md task 6 (beautify photo) remains BLOCKED — awaiting Master KT's "try again"

### Noted [2026-04-29 03:30 GMT+8]
- No stale tasks, no broken links, no gaps found

### Noted [2026-04-29 03:32 GMT+8]
- No stale tasks, no broken links, no gaps found

### Noted [2026-04-30 03:30 GMT+8]
- Script: `~/.openclaw/reminders/wa_reminder.py`

### Noted [2026-04-30 03:36 GMT+8]
- Script: `~/.openclaw/reminders/wa_reminder.py`

### Noted [2026-05-01 03:32 GMT+8]
- New: WAHA HTTP API via cron (send_reminder.py + macOS crontab)

### Noted [2026-05-02 03:30 GMT+8]
- New: WAHA HTTP API via cron (send_reminder.py + macOS crontab)

### Noted [2026-05-15 03:31 GMT+8]
- Cron job: `0 22 * * 1-5` → writes trigger file → Wis heartbeat picks up → runs analysis → sends to stock group
- Script: `~/.openclaw/etf_analysis_cron.py`

### Noted [2026-05-20 03:30 GMT+8]
- Cron job 7143f102 updated to include Tesla in 9:45pm daily stock radar check
- ETF Sell PUT analysis still runs as Task 2 in same cron job
