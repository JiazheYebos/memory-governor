#!/usr/bin/env python3
"""
Memory Governor — Backup Engine
Creates timestamped backup of entire memory directory.
MUST run before any optimize/compact operation.
"""

import shutil
from pathlib import Path
from datetime import datetime

def find_memory_dir():
    for pattern in [Path.home() / ".claude" / "projects"]:
        for d in pattern.rglob("memory"):
            if (d / "MEMORY.md").exists():
                return d
    return None

def create_backup(memory_dir):
    backup_root = memory_dir / ".backup"
    backup_root.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = backup_root / timestamp

    # Copy everything except .backup and .compiled
    def ignore(dir, files):
        return [f for f in files if f in ('.backup', '.compiled', '.metabolism_stats.json')]

    shutil.copytree(memory_dir, backup_dir, ignore=ignore)

    file_count = sum(1 for _ in backup_dir.rglob("*.md"))
    total_kb = sum(f.stat().st_size for f in backup_dir.rglob("*") if f.is_file()) // 1024

    print(f"[memory-governor] Backup created: {backup_dir}")
    print(f"  Files: {file_count}, Size: {total_kb}KB")

    # Keep only last 5 backups
    backups = sorted(backup_root.iterdir())
    while len(backups) > 5:
        old = backups.pop(0)
        shutil.rmtree(old)
        print(f"  Pruned old backup: {old.name}")

    return str(backup_dir)

if __name__ == "__main__":
    memory_dir = find_memory_dir()
    if memory_dir:
        create_backup(memory_dir)
    else:
        print("[memory-governor] No memory directory found")
