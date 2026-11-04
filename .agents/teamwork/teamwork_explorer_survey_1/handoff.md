# Track 01 Flagship Project "OpsSwitch" Codebase Survey & Gap Analysis

**Author:** Teamwork Explorer Survey 1  
**Date:** 2026-11-04  
**Target:** Track 01 — Best Business Workflow ($2,000 Cash Prize)  
**System Name:** OpsSwitch Autonomous Incident Commander & War Room  
**Artifact Path:** `d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_explorer_survey_1\handoff.md`

---

## 1. Observation

### 1.1 Blueprint Specifications in `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/`
A comprehensive, high-fidelity blueprint for OpsSwitch is present in `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/`. It consists of six key specification files:

1. **`PROJECT_SPECIFICATION.md`** (195 lines, 12,446 bytes):
   - **Problem Statement (lines 10–22):** Addresses enterprise downtime costs ($5,600/min), MTTA/MTTD diagnostic bottlenecks (70% of incident duration), and context switching across Sentry, GitHub, Datadog, Slack.
   - **Multi-Room Topology (lines 24–50):** Establishes two linked Switch rooms:
     - `#incident-intake`: Public channel for On-call engineers, PMs, customer support, and `ops-triager`. Ingestion, dedup, SEV classification, status updates, and final RCA.
     - `#incident-war-room`: Restricted channel for Incident Commander, `ops-investigator`, `ops-remediator`, and Lead On-Call Engineer. Deep-dive telemetry, commit diffing, deterministic repro execution, PR creation, and human sign-off.
     - Link label: `escalations` bridging intake and war room.
   - **Specialized Agent Roles (lines 52–93):**
     - `{team}-triager`: Addressing mode `anyone`. Classifies SEV-1 through SEV-4. Escalates SEV-1/SEV-2 across room link to `@{team}-investigator`. Posts executive post-mortem to intake on resolution.
     - `{team}-investigator`: Addressing mode `owner-agents`. Gathers telemetry, checks deployment commits within 2-hour window, runs semantic git diff, writes minimal deterministic reproduction script (`repro.py`), captures exit code/traceback, and hands off to `@{team}-remediator`.
     - `{team}-remediator`: Addressing mode `owner-agents`. Evaluates mitigation (git revert, rollback image, hotfix PR). Generates rollback branch & draft PR. Emits interactive Authorization Card with explicit gate (`"Awaiting sign-off from On-Call Lead @Farhan"`). Strictly enforces that zero merges/deployments occur without verbatim approval. Verifies recovery via HTTP 200 OK polling.
   - **Protocol Architecture (lines 96–122):** Switch Agent Protocol with SSE streaming in (`/v1/agents/{agent_id}/events`) and HTTP posting out (`/v1/rooms/{room_id}/messages`), with loopback MCP calls.
   - **State Machine (lines 124–164):** 4-phase lifecycle: `Ingestion & Triage` → `Investigation & Repro` → `Remediation & Human Gate` → `Post-Mortem & Closure`.
   - **Security & Blast Radius (lines 167–185):** Credential pass-through via Session Host (zero token leakage), Mandatory human-in-the-loop gate, Read-before-write privilege boundaries.
   - **Verification Plan (lines 186–195):** Calls for `scripts/simulate_incident.py`, `tests/test_incident_flow.py`, and Switch template integrity check.

2. **`TEMPLATE_YAML_SPECIFICATION.yaml`** (142 lines, 6,965 bytes):
   - **Version:** `version: 1`
   - **Parameters:** `team` (string, default "sre"), `provider` (provider, default `[claude, codex, opencode]`), `location` (location, default `local`), `directory` (directory, default `"{$agents_dir}/{agent}"`), `bridge` (bridge, default `[$first]`).
   - **Agents:** 3 declared agents (`{team}-triager`, `{team}-investigator`, `{team}-remediator`) with comprehensive role instructions.
   - **Group:** `"{team} Incident Command"`.
   - **Rooms:** `"{team}-incident-intake"` and `"{team}-incident-war-room"`, each with `bridge`, `agents`, `users: ["{$creator}"]`, and specialized `kickoff` messages.
   - **Links:** 1 directed link from `"{team}-incident-intake"` to `"{team}-incident-war-room"` with label `escalations`.

3. **`README.md`** (111 lines, 7,131 bytes):
   - OpsSwitch showcase with badges, overview, Switch centrality rationale, 5-minute quickstart guide, live scenario simulation script, and repository layout.

4. **`ARCHITECTURE_DIAGRAMS.md`** (149 lines, 6,417 bytes):
   - Dual-room topology graph, end-to-end 11-step incident resolution sequence diagram, and credential pass-through dataflow.

5. **`SUBMISSION_METADATA_AND_DEVPOST_TEXT.md`** (98 lines, 6,078 bytes):
   - Ready-to-submit Devpost/WeMakeDevs text: Team Algo Alchemist (`K8H5DE`), Lead Farhan Mallik (`@farhanmallik`), elevator pitch, problem narrative, technical implementation details, challenges, accomplishments, and tech stack tags.

6. **`VIDEO_DEMO_SCRIPT_AND_STORYBOARD.md`** (75 lines, 5,975 bytes):
   - 2m45s video storyboard across 6 acts with voiceover narration, visual cues, split-screen layout, and recording tips.

### 1.2 Current Workspace Implementation State
Inspection of the project root directory (`d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon`) revealed:
- Only three directories exist at root: `.agents`, `plan`, and `switch-repo`.
- **`scripts/simulate_incident.py` does NOT exist** (`find_by_name` returned 0 matches).
- **`scripts/` directory does NOT exist at project root**.
- **`tests/` directory does NOT exist at project root** (only `switch-repo/core/tests` exists, which contains upstream Switch core tests).
- **No standalone `template.yaml` exists at the root or under a dedicated `templates/` folder**.
- **No root-level `README.md` exists** to serve as the project entrypoint (the blueprint README is isolated inside `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/README.md`).
- **No root `pyproject.toml` or `requirements.txt` exists** for the OpsSwitch demonstration and test suite.

### 1.3 Verified Python Runtime & Dependency Environment
Execution of diagnostic commands on the local machine confirmed:
- **Python Version:** Python 3.13.14 (`python --version`)
- **UV Package Manager:** uv 0.11.2 (`uv --version`)
- **Test Runner:** pytest 9.0.3 (`pytest --version`)
- **Key Libraries Pre-installed in Global Environment:**
  - `pytest-asyncio` 1.3.0
  - `pydantic` 2.13.4
  - `yaml` (PyYAML) 6.0.3
  - `fastapi` 0.136.1
  - `uvicorn` 0.47.0
  - `httpx` 0.28.1
  - `sse-starlette` 1.6.5
  - `starlette` 0.46.2
- **Upstream Switch Core Environment:**
  - Located at `switch-repo/core/` with `pyproject.toml` and `uv.lock`.
  - Configured for `requires-python = ">=3.12"` with dependencies on `pydantic>=2`, `fastapi>=0.115`, `httpx>=0.28`, `PyYAML>=6`, `pytest>=8`, `pytest-asyncio>=0.24`.

### 1.4 Switch Template Schema Compliance & Analysis
- `TEMPLATE_YAML_SPECIFICATION.yaml` was parsed and checked against `switch-repo/core/switch_core/rooms_yaml.py` and `template_lint.py`.
- In `rooms_yaml.py`:
  - Top-level keys for v1 room groups are `version`, `params`, `agents`, `group`, `rooms`, `links`, which match `TEMPLATE_YAML_SPECIFICATION.yaml` exactly.
  - Declared parameter types (`string`, `provider`, `location`, `directory`, `bridge`) are valid members of `ParamType` and `CONSOLE_PARAM_TYPES`.
  - Placeholders (`{team}`, `{provider}`, `{location}`, `{directory}`, `{bridge}`) and builtins (`{$creator}`, `{$agents_dir}`) follow Switch placeholder parsing syntax (`PLACEHOLDER_RE = re.compile(r"\{(\$?[A-Za-z_][A-Za-z0-9_]*)\}")`).
  - Agent addressing policies (`anyone` for triager, `owner-agents` for investigator and remediator) are valid Switch agent addressing modes.
  - Linked rooms syntax (`from`, `to`, `label: escalations`) conforms to Switch's cross-room escalation primitives.
- Reference comparison: `switch-repo/examples/agent-templates/triage-pair.template.yaml` and `switch-repo/examples/room-templates/red-blue-workroom.template.yaml` demonstrate identical parameter handling, agent configurations, and kickoff message patterns.

---

## 2. Logic Chain

### Step 1: Mapping Acceptance Criteria (R1) to Blueprints
Requirement R1 in `ORIGINAL_REQUEST.md` stipulates:
- **Criterion 1:** Mock incident simulation script `scripts/simulate_incident.py` executes end-to-end without unhandled errors.
- **Criterion 2:** Pytest integration test suite for OpsSwitch passes with zero failures.
- **Criterion 3:** OpsSwitch template satisfies the Switch template specification and is verified.

Cross-referencing this with `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/PROJECT_SPECIFICATION.md` Section 6 and `plan/06_EXECUTION_TIMELINE_AND_CHECKLISTS/FINAL_SUBMISSION_AUDIT_CHECKLIST.md`:
- The mock incident script must simulate a realistic, reproducible microservice incident (specifically an HTTP 500 NullPointerException on `/checkout` triggered by coupon payload parsing in commit `f3c8a91`).
- The simulation must demonstrate the complete multi-agent workflow across the two rooms: alert ingestion → triage classification → war room escalation → diagnostic commit search → local reproduction execution → rollback PR generation → human authorization gate → rollback merge and health check verification → post-mortem RCA.
- The pytest suite must programmatically assert every stage of this lifecycle with zero flaky tests or external cloud dependencies.

### Step 2: Gap Assessment
Because no implementation code currently exists in `scripts/` or `tests/`, there is a 100% implementation delta between the blueprints and runnable code:
1. **Delta 1 (Simulation Engine):** No executable exists to demonstrate the incident scenario or drive the agents.
2. **Delta 2 (Test Suite):** No test suite exists to validate the template, state machine, gate enforcement, or API endpoints.
3. **Delta 3 (Workspace Layout):** Root directory lacks the expected project artifacts (`README.md`, `template.yaml`, runnable entrypoint).
4. **Delta 4 (Execution Tooling):** No root-level runner (`justfile` or standard `python -m pytest`) is pre-configured for judges to run `just test` or `just simulate` out of the box as promised in `FINAL_SUBMISSION_AUDIT_CHECKLIST.md:19`.

### Step 3: Simulation Engine Architectural Requirements
To ensure judges can run the project in under 60 seconds without requiring external paid API keys (Anthropic/OpenAI) or complex live Slack bridges, `scripts/simulate_incident.py` must feature:
- **Autonomous & Mock Mode:** A dual-mode design that can operate either in standalone simulation mode (fast, deterministic, zero-dependency) or against a live Switch server/bridge.
- **Embedded Mock Service:** A lightweight HTTP server representing the target microservice (`Cart & Checkout Service`), providing `/health` and `/checkout` endpoints.
- **Fault Injection:** An injectable defect where `POST /checkout` with `{"coupon": null}` or empty coupons crashes with HTTP 500 and a realistic stack trace (`NullPointerException in CartService:142`).
- **Deterministic Multi-Agent Turn Engine:**
  - `Triager`: Parses alert, extracts service name, assigns `SEV-1`, outputs intake acknowledgement, creates war room escalation payload.
  - `Investigator`: Queries commit history, identifies commit `f3c8a91` ("feat: coupon code parser"), dynamically synthesizes a minimal repro script, executes it in a temporary sandbox, captures the non-zero exit code and traceback, and notifies Remediator.
  - `Remediator`: Drafts rollback PR #412 reverting `f3c8a91`, renders the formatted Authorization Card, and prompts for human sign-off.
  - `Human Gate`: Evaluates input. Verifies that without `"Approved"`, execution is blocked. Upon receiving `"Approved. Roll it back."`, simulates PR merge, restores the service to HTTP 200 OK, and posts the final RCA post-mortem.
- **Rich CLI Flags:**
  - `--mode {simulate, serve, inject, interactive}`
  - `--port {port}` (default: 8000)
  - `--auto-approve` (bypasses manual interactive confirmation for CI/automated runs)
  - `--step-delay {seconds}` (controls pacing for live video demo)
  - `--json` (outputs structured event telemetry for automated validation)

### Step 4: Pytest Integration Test Suite Architectural Requirements
`tests/test_incident_flow.py` must provide exhaustive test coverage:
1. **Template Validation Test (`test_template_syntax_and_structure`):**
   - Validates that `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/TEMPLATE_YAML_SPECIFICATION.yaml` (and root `template.yaml`) is valid YAML.
   - Asserts all required top-level keys exist (`version: 1`, `params`, `agents`, `group`, `rooms`, `links`).
   - Asserts parameter typing and default fallback chains match Switch specifications.
   - Asserts both rooms (`{team}-incident-intake` and `{team}-incident-war-room`) and the link (`escalations`) are defined.
2. **Microservice Fault & Recovery Test (`test_mock_service_behavior`):**
   - Verifies `/health` returns 200 OK.
   - Verifies unhandled coupon payload triggers HTTP 500 with stack trace.
   - Verifies reverting defect restores `/checkout` to HTTP 200 OK.
3. **Triager Classification Test (`test_triager_severity_classification`):**
   - Tests SEV-1 assignment for checkout/payment/auth outages.
   - Tests SEV-2 for degraded functionality.
   - Tests SEV-3 and SEV-4 for minor/cosmetic issues.
   - Verifies escalation occurs only for SEV-1 and SEV-2.
4. **Investigator Diagnostic & Sandbox Repro Test (`test_investigator_repro_generation`):**
   - Verifies semantic diffing isolates commit `f3c8a91`.
   - Verifies repro script executes in sandbox and deterministically reproduces failure with exit code 1.
5. **Remediator Human Gate Enforcement Test (`test_remediator_gate_enforcement`):**
   - Asserts arbitrary text or rejection tokens (`"No"`, `"Wait"`) do not execute rollback.
   - Asserts exact approval phrase (`"Approved. Roll it back."`) passes the authorization gate.
   - Asserts merge and recovery are triggered only after approval.
6. **End-to-End Async Incident Lifecycle Test (`test_end_to_end_lifecycle`):**
   - Runs full lifecycle asynchronously from alert ingestion to final RCA summary.
   - Verifies all room turns and SSE events match expected states and sequences.
7. **Security & Zero-Token Leakage Test (`test_security_zero_token_leakage`):**
   - Asserts chat payloads and agent logs contain no hardcoded API keys, tokens, or private secrets.

---

## 3. Caveats

1. **Standalone Execution vs Full Switch Server Stack:** Running the complete upstream Switch Core server in `switch-repo/core` requires running PostgreSQL and Tuwunel or Docker containers (`just up`). For judging and grading reproducibility, `scripts/simulate_incident.py` and `tests/test_incident_flow.py` must be completely self-contained and run cleanly under standard Python 3.13 without requiring a running Docker daemon or live external databases.
2. **Read-Only Explorer Scope:** In accordance with the Explorer archetype and the user's explicit instructions, this investigation is strictly read-only. No source files, scripts, or tests have been created or modified in the project root or `switch-repo`. All proposed files and instructions are cataloged here for subsequent implementation agents.
3. **Template Format Versions (v1 vs v2):** Switch supports both v1 (group/rooms/links) and v2 (resources). The blueprint specifies v1, which is fully supported and matches official templates like `triage-pair.template.yaml`.

---

## 4. Conclusion & Actionable Implementation Plan

To fulfill Requirement R1 and achieve 100% compliance with the hackathon judging rubric, the following concrete deliverables must be implemented:

### Deliverables Breakdown

| # | Target File Path | Purpose & Description |
|---|---|---|
| 1 | `scripts/simulate_incident.py` | Production-grade incident simulation CLI supporting `--mode {simulate, serve, inject, interactive}`, embedded mock cart service, automated agent turns (triager, investigator, remediator), local sandbox repro script execution, human authorization gate, and final RCA reporting. |
| 2 | `tests/test_incident_flow.py` | Pytest integration suite with 7 exhaustive test cases covering template validation, mock service endpoints, SEV classification, git diff analysis, repro sandboxing, human sign-off gate, and end-to-end async workflow. |
| 3 | `template.yaml` (root) & `templates/opsswitch/template.yaml` | Directly importable Switch v1 template copied from `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/TEMPLATE_YAML_SPECIFICATION.yaml` for Switch Console import. |
| 4 | `README.md` (root) | Flagship entrypoint showcasing OpsSwitch, architecture diagrams, judging criteria alignment, Wispr Flow attribution, and copy-paste 5-minute quickstart. |
| 5 | `pyproject.toml` / `requirements.txt` (root) | Lightweight project definition specifying dependencies (`pytest`, `pytest-asyncio`, `fastapi`, `uvicorn`, `httpx`, `pyyaml`, `pydantic`). |
| 6 | `justfile` (root) | Simple runner recipes (`just simulate`, `just test`, `just serve`) to satisfy `FINAL_SUBMISSION_AUDIT_CHECKLIST.md:19`. |

### Implementation Roadmap for Implementer Agent:
1. **Step 1 (Root Template & Docs):** Copy `TEMPLATE_YAML_SPECIFICATION.yaml` to root `template.yaml` and `templates/opsswitch/template.yaml`. Place root `README.md` adapted from `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/README.md`.
2. **Step 2 (Mock Simulation Script):** Author `scripts/simulate_incident.py` implementing the mock web service (`FastAPI`), mock git repository commit logs, triager logic, investigator repro sandbox runner, remediator PR generator, human gate validator, and colorful formatted console output.
3. **Step 3 (Integration Test Suite):** Author `tests/test_incident_flow.py` using `pytest` and `pytest-asyncio` verifying all 7 test pillars.
4. **Step 4 (Validation):** Run `python scripts/simulate_incident.py --auto-approve` and `pytest tests/ -v` to ensure zero errors and 100% test pass rate.
5. **Step 5 (Root Configuration):** Add root `requirements.txt` and `justfile` ensuring frictionless one-command execution.

---

## 5. Verification Method

To independently verify the findings in this report, execute the following commands in the workspace root:

1. **Verify Missing Script & Test Files:**
   ```powershell
   Test-Path "scripts\simulate_incident.py"  # Expects False
   Test-Path "tests\test_incident_flow.py"  # Expects False
   Test-Path "template.yaml"                 # Expects False
   ```

2. **Verify Blueprint Template Syntax:**
   ```powershell
   python -c "import yaml; d = yaml.safe_load(open(r'plan\01_FLAGSHIP_PROJECT_BLUEPRINT\TEMPLATE_YAML_SPECIFICATION.yaml', encoding='utf-8')); assert d['version'] == 1; assert len(d['agents']) == 3; assert len(d['rooms']) == 2; print('Template syntax verified valid')"
   ```

3. **Verify Python Environment Readiness:**
   ```powershell
   python -c "import pytest, pytest_asyncio, fastapi, uvicorn, httpx, pydantic, yaml; print('All required testing & simulation packages available')"
   ```

4. **Post-Implementation Verification (Target Acceptance Test for Implementer):**
   ```powershell
   python scripts/simulate_incident.py --auto-approve
   pytest tests/test_incident_flow.py -v
   ```

### Invalidation Conditions
This survey report would be invalidated if:
- `TEMPLATE_YAML_SPECIFICATION.yaml` were found to use unsupported keys or incompatible parameter types under Switch v1 specifications (verified: keys and types are fully valid).
- Python 3.13 were incompatible with the required libraries (verified: all libraries imported successfully).
