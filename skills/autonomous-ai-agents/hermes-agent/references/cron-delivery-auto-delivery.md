# Cron Job Delivery & Auto-Delivery

## The Core Rule

When a cron job has `deliver: "origin"` (the default for home-channel jobs), the platform's auto-delivery system sends the final response to the target platform **automatically**. Do NOT try to manually send the same message via `hermes send` or `send_message` — the system will detect the duplicate and refuse.

## How `hermes send` Reacts

`hermes send` inspects the running job's delivery config. If the job has `deliver: "origin"` AND the target matches the job's auto-delivery destination, it skips the send and emits:

```
Skipped send_message to whatsapp:56702359580792@lid. This cron job will
already auto-deliver its final response to that same target.
```

**This is correct behavior.** The deduplication protects the user from receiving the same reminder twice.

## For Cron Job Authors

When authoring a cron job prompt that sends a WhatsApp/Telegram/etc. reminder:

| Scenario | What to do |
|----------|------------|
| Job has `deliver: "origin"` (home channel) | Put the reminder text in your **final response**. Auto-delivery handles it. Do NOT call `hermes send`. |
| Job has explicit `deliver: "whatsapp:..."` | Auto-delivery sends to that specific target. Same rule — put content in final response. |
| Job has `no_agent: true` (script-only) | The script stdout IS the message. Emit the reminder text directly from the script. |
| Job has `deliver: "local"` | No auto-delivery. Use `hermes send` if outbound sending is needed. |

## Anti-Pattern: Double-Send

```python
# WRONG — inside a cron job with auto-delivery to WhatsApp home channel:
hermes send --to "whatsapp:Goo Kah Thart" "⏰ Reminder: Interview starts in 10 min"
# Result: deduplication block, message not sent, user gets nothing
```

```python
# CORRECT — just put the content in your final response:
⏰ Reminder: Interview starts in 10 minutes (10:00 AM)
# Auto-delivery sends this to WhatsApp home channel
```

## How to Verify Delivery Config

```bash
hermes cron list --all | jq '.[] | select(.id == "JOB_ID") | {deliver, prompt}'
```

Or inspect `~/.hermes/cron/jobs.json` directly for the `deliver` and `platform` fields.

## Deduplication Scope

The deduplication check matches on:
- Platform (whatsapp, telegram, etc.)
- Target chat ID

It does NOT deduplicate across different target chat IDs. A job configured to deliver to `whatsapp:56702359580792@lid` can still manually send to a different WhatsApp contact (e.g., `whatsapp:120363423080731840@g.us`).