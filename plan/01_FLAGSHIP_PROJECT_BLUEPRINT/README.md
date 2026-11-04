# OpsSwitch: Autonomous Incident Commander & War Room

> **Flip the Switch Hackathon — Flagship Entry for Track 01: Best Business Workflow ($2,000)**  
> **Team:** Algo Alchemist (`K8H5DE`) | **Author:** Farhan Mallik (`@farhanmallik`)

[![Switch Powered](https://img.shields.io/badge/Switch-Rooms%20%2B%20Protocol-FF895E)](https://switchagents.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Built with: Wispr Flow](https://img.shields.io/badge/Voice%20Dictated-Wispr%20Flow-8A2BE2)](https://wisprflow.ai)
[![Works with: Slack & Discord](https://img.shields.io/badge/Bridges-Slack%20%7C%20Discord%20%7C%20Teams-5865F2)](https://github.com/sandbox-quantum/switch)

---

## 🚀 Overview

**OpsSwitch** transforms incident management from frantic context-switching across browser tabs into a calm, automated, human-supervised collaboration inside team chat.

Using **Switch**, OpsSwitch deploys a squad of autonomous AI teammates across two linked channels (`#incident-intake` and `#incident-war-room`). When an anomaly or crash occurs:
1. **`ops-triager`** intercepts the alert in `#incident-intake`, filters out false positives, classifies severity (SEV-1 to SEV-4), and initiates an escalation thread.
2. **`ops-investigator`** receives the handoff in `#incident-war-room`, inspects recent git commits and error traces, writes a minimal reproduction test, and isolates the offending line of code.
3. **`ops-remediator`** drafts an emergency rollback or hotfix PR, computes risk metrics, and presents an interactive authorization prompt to the human On-Call Engineer.
4. **Human Engineer** signs off with a single message (`"Approved. Execute rollback."`).
5. **`ops-remediator`** triggers the GitHub rollback, monitors health recovery, and writes an automated RCA (Root Cause Analysis) post-mortem back to `#incident-intake`.

```
        ┌─────────────────────────────────────────────────────────┐
        │                 SLACK / DISCORD CHAT                    │
        │                                                         │
        │  [#incident-intake]               [#incident-war-room]  │
        │   • Alert arrives                  • Log triage         │
        │   • Customer reports               • Commit diff audit  │
        │   • Executive updates              • Repro execution    │
        │            │                               │            │
        │      ops-triager ───────────────►  ops-investigator    │
        │     (Triage & Dedup)   (Linked Room)       │            │
        │                                            ▼            │
        │                                      ops-remediator     │
        │                                     (Patch & Rollback)  │
        │                                            │            │
        │   Human On-Call Lead ◄─────────────────────┘            │
        │   "Approved. Roll it back."                             │
        └─────────────────────────────────────────────────────────┘
```

---

## 💡 Why Switch is Central (Judging Rubric #1)

OpsSwitch **cannot function as a generic single-agent chatbot**:
- **Room Topology**: It requires cross-room context isolation. Customer-facing engineers in `#incident-intake` should not be flooded with hundreds of lines of stack traces and git diffs generated in `#incident-war-room`. Switch's **linked rooms** provide clean, selective context transmission.
- **Agent-to-Agent Delegation**: The Triager invokes the Investigator by name (`@ops-investigator`), and the Investigator passes reproduction evidence directly to the Remediator.
- **True Multi-Harness Teammates**: The Triager can run on Claude Code locally, the Investigator can run on Codex CLI, and the Remediator can run on a secure server harness—unified seamlessly by the **Switch Agent Protocol** (SSE in, HTTP out).
- **Zero Token Leakage**: Third-party credentials (GitHub tokens, Sentry keys) are brokered through Switch's secure session host, never injected into the LLM context.

---

## 🛠️ Quickstart (Run in 5 Minutes)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ or Python 3.11+
- [Switch Console](https://github.com/sandbox-quantum/switch/releases) installed on Windows, macOS, or Linux
- Slack or Discord workspace with bot permissions

### 1. Import the Template into Switch Console
1. Launch **Switch Console**.
2. Navigate to **Templates** → **Import Custom Template**.
3. Select `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/TEMPLATE_YAML_SPECIFICATION.yaml`.
4. Fill in the template parameters:
   - `team`: `sre` (or your company prefix)
   - `bridge`: `slack` (or `discord`)
   - `provider`: `claude` (or `codex`, `opencode`)

### 2. Connect Your Integrations
In Switch Console → **Connections**:
- Connect **GitHub** (Read & Write permissions for repositories).
- Connect **Sentry** or **Datadog** (Read permissions for issues and metrics).

### 3. Kick Off the Incident Room
Click **Launch Group**. Switch Console automatically:
- Creates `#sre-incident-intake` and `#sre-incident-war-room` in your Slack/Discord.
- Spawns the three agents in their isolated working directories.
- Establishes the bi-directional room link.
- Emits the kickoff message introducing the on-call team.

---

## 📊 Live Scenario Simulation

Try typing this in `#sre-incident-intake`:
> *"@sre-triager checkout service is throwing HTTP 500 errors since the 09:30 UTC deploy. Users cannot complete purchases."*

**Watch the magic happen:**
1. `@sre-triager` confirms intake: *"Acknowledged. Classified as SEV-1 (Revenue Impact). Escalating to #sre-incident-war-room."*
2. In `#sre-incident-war-room`, `@ops-investigator` reports: *"Inspecting Sentry issues. Found NullPointerException in `CartService.java:142` introduced in commit `f3c8a91` (v2.14.0)."*
3. `@ops-investigator` runs a local repro test: *"Repro confirmed: passing empty coupon code triggers NPE."*
4. `@ops-remediator` chimes in: *"Rollback PR #412 prepared to restore v2.13.2. @Farhan (On-Call Lead), do you approve deployment?"*
5. You reply: *"Approved. Deploy rollback."*
6. `@ops-remediator` executes the merge, triggers deployment, verifies health endpoints return 200 OK, and posts a full post-mortem to `#sre-incident-intake`.

---

## 📁 Repository Layout

```
├── TEMPLATE_YAML_SPECIFICATION.yaml   # Production Switch Console template
├── PROJECT_SPECIFICATION.md          # Complete technical & functional architecture
├── ARCHITECTURE_DIAGRAMS.md          # System sequence & data flow diagrams
├── VIDEO_DEMO_SCRIPT_AND_STORYBOARD.md # Script for 3-minute video presentation
└── SUBMISSION_METADATA_AND_DEVPOST_TEXT.md # Full submission text for judges
```
