# LIL OS (v0.1.1)

## What and why is LIL OS?

LIL OS is a thoughtfully crafted operating system that helps protect vibecoders, inexperienced developers, and experienced developers who are new to agentic workflows from the seemingly unavoidable headaches that come when agentic tools operate without proper boundaries. Learn more at - https://www.lilco.io

In a nutshell, LIL OS governs **change** (evolution over time) in AI-assisted systems by managing three critical dimensions: **intent** (what your project is meant to do), **authority** (who can make what decisions), and **context** (the rules, instructions, and automation that guide behavior).

Unlike tools that only manage code execution and resources, LIL OS implements a governance layer that prevents AI assistants from making unauthorized changes, accumulating conflicting rules, or drifting from your original goals and intent. By enforcing context budgets, where instructions, rules, memory, and automation are treated as finite resources, LIL OS prevents the complexity creep that causes projects to become unmanageable. Every new rule must justify its cost, every important decision must get logged, and the system automatically flags when complexity is growing faster than it's being managed.

> In this way, governance is deliberate friction, applied at points of irreversible change because some decisions require justification, not just permission.

## What exactly does LIL OS do?
LIL OS gives you a set of practical tools to keep your AI-assisted projects under your control:

**Key Features:**

- **Setup Wizard** — Get started in minutes! The setup wizard walks you through initializing LIL OS, configuring governance rules, and setting up validation. Read the User Guide first to understand how your setup choices impact your system design.

- **Standardized Project Structure** — Organized governance from day one. LIL OS provides a best-practices directory and file structure that keeps all governance files, rules, decision logs, and validation scripts in the right places. Your team and AI assistants can find and enforce rules consistently—no more wondering where things belong.

- **Governance Without Bureaucracy** — Only important changes need governance (changes to goals, authority, or automation). Regular code changes work exactly like before—no red tape for everyday development.

- **Rules Management** — Every rule has a unique ID (like `LIL-CR-PROCESS-0001`) for tracking, finding, and monitoring changes. No more hunting through documentation to figure out what rule applies where.

- **File Auditing & Decision Logging** — Every important decision gets logged with who made it, why, and what tradeoffs were considered. Six months from now, you'll know exactly why a decision was made and whether it still makes sense. Perfect for teams or when you need to explain your choices.

- **Reset Triggers (Circuit Breakers)** — Automatic safety nets that pause and force scope reduction when: rules are added faster than removed, failures repeat without clear cause, the system can't explain its behavior, or optimization overrides important tradeoffs.

- **Context Budgets** — Prevent rule bloat and complexity creep. Every new rule, instruction, or piece of automation must justify its cost, keeping your system understandable and maintainable instead of accumulating layers of complexity.

- **Automated Validation & Pre-commit Hooks** — Catch problems before they become problems. Run validation scripts manually or set up pre-commit hooks to automatically check rule formatting, decision log completeness, reset triggers, and context budget compliance.

- **CI/CD Integration** — Works with your existing workflow. GitHub Actions integration means validation runs automatically on every push, keeping the whole team in sync without extra effort.

## IDE Compatibility & Environment Adaptation

LIL OS is **optimized for local development** that uses IDEs with integrated AI agents like Cursor AI, Claude Code, Codex, Gemini CLI, etc. :
- **Cursor** (with Cursor AI)
- **VS Code** (with GitHub Copilot, Cursor extension, or other AI assistants)
- **JetBrains IDEs** (IntelliJ IDEA, WebStorm, PyCharm, etc. with AI plugins)

**Claude Pro Subscription Optimization:** If you're a Claude Pro or Max subscriber, we **strongly recommend** using Claude Code directly in your IDE terminal rather than via an API integration. This ensures you benefit from your flat-rate subscription allowance without additional API token charges, while maintaining seamless integration with LIL OS's governance features.

The framework works best in these environments because it relies on:
- File system access for governance documents and decision logs
- Pre-commit hooks for validation
- Terminal access for running validation scripts
- Direct integration with your development workflow

**Not using a local IDE with integrated AI agents?** See the [Adapting LIL OS](docs/CONTRIBUTING.md#adapting-lil-os-for-web-based-environments) section in CONTRIBUTING.md for guidance (note: adaptations are done at your own risk and may result in limited functionality).


## Quick Start

### Step 0: Check if you have Python installed

**First, let's make sure you have Python 3 installed:**

1. Open your terminal (on Mac: press `Cmd + Space`, type "Terminal", press Enter)
2. Type this command and press Enter:
   ```bash
   python3 --version
   ```
3. **If you see a version number** (like "Python 3.9.6"): ✅ You're good! Skip to Step 1.
4. **If you see an error** (like "command not found"): You need to install Python first.

**Don't have Python? Here's how to install it:**
- **Mac:** Download from [python.org](https://www.python.org/downloads/) or install Homebrew first, then run `brew install python3`
- **Windows:** Download from [python.org](https://www.python.org/downloads/) - make sure to check "Add Python to PATH" during installation
- **Linux:** Run `sudo apt install python3` (Ubuntu/Debian) or use your package manager

---

### Step 1: Get the LIL OS files

**Choose one option:**

**Option A: Download from GitHub (Easiest)**
1. Go to https://github.com/mecxist/LIL_OS
2. Click the green "Code" button
3. Click "Download ZIP"
4. Unzip the file to a location you can find (like your Desktop or Documents folder)
5. Open Terminal and navigate to the folder:
   ```bash
   cd ~/Downloads/LIL_OS-main
   ```
   (Replace `Downloads` with wherever you saved the file)

**Option B: Use Git (if you have it installed)**
1. Open Terminal
2. Navigate to where you want LIL OS (like your Documents folder):
   ```bash
   cd ~/Documents
   ```
3. Copy and paste this command:
   ```bash
   git clone https://github.com/mecxist/LIL_OS.git
   ```
4. Navigate into the folder:
   ```bash
   cd LIL_OS
   ```

**Option C: I already have the files on my computer**
1. Open Terminal
2. Navigate to your LIL_OS folder:
   ```bash
   cd /path/to/your/LIL_OS
   ```
   (Replace `/path/to/your/LIL_OS` with the actual location of your LIL_OS folder)

---

### Step 2: Run the Setup Wizard

**Now that you're in the LIL_OS folder, run the setup wizard:**

```bash
python3 scripts/setup_wizard.py
```

**What this command does:**
- `python3` - Runs Python 3
- `scripts/setup_wizard.py` - The setup wizard script that will guide you through configuration

**If you get an error:**
- Make sure you're in the LIL_OS folder (check with `pwd` command)
- Make sure Python 3 is installed (go back to Step 0)
- Try `python scripts/setup_wizard.py` instead (some systems use `python` instead of `python3`)

The wizard will ask you a few questions and set everything up automatically!

---

### Alternative: Let Your AI Assistant Help You

**If you're not comfortable with the terminal (yet), copy this prompt to your AI assistant:**

```
I want to set up LIL OS in my project. Please help me step by step:

1. First, check if Python 3 is installed on my system by having me run: python3 --version
2. If Python isn't installed, guide me through installing it for my operating system
3. Help me download or clone the LIL OS repository from https://github.com/mecxist/LIL_OS
4. Navigate to the LIL_OS folder in terminal
5. Run the setup wizard: python3 scripts/setup_wizard.py
6. Guide me through answering the setup wizard's questions
7. Explain what each step does in simple terms

Start with step 1 and wait for me to confirm before moving to the next step.
```

Your AI assistant will walk you through everything!

**Want to learn the terminal?** Here are resources for the IDEs that work best with LIL OS:
- **Cursor:** [Cursor Terminal Documentation](https://docs.cursor.com/features/terminal) - Learn how to use the integrated terminal in Cursor
- **VS Code:** [VS Code Integrated Terminal Guide](https://code.visualstudio.com/docs/terminal/basics) - Official VS Code terminal documentation
- **JetBrains (IntelliJ, WebStorm, etc.):** [JetBrains Terminal Guide](https://www.jetbrains.com/help/idea/terminal-emulator.html) - Using the terminal in JetBrains IDEs
- **General Terminal Tutorials:** [Command Line Crash Course](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line) - Cross-platform terminal basics

---

### What's Next?

After the setup wizard completes:
1. Read `docs/USER_GUIDE.md` - This is a beginner-friendly guide that explains everything
2. Start using LIL OS in your project - Most of the time, you can code normally!
3. When you make an important decision, log it in `docs/DECISION_LOG.md`

**Remember:** LIL OS only steps in for important decisions. Regular coding works exactly like before!

## Documentation

**New to LIL OS?** Start with `docs/USER_GUIDE.md` — a beginner-friendly guide written in plain language.

See `docs/` for complete documentation:
- `USER_GUIDE.md` — **start here!** Beginner-friendly guide with examples
- `CONTRIBUTING.md` — how to contribute, join the collective, and adapt LIL OS for web-based environments
- `GOVERNANCE.md` — governance framework
- `CONTEXT_BUDGET.md` — context scarcity doctrine
- `RESET_TRIGGERS.md` — circuit breaker conditions
- `DECISION_LOG.md` — decision logging template
- `MASTER_RULES.md` — non-negotiable boundaries

## Contributing

Anyone can contribute bug fixes, documentation, and examples. Intent-level changes (governance, rules, philosophy) require Official Contributor status. See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

## License

See [LICENSE.md](LICENSE.md) for license information.


