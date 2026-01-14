#!/usr/bin/env python3
"""
LIL OS² CLI v2 - Enhanced command-line interface using Typer

Provides modern CLI with Rich-based output, streaming, and enhanced UX.
Maintains backwards compatibility with cli.py while adding new features.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

try:
    import typer
    from typer import Typer
    TYPER_AVAILABLE = True
except ImportError:
    TYPER_AVAILABLE = False
    # Fallback if typer not available
    class Typer:
        def __init__(self, *args, **kwargs):
            pass
        def command(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        def callback(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        def add_typer(self, *args, **kwargs):
            pass

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Import existing CLI functions
from . import cli
from . import status
from . import decision_prompt
from . import help_system
from . import shell_enhanced
from . import watch
from . import box_designer
from . import daemon
from . import events

# Import UI components
try:
    from . import cli_ux
    RICH_AVAILABLE = cli_ux.RICH_AVAILABLE
    if RICH_AVAILABLE:
        from rich.panel import Panel
except ImportError:
    RICH_AVAILABLE = False
    Panel = None

# Create main app
if TYPER_AVAILABLE:
    app = Typer(
        name="lil-os",
        help="LIL OS² - A constitutional substrate for AI-assisted software development",
        add_completion=False,
    )
else:
    app = Typer()

# Global flags
class GlobalState:
    """Global state for CLI options."""
    json_output: bool = False
    markdown_output: bool = False
    quiet: bool = False
    verbose: bool = False
    no_color: bool = False

state = GlobalState()

# Create subcommand groups
if TYPER_AVAILABLE:
    drift_app = Typer(help="ML drift detection commands")
    report_app = Typer(help="Validation report viewing commands")
    app.add_typer(drift_app, name="drift")
    app.add_typer(report_app, name="report")
else:
    drift_app = app
    report_app = app


@app.callback()
def main_callback(
    json: bool = typer.Option(False, "--json", help="JSON output format"),
    md: bool = typer.Option(False, "--md", help="Markdown output format"),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress non-error output"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose output"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colors"),
):
    """LIL OS² - A constitutional substrate for AI-assisted software development."""
    state.json_output = json
    state.markdown_output = md
    state.quiet = quiet
    state.verbose = verbose
    state.no_color = no_color


@app.command()
def setup():
    """Run the setup wizard."""
    class Args:
        pass
    args = Args()
    return cli.setup_command(args)


@app.command()
def lint(
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Run in interactive mode")
):
    """Check rule IDs for format and consistency."""
    class Args:
        def __init__(self, interactive):
            self.interactive = interactive
    args = Args(interactive)
    return cli.lint_command(args)


@app.command()
def check(
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Run in interactive mode")
):
    """Run reset trigger checks."""
    class Args:
        def __init__(self, interactive):
            self.interactive = interactive
    args = Args(interactive)
    return cli.check_command(args)


@app.command()
def warn(
    pre_commit: bool = typer.Option(False, "--pre-commit", help="Run in pre-commit mode")
):
    """Check for critical changes."""
    class Args:
        def __init__(self, pre_commit):
            self.pre_commit = pre_commit
    args = Args(pre_commit)
    return cli.warn_command(args)


@app.command()
def status_cmd(
    live: bool = typer.Option(False, "--live", help="Live updates every 5s"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Show interactive menu"),
    json: bool = typer.Option(False, "--json", help="JSON output"),
    md: bool = typer.Option(False, "--md", help="Markdown output"),
):
    """Show system status."""
    class Args:
        def __init__(self, live, interactive, json, md):
            self.live = live
            self.interactive = interactive
            self.json = json
            self.md = md
    args = Args(live, interactive, json, md)
    return cli.status_command(args)


@app.command(name="report")
def report_cmd(
    report_id: Optional[str] = typer.Argument(None, help="Report timestamp or 'latest'"),
    format: str = typer.Option("panel", "--format", help="Output format: panel, table, or json"),
):
    """Render validation reports in panels."""
    # TODO: Implement report rendering
    if not RICH_AVAILABLE:
        print("Rich library required for report rendering. Install with: pip install rich")
        return 1
    
    reports_dir = Path(".lil_os/reports")
    if not reports_dir.exists():
        print("No reports directory found. Run validation first.")
        return 1
    
    if report_id is None or report_id == "latest":
        # Find latest report
        json_reports = list(reports_dir.glob("*.json"))
        if not json_reports:
            print("No reports found.")
            return 1
        report_path = max(json_reports, key=lambda p: p.stat().st_mtime)
    else:
        # Find report by timestamp
        report_path = reports_dir / f"{report_id}_*_report.json"
        matches = list(reports_dir.glob(str(report_path.name)))
        if not matches:
            print(f"Report not found: {report_id}")
            return 1
        report_path = matches[0]
    
    # Load and display report
    import json
    report_data = json.loads(report_path.read_text())
    
    if format == "json" or state.json_output:
        print(json.dumps(report_data, indent=2))
        return 0
    
    # Render with Rich
    console = cli_ux.get_console()
    
    if format == "table":
        table = cli_ux.create_findings_table(report_data.get("findings", []))
        console.print(table)
    else:
        # Panel format (default)
        content = cli_ux.format_report_content(report_data)
        panel = Panel(content, title="Validation Report", border_style="cyan")
        console.print(panel)
    
    return 0


@drift_app.command()
def train(
    force: bool = typer.Option(False, "--force", help="Retrain even if model exists"),
    data_dir: Optional[str] = typer.Option(None, "--data-dir", help="Custom feature data directory"),
    days: int = typer.Option(90, "--days", help="Number of days of history to use"),
):
    """Train anomaly detection model on historical data."""
    try:
        from .ml.trainer import ModelTrainer
        from .ml.features import extract_historical_features
        from pathlib import Path
        
        features_dir = Path(data_dir) if data_dir else Path(".lil_os/ml/features")
        
        # Extract features if needed
        if not list(features_dir.glob("*.json")):
            print("No feature files found. Extracting features from git history and reports...")
            extract_historical_features(days=days, output_dir=features_dir)
        
        # Train model
        trainer = ModelTrainer(features_dir=features_dir)
        model_path, metadata = trainer.train_model(days=days, force=force)
        
        if state.json_output:
            import json
            print(json.dumps({
                "status": "success",
                "model_path": str(model_path),
                "metadata": metadata
            }, indent=2))
        else:
            console = cli_ux.get_console() if RICH_AVAILABLE else None
            if console:
                from rich.panel import Panel
                content = [
                    f"Model trained successfully!",
                    f"",
                    f"Model: {model_path.name}",
                    f"Training samples: {metadata.get('training_samples', 0)}",
                    f"Threshold: {metadata.get('threshold', 0):.3f}",
                    f"",
                    f"Model saved to: {model_path}",
                ]
                panel = Panel("\n".join(content), title="Training Complete", border_style="green")
                console.print(panel)
            else:
                print(f"Model trained successfully: {model_path}")
                print(f"Training samples: {metadata.get('training_samples', 0)}")
                print(f"Threshold: {metadata.get('threshold', 0):.3f}")
        
        return 0
    except Exception as e:
        print(f"Error training model: {e}", file=sys.stderr)
        if state.verbose:
            import traceback
            traceback.print_exc()
        return 1


@drift_app.command(name="check")
def check_drift(
    threshold: float = typer.Option(None, "--threshold", help="Anomaly score threshold (overrides model default)"),
    json: bool = typer.Option(False, "--json", help="JSON output"),
):
    """Check current state for anomalies."""
    try:
        from .ml.detector import AnomalyDetector
        from .ml.trainer import ModelTrainer
        from .ml.features import extract_current_features
        from pathlib import Path
        
        # Get latest model
        trainer = ModelTrainer()
        model_path = trainer.get_latest_model()
        
        if not model_path:
            print("No trained model found. Run 'lil-os drift train' first.", file=sys.stderr)
            return 1
        
        # Load model
        detector = AnomalyDetector(model_path=model_path)
        
        # Extract current features
        current_features = extract_current_features()
        
        # Check for anomalies
        is_anomaly, score = detector.predict(current_features)
        
        # Override threshold if provided
        if threshold is not None:
            is_anomaly = score > threshold
        
        if state.json_output or json:
            import json
            result = {
                "anomaly_detected": is_anomaly,
                "anomaly_score": score,
                "threshold": threshold or detector.threshold,
                "model": model_path.name,
            }
            print(json.dumps(result, indent=2))
            return 2 if is_anomaly else 0
        else:
            console = cli_ux.get_console() if RICH_AVAILABLE else None
            if console:
                from rich.panel import Panel
                status_emoji = "⚠️" if is_anomaly else "✅"
                status_text = "ANOMALY DETECTED" if is_anomaly else "Normal"
                border_style = "red" if is_anomaly else "green"
                
                content = [
                    f"Status: {status_emoji} {status_text}",
                    f"",
                    f"Anomaly Score: {score:.3f}",
                    f"Threshold: {threshold or detector.threshold:.3f}",
                    f"Model: {model_path.name}",
                ]
                
                if is_anomaly:
                    content.extend([
                        "",
                        "Anomalous Patterns Detected:",
                        "  • Review recent changes for potential drift",
                        "  • Consider running 'lil-os check' for reset triggers",
                    ])
                
                panel = Panel("\n".join(content), title="Drift Detection", border_style=border_style)
                console.print(panel)
            else:
                if is_anomaly:
                    print(f"⚠️  ANOMALY DETECTED")
                    print(f"Anomaly Score: {score:.3f} (threshold: {threshold or detector.threshold:.3f})")
                else:
                    print(f"✅ Normal")
                    print(f"Anomaly Score: {score:.3f} (threshold: {threshold or detector.threshold:.3f})")
            
            return 2 if is_anomaly else 0
    except Exception as e:
        print(f"Error checking for drift: {e}", file=sys.stderr)
        if state.verbose:
            import traceback
            traceback.print_exc()
        return 1


@drift_app.command()
def history(
    limit: int = typer.Option(50, "--limit", help="Limit to N recent anomalies"),
    json: bool = typer.Option(False, "--json", help="JSON output"),
):
    """Show anomaly history."""
    # TODO: Implement anomaly history tracking
    # This would require storing anomaly detection results over time
    print("Anomaly history tracking not yet implemented.")
    print("This will show historical anomaly detections.")
    return 0


@drift_app.command()
def reset():
    """Reset model (clear learned patterns)."""
    try:
        from pathlib import Path
        models_dir = Path(".lil_os/ml/models")
        
        if not models_dir.exists():
            print("No models directory found.", file=sys.stderr)
            return 1
        
        # Remove all model files
        model_files = list(models_dir.glob("model_*.pkl"))
        if not model_files:
            print("No models found to reset.", file=sys.stderr)
            return 1
        
        for model_file in model_files:
            model_file.unlink()
            # Also remove metadata file
            metadata_file = model_file.with_suffix(".json")
            if metadata_file.exists():
                metadata_file.unlink()
        
        print(f"Reset complete: removed {len(model_files)} model(s).")
        return 0
    except Exception as e:
        print(f"Error resetting models: {e}", file=sys.stderr)
        return 1


@app.command()
def shell(
    no_daemon: bool = typer.Option(False, "--no-daemon", help="Don't auto-start daemon"),
    session: Optional[str] = typer.Option(None, "--session", help="Load named session"),
):
    """Launch enhanced interactive shell."""
    # TODO: Add session loading
    return shell_enhanced.main()


@app.command()
def info():
    """Show system information."""
    class Args:
        pass
    args = Args()
    return cli.info_command(args)


@app.command()
def version():
    """Show version information."""
    class Args:
        pass
    args = Args()
    return cli.version_command(args)


@app.command()
def health():
    """Quick health check."""
    class Args:
        pass
    args = Args()
    return cli.health_command(args)


@app.command(name="log-decision")
def log_decision():
    """Interactively create a decision log entry."""
    class Args:
        pass
    args = Args()
    return cli.log_decision_command(args)


@app.command()
def help_cmd(
    command: Optional[str] = typer.Argument(None, help="Command to get help for"),
    rule_id: Optional[str] = typer.Option(None, "--explain", help="Explain a rule ID"),
    scenario: Optional[str] = typer.Option(None, "--guide", help="Show scenario guide"),
):
    """Show help information."""
    class Args:
        def __init__(self, command, rule_id, scenario):
            self.command = command
            self.rule_id = rule_id
            self.scenario = scenario
    args = Args(command, rule_id, scenario)
    return cli.help_command(args)


@app.command()
def watch_cmd(
    interval: float = typer.Option(2.0, "--interval", help="Check interval in seconds"),
):
    """Monitor governance files for changes."""
    class Args:
        def __init__(self, interval):
            self.interval = interval
    args = Args(interval)
    return cli.watch_command(args)


@app.command(name="design")
def design():
    """Run the interactive box designer."""
    class Args:
        pass
    args = Args()
    return cli.designer_command(args)


@app.command()
def daemon_cmd(
    action: str = typer.Argument(..., help="Daemon action: start, stop, status, run"),
    config: Optional[str] = typer.Option(None, "--config", help="Path to daemon config file"),
):
    """Manage background daemon."""
    class Args:
        def __init__(self, action, config):
            self.action = action
            self.config = Path(config) if config else None
    args = Args(action, config)
    return cli.daemon_command(args)


@app.command()
def activity(
    limit: int = typer.Option(50, "--limit", help="Maximum number of events to show"),
    type: Optional[str] = typer.Option(None, "--type", help="Filter by event type"),
):
    """Show activity feed."""
    class Args:
        def __init__(self, limit, type):
            self.limit = limit
            self.type = type
    args = Args(limit, type)
    return cli.activity_command(args)


def main():
    """Main entry point for CLI v2."""
    if not TYPER_AVAILABLE:
        # Fallback to old CLI if typer not available
        print("Warning: typer not available, falling back to legacy CLI", file=sys.stderr)
        return cli.main()
    
    try:
        app()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        if state.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
