#!/usr/bin/env python3
"""
LIL OS Rule ID Scheme + Linter (v1)

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

# Import shared utilities
from lil_os_utils import Finding, load_simple_yaml, read_text

def emit(findings: List[Finding]) -> int:
    hard = [f for f in findings if f.level == "HARD_FAIL"]
    warn = [f for f in findings if f.level == "WARN"]

    for f in findings:
        print(f"[{f.level}] {f.code}: {f.message}")
        if f.details:
            print("  details:", json.dumps(f.details, indent=2))

    print("\nSummary:", f"{len(hard)} hard fail(s), {len(warn)} warning(s), {len(findings)} total finding(s).")
    return 1 if hard else 0

def iter_sources(scan_paths: List[str]) -> List[Path]:
    out: List[Path] = []
    for p in scan_paths:
        path = Path(p)
        if path.is_file():
            out.append(path)
        elif path.is_dir():
            out.extend([x for x in path.rglob("*") if x.is_file() and x.suffix.lower() == ".md"])
        else:
            continue
    return out

def normalize_rule_text(line: str, rule_id: str) -> str:
    s = line.replace(rule_id, "")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def main() -> int:
    cfg_path = Path("lil_os.rule_id.yaml")
    if not cfg_path.exists():
        print("[HARD_FAIL] CONFIG_MISSING: lil_os.rule_id.yaml not found.")
        return 1

    cfg = load_simple_yaml(cfg_path)
    scan_paths = cfg.get("scan_paths", ["docs", ".cursorrules"])
    rule_cfg = cfg.get("rule_id", {})
    checks = cfg.get("checks", {})
    strict_sequences = bool(cfg.get("strict_sequences", False))

    pattern = rule_cfg.get("pattern")
    if not pattern:
        print("[HARD_FAIL] CONFIG_INVALID: rule_id.pattern missing.")
        return 1

    id_re = re.compile(pattern)
    require_norm = bool(rule_cfg.get("require_normative_keyword", True))
    normative = rule_cfg.get("normative_keywords", ["MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "MAY"])
    normative_sorted = sorted(normative, key=len, reverse=True)

    sources = iter_sources(scan_paths)

    findings: List[Finding] = []
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

    return emit(findings)

if __name__ == "__main__":
    raise SystemExit(main())
