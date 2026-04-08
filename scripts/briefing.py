#!/usr/bin/env python3
"""
Memory Governor — Briefing Engine
Generates a human-readable status summary at session start.
Reads state_current.md + recent governance alerts.

Output: printed to stdout (shown in session start hook output)
"""

import os
from pathlib import Path
from datetime import datetime

def find_memory_dir():
    for pattern in [Path.home() / ".claude" / "projects"]:
        for d in pattern.rglob("memory"):
            if (d / "MEMORY.md").exists():
                return d
    return None

def generate_briefing(memory_dir):
    """Generate human-readable briefing"""

    lines = []
    lines.append("📋 Session Briefing")
    lines.append(f"   {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # Read state file
    state_file = memory_dir / "state_current.md"
    if state_file.exists():
        text = state_file.read_text(encoding="utf-8")

        # Extract urgent/blocked items
        urgent = []
        in_progress = []
        in_section = None

        for line in text.split("\n"):
            if "紧急" in line or "阻塞" in line or "Urgent" in line or "Blocked" in line:
                in_section = "urgent"
            elif "进行中" in line or "In Progress" in line or "In progress" in line:
                in_section = "progress"
            elif "已完成" in line or "Completed" in line or "完成" in line:
                in_section = None
            elif "待办" in line or "TODO" in line:
                in_section = "todo"
            elif line.startswith("##"):
                in_section = None

            if in_section == "urgent" and line.strip().startswith("- "):
                urgent.append(line.strip())
            elif in_section == "progress" and line.strip().startswith("- "):
                in_progress.append(line.strip())

        if urgent:
            lines.append("🚨 Blocked/Urgent:")
            for item in urgent[:5]:
                lines.append(f"  {item}")
            lines.append("")

        if in_progress:
            lines.append("🔄 In Progress:")
            for item in in_progress[:5]:
                lines.append(f"  {item}")
            lines.append("")
    else:
        lines.append("ℹ️  No state file found. Create memory/state_current.md to enable briefing.")
        lines.append("")

    # Check alerts
    alert_log = memory_dir / "governance_alerts.log"
    if alert_log.exists() and alert_log.stat().st_size > 0:
        lines.append("⚠️ Memory Governance Alerts:")
        for line in alert_log.read_text().strip().split("\n")[-3:]:  # Last 3 alerts
            lines.append(f"  {line}")
        lines.append("")

    # Check how many procedures exist
    proc_dir = memory_dir / "procedures"
    if proc_dir.exists():
        proc_count = len(list(proc_dir.glob("*.md")))
        lines.append(f"📚 {proc_count} proven procedures available")

    return "\n".join(lines)

if __name__ == "__main__":
    memory_dir = find_memory_dir()
    if memory_dir:
        print(generate_briefing(memory_dir))
    else:
        print("[memory-governor] No memory directory found")
