#!/usr/bin/env python3
"""
LIL OS Setup Wizard
Helps users set up LIL OS in their project with an interactive guide.
"""

import os
import sys
from pathlib import Path

def print_header():
    print("\n" + "="*60)
    print("  LIL OS Setup Wizard")
    print("  A constitutional substrate for AI-assisted software development")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python 3 is available."""
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_project_structure():
    """Check if we're in a project directory."""
    current_dir = Path.cwd()
    has_git = (current_dir / ".git").exists()
    has_package_json = (current_dir / "package.json").exists()
    has_requirements = (current_dir / "requirements.txt").exists()
    has_pyproject = (current_dir / "pyproject.toml").exists()
    
    print(f"\n📁 Current directory: {current_dir}")
    
    if has_git:
        print("✅ Git repository detected")
    if has_package_json or has_requirements or has_pyproject:
        print("✅ Project files detected")
    
    if not (has_git or has_package_json or has_requirements or has_pyproject):
        print("⚠️  Warning: This doesn't look like a project directory")
        response = input("   Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return False
    
    return True

def create_docs_directory():
    """Create docs directory if it doesn't exist."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        docs_dir.mkdir()
        print("✅ Created docs/ directory")
    else:
        print("✅ docs/ directory already exists")
    return docs_dir

def create_decision_log():
    """Create or check decision log."""
    decision_log = Path("docs/DECISION_LOG.md")
    
    if decision_log.exists():
        print("✅ Decision log already exists")
        return
    
    template = """# Decision Log (v1.0)

## Purpose
Records intent-level decisions that alter meaning, authority, or trajectory. Prevents silent drift.

## What Belongs Here
Required:
- changes governed by GOVERNANCE.md
- emergency overrides
- automation expansions
- metric changes / success-criteria shifts

Not required:
- bug fixes, refactors, style changes

## Required Fields
Each entry MUST include:
- Date:
- Decision:
- Trigger:
- Rationale:
- Tradeoffs:
- Expected Impact:
- Review Date: (recommended; optional if N/A)

---

## Template

<!-- This template is for reference only and should not be parsed as an actual entry -->

```
Date:
Decision:
Trigger:
Rationale:
Tradeoffs:
Expected Impact:
Review Date:
```

---

## Entries

<!-- Actual decision log entries go below this line -->
"""
    
    decision_log.write_text(template, encoding="utf-8")
    print("✅ Created decision log template")

def create_lil_os_directory():
    """Create .lil_os directory for markers."""
    lil_os_dir = Path(".lil_os")
    if not lil_os_dir.exists():
        lil_os_dir.mkdir()
        (lil_os_dir / ".gitkeep").touch()
        print("✅ Created .lil_os/ directory")
    else:
        print("✅ .lil_os/ directory already exists")

def check_scripts():
    """Check if LIL OS scripts are available."""
    scripts_dir = Path("scripts")
    rule_id_script = scripts_dir / "lil_os_rule_id_lint.py"
    reset_script = scripts_dir / "lil_os_reset_checks.py"
    
    if rule_id_script.exists() and reset_script.exists():
        print("✅ LIL OS validation scripts found")
        return True
    else:
        print("⚠️  Warning: LIL OS scripts not found in scripts/ directory")
        print("   You may need to copy them from the LIL OS repository")
        return False

def setup_pre_commit():
    """Offer to set up pre-commit hooks."""
    response = input("\n🔧 Would you like to set up pre-commit hooks? (y/n): ").strip().lower()
    
    if response != 'y':
        print("   Skipping pre-commit setup (you can do this later)")
        return False
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Installed pre-commit")
            
            pre_commit_config = Path(".pre-commit-config.yaml")
            if not pre_commit_config.exists():
                config = """repos:
  - repo: local
    hooks:
      - id: lil-os-rule-id-lint
        name: LIL OS Rule ID Lint
        entry: python3 scripts/lil_os_rule_id_lint.py
        language: system
        pass_filenames: false
        always_run: true
      - id: lil-os-reset-checks
        name: LIL OS Reset Checks
        entry: python3 scripts/lil_os_reset_checks.py
        language: system
        pass_filenames: false
        always_run: true
"""
                pre_commit_config.write_text(config, encoding="utf-8")
                print("✅ Created .pre-commit-config.yaml")
            
            result = subprocess.run(["pre-commit", "install"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Pre-commit hooks installed")
                return True
            else:
                print("⚠️  Could not install pre-commit hooks")
                print(f"   Error: {result.stderr}")
        else:
            print("⚠️  Could not install pre-commit")
            print(f"   Error: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Error setting up pre-commit: {e}")
    
    return False

def run_validation():
    """Offer to run validation scripts."""
    response = input("\n🔍 Would you like to run validation scripts now? (y/n): ").strip().lower()
    
    if response != 'y':
        print("   Skipping validation (you can run them later)")
        return
    
    scripts_dir = Path("scripts")
    rule_id_script = scripts_dir / "lil_os_rule_id_lint.py"
    reset_script = scripts_dir / "lil_os_reset_checks.py"
    
    if not (rule_id_script.exists() and reset_script.exists()):
        print("⚠️  Validation scripts not found. Skipping.")
        return
    
    try:
        import subprocess
        
        print("\n   Running rule ID linter...")
        result = subprocess.run([sys.executable, str(rule_id_script)], 
                               capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        print("\n   Running reset checks...")
        result = subprocess.run([sys.executable, str(reset_script)], 
                               capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        print("✅ Validation complete")
    except Exception as e:
        print(f"⚠️  Error running validation: {e}")

def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "="*60)
    print("  Setup Complete! 🎉")
    print("="*60)
    print("\n📚 Next Steps:")
    print("   1. Read docs/USER_GUIDE.md for a beginner-friendly guide")
    print("   2. Read docs/GOVERNANCE.md to understand the rules")
    print("   3. Start coding normally - LIL OS only steps in for important decisions")
    print("   4. When you make an important decision, log it in docs/DECISION_LOG.md")
    print("\n💡 Tip: Copy this prompt to your AI assistant for help:")
    print("   'I just set up LIL OS. Can you help me understand when I need to")
    print("    log decisions vs when I can just code normally?'")
    print("\n" + "="*60 + "\n")

def main():
    """Main setup wizard flow."""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_project_structure():
        print("\n❌ Setup cancelled")
        sys.exit(1)
    
    # Create necessary directories and files
    print("\n📦 Setting up LIL OS structure...")
    create_docs_directory()
    create_decision_log()
    create_lil_os_directory()
    check_scripts()
    
    # Optional setup
    setup_pre_commit()
    run_validation()
    
    # Final instructions
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

