# TODOS (v0.1.1)

Authoritative backlog.

## Governance Hooks
- Any TODO that changes goals/metrics/agent autonomy MUST result in a DECISION_LOG entry when executed.
- Any TODO that increases rules/agents/memory MUST consider CONTEXT_BUDGET.md ceilings.

## Pre-Release Tasks
- ✅ Document missing features - Add an "Implementation Status" section to RESET_TRIGGERS.md showing which triggers are implemented vs. documented
- ✅ Clarify enforcement model - Update README to explain that LIL OS provides governance patterns and validation, not runtime enforcement
- ✅ Rule ID linter verification - Verify rule ID linter finds rules correctly (the earlier warning may have been a false positive)
- ✅ Create warning system for critical changes - Build a script that warns inexperienced developers when important/critical changes are about to be made (non-blocking warnings)
- ✅ Enhance setup wizard pre-commit configuration - Improve setup wizard to better explain pre-commit hooks with opt-in/opt-out, help keep docs tidy for multiple agents
- ✅ Create git hook for critical change warnings - Add a git hook that provides warnings (not blocks) for governance file changes before commits
- ✅ Update documentation on enforcement model - Clarify that warnings are provided but system can be bypassed, designed for inexperienced developer safety

## v0.2.0 Implementation Tasks
- ✅ Phase 1: Automation Creep Detection - Implement check_automation_creep() function to detect when automation expands into human-judgment domains
- ✅ Phase 2: Basic Rule Contradiction Detection - Implement pattern-based rule contradiction detection with helper functions
- ✅ Phase 3: Enhanced Rule Contradiction Detection - Set up structure/placeholder for future semantic analysis implementation

## Code Optimization Tasks
- ✅ Create shared utilities module - Consolidated duplicate code into scripts/lil_os_utils.py (Colors, Finding, load_simple_yaml, read_text)
- ✅ Fix YAML parser workarounds - Added normalize_yaml_list() helper to clean up YAML parser output
- ✅ Update all scripts to use shared utilities - Refactored all 4 scripts to use shared utilities module
- ✅ Test all scripts - Verified all scripts work correctly after refactoring
