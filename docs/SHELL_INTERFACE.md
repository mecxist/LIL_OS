# LIL OS Shell Interface Guide

## Overview

LIL OS provides an enhanced shell interface similar to Claude Code, where builders can monitor background actions, receive real-time prompts for governance decisions, and interact with the system through a persistent terminal interface.

## Features

- **Real-time Activity Feed**: See all system events as they happen
- **Governance Decision Prompts**: Get notified when governance decisions are needed
- **Background Monitoring**: Continuous monitoring of files, git operations, and validation
- **Interactive Commands**: Full access to all LIL OS commands

## Getting Started

### Launching the Enhanced Shell

```bash
lil-os shell
```

Or using the Python module:

```bash
python3 -m lil_os.cli shell
```

The enhanced shell will:
1. Start automatically
2. Display a welcome banner
3. Show a status bar with daemon and validation status
4. Display any pending governance prompts

### Background Daemon

The daemon runs automatically when you start the shell. You can also manage it separately:

```bash
# Start daemon
lil-os daemon start

# Stop daemon
lil-os daemon stop

# Check status
lil-os daemon status

# Run in foreground
lil-os daemon run
```

## Shell Commands

### Standard Commands

All standard LIL OS commands work in the shell:

- `status` - Show system status
- `info` - Show system information
- `version` - Show version
- `health` - Quick health check
- `lint` - Check rule IDs
- `check` - Run reset trigger checks
- `warn` - Check for critical changes
- `log-decision` - Create decision log entry
- `setup` - Run setup wizard
- `explain <rule-id>` - Explain a rule ID
- `guide <scenario>` - Show scenario guide

### Enhanced Commands

New commands specific to the enhanced shell:

#### Activity Feed

```bash
activity [N]    # Show last N events (default: 20)
```

Displays a scrollable feed of recent system events, color-coded by severity.

#### Events

```bash
events [--type TYPE] [--limit N]
```

List recent events with optional filtering:
- `--type`: Filter by event type (e.g., `GOVERNANCE_FILE_CHANGED`)
- `--limit`: Maximum number of events to show

#### Governance Prompts

```bash
prompt              # Show pending governance prompts
prompt details      # Show detailed prompt information
```

When governance files are modified without decision log entries, prompts appear automatically. You can:
- View them with `prompt`
- Create a decision log entry with `log-decision`
- View details with `prompt details`

#### Daemon Management

```bash
daemon start     # Start background daemon
daemon stop      # Stop background daemon
daemon status    # Show daemon status
daemon restart   # Restart background daemon
```

## Status Bar

The status bar appears above each prompt and shows:

- **Daemon Status**: ● (green) = running, ○ (dim) = stopped
- **Validation Status**: ✓ (green) = passed, ✗ (red) = failed, ○ (dim) = unknown
- **Pending Decisions**: ⚠ (yellow) = number of pending governance decisions

## Activity Feed

The activity feed shows real-time events as they occur:

- **INFO** (cyan): Informational events
- **WARN** (yellow): Warning events
- **ERROR** (red): Error events
- **CRITICAL** (red, bold): Critical events

Events include:
- File changes
- Governance file modifications
- Git operations (staging, commits)
- AI agent actions
- Validation runs and results
- Governance decision needs

## Governance Decision Prompts

When a governance file is modified without a corresponding decision log entry, a prompt appears:

```
╔══════════════════════════════════════════════════════════╗
║              Governance Prompt                           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  ⚠ Governance Decision Required ⚠                      ║
║                                                          ║
║  File: GOVERNANCE.md                                     ║
║  Reason: governance_file_changed                         ║
║                                                          ║
║  A governance file has been modified without a           ║
║  corresponding decision log entry...                     ║
║                                                          ║
║  Actions:                                                ║
║    1. Create decision log entry (type 'log-decision')   ║
║    2. Dismiss this prompt (type 'dismiss <id>')          ║
║    3. View details (type 'prompt details')              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

To resolve:
1. Run `log-decision` to create a decision log entry
2. The prompt will automatically clear once the entry is created

## Event Types

The system tracks various event types:

- `FILE_CHANGED` - File system changes
- `GOVERNANCE_FILE_CHANGED` - Governance file modifications
- `GIT_COMMIT` - Git commits detected
- `GIT_STAGE` - Files staged for commit
- `VALIDATION_RUN` - Validation scripts executed
- `VALIDATION_FAILED` - Validation failures
- `VALIDATION_PASSED` - Validation passed
- `GOVERNANCE_DECISION_NEEDED` - Governance prompt required
- `AI_AGENT_ACTION` - AI agent making changes
- `DECISION_LOG_CREATED` - Decision log entry created
- `DAEMON_STARTED` - Daemon started
- `DAEMON_STOPPED` - Daemon stopped

## Configuration

Daemon configuration is in `lil_os.daemon.yaml`:

```yaml
daemon:
  enabled: true
  watch_interval: 2.0
  event_history_size: 1000

monitoring:
  file_watcher:
    enabled: true
    watch_paths:
      - docs/
      - .cursorrules
  git_monitor:
    enabled: true
    detect_ai_agents: true
  validation_monitor:
    enabled: true
```

## Tips

1. **Keep the shell open**: The shell provides continuous monitoring, so keep it running while you work
2. **Check activity regularly**: Use `activity` to see what's happening in the background
3. **Respond to prompts**: Don't ignore governance prompts - they indicate important changes that need documentation
4. **Monitor validation**: The status bar shows validation status at a glance
5. **Use daemon commands**: Manage the daemon separately if needed for troubleshooting

## Troubleshooting

**Daemon won't start:**
- Check if you're in a git repository (required for git monitor)
- Verify `lil_os.daemon.yaml` exists and is valid
- Check file permissions

**Events not appearing:**
- Ensure daemon is running (`daemon status`)
- Check event history size in config
- Verify monitors are enabled

**Governance prompts not clearing:**
- Make sure decision log entry references the changed file
- Check that entry date is within 7 days of file change
- Verify decision log format is correct

## Architecture

The shell interface consists of:

1. **Event System** (`lil_os/events.py`): Central event bus for all activities
2. **Background Daemon** (`lil_os/daemon.py`): Orchestrates monitoring components
3. **Enhanced Shell** (`lil_os/shell_enhanced.py`): Interactive terminal interface
4. **Monitors**: File watcher, git monitor, validation monitor
5. **Governance Detector**: Analyzes events and triggers prompts

All components communicate through the event bus, providing a decoupled, extensible architecture.

