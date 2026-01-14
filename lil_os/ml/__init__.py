"""
LIL OS² ML Module

Machine learning-powered governance features for semantic analysis,
pattern detection, predictive governance, and drift detection.
"""

from .service import MLService
from .models.contradiction import ContradictionModel
from .models.automation import AutomationCreepModel
from .models.patterns import PatternRecognitionModel

# Drift detection components
from .schema import FeatureSet, GitFeatures, ValidationFeatures, GovernanceFeatures
from .extractor import FeatureExtractor, GitExtractor, ReportExtractor, GovernanceExtractor
from .detector import AnomalyDetector
from .trainer import ModelTrainer
from .evaluator import ModelEvaluator, EvaluationMetrics
from .features import extract_current_features, extract_historical_features

__all__ = [
    # Existing ML services
    "MLService",
    "ContradictionModel",
    "AutomationCreepModel",
    "PatternRecognitionModel",
    # Drift detection
    "FeatureSet",
    "GitFeatures",
    "ValidationFeatures",
    "GovernanceFeatures",
    "FeatureExtractor",
    "GitExtractor",
    "ReportExtractor",
    "GovernanceExtractor",
    "AnomalyDetector",
    "ModelTrainer",
    "ModelEvaluator",
    "EvaluationMetrics",
    "extract_current_features",
    "extract_historical_features",
]
