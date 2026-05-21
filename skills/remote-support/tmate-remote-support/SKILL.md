---
name: tmate-remote-support
description: Instant terminal sharing for remote support — no account, no config, free.
tags: [remote-support, tmate, terminal]
---
# tmate Remote Support

**Purpose:** Instant terminal sharing for remote support — no account, no config, free.

**Setup:** Already installed on this Mac (`brew install tmate` ✓)

**How it works:**
1. Friend runs `tmate` on their Mac
2. tmate shows two connection URLs (read-only + read-write)
3. Friend sends you the URL
4. You paste the URL in your terminal — you're in their session

**Important note:** tmate is deprecated upstream, disabled ~Dec 2026. Keep an eye on alternatives.

## Usage

### Friend's side (their Mac):
```bash
brew install tmate   # one-time only
tmate                # run when they need help
```

They'll see something like:
```
[tmate] web session: https://tmate.io/t/xxxxx
[tmate] web session (read-only): https://tmate.io/t/xxxxx-ro
[tmate] ssh session: ssh xxxxx@tmate.io
[tmate] ssh session (read-only): ssh xxxxx-ro@tmate.io
```

Tell them to send you ANY ONE of those URLs.

### Your side:
Paste the URL they send you into your terminal. Done.

## Pitfalls
- tmate is deprecated upstream (disabled ~Dec 2026). Monitor for alternatives.
- Always confirm the friend's exact macOS/terminal setup before asking them to run commands.
- If they get "command not found", run `brew install tmate` first.