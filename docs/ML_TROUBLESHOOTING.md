# ML Module Troubleshooting Guide

## Common Issues

### ML Module Not Loading

**Symptoms:**
- `lil-os ml status` shows models not loaded
- ML checks return "ML module not enabled"

**Solutions:**
1. Check Python version (requires 3.10+)
2. Verify imports work:
   ```python
   from lil_os.ml.service import MLService
   ```
3. Check for import errors in logs
4. Ensure all ML module files are present

### False Positives in Contradiction Detection

**Symptoms:**
- Rules flagged as contradictory but aren't
- Low confidence scores (<0.5)

**Solutions:**
1. Review the explanation - understand why it was flagged
2. Check rule subjects - may be similar but not contradictory
3. Adjust rule wording to be more specific
4. This is expected in Phase 1 (pattern-based detection)

### False Negatives in Contradiction Detection

**Symptoms:**
- Contradictory rules not detected
- Missing obvious contradictions

**Solutions:**
1. Verify rules actually contradict (check manually)
2. Ensure rules have similar subjects
3. Check normative keywords conflict
4. Report for model improvement

### Automation Creep Detection Too Sensitive

**Symptoms:**
- Many false positives for automation creep
- Legitimate automation flagged

**Solutions:**
1. Review detected keywords
2. Refine automation descriptions
3. Add context to automation descriptions
4. Adjust keyword list (future feature)

### Pattern Recognition Not Finding Patterns

**Symptoms:**
- `lil-os ml detect-patterns` shows no patterns
- Decision log has clear patterns

**Solutions:**
1. Ensure decision log has enough entries (>5 recommended)
2. Check decision log format is correct
3. Verify dates are parseable
4. Patterns require sufficient data

### Performance Issues

**Symptoms:**
- Slow ML checks
- High CPU usage

**Solutions:**
1. Check number of rules (very large rule sets may be slow)
2. Review decision log size
3. ML module is lightweight - investigate other causes
4. Check system resources

## Error Messages

### "ML module not enabled"

**Cause:** ML service not initialized or disabled

**Fix:**
```python
from lil_os.ml.service import MLService
ml = MLService(enabled=True)
```

### "Error during contradiction check"

**Cause:** Exception in contradiction model

**Fix:**
1. Check rule format is valid
2. Verify rule manager can parse rules
3. Check for malformed rule text

### "Error during creep check"

**Cause:** Exception in automation creep model

**Fix:**
1. Verify automation description is valid text
2. Check context budget items format
3. Ensure inputs are not None

### "Error during pattern detection"

**Cause:** Exception in pattern recognition model

**Fix:**
1. Verify decision log entries are valid
2. Check date formats
3. Ensure entries have required fields

## Debugging

### Enable Verbose Logging

```python
from lil_os.ml.monitoring import get_ml_logger

logger = get_ml_logger()
recent_logs = logger.get_recent_logs(limit=100)
for log in recent_logs:
    print(f"{log.timestamp}: {log.model_name} - {log.prediction}")
```

### Check Metrics

```python
from lil_os.ml.monitoring import get_metrics_collector

collector = get_metrics_collector()
summary = collector.get_summary()
print(summary)
```

### Test Individual Models

```python
from lil_os.ml.models.contradiction import ContradictionModel
from lil_os.core.rules import Rule, RuleLifecycle
from pathlib import Path

model = ContradictionModel()
rule = Rule(
    rule_id="[LIL-TEST-0001]",
    text="[LIL-TEST-0001] Test rule",
    file_path=Path("test.md"),
    line_number=1,
    normative_keyword="MUST",
)
result = model.check(rule, [])
print(result)
```

## Getting Help

1. Check this troubleshooting guide
2. Review [ML User Guide](ML_USER_GUIDE.md)
3. Check [ML Operations Runbook](ML_OPERATIONS_RUNBOOK.md)
4. File an issue in Linear with:
   - Error message
   - Steps to reproduce
   - ML module status output
   - Relevant logs
