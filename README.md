# LIL OS (v0.1.1)

## What and why is LIL OS?

LIL OS is a thoughtfully designed operating system that helps protect vibecoders, inexperienced developers, and experienced developers who are new to agentic workflows from the seemingly unavoidable headaches that come when agentic tools operate without properly established boundaries. Learn more at https://www.lilco.io

In a nutshell, LIL OS governs **change** (evolution over time) in AI-assisted systems by managing three critical dimensions: **intent** (what your project is meant to do), **authority** (who can make what decisions), and **context** (the rules, instructions, and automation that guide behavior).

Unlike tools that only manage code execution and resources, LIL OS implements a governance layer that prevents AI assistants from making unauthorized changes, accumulating conflicting rules, or drifting from your original goals and intent. By enforcing context budgets, where instructions, rules, memory, and automation are treated as finite resources, LIL OS prevents the complexity creep that causes projects to veer off track. Every new rule must justify its cost, every important decision must get logged, and the system automatically flags when complexity is growing faster than it's being managed.

> In this way, governance is deliberate friction, applied at points of irreversible change because some decisions require justification, not just permission.

## What exactly does LIL OS do?
LIL OS provides a practical starting point for AI-assisted software projects that keeps you from being at the mercy of your agentic tools:

**Key Features:**

- 🚀 **Setup Wizard** - Get started in minutes! The setup wizard walks you through initializing LIL OS, configuring governance rules, and setting up validation. Read the User Guide first to understand how your setup choices impact your system design.

- 📁 **Standardized Project Structure** - Organized governance from day one. LIL OS provides a best-practices directory and file structure that keeps all governance files, rules, decision logs, and validation scripts in the right places. Your team and AI assistants can find and enforce rules consistently. No more wondering where things belong.

- ⚖️ **Governance With Smart Enforcement** - Only important changes need governance (changes to goals, authority, or automation). Regular code changes work exactly like before. No red tape for everyday development. When governance is required, LIL OS automatically ensures all governance file changes are properly documented with decision log entries. Validation fails if critical governance files are modified without corresponding documentation.

- 🏷️ **Rules Management** - Every rule has a unique ID (like `LIL-CR-PROCESS-0001`) for tracking, finding, and monitoring changes. No more hunting through documentation to figure out what rule applies where.

- 📝 **File Auditing & Decision Logging** - Every important decision gets logged with who made it, why, and what tradeoffs were considered. Six months from now, you'll know exactly why a decision was made and whether it still makes sense. Perfect for teams or when you need to explain your choices.

- 🛑 **Reset Triggers (Circuit Breakers)** - Automatic safety nets that pause and force scope reduction when: rules are added faster than removed, failures repeat without clear cause, the system can't explain its behavior, or optimization overrides important tradeoffs.

- 💰 **Context Budgets** - Prevent rule bloat and complexity creep. Every new rule, instruction, or piece of automation must justify its cost, keeping your system understandable and maintainable instead of accumulating layers of complexity.

- ✅ **Automated Validation & Pre-commit Hooks** - Catch problems before they become problems. Run validation scripts manually or set up pre-commit hooks to automatically check rule formatting, decision log completeness, reset triggers, and context budget compliance. Pre-commit hooks provide **warnings** (not blocks) to help inexperienced developers catch critical changes before committing, especially useful when using multiple AI agents or collaborating with others.

- 🔒 **Secret Detection** - Automatically scans decision logs and governance files for accidentally committed secrets like API keys, tokens, passwords, and credentials. Prevents sensitive information from being exposed in version control. If secrets are detected, validation fails immediately, protecting your project and your team.

- ⚙️ **CI/CD Integration** - Works with your existing workflow. GitHub Actions integration means validation runs automatically on every push, keeping the whole team in sync without extra effort.

## IDE Compatibility & Environment Adaptation

LIL OS is **optimized for local development** that uses IDEs with integrated AI agents like Cursor AI, Claude Code, Codex, Gemini CLI, etc.:
- **Cursor** (with Cursor AI) - Free tier available; Pro subscription ~$20/month for unlimited AI usage
- **VS Code** (with GitHub Copilot, Cursor extension, or other AI assistants) - IDE is free; GitHub Copilot is $10/month for individuals (free for students/teachers)
- **JetBrains IDEs** (IntelliJ IDEA, WebStorm, PyCharm, etc. with AI plugins) - Free Community editions available; Professional editions ~$149-199/year for individuals (discounted after first year)

**Claude Pro Subscription Optimization:** If you're a Claude Pro or Max subscriber, we **strongly recommend** using Claude Code directly in your IDE terminal rather than via an API integration. This ensures you benefit from your flat-rate subscription allowance without additional API token charges, while maintaining seamless integration with LIL OS's governance features.

The framework works best in these environments because it relies on:
- File system access for governance documents and decision logs
- Pre-commit hooks for validation
- Terminal access for running validation scripts
- Direct integration with your development workflow

We recommend you research and decide on an IDE, then install it to best implement LIL OS in your next project before moving on.

**Not using a local IDE with integrated AI agents?** See the [Adapting LIL OS](docs/CONTRIBUTING.md#adapting-lil-os-for-web-based-environments) section in CONTRIBUTING.md for guidance (note: adaptations are done at your own risk and may result in limited functionality).

## Getting Started (Using Terminal Commands) 

**We provide manual installation instructions because we believe in developer autonomy**, a core principle of Liberatory Intelligence. These step-by-step terminal instructions equip you with fundamental skills while setting up LIL OS, ensuring you understand your tools rather than just using them. See the [Installation Guide](docs/INSTALLATION.md) for complete setup instructions which include:

Step 0: Check for or Install Python
Step 1: Get the LIL OS files (various methods for Mac, PC & Linux)
Step 2: Run the Setup Wizard

**Not quite ready to do things manually yet, and want to quickly get a feel for working within GitHub?** We understand! Read the [User Guide](docs/USER_GUIDE.md) which includes chat prompts you can use with your preferred AI assistant to get guided help through the setup process.

**Ready to learn the terminal?** Here are resources to help you get familiar with the terminal within the IDEs we recommend:

Here are the official resources for the IDEs that work best with LIL OS, for reference:
- **Cursor:** [Cursor Terminal Documentation](https://docs.cursor.com/features/terminal) - Learn how to use the integrated terminal in Cursor
- **VS Code:** [VS Code Integrated Terminal Guide](https://code.visualstudio.com/docs/terminal/basics) - Official VS Code terminal documentation
- **JetBrains (IntelliJ, WebStorm, etc.):** [JetBrains Terminal Guide](https://www.jetbrains.com/help/idea/terminal-emulator.html) - Using the terminal in JetBrains IDEs
- **General Terminal Tutorials:** [Command Line Crash Course](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line) - Cross-platform terminal basics

## Documentation

See `docs/` for complete documentation:
- `USER_GUIDE.md` - **start here!** Beginner-friendly guide with examples
- `INSTALLATION.md` - step-by-step installation instructions
- `DEPLOYMENT.md` - guidelines for excluding LIL OS components when packaging or deploying
- `CONTRIBUTING.md` - how to contribute, join the collective, and adapt LIL OS for web-based environments
- `GOVERNANCE.md` - governance framework
- `GOVERNANCE_HOOKS.md` - domain-specific governance hooks (API, Architecture, Auth, Data, Performance, Quality, Systems)
- `CONTEXT_BUDGET.md` - context scarcity doctrine
- `RESET_TRIGGERS.md` - circuit breaker conditions
- `DECISION_LOG.md` - decision logging template
- `MASTER_RULES.md` - non-negotiable boundaries
- `CONTEXT_HIERARCHY.md` - guidance for AI agents on efficient context loading

## How LIL OS Enforces Governance

LIL OS provides **governance patterns and validation**, not runtime enforcement. This means:

- **Pre-commit hooks provide warnings** - They alert you to critical changes (like modifying governance files without decision log entries) but don't block your commits. You can bypass with `git commit --no-verify` if needed.
- **Validation happens at commit time** - The system checks your changes before they're committed, catching issues early without restricting your workflow.
- **Designed for safety, not restriction** - The system is designed to help inexperienced developers catch important decisions before committing, keep documentation tidy when using multiple AI agents, and collaborate more safely with others.
- **Can be bypassed** - All validation can be bypassed if needed. The system provides accountability through decision logging, not technical prevention.

**Why this approach?** LIL OS follows the principle that "governance is memory, not control." The system creates friction and accountability through validation and decision logging, not by technically preventing actions. This aligns with Liberatory Intelligence principles of preserving human agency while providing helpful safeguards.

For teams using pull requests, CI/CD provides additional enforcement that cannot be bypassed. See [SECURITY.md](docs/SECURITY.md) for details on the security architecture.

## Contributing

Anyone can contribute bug fixes, documentation, and examples. Intent-level changes (governance, rules, philosophy) require Official Contributor status. See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

## License

See [LICENSE.md](LICENSE.md) for license information.


