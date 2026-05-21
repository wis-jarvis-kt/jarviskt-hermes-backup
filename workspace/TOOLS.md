# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## TTS / Voice

- **Preferred voice:** Daniel (Steady Broadcaster)
  - ElevenLabs voice ID: `onwK4e9ZLuTAKqWW03F9`
  - ElevenLabs API key: stored in `~/.openclaw/.env` as `ELEVENLABS_API_KEY`
  - ⚠️ **ElevenLabs auth issue (2026-05-01):** TTS returning 401 Unauthorized — under investigation. Currently using macOS `say -v Daniel` as fallback.
- **Whisper model:** `tiny` (fast, default); use `medium` for higher accuracy
- **Fallback for TTS:** `say -v Daniel` (macOS native, no auth needed)
- **Note on voice send:** When sending voice via WhatsApp media — file goes to `~/.openclaw/workspace/media/` → sent via OpenClaw gateway. First attempt may race with gateway's encryption tempfile → auto-retry on reconnect succeeds. Confirmed working 2026-05-01.

## Devices / Network

- **Mac mini (2):** 192.168.0.118 — always on, locked screen OK
- **OpenClaw gateway:** http://127.0.0.1:18789 (local loopback only)

## Calendars

- **Primary calendar:** jarvisktgoo@gmail.com (Google Calendar)
- **"Set appt" rule:** Whenever Master KT says "set appointment" or "set appt" → create in Google Calendar (jarvisktgoo@gmail.com), no need to ask first
- **"Lock" rule:** Whenever Master KT says "lock the interview" or equivalent ("lock it", "confirm", "book it") → automatically add a WAHA reminder 15 minutes before the appointment start time via the Remind skill
- **Default duration:**
  - **Interviews & Closings:** 30 minutes
  - **All other appointments:** 1 hour
  - Unless KT specifies a different duration
- **Terminology rule (set 2026-05-07):** "Closing" and "Interview" are the SAME thing in Master KT's world. Don't ask which — just lock the appointment with whichever word he used (or use "Interview" by default). Both are 30 min.

## WhatsApp

- **Wis number:** +60175972035
- **Master KT number:** +60125226892
- **499 disconnects:** Status 499 = normal keep-alive idle restart. Connection always recovers on its own within seconds. **Do NOT alert Master KT about 499s** — they are not errors and do not require QR re-scan.
  - Only alert if Wis actually stops responding to messages (i.e. gateway fails to reconnect after >5 min)
  - Rule corrected 2026-04-02 after KT flagged excessive false alerts
- **WAHA restart recovery (set 2026-05-05):** When WAHA Docker container is restarted, the OpenClaw gateway needs to be restarted too to re-register the WhatsApp outbound channel.
  - Symptom: `openclaw message send --channel whatsapp` returns `Outbound not configured for channel: whatsapp`
  - Fix: `openclaw gateway restart` — gateway will re-register the WhatsApp channel within a few seconds
  - The WAHA WhatsApp session itself usually persists (no QR re-scan needed) — only the gateway-to-WAHA bridge needs refreshing

## GitHub (Wis)

- **Username:** `wis-jarvis-kt`
- **Email:** jarvisktgoo@gmail.com
- **Backup repo:** `wis-jarvis-kt/openclaw-backups` (private)
- **Token:** stored in `~/.openclaw/.env` as `GH_TOKEN`

## Accounts / APIs

- **Google Gemini API key (direct):** `AIzaSyCPNn0kYexI6r2-JpvC5BWvCUesNw6UMj0` — stored in macOS Keychain as `google-gemini-api-key` / `jarvisktgoo@gmail.com`. Configured as `google-gemini` provider in openclaw.json (gemini-2.5-flash model). No OAuth needed.
- **gog Gmail OAuth:** Token stored in macOS Keychain (`gogcli` service, entry: `token:default:jarvisktgoo@gmail.com`). Can expire — re-auth with: `gog auth add jarvisktgoo@gmail.com --services gmail,calendar,drive,contacts,docs,sheets`
- **HLA portal:** https://portal.hla.com.my/login/default.aspx | Login: ktgoo2880 / PortalKT88-3
- **Script:** `skills/hla-annual-stmt/scripts/hla_life_ins_prem_stmt.py` — downloads statements, saves to `~/WisSend/`

## HLA Client Policy Reference

- **Agent A0022418 = KT (GOO KAH THART)** — default agent code on portal load
- **Agent A0037263 = THAM MAY PENG (May Peng)** — must change dropdown before searching under this agent
- **Wong Kar Wai:** Policy UL202528294172 under A0037263
- **Wong Yik Chun (A0037263):** Policy UL202528370623, RM470/mth, next due 16-Apr-2026
- **Too Foong Theng (A0037263):** Policy UL202528373530, RM260/mth, next due 16-Apr-2026, payer = Wong Yik Chun
- **Annual statement workflow:** Hamburger → Servicing → Policy → Letter/Statement → Life Insurance Premium Statement. Select agent code FIRST, then Life Assured name, then Year, then Get Record.
- **Key selectors:** agent code `cphContent_ddlSearchAgentCode`, name `cphContent_txtLifeAssuredName`, year `cphContent_cboDUYear`, button `cphContent_btnGetRec`, PDF link `a[id*="Hyperlink1"]`
- **PDF filename format:** `YYYY_YYYYMMDD_AnnStmt_XXXXXX`
- **Session timeout:** ~2 min — always re-login if expired

## Formatting Rules

- **WhatsApp:** No markdown tables; use bullet lists. No headers — use **bold** or CAPS
- **Discord:** No tables; wrap multiple links in `<>` to suppress embeds

## Instagram Scraping (set 2026-04-24)
- **Script:** `workspace/scripts/instagram_extract.py` — uses instaloader + imginn fallback
- **Usage:** `python3 instagram_extract.py <shortcode|URL> --fallback`
- **Output:** Lists all carousel slide URLs (1 per line, "Slide N: URL")
- **Standard pipeline:** Scrape → extract shortcode → download slides (ThreadPoolExecutor) → batch analyse (image tool) → compile summary → send to **BOTH email AND WhatsApp**
- **Download:** Slides saved to `workspace/media/ig_[shortcode]_[N].jpg`

## Email Sending (Wis learned)
- **Preferred email path:** use `gog gmail send` with account `jarvisktgoo@gmail.com`
  - ⚠️ **gog OAuth token can expire** — if `gog auth list --check` shows `false` or `invalid_grant`, re-run: `gog auth add jarvisktgoo@gmail.com --services gmail,calendar,drive,contacts,docs,sheets`
- **Permanent email fix (2026-04-24):** App Password `obdiubdgknggyptp` stored in macOS Keychain. Send email via smtplib directly:
  ```python
  smtplib.SMTP('smtp.gmail.com', 587) → starttls() → login(my_email, app_password)
  ```
  No OAuth needed — works forever without re-auth.
  Keychain entry: `gmail-smtp-app-password` / `jarvisktgoo@gmail.com`
- **For file attachments:** use `gog gmail send --attach <file>`
- **Do not default to himalaya** unless a verified config exists, because it is currently not configured on this machine
- **If Master KT asks to email a file:** use `gog gmail send --to ktgoofp@gmail.com --subject ... --body-file ... --attach <file>`
- **Master KT email:** `ktgoofp@gmail.com`

## Reminder System — WAHA (set 2026-04-30)
**Independent WhatsApp reminder sender - no OpenClaw, no AI, no pyautogui.**
- WAHA Docker on port 3000 (linked to +60175972035, session "default", status WORKING)
- Reminder DB: `~/.openclaw/reminders_db.json`
- Sender: `~/.openclaw/send_reminder.py` (urllib > WAHA HTTP API)
- Cron: `* * * * * /usr/bin/python3 ~/.openclaw/send_reminder.py` (every min, no daemon)
- WAHA API key: `c838c39d3a9d4d40ac151f6a0f7372f1` (new, needs QR scan)
- **Add reminders:** tell Wis, I write to `reminders_db.json`
- **No pyautogui, no Chrome windows, no extra WhatsApp tabs**
- OLD files deleted 2026-04-30: `~/.openclaw/reminders/` (reminder_keeper, wa_send_chrome.py, etc.)

### Active Reminders:
| Message | Schedule |
|---------|----------|
| Stock radar check - is today a buy day? | weekdays 21:45 |
| Victor 6PM Learning Scan - top 5 stocks | weekdays 18:00 |

### Commands:
```bash
cat ~/.openclaw/reminders_db.json   # list reminders
tail ~/.openclaw/waha_reminder.log   # check logs
/usr/bin/python3 ~/.openclaw/send_reminder.py  # manual test
```

## HLA Annual Statement — Full Workflow (set 2026-04-29)
When Master KT asks for annual statement (HLA):
1. Edit SEARCHES list in `hla-annual-stmt/scripts/hla_life_ins_prem_stmt.py`
2. Ensure Chrome running on port 9250 with `--remote-debugging-port=9250`
3. Run: `python3 hla-annual-stmt/scripts/hla_life_ins_prem_stmt.py`
4. Wait for PDFs in `~/WisSend/`
5. Send each PDF: `openclaw message send --channel whatsapp --target +60125226892 --media ~/WisSend/{filename}.pdf --message "HLA Annual Statement 2025 — {NAME}"`
6. Delete PDFs after sending
7. Reset SEARCHES to default ("Lee Yoke Ming")
