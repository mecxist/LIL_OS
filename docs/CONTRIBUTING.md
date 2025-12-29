# Contributing to LIL OS

Thank you for your interest in contributing to LIL OS! This document explains how to contribute and how to join our talent collective.

## Types of Contributions

### Open Contributions (Anyone Can Contribute)

No approval required:
- **Bug fixes** - Fixing errors in scripts, documentation, or tooling
- **Documentation improvements** - Clarifying explanations, adding examples, fixing typos
- **Code refactoring** - Improving code quality without changing behavior
- **Tooling enhancements** - Adding features to validation scripts or CI/CD integration
- **Examples and use cases** - Documenting how LIL OS is used in practice

**Process:** Fork → Branch → PR → Review → Merge

### Official Contributor Required

These require Official Contributor status (see [Joining the Collective](#joining-the-collective) below):
- **Changes to governance principles** - Modifying GOVERNANCE.md, CONTEXT_BUDGET.md, RESET_TRIGGERS.md
- **Modifications to core rules** - Changing MASTER_RULES.md or RULE_IDS.md
- **Changes to system scope** - Expanding or contracting what LIL OS governs
- **Automation expansions** - Adding new automated checks or processes
- **Philosophical changes** - Altering the underlying principles of Liberatory Intelligence
- **Major platform adaptations** - Extending LIL OS to work with new IDEs, platforms, or environments
- **Architectural changes** - Modifications to core systems and infrastructure

**Why?** Intent-level changes affect the fundamental principles of LIL OS. Official Contributors have demonstrated alignment with Liberatory Intelligence principles and commitment to the project's mission.

**Process:** 
1. Apply to become an Official Contributor
2. Follow governance rules: create decision log entries, get feedback, run validation scripts
3. Submit pull request with proper documentation

## How to Contribute

### For Open Contributions

1. **Fork the repository** and create a feature branch
2. **Make your changes**
3. **Run validation scripts:**
   ```bash
   python3 scripts/lil_os_rule_id_lint.py
   python3 scripts/lil_os_reset_checks.py
   ```
4. **Submit a pull request** with a clear description
5. **Wait for review** - Maintainers will review and merge

### For Intent-Level Changes (Official Contributors Only)

1. **Read the governance docs** - Understand `docs/GOVERNANCE.md`
2. **Propose the change** - Open an issue explaining what, why, who benefits, tradeoffs, and alternatives
3. **Get feedback** - Discuss with maintainers and community
4. **Create a decision log entry** - Document in `docs/DECISION_LOG.md`
5. **Implement the change**
6. **Run validation scripts**
7. **Submit a pull request** - Include decision log entry and justification

## Contribution Guidelines

- **Be respectful**
- **Explain your reasoning** - Especially for intent-level changes
- **Consider reversibility** - Ensure changes can be understood and potentially rolled back
- **Follow existing patterns** - Match style and structure
- **Test your changes** - Run validation scripts before submitting
- **Keep scope focused** - One clear change per pull request

## Adapting LIL OS for Web-Based Environments

> **⚠️ Warning:** Adapting LIL OS for web-based environments is done **at your own risk**. LIL OS is optimized for local IDEs with full file system access, pre-commit hooks, and terminal integration. Web-based adaptations may have limited functionality and reduced rule enforcement capabilities.

LIL OS **may be adapted** for web-based app builders (like Replit, CodeSandbox, Glitch, or browser-based AI coding assistants), though the rule enforcement architecture may be significantly limited. In these environments, you may not have:
- Full file system access
- Pre-commit hook support
- Direct terminal integration
- The same level of automated validation

**If you're using a web-based environment and want to adapt LIL OS to your setup:**

Copy one of these prompts to your AI assistant:

### Prompt 1: General Adaptation

```
I want to use LIL OS (a governance framework for AI-assisted development) in my [web-based environment name]. However, LIL OS is designed for local IDEs with file system access and pre-commit hooks. Please help me:

1. Adapt the LIL OS governance structure to work in this environment
2. Create alternative methods for decision logging that work without direct file system access
3. Set up validation checks that can run in this environment
4. Modify the workflow to work with the constraints of web-based development
5. Explain how to maintain the core principles (intent, authority, context, change management) in this environment

The key principles I need to preserve are:
- Decision logging for important changes
- Context budget management
- Rule tracking and validation
- Governance without bureaucracy
```

### Prompt 2: For Replit/CodeSandbox-style Environments

```
I'm using [Replit/CodeSandbox/other] and want to implement LIL OS governance. Since I don't have pre-commit hooks or full file system access, please help me:

1. Create a simplified LIL OS structure that works in this environment
2. Set up decision logging using available file storage or cloud sync
3. Create manual validation checkpoints I can run before committing changes
4. Adapt the context budget system to work with this environment's constraints
5. Provide a workflow that maintains LIL OS principles without requiring local IDE features
```

### Prompt 3: For Browser-Based AI Assistants

```
I'm using a browser-based AI coding assistant and want to implement LIL OS governance principles. Since I don't have terminal access or pre-commit hooks, please help me:

1. Create a browser-compatible version of LIL OS decision logging
2. Set up manual validation processes I can run
3. Adapt the governance structure to work with cloud-based file storage
4. Create prompts I can use to ensure my AI assistant follows LIL OS principles
5. Design a workflow that maintains accountability and decision tracking in this environment
```

**Remember:** The core value of LIL OS is governance and accountability. Even if you can't use all the automated features, you can still maintain decision logs, track context budgets, and enforce governance principles manually. However, adaptations are not officially supported and may not provide the same level of protection as the standard implementation.

If you successfully adapt LIL OS for a web-based environment, consider contributing your adaptation or [joining the collective](#joining-the-collective) to help others facing similar constraints.

## Joining the Collective

### Why Join LIL Co. as an Official Contributor?

**Liberatory Intelligence Laboratories (LIL Co.)** is a collective of designers, developers, and creative technologists building technologies, protocols, and ecosystems that restore human agency, protect civil liberties, and dismantle technological oppression.

**Benefits:**
- **Direct influence** on LIL OS development and direction
- **Collaboration** with other builders creating liberatory systems
- **Recognition** for advancing Liberatory Intelligence and Cyber Syndicalism
- **Access** to the collective's resources, network, and expertise
- **Participation** in Builder Studio (partnering with organizations) and Product Lab (building infrastructure)

**What we're looking for:**

Commitment to:
- **Ethical technology** - Systems that respect user autonomy and dignity
- **Liberatory design** - Technologies that restore human agency
- **Cyber Syndicalism** - Organizing infrastructure itself, treating software and AI as means of production
- **Governance through architecture** - Enforcing accountability through design
- **Collective intelligence** - Systems that enable coordination and collective power

**Roles:** Technical talents, creative talents, strategic talents

### How to Apply

Visit [Liberatory Intelligence Laboratories](https://www.lilco.io) to learn more and apply.

**Apply Now:** [https://www.lilco.io](https://www.lilco.io)

## Governance for LIL OS Itself

LIL OS follows its own governance rules. Any intent-level changes to LIL OS itself must:
1. Follow `docs/GOVERNANCE.md`
2. Be logged in `docs/DECISION_LOG.md`
3. Pass validation scripts
4. Honor reset triggers

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for philosophical questions or governance proposals
- Visit [lilco.io](https://www.lilco.io) to learn more about joining the collective

---

**Remember:** Governance doesn't grant permission. It preserves legibility, reversibility, and accountability. Governance is memory, not control.
