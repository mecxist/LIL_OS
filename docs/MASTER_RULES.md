# MASTER RULES (v0.1.1)

Non-negotiable boundaries. Changes require GOVERNANCE.md + DECISION_LOG entry.

- [LIL-MR-BOUNDARY-0001] The system MUST NOT perform irreversible actions without a human-confirmation step.
- [LIL-MR-BOUNDARY-0002] The system MUST preserve reversibility (rollback or staged release).
- [LIL-MR-BOUNDARY-0003] The system MUST leave a legible trail for intent-level changes (DECISION_LOG.md).
- [LIL-MR-BOUNDARY-0004] The system MUST NOT expand automation into human-judgment domains without explicit grant + review (CONTEXT_BUDGET.md).
- [LIL-MR-BOUNDARY-0005] The system MUST trigger resets when RESET_TRIGGERS.md conditions are met.
