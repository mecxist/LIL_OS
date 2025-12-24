# LIL OS Governance (v1.0)

## Purpose
LIL OS governance defines how the system is allowed to change over time.

It is not democratic, token-based, or committee-driven. Governance in LIL OS is **operational**: self-binding rules that constrain how goals, authority, and automation evolve.

Governance exists to prevent:
- silent drift
- coercive optimization
- irreversible automation
- future self-betrayal under pressure

## Core Principle
> Governance in LIL OS is deliberate friction at points of irreversible change.

Speed, optimization, and automation are permitted. Unexamined transformation is not.

## Scope of Governance
Governance applies only to **intent-level changes** — changes that alter meaning, authority, or direction.

This includes:
- changes to system goals or success metrics
- modifications to agent identity, scope, or autonomy
- adding or removing agents
- changes to `.cursorrules` or system-level prompts
- automating decisions previously requiring human judgment
- modifying MASTER_RULES, CONTEXT_BUDGET, RULE_IDS, or RESET_TRIGGERS

Implementation changes (bug fixes, refactors, formatting) are out of scope.

## Decision Authority (Solo-Builder Default)
- Builder is sovereign.
- Builder is accountable via traceability.
- No approval required; justification required.

## Justification Requirement
All intent-level changes MUST include a rationale answering:
1. Why now?
2. Who benefits?
3. What tradeoff/risk is accepted?
4. What alternatives were rejected?

If you can’t answer clearly, delay the change.

## Temporal Legitimacy Test
Ask:
> Would this explanation still make sense in six months, under worse conditions?

If no, the system SHOULD resist the change.

## Override Conditions
Emergency overrides are permitted only when:
- security/safety is at immediate risk, or
- legal compliance requires action, or
- credible human harm is imminent.

All overrides MUST be logged retroactively in DECISION_LOG.md.

## Governance Philosophy
Governance doesn’t grant permission. It preserves legibility, reversibility, and accountability.

Governance is memory — not control.
