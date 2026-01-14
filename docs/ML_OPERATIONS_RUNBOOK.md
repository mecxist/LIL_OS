# ML Operations Runbook

## Overview

This runbook provides operational procedures for the LIL OS² ML module.

## Model Status

### Checking Model Status

```bash
lil-os ml status
```

This shows:
- Whether ML module is enabled
- Which models are loaded
- Model health status

## Monitoring

### Viewing Metrics

ML model metrics are tracked automatically. To view:

```python
from lil_os.ml.monitoring import get_metrics_collector

collector = get_metrics_collector()
summary = collector.get_summary()
print(summary)
```

### Viewing Logs

ML decision logs are stored for audit:

```python
from lil_os.ml.monitoring import get_ml_logger

logger = get_ml_logger()
recent_logs = logger.get_recent_logs(limit=100)
```

## Troubleshooting

### ML Module Not Loading

1. Check that ML module is enabled:
   ```bash
   lil-os ml status
   ```

2. Verify imports work:
   ```python
   from lil_os.ml.service import MLService
   ml = MLService()
   ```

3. Check for errors in logs

### Low Model Accuracy

1. Review metrics:
   - Check false positive/negative rates
   - Review confidence scores
   - Analyze prediction patterns

2. Model refinement:
   - Adjust thresholds
   - Improve feature extraction
   - Retrain models (future)

### High False Positive Rate

1. Review contradiction detection:
   - Check similarity thresholds
   - Review keyword matching
   - Adjust confidence thresholds

2. Review automation creep detection:
   - Refine forbidden keywords
   - Adjust domain classification
   - Improve context understanding

## Model Updates

### Phase 1 (Current)

Models use pattern-based detection. Updates involve:
- Adjusting thresholds
- Adding keywords
- Improving heuristics

### Future Phases

Model updates will involve:
- Retraining on new data
- A/B testing new models
- Gradual rollout
- Performance monitoring

## Performance Optimization

### Current Phase

- Models are lightweight (pattern-based)
- No external dependencies
- Fast inference (<10ms)

### Future Optimization

- Model quantization
- Caching predictions
- Batch processing
- Async inference

## Security Considerations

1. **Input Validation:** All inputs are validated
2. **Error Handling:** Failures return safe defaults
3. **Logging:** All decisions are logged
4. **Privacy:** No sensitive data stored

## Backup and Recovery

### Logs

ML decision logs should be backed up regularly:
- Location: In-memory by default
- File logging: Configure via `MLLogger(log_file=path)`

### Metrics

Metrics are in-memory only. For persistence:
- Export metrics periodically
- Store in database (future)
- Use monitoring service (future)

## Support

For issues:
1. Check this runbook
2. Review logs
3. Check metrics
4. File issue in Linear
