# SECURITY (v0.1.1)

## Overview

LIL OS implements security measures to protect governance integrity, prevent unauthorized changes, and ensure accountability. This document outlines security considerations, risks, and mitigations.

## Security Architecture

LIL OS uses a multi-layered security approach:

1. **Pre-commit Hooks** - Local validation before commits
2. **CI/CD Enforcement** - Server-side validation that cannot be bypassed
3. **Integrity Checks** - Detection of tampering and unauthorized modifications
4. **Governance File Protection** - Requirements for documenting governance changes

## Critical Security Risks

### 1. Pre-commit Hook Bypass

**Risk:** Users can bypass pre-commit hooks using `git commit --no-verify`, allowing invalid changes to be committed locally.

**Mitigation:**
- **CI/CD Workflow** (`.github/workflows/lil_os_checks.yml`) runs validation on all pull requests
- Branch protection rules require CI checks to pass before merging
- Pre-commit hooks cannot be bypassed in CI/CD environment

**Best Practice:**
- Always use pull requests for important changes
- Never use `--no-verify` flag unless absolutely necessary (and log why in decision log)
- Review CI/CD check results before merging

### 2. Decision Log Tampering

**Risk:** Decision logs can be retroactively modified to hide unauthorized changes or remove accountability.

**Mitigation:**
- **Decision Log Integrity Check** detects suspicious retroactive modifications
- Git history tracks all changes to decision logs
- Validation scripts flag entries modified after initial creation without proper justification

**Best Practice:**
- Never modify decision log entries after they're committed without adding a new entry explaining why
- If you must correct an entry, add a new entry documenting the correction
- Use git commit messages that clearly explain decision log changes

### 3. Governance File Modification Without Documentation

**Risk:** Critical governance files (`MASTER_RULES.md`, `GOVERNANCE.md`, `RESET_TRIGGERS.md`) can be modified without proper decision log entries.

**Mitigation:**
- **Governance File Change Detection** requires decision log entries for all governance file modifications
- Validation fails if governance files are changed without corresponding decision log entries
- CI/CD enforces this check on all pull requests

**Best Practice:**
- Always create a decision log entry before modifying governance files
- Link the decision log entry to the specific governance change
- Follow the governance process outlined in `GOVERNANCE.md`

### 4. Validation Script Tampering

**Risk:** Validation scripts can be replaced with malicious versions that bypass security checks.

**Mitigation:**
- Validation scripts are part of the repository and tracked in git
- CI/CD uses the repository version, not local copies
- Script modifications are subject to the same governance requirements

**Best Practice:**
- Never modify validation scripts without understanding their security implications
- Review script changes in pull requests carefully
- Consider script checksum verification for high-security environments (future enhancement)

### 5. AI Assistant Manipulation

**Risk:** AI assistants can be prompted to bypass governance rules or make unauthorized changes.

**Mitigation:**
- Governance rules are encoded in files that AI assistants should read
- Validation scripts enforce rules regardless of how changes are made
- CI/CD provides a final enforcement layer

**Best Practice:**
- Include governance files in your AI assistant's context
- Prompt AI assistants to check governance rules before making intent-level changes
- Never ask AI assistants to bypass validation or use `--no-verify`
- Review all AI-generated changes, especially to governance files

## Security Features

### CI/CD Enforcement

The GitHub Actions workflow (`.github/workflows/lil_os_checks.yml`) provides server-side enforcement that cannot be bypassed:

- Runs on all pull requests
- Validates rule IDs and reset triggers
- Checks decision log integrity
- Verifies governance file changes are documented
- Scans for accidentally committed secrets
- Blocks merges if validation fails

**This is the primary security layer** - even if pre-commit hooks are bypassed, CI/CD will catch violations.

### Decision Log Integrity Check

Automatically detects:
- Entries modified after initial creation
- Suspicious retroactive modifications
- Missing justification for entry changes

Configuration in `lil_os.reset_checks.yaml`:
```yaml
security:
  check_decision_log_integrity: true
```

### Governance File Change Detection

Requires decision log entries for modifications to:
- `docs/MASTER_RULES.md`
- `docs/GOVERNANCE.md`
- `docs/RESET_TRIGGERS.md`

Validation fails if these files are modified without corresponding decision log entries.

Configuration in `lil_os.reset_checks.yaml`:
```yaml
security:
  check_governance_file_changes: true
```

### Secret Detection

Automatically scans decision logs and governance files for accidentally committed secrets:
- API keys and access tokens
- AWS credentials
- GitHub tokens
- Database connection strings
- OAuth client secrets
- Private keys
- Passwords

**Validation fails immediately if secrets are detected** - preventing sensitive information from being committed to version control.

**If secrets are detected:**
1. Remove the secrets from files immediately
2. Rotate any exposed credentials
3. Use environment variables or secret management tools instead
4. Re-run validation to confirm secrets are removed

Configuration in `lil_os.reset_checks.yaml`:
```yaml
security:
  check_secrets: true
  secret_patterns:
    - "(?i)(api[_-]?key|apikey)[\s:=]+['\"]?([a-zA-Z0-9_\-]{20,})['\"]?"
    # ... additional patterns
```

### Script Checksum Verification

Verifies that validation scripts haven't been modified or tampered with by comparing SHA256 checksums.

**When to enable:**
- High-security environments
- When scripts are shared across teams
- To detect unauthorized modifications

**To enable:**
1. Calculate checksums of your scripts:
   ```bash
   python3 -c "import hashlib; print(hashlib.sha256(open('scripts/lil_os_rule_id_lint.py','rb').read()).hexdigest())"
   ```
2. Add checksums to `lil_os.reset_checks.yaml`:
   ```yaml
   security:
     check_script_checksums: true
     script_checksums:
       lil_os_rule_id_lint.py: "your_checksum_here"
       lil_os_reset_checks.py: "your_checksum_here"
   ```
3. **Important:** Update checksums whenever you intentionally modify scripts

**Note:** Checksum verification is disabled by default. Enable it only after setting expected checksums, otherwise validation will fail.

## Emergency Overrides

Emergency overrides are permitted only when:
- Security/safety is at immediate risk
- Legal compliance requires action
- Credible human harm is imminent

**All overrides MUST:**
- Be logged retroactively in `DECISION_LOG.md`
- Include justification for the override
- Be reviewed for legitimacy

Repeated overrides trigger reset triggers (see `RESET_TRIGGERS.md`).

## Secret Management

**Never commit secrets to:**
- Decision logs
- Governance files
- Validation scripts
- Any tracked files

**LIL OS automatically detects secrets** in decision logs and governance files using pattern matching. If secrets are detected, validation fails immediately.

**Best Practices:**
- Use environment variables for API keys and tokens
- Use `.gitignore` to exclude secret files
- Use secret management tools (e.g., GitHub Secrets, AWS Secrets Manager)
- If secrets are accidentally committed:
  1. Remove them immediately
  2. Rotate any exposed credentials
  3. Re-run validation to confirm removal
  4. Consider enabling secret detection in your CI/CD pipeline

## Protecting Validation Scripts

Validation scripts are critical security components:

1. **Never disable validation scripts** - They're your last line of defense
2. **Review script changes carefully** - Understand what each modification does
3. **Test script changes** - Ensure modifications don't introduce vulnerabilities
4. **Use version control** - All script changes should be tracked and reviewed

## Branch Protection

For repositories using LIL OS, configure branch protection rules:

- Require pull request reviews
- Require status checks to pass (CI/CD validation)
- Prevent force pushes to main branch
- Require decision log entries for intent-level changes

See `.github/PERMISSIONS.md` for detailed branch protection configuration.

## Reporting Security Issues

If you discover a security vulnerability in LIL OS:

1. **Do not** open a public issue
2. Contact maintainers directly
3. Provide detailed information about the vulnerability
4. Allow time for remediation before public disclosure

## Security Checklist

Before making intent-level changes:

- [ ] Read `GOVERNANCE.md` to understand requirements
- [ ] Create decision log entry with full justification
- [ ] Run validation scripts locally
- [ ] Ensure pre-commit hooks are active
- [ ] Submit pull request (CI/CD will validate)
- [ ] Review CI/CD check results
- [ ] Get required approvals before merging

## Additional Resources

- `GOVERNANCE.md` - Governance framework and requirements
- `RESET_TRIGGERS.md` - Conditions that trigger security resets
- `.github/PERMISSIONS.md` - Access control and branch protection
- `MASTER_RULES.md` - Non-negotiable security boundaries

## ML Module Security

LIL OS² includes optional ML modules that process git history and validation reports. These modules have specific security considerations:

### Signal Collection Security

**Risk:** ML modules collect signals from git commits and validation reports, which may contain sensitive information.

**Mitigation:**
- Signal collection redacts sensitive strings using patterns from `lil_os.reset_checks.yaml`
- Secrets are replaced with `[REDACTED]` in signal storage
- Signal storage (`.lil_os/ml/`) is excluded from git by default
- SQLite database is local-only and not synced to version control

**Best Practice:**
- Review signal collection patterns regularly
- Never commit `.lil_os/ml/` directory to git
- Use ML modules only in trusted environments
- Disable ML modules if signal collection is a concern

### Model Artifact Security

**Risk:** Trained models may contain information from training data.

**Mitigation:**
- Models are stored locally in `.lil_os/ml/models/`
- Model artifacts are excluded from git
- Model metadata includes provenance information
- Models can be versioned and validated

**Best Practice:**
- Never commit model artifacts to git
- Validate model checksums before loading
- Review model metadata for training data sources
- Retrain models if training data contained sensitive information

### ML Module Configuration

ML modules are **opt-in** and disabled by default. To use ML modules:

1. Install with ML extras: `pip install lil-os[ml]`
2. Enable modules explicitly in `lil_os.ml.yaml`
3. Review configuration before enabling

**Default Configuration:**
- All ML modules are disabled by default
- Signal collection requires explicit enablement
- Model training is manual (not automatic)

### Secret Redaction in Signals

ML signal collectors automatically redact:
- API keys and tokens
- Passwords and credentials
- OAuth secrets
- Database connection strings

Redaction uses the same patterns as secret detection in validation scripts.

**If sensitive data is detected in signals:**
1. Review signal collection configuration
2. Update redaction patterns if needed
3. Clear signal storage if necessary
4. Retrain models if they were trained on sensitive data

## Version History

- **v0.1.1** - Initial security documentation with integrity checks, CI/CD enforcement, secret detection, and script checksum verification
- **v2.0.0** - Added ML module security considerations and signal collection redaction