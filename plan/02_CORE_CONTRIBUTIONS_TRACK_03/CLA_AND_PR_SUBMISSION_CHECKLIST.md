# Track 03: CLA & Pull Request Submission Protocol

This guide outlines the step-by-step technical procedure for opening, signing, and merging pull requests to `sandbox-quantum/switch`.

---

## 1. Live Active PR Tracking (Max 5 Concurrent)

| Slot | Issue # | Title | Branch | PR URL | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Slot 1** | **#808** | docs(contributing): add five-minute contributor quickstart | `docs/quickstart-808` | [PR #1397](https://github.com/sandbox-quantum/switch/pull/1397) | **Open (CLA Signed, Socket & Semgrep Green)** |
| **Slot 2** | **#807** | docs(deploy): add agent controller user guide | `docs/agent-controller-807` | [PR #1399](https://github.com/sandbox-quantum/switch/pull/1399) | **Open (Security Checks Green)** |
| **Slot 3** | **#827** | feat(connections): add Supabase connector | `feat/supabase-827` | Blueprint Ready | Ready to stage |
| **Slot 4** | **#820** | feat(connections): add Sentry connector | `feat/sentry-820` | Blueprint Ready | Ready to stage |
| **Slot 5** | **#829** | feat(connections): add Stripe connector | `feat/stripe-829` | Blueprint Ready | Ready to stage |

---

## 2. Local Environment Preparation & Branch Hygiene

```bash
# 1. Fetch latest upstream main
git -C switch-repo fetch upstream

# 2. Create feature branch off upstream/main
git -C switch-repo checkout -b feat/my-feature upstream/main
```

---

## 3. Running Mandatory Local Checks

Switch's continuous integration (`pr-ci.yml`) automatically enforces:

```bash
uv sync --project core
just check       # Ruff format & lint check
just typecheck   # Mypy static typing
just test        # Pytest backend test suite
```

---

## 4. CLA Signing Protocol

Once your first pull request is opened:
1. The automated CLA Assistant bot comments on the PR with the status check `cla`.
2. Reply to the PR with the exact phrase:
   > **I have read the CLA Document and I hereby sign the CLA**
3. Once signed on one PR, the signature applies globally across all PRs submitted by `@farhanmallik05`.
