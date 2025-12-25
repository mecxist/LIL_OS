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

## Who is LIL OS For?

LIL OS is designed for:

- **Solo builders** who want to maintain control and prevent their AI assistants from making unauthorized changes to system goals
- **Teams** building AI-powered tools who need governance without bureaucracy
- **Organizations** that need to prevent AI systems from optimizing themselves into dangerous or unintended states
- **Anyone** building systems where AI has significant autonomy and you need to ensure it doesn't drift from original intent
- **Developers who don't know what they don't know** — LIL OS helps you discover when your AI system is making decisions you didn't realize needed human judgment

LIL OS is **not** for:
- Simple automation scripts
- Systems where AI has no autonomy
- Projects that don't need governance or change management

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

LIL OS gives you practical tools to keep your AI-assisted projects under control. Here's what you get:

### Rules Management
**Every rule has a unique ID** (like `LIL-CR-PROCESS-0001`) so you can track where rules come from, find them quickly, and see when they change. No more hunting through documentation to figure out what rule applies where.

### Governance Without Bureaucracy
**Only important changes need governance** — changes to goals, who has authority, or what can be automated. Regular code changes (bug fixes, refactors) work exactly like before. No red tape for everyday development.

### File Auditing & Decision Logging
**Every important decision gets logged** with who made it, why, and what tradeoffs were considered. Six months from now, you'll know exactly why a decision was made and whether it still makes sense. Perfect for teams or when you need to explain your choices.

### Automated Validation & Pre-commit Hooks
**Catch problems before they become problems.** Run validation scripts manually or set up pre-commit hooks to automatically check:
- Are your rules properly formatted?
- Are decision log entries complete?
- Are you hitting any reset triggers?
- Is your context budget being respected?

### Reset Triggers (Circuit Breakers)
**Automatic safety nets** that pause and force you to reduce scope when:
- Rules are being added faster than removed
- Failures keep happening without clear cause
- The system can't explain its own behavior
- Optimization is overriding important tradeoffs

### Context Budgets
**Prevent rule bloat and complexity creep.** Every new rule, instruction, or piece of automation must justify its cost. This keeps your system understandable and maintainable instead of accumulating layers of complexity.

### CI/CD Integration
**Works with your existing workflow.** GitHub Actions integration means validation runs automatically on every push, so the whole team stays in sync without extra effort.

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

MIT License

Copyright (c) 2024 LIL OS Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

