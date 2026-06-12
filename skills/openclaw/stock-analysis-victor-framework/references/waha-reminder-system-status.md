# WAHA Reminder System — DEPRECATED (2026-06-12)

## Status: REMOVED

WAHA reminder system has been fully removed from the setup.

## What was removed
- `~/.openclaw/send_reminder.py` — deleted, replaced with dummy `exit(0)` stub
- `~/.openclaw/waha_reminder.log` — deleted
- `~/.openclaw/reminders_db.json` — cleared of all WAHA entries (71 entries removed)
- Cron entry `* * * * * /usr/bin/python3 ~/.openclaw/send_reminder.py` — crontab entry exists but script now does nothing (safe stub)
- All WAHA references removed from TOOLS.md, MEMORY.md, HEARTBEAT.md

## Current WhatsApp setup
Hermes Agent handles WhatsApp natively via its own bridge:
- Bridge: `~/.hermes/hermes-agent/scripts/whatsapp-bridge/bridge.js --port 3000 --session ~/.hermes/whatsapp/session --mode bot`
- Session state: `~/.hermes/whatsapp/session/`
- Logs: `~/.hermes/whatsapp/bridge.log`

## Replacement
Reminder functionality is handled by Hermes cron jobs:
- `hermes-victor-6pm` (4eee4adab1e8) — weekdays 6pm → **Master KT's DM** (`56702359580792@lid`) — corrected 2026-06-12
- `hermes-stock-radar-945pm` (505bb59fcf82) — weekdays 9:45pm → stocks group

**Delivery fix (2026-06-12):** Prior to today, `hermes-victor-6pm` was delivering to the stocks group instead of Master KT's DM. This was a side effect of the WAHA decommissioning. The cron deliver target has been updated to `whatsapp:56702359580792@lid`. Always use LID format for DM delivery to WhatsApp.

To set interview reminders: use the Remind skill which leverages Hermes's built-in messaging.