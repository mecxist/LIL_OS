# LIL OS v0.1.1 — Governance + Reset Enforcement Pack

This bundle includes:
- Governance layer docs (GOVERNANCE, CONTEXT_BUDGET, RESET_TRIGGERS, DECISION_LOG, RULE_IDS)
- Back-propagated governance hooks into core LIL OS docs
- Executable checks + CI wiring

## Quick start

Run locally:
```bash
python3 scripts/lil_os_rule_id_lint.py
python3 scripts/lil_os_reset_checks.py
```

Enable pre-commit (optional):
```bash
pip install pre-commit
pre-commit install
```

## Circuit breaker: Explanation Failure

Create the marker to force a reset:
```bash
mkdir -p .lil_os
touch .lil_os/EXPLANATION_FAILED
```

Remove it after the reset work is completed.
