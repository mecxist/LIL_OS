# Installation

## Getting Started (Using Terminal Commands) 

**Manual installation instructions are provided inline with Liberatory Intelligence principles** — we believe in empowering developers with the knowledge and skills to work autonomously in their development environments. These step-by-step terminal instructions help you learn fundamental skills while setting up LIL OS.

**Not quite ready to do things manually yet, or want to get a feel for working within GitHub?** We understand! Read the [User Guide](USER_GUIDE.md) which includes chat prompts you can use with your AI assistant to get guided help through the setup process.

**Want to learn the terminal?** Here are resources to help you get familiar with the terminal within the IDEs we recommend:

Here are the official resources for the IDEs that work best with LIL OS, for reference:
- **Cursor:** [Cursor Terminal Documentation](https://docs.cursor.com/features/terminal) - Learn how to use the integrated terminal in Cursor
- **VS Code:** [VS Code Integrated Terminal Guide](https://code.visualstudio.com/docs/terminal/basics) - Official VS Code terminal documentation
- **JetBrains (IntelliJ, WebStorm, etc.):** [JetBrains Terminal Guide](https://www.jetbrains.com/help/idea/terminal-emulator.html) - Using the terminal in JetBrains IDEs
- **General Terminal Tutorials:** [Command Line Crash Course](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line) - Cross-platform terminal basics

### Step 0: Check if you have Python installed

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
1. **Note:** You don't need a GitHub account to clone the repository, but it's recommended that all developers familiarize themselves with GitHub sooner than later. You can create a free account at [github.com](https://github.com).
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

**Before running the setup wizard, we recommend reading `USER_GUIDE.md`** (especially the "Setting Up LIL OS" section starting around line 38). The User Guide explains what questions the wizard will ask and how to answer them correctly, which is especially helpful if you're new to LIL OS or development tools.

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
1. If you haven't already, read `USER_GUIDE.md` - This beginner-friendly guide explains day-to-day usage and when to log decisions
2. Start using LIL OS in your project - Most of the time, you can code normally!
3. When you make an important decision, log it in `docs/DECISION_LOG.md`

**Remember:** LIL OS only steps in for important decisions. Regular coding works exactly like before!

