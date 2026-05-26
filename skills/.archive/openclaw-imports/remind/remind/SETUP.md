# Remind Skill — Setup Guide

Set up an independent WhatsApp reminder system. No AI, no pyautogui, no OpenClaw in the firing path.

---

## What This Does

A Python script fires WhatsApp reminders every minute via WAHA HTTP API. You schedule reminders by editing a JSON file — Wis handles the rest.

---

## Architecture

| Component | Purpose |
|-----------|---------|
| WAHA Docker | WhatsApp session manager, exposes HTTP API on port 3000 |
| `send_reminder.py` | Python script — reads DB, calls WAHA API every minute |
| `reminders_db.json` | JSON file storing all reminder schedules |
| macOS cron | Runs `send_reminder.py` every minute automatically |

---

## Step 1 — WAHA Setup

WAHA is a Docker container that links a phone number to a WhatsApp Web session.

**Run WAHA Docker:**
```bash
docker run -d \
  --name waha \
  -p 3000:3000 \
  -e TZ=Asia/Kuala_Lumpur \
  devlikebear/waha:latest
```

**Configure the session:**
1. Open http://localhost:3000 in browser
2. Scan WhatsApp QR code with the phone number you want to use
3. Note the session name (default: `default`)

**WAHA API key:** Get from the WAHA dashboard or config. You'll need it for the API calls.

**Test WAHA is running:**
```bash
curl -s -X POST "http://localhost:3000/api/sendText" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"session":"default","chatId":"60123456789@c.us","text":"test"}'
```

Replace `60123456789` with the target phone number (E.164 without `+`).

---

## Step 2 — Create the Reminder Scripts

**File 1: `~/.openclaw/send_reminder.py`**

```python
#!/usr/bin/python3
"""
Wis Reminder — via WAHA HTTP API
Cron runs this every minute. Checks DB for due reminders and fires via WAHA.
No OpenClaw, no AI in the firing path.
"""
import json, sys, datetime, urllib.request, urllib.error
from pathlib import Path

WAHA_URL = "http://localhost:3000/api/sendText"
WAHA_KEY = "YOUR_API_KEY_HERE"
DB       = Path.home() / ".openclaw" / "reminders_db.json"
LOG      = Path.home() / ".openclaw" / "waha_reminder.log"

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def load_db():
    if not DB.exists():
        return []
    with open(DB) as f:
        return json.load(f)

def is_due(r):
    now = datetime.datetime.now()
    sched = r.get("schedule", {})
    kind  = sched.get("kind", "once")

    if kind == "once" and r.get("done"):
        return False

    if kind == "once":
        due_str = f"{sched.get('due_date')}T{sched.get('due_time')}"
        try:
            due = datetime.datetime.fromisoformat(due_str)
            return due <= now
        except:
            return False

    elif kind in ("daily", "weekdays"):
        t = sched.get("time", "09:00")
        h, m = map(int, t.split(":"))
        if kind == "weekdays" and now.strftime("%A") in ("Saturday", "Sunday"):
            return False
        return now.hour == h and now.minute == m and now.second < 30

    return False

def send_wa(phone, text):
    """Send WhatsApp via WAHA HTTP API using urllib."""
    chat_id = phone.lstrip("+") + "@c.us"
    payload = json.dumps({"session": "default", "chatId": chat_id, "text": text}).encode()
    req = urllib.request.Request(
        WAHA_URL,
        data=payload,
        headers={"X-Api-Key": WAHA_KEY, "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status in (200, 201):
                log(f"✓ Sent to {phone}: {text[:50]}")
                return True
        log(f"✗ WAHA status {resp.status}")
        return False
    except Exception as e:
        log(f"✗ Send failed: {e}")
        return False

def process():
    db = load_db()
    fired = 0
    for r in db:
        if is_due(r):
            target = r.get("to", "+60125226892")
            msg    = r.get("message", "")
            if send_wa(target, msg):
                r["last_fired"] = datetime.datetime.now().isoformat()
                if r.get("schedule", {}).get("kind") == "once":
                    r["done"] = True
                fired += 1
    with open(DB, "w") as f:
        json.dump(db, f, indent=2)
    return fired

if __name__ == "__main__":
    n = process()
    log(f"Processed {n} reminders.")
```

**File 2: `~/.openclaw/reminders_db.json`** — empty starter:

```json
[]
```

---

## Step 3 — Set Up Cron Job

Add this to your macOS crontab:
```bash
crontab -e
```

Paste this line:
```
* * * * * /usr/bin/python3 ~/.openclaw/send_reminder.py
```

This runs every minute, every hour, every day.

**Check cron is active:**
```bash
crontab -l
```

---

## Step 4 — Create the SKILL.md

Save `~/.openclaw/skills/remind/SKILL.md` with the skill reference.

---

## Step 5 — Add Reminders

Wis adds reminders by editing `reminders_db.json`. The format:

```json
{
  "id": "unique-id-1",
  "message": "Your reminder message here",
  "to": "+60123456789",
  "schedule": {
    "kind": "once",
    "due_date": "2026-05-01",
    "due_time": "09:00"
  },
  "done": false,
  "last_fired": null
}
```

**Schedule types:**
- `once` — fires once at `due_date` + `due_time`, then marks `done: true`
- `daily` — fires every day at `time`
- `weekdays` — fires Monday–Friday at `time`

**To add via Wis:** Just tell Wis "add a reminder for [date] at [time] to [message]"

---

## Step 6 — Verify It Works

```bash
# Manual test
/usr/bin/python3 ~/.openclaw/send_reminder.py

# Check log
tail ~/.openclaw/waha_reminder.log

# View reminders
cat ~/.openclaw/reminders_db.json
```

---

## Troubleshooting

**Reminders not firing:**
1. Check cron: `crontab -l`
2. Check WAHA is running: `curl -s http://localhost:3000/health`
3. Check log: `tail ~/.openclaw/waha_reminder.log`

**WAHA session disconnected:**
- WAHA dashboard → rescan QR code
- Or restart Docker: `docker restart waha`

**Python script error:**
- Check Python path: `which python3`
- Make executable: `chmod +x ~/.openclaw/send_reminder.py`

---

## Key Design Principles

- **No AI in firing path** — Wis only writes to the JSON DB; the Python script fires reminders independently
- **No pyautogui** — no image-based automation
- **WAHA API is fire-and-forget** — Python calls WAHA directly, no browser needed
- **Fails gracefully** — if WAHA is down, script logs error and retries next minute
