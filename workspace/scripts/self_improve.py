#!/usr/bin/env python3
"""
Wis Self-Improvement Engine
Runs nightly 2AM–5AM
1. Backs up core identity/memory files
2. Reviews them for improvements (clarity, outdated info, gaps)
3. Applies improvements
4. Sends WhatsApp report to Master KT
"""

import os
import sys
import json
import shutil
import subprocess
import datetime
from pathlib import Path

WORKSPACE = Path("/Users/ktoclaw/.openclaw/workspace")
BACKUP_BASE = WORKSPACE / "self-improve-backups"
MEMORY_DIR = WORKSPACE / "memory"
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Files eligible for self-improvement review
CORE_FILES = [
    WORKSPACE / "SOUL.md",
    WORKSPACE / "AGENTS.md",
    WORKSPACE / "TOOLS.md",
    WORKSPACE / "HEARTBEAT.md",
    WORKSPACE / "MEMORY.md",
    WORKSPACE / "IDENTITY.md",
]

BACKUP_DIR = BACKUP_BASE / TIMESTAMP


def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def backup_files():
    """Back up all core files before any edits."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backed_up = []
    for f in CORE_FILES:
        if f.exists():
            dest = BACKUP_DIR / f.name
            shutil.copy2(f, dest)
            backed_up.append(f.name)
            log(f"✅ Backed up: {f.name}")
    # Write backup manifest
    manifest = {
        "timestamp": TIMESTAMP,
        "date": TODAY,
        "files": backed_up,
    }
    (BACKUP_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    log(f"📦 Backup saved to: {BACKUP_DIR}")
    return backed_up


def read_file(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        return ""


def call_claude(prompt, max_tokens=4000):
    """Call Claude via the claude CLI for improvement suggestions."""
    cmd = [
        os.path.expanduser("~/.local/bin/claude"),
        "--print",
        "--permission-mode", "bypassPermissions",
        "--model", "claude-sonnet-4-5",
        prompt
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            log(f"⚠️ Claude error: {result.stderr[:200]}")
            return None
    except subprocess.TimeoutExpired:
        log("⚠️ Claude timed out")
        return None
    except FileNotFoundError:
        log("⚠️ Claude CLI not found at ~/.local/bin/claude")
        return None


def improve_file(filepath):
    """Ask Claude to review and improve a single file. Returns (improved_content, summary) or None."""
    content = read_file(filepath)
    if not content or len(content) < 50:
        return None

    filename = Path(filepath).name
    prompt = f"""You are Wis, an AI assistant. You are reviewing your own configuration file: {filename}

Current content:
---
{content}
---

Your job: Identify improvements to make this file better. Look for:
1. Outdated info, dead tasks, or stale references
2. Missing clarity — things that are ambiguous or confusing
3. Rules that could be tightened or made more actionable
4. Anything that would make you more effective or accurate

RULES:
- DO NOT change Master KT's name, identity, or personal details
- DO NOT remove standing rules without very strong reason
- DO NOT invent new information — only clarify or restructure existing info
- Keep changes minimal and surgical — do not rewrite unnecessarily
- If no improvements needed, reply with exactly: NO_CHANGE

If improvements are needed, output:
SUMMARY: [1–3 bullet points describing what you changed]
---IMPROVED---
[Full improved content here]"""

    response = call_claude(prompt)
    if not response:
        return None

    if "NO_CHANGE" in response[:50]:
        return None

    if "---IMPROVED---" in response:
        parts = response.split("---IMPROVED---", 1)
        summary_block = parts[0].strip()
        improved_content = parts[1].strip()
        # Extract summary bullets
        summary = summary_block.replace("SUMMARY:", "").strip()
        return improved_content, summary

    return None


def prune_old_backups():
    """Keep only last 14 days of self-improve backups."""
    if not BACKUP_BASE.exists():
        return
    backups = sorted([d for d in BACKUP_BASE.iterdir() if d.is_dir()])
    if len(backups) > 14:
        for old in backups[:-14]:
            shutil.rmtree(old, ignore_errors=True)
            log(f"🗑️ Pruned old backup: {old.name}")


def send_whatsapp(message):
    """Send WhatsApp message to Master KT via openclaw message tool."""
    # Use the wacli or openclaw message tool via subprocess
    cmd = [
        "node",
        "-e",
        f"""
const {{ OpenClaw }} = require('/opt/homebrew/lib/node_modules/openclaw');
// fallback: use wacli if available
"""
    ]
    # Simpler: write message to a temp file and use openclaw send
    # Actually use the message action via openclaw CLI
    msg_cmd = [
        "openclaw", "message", "send",
        "--channel", "whatsapp",
        "--target", "+60125226892",
        "--message", message
    ]
    try:
        result = subprocess.run(msg_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            log("📱 WhatsApp report sent!")
        else:
            log(f"⚠️ WhatsApp send failed: {result.stderr[:200]}")
            # Try fallback: write to a report file
            report_path = WORKSPACE / f"memory/self-improve-report-{TODAY}.md"
            report_path.write_text(message)
            log(f"📝 Report saved to: {report_path}")
    except Exception as e:
        log(f"⚠️ Failed to send WhatsApp: {e}")
        report_path = WORKSPACE / f"memory/self-improve-report-{TODAY}.md"
        report_path.write_text(message)
        log(f"📝 Report saved to: {report_path}")


def write_daily_memory(changes_summary):
    """Append improvement log to today's memory file."""
    MEMORY_DIR.mkdir(exist_ok=True)
    mem_file = MEMORY_DIR / f"{TODAY}.md"
    entry = f"\n\n## 🔧 Self-Improvement Run — {NOW}\n\n"
    if changes_summary:
        for fname, summary in changes_summary:
            entry += f"### {fname}\n{summary}\n\n"
    else:
        entry += "_No improvements needed tonight._\n"

    with open(mem_file, "a", encoding="utf-8") as f:
        f.write(entry)
    log(f"📝 Logged to {mem_file}")


def main():
    log("🚀 Wis Self-Improvement Engine starting...")
    log(f"📅 Date: {TODAY}")

    # 1. Backup first
    backed_up = backup_files()
    if not backed_up:
        log("⚠️ No files backed up — aborting")
        return

    # 2. Review and improve each file
    changes = []  # list of (filename, summary)
    for filepath in CORE_FILES:
        if not filepath.exists():
            continue
        log(f"🔍 Reviewing {filepath.name}...")
        result = improve_file(filepath)
        if result:
            improved_content, summary = result
            # Write improved file
            filepath.write_text(improved_content, encoding="utf-8")
            changes.append((filepath.name, summary))
            log(f"✏️ Improved: {filepath.name}")
        else:
            log(f"✅ No changes needed: {filepath.name}")

    # 3. Log to daily memory
    write_daily_memory(changes)

    # 4. Send WhatsApp report
    if changes:
        report_lines = [f"🧠 *Wis Self-Improvement Report — {TODAY}*\n"]
        report_lines.append(f"📦 Backup saved: `self-improve-backups/{TIMESTAMP}/`\n")
        report_lines.append("Changes made tonight:\n")
        for fname, summary in changes:
            report_lines.append(f"*{fname}*\n{summary}\n")
        report_lines.append("\nAll originals backed up. Reply 'revert [filename]' to roll back any change.")
        report = "\n".join(report_lines)
    else:
        report = f"🧠 *Wis Self-Improvement Check — {TODAY}*\n\nAll core files reviewed. No improvements needed tonight. ✅"

    send_whatsapp(report)
    prune_old_backups()
    log("✅ Self-improvement run complete!")


if __name__ == "__main__":
    main()
