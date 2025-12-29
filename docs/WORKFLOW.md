# WORKFLOW (v0.1.1)

## Governance Hooks
Intent-level changes MUST:
- include justification (GOVERNANCE.md)
- create/update a DECISION_LOG entry
- pass:
  - scripts/lil_os_rule_id_lint.py
  - scripts/lil_os_reset_checks.py
- honor RESET_TRIGGERS.md (reduce scope before proceeding if triggered)

## Standard Flow
1) Plan (TODOS.md)
2) Implement
3) Evaluate (GOVERNANCE_HOOKS.md - Quality section)
4) Log intent changes (DECISION_LOG.md)
5) Ship with rollback plan (MASTER_RULES.md)
