#!/usr/bin/env python3
"""
LIL OS² Rule ID Scheme + Linter (v1)

Checks:
- Rule ID format
- Uniqueness across scanned sources
- Normative keyword presence on rule lines
- Duplicate rule text across different IDs (warn)
- Dangling references to undefined rule IDs
"""

from __future__ import annotations
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Add lil_os to path for event system
lil_os_dir = Path(__file__).parent.parent / "lil_os"
sys.path.insert(0, str(lil_os_dir.parent))

# Import shared utilities
from lil_os_utils import (
    Finding, load_simple_yaml, read_text, Colors,
    Timer, print_startup_banner, print_success_message, generate_report, save_report,
    print_os_error, format_os_finding, print_os_message, normalize_yaml_list
)

# Import event system (optional - won't break if not available)
try:
    from lil_os.events import Event, EventType, EventSeverity, get_event_bus
    EVENTS_AVAILABLE = True
except ImportError:
    EVENTS_AVAILABLE = False

def emit(findings: List[Finding]) -> int:
    hard = [f for f in findings if f.level == "HARD_FAIL"]
    warn = [f for f in findings if f.level == "WARN"]

    # Print all findings with OS-like formatting
    for f in findings:
        if f.level == "HARD_FAIL":
            print_os_error(f, include_actions=True)
        else:
            print(format_os_finding(f))
            print()

    # Summary with OS-like formatting
    if hard:
        print_os_message(f"Summary: {len(hard)} hard fail(s), {len(warn)} warning(s), {len(findings)} total finding(s).", "ERROR")
    elif warn:
        print_os_message(f"Summary: {len(warn)} warning(s), {len(findings)} total finding(s).", "WARN")
    else:
        print_os_message(f"Summary: {len(findings)} finding(s).", "INFO")
    
    return 1 if hard else 0

def iter_sources(scan_paths: List[str], exclude_paths: List[str] = None) -> List[Path]:
    exclude_set = set(Path(p).resolve() for p in (exclude_paths or []))
    out: List[Path] = []
    for p in scan_paths:
        path = Path(p)
        if path.is_file():
            if path.resolve() not in exclude_set:
                out.append(path)
        elif path.is_dir():
            for x in path.rglob("*"):
                if x.is_file() and x.suffix.lower() == ".md" and x.resolve() not in exclude_set:
                    out.append(x)
        else:
            continue
    return out

def normalize_rule_text(line: str, rule_id: str) -> str:
    s = line.replace(rule_id, "")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def main() -> int:
    timer = Timer()
    check_name = "Rule ID Lint"
    
    cfg_path = Path("lil_os.rule_id.yaml")
    if not cfg_path.exists():
        print("[HARD_FAIL] CONFIG_MISSING: lil_os.rule_id.yaml not found.")
        return 1

    cfg = load_simple_yaml(cfg_path)
    
    # Get reporting config
    reporting_config = cfg.get("reporting", {})
    show_banner = reporting_config.get("show_startup_banner", True)
    show_success = reporting_config.get("show_success_message", True)
    show_timing = reporting_config.get("show_timing", True)
    
    print_startup_banner(check_name, show_banner)
    
    scan_paths = normalize_yaml_list(cfg.get("scan_paths", ["docs", ".cursorrules"]))
    exclude_paths = normalize_yaml_list(cfg.get("exclude_paths", []))
    rule_cfg = cfg.get("rule_id", {})
    checks = cfg.get("checks", {})
    strict_sequences = bool(cfg.get("strict_sequences", False))

    pattern = rule_cfg.get("pattern")
    if not pattern:
        print("[HARD_FAIL] CONFIG_INVALID: rule_id.pattern missing.")
        return 1

    id_re = re.compile(pattern)
    require_norm = bool(rule_cfg.get("require_normative_keyword", True))
    normative = normalize_yaml_list(rule_cfg.get("normative_keywords", ["MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "MAY"]))
    normative_sorted = sorted(normative, key=len, reverse=True)

    findings: List[Finding] = []
    
    # Wrap checks in timer context
    with timer:
        sources = iter_sources(scan_paths, exclude_paths)
        defined_ids: Dict[str, dict] = {}
        normalized_text_map: Dict[str, List[str]] = {}
        all_text = ""

        for src in sources:
            text = read_text(src)
            all_text += "\n" + text

            for i, line in enumerate(text.splitlines(), start=1):
                for m in id_re.finditer(line):
                    rid = m.group(0)

                    if require_norm:
                        has_norm = any(k.lower() in line.lower() for k in normative_sorted)
                        if not has_norm:
                            findings.append(Finding(
                                "HARD_FAIL",
                                "RULE_MISSING_NORMATIVE_KEYWORD",
                                "Rule ID appears on a line without a normative keyword (MUST/SHOULD/MAY).",
                                {"rule_id": rid, "path": str(src), "line_no": i, "line": line.strip()[:240]}
                            ))

                    if checks.get("unique_ids", True):
                        if rid in defined_ids:
                            findings.append(Finding(
                                "HARD_FAIL",
                                "RULE_ID_DUPLICATE",
                                "Rule ID is defined more than once.",
                                {"rule_id": rid, "first": defined_ids[rid], "second": {"path": str(src), "line_no": i}}
                            ))
                        else:
                            defined_ids[rid] = {"path": str(src), "line_no": i, "line": line.strip()[:240]}

                    if checks.get("duplicate_rule_text", True):
                        norm = normalize_rule_text(line, rid)
                        if norm:
                            normalized_text_map.setdefault(norm, []).append(rid)

        if checks.get("duplicate_rule_text", True):
            dup_groups = [{"text": t, "ids": ids} for t, ids in normalized_text_map.items() if len(set(ids)) > 1]
            if dup_groups:
                findings.append(Finding(
                    "WARN",
                    "RULE_TEXT_DUPLICATE",
                    "Multiple rule IDs share identical/similar rule text (possible duplication or drift).",
                    {"examples": dup_groups[:20]}
                ))

        if checks.get("dangling_references", True):
            referenced = set(m.group(0) for m in id_re.finditer(all_text))
            defined = set(defined_ids.keys())
            dangling = sorted(list(referenced - defined))
            if dangling:
                findings.append(Finding(
                    "HARD_FAIL",
                    "RULE_ID_DANGLING_REFERENCE",
                    "Referenced rule IDs were not found as defined rules in scanned sources.",
                    {"dangling_ids": dangling[:200], "count": len(dangling)}
                ))

        if not defined_ids:
            findings.append(Finding(
                "WARN",
                "NO_RULE_IDS_FOUND",
                "No rule IDs were found in scanned sources; linter has nothing to validate.",
                {"scan_paths": scan_paths}
            ))
    
    # Emit findings (prints them)
    exit_code = emit(findings)
    
    # Emit event for validation run
    if EVENTS_AVAILABLE:
        try:
            event_bus = get_event_bus()
            hard_fails = [f for f in findings if f.level == "HARD_FAIL"]
            if exit_code == 0:
                event = Event(
                    type=EventType.VALIDATION_PASSED,
                    source="lil_os_rule_id_lint",
                    data={
                        "script": "lil_os_rule_id_lint",
                        "findings_count": len(findings),
                        "hard_fails": len(hard_fails),
                        "warnings": len([f for f in findings if f.level == "WARN"]),
                        "duration": timer.elapsed
                    },
                    severity=EventSeverity.INFO,
                    message=f"Rule ID lint passed: {len(findings)} finding(s)"
                )
            else:
                event = Event(
                    type=EventType.VALIDATION_FAILED,
                    source="lil_os_rule_id_lint",
                    data={
                        "script": "lil_os_rule_id_lint",
                        "exit_code": exit_code,
                        "findings_count": len(findings),
                        "hard_fails": len(hard_fails),
                        "warnings": len([f for f in findings if f.level == "WARN"]),
                        "duration": timer.elapsed
                    },
                    severity=EventSeverity.ERROR,
                    message=f"Rule ID lint failed: {len(hard_fails)} hard fail(s)"
                )
            event_bus.publish(event)
        except Exception:
            # Don't let event errors break validation
            pass
    
    # Print timing
    if show_timing and timer.elapsed > 0:
        print(f"{Colors.DIM}⏱️  Completed in {timer.format_elapsed()}{Colors.RESET}")
    
    # Generate and save report
    report = generate_report(check_name, findings, timer, cfg)
    if report:
        report_path = save_report(report, cfg)
        if report_path:
            print(f"{Colors.DIM}📄 Report saved to {report_path}{Colors.RESET}")
    
    # Print success message
    print_success_message(check_name, findings, timer, show_success)
    
    return exit_code

if __name__ == "__main__":
    raise SystemExit(main())
