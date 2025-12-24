#!/usr/bin/env python3
"""
LIL OS Reset Triggers — Executable Checks (v1)

Runs checks corresponding to docs/RESET_TRIGGERS.md and exits non-zero on HARD failures.
Designed for CI, pre-commit, or agent tool execution.

Dependencies: Python 3.10+ (standard library only)
"""

from __future__ import annotations

import re
import sys
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Optional

# ----------------------------
# Tiny YAML loader (subset)
# ----------------------------
def load_simple_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = [ln.rstrip("\n") for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    root: dict = {}
    stack: List[Tuple[int, dict | list]] = [(0, root)]
    current_key_stack: List[Optional[str]] = [None]

    def parse_value(v: str):
        v = v.strip()
        if v.isdigit():
            return int(v)
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            return v[1:-1]
        return v

    for ln in lines:
        indent = len(ln) - len(ln.lstrip(" "))
        ln = ln.lstrip(" ")
        while stack and indent < stack[-1][0]:
            stack.pop()
            current_key_stack.pop()

        container = stack[-1][1]

        if ln.startswith("- "):
            item = parse_value(ln[2:])
            if not isinstance(container, list):
                key = current_key_stack[-1]
                if key is None or not isinstance(container, dict):
                    raise ValueError(f"List item without list context near: {ln}")
                if key not in container or not isinstance(container[key], list):
                    container[key] = []
                container = container[key]
                stack.append((indent, container))
                current_key_stack.append(key)
            container.append(item)
            continue

        if ":" in ln:
            key, rest = ln.split(":", 1)
            key = key.strip()
            rest = rest.strip()
            if isinstance(container, list):
                raise ValueError(f"Unexpected mapping inside list near: {ln}")
            if rest == "":
                container[key] = {}
                stack.append((indent + 2, container[key]))
                current_key_stack.append(key)
            else:
                container[key] = parse_value(rest)
                current_key_stack[-1] = key
            continue

        raise ValueError(f"Unparseable line: {ln}")

    return root

# ----------------------------
# Reporting
# ----------------------------
@dataclass
class Finding:
    level: str  # HARD_FAIL | WARN | INFO
    code: str
    message: str
    details: Optional[dict] = None

def print_findings(findings: List[Finding]) -> int:
    hard = [f for f in findings if f.level == "HARD_FAIL"]
    warn = [f for f in findings if f.level == "WARN"]

    def emit(f: Finding):
        print(f"[{f.level}] {f.code}: {f.message}")
        if f.details:
            print("  details:", json.dumps(f.details, indent=2))

    for f in findings:
        emit(f)

    print("\nSummary:", f"{len(hard)} hard fail(s), {len(warn)} warning(s), {len(findings)} total finding(s).")
    return 1 if hard else 0

# ----------------------------
# Helpers
# ----------------------------
def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")

def git_available() -> bool:
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True, text=True)
        return True
    except Exception:
        return False

def git_changed_lines_since(days: int) -> Tuple[int, int]:
    if not git_available():
        return (0, 0)
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    cmd = ["git", "log", f"--since={since}", "--numstat", "--pretty=format:"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return (0, 0)

    added = deleted = 0
    for ln in res.stdout.splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            added += int(parts[0])
            deleted += int(parts[1])
    return (added, deleted)

def count_rules_in_text(text: str) -> int:
    bullets = len(re.findall(r"^\s*[-*]\s+\S+", text, flags=re.MULTILINE))
    musts = len(re.findall(r"\b(MUST NOT|MUST|SHALL NOT|SHALL)\b", text))
    return bullets + musts

def parse_decision_log_entries(text: str) -> List[str]:
    # Skip metadata sections - only parse entries after "Entries" section or entries with actual field values
    skip_sections = {"purpose", "what belongs here", "required fields", "template", "entries"}
    
    parts = re.split(r"(?m)^\s*#{2,6}\s+", text)
    if len(parts) > 1:
        entries = []
        in_entries_section = False
        for p in parts[1:]:
            p = p.strip()
            if not p:
                continue
            # Check if this is the "Entries" section marker
            first_line = p.split('\n')[0].strip().lower()
            if "entries" in first_line:
                in_entries_section = True
                continue
            # Skip known metadata sections
            if first_line in skip_sections:
                continue
            # Only include entries that have actual field values (not just headers)
            # An entry should have at least "Date:" and "Decision:" fields
            if "Date:" in p and "Decision:" in p:
                entries.append(p)
            elif in_entries_section:
                # If we're in entries section, include it even if format is slightly off
                entries.append(p)
        return entries
    return [p.strip() for p in re.split(r"\n-{3,}\n", text) if p.strip() and "Date:" in p and "Decision:" in p]

def entry_missing_fields(entry: str, required_fields: List[str]) -> List[str]:
    missing = []
    for field in required_fields:
        if field.lower().startswith("review date"):
            # review date optional in v1 checks; treat absence as warning only
            continue
        if field.lower() not in entry.lower():
            missing.append(field)
    return missing

# ----------------------------
# Checks
# ----------------------------
def check_justification_decay(decision_log: Path, required_fields: List[str], incomplete_threshold: int, rolling_entries: int) -> List[Finding]:
    findings: List[Finding] = []
    text = read_text(decision_log)
    if not text:
        return [Finding("WARN", "DECISION_LOG_MISSING", "Decision log not found or empty.", {"path": str(decision_log)})]

    entries = parse_decision_log_entries(text)[:rolling_entries]
    incomplete = []
    for idx, entry in enumerate(entries, start=1):
        missing = entry_missing_fields(entry, required_fields)
        if missing:
            incomplete.append({"entry_index": idx, "missing": missing})

    if len(incomplete) >= incomplete_threshold:
        findings.append(Finding(
            "HARD_FAIL",
            "DRIFT_JUSTIFICATION_DECAY",
            f"{len(incomplete)} decision log entry(ies) missing required fields (threshold {incomplete_threshold}).",
            {"incomplete": incomplete[:20], "checked_entries": len(entries)}
        ))
    elif incomplete:
        findings.append(Finding(
            "WARN",
            "DRIFT_JUSTIFICATION_DECAY_WARN",
            f"{len(incomplete)} decision log entry(ies) missing required fields.",
            {"incomplete": incomplete[:20], "checked_entries": len(entries)}
        ))
    return findings

def check_context_budget_overflow(rule_files: List[Path], agents_dir: Path, memory_dir: Path, max_rules: int, max_agents: int, max_memory: int) -> List[Finding]:
    findings: List[Finding] = []
    combined = "\n\n".join([read_text(p) for p in rule_files if p.exists()])
    rule_count = count_rules_in_text(combined)

    agent_count = len([p for p in agents_dir.rglob("*") if p.is_file()]) if agents_dir.exists() else 0
    mem_count = len([p for p in memory_dir.rglob("*") if p.is_file()]) if memory_dir.exists() else 0

    if rule_count > max_rules:
        findings.append(Finding("HARD_FAIL", "LOAD_CONTEXT_BUDGET_RULES", f"Rule budget exceeded: {rule_count} > {max_rules}.",
                                {"rule_count": rule_count, "max_rules": max_rules}))
    if agent_count > max_agents:
        findings.append(Finding("HARD_FAIL", "LOAD_CONTEXT_BUDGET_AGENTS", f"Agent budget exceeded: {agent_count} > {max_agents}.",
                                {"agent_files": agent_count, "max_agents": max_agents}))
    if mem_count > max_memory:
        findings.append(Finding("HARD_FAIL", "LOAD_CONTEXT_BUDGET_MEMORY", f"Memory artifact budget exceeded: {mem_count} > {max_memory}.",
                                {"memory_files": mem_count, "max_memory_artifacts": max_memory}))

    if not findings:
        findings.append(Finding("INFO", "LOAD_CONTEXT_BUDGET_OK", "Context budgets within limits.",
                                {"rule_count": rule_count, "agent_files": agent_count, "memory_files": mem_count}))
    return findings

def check_silent_memory_growth(memory_dir: Path, required_meta: List[str]) -> List[Finding]:
    findings: List[Finding] = []
    if not memory_dir.exists():
        return [Finding("INFO", "MEMORY_DIR_MISSING", "Memory directory not present; skipping memory metadata checks.", {"path": str(memory_dir)})]

    offenders = []
    for p in [x for x in memory_dir.rglob("*") if x.is_file()]:
        txt = read_text(p)
        missing = [k for k in required_meta if k.lower() not in txt.lower()]
        if missing:
            offenders.append({"path": str(p), "missing": missing})

    if offenders:
        findings.append(Finding("HARD_FAIL", "LOAD_SILENT_MEMORY_GROWTH", "Memory artifacts missing required metadata.",
                                {"offenders": offenders[:50], "count": len(offenders)}))
    else:
        findings.append(Finding("INFO", "LOAD_MEMORY_METADATA_OK", "All memory artifacts include required metadata."))
    return findings

def check_rule_accretion_velocity(days: int) -> List[Finding]:
    added, deleted = git_changed_lines_since(days)
    if added > deleted:
        return [Finding("WARN", "DRIFT_RULE_ACCRETION_WINDOW",
                        f"Net additions over last {days} days (proxy for rule accretion).",
                        {"added_lines": added, "deleted_lines": deleted, "window_days": days})]
    return [Finding("INFO", "DRIFT_RULE_ACCRETION_OK", f"No net additions over last {days} days.", {"added_lines": added, "deleted_lines": deleted})]

def check_override_normalization(decision_log: Path, override_markers: List[str], per_window_threshold: int) -> List[Finding]:
    text = read_text(decision_log)
    if not text:
        return []
    entries = parse_decision_log_entries(text)
    override_entries = []
    for idx, entry in enumerate(entries, start=1):
        if any(m.lower() in entry.lower() for m in override_markers):
            override_entries.append(idx)

    if len(override_entries) >= per_window_threshold:
        return [Finding("HARD_FAIL", "LEGIT_OVERRIDE_NORMALIZATION",
                        f"Override normalization detected: {len(override_entries)} override-tagged entries (threshold {per_window_threshold}).",
                        {"override_entry_indices": override_entries[:50], "count": len(override_entries)})]
    if override_entries:
        return [Finding("WARN", "LEGIT_OVERRIDE_PRESENT", f"Override usage present: {len(override_entries)} entry(ies).",
                        {"override_entry_indices": override_entries[:50]})]
    return [Finding("INFO", "LEGIT_OVERRIDE_OK", "No override-tagged decisions detected.")]

def check_metric_dominance(decision_log: Path, metric_markers: List[str], consecutive_threshold: int) -> List[Finding]:
    text = read_text(decision_log)
    if not text:
        return []
    entries = parse_decision_log_entries(text)
    streak = 0
    streak_indices = []
    for idx, entry in enumerate(entries, start=1):
        if any(m.lower() in entry.lower() for m in metric_markers):
            streak += 1
            streak_indices.append(idx)
            if streak >= consecutive_threshold:
                return [Finding("HARD_FAIL", "LEGIT_METRIC_DOMINANCE",
                                f"Metric dominance heuristic: {streak} consecutive decisions reference a metric (threshold {consecutive_threshold}).",
                                {"streak_entry_indices": streak_indices[-consecutive_threshold:]})]
        else:
            streak = 0
            streak_indices = []
    if streak > 0:
        return [Finding("WARN", "LEGIT_METRIC_DOMINANCE_WARN", enabling := f"Metric references detected in recent decisions (streak {streak}).",
                        {"current_streak": streak, "streak_entry_indices": streak_indices})]
    return [Finding("INFO", "LEGIT_METRIC_OK", "No metric dominance streak detected.")]

def check_explanation_failure_marker() -> List[Finding]:
    marker = Path(".lil_os/EXPLANATION_FAILED")
    if marker.exists():
        return [Finding("HARD_FAIL", "LEGIT_EXPLANATION_FAILURE",
                        "Explanation failure marker present. Reduce scope and reassert MASTER_RULES before proceeding.",
                        {"marker": str(marker)})]
    return [Finding("INFO", "LEGIT_EXPLANATION_OK", "No explanation failure marker present.")]

def main() -> int:
    cfg_path = Path("lil_os.reset_checks.yaml")
    if not cfg_path.exists():
        print("[HARD_FAIL] CONFIG_MISSING: lil_os.reset_checks.yaml not found.")
        return 1

    cfg = load_simple_yaml(cfg_path)
    paths = cfg.get("paths", {})
    windows = cfg.get("windows", {})
    thresholds = cfg.get("thresholds", {})
    conventions = cfg.get("conventions", {})

    master_rules = Path(paths.get("master_rules", "docs/MASTER_RULES.md"))
    governance = Path(paths.get("governance", "docs/GOVERNANCE.md"))
    context_budget = Path(paths.get("context_budget", "docs/CONTEXT_BUDGET.md"))
    cursor_rules = Path(paths.get("cursor_rules", ".cursorrules"))
    decision_log = Path(paths.get("decision_log", "docs/DECISION_LOG.md"))
    agents_dir = Path(paths.get("agents_dir", "agents"))
    memory_dir = Path(paths.get("memory_dir", "memory"))

    findings: List[Finding] = []
    findings += check_rule_accretion_velocity(int(windows.get("rule_velocity_days", 30)))
    findings += check_justification_decay(
        decision_log=decision_log,
        required_fields=conventions.get("decision_log_required_fields", []),
        incomplete_threshold=int(thresholds.get("justification_decay_incomplete_entries", 2)),
        rolling_entries=int(windows.get("decision_log_rolling_entries", 20)),
    )
    findings += check_context_budget_overflow(
        rule_files=[master_rules, governance, context_budget, cursor_rules],
        agents_dir=agents_dir,
        memory_dir=memory_dir,
        max_rules=int(thresholds.get("max_rules", 120)),
        max_agents=int(thresholds.get("max_agents", 8)),
        max_memory=int(thresholds.get("max_memory_artifacts", 200)),
    )
    findings += check_silent_memory_growth(
        memory_dir=memory_dir,
        required_meta=conventions.get("memory_required_metadata", []),
    )
    findings += check_override_normalization(
        decision_log=decision_log,
        override_markers=conventions.get("override_markers", []),
        per_window_threshold=int(thresholds.get("override_normalization_per_window", 2)),
    )
    findings += check_metric_dominance(
        decision_log=decision_log,
        metric_markers=conventions.get("metric_markers", []),
        consecutive_threshold=int(thresholds.get("metric_dominance_consecutive_decisions", 3)),
    )
    findings += check_explanation_failure_marker()

    # Print
    hard = [f for f in findings if f.level == "HARD_FAIL"]
    warn = [f for f in findings if f.level == "WARN"]

    for f in findings:
        print(f"[{f.level}] {f.code}: {f.message}")
        if f.details:
            print("  details:", json.dumps(f.details, indent=2))

    print("\nSummary:", f"{len(hard)} hard fail(s), {len(warn)} warning(s), {len(findings)} total finding(s).")
    return 1 if hard else 0

if __name__ == "__main__":
    raise SystemExit(main())
