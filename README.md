# LIL OS (v0.1.1)

**A constitutional substrate for human–AI systems**

LIL OS is a governance framework that governs how goals are formed, challenged, revised, and revoked — not just how agents execute tasks. It provides operational rules that prevent silent drift, coercive optimization, and irreversible automation in AI-assisted development.

## What is LIL OS?

LIL OS is a **governance layer** for AI-assisted software development. Unlike traditional operating systems that manage resources, LIL OS manages **intent, authority, and change** in human–AI collaborative systems.

**Core Purpose:**
- Prevent silent drift — ensure system goals don't change without explicit acknowledgment
- Block coercive optimization — resist pressure to automate decisions that require human judgment
- Maintain reversibility — ensure all changes can be understood, challenged, and rolled back
- Preserve legibility — create an audit trail for all intent-level changes

## Quick Start

1. **Read the core docs:**
   - `docs/GOVERNANCE.md` — how intent-level changes work
   - `docs/CONTEXT_BUDGET.md` — why context is scarce
   - `docs/RESET_TRIGGERS.md` — when to reduce scope

2. **Run validation scripts:**
   ```bash
   python3 scripts/lil_os_rule_id_lint.py
   python3 scripts/lil_os_reset_checks.py
   ```

3. **Enable pre-commit hooks (optional):**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Key Features

- **Intent-Level Change Governance** — only changes to goals, authority, or automation require governance
- **Context Budget System** — every addition to context must justify its cost
- **Reset Triggers** — automatic circuit breakers that force scope reduction
- **Decision Logging** — audit trail of all intent-level changes
- **Rule ID System** — traceable, lintable rules with unique identifiers

## Philosophy

Built on **Liberatory Intelligence** — the principle that AI systems should liberate human agency rather than constrain it, preserve human values rather than optimize them away, and maintain human control rather than automate it out of existence.

> Governance in LIL OS is deliberate friction at points of irreversible change.

## Documentation

See `docs/` for complete documentation:
- `GOVERNANCE.md` — governance framework
- `CONTEXT_BUDGET.md` — context scarcity doctrine
- `RESET_TRIGGERS.md` — circuit breaker conditions
- `DECISION_LOG.md` — decision logging template
- `MASTER_RULES.md` — non-negotiable boundaries

## Contributing

We welcome contributions! See the [full contribution guidelines](docs/CONTRIBUTING.md) or check `docs/TODOS.md` for current work items.

**Implementation changes** (bug fixes, docs, tooling) require no governance overhead.

**Intent-level changes** (governance, rules, philosophy) must follow `docs/GOVERNANCE.md` and be logged in `docs/DECISION_LOG.md`.

## License

[Add your license here]

---

**Remember**: Governance doesn't grant permission. It preserves legibility, reversibility, and accountability. Governance is memory — not control.
