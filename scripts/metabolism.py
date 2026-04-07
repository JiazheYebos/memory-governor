#!/usr/bin/env python3
"""
Memory Governor — Metabolism Engine
Tracks which memory files are accessed, updates temperatures,
and generates health report.

Runs at SessionEnd via hook.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, timedelta

def find_memory_dir():
    for pattern in [Path.home() / ".claude" / "projects"]:
        for d in pattern.rglob("memory"):
            if (d / "MEMORY.md").exists():
                return d
    return None

def parse_accessed(text):
    """Extract accessed dates from frontmatter"""
    match = re.search(r'accessed:\s*\[([^\]]*)\]', text)
    if match:
        dates_str = match.group(1)
        return [d.strip() for d in dates_str.split(",") if d.strip()]
    return []

def calculate_temperature(dates):
    """hot/warm/cool/cold based on access frequency"""
    now = datetime.now()
    recent_14d = 0
    recent_30d = 0

    for ds in dates:
        try:
            d = datetime.strptime(ds, "%Y-%m-%d")
            delta = (now - d).days
            if delta <= 14:
                recent_14d += 1
            if delta <= 30:
                recent_30d += 1
        except:
            continue

    if recent_14d >= 3:
        return "hot"
    elif recent_14d >= 1:
        return "warm"
    elif recent_30d >= 1:
        return "cool"
    else:
        return "cold"

def run_metabolism(memory_dir):
    """Scan all memory files and calculate temperatures"""
    stats = {"hot": 0, "warm": 0, "cool": 0, "cold": 0, "untracked": 0, "critical": 0}
    report = []

    all_files = list(memory_dir.glob("*.md")) + list((memory_dir / "procedures").glob("*.md")) if (memory_dir / "procedures").exists() else list(memory_dir.glob("*.md"))

    for f in sorted(all_files):
        if f.name in ("MEMORY.md",) or f.name.startswith("."):
            continue

        text = f.read_text(encoding="utf-8")

        # Check critical
        is_critical = "critical: true" in text

        # Get temperature
        dates = parse_accessed(text)
        if dates:
            temp = calculate_temperature(dates)
            stats[temp] += 1
        else:
            temp = "untracked"
            stats["untracked"] += 1

        if is_critical:
            stats["critical"] += 1
            temp = f"{temp} 🔒"

        rel_path = f.relative_to(memory_dir) if memory_dir in f.parents else f.name
        report.append(f"  {temp:12s}  {rel_path}")

    # Print report
    print("[memory-governor] Metabolism Report")
    print(f"  🔴 Hot:       {stats['hot']}")
    print(f"  🟡 Warm:      {stats['warm']}")
    print(f"  🔵 Cool:      {stats['cool']}")
    print(f"  ⚪ Cold:      {stats['cold']}")
    print(f"  ❓ Untracked: {stats['untracked']}")
    print(f"  🔒 Critical:  {stats['critical']}")
    print()
    for line in report:
        print(line)

    # Write stats
    stats_file = memory_dir / ".metabolism_stats.json"
    stats["timestamp"] = datetime.now().isoformat()
    stats_file.write_text(json.dumps(stats, indent=2))

if __name__ == "__main__":
    memory_dir = find_memory_dir()
    if memory_dir:
        run_metabolism(memory_dir)
    else:
        print("[memory-governor] No memory directory found")
