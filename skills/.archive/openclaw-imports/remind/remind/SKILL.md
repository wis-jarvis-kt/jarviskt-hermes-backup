---
name: remind
description: Send timed WhatsApp reminders to Master KT with zero AI, zero pyautogui.
tags: [whatsapp, reminders, waha, openclaw]
version: 1.2.0
---

# Remind — WhatsApp Reminder Skill

Send timed WhatsApp reminders to Master KT with zero AI, zero pyautogui.

## What it does

- Reads `~/.openclaw/reminders_db.json` for scheduled reminders
- Fires them via WAHA HTTP API every minute via cron
- No OpenClaw gateway involvement in the firing path

## Quick Reference

```bash
# View all reminders
cat ~/.openclaw/reminders_db.json

# View recent logs
tail ~/.openclaw/waha_reminder.log

# Manual test
/usr/bin/python3 ~/.openclaw/send_reminder.py
```

## Add a New Reminder

Tell Wis to add a reminder. Wis edits `reminders_db.json` with:
- `message` — what to send
- `to` — phone number (default: +60125226892)
- `schedule.kind` — `daily`, `weekdays`, or `once`
- `schedule.time` — 24h format e.g. `"21:45"`
- `schedule.due_date` / `schedule.due_time` — for `once` type

Example entry:
```json
{
  "message": "Stock radar check - is today a buy day?",
  "to": "+60125226892",
  "schedule": {
    "kind": "weekdays",
    "time": "21:45"
  }
}
```

## Architecture

| Component | Purpose |
|-----------|---------|
| `~/.openclaw/reminders_db.json` | Reminder definitions |
| `~/.openclaw/send_reminder.py` | Cron-able Python sender |
| WAHA (`localhost:3000`) | WhatsApp HTTP API delivery |
| macOS cron | Triggers every minute |

## WAHA API — Live Endpoint

**URL:** `http://localhost:3000/send`  ← not `/api/sendText`

- **Auth:** none required (local-only instance)
- **Payload:** `{"chatId": "<phone>@c.us", "message": "<text>"}`
- **Phone format:** E.164 stripped of `+` + `@c.us`
- **Method:** POST with `Content-Type: application/json`
- **Note:** The documented `/api/sendText` path does NOT work — always use `/send`

### Verified working curl

```bash
curl -s -X POST "http://localhost:3000/send" \
  -H "Content-Type: application/json" \
  -d '{"chatId": "60125226892@c.us", "message": "your message here"}'
```

## Current Active Reminders

| Message | Schedule |
|---------|----------|
| Stock radar check - is today a buy day? | weekdays 21:45 |
| Victor 6PM Learning Scan - top 5 stocks | weekdays 18:00 |

## Notes

- ElevenLabs TTS is **not** used for reminders — plain text only
- Voice messages require a separate pipeline (see SOUL.md / TOOLS.md TTS section)
- WAHA session name is `default`, linked to Wisgoo (+601****2035)
- The `send_reminder.py` script uses a different URL — if direct sending, use `/send` not what the script has configured
