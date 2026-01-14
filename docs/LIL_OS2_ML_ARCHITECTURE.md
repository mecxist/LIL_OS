# LIL OS² ML Architecture Design

## Overview

LIL OS² ML consists of two main components:
1. **LIL OS²:** Enhanced version of LIL OS v0.1.1 with improved governance features
2. **ML Module:** Machine learning-powered governance analysis and detection

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LIL OS² ML System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │   LIL OS² Core   │◄────────┤   ML Module      │        │
│  │                  │         │                  │        │
│  │ - Rule Mgmt     │         │ - ML Service     │        │
│  │ - Decision Log  │         │ - Models         │        │
│  │ - Context Budget│         │ - Training       │        │
│  │ - Validation    │         │ - Inference      │        │
│  └──────────────────┘         └──────────────────┘        │
│         │                              │                    │
│         └──────────┬───────────────────┘                    │
│                    │                                         │
│         ┌──────────▼──────────┐                             │
│         │   CLI / API Layer  │                             │
│         └────────────────────┘                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## LIL OS² v2.0 Architecture

### Core Module Structure

```
lil_os/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── rules.py          # Enhanced rule management
│   ├── decisions.py       # Improved decision logging
│   ├── context_budget.py # Real-time budget monitoring
│   └── validation.py      # Enhanced validation
├── ml/                    # ML module (new)
│   ├── __init__.py
│   ├── service.py        # ML service interface
│   ├── models.py         # Model definitions
│   ├── training.py       # Training pipeline
│   └── inference.py      # Inference engine
├── cli.py                 # Enhanced CLI
├── api.py                 # API layer (new)
└── ...
```

### Key Enhancements from v0.1.1

1. **Modular Architecture:** Separated core functionality into modules
2. **Extensibility:** Plugin architecture for ML module integration
3. **API Layer:** RESTful API for programmatic access
4. **Enhanced Error Handling:** Better error messages and recovery
5. **Real-time Monitoring:** Live updates for context budgets and rules

## ML Module Architecture

### Component Structure

```
lil_os/ml/
├── __init__.py
├── service.py           # ML service interface
├── models/
│   ├── contradiction.py # Contradiction detection model
│   ├── automation.py    # Automation creep detection model
│   └── patterns.py      # Pattern recognition model
├── training/
│   ├── pipeline.py      # Training pipeline
│   ├── data.py          # Data preparation
│   └── evaluation.py    # Model evaluation
├── inference/
│   ├── engine.py        # Inference engine
│   ├── features.py     # Feature extraction
│   └── explanations.py # Explanation generation
└── monitoring/
    ├── metrics.py       # Performance metrics
    └── logging.py      # ML decision logging
```

### ML Service Interface

```python
class MLService:
    """Interface for ML module services"""
    
    def check_contradiction(self, rule: Rule, existing_rules: List[Rule]) -> ContradictionResult:
        """Check for semantic contradictions"""
        pass
    
    def check_automation_creep(self, automation: Automation, context_budget: ContextBudget) -> CreepResult:
        """Check for automation creep"""
        pass
    
    def detect_patterns(self, decision_log: DecisionLog) -> PatternResult:
        """Detect governance patterns"""
        pass
```

## Integration Points

### 1. Rule Management Integration

**Flow:**
1. User adds/modifies rule in LIL OS²
2. LIL OS² calls ML module to check for contradictions
3. ML module returns contradiction analysis
4. LIL OS² displays results to user
5. User can accept/reject based on ML insights

**API:**
```python
# In LIL OS² core
rule_manager.add_rule(rule)
contradiction_check = ml_service.check_contradiction(rule, existing_rules)
if contradiction_check.has_contradiction:
    display_warning(contradiction_check)
```

### 2. Decision Logging Integration

**Flow:**
1. Decision logged in LIL OS²
2. Periodically, ML module analyzes decision log
3. ML module detects patterns and anti-patterns
4. Results displayed in decision log viewer
5. Recommendations provided to user

**API:**
```python
# In LIL OS² core
decision_log.add_entry(decision)
# Periodic analysis
patterns = ml_service.detect_patterns(decision_log)
decision_log_viewer.display_patterns(patterns)
```

### 3. Context Budget Integration

**Flow:**
1. Context budget monitored in real-time
2. Automation changes trigger ML check
3. ML module analyzes automation scope
4. Creep detection alerts user
5. Budget visualization updated

**API:**
```python
# In LIL OS² core
context_budget.monitor()
automation_change = detect_automation_change()
creep_check = ml_service.check_automation_creep(automation_change, context_budget)
if creep_check.has_creep:
    alert_user(creep_check)
```

### 4. Validation Scripts Integration

**Flow:**
1. Validation script runs (pre-commit or CI/CD)
2. Calls ML module for ML-powered checks
3. ML module performs semantic analysis
4. Results included in validation output
5. Warnings/errors displayed

**API:**
```python
# In validation script
ml_checks = ml_service.run_all_checks(project_state)
validation_results.add_ml_results(ml_checks)
```

## Data Flow

### Rule Contradiction Detection Flow

```
User Input (Rule)
    │
    ▼
LIL OS² Rule Manager
    │
    ▼
ML Service (check_contradiction)
    │
    ▼
Feature Extraction
    │
    ▼
ML Model Inference
    │
    ▼
Result (Contradiction + Explanation)
    │
    ▼
LIL OS² Display
```

### Automation Creep Detection Flow

```
Automation Change Detected
    │
    ▼
LIL OS² Context Budget Monitor
    │
    ▼
ML Service (check_automation_creep)
    │
    ▼
Domain Classification
    │
    ▼
ML Model Inference
    │
    ▼
Result (Creep + Domain + Recommendation)
    │
    ▼
LIL OS² Alert System
```

### Pattern Recognition Flow

```
Decision Log Updated
    │
    ▼
Periodic Analysis Trigger
    │
    ▼
ML Service (detect_patterns)
    │
    ▼
Feature Extraction from Decision Log
    │
    ▼
ML Model Inference
    │
    ▼
Result (Patterns + Recommendations)
    │
    ▼
Decision Log Viewer
```

## API Design

### RESTful API Endpoints

```
POST   /api/v1/ml/contradiction/check
POST   /api/v1/ml/automation/check
POST   /api/v1/ml/patterns/detect
GET    /api/v1/ml/models/status
GET    /api/v1/ml/metrics
```

### CLI Commands

```bash
lil-os ml check-contradiction <rule-file>
lil-os ml check-automation <automation-description>
lil-os ml detect-patterns [--decision-log <path>]
lil-os ml status
lil-os ml metrics
```

## Module Boundaries

### LIL OS² Core Responsibilities
- Rule management and storage
- Decision logging
- Context budget tracking
- Validation orchestration
- User interface (CLI/API)

### ML Module Responsibilities
- ML model inference
- Feature extraction
- Model training (separate process)
- Performance monitoring
- Explanation generation

### Shared Responsibilities
- Data format definitions
- Error handling standards
- Logging standards
- Configuration management

## Deployment Architecture

### Development
- ML models run locally
- Training on local data
- Direct integration

### Production
- ML service as separate service (optional)
- Model serving via API
- Scalable architecture
- Managed ML services (optional)

## Security Architecture

### ML Service Security
- Authentication for ML API
- Input validation and sanitization
- Rate limiting
- Audit logging

### Model Security
- Model versioning
- Secure model storage
- Model integrity checks
- Rollback capabilities

## Performance Considerations

### Caching Strategy
- Cache ML results for unchanged rules
- Cache feature extractions
- Invalidate on rule changes

### Optimization
- Batch processing for multiple checks
- Async processing for non-critical checks
- Model quantization for faster inference

## Migration from v0.1.1

### Backwards Compatibility
- v0.1.1 projects work without ML module
- ML module is opt-in
- Gradual migration path
- Compatibility layer for old formats

### Migration Steps
1. Upgrade LIL OS to v2.0 (backwards compatible)
2. Opt-in to ML module
3. Run initial ML analysis
4. Review and act on ML insights
5. Enable ML-powered validation

## Future Enhancements

- Distributed ML training
- Custom model training per project
- Real-time ML insights dashboard
- Integration with external ML services
- Multi-model ensemble approaches
