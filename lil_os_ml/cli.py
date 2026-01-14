#!/usr/bin/env python3
"""
ML CLI Commands

Command-line interface for ML modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from .config import load_config, save_config
from .signals import GitSignalCollector, ReportSignalCollector, SignalStorage
from .evaluators.change_risk import ChangeRiskEvaluator
from .evaluators.drift import DriftEvaluator
from .evaluators.rag_quality import RAGQualityEvaluator


def ml_status_command(args) -> int:
    """Show ML modules status."""
    try:
        from lil_os import cli_ux
        use_rich = cli_ux.is_rich_available()
    except ImportError:
        use_rich = False
    
    config = load_config()
    
    if use_rich:
        console = cli_ux.get_console()
        content = []
        
        for module_name in ["change_risk", "drift", "rag_quality"]:
            module_config = config.get(module_name, {})
            enabled = module_config.get("enabled", False)
            mode = module_config.get("mode", "warn")
            
            status_icon = "✅" if enabled else "⚠️"
            content.append(f"Module: {module_name}")
            content.append(f"  Status: {status_icon} {'Enabled' if enabled else 'Disabled'} ({mode} mode)")
            content.append("")
        
        cli_ux.print_rich_panel("ML Modules Status", content)
    else:
        from scripts.lil_os_utils import print_os_box
        content = []
        for module_name in ["change_risk", "drift", "rag_quality"]:
            module_config = config.get(module_name, {})
            enabled = module_config.get("enabled", False)
            mode = module_config.get("mode", "warn")
            status = "✅ Enabled" if enabled else "⚠️ Disabled"
            content.append(f"  {module_name}: {status} ({mode} mode)")
        print_os_box("ML Modules Status", content)
    
    return 0


def ml_run_command(args) -> int:
    """Run ML evaluations."""
    config = load_config()
    
    if not config.get("ml", {}).get("enabled", False):
        print("ML is disabled in configuration")
        return 1
    
    # Collect signals
    signals_db_path = Path(config["ml"]["signals_db"])
    storage = SignalStorage(signals_db_path)
    
    git_collector = GitSignalCollector()
    report_collector = ReportSignalCollector()
    
    print("Collecting signals...")
    git_signals = git_collector.collect(limit=50)
    report_signals = report_collector.collect(limit=50)
    
    all_signals = git_signals + report_signals
    
    # Save signals
    if all_signals:
        storage.save_signals(all_signals)
        print(f"✓ Collected {len(all_signals)} signals")
    
    # Run evaluations
    modules_to_run = []
    if args.all or (not args.module):
        modules_to_run = ["change_risk", "drift", "rag_quality"]
    else:
        modules_to_run = [args.module]
    
    results = {}
    
    for module_name in modules_to_run:
        module_config = config.get(module_name, {})
        if not module_config.get("enabled", False):
            continue
        
        print(f"\nRunning {module_name} evaluation...")
        
        try:
            if module_name == "change_risk":
                evaluator = ChangeRiskEvaluator(module_config)
            elif module_name == "drift":
                evaluator = DriftEvaluator(module_config)
            elif module_name == "rag_quality":
                evaluator = RAGQualityEvaluator(module_config)
            else:
                continue
            
            result = evaluator.evaluate(all_signals)
            results[module_name] = {
                "status": result.status,
                "score": result.score,
                "findings": result.findings
            }
            
            print(f"  Status: {result.status}")
            print(f"  Score: {result.score:.2f}")
            print(f"  Findings: {len(result.findings)}")
        except Exception as e:
            print(f"  Error: {e}")
            results[module_name] = {"status": "error", "error": str(e)}
    
    # Output results
    if args.json:
        output = {
            "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            "modules": results
        }
        print("\n" + json.dumps(output, indent=2))
    elif args.md:
        # Markdown output
        md_lines = ["# ML Evaluation Results", ""]
        for module_name, result in results.items():
            md_lines.append(f"## {module_name}")
            md_lines.append(f"- Status: {result['status']}")
            md_lines.append(f"- Score: {result.get('score', 0.0):.2f}")
            md_lines.append("")
        print("\n" + "\n".join(md_lines))
    
    return 0


def ml_enable_command(args) -> int:
    """Enable an ML module."""
    config = load_config()
    
    if args.module not in ["change_risk", "drift", "rag_quality"]:
        print(f"Unknown module: {args.module}")
        return 1
    
    config[args.module]["enabled"] = True
    save_config(config)
    print(f"Enabled {args.module}")
    return 0


def ml_disable_command(args) -> int:
    """Disable an ML module."""
    config = load_config()
    
    if args.module not in ["change_risk", "drift", "rag_quality"]:
        print(f"Unknown module: {args.module}")
        return 1
    
    config[args.module]["enabled"] = False
    save_config(config)
    print(f"Disabled {args.module}")
    return 0


def ml_train_command(args) -> int:
    """Train ML models."""
    config = load_config()
    
    modules_to_train = []
    if args.module:
        modules_to_train = [args.module]
    else:
        modules_to_train = ["change_risk", "drift", "rag_quality"]
    
    # Collect signals for training
    signals_db_path = Path(config["ml"]["signals_db"])
    storage = SignalStorage(signals_db_path)
    
    all_signals = storage.get_signals(limit=1000)
    
    if not all_signals:
        print("No signals available for training")
        return 1
    
    for module_name in modules_to_train:
        module_config = config.get(module_name, {})
        if not module_config.get("enabled", False):
            continue
        
        print(f"Training {module_name}...")
        
        try:
            if module_name == "change_risk":
                evaluator = ChangeRiskEvaluator(module_config)
            elif module_name == "drift":
                evaluator = DriftEvaluator(module_config)
            elif module_name == "rag_quality":
                evaluator = RAGQualityEvaluator(module_config)
            else:
                continue
            
            metrics = evaluator.train(all_signals)
            print(f"  Training complete: {metrics}")
        except Exception as e:
            print(f"  Error: {e}")
    
    return 0
