# Hackathon Pre-Flight Verification Checklist

Run this checklist immediately (during Hackathon Eve) to ensure that your workstation has zero blockers when building begins.

---

## 1. Toolchain & Runtime Verification

Run each command in PowerShell / Bash to confirm operational readiness:

- [ ] **Docker Daemon Running:**
  ```bash
  docker info
  # Verify Docker Desktop or daemon is active and responsive.
  ```
- [ ] **uv (Python Package Manager):**
  ```bash
  uv --version
  # Should report uv 0.5.0 or later.
  ```
- [ ] **just Task Runner:**
  ```bash
  just --version
  # Should report just 1.14 or later.
  ```
- [ ] **Node.js & pnpm:**
  ```bash
  node -v   # Must be v22.13.0 or later
  pnpm -v   # Must be v9.0.0 or later
  ```
- [ ] **GitHub CLI:**
  ```bash
  gh auth status
  # Verify authenticated GitHub session.
  ```

---

## 2. Desktop Application Setup

- [ ] **Switch Console Desktop App:**
  - Downloaded and installed from [GitHub Releases](https://github.com/sandbox-quantum/switch/releases).
  - Successfully launches and displays the initial setup screen.
- [ ] **Wispr Flow Desktop App:**
  - Installed and logged into account with 1 month free Pro tier.
  - Push-to-talk hotkey tested and verified.
  - Dictated a test sentence to confirm voice accuracy.

---

## 3. Communication Bridges & Tokens

- [ ] **Slack or Discord Test Workspace:**
  - Have an active Slack workspace (or Discord server) where you hold administrator permissions.
  - Created test channels: `#sre-incident-intake` and `#sre-incident-war-room`.
- [ ] **GitHub Personal Access Token:**
  - Generated fine-grained PAT with `repo` and `pull_requests:write` permissions for mock testing.
- [ ] **Sentry Account (Optional / Test Mode):**
  - Free developer account created on `sentry.io` with a test project initialized.

---

## 4. Repository & Git Remote Sanity

- [ ] Fork of `sandbox-quantum/switch` created under your GitHub account.
- [ ] Upstream remote configured: `git remote add upstream https://github.com/sandbox-quantum/switch.git`.
- [ ] Git line endings configured to prevent CRLF corruption:
  ```bash
  git config --global core.autocrlf false
  ```
