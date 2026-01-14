#!/usr/bin/env python3
"""
LIL OS² Setup Wizard
Helps users set up LIL OS² in their project with an interactive guide.
"""

import os
import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import shared utilities
from lil_os_utils import Colors, load_simple_yaml

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
    """Check if LIL OS² scripts are available."""
    scripts_dir = Path("scripts")
    rule_id_script = scripts_dir / "lil_os_rule_id_lint.py"
    reset_script = scripts_dir / "lil_os_reset_checks.py"
    
    if rule_id_script.exists() and reset_script.exists():
        print(f"{Colors.BRIGHT_GREEN}✅ LIL OS² validation scripts found{Colors.RESET}")
        return True
    else:
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Warning: LIL OS² scripts not found in scripts/ directory{Colors.RESET}")
        print(f"{Colors.YELLOW}   You may need to copy them from the LIL OS² repository{Colors.RESET}")
        return False

def setup_pre_commit():
    """Offer to set up pre-commit hooks with clear explanation."""
    print(f"\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  Pre-commit Hooks Setup{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"\n{Colors.WHITE}Pre-commit hooks automatically check your code before you commit.{Colors.RESET}")
    print(f"\n{Colors.BRIGHT_GREEN}Benefits:{Colors.RESET}")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Warns you about critical changes (governance files, missing decision logs)")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Helps keep your documentation tidy when using multiple AI agents")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Catches problems before they're committed")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Safer collaboration with others")
    print(f"\n{Colors.BRIGHT_YELLOW}Important:{Colors.RESET}")
    print(f"  {Colors.YELLOW}•{Colors.RESET} Hooks provide {Colors.BOLD}warnings{Colors.RESET}, not blocks (you can still commit)")
    print(f"  {Colors.YELLOW}•{Colors.RESET} You can bypass with {Colors.DIM}git commit --no-verify{Colors.RESET} if needed")
    print(f"  {Colors.YELLOW}•{Colors.RESET} Designed to help inexperienced developers, not restrict experienced ones")
    print(f"\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    
    response = input(f"\n{Colors.BRIGHT_CYAN}🔧 Would you like to set up pre-commit hooks? (y/n): {Colors.RESET}").strip().lower()
    
    if response != 'y':
        print(f"\n{Colors.DIM}   Skipping pre-commit setup (you can do this later){Colors.RESET}")
        print(f"{Colors.DIM}   You can set it up manually by running: pip install pre-commit && pre-commit install{Colors.RESET}")
        return False
    
    try:
        import subprocess
        print(f"\n{Colors.BRIGHT_BLUE}📦 Installing pre-commit...{Colors.RESET}")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.BRIGHT_GREEN}✅ Installed pre-commit{Colors.RESET}")
            
            pre_commit_config = Path(".pre-commit-config.yaml")
            if not pre_commit_config.exists():
                config = """repos:
  - repo: local
    hooks:
      - id: lil-os-critical-change-warning
        name: LIL OS² Critical Change Warning
        entry: python3 scripts/lil_os_critical_change_warning.py --pre-commit
        language: system
        pass_filenames: false
        always_run: true
        verbose: true
      - id: lil-os-rule-id-lint
        name: LIL OS² Rule ID Lint
        entry: python3 scripts/lil_os_rule_id_lint.py
        language: system
        pass_filenames: false
        always_run: true
      - id: lil-os-reset-checks
        name: LIL OS² Reset Checks
        entry: python3 scripts/lil_os_reset_checks.py
        language: system
        pass_filenames: false
        always_run: true
"""
                pre_commit_config.write_text(config, encoding="utf-8")
                print(f"{Colors.BRIGHT_GREEN}✅ Created .pre-commit-config.yaml{Colors.RESET}")
            else:
                print(f"{Colors.BRIGHT_YELLOW}⚠️  .pre-commit-config.yaml already exists{Colors.RESET}")
                print(f"{Colors.YELLOW}   You may want to manually add the LIL OS² hooks{Colors.RESET}")
            
            print(f"\n{Colors.BRIGHT_BLUE}📝 Installing git hooks...{Colors.RESET}")
            result = subprocess.run(["pre-commit", "install"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Colors.BRIGHT_GREEN}✅ Pre-commit hooks installed successfully!{Colors.RESET}")
                print(f"\n{Colors.BRIGHT_MAGENTA}💡 Tip:{Colors.RESET} {Colors.DIM}The hooks will now run automatically before each commit.{Colors.RESET}")
                print(f"{Colors.DIM}   They'll warn you about important changes but won't block your commits.{Colors.RESET}")
                return True
            else:
                print(f"{Colors.BRIGHT_YELLOW}⚠️  Could not install pre-commit hooks{Colors.RESET}")
                print(f"{Colors.YELLOW}   Error: {result.stderr}{Colors.RESET}")
                print(f"{Colors.YELLOW}   You can try running 'pre-commit install' manually{Colors.RESET}")
        else:
            print(f"{Colors.BRIGHT_YELLOW}⚠️  Could not install pre-commit{Colors.RESET}")
            print(f"{Colors.YELLOW}   Error: {result.stderr}{Colors.RESET}")
            print(f"{Colors.YELLOW}   You may need to install it manually: pip install pre-commit{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.BRIGHT_YELLOW}⚠️  Error setting up pre-commit: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}   You can set it up manually later{Colors.RESET}")
    
    return False

def setup_reporting():
    """Configure reporting options."""
    print(f"\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  Reporting Configuration{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"\n{Colors.WHITE}LIL OS² can generate reports of validation results.{Colors.RESET}")
    print(f"\n{Colors.BRIGHT_GREEN}Benefits:{Colors.RESET}")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Track validation history over time")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Debug issues with detailed reports")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Audit trail for compliance")
    print(f"\n{Colors.BRIGHT_YELLOW}Note:{Colors.RESET}")
    print(f"  {Colors.YELLOW}•{Colors.RESET} Reports are saved to {Colors.DIM}.lil_os/reports/{Colors.RESET}")
    print(f"  {Colors.YELLOW}•{Colors.RESET} You can enable/disable this later in config files")
    print(f"  {Colors.YELLOW}•{Colors.RESET} Reports are excluded from git by default")
    print(f"{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    
    response = input(f"\n{Colors.BRIGHT_CYAN}📊 Enable report generation? (y/n): {Colors.RESET}").strip().lower()
    
    enable_reports = response == 'y'
    
    # Update reset checks config
    reset_config_path = Path("lil_os.reset_checks.yaml")
    if reset_config_path.exists():
        try:
            config = load_simple_yaml(reset_config_path)
            if "reporting" not in config:
                config["reporting"] = {}
            
            config["reporting"]["generate_reports"] = enable_reports
            config["reporting"]["report_format"] = ["json", "markdown"]
            config["reporting"]["report_location"] = ".lil_os/reports"
            config["reporting"]["show_startup_banner"] = True
            config["reporting"]["show_success_message"] = True
            config["reporting"]["show_timing"] = True
            
            # Write updated config (simple YAML writer)
            write_simple_yaml(reset_config_path, config)
            print(f"{Colors.BRIGHT_GREEN}✅ Updated lil_os.reset_checks.yaml{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.BRIGHT_YELLOW}⚠️  Could not update reset checks config: {e}{Colors.RESET}")
    
    # Update rule ID config
    rule_id_config_path = Path("lil_os.rule_id.yaml")
    if rule_id_config_path.exists():
        try:
            config = load_simple_yaml(rule_id_config_path)
            if "reporting" not in config:
                config["reporting"] = {}
            
            config["reporting"]["generate_reports"] = enable_reports
            config["reporting"]["report_format"] = ["json", "markdown"]
            config["reporting"]["report_location"] = ".lil_os/reports"
            config["reporting"]["show_startup_banner"] = True
            config["reporting"]["show_success_message"] = True
            config["reporting"]["show_timing"] = True
            
            write_simple_yaml(rule_id_config_path, config)
            print(f"{Colors.BRIGHT_GREEN}✅ Updated lil_os.rule_id.yaml{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.BRIGHT_YELLOW}⚠️  Could not update rule ID config: {e}{Colors.RESET}")
    
    if enable_reports:
        print(f"\n{Colors.BRIGHT_MAGENTA}💡 Tip:{Colors.RESET} {Colors.DIM}Reports will be saved to .lil_os/reports/ after each validation run.{Colors.RESET}")
    else:
        print(f"\n{Colors.DIM}   Reporting disabled. You can enable it later by editing the config files.{Colors.RESET}")

def write_simple_yaml(path: Path, data: dict):
    """Simple YAML writer - appends reporting section to existing file."""
    # Read existing content
    existing_content = path.read_text(encoding="utf-8") if path.exists() else ""
    
    # Remove existing reporting section if present
    lines = existing_content.splitlines()
    new_lines = []
    skip_until_empty = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith("reporting:"):
            skip_until_empty = True
            continue
        if skip_until_empty:
            if line.strip() == "" and i < len(lines) - 1 and lines[i + 1].strip() != "":
                skip_until_empty = False
            continue
        new_lines.append(line)
    
    # Remove trailing empty lines
    while new_lines and new_lines[-1].strip() == "":
        new_lines.pop()
    
    # Add reporting section
    if new_lines and new_lines[-1].strip() != "":
        new_lines.append("")
    
    new_lines.append("reporting:")
    new_lines.append(f"  generate_reports: {str(data['reporting']['generate_reports']).lower()}")
    # Format list properly
    report_format = data['reporting']['report_format']
    if isinstance(report_format, list):
        new_lines.append("  report_format:")
        for item in report_format:
            new_lines.append(f"    - \"{item}\"")
    else:
        new_lines.append(f"  report_format: {report_format}")
    new_lines.append(f"  report_location: \"{data['reporting']['report_location']}\"")
    new_lines.append(f"  keep_reports_days: {data['reporting'].get('keep_reports_days', 30)}")
    new_lines.append(f"  show_startup_banner: {str(data['reporting']['show_startup_banner']).lower()}")
    new_lines.append(f"  show_success_message: {str(data['reporting']['show_success_message']).lower()}")
    new_lines.append(f"  show_timing: {str(data['reporting']['show_timing']).lower()}")
    
    path.write_text("\n".join(new_lines), encoding="utf-8")

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
    print(f"{Colors.WHITE}   3. Start coding normally - LIL OS² only steps in for important decisions{Colors.RESET}")
    print(f"{Colors.WHITE}   4. When you make an important decision, log it in docs/DECISION_LOG.md{Colors.RESET}")
    print(f"\n{Colors.BRIGHT_MAGENTA}💡 Tip:{Colors.RESET} {Colors.DIM}Copy this prompt to your AI assistant for help:{Colors.RESET}")
    print(f"{Colors.DIM}   'I just set up LIL OS². Can you help me understand when I need to{Colors.RESET}")
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
    print(f"\n{Colors.BRIGHT_BLUE}📦 Setting up LIL OS² structure...{Colors.RESET}")
    create_docs_directory()
    create_decision_log()
    create_lil_os_directory()
    check_scripts()
    
    # Optional setup
    setup_pre_commit()
    setup_reporting()
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

