# HEARTBEAT.md

## 🔧 Self-Improvement Trigger (SELF_IMPROVE_NIGHTLY)
When you receive the system event `SELF_IMPROVE_NIGHTLY`, follow these steps exactly:

1. **Backup first** — copy SOUL.md, AGENTS.md, TOOLS.md, HEARTBEAT.md, MEMORY.md, IDENTITY.md to `workspace/self-improve-backups/[YYYYMMDD-HHMMSS]/`
2. **Review each file** — look for: outdated tasks, stale references, clarity gaps, missing or conflicting rules
3. **Improve surgically** — small targeted edits only; do NOT rewrite unnecessarily; never alter KT's personal info
4. **Log changes** — append a `## 🔧 Self-Improvement Run` section to today's `memory/YYYY-MM-DD.md`
5. **Report to Master KT** — send WhatsApp to +60125226892 with: what changed, backup path, how to revert
6. **Prune backups** — keep last 14 days only

If no improvements needed: send brief "nothing needed" report to Master KT.

---

## Tasks

### 1. Check jarvisktgoo@gmail.com inbox
- Run: `gog gmail search 'in:inbox newer_than:1d' --account jarvisktgoo@gmail.com --max 10 --json`
- Summarize any new/unread emails
- Report to KT on WhatsApp with:
  - Sender, subject, brief summary
  - Options: Reply / Forward / Delete / Archive / Ignore
- Wait for KT's instruction before acting

### 2. Monitor GitHub backup size + Disk Space
- Check daily backup notifications for file size
- **Alert Master KT immediately** when backup size approaches 80–90 MB
- Hard limit is 100 MB per file — alert before it gets there
- Fresh reference: 56.1 MB on 2026-04-06 (`7d2d51ff-b2cb-4845-b015-8995f8b712c0.jsonl`)
- **Disk space: alert if data volume free space drops below 50GB**
  - Run: `df -g /System/Volumes/Data | awk 'NR==2 {print $4}'`
  - If <60GB: send WhatsApp alert immediately with free GB amount
  - Include disk space check in nightly SELF_IMPROVE_NIGHTLY report

### 3. Webinar Conversion Brain integrity check (weekly, Mondays)
- Verify expert-panel folder exists: `/Users/ktoclaw/.openclaw/workspace/expert-panel/`
- Check BRAIN.md exists and is non-empty
- Check VERSION.md exists
- Count expert files in `experts/` — should be 7 unique files (VERSION.md may still mention 8 because expert #6 and #7 map to the same file — known typo)
- If fewer than 7: alert KT immediately with: "⚠️ Webinar Conversion Brain integrity issue — [what's missing]"
- If all good: no need to report (stay HEARTBEAT_OK)

### 4. WAHA WhatsApp Session Health Check
- Run: `curl -s "http://localhost:3000/api/sessions/default" -H "X-Api-Key: c838c39d3a9d4d40ac151f6a0f7372f1"`
- Check `status` field — must be `WORKING`
- If status is `STOPPED` or any other non-WORKING state:
  1. Restart: `curl -s -X POST "http://localhost:3000/api/sessions/start" -H "X-Api-Key: c838c39d3a9d4d40ac151f6a0f7372f1" -H "Content-Type: application/json" -d '{"session": "default", "name": "default"}'`
  2. Wait 10 seconds
  3. Verify: re-check the session status
  4. If still not WORKING after 30s: alert Master KT on WhatsApp with "⚠️ WAHA session DOWN — manual intervention needed"
- If WORKING: no action needed (stay HEARTBEAT_OK)
- This runs on every heartbeat (~30 min) to ensure reminders keep firing

### State tracking
- Track last checked time in memory/heartbeat-state.json
- Only report emails not previously reported
- Skip if no new emails (stay HEARTBEAT_OK)

### 5. ~~Google OAuth Auto-Refresh~~ (REMOVED — no such command in gog)
- ~~`gog auth refresh`~~ does not exist in gog CLI. Token refresh cannot be automated.
- **Permanent fix:** Publish the "Jarvis Access" OAuth app in Google Cloud Console (OAuth consent screen → Publish App). Refresh tokens will then last months/years instead of 7 days.
- See OpenClaw docs or Google Cloud OAuth documentation for the publishing steps.

### 7. Stock Radar
- Cron 7143f102 runs at 9:45pm MYT every weekday (Mon-Fri)
- Runs TWO tasks back-to-back:
  **Task 1 - Stock Radar Check:** AAPL, NVDA, META, GOOGL, MSFT, TSLA
    - Victor's Masterclass framework: PEG vs 5Y avg, P/E vs 5Y avg, quality score
    - RED/BIG RED day classification from S&P500 + tech stock moves
    - Per stock verdict: Buy / Conditional Buy / Wait / Skip
    - Morningstar links
  **Task 2 - ETF Sell PUT Analysis:** AIQ, TDIV, PSI, SOXQ, IETC, SCHG, DYNF, CGGR, SPHQ, XLG, USMC, SNPE, TMFC, FLQL, SPYM, FNDX, FDVV, WTV
    - Victor's CSP rules: RED day check → ETF price/% change → IV estimate → Volume → SELL PUT or WAIT
    - Cash reminder: USD $500/contract
- Both results sent to: 120363423080731840@g.us via message tool
- Delivery mode: not-requested (cron uses message tool directly)
- Format: WhatsApp-friendly, bullet points, bold tickers, no tables

### 8. Beautify photo for Master KT (BLOCKED — awaiting KT confirmation)
