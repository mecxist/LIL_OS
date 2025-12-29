# Governance Hooks by Domain (v0.1.1)

This document consolidates domain-specific governance hooks that apply when working in different areas of a system. These hooks ensure that changes in each domain respect LIL OS governance principles.

## API

- Breaking API changes are intent-level changes.
- Side-effecting external calls MUST respect MASTER_RULES.md and CONTEXT_BUDGET.md.

## Architecture

- Architecture changes that alter authority, irreversibility, or data access are intent-level and MUST be logged.
- Override normalization triggers RESET_TRIGGERS.md.

## Authentication & Authorization

- Permission changes are intent-level and MUST be justified + logged.

## Data

- Data retention affects Memory Budget (CONTEXT_BUDGET.md).
- Silent memory growth triggers RESET_TRIGGERS.md.

## Performance

- Performance optimization MUST NOT override MASTER_RULES.md.
- Metric dominance triggers RESET_TRIGGERS.md.

## Quality

- Repeated failures without clear cause MUST trigger RESET_TRIGGERS.md → Context Reset.
- Quality optimization MUST NOT override MASTER_RULES.md.

## Systems

- Changes to system boundaries are intent-level changes and MUST follow GOVERNANCE.md + DECISION_LOG.md.
- Boundary shifts that increase agent autonomy MUST re-check CONTEXT_BUDGET.md and pass reset checks.

