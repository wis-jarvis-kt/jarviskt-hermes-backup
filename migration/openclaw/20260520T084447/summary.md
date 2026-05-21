# OpenClaw -> Hermes Migration Report

- Timestamp: 20260520T084447
- Mode: execute
- Source: `/Users/ktoclaw/.openclaw`
- Target: `/Users/ktoclaw/.hermes`

## Summary

- migrated: 17
- archived: 4
- skipped: 31
- conflict: 2
- error: 0

## Warnings

- Conflicts were found. Re-run with --overwrite to replace conflicting targets after item-level backups.
- A config.yaml write hit a conflict or error mid-apply; later config items were skipped to avoid a partial write.

## What Was Not Fully Brought Over

- `/Users/ktoclaw/.openclaw/workspace/AGENTS.md` -> `(n/a)`: No workspace target was provided
- `/Users/ktoclaw/.openclaw/openclaw.json` -> `/Users/ktoclaw/.hermes/.env`: No Hermes-compatible messaging settings found
- `/Users/ktoclaw/.openclaw/openclaw.json` -> `/Users/ktoclaw/.hermes/.env`: No allowlisted Hermes-compatible secrets found
- `/Users/ktoclaw/.openclaw/openclaw.json` -> `/Users/ktoclaw/.hermes/.env`: No Discord settings found
- `/Users/ktoclaw/.openclaw/openclaw.json` -> `/Users/ktoclaw/.hermes/.env`: No Slack settings found
- `/Users/ktoclaw/.openclaw/openclaw.json` -> `/Users/ktoclaw/.hermes/.env`: No WhatsApp settings found
- `/Users/ktoclaw/.openclaw/openclaw.json` -> `/Users/ktoclaw/.hermes/.env`: No Signal settings found
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `/Users/ktoclaw/.hermes/tts`: Source directory not found
- `/Users/ktoclaw/.openclaw/openclaw.json` -> `(n/a)`: Selected Hermes-compatible values were extracted; raw OpenClaw config was not copied.
- `/Users/ktoclaw/.openclaw/memory/main.sqlite` -> `(n/a)`: Contains secrets, binary state, or product-specific runtime data
- `/Users/ktoclaw/.openclaw/credentials` -> `(n/a)`: Contains secrets, binary state, or product-specific runtime data
- `/Users/ktoclaw/.openclaw/devices` -> `(n/a)`: Contains secrets, binary state, or product-specific runtime data
- `/Users/ktoclaw/.openclaw/identity` -> `(n/a)`: Contains secrets, binary state, or product-specific runtime data
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `(n/a)` -> `(n/a)`: blocked by earlier apply conflict
- `/Users/ktoclaw/.openclaw/workspace/SOUL.md` -> `/Users/ktoclaw/.hermes/SOUL.md`: Target exists and overwrite is disabled
- `/Users/ktoclaw/.openclaw/openclaw.json` -> `/Users/ktoclaw/.hermes/config.yaml`: Model already set and overwrite is disabled

## Next Steps

- Review the migration report at /Users/ktoclaw/.hermes/migration/openclaw/20260520T084447/summary.md
- Start a new Hermes session (or /reset) to pick up the imported config.
- Re-run with --overwrite to apply items that were blocked by conflicts.
