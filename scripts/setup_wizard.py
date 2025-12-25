#!/usr/bin/env python3
"""
LIL OS Setup Wizard
Helps users set up LIL OS in their project with an interactive guide.
"""

import os
import sys
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Text colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

def print_header():
    """Print colorful ASCII art header."""
    ascii_art = f"""
{Colors.BRIGHT_CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  {Colors.BRIGHT_WHITE}██╗     ██╗██╗     {Colors.BRIGHT_CYAN}      ██████  ███████     ║
║  {Colors.BRIGHT_WHITE}██║     ██║██║     {Colors.BRIGHT_CYAN}     ██╔═══██╗██╔════╝     ║
║  {Colors.BRIGHT_WHITE}██║     ██║██║     {Colors.BRIGHT_CYAN}     ██║   ██║███████╗     ║
║  {Colors.BRIGHT_WHITE}██║     ██║██║     {Colors.BRIGHT_CYAN}     ██║   ██║╚════██║     ║
║  {Colors.BRIGHT_WHITE}███████╗██║███████╗{Colors.BRIGHT_CYAN}     ╚██████╔╝███████║     ║
║  {Colors.BRIGHT_WHITE}╚══════╝╚═╝╚══════╝{Colors.BRIGHT_CYAN}      ╚═════╝ ╚══════╝     ║
║                                                           ║
║  {Colors.BRIGHT_MAGENTA}        Setup Wizard v0.1.1{Colors.BRIGHT_CYAN}                    ║
║  {Colors.DIM}   A constitutional substrate for AI-assisted{Colors.BRIGHT_CYAN}     ║
║  {Colors.DIM}        software development{Colors.BRIGHT_CYAN}                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(ascii_art)

def check_python_version():
    """Check if Python 3 is available."""
    if sys.version_info < (3, 6):
        print(f"{Colors.BRIGHT_RED}❌ Error: Python 3.6 or higher is required.{Colors.RESET}")
        print(f"{Colors.RED}   Current version: {sys.version}{Colors.RESET}")
        return False
    print(f"{Colors.BRIGHT_GREEN}✅ Python {sys.version_info.major}.{sys.version_info.minor} detected{Colors.RESET}")
    return True

def check_project_structure():
    """Check if we're in a project directory."""
    current_dir = Path.cwd()
    has_git = (current_dir / ".git").exists()
    has_package_json = (current_dir / "package.json").exists()
    has_requirements = (current_dir / "requirements.txt").exists()
    has_pyproject = (current_dir / "pyproject.toml").exists()
    
    print(f"\n{Colors.BRIGHT_BLUE}📁 Current directory: {Colors.CYAN}{current_dir}{Colors.RESET}")
    
    if has_git:
        print(f"{Colors.BRIGHT_GREEN}✅ Git repository detected{Colors.RESET}")
    if has_package_json or has_requirements or has_pyproject:
        print(f"{Colors.BRIGHT_GREEN}✅ Project files detected{Colors.RESET}")
    
    if not (has_git or has_package_json or has_requirements or has_pyproject):
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Warning: This doesn't look like a project directory{Colors.RESET}")
        response = input(f"{Colors.YELLOW}   Continue anyway? (y/n): {Colors.RESET}").strip().lower()
        if response != 'y':
            return False
    
    return True

def create_docs_directory():
    """Create docs directory if it doesn't exist."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        docs_dir.mkdir()
        print(f"{Colors.BRIGHT_GREEN}✅ Created docs/ directory{Colors.RESET}")
    else:
        print(f"{Colors.BRIGHT_GREEN}✅ docs/ directory already exists{Colors.RESET}")
    return docs_dir

def create_decision_log():
    """Create or check decision log."""
    decision_log = Path("docs/DECISION_LOG.md")
    
    if decision_log.exists():
        print(f"{Colors.BRIGHT_GREEN}✅ Decision log already exists{Colors.RESET}")
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
    print(f"{Colors.BRIGHT_GREEN}✅ Created decision log template{Colors.RESET}")

def create_lil_os_directory():
    """Create .lil_os directory for markers."""
    lil_os_dir = Path(".lil_os")
    if not lil_os_dir.exists():
        lil_os_dir.mkdir()
        (lil_os_dir / ".gitkeep").touch()
        print(f"{Colors.BRIGHT_GREEN}✅ Created .lil_os/ directory{Colors.RESET}")
    else:
        print(f"{Colors.BRIGHT_GREEN}✅ .lil_os/ directory already exists{Colors.RESET}")

def check_scripts():
    """Check if LIL OS scripts are available."""
    scripts_dir = Path("scripts")
    rule_id_script = scripts_dir / "lil_os_rule_id_lint.py"
    reset_script = scripts_dir / "lil_os_reset_checks.py"
    
    if rule_id_script.exists() and reset_script.exists():
        print(f"{Colors.BRIGHT_GREEN}✅ LIL OS validation scripts found{Colors.RESET}")
        return True
    else:
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Warning: LIL OS scripts not found in scripts/ directory{Colors.RESET}")
        print(f"{Colors.YELLOW}   You may need to copy them from the LIL OS repository{Colors.RESET}")
        return False

def setup_pre_commit():
    """Offer to set up pre-commit hooks."""
    response = input(f"\n{Colors.BRIGHT_CYAN}🔧 Would you like to set up pre-commit hooks? (y/n): {Colors.RESET}").strip().lower()
    
    if response != 'y':
        print(f"{Colors.DIM}   Skipping pre-commit setup (you can do this later){Colors.RESET}")
        return False
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.BRIGHT_GREEN}✅ Installed pre-commit{Colors.RESET}")
            
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
                print(f"{Colors.BRIGHT_GREEN}✅ Created .pre-commit-config.yaml{Colors.RESET}")
            
            result = subprocess.run(["pre-commit", "install"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Colors.BRIGHT_GREEN}✅ Pre-commit hooks installed{Colors.RESET}")
                return True
            else:
                print(f"{Colors.BRIGHT_YELLOW}⚠️  Could not install pre-commit hooks{Colors.RESET}")
                print(f"{Colors.YELLOW}   Error: {result.stderr}{Colors.RESET}")
        else:
            print(f"{Colors.BRIGHT_YELLOW}⚠️  Could not install pre-commit{Colors.RESET}")
            print(f"{Colors.YELLOW}   Error: {result.stderr}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Error setting up pre-commit: {e}{Colors.RESET}")
    
    return False

def run_validation():
    """Offer to run validation scripts."""
    response = input(f"\n{Colors.BRIGHT_CYAN}🔍 Would you like to run validation scripts now? (y/n): {Colors.RESET}").strip().lower()
    
    if response != 'y':
        print(f"{Colors.DIM}   Skipping validation (you can run them later){Colors.RESET}")
        return
    
    scripts_dir = Path("scripts")
    rule_id_script = scripts_dir / "lil_os_rule_id_lint.py"
    reset_script = scripts_dir / "lil_os_reset_checks.py"
    
    if not (rule_id_script.exists() and reset_script.exists()):
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Validation scripts not found. Skipping.{Colors.RESET}")
        return
    
    try:
        import subprocess
        
        print(f"\n{Colors.BRIGHT_BLUE}   Running rule ID linter...{Colors.RESET}")
        result = subprocess.run([sys.executable, str(rule_id_script)], 
                               capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        print(f"\n{Colors.BRIGHT_BLUE}   Running reset checks...{Colors.RESET}")
        result = subprocess.run([sys.executable, str(reset_script)], 
                               capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        print(f"{Colors.BRIGHT_GREEN}✅ Validation complete{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Error running validation: {e}{Colors.RESET}")

def print_next_steps():
    """Print instructions for next steps."""
    print(f"\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BRIGHT_GREEN}  Setup Complete! 🎉{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"\n{Colors.BRIGHT_BLUE}📚 Next Steps:{Colors.RESET}")
    print(f"{Colors.WHITE}   1. Read docs/USER_GUIDE.md for a beginner-friendly guide{Colors.RESET}")
    print(f"{Colors.WHITE}   2. Read docs/GOVERNANCE.md to understand the rules{Colors.RESET}")
    print(f"{Colors.WHITE}   3. Start coding normally - LIL OS only steps in for important decisions{Colors.RESET}")
    print(f"{Colors.WHITE}   4. When you make an important decision, log it in docs/DECISION_LOG.md{Colors.RESET}")
    print(f"\n{Colors.BRIGHT_MAGENTA}💡 Tip:{Colors.RESET} {Colors.DIM}Copy this prompt to your AI assistant for help:{Colors.RESET}")
    print(f"{Colors.DIM}   'I just set up LIL OS. Can you help me understand when I need to{Colors.RESET}")
    print(f"{Colors.DIM}    log decisions vs when I can just code normally?'{Colors.RESET}")
    print(f"\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}\n")

def main():
    """Main setup wizard flow."""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_project_structure():
        print(f"\n{Colors.BRIGHT_RED}❌ Setup cancelled{Colors.RESET}")
        sys.exit(1)
    
    # Create necessary directories and files
    print(f"\n{Colors.BRIGHT_BLUE}📦 Setting up LIL OS structure...{Colors.RESET}")
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
        print(f"\n\n{Colors.BRIGHT_RED}❌ Setup cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}❌ Error during setup: {e}{Colors.RESET}")
        sys.exit(1)

