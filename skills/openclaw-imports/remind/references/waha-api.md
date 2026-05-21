# WAHA API Reference — remind skill

## ⚠️ Bridge Type: Baileys (NOT WAHA)

The WhatsApp bridge running at `localhost:3000` is a **Baileys** WebSocket bridge
(`@whiskeysockets/baileys`), NOT WAHA. It was set up as part of the Hermes Agent
WhatsApp gateway integration (`hermes-agent/gateway/platforms/whatsapp.py`).

**Critical implication:** chatId must be a full WhatsApp JID, not a WAHA-style
phone handle.

## Verified working request (2026-05-21)

**URL:** `POST http://localhost:3000/send`
**Auth:** none required (local bridge, localhost)

```json
{
  "chatId": "34652029134@s.whatsapp.net",
  "message": "🔔 Interview with Chris starting in 10 minutes (3:30 PM)"
}
```

Response: `{"success":true,"messageId":"3EB08A9079C3391BEE86E4"}`

## chatId format — CRITICAL

The Baileys bridge requires **full JID format**:

```
<phone_number>@s.whatsapp.net
```

**Never use:**
- Bare usernames like `ktoclaw` → `"Cannot destructure property 'user' of 'jidDecode(...)' as it is undefined."`
- Old `c.us` suffix (WAHA style) → not accepted by Baileys
- `lid` JIDs → for Linked Identity Devices only, not regular chats

**To find a contact's JID:**
```bash
curl http://localhost:3000/chat/<identifier>
# → {"name":"ktoclaw","isGroup":false,"participants":[]}
```

**Known working JIDs:**
- Master KT: `34652029134@s.whatsapp.net`

## What was broken (2026-05-21)

The skill doc previously used the WAHA API format (from the old `~/.openclaw/send_reminder.py` script):
- **Wrong endpoint:** `/api/sendText` → 404
- **Wrong payload:** `{"session": "default", "chatId": "...", "text": "..."}` → `"chatId and message are required"`
- **Correct payload:** `{"chatId": "...", "message": "..."}`

Also the old `c.us` suffix and API key auth are no longer valid — the Baileys bridge
accepts plain JSON POST with no auth header when called from localhost.

## Health check

```bash
curl http://localhost:3000/health
# → {"status":"connected","queueLength":0,"uptime":44035.492060917}
```

## Timeout errors

`"sendMessage timed out after 60s"` means the WhatsApp session is dead or not
fully authenticated. Retry or restart the bridge rather than continuing to poll.