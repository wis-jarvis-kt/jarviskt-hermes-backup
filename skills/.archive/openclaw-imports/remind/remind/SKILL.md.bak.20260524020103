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

## WAHA API Details

- **URL:** `http://localhost:3000/api/sendText`
- **Auth:** `X-Api-Key: 63b5195f18e94c0e86976b2dfb9f6d7c`
- **Payload:** `{"session": "default", "chatId": "<phone>@c.us", "text": "<message>"}`
- **Phone format:** E.164 stripped of `+` + `@c.us`

## Current Active Reminders

| Message | Schedule |
|---------|----------|
| Stock radar check - is today a buy day? | weekdays 21:45 |
| Victor 6PM Learning Scan - top 5 stocks | weekdays 18:00 |

## Notes

- ElevenLabs TTS is **not** used for reminders — plain text only
- Voice messages require a separate pipeline (see SOUL.md / TOOLS.md TTS section)
- WAHA session name is `default`, linked to Wisgoo (+60175972035)
