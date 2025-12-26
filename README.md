# LIL OS (v0.1.1)

## What and why is LIL OS?

LIL OS is a thoughtfully crafted operating system that helps protect vibecoders, inexperienced developers, and experienced developers who are new to agentic workflows from the seemingly unavoidable headaches that come when agentic tools operate without proper boundaries. Learn more at - https://www.lilco.io

In a nutshell, LIL OS governs **change** (evolution over time) in AI-assisted systems by managing three critical dimensions: **intent** (what your project is meant to do), **authority** (who can make what decisions), and **context** (the rules, instructions, and automation that guide behavior).

Unlike tools that only manage code execution and resources, LIL OS implements a governance layer that prevents AI assistants from making unauthorized changes, accumulating conflicting rules, or drifting from your original goals and intent. By enforcing context budgets, where instructions, rules, memory, and automation are treated as finite resources, LIL OS prevents the complexity creep that causes projects to veer off track. Every new rule must justify its cost, every important decision must get logged, and the system automatically flags when complexity is growing faster than it's being managed.

> In this way, governance is deliberate friction, applied at points of irreversible change because some decisions require justification, not just permission.

## What exactly does LIL OS do?
LIL OS provides a practical starting point for AI-assisted software projects that keeps you from being at the mercy of your agentic tools:

**Key Features:**

- 🚀 **Setup Wizard** 
- 📁 **Standardized Project Structure** 
- ⚖️ **Governance Without Bureaucracy**
- 🏷️ **Rules Management**
- 📝 **File Auditing & Decision Logging**
- 🛑 **Reset Triggers (Circuit Breakers)** 
- 💰 **Context Budgets**
- ✅ **Automated Validation & Pre-commit Hooks**
- ⚙️ **CI/CD Integration**

## IDE Compatibility & Environment Adaptation

LIL OS is **optimized for local development** that uses IDEs with integrated AI agents like Cursor AI, Claude Code, Codex, Gemini CLI, etc. :
- **Cursor** (with Cursor AI) — Free tier available; Pro subscription ~$20/month for unlimited AI usage
- **VS Code** (with GitHub Copilot, Cursor extension, or other AI assistants) — IDE is free; GitHub Copilot is $10/month for individuals (free for students/teachers)
- **JetBrains IDEs** (IntelliJ IDEA, WebStorm, PyCharm, etc. with AI plugins) — Free Community editions available; Professional editions ~$149-199/year for individuals (discounted after first year)

**Claude Pro Subscription Optimization:** If you're a Claude Pro or Max subscriber, we **strongly recommend** using Claude Code directly in your IDE terminal rather than via an API integration. This ensures you benefit from your flat-rate subscription allowance without additional API token charges, while maintaining seamless integration with LIL OS's governance features.

The framework works best in these environments because it relies on:
- File system access for governance documents and decision logs
- Pre-commit hooks for validation
- Terminal access for running validation scripts
- Direct integration with your development workflow

We recommend you research and decide on an IDE and install it, to best implement LIL OS in your next project, before moving on.

**Not using a local IDE with integrated AI agents?** See the [Adapting LIL OS](docs/CONTRIBUTING.md#adapting-lil-os-for-web-based-environments) section in CONTRIBUTING.md for guidance (note: adaptations are done at your own risk and may result in limited functionality).

---

## Getting Started

**Manual installation instructions are provided inline with Liberatory Intelligence principles** — we believe in empowering developers with the knowledge and skills to work autonomously in their development environments.

**Ready to install?** See the [Installation Guide](docs/INSTALLATION_GUIDE.md) for step-by-step terminal instructions that help you learn fundamental skills while setting up LIL OS.

**Not quite ready to do things manually yet, or want to get a feel for working within GitHub?** We understand! Read the [User Guide](docs/USER_GUIDE.md) which includes chat prompts you can use with your AI assistant to get guided help through the setup process.

**First, let's make sure you have Python 3 installed:**

1. Open a terminal:
   - **In your IDE:** Use the integrated terminal (Cursor, VS Code, JetBrains all have built-in terminals)
   - **Or system terminal:** On Mac: press `Cmd + Space`, type "Terminal", press Enter
2. Type this command and press Enter:
   ```bash
   python3 --version
   ```
3. **If you see a version number** (like "Python 3.9.6"): ✅ You're good! Skip to Step 1.
4. **If you see an error** (like "command not found"): You need to install Python first.

**Don't have Python? Here's how to install it:**

**Mac:**
- **Option 1 (Recommended):** If you have Homebrew installed, run this in your terminal:
  ```bash
  brew install python3
  ```
- **Option 2:** Download the installer from [python.org](https://www.python.org/downloads/) and follow the installation wizard

**Windows:**
- Download the installer from [python.org](https://www.python.org/downloads/)
- **Important:** During installation, make sure to check the box that says "Add Python to PATH"
- After installation, close and reopen your terminal, then verify with `python3 --version`

**Linux (Ubuntu/Debian):**
- Run this command in your terminal:
  ```bash
  sudo apt update && sudo apt install python3
  ```
- For other Linux distributions, use your package manager (e.g., `yum` for CentOS/RHEL, `pacman` for Arch)

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

**Option B: Use Git (Highly Recommended)**
1. **Note:** You don't need a GitHub account to clone the repository, but it's recommended that all developers familiarize tthemselves with github sooner than later. You can create a free account at [github.com](https://github.com).
2. **Check if Git is installed:** Open a terminal (IDE terminal or system terminal) and run:
   ```bash
   git --version
   ```
   - **If you see a version number:** ✅ You're good! Skip to step 4.
   - **If you see an error:** You need to install Git first (see instructions below)

4. Navigate to where you want LIL OS (like your Documents folder):
   ```bash
   cd ~/Documents
   ```
5. Copy and paste this command:
   ```bash
   git clone https://github.com/mecxist/LIL_OS.git
   ```
6. Navigate into the folder:
   ```bash
   cd LIL_OS
   ```

**Don't have Git installed? Here's how to install it:**

**Mac:**
- **Option 1 (Recommended):** If you have Homebrew installed, run this in your terminal:
  ```bash
  brew install git
  ```
- **Option 2:** Download the installer from [git-scm.com](https://git-scm.com/download/mac) and follow the installation wizard

**Windows:**
- Download Git for Windows from [git-scm.com](https://git-scm.com/download/win)
- Run the installer and use the default options (they'll set up Git properly)
- After installation, close and reopen your terminal, then verify with `git --version`

**Linux (Ubuntu/Debian):**
- Run this command in your terminal:
  ```bash
  sudo apt update && sudo apt install git
  ```
- For other Linux distributions, use your package manager (e.g., `yum` for CentOS/RHEL, `pacman` for Arch)

**Option C: I already have the files on my computer**
1. Open Terminal
2. Navigate to your LIL_OS folder:
   ```bash
   cd /path/to/your/LIL_OS
   ```
   (Replace `/path/to/your/LIL_OS` with the actual location of your LIL_OS folder)

---



### Step 2: Run the Setup Wizard

**Before running the setup wizard, we recommend reading `docs/USER_GUIDE.md`** (especially the "Setting Up LIL OS" section starting around line 38). The User Guide explains what questions the wizard will ask and how to answer them correctly, which is especially helpful if you're new to LIL OS or development tools.

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

The wizard will ask you a few questions about pre-commit hooks and validation. The User Guide explains what each question means and how to answer it.

---

### What's Next?

After the setup wizard completes:
1. If you haven't already, read `docs/USER_GUIDE.md` - This beginner-friendly guide explains day-to-day usage and when to log decisions
2. Start using LIL OS in your project - Most of the time, you can code normally!
3. When you make an important decision, log it in `docs/DECISION_LOG.md`

**Remember:** LIL OS only steps in for important decisions. Regular coding works exactly like before!

## Documentation

See `docs/` for complete documentation:
- `INSTALLATION_GUIDE.md` — **start here!** Step-by-step installation instructions
- `USER_GUIDE.md` — beginner-friendly guide with examples and chat prompts
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


