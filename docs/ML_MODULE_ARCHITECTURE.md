# ML Module Architecture

## Overview

The ML module extends LIL OS² with machine learning-powered governance features. It provides semantic analysis, pattern detection, and predictive governance capabilities.

## Architecture

```
lil_os/ml/
├── __init__.py
├── service.py           # ML service interface
├── models/
│   ├── __init__.py
│   ├── contradiction.py # Contradiction detection model
│   ├── automation.py    # Automation creep detection model
│   └── patterns.py      # Pattern recognition model
├── training/
│   └── __init__.py      # Training pipeline (future)
├── inference/
│   └── __init__.py      # Inference engine (future)
└── monitoring/
    ├── __init__.py
    ├── metrics.py       # Performance metrics
    └── logging.py      # ML decision logging
```

## Models

### Contradiction Detection Model

**Purpose:** Detect semantic contradictions between rules.

**Phase 1 Implementation:**
- Pattern-based detection using word overlap and keyword analysis
- Subject extraction and normalization
- Confidence scoring

**Future Enhancements:**
- Semantic embeddings for deeper understanding
- Fine-tuned classification models
- Context-aware contradiction detection

### Automation Creep Detection Model

**Purpose:** Detect when automation expands into human-judgment domains.

**Phase 1 Implementation:**
- Keyword-based detection for forbidden domains
- Human-judgment domain classification
- Confidence scoring

**Future Enhancements:**
- Semantic classification models
- Context-aware domain detection
- Historical pattern analysis

### Pattern Recognition Model

**Purpose:** Detect patterns and anti-patterns in decision logs.

**Phase 1 Implementation:**
- Simple pattern detection (frequent overrides, rapid decisions, etc.)
- Anti-pattern identification
- Recommendation generation

**Future Enhancements:**
- Sequence models for temporal patterns
- Clustering for pattern discovery
- Predictive pattern analysis

## Integration Points

### With LIL OS² Core

The ML module integrates with:
- **RuleManager:** For contradiction detection
- **DecisionLogManager:** For pattern recognition
- **ContextBudgetManager:** For automation creep detection
- **ValidationOrchestrator:** For ML-enhanced validation

### API Usage

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
        print(f"Contradiction detected: {result.explanation}")
```

## Monitoring

### Metrics Collection

The ML module tracks:
- Prediction accuracy
- False positive/negative rates
- Average confidence scores
- Model performance over time

### Decision Logging

All ML decisions are logged for:
- Audit trails
- Model improvement
- Debugging
- Analysis

## Future Enhancements

1. **Model Training Pipeline:** Automated training and deployment
2. **Advanced Models:** Semantic embeddings, transformers
3. **Real-time Learning:** Online learning from user feedback
4. **A/B Testing:** Compare model versions
5. **Explainability:** Enhanced explanations for predictions
