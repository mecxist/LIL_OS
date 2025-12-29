# Reset Triggers (v1.0)

## Purpose
Defines conditions under which LIL OS MUST pause, reduce scope, or reassert constraints to preserve legitimacy, clarity, and human agency.

Resets are protective circuit breakers.

## Reset Doctrine
> When a system can no longer explain itself clearly, it must reduce complexity before proceeding.

## Reset Classes
1. Drift Resets — meaning erosion and rule conflict
2. Load Resets — context and automation overload
3. Legitimacy Resets — misuse of power or coercive optimization

Triggers are observable signals, not intuition.

---

## Drift Resets

### Rule Contradiction
- Trigger: active rules conflict, or new rule requires multiple exceptions
- Detection: scan MASTER_RULES/GOVERNANCE/CONTEXT_BUDGET/.cursorrules
- Threshold: any unresolvable contradiction
- Action: freeze new rules; prune/consolidate; log in DECISION_LOG

### Rule Accretion Velocity
- Trigger: rules added faster than removed
- Detection: additions vs deletions over 30 days
- Threshold: net additions for 2 consecutive windows
- Action: mandatory rule audit; reduce rule count before expansion

### Justification Decay
- Trigger: intent-level decisions missing full justification
- Detection: DECISION_LOG missing Tradeoffs / rejected alternatives
- Threshold: 2+ incomplete entries (rolling window)
- Action: pause intent-level changes; backfill; resume after clarity restored

---

## Load Resets

### Context Budget Overflow
- Trigger: budgets exceeded
- Detection: active rules, agent count, memory artifacts
- Threshold: any ceiling exceeded
- Action: reduce scope; block expansion until under budget

### Automation Creep
- Trigger: automation expands into human-judgment domains
- Detection: compare automation scope to CONTEXT_BUDGET forbidden list
- Threshold: any violation
- Action: roll back automation; reinstate human-in-loop; require justification + review date

### Silent Memory Growth
- Trigger: persistent memory without metadata
- Detection: memory artifacts missing Purpose/Retention/Review Trigger
- Threshold: any violation
- Action: disable persistence; audit; re-enable selectively

---

## Legitimacy Resets

### Metric Dominance
- Trigger: single metric repeatedly overrides tradeoffs
- Detection: Decision log shows repeated optimization for same metric
- Threshold: 3 consecutive metric-optimized decisions
- Action: suspend metric optimization; run legitimacy review (benefit/harm/alternatives)

### Override Normalization
- Trigger: emergency overrides become routine
- Detection: count override-tagged entries
- Threshold: 2+ overrides in 30 days
- Action: freeze overrides; require structural/workflow change

### Explanation Failure
- Trigger: builder cannot produce coherent explanation of system behavior
- Detection: explicit failure marker (.lil_os/EXPLANATION_FAILED)
- Threshold: single failure
- Action: halt expansion; reduce scope; reassert MASTER_RULES; resume only after explanation restored

---

## Reset Requirements
All resets MUST:
- be logged in DECISION_LOG.md
- reduce scope before re-expansion
- preserve reversibility
- protect human agency

---

## Implementation Status

This section shows which reset triggers are currently implemented in `scripts/lil_os_reset_checks.py` vs. documented above.

### Implemented Triggers ✅

- **Rule Accretion Velocity** - Detects when rules are added faster than removed over 30-day windows
- **Justification Decay** - Checks decision log entries for missing required fields (Tradeoffs, rejected alternatives)
- **Context Budget Overflow** - Validates against max rules, agents, and memory artifact limits
- **Silent Memory Growth** - Checks memory artifacts for required metadata (Purpose, Retention, Review Trigger)
- **Automation Creep** - Detects when automation expands into human-judgment domains by scanning decision logs for automation keywords and forbidden domains from CONTEXT_BUDGET.md
- **Rule Contradiction** - Detects conflicting rules using pattern-based analysis. Identifies direct contradictions (MUST NOT vs MUST for same subject), soft contradictions (SHOULD NOT vs SHOULD), and explicit contradiction markers
- **Override Normalization** - Detects when emergency overrides become routine (2+ in 30 days)
- **Metric Dominance** - Identifies when single metric repeatedly overrides tradeoffs (3 consecutive decisions)
- **Explanation Failure** - Checks for `.lil_os/EXPLANATION_FAILED` marker file

### Documented but Not Yet Implemented ⚠️

- **Rule Contradiction (Enhanced)** - Basic pattern-based detection implemented. Enhanced semantic analysis using NLP planned for v0.3.0 to detect subtle contradictions that pattern matching may miss.

### Notes

- All implemented triggers run automatically via pre-commit hooks and CI/CD
- Non-implemented triggers should be manually reviewed until implemented
- See `RELEASE_ASSESSMENT.md` for detailed analysis of implementation gaps
