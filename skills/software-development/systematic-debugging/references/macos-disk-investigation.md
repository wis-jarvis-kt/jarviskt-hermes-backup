# macOS Disk Investigation — APFS Volume gotchas

## The Critical macOS APFS Volume Structure

macOS with APFS uses TWO volumes in one container:

| Mount | Volume | What lives here |
|-------|--------|-----------------|
| `/` (disk3s1s1) | Macintosh HD | System files, APFS snapshots |
| `/System/Volumes/Data` (disk3s5) | Macintosh HD — Data | User files, apps, home directory |

**`df -h /` is USELESS for user disk analysis.** It shows the read-only system volume (~17GB used, tiny). The real data is on `/System/Volumes/Data`.

**Always check the DATA volume:**
```bash
df -h /System/Volumes/Data
```

## APFS Snapshots Pin Space

macOS creates read-only snapshots that `tmutil` manages. These pin space on the data volume and cannot be deleted without sudo.

```
tmutil listlocalsnapshots /System/Volumes/Data
# Lists snapshots like com.apple.os.update-XXXXXXXXXXXX
```

**Delete a snapshot (requires sudo):**
```bash
sudo tmutil deletelocalsnapshots <snapshot-id>
```

**Thin snapshots (requires sudo):**
```bash
sudo tmutil thinlocalsnapshots /System/Volumes/Data 200000 2
```

## `du -sh /Users/*` Hangs on Large Home Directories

60-second timeout is not enough when scanning all user home directories.

**Workaround: scan subdirectories individually:**
```bash
du -sh ~/Library/Caches ~/Library/Application\ Support ~/.cache ~/.hermes /tmp
```

## Typical Space Consumers on macOS

From largest to smallest on a developer machine:

- `~/Library/Application Support/<App>` — app data (Chrome profile, Claude, games, etc.)
- `~/Library/Caches/<App>` — caches (safe to delete, apps rebuild them)
- `~/.cache/` — pip, uv, puppeteer, playwright, etc.
- `~/.hermes/` — agent state, sessions, logs
- `/tmp` — temp files (usually tiny)

## Key Commands

```bash
# Check data volume (correct)
df -h /System/Volumes/Data

# Check which disk is data volume
diskutil info / | grep -E "Volume Name|Container|Total"

# List snapshots
tmutil listlocalsnapshots /System/Volumes/Data

# Scan home subdirs (fast, no hang)
du -sh ~/Library/Caches ~/Library/Application\ Support ~/.cache ~/.hermes /tmp

# Find files > 50MB modified in last 7 days
find /Users/ktoclaw -type f -size +50M -mtime -7 2>/dev/null | sort
```

## What NOT to Delete Without Asking

- `~/Library/Application Support/Google/Chrome` — Chrome profile, signing you out of everything
- `~/Library/Application Support/Claude` — your Claude data
- `~/.hermes/` — agent state and memory

## Safe to Delete Without Asking

- `~/.cache/uv/*` — uv package cache, re-downloads as needed
- `~/.cache/puppeteer/*` — puppeteer browser cache
- `~/.cache/qmd/*` — Quarto cache
- `~/.cache/whisper/*` — Whisper cache
- `~/Library/Caches/pip/*` — pip cache
- `~/Library/Caches/Homebrew/*` — Homebrew cache
- `~/Library/Caches/ms-playwright/*` — Playwright browser cache
- `~/Library/Application Support/Google/GoogleUpdater/*` — updater artifacts
- `~/Library/Application Support/gogcli/drive-downloads/*` — game installers
