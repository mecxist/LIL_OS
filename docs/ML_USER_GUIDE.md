# ML Module User Guide

## Overview

The ML module enhances LIL OS² with machine learning-powered governance features. It provides semantic analysis, pattern detection, and predictive governance capabilities.

## Getting Started

### Enabling ML Features

ML features are enabled by default. To check status:

```bash
lil-os ml status
```

### Basic Usage

The ML module integrates seamlessly with LIL OS². All ML features are accessible through standard commands and automatically run during validation.

## ML Features

### 1. Semantic Rule Contradiction Detection

**What it does:** Detects semantic contradictions between rules, not just pattern matches.

**How to use:**

```bash
# Check a specific rule for contradictions
lil-os ml check-contradiction [LIL-MR-BOUNDARY-0001]

# Contradictions are also checked automatically during validation
lil-os check
```

**Understanding results:**
- **Confidence score:** How confident the model is (0.0-1.0)
- **Conflicting rules:** List of rules that may contradict
- **Explanation:** Why the contradiction was detected

**Example output:**
```
Contradiction Detected: YES
Confidence: 70.0%
Explanation: Potential contradiction detected with 1 rule(s)
Conflicting Rules:
  - [LIL-MR-BOUNDARY-0002]
```

### 2. Automation Creep Detection

**What it does:** Detects when automation expands into human-judgment domains.

**How it works:**
- Automatically checks automation descriptions
- Flags keywords related to human judgment
- Provides recommendations

**Example:**
If you add automation that mentions "approve", "judge", or "decide", the ML module will flag it as potential creep.

### 3. Pattern Recognition in Decision Logs

**What it does:** Analyzes decision logs to find patterns and anti-patterns.

**How to use:**

```bash
# Detect patterns in decision log
lil-os ml detect-patterns
```

**Detected patterns:**
- Frequent rule overrides
- Rapid decision-making
- Missing reviews
- Rule accumulation

**Example output:**
```
Anti-Patterns Detected:
  [MEDIUM] High rate of rule overrides (5/10)
  [MEDIUM] 3 decision entries overdue for review

Recommendations:
  - Review rules that are frequently overridden
  - Review overdue decision entries and update actual impact
```

## Integration with Core Features

### Rule Management

ML contradiction detection is integrated with rule management:

```bash
# List all rules (ML checks run automatically)
lil-os rules list

# Check rule impact (includes ML analysis)
lil-os rules impact [LIL-MR-BOUNDARY-0001]

# Find contradictions
lil-os rules contradictions
```

### Decision Logging

Pattern recognition is integrated with decision logging:

```bash
# View decision log (patterns shown automatically)
lil-os decisions list

# Search decisions (ML patterns included)
lil-os decisions search "automation"

# View analytics (includes ML insights)
lil-os decisions analytics
```

### Context Budgets

Automation creep detection is integrated with context budgets:

```bash
# View budget status (includes ML alerts)
lil-os budget status

# View budget alerts (includes ML creep detection)
lil-os budget alerts

# Visualize budgets (includes ML recommendations)
lil-os budget visualize
```

## Validation with ML

ML-enhanced validation runs automatically:

```bash
# Run all checks (includes ML checks)
lil-os check
```

ML checks include:
- Semantic contradiction detection
- Pattern recognition
- Anti-pattern warnings

## Troubleshooting

### ML Module Not Working

1. Check status:
   ```bash
   lil-os ml status
   ```

2. Verify models are loaded:
   - Contradiction model
   - Automation creep model
   - Pattern recognition model

3. Check for errors in output

### False Positives

If ML detects false positives:

1. Review the explanation provided
2. Check confidence scores (lower = less certain)
3. Adjust thresholds if needed (future feature)
4. Report false positives for model improvement

### Performance

ML inference is fast (<10ms per check). If you experience slowdowns:

1. Check system resources
2. Review number of rules/decisions
3. ML module is lightweight and shouldn't cause issues

## Best Practices

1. **Review ML Alerts:** Don't ignore ML warnings - they often catch real issues
2. **Understand Confidence:** Lower confidence scores mean less certainty
3. **Combine with Manual Review:** ML is a tool, not a replacement for judgment
4. **Provide Feedback:** Report false positives/negatives to improve models

## Advanced Usage

### Programmatic Access

```python
from lil_os.ml.service import MLService
from lil_os.core import RuleManager

ml_service = MLService(enabled=True)
rule_manager = RuleManager()

# Check for contradictions
rules = rule_manager.get_all_rules()
for rule in rules:
    result = ml_service.check_contradiction(rule, other_rules)
    if result.has_contradiction:
        print(f"Contradiction: {result.explanation}")
```

### Monitoring ML Performance

```python
from lil_os.ml.monitoring import get_metrics_collector

collector = get_metrics_collector()
summary = collector.get_summary()
print(f"Accuracy: {summary['models']['contradiction']['accuracy']}")
```

## FAQ

**Q: Do I need to train the models?**  
A: No, Phase 1 models use pattern-based detection. Training will be available in future phases.

**Q: Can I disable ML features?**  
A: Yes, but they're enabled by default and lightweight. Disabling reduces governance capabilities.

**Q: How accurate are the models?**  
A: Phase 1 models use pattern-based detection with ~70% confidence. Accuracy improves in later phases.

**Q: Does ML slow down my workflow?**  
A: No, ML checks are fast (<10ms) and run asynchronously where possible.

**Q: Can I customize ML behavior?**  
A: Basic customization is available. Advanced customization will be in future phases.

## Next Steps

- Read the [ML Module Architecture](ML_MODULE_ARCHITECTURE.md) for technical details
- Review [ML Operations Runbook](ML_OPERATIONS_RUNBOOK.md) for operations
- Check [LIL OS² Architecture](LIL_OS2_ML_ARCHITECTURE.md) for integration details
