# LIL OS Permission Structure

This document outlines the permission structure for the LIL OS repository, aligned with our [tiered contribution model](../docs/CONTRIBUTING.md).

## Teams & Roles

### Maintainers Team
- **Role:** Admin
- **Members:** Core team and project maintainers
- **Permissions:**
  - Full repository access
  - Can merge all PRs (implementation and intent-level)
  - Can bypass branch protection rules
  - Can manage repository settings
  - Can manage teams and permissions

### Official Contributors Team
- **Role:** Write
- **Members:** Approved contributors who have applied and been accepted through [LIL Co.](https://www.lilco.io)
- **Permissions:**
  - Can create branches and push code
  - Can merge intent-level PRs (after review)
  - Can review and approve PRs
  - Required reviewers for intent-level changes
- **Requirements:**
  - Must have demonstrated alignment with Liberatory Intelligence principles
  - Must have commitment to the project's mission
  - Must understand the governance framework

### Community Contributors
- **Role:** Read (public access)
- **Members:** Anyone (no approval required)
- **Permissions:**
  - Can fork the repository
  - Can submit pull requests
  - Can comment on issues and PRs
  - Can view all code and documentation
- **Limitations:**
  - Cannot merge PRs directly
  - Cannot push to main branch
  - Cannot bypass branch protection

## Branch Protection Rules

### Main Branch (`main`)

**Required Settings:**
- ✅ Require pull request reviews before merging
- ✅ Require review from "Official Contributors" team (for intent-level PRs)
- ✅ Allow maintainers to bypass (for implementation fixes)
- ✅ Require status checks to pass:
  - `lil_os_rule_id_lint` (rule ID validation)
  - `lil_os_reset_checks` (reset trigger checks)
- ❌ Do not allow force pushes
- ❌ Do not allow deletions

**Review Requirements:**
- **Implementation PRs** (bug fixes, docs, tooling):
  - At least 1 approval from any maintainer or Official Contributor
  - Maintainers can merge directly if needed
- **Intent-Level PRs** (governance, rules, philosophy):
  - At least 1 approval from an Official Contributor (required)
  - Additional maintainer review recommended
  - Must include decision log entry
  - Must follow `docs/GOVERNANCE.md` process

## Contribution Types & Permissions

### Open Contributions (No Approval Required)
Anyone can:
- Submit bug fixes
- Improve documentation
- Refactor code
- Enhance tooling
- Share examples and use cases

**Process:** Fork → Branch → PR → Review → Merge

### Official Contributor Required
These require Official Contributor status:
- Intent-level changes (governance, rules, philosophy)
- Major platform adaptations
- Architectural changes
- Changes to core systems

**Process:** Apply to LIL Co. → Get approved → Follow governance → PR with decision log → Official Contributor review → Merge

## Permission Escalation

### Becoming an Official Contributor

1. **Apply:** Visit [LIL Co.](https://www.lilco.io) and apply to join the collective
2. **Review:** Application reviewed for alignment with Liberatory Intelligence principles
3. **Approval:** If approved, added to "Official Contributors" team
4. **Access:** Gain write access and ability to review intent-level PRs

### Becoming a Maintainer

Maintainer status is granted by existing maintainers based on:
- Consistent high-quality contributions
- Deep understanding of LIL OS governance
- Commitment to project mission
- Alignment with Liberatory Intelligence principles

## Security & Access Management

- All team members must use two-factor authentication (2FA)
- SSH keys or Personal Access Tokens (PATs) required for write access
- Regular access audits to ensure permissions remain appropriate
- Revocation of access if contributor no longer aligns with project principles

## Questions?

- For permission questions: Open an issue or contact maintainers
- For joining the collective: Visit [lilco.io](https://www.lilco.io)
- For contribution process: See [CONTRIBUTING.md](../docs/CONTRIBUTING.md)

---

**Remember:** Permissions are not about control—they're about ensuring that changes to LIL OS's fundamental principles are made by those who understand and are committed to the project's mission of liberatory governance.

