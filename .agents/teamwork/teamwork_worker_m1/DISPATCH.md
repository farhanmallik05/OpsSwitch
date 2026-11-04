# Dispatch for Worker M1: Track 01 OpsSwitch Flagship
Path to original request: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\ORIGINAL_REQUEST.md
Working directory: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_worker_m1
Explorer Report: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_explorer_survey_1\handoff.md
Project Scope: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\PROJECT.md

Exclusive File Ownership:
- template.yaml (root)
- templates/opsswitch/template.yaml
- README.md (root)
- scripts/simulate_incident.py
- tests/test_incident_flow.py
- pyproject.toml
- requirements.txt
- justfile

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## 2026-11-04T11:58:46Z
You are teamwork_worker assigned to Milestone 1: OpsSwitch Flagship Build & Verification.
Your working directory is: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_worker_m1

Implementation Tasks:
1. Create `template.yaml` at project root and `templates/opsswitch/template.yaml` by adapting `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/TEMPLATE_YAML_SPECIFICATION.yaml`. Ensure it satisfies Switch v1 template specifications (valid YAML, groups, rooms `{team}-incident-intake` and `{team}-incident-war-room`, link `escalations`, parameters, and agents).
2. Create root `README.md` adapted from `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/README.md` with complete documentation, architecture diagrams, and quickstart commands.
3. Build `scripts/simulate_incident.py`:
   - Full incident simulation CLI supporting `--mode {simulate, serve, inject, interactive}`, `--auto-approve`, `--port`, `--step-delay`, and `--json`.
   - Embedded mock Cart & Checkout service (FastAPI/Uvicorn) with `/health` returning 200 OK and `/checkout` failing with HTTP 500 when coupon is null/empty ("NullPointerException in CartService:142").
   - Deterministic multi-agent turn engine: Triager (SEV classification, intake acknowledgement, war room escalation), Investigator (commit diff search finding `f3c8a91`, minimal repro script generation and sandbox execution in temp directory with exit code 1), Remediator (draft rollback PR #412, render interactive Authorization Card, strict human approval gate checking for "Approved", simulated rollback merge restoring service to HTTP 200 OK, and final RCA post-mortem).
4. Build `tests/test_incident_flow.py`:
   - Comprehensive Pytest test suite covering all 7 pillars outlined in Explorer 1's report:
     1) `test_template_syntax_and_structure`
     2) `test_mock_service_behavior`
     3) `test_triager_severity_classification`
     4) `test_investigator_repro_generation`
     5) `test_remediator_gate_enforcement`
     6) `test_end_to_end_lifecycle`
     7) `test_security_zero_token_leakage`
5. Create root `requirements.txt`, `pyproject.toml`, and `justfile` (recipes: `simulate`, `test`, `serve`).
6. Run builds and verification commands:
   - `python scripts/simulate_incident.py --auto-approve`
   - `pytest tests/test_incident_flow.py -v`
   Ensure 100% pass rate with zero errors.
7. Document all created files, test execution outputs, and verification results in `handoff.md` in your directory.
Send a completion message when finished.

