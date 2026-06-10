---
name: imessage
description: Send and receive iMessages/SMS via the imsg CLI on macOS.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [iMessage, SMS, messaging, macOS, Apple]
prerequisites:
  commands: [imsg]
---

# iMessage

Use `imsg` to read and send iMessage/SMS via macOS Messages.app.

## Prerequisites

- **macOS** with Messages.app signed in
- Install: `brew install steipete/tap/imsg`
- Grant Full Disk Access for terminal (System Settings → Privacy → Full Disk Access)
- Grant Automation permission for Messages.app when prompted

## When to Use

- User asks to send an iMessage or text message
- Reading iMessage conversation history
- Checking recent Messages.app chats
- Sending to phone numbers or Apple IDs

## When NOT to Use

- Telegram/Discord/Slack/WhatsApp messages → use the appropriate gateway channel
- Group chat management (adding/removing members) → not supported
- Bulk/mass messaging → always confirm with user first

## Quick Reference

### List Chats

```bash
imsg chats --limit 10 --json
```

### View History

```bash
# By chat ID
imsg history --chat-id 1 --limit 20 --json

# With attachments info
imsg history --chat-id 1 --limit 20 --attachments --json
```

### Send Messages

```bash
# Text only
imsg send --to "+14155551212" --text "Hello!"

# With attachment
imsg send --to "+14155551212" --text "Check this out" --file /path/to/image.jpg

# Force iMessage or SMS
imsg send --to "+14155551212" --text "Hi" --service imessage
imsg send --to "+14155551212" --text "Hi" --service sms
```

### Watch for New Messages

```bash
imsg watch --chat-id 1 --attachments
```

## Service Options

- `--service imessage` — Force iMessage (requires recipient has iMessage)
- `--service sms` — Force SMS (green bubble)
- `--service auto` — Let Messages.app decide (default)

## Pitfalls

### Attachments Folder Permission Error (NSCocoaErrorDomain Code 513)
When sending files with `--file`, `imsg` attempts to copy the attachment to `~/Library/Messages/Attachments/`. If that directory is not writable (e.g., permission denied), the send fails with:
```
Error Domain=NSCocoaErrorDomain Code=513 "You don't have permission to save the file 'imsg' in the folder 'Attachments'."
```
**Workarounds (in order):**
1. Copy the file to `/tmp/` first — avoid `~/Library/Messages/Attachments/` by using a temp path
2. If that still fails, the macOS Messages app itself is blocking the attachment path — fall back to Hermes `send_message` for text-only, or use `open` to open the file so the user can send manually
3. osascript fallback (`tell application "Messages" to send ...`) is unreliable on some setups — it times out. Do not use as primary path.

### Cron Jobs / Headless Context
`imsg` reads from `~/Library/Messages/chat.db` and **requires Full Disk Access**. Running in a cron job, LaunchAgent, or headless context (no GUI session) will fail with `permissionDenied` even if the tool is installed. Workarounds:
- Use a macOS GUI session that's been authorized
- Use a platform gateway (Telegram, Discord, etc.) as the delivery channel instead of iMessage
- If iMessage delivery is required, deliver the text to a file and have a GUI-side script pick it up

### Wrong Send Flag
`imsg send -c <id>` is **wrong** — `-c` is not a valid flag for `send`. Use one of:
- `--chat-guid <guid>` — the full chat identifier string (e.g. `iMessage;+;chat...`)
- `--chat-id <rowid>` — the numeric database rowid (from `imsg chats --json`)
- `--to <phone>` — send to a phone number

### Confusing Chat-ID vs Chat-Guid
`imsg chats --json` returns both `id` (rowid) and `guid`/`chatIdentifier` fields. `--chat-id` takes the numeric rowid; `--chat-guid` takes the string identifier. Mixing them up produces `Unknown chat` errors.

## Rules

1. **Always confirm recipient and message content** before sending
2. **Never send to unknown numbers** without explicit user approval
3. **Verify file paths** exist before attaching
4. **Don't spam** — rate-limit yourself
5. **Test `imsg chats` first** to verify database access before a mission-critical send

## Example Workflow

User: "Text mom that I'll be late"

```bash
# 1. Find mom's chat
imsg chats --limit 20 --json | jq '.[] | select(.displayName | contains("Mom"))'

# 2. Confirm with user: "Found Mom at +1555123456. Send 'I'll be late' via iMessage?"

# 3. Send after confirmation
imsg send --to "+1555123456" --text "I'll be late"
```
