# Deployment & Packaging Guidelines

**Version:** v0.1.1  
**Purpose:** Guidelines for excluding LIL OS development components when packaging or deploying your project

## Overview

LIL OS is a **development-time governance framework** designed to help manage AI-assisted development. When packaging or deploying your application, you typically want to exclude development tools and validation scripts while potentially keeping documentation that provides value in production.

This document explains what to exclude, what to keep, and how to do it.

---

## What to Exclude from Production Builds

These components are development tools and should **not** be included in production deployments:

### Development Scripts
- `scripts/lil_os_rule_id_lint.py` - Rule ID validation script
- `scripts/lil_os_reset_checks.py` - Reset trigger validation script
- `scripts/lil_os_critical_change_warning.py` - Critical change warning script
- `scripts/setup_wizard.py` - Setup wizard (development only)

### Development Configuration
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `lil_os.rule_id.yaml` - Rule ID linter configuration
- `lil_os.reset_checks.yaml` - Reset checks configuration
- `.lil_os/` directory - Marker files for explanation failures

### CI/CD Workflows (Optional)
- `.github/workflows/lil_os_checks.yml` - CI/CD validation workflow
  - **Note:** Keep this in your repository, but it won't run in production environments
  - Only needed for GitHub-hosted repositories

---

## What to Optionally Keep

These components may provide value in production and can be included:

### Decision Logs (Recommended for Audit Trails)
- `docs/DECISION_LOG.md` - Historical record of important decisions
  - **Why keep:** Provides audit trail, compliance documentation, and explains system evolution
  - **Use cases:** Compliance audits, understanding system behavior, debugging production issues
  - **Size:** Typically small, adds minimal overhead

### Governance Documentation (Optional)
- `docs/GOVERNANCE.md` - Governance framework documentation
- `docs/MASTER_RULES.md` - Non-negotiable boundaries
- `docs/CONTEXT_BUDGET.md` - Context budget doctrine
  - **Why keep:** Helps explain system design and constraints to operations teams
  - **Use cases:** Onboarding new team members, understanding system architecture
  - **Consideration:** May contain internal decision-making processes

### AI Agent Rules (If Production Uses AI)
- `.cursorrules` - Rules for AI assistants
  - **Why keep:** If your production system uses AI agents, these rules may be needed
  - **Use cases:** Production AI agents, runtime AI assistance
  - **Consideration:** Review rules to ensure they're appropriate for production

### Other Documentation (Optional)
- `docs/RESET_TRIGGERS.md` - Reset trigger documentation
- `docs/RULE_IDS.md` - Rule ID scheme documentation
  - **Why keep:** Reference documentation for understanding system design
  - **Consideration:** Only needed if operations teams need to understand governance

---

## How to Exclude Components

### Method 1: Using .dockerignore (Docker Deployments)

Create or update `.dockerignore`:

```dockerignore
# LIL OS Development Components
scripts/
.pre-commit-config.yaml
lil_os.rule_id.yaml
lil_os.reset_checks.yaml
.lil_os/

# Optional: Exclude all docs except decision log
docs/*
!docs/DECISION_LOG.md

# Optional: Exclude governance docs if not needed
# !docs/GOVERNANCE.md
# !docs/MASTER_RULES.md
```

### Method 2: Using .gitignore for Build Artifacts

If your build process creates artifacts, add to `.gitignore`:

```gitignore
# Build artifacts (if LIL OS files are copied during build)
dist/
build/
*.egg-info/

# Production builds shouldn't include these
production/scripts/
production/.pre-commit-config.yaml
```

### Method 3: Build Script Exclusion

For custom build scripts, exclude LIL OS components:

**Python (setup.py or pyproject.toml):**
```python
# In your setup.py or pyproject.toml
exclude_packages = [
    'scripts',
    '.lil_os',
]

# Or use MANIFEST.in
# recursive-exclude scripts *
# recursive-exclude .lil_os *
```

**Node.js (package.json):**
```json
{
  "files": [
    "src",
    "docs/DECISION_LOG.md",
    "!scripts",
    "!.pre-commit-config.yaml",
    "!lil_os.*.yaml"
  ]
}
```

**Makefile example:**
```makefile
.PHONY: package
package:
	# Copy source files
	cp -r src dist/
	# Copy decision log if needed
	cp docs/DECISION_LOG.md dist/docs/ 2>/dev/null || true
	# Exclude LIL OS development files
	# (they're not copied, so no exclusion needed)
```

### Method 4: CI/CD Build Configuration

Configure your CI/CD pipeline to exclude LIL OS components:

**GitHub Actions example:**
```yaml
- name: Create production build
  run: |
    # Copy source files
    cp -r src dist/
    # Optionally copy decision log
    mkdir -p dist/docs
    cp docs/DECISION_LOG.md dist/docs/
    # LIL OS scripts are not copied (excluded by default)
```

**GitLab CI example:**
```yaml
build:
  script:
    - mkdir -p dist
    - cp -r src dist/
    - mkdir -p dist/docs
    - cp docs/DECISION_LOG.md dist/docs/ || true
  artifacts:
    paths:
      - dist/
    exclude:
      - dist/scripts/
      - dist/.pre-commit-config.yaml
```

---

## Decision Matrix

Use this matrix to decide what to include:

| Component | Development | Production | Reason |
|-----------|------------|------------|--------|
| `scripts/` | ✅ Required | ❌ Exclude | Development tools only |
| `.pre-commit-config.yaml` | ✅ Required | ❌ Exclude | Pre-commit hooks don't run in production |
| `lil_os.*.yaml` | ✅ Required | ❌ Exclude | Validation configuration not needed |
| `.lil_os/` | ✅ Required | ❌ Exclude | Marker files for development |
| `docs/DECISION_LOG.md` | ✅ Required | ⚠️ Optional | Keep for audit trails if needed |
| `docs/GOVERNANCE.md` | ✅ Required | ⚠️ Optional | Keep if operations team needs it |
| `.cursorrules` | ✅ Required | ⚠️ Optional | Keep if production uses AI agents |
| `.github/workflows/` | ✅ Required | ⚠️ N/A | Stays in repo, doesn't deploy |

---

## Special Considerations

### Compliance & Audit Requirements

If your project has compliance or audit requirements:
- **Keep:** `docs/DECISION_LOG.md` - Provides decision audit trail
- **Keep:** `docs/GOVERNANCE.md` - Documents governance framework
- **Consider:** Including governance docs in compliance documentation package

### Production AI Agents

If your production system uses AI agents:
- **Keep:** `.cursorrules` - Rules for production AI agents
- **Review:** Ensure rules are appropriate for production (not just development)
- **Consider:** Creating separate `.cursorrules.production` if rules differ

### Container Deployments

For containerized deployments (Docker, Kubernetes):
- Use `.dockerignore` to exclude development components
- Decision logs can be mounted as volumes if needed for audit
- Governance docs can be included in base image if operations team needs them

### Serverless Deployments

For serverless deployments (AWS Lambda, Vercel, etc.):
- Most LIL OS components are automatically excluded (not in function code)
- Decision logs can be stored separately (S3, database) if needed
- Governance docs can be in separate documentation service

### Package Distribution

For libraries/packages distributed via package managers:
- **Always exclude:** All `scripts/` and configuration files
- **Optionally include:** Decision log in package metadata/docs
- **Use:** Package manifest files (package.json, setup.py, etc.) to control inclusion

---

## Quick Reference: Exclusion Patterns

### Complete Exclusion (Recommended for Most Cases)

Exclude all LIL OS development components:

```bash
# Exclude from build
rm -rf scripts/
rm -f .pre-commit-config.yaml
rm -f lil_os.*.yaml
rm -rf .lil_os/
```

### Minimal Exclusion (Keep Documentation)

Exclude only development tools, keep documentation:

```bash
# Exclude development tools
rm -rf scripts/
rm -f .pre-commit-config.yaml
rm -f lil_os.*.yaml
rm -rf .lil_os/

# Keep documentation (already in docs/, no action needed)
```

### Audit-Ready Build (Keep Decision Logs)

Exclude development tools, keep audit documentation:

```bash
# Exclude development tools
rm -rf scripts/
rm -f .pre-commit-config.yaml
rm -f lil_os.*.yaml
rm -rf .lil_os/

# Ensure decision log is included
# (already in docs/, copy to build if needed)
cp docs/DECISION_LOG.md dist/docs/ 2>/dev/null || true
```

---

## Best Practices

1. **Automate Exclusion** - Use build scripts or CI/CD to automatically exclude components
2. **Document Your Choices** - Note in your deployment docs what LIL OS components you're including/excluding
3. **Review Regularly** - As your project evolves, review what documentation is needed in production
4. **Consider Compliance** - If you have audit requirements, include decision logs
5. **Test Your Builds** - Verify that excluded components aren't accidentally included

---

## Example Build Scripts

### Simple Python Project

```bash
#!/bin/bash
# build.sh - Production build script

# Create build directory
mkdir -p dist

# Copy source code
cp -r src dist/

# Copy decision log (optional)
mkdir -p dist/docs
cp docs/DECISION_LOG.md dist/docs/ 2>/dev/null || true

# LIL OS scripts are not copied (excluded)
# Validation: Verify scripts/ is not in dist/
if [ -d "dist/scripts" ]; then
    echo "ERROR: scripts/ directory should not be in production build"
    exit 1
fi

echo "Build complete. LIL OS development components excluded."
```

### Node.js Project

```json
{
  "scripts": {
    "build": "npm run build:src && npm run build:docs",
    "build:src": "webpack --mode production",
    "build:docs": "mkdir -p dist/docs && cp docs/DECISION_LOG.md dist/docs/ || true"
  },
  "files": [
    "dist",
    "package.json",
    "README.md"
  ]
}
```

---

## Troubleshooting

### Problem: LIL OS scripts are in production build

**Solution:** Check your build configuration:
1. Verify `.dockerignore` or build script excludes `scripts/`
2. Check that build process doesn't copy entire project root
3. Review CI/CD pipeline to ensure exclusion

### Problem: Decision log is missing from production

**Solution:** If you need it:
1. Explicitly copy `docs/DECISION_LOG.md` in build script
2. Or mount it as a volume/config in deployment
3. Or store it separately (database, object storage)

### Problem: Build fails because scripts are referenced

**Solution:** 
1. Ensure no production code imports from `scripts/`
2. Check that build process doesn't try to execute validation scripts
3. Verify package.json or setup.py doesn't include scripts as dependencies

---

## Summary

LIL OS is designed for **development-time governance**, not runtime enforcement. When deploying:

- **Always exclude:** Development scripts, pre-commit hooks, validation configs
- **Optionally keep:** Decision logs (for audit), governance docs (for operations)
- **Automate exclusion:** Use build scripts, `.dockerignore`, or CI/CD configuration
- **Document choices:** Note what you're including/excluding and why

The goal is to keep your production builds clean while preserving valuable documentation when needed.

---

**See Also:**
- [INSTALLATION.md](INSTALLATION.md) - How to set up LIL OS
- [USER_GUIDE.md](USER_GUIDE.md) - How to use LIL OS day-to-day
- [GOVERNANCE.md](GOVERNANCE.md) - Governance framework

