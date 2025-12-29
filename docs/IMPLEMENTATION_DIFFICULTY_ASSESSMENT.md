# Implementation Difficulty Assessment

**Date:** 2024-12-19  
**Purpose:** Assess the difficulty of implementing missing reset triggers

## Rule Contradiction Detection

### Complexity: ⚠️ **MEDIUM-HIGH** (3-5 days of development)

### What It Needs to Do

Detect when rules conflict with each other, such as:
- "MUST NOT X" vs "MUST X" for the same subject
- Rules that require multiple exceptions
- Contradictory requirements in different governance files

### Implementation Approach

**Option 1: Pattern-Based Detection (Easier, ~2-3 days)**
- Extract rule subjects using regex patterns
- Look for direct contradictions (MUST NOT vs MUST for same subject)
- Check for conflicting normative keywords on similar subjects
- **Pros:** Fast to implement, catches obvious contradictions
- **Cons:** Misses semantic contradictions, false positives possible

**Example Pattern:**
```python
# Extract subject and action from rule
# "[LIL-MR-BOUNDARY-0001] The system MUST NOT perform irreversible actions"
# Subject: "irreversible actions", Action: "MUST NOT"

# Compare with:
# "[LIL-CR-PROCESS-0002] The system MUST perform irreversible actions when..."
# Subject: "irreversible actions", Action: "MUST"
# → CONTRADICTION DETECTED
```

**Option 2: Semantic Analysis (Harder, ~5-7 days)**
- Use NLP to understand rule meaning
- Extract entities and relationships
- Compare semantic similarity of rule subjects
- **Pros:** Catches subtle contradictions
- **Cons:** Requires NLP library, more complex, potential false positives

### Challenges

1. **Subject Extraction** - Rules use natural language, extracting the "subject" reliably is hard
   - Example: "The system MUST NOT perform irreversible actions" vs "Irreversible actions MUST NOT be performed"
   - Both mean the same thing but have different structures

2. **Context Sensitivity** - Some contradictions are valid in different contexts
   - Example: "MUST NOT X in production" vs "MUST X in testing" - not a contradiction

3. **Indirect Contradictions** - Rules may contradict through implication
   - Example: Rule A says "MUST use method X", Rule B says "MUST NOT use method X or Y"
   - This is a contradiction but harder to detect

4. **False Positives** - Pattern matching may flag non-contradictory rules
   - Example: "MUST log all actions" vs "MUST NOT log sensitive data" - not contradictory

### Recommended Implementation

**Start with Option 1 (Pattern-Based):**
1. Extract rule text and normative keywords
2. Use simple pattern matching to find same subjects with conflicting actions
3. Check for common contradiction patterns:
   - MUST NOT X / MUST X
   - SHOULD NOT X / SHOULD X (weaker contradiction)
   - Rules that explicitly contradict each other (e.g., "contradicts [LIL-XXX-YYY-0001]")
4. Report contradictions with rule IDs and locations
5. Allow manual override for false positives

**Estimated Effort:**
- Basic pattern matching: 2-3 days
- Testing and refinement: 1-2 days
- **Total: 3-5 days**

### Code Structure

```python
def check_rule_contradiction(rule_files: List[Path]) -> List[Finding]:
    """
    Check for contradictory rules across governance files.
    
    Steps:
    1. Parse all rules from MASTER_RULES, GOVERNANCE, CONTEXT_BUDGET, .cursorrules
    2. Extract subject and normative keyword for each rule
    3. Group rules by similar subjects (using text similarity)
    4. Check for conflicting normative keywords (MUST NOT vs MUST)
    5. Report contradictions
    """
    # Implementation would go here
    pass
```

---

## Automation Creep Detection

### Complexity: ⚠️ **MEDIUM** (2-3 days of development)

### What It Needs to Do

Detect when automation expands into human-judgment domains by:
- Scanning decision logs for automation-related keywords
- Comparing against CONTEXT_BUDGET forbidden list
- Flagging when automation is added to forbidden domains

### Implementation Approach

**Pattern Matching + Keyword Detection (Recommended, ~2-3 days)**

1. **Extract forbidden domains from CONTEXT_BUDGET.md:**
   - Value judgments
   - Moral tradeoffs
   - Decisions involving irreversible harm
   - Actions without audit trail

2. **Scan decision log entries for automation keywords:**
   - "automate", "automation", "automatic", "auto-"
   - "AI decision", "agent decides", "system chooses"
   - "without human", "no human intervention"

3. **Check if automation targets forbidden domains:**
   - Look for forbidden domain keywords in same entry as automation keywords
   - Pattern: "automating [forbidden domain]" = violation

4. **Report violations with entry details**

### Challenges

1. **Natural Language Variation** - Automation can be described many ways
   - "AI will decide" vs "automated decision" vs "system chooses"
   - Need comprehensive keyword list

2. **Context Understanding** - Need to understand what domain automation targets
   - Example: "automating user authentication" - is this a value judgment? (No)
   - Example: "automating hiring decisions" - is this a value judgment? (Yes)

3. **False Positives** - May flag legitimate automation
   - Example: "automating code formatting" - not a forbidden domain
   - Need to distinguish automation scope

### Recommended Implementation

**Keyword-Based Detection with Context:**

1. **Define automation keywords:**
   ```python
   automation_keywords = [
       "automate", "automation", "automatic", "auto-",
       "AI decision", "agent decides", "system chooses",
       "without human", "no human", "unattended"
   ]
   ```

2. **Define forbidden domains from CONTEXT_BUDGET.md:**
   ```python
   forbidden_domains = [
       "value judgment", "moral", "ethics", "ethical",
       "irreversible harm", "permanent damage",
       "without audit", "no audit trail", "no logging"
   ]
   ```

3. **Scan decision log entries:**
   - Check if entry contains automation keywords
   - Check if entry contains forbidden domain keywords
   - If both present, flag as potential violation

4. **Report with context:**
   - Show the entry text
   - Highlight the automation and forbidden domain keywords
   - Allow manual review (may be false positive)

**Estimated Effort:**
- Keyword extraction and matching: 1-2 days
- Testing and refinement: 1 day
- **Total: 2-3 days**

### Code Structure

```python
def check_automation_creep(
    decision_log: Path,
    context_budget: Path,
    automation_keywords: List[str],
    forbidden_domains: List[str]
) -> List[Finding]:
    """
    Check if automation is expanding into human-judgment domains.
    
    Steps:
    1. Parse CONTEXT_BUDGET.md to extract forbidden domains
    2. Parse decision log entries
    3. For each entry with automation keywords, check for forbidden domains
    4. Report violations
    """
    # Implementation would go here
    pass
```

---

## Comparison

| Feature | Difficulty | Time Estimate | Complexity |
|---------|-----------|---------------|------------|
| **Rule Contradiction** | Medium-High | 3-5 days | Pattern matching + subject extraction |
| **Automation Creep** | Medium | 2-3 days | Keyword matching + context checking |

## Recommendations

### For v0.2.0 Release:

1. **Start with Automation Creep Detection** (easier, faster)
   - Lower complexity
   - More straightforward implementation
   - Good user value (catches important violations)
   - Can be implemented in 2-3 days

2. **Then implement Rule Contradiction Detection** (more complex)
   - Start with basic pattern matching
   - Can be enhanced later with semantic analysis
   - More valuable but requires more testing
   - Can be implemented in 3-5 days

### Implementation Priority:

1. **Phase 1 (v0.2.0):** Automation Creep Detection
2. **Phase 2 (v0.2.0):** Basic Rule Contradiction Detection (pattern-based)
3. **Phase 3 (v0.3.0):** Enhanced Rule Contradiction Detection (semantic analysis)

### Notes:

- Both features can be implemented incrementally
- Start with simple pattern matching, enhance based on user feedback
- False positives are acceptable - better to catch potential issues than miss them
- Users can review and override false positives manually

---

**Assessment Complete**

