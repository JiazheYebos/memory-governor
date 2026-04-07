#!/usr/bin/env python3
"""
Memory Governor — Compile Engine
Automatically generates minimal compiled context based on:
1. Procedures (always first)
2. Temperature (access frequency)
3. Intent matching (keyword scan from session topic)

Runs at SessionStart via hook. Output: memory/.compiled/context.md
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def find_memory_dir():
    """Find the memory directory"""
    for pattern in [
        Path.home() / ".claude" / "projects",
    ]:
        for d in pattern.rglob("memory"):
            if (d / "MEMORY.md").exists():
                return d
    return None

def parse_frontmatter(filepath):
    """Extract frontmatter from a markdown file"""
    try:
        text = filepath.read_text(encoding="utf-8")
    except:
        return {}, ""

    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    meta = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            # Parse lists
            if val.startswith("[") and val.endswith("]"):
                val = [x.strip().strip("'\"") for x in val[1:-1].split(",")]
            # Parse booleans
            elif val.lower() in ("true", "false"):
                val = val.lower() == "true"
            meta[key] = val

    return meta, parts[2]

def calculate_temperature(accessed_dates):
    """Calculate temperature based on access history"""
    if not accessed_dates:
        return "cold", 0.1

    now = datetime.now()
    recent_14d = 0
    recent_30d = 0

    for date_str in accessed_dates:
        try:
            d = datetime.strptime(date_str.strip(), "%Y-%m-%d")
            delta = (now - d).days
            if delta <= 14:
                recent_14d += 1
            if delta <= 30:
                recent_30d += 1
        except:
            continue

    if recent_14d >= 3:
        return "hot", 2.0
    elif recent_14d >= 1:
        return "warm", 1.0
    elif recent_30d >= 1:
        return "cool", 0.5
    else:
        return "cold", 0.1

def score_file(meta, content, intent_keywords):
    """Score a memory file's relevance"""
    score = 0.0

    # Temperature weight
    accessed = meta.get("accessed", [])
    if isinstance(accessed, str):
        accessed = [accessed]
    temp_name, temp_weight = calculate_temperature(accessed)

    # Critical files always included
    if meta.get("critical"):
        return 100.0, temp_name

    # Tag matching
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    for tag in tags:
        if tag.lower() in intent_keywords:
            score += 2.0

    # Filename/name matching
    name = meta.get("name", "")
    for kw in intent_keywords:
        if kw in name.lower():
            score += 1.0

    # Content keyword matching (lightweight — first 500 chars)
    preview = content[:500].lower()
    for kw in intent_keywords:
        if kw in preview:
            score += 0.5

    # Apply temperature weight
    score *= temp_weight

    # State files always get a boost
    if "state" in name.lower() or "current" in name.lower():
        score += 3.0

    return score, temp_name

def extract_links(content):
    """Extract [[links]] from content"""
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def compile_context(memory_dir, session_topic=""):
    """Main compile function"""
    compiled_dir = memory_dir / ".compiled"
    compiled_dir.mkdir(exist_ok=True)

    procedures_dir = memory_dir / "procedures"

    # Extract intent keywords from session topic
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "to", "of", "in", "for", "on", "with", "at", "by", "this", "that", "it", "do", "does", "did", "will", "would", "can", "could", "should", "may", "might", "shall"}
    intent_keywords = set()
    if session_topic:
        words = re.findall(r'[a-zA-Z\u4e00-\u9fff]+', session_topic.lower())
        intent_keywords = {w for w in words if w not in stop_words and len(w) > 2}

    output_sections = []
    included_files = set()

    # === Phase 1: Procedures (ALWAYS FIRST) ===
    procedures = []
    if procedures_dir.exists():
        for f in sorted(procedures_dir.glob("*.md")):
            meta, content = parse_frontmatter(f)
            if meta.get("proven"):
                # If we have intent, only include matching procedures
                if intent_keywords:
                    tags = meta.get("tags", [])
                    if isinstance(tags, str):
                        tags = [tags]
                    if any(t.lower() in intent_keywords for t in tags) or meta.get("critical"):
                        procedures.append((f.name, meta, content))
                        included_files.add(f.name)
                else:
                    # No intent specified — include critical procedures only
                    if meta.get("critical"):
                        procedures.append((f.name, meta, content))
                        included_files.add(f.name)

    if procedures:
        output_sections.append("## Proven Methods (use these directly, do NOT explore alternatives)\n")
        for name, meta, content in procedures:
            # Extract just the working solution section
            lines = content.strip().split("\n")
            title = meta.get("name", name)
            working = []
            in_working = False
            for line in lines:
                if "## Working Solution" in line or "## Working" in line:
                    in_working = True
                    continue
                elif line.startswith("## ") and in_working:
                    break
                elif in_working:
                    working.append(line)

            if working:
                output_sections.append(f"### {title}")
                output_sections.append("\n".join(working[:10]))  # Max 10 lines
                output_sections.append("")

    # === Phase 2: Score and rank memory files ===
    scored_files = []
    for f in sorted(memory_dir.glob("*.md")):
        if f.name == "MEMORY.md" or f.name.startswith("."):
            continue
        meta, content = parse_frontmatter(f)
        score, temp = score_file(meta, content, intent_keywords)
        if score > 0:
            scored_files.append((score, temp, f, meta, content))

    scored_files.sort(key=lambda x: x[0], reverse=True)

    # Take top N files (budget: ~1500 tokens ≈ 4500 chars)
    char_budget = 4500
    char_used = sum(len(s) for s in output_sections)

    relevant_sections = []
    for score, temp, f, meta, content in scored_files:
        if f.name in included_files:
            continue
        if char_used > char_budget:
            break

        # Extract first meaningful paragraph
        lines = content.strip().split("\n")
        summary_lines = []
        for line in lines:
            if line.strip() and not line.startswith("#"):
                summary_lines.append(line.strip())
                if len(summary_lines) >= 3:
                    break

        if summary_lines:
            name = meta.get("name", f.stem)
            entry = f"- **{name}** [{temp}]: {' '.join(summary_lines)}"
            if len(entry) > 200:
                entry = entry[:200] + "..."
            relevant_sections.append(entry)
            char_used += len(entry)
            included_files.add(f.name)

            # Follow links
            for link in extract_links(content):
                linked_file = memory_dir / f"{link}.md"
                if not linked_file.exists():
                    # Try fuzzy match
                    matches = list(memory_dir.glob(f"*{link}*"))
                    if matches:
                        linked_file = matches[0]

                if linked_file.exists() and linked_file.name not in included_files:
                    lmeta, lcontent = parse_frontmatter(linked_file)
                    lsummary = lcontent.strip().split("\n")[0][:150]
                    relevant_sections.append(f"- **{link}** [linked]: {lsummary}")
                    included_files.add(linked_file.name)

    if relevant_sections:
        output_sections.append("## Relevant Knowledge\n")
        output_sections.extend(relevant_sections)

    # === Phase 3: Global memory ===
    global_dir = Path.home() / ".claude" / "global-memory"
    if global_dir.exists():
        for f in global_dir.glob("*.md"):
            if f.stat().st_size < 500:  # Only small global files
                meta, content = parse_frontmatter(f)
                output_sections.append(f"\n## Global: {f.stem}")
                output_sections.append(content.strip()[:300])

    # === Write compiled output ===
    compiled_output = "\n".join(output_sections)
    output_file = compiled_dir / "context.md"
    output_file.write_text(f"<!-- Compiled by memory-governor at {datetime.now().strftime('%Y-%m-%d %H:%M')} -->\n\n{compiled_output}\n")

    # Stats
    token_estimate = len(compiled_output) // 3
    print(f"[memory-governor] Compiled {len(included_files)} files → {len(compiled_output)} chars (~{token_estimate} tokens)")

    return str(output_file)

def record_access(memory_dir, accessed_files):
    """Record which files were accessed during a session"""
    today = datetime.now().strftime("%Y-%m-%d")

    for filename in accessed_files:
        filepath = memory_dir / filename
        if not filepath.exists():
            continue

        text = filepath.read_text(encoding="utf-8")

        if "accessed:" in text:
            # Update existing accessed list
            match = re.search(r'accessed:\s*\[([^\]]*)\]', text)
            if match:
                existing = match.group(1)
                if today not in existing:
                    new_accessed = f"accessed: [{existing}, {today}]" if existing else f"accessed: [{today}]"
                    text = text.replace(f"accessed: [{existing}]", new_accessed)
        else:
            # Add accessed field after frontmatter start
            if text.startswith("---"):
                text = text.replace("---\n", f"---\naccessed: [{today}]\n", 1)

        filepath.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    memory_dir = find_memory_dir()
    if not memory_dir:
        print("[memory-governor] No memory directory found")
        sys.exit(0)

    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    compile_context(memory_dir, topic)
