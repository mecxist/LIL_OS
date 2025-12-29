# Context Loading Hierarchy (v1.0)

## Purpose

This document guides AI agents and developers on which LIL OS documentation files to load based on the task at hand. Following this hierarchy minimizes context window usage while ensuring all necessary information is available.

## Essential Files (Always Load for LIL OS Tasks)

These files contain core governance principles and should be loaded for any LIL OS-related work:

- **`LIL_OS.md`** - Entry point and index to required reading
- **`GOVERNANCE.md`** - Core governance framework
- **`MASTER_RULES.md`** - Non-negotiable boundaries
- **`DECISION_LOG.md`** - Decision logging template and structure

## Task-Specific Files

Load these files only when working on the corresponding task:

### Setup & Installation
- **`INSTALLATION.md`** - Step-by-step installation instructions
- **`USER_GUIDE.md`** - Beginner-friendly guide with examples

### Contributing & Adaptation
- **`CONTRIBUTING.md`** - Contribution guidelines and adaptation guidance
- **`DEPLOYMENT.md`** - Guidelines for packaging/deployment

### Security & Validation
- **`SECURITY.md`** - Security architecture and best practices
- **`RULE_IDS.md`** - Rule ID format and lifecycle management

### Governance Details
- **`CONTEXT_BUDGET.md`** - Context scarcity doctrine
- **`RESET_TRIGGERS.md`** - Circuit breaker conditions
- **`GOVERNANCE_HOOKS.md`** - Domain-specific governance hooks

### Workflow & Process
- **`WORKFLOW.md`** - Standard development workflow
- **`TODOS.md`** - Task management structure

## Reference Documents (Load Only When Needed)

These are analysis documents, assessments, or reference materials that should only be loaded when specifically referenced or when working on related features:

- **`RUNTIME_ENFORCEMENT_ANALYSIS.md`** - Analysis of runtime enforcement approaches (500+ lines)
- **`IMPLEMENTATION_DIFFICULTY_ASSESSMENT.md`** - Assessment of feature implementation difficulty (200+ lines)
- **`RELEASE_ASSESSMENT.md`** - Release readiness assessment (400+ lines)

## Context Loading Strategy

### For New Projects
1. Load Essential Files
2. Load `INSTALLATION.md` and `USER_GUIDE.md`
3. Load `GOVERNANCE_HOOKS.md` for domain-specific guidance

### For Intent-Level Changes
1. Load Essential Files
2. Load `GOVERNANCE.md` (detailed review)
3. Load `RESET_TRIGGERS.md` (check for triggers)
4. Load `CONTEXT_BUDGET.md` (verify budget compliance)

### For Contributing
1. Load Essential Files
2. Load `CONTRIBUTING.md`
3. Load `RULE_IDS.md` (if adding/modifying rules)

### For Security Work
1. Load Essential Files
2. Load `SECURITY.md`
3. Load `GOVERNANCE_HOOKS.md` (for security-related hooks)

### For Deployment/Packaging
1. Load `DEPLOYMENT.md`
2. Load `GOVERNANCE_HOOKS.md` (if deployment affects governance)

## File Size Reference

- **Small (< 100 lines):** LIL_OS.md, MASTER_RULES.md, DECISION_LOG.md, WORKFLOW.md, GOVERNANCE_HOOKS.md, etc.
- **Medium (100-200 lines):** GOVERNANCE.md, RESET_TRIGGERS.md, CONTEXT_BUDGET.md, RULE_IDS.md, INSTALLATION.md
- **Large (200-400 lines):** USER_GUIDE.md, CONTRIBUTING.md, SECURITY.md, DEPLOYMENT.md
- **Reference (400+ lines):** RUNTIME_ENFORCEMENT_ANALYSIS.md, IMPLEMENTATION_DIFFICULTY_ASSESSMENT.md, RELEASE_ASSESSMENT.md

## Best Practices

1. **Start with Essential Files** - Always load the 4 essential files first
2. **Load Task-Specific Files** - Only load files relevant to your current task
3. **Avoid Reference Documents** - Don't load analysis/assessment documents unless specifically needed
4. **Use Cross-References** - When a document references another, load that document only if needed
5. **Check File Sizes** - Be aware that reference documents are large and should be loaded sparingly

## Notes

- This hierarchy is designed to minimize context window usage while maintaining access to necessary information
- The structure allows for modular loading based on task requirements
- Reference documents are intentionally kept separate to avoid unnecessary context bloat

