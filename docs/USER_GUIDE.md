# LIL OS User Guide

Welcome to LIL OS! This guide will walk you through everything you need to know to get started, written in plain language that anyone can understand.

## What is LIL OS? (In Simple Terms)

Think of LIL OS like a safety system for your AI assistant. Just like a car has seatbelts and airbags to keep you safe, LIL OS has rules and checks to make sure your AI doesn't make changes that could cause problems later.

**The main idea:** Your AI assistant is powerful, but sometimes it might make decisions you didn't want it to make. LIL OS helps you catch those decisions before they become problems.

## Who Should Use This Guide?

This guide is for:
- People who are new to using AI assistants for coding
- Developers who want to use AI but are worried about losing control
- Anyone who wants to understand what LIL OS does without reading technical documentation

If you're comfortable with coding and just want the technical details, check out the other documentation files in the `docs/` folder.

---

## Part 1: Getting Started

### Step 1: What You Need

Before you start, make sure you have:
- A computer (Mac, Windows, or Linux)
- Python 3 installed (most computers already have this)
- An AI assistant like Cursor, GitHub Copilot, or ChatGPT
- A project where you want to use LIL OS

**How to check if you have Python 3:**
1. Open your terminal (on Mac) or command prompt (on Windows)
2. Type: `python3 --version`
3. If you see a version number (like "Python 3.9.0"), you're good to go!
4. If you get an error, you'll need to install Python 3 first

### Alternative: Getting Set Up (Using Chat Prompts)

**Not comfortable with terminal commands yet?** That's okay! You can use your AI assistant to guide you through the setup process. Copy and paste this prompt to your AI assistant:

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

Your AI assistant will walk you through everything! This is a great way to learn while getting help, and you'll gradually become more comfortable with terminal commands.

### Step 2: Setting Up LIL OS

The easiest way to get started is using the setup wizard. This is also a great opportunity to get familiar with using terminal commands in your IDE!

**Open the terminal in your IDE** (Cursor, VS Code, and JetBrains all have built-in terminals - this is a good skill to learn). Make sure you're in the LIL_OS folder, then copy and paste this command:

```bash
python3 scripts/setup_wizard.py
```

**What you're doing:** You're running a Python script that will guide you through setting up LIL OS. Even though you're copying and pasting the command, you're learning how to run scripts in the terminal - a fundamental skill for developers.

The setup wizard will ask you a few simple questions. Here's what each question means and how to answer:

**Question 1: "Continue anyway? (y/n)"**
- **When you'll see this:** Only if the wizard doesn't detect a project directory (no `.git` folder, `package.json`, `requirements.txt`, or `pyproject.toml`)
- **What it means:** The wizard thinks you might not be in a project folder, but you can still set up LIL OS here
- **How to answer:**
  - Type `y` and press Enter if you want to set up LIL OS in this folder anyway
  - Type `n` and press Enter if you want to cancel and navigate to your project folder first
- **Recommendation:** If you're setting up LIL OS in a new project that doesn't have these files yet, type `y`. If you're in the wrong folder, type `n` and navigate to your project folder first.

**Question 2: "Would you like to set up pre-commit hooks? (y/n)"**
- **What it means:** Pre-commit hooks automatically check your code before you commit changes. This helps catch problems early.
- **How to answer:**
  - Type `y` and press Enter if you want automatic checks (recommended for most users)
  - Type `n` and press Enter if you prefer to run checks manually
- **Recommendation:** Type `y` if you're new to LIL OS - it helps prevent mistakes. You can always disable it later if needed.

**Question 3: "Would you like to run validation scripts now? (y/n)"**
- **What it means:** The wizard can test that everything is set up correctly right away
- **How to answer:**
  - Type `y` and press Enter to verify your setup works (recommended)
  - Type `n` and press Enter to skip this check
- **Recommendation:** Type `y` to make sure everything is working correctly before you start using LIL OS.

Just answer the questions, and the wizard will set everything up for you!

### Step 3: Understanding the Basics

Once LIL OS is set up, you'll have a few new files in your project:
- `docs/DECISION_LOG.md` - This is where important decisions get recorded
- `docs/GOVERNANCE.md` - This explains the rules
- `scripts/` folder - These are the tools that check your project

**Don't worry** - you don't need to read all these files right away. LIL OS will remind you when you need to do something.

---

## Part 2: Using LIL OS Day-to-Day

### Normal Coding (No Extra Steps Needed)

Here's the good news: **most of the time, you can code exactly like you always have!**

When you're:
- Fixing bugs
- Adding new features
- Refactoring code
- Writing tests
- Updating documentation

...you don't need to do anything special. Just code normally!

### When LIL OS Steps In

LIL OS only gets involved when you're making **important decisions** that could change what your project is supposed to do. These are called "intent-level changes."

**Examples of intent-level changes:**
- Changing what your project's main goal is
- Giving your AI assistant new powers to make decisions
- Automating something that used to require your approval
- Changing how success is measured

**Examples of things that are NOT intent-level changes:**
- Fixing a typo
- Adding a new function
- Updating a dependency
- Changing the color of a button

### How to Make an Intent-Level Change

If you need to make an important decision, here's the simple process:

1. **Think about it** - Ask yourself:
   - Why am I making this change?
   - Who will benefit from this?
   - What could go wrong?
   - Are there other ways to solve this?

2. **Log it** - Open `docs/DECISION_LOG.md` and add a new entry. Use this template:

```
Date: [Today's date]
Decision: [What you're deciding to do]
Trigger: [What made you need to make this decision]
Rationale: [Why you're doing this]
Tradeoffs: [What you're giving up or risking]
Expected Impact: [What you think will happen]
Review Date: [When you'll check if this was a good decision]
```

3. **Run the checks** - Before you commit your changes, run:

```bash
python3 scripts/lil_os_rule_id_lint.py
python3 scripts/lil_os_reset_checks.py
```

If everything passes, you're good to go!

---

## Part 3: Common Scenarios

### Scenario 1: Your AI Assistant Wants to Change Something Important

**What happens:** Your AI suggests changing how your project works, or wants to automate something you usually decide yourself.

**What to do:**
1. Stop and think: "Is this an important decision?"
2. If yes, log it in the decision log first
3. Then proceed with the change

**Example prompt for your AI:**
```
My AI assistant suggested [describe the change]. Before I proceed, I need to check if this is an intent-level change. Can you help me:
1. Determine if this needs to be logged in DECISION_LOG.md
2. If yes, help me create a proper log entry
3. Then help me implement the change
```

### Scenario 2: You're Not Sure if Something Needs to Be Logged

**What happens:** You're making a change and you're not sure if it's important enough to log.

**What to do:**
Ask yourself: "If I look back at this in 6 months, will I wonder why I made this decision?" If yes, log it. If no, you're probably fine.

**Example prompt for your AI:**
```
I'm about to [describe change]. I'm not sure if this needs to be logged in LIL OS. Can you help me figure out:
1. Is this an intent-level change?
2. Does it change goals, authority, or automation?
3. Should I log it in DECISION_LOG.md?
```

### Scenario 3: The Validation Scripts Fail

**What happens:** You run the validation scripts and they show errors.

**What to do:**
1. Don't panic! The scripts are trying to help you
2. Read the error message - it will tell you what's wrong
3. Fix the issue (usually it's a missing field in the decision log)
4. Run the scripts again

**Example prompt for your AI:**
```
I ran the LIL OS validation scripts and got this error: [paste the error]. Can you help me understand what's wrong and how to fix it?
```

### Scenario 4: You Want to Add a New Rule

**What happens:** You want to add a new rule to your project (like "always use TypeScript" or "never commit on Fridays").

**What to do:**
1. This IS an intent-level change, so log it first
2. Add the rule to the appropriate file
3. Give it a unique ID (the format is `LIL-CR-[CATEGORY]-[NUMBER]`)
4. Run the validation scripts

**Example prompt for your AI:**
```
I want to add a new rule to my project: [describe the rule]. Can you help me:
1. Create a proper log entry in DECISION_LOG.md
2. Add the rule with a proper ID format
3. Run the validation scripts to make sure everything is correct
```

---

## Part 4: Understanding the Tools

### The Validation Scripts

LIL OS comes with two main scripts that check your project:

**1. Rule ID Linter** (`lil_os_rule_id_lint.py`)
- Checks that all rules have proper IDs
- Makes sure rules aren't duplicated
- Verifies rules are formatted correctly

**2. Reset Checks** (`lil_os_reset_checks.py`)
- Checks if you're adding rules too fast
- Verifies decision log entries are complete
- Looks for signs that your project might be getting too complex

**When to run them:**
- Before committing important changes
- If you're not sure if something is set up correctly
- Once a week as a health check

### Pre-commit Hooks (Optional)

Pre-commit hooks automatically run the validation scripts every time you try to commit code. This means you can't accidentally commit something that breaks the rules.

**To set it up:**
```bash
pip install pre-commit
pre-commit install
```

After this, the checks will run automatically. If something fails, the commit will be blocked until you fix it.

---

## Part 5: Example Workflows

### Example 1: Starting a New Project

1. Set up your project normally
2. Run the LIL OS setup wizard
3. Start coding - no special steps needed!
4. When you make your first important decision, log it

**Prompt for your AI:**
```
I'm starting a new project and just set up LIL OS. Can you help me:
1. Understand what I need to do differently (if anything)
2. Show me an example of when I would need to log a decision
3. Set up pre-commit hooks so I don't forget
```

### Example 2: Adding AI Automation to an Existing Project

1. This is an intent-level change - log it first!
2. Explain why you're adding automation
3. Document what tradeoffs you're accepting
4. Then implement the automation

**Prompt for your AI:**
```
I want to add AI automation to [describe what]. This seems like an important decision. Can you help me:
1. Create a proper decision log entry explaining why I'm doing this
2. List the tradeoffs and risks
3. Then help me implement the automation
```

### Example 3: Your Project is Getting Complex

1. Run the reset checks script
2. If it warns you about complexity, take a step back
3. Review your decision log - are there decisions you should revisit?
4. Simplify before adding more complexity

**Prompt for your AI:**
```
The LIL OS reset checks are warning me that my project might be getting too complex. Can you help me:
1. Understand what the warnings mean
2. Review my decision log to find decisions that might need revisiting
3. Suggest ways to simplify before adding more features
```

---

## Part 6: Troubleshooting

### "I don't understand what LIL OS wants me to do"

**Solution:** Start simple. You don't need to use all of LIL OS's features right away. Just:
1. Set it up
2. Code normally
3. When you make an important decision, log it
4. That's it!

### "The validation scripts keep failing"

**Solution:** Usually this means a decision log entry is missing information. The error message will tell you exactly what's missing. Just add it and run again.

**Prompt for your AI:**
```
The validation script is failing with this error: [paste error]. Can you help me fix the decision log entry?
```

### "I'm not sure if something is an intent-level change"

**Solution:** When in doubt, ask yourself: "Would I want to know why this decision was made in 6 months?" If yes, log it. If you're still not sure, it's better to log it than not.

### "This seems like too much work"

**Solution:** Remember - you only need to log important decisions. Most of your coding can be completely normal. LIL OS is there to help with the big stuff, not slow you down on the small stuff.

---

## Part 7: Getting Help

### If You're Stuck

1. **Check the error message** - LIL OS tries to give clear error messages
2. **Ask your AI assistant** - Use the example prompts in this guide
3. **Read the decision log** - Sometimes seeing examples helps
4. **Start simple** - You don't need to use every feature

### Useful Prompts for Your AI Assistant

**General help:**
```
I'm using LIL OS and I'm confused about [describe your confusion]. Can you help me understand what I need to do?
```

**Checking if something is correct:**
```
I just [describe what you did]. Can you help me verify that I followed LIL OS correctly and run the validation scripts?
```

**Understanding an error:**
```
I got this error from LIL OS: [paste error]. Can you explain what it means and how to fix it?
```

---

## Remember

- **Most coding is normal** - LIL OS only steps in for important decisions
- **When in doubt, log it** - Better to log something that doesn't need it than miss something that does
- **Start simple** - You don't need to understand everything at once
- **The tools help you** - The validation scripts are there to catch mistakes, not to judge you

LIL OS is here to help you maintain control over your AI-assisted projects. It's not meant to slow you down - it's meant to help you avoid problems later.

Good luck, and happy coding!

