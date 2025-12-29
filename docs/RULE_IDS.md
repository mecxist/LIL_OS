# Rule IDs (v1.0)

## Canonical Format
[LIL-<DOC>-<CAT>-<NNNN>]

DOC:
MR, GOV, CB, RT, WF, QL, SEC, DATA, API, PERF, CR

CAT:
BOUNDARY, AUTH, PROCESS, SAFETY, SCOPE, FORMAT, BUDGET, LOG, RESET

NNNN:
0001+

## Normative Keywords
Each rule line containing an ID MUST include one of:
MUST, MUST NOT, SHOULD, SHOULD NOT, MAY

## Example
- [LIL-MR-BOUNDARY-0001] The system MUST NOT perform irreversible actions without human confirmation.
  - Because: irreversibility amplifies drift and harm.

## Referencing
See [LIL-MR-BOUNDARY-0001].

## Rule Lifecycle

Rules evolve over time. This section describes how to manage rule changes, deprecations, and migrations.

### Creating Rules

1. **Assign a unique ID** - Use the canonical format `[LIL-<DOC>-<CAT>-<NNNN>]`
2. **Include normative keyword** - Each rule MUST include MUST, MUST NOT, SHOULD, SHOULD NOT, or MAY
3. **Document the rationale** - Explain why the rule exists (can be inline or in decision log)
4. **Log intent-level changes** - If the rule changes system scope or authority, create a decision log entry

### Modifying Rules

**When modifying a rule:**
- Keep the same rule ID (rules are identified by ID, not text)
- Update the rule text to reflect the change
- If the modification changes intent, create a decision log entry
- Consider if the modification creates contradictions with other rules

**Example:**
```
Before: [LIL-MR-BOUNDARY-0001] The system MUST NOT perform irreversible actions.
After:  [LIL-MR-BOUNDARY-0001] The system MUST NOT perform irreversible actions without human confirmation.
```

### Deprecating Rules

**When a rule is no longer needed:**
1. **Mark as deprecated** - Add `(DEPRECATED)` to the rule text or create a deprecation marker
2. **Document why** - Explain in decision log why the rule is being removed
3. **Remove references** - Update any documentation that references the rule
4. **Remove the rule** - Delete the rule after a grace period (e.g., 30 days)

**Example:**
```
[DEPRECATED] [LIL-CR-PROCESS-0001] Old rule text here
Reason: Replaced by [LIL-CR-PROCESS-0002] in decision log entry dated YYYY-MM-DD
```

### Rule Migration

**When replacing one rule with another:**
1. **Create new rule** - Assign new ID with updated requirements
2. **Mark old rule as deprecated** - Reference the new rule ID
3. **Document migration** - Create decision log entry explaining the change
4. **Update references** - Find and update all references to the old rule ID
5. **Remove old rule** - After migration period, remove deprecated rule

**Example:**
```
Old: [LIL-CR-PROCESS-0001] Old requirement
New: [LIL-CR-PROCESS-0002] New requirement (replaces LIL-CR-PROCESS-0001)
```

### Rule Versioning

Rules are identified by their ID, not version numbers. If a rule needs significant changes:
- **Minor changes:** Update the rule text, keep same ID
- **Major changes:** Create new rule with new ID, deprecate old rule
- **Document changes:** Always document significant changes in decision log

### Best Practices

- **Review rules periodically** - Check if rules are still relevant (see RESET_TRIGGERS.md)
- **Avoid rule accumulation** - Remove deprecated rules promptly
- **Maintain rule clarity** - If a rule becomes unclear, clarify or replace it
- **Track rule dependencies** - Document when rules reference or depend on other rules
- **Use rule IDs consistently** - Always reference rules by their ID, not by description
