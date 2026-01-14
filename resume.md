# LIL OS // Product Engineer // New York, NY // Jan 2026 - Present

Technologies: Python, Git/GitHub, CI/CD (GitHub Actions), YAML, Watchdog, Rich, Pre-commit Hooks, Markdown, Figma, JSON, Setuptools, Subprocess, Pathlib, Dataclasses, Threading, Regex

Overview:
Architected and developed LIL OS, a governance framework for AI-assisted software development that prevents unauthorized changes, rule accumulation, and project drift in agentic workflows. Engineered a comprehensive system with automated validation, decision logging, and context budget enforcement to protect developers from complexity creep and maintain project integrity.
Built a production-ready Python package with CLI interface, real-time file monitoring, git integration, and enhanced shell interface featuring live activity feeds and governance decision prompts. Implemented security features including secret detection, integrity checks, and CI/CD enforcement with GitHub Actions integration.
Designed and documented a complete governance framework with 15+ documentation files covering installation, user guides, security architecture, and workflow processes. Created a standardized project structure with rule management system, reset triggers (circuit breakers), and automated validation scripts that catch critical changes before commits.

Key Achievements:
• Architected and developed a complete governance framework system with 22+ Python modules and 15+ documentation files, reducing project complexity creep by enforcing context budgets and automated validation
• Engineered automated validation pipeline with pre-commit hooks and CI/CD integration (GitHub Actions), catching 100% of critical governance file changes before commits and preventing unauthorized modifications
• Implemented real-time monitoring system with file watchers, git monitors, and validation monitors using Watchdog library, providing live activity feeds and governance decision prompts for enhanced developer experience
• Built comprehensive CLI tool with setup wizard, linting, reset checks, and enhanced shell interface, enabling developers to initialize and manage governance in minutes with standardized project structures
• Designed security architecture with secret detection, decision log integrity checks, and governance file change detection, preventing accidental credential exposure and maintaining audit trail accountability
• Created rule management system with unique ID tracking (LIL-<DOC>-<CAT>-<NNNN> format) and lifecycle management, enabling traceable rule evolution and preventing conflicting governance directives
• Developed decision logging framework with temporal legitimacy testing and justification requirements, ensuring all intent-level changes are documented with tradeoff analysis for future reference
• Implemented reset triggers (circuit breakers) that automatically flag complexity growth, repeated failures, and optimization overrides, forcing scope reduction when system behavior becomes unexplainable
• Built Python package distribution with setuptools, pyproject.toml configuration, and pip/pipx installation support, making the framework easily deployable across development environments
• Designed multi-layered enforcement model with pre-commit warnings (non-blocking) and CI/CD validation (non-bypassable), balancing developer autonomy with governance accountability
• Created comprehensive documentation suite including user guides, installation instructions, security architecture, and governance frameworks, supporting both beginner and advanced users
• Engineered event-driven architecture with threading, queues, and event bus system, enabling real-time monitoring and background daemon processes for continuous governance enforcement


