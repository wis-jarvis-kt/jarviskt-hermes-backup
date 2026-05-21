#!/usr/bin/env python3
import json
import os
import shutil
import tarfile
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path('/Users/ktoclaw/.openclaw/workspace')
STATE = Path('/Users/ktoclaw/.openclaw')
BACKUP_ROOT = WORKSPACE / 'wis-backups'
EXPORT_ROOT = BACKUP_ROOT / 'exports'
MANIFEST_NAME = 'manifest.json'
README_NAME = 'RESTORE_README.md'
RETENTION_DAYS = int(os.environ.get('WIS_BACKUP_RETENTION', 7))

INCLUDE_PATHS = [
    WORKSPACE / 'AGENTS.md',
    WORKSPACE / 'SOUL.md',
    WORKSPACE / 'USER.md',
    WORKSPACE / 'IDENTITY.md',
    WORKSPACE / 'TOOLS.md',
    WORKSPACE / 'MEMORY.md',
    WORKSPACE / 'HEARTBEAT.md',
    WORKSPACE / 'memory',
    WORKSPACE / 'skills',
    WORKSPACE / 'projects',
    WORKSPACE / 'investing',
    WORKSPACE / 'reports',
    WORKSPACE / 'guides',
    WORKSPACE / 'conversion-codex',
    WORKSPACE / 'expert-panel',
    WORKSPACE / 'state',
    WORKSPACE / 'MODEL_CONFIG.md',
    WORKSPACE / 'MODEL_FALLBACK.md',
    STATE / 'openclaw.json',
    STATE / 'openclaw.json.bak',
    STATE / 'cron',
    STATE / 'memory',
    STATE / 'skills',
    STATE / 'agents',
]

EXCLUDE_NAMES = {
    '.git', 'node_modules', '__pycache__', '.DS_Store', 'venv', '.venv',
    'trash-review', 'wis-backups'
}

README = '''# Wis Restore Bundle

Purpose:
This backup is designed to restore Wis's continuity as completely as practical.

Included:
- persona/behavior files
- long-term and daily memory
- workspace skills and project context
- OpenClaw local state snapshots relevant to Wis
- cron job definitions
- restore manifest

Important limits:
- External provider sessions/tokens may still require re-auth
- Device pairings or browser sessions may not fully restore from this bundle alone
- This restores local continuity, not every remote service state

Suggested restore flow:
1. Unpack this bundle into the replacement workspace/state environment
2. Review manifest.json
3. Restore workspace files into the new workspace
4. Restore selected ~/.openclaw state files carefully
5. Ask the new Wis to read AGENTS.md, SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, TOOLS.md
6. Ask the new Wis to ingest this bundle and reconcile any missing auth/device state
'''


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_NAMES for part in path.parts)


def copy_path(src: Path, dest_root: Path, manifest_entries: list):
    if not src.exists():
        return
    rel = src.as_posix().lstrip('/')
    dest = dest_root / rel
    if src.is_dir():
        for root, dirs, files in os.walk(src):
            root_p = Path(root)
            dirs[:] = [d for d in dirs if d not in EXCLUDE_NAMES]
            if should_skip(root_p):
                continue
            for f in files:
                fp = root_p / f
                if should_skip(fp):
                    continue
                relf = fp.as_posix().lstrip('/')
                out = dest_root / relf
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fp, out)
                manifest_entries.append({
                    'path': '/' + relf,
                    'size': fp.stat().st_size,
                    'mtime': datetime.fromtimestamp(fp.stat().st_mtime).isoformat()
                })
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        manifest_entries.append({
            'path': '/' + rel,
            'size': src.stat().st_size,
            'mtime': datetime.fromtimestamp(src.stat().st_mtime).isoformat()
        })


def prune_old_exports(root: Path, days: int):
    cutoff = datetime.now() - timedelta(days=days)
    if not root.exists():
        return
    for item in root.iterdir():
        try:
            dt = datetime.fromtimestamp(item.stat().st_mtime)
            if dt < cutoff:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
        except Exception:
            pass


def main():
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    export_dir = EXPORT_ROOT / ts
    payload_dir = export_dir / 'payload'
    payload_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        'createdAt': datetime.now().isoformat(),
        'type': 'wis-continuity-backup',
        'retentionDays': RETENTION_DAYS,
        'entries': []
    }

    for p in INCLUDE_PATHS:
        copy_path(p, payload_dir, manifest['entries'])

    (export_dir / README_NAME).write_text(README)
    (export_dir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2))

    tar_path = BACKUP_ROOT / f'wis-backup-{ts}.tar.gz'
    tar_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path, 'w:gz') as tar:
        tar.add(export_dir, arcname=export_dir.name)

    latest = BACKUP_ROOT / 'latest.tar.gz'
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(tar_path.name)

    prune_old_exports(EXPORT_ROOT, RETENTION_DAYS)
    prune_old_exports(BACKUP_ROOT, RETENTION_DAYS)

    print(json.dumps({
        'ok': True,
        'backup': str(tar_path),
        'latest': str(latest),
        'entries': len(manifest['entries'])
    }))


if __name__ == '__main__':
    main()
