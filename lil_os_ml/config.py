#!/usr/bin/env python3
"""
ML Config Loader

Loads and validates lil_os.ml.yaml configuration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional
import sys

# Add scripts directory for YAML parser
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os_utils import load_simple_yaml


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load ML configuration from YAML file.
    
    Args:
        config_path: Path to config file (default: lil_os.ml.yaml)
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = Path("lil_os.ml.yaml")
    
    if not config_path.exists():
        return get_default_config()
    
    try:
        config = load_simple_yaml(config_path)
        return validate_config(config)
    except Exception:
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Get default ML configuration."""
    return {
        "version": 1,
        "ml": {
            "enabled": True,
            "storage_dir": ".lil_os/ml",
            "signals_db": ".lil_os/ml/signals.db",
            "models_dir": ".lil_os/ml/models"
        },
        "change_risk": {
            "enabled": False,
            "mode": "warn",
            "threshold": 0.7,
            "model": {
                "type": "random_forest",
                "retrain_interval_days": 30
            }
        },
        "drift": {
            "enabled": False,
            "mode": "warn",
            "threshold": 0.8,
            "model": {
                "type": "isolation_forest",
                "window_size": 100
            }
        },
        "rag_quality": {
            "enabled": False,
            "mode": "warn",
            "threshold": 0.6,
            "model": {
                "type": "cosine_similarity"
            }
        }
    }


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize configuration."""
    # Ensure all required sections exist
    if "ml" not in config:
        config["ml"] = get_default_config()["ml"]
    
    for module in ["change_risk", "drift", "rag_quality"]:
        if module not in config:
            config[module] = get_default_config()[module]
        else:
            # Ensure required fields
            if "enabled" not in config[module]:
                config[module]["enabled"] = False
            if "mode" not in config[module]:
                config[module]["mode"] = "warn"
            if "threshold" not in config[module]:
                config[module]["threshold"] = get_default_config()[module]["threshold"]
    
    return config


def save_config(config: Dict[str, Any], config_path: Optional[Path] = None):
    """Save configuration to YAML file (simplified - would use proper YAML library)."""
    if config_path is None:
        config_path = Path("lil_os.ml.yaml")
    
    # Simple YAML writer (for basic configs)
    lines = ["version: 1", ""]
    lines.append("# Global ML settings")
    lines.append("ml:")
    lines.append(f"  enabled: {str(config['ml']['enabled']).lower()}")
    lines.append(f"  storage_dir: \"{config['ml']['storage_dir']}\"")
    lines.append(f"  signals_db: \"{config['ml']['signals_db']}\"")
    lines.append(f"  models_dir: \"{config['ml']['models_dir']}\"")
    lines.append("")
    
    for module in ["change_risk", "drift", "rag_quality"]:
        lines.append(f"# Module: {module}")
        lines.append(f"{module}:")
        lines.append(f"  enabled: {str(config[module]['enabled']).lower()}")
        lines.append(f"  mode: \"{config[module]['mode']}\"")
        lines.append(f"  threshold: {config[module]['threshold']}")
        if "model" in config[module]:
            lines.append("  model:")
            for key, value in config[module]["model"].items():
                if isinstance(value, str):
                    lines.append(f"    {key}: \"{value}\"")
                else:
                    lines.append(f"    {key}: {value}")
        lines.append("")
    
    config_path.write_text("\n".join(lines), encoding="utf-8")
