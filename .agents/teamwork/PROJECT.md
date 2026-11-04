# Project: Flip the Switch Hackathon Deliverables Showcase

## Architecture
- **Track 01 (OpsSwitch Flagship)**: Dual-room autonomous incident commander built on Switch v1 template specification. Links public `#incident-intake` to restricted `#incident-war-room`. Microservice mock fault simulation, 3 autonomous agent roles (`{team}-triager`, `{team}-investigator`, `{team}-remediator`), deterministic repro sandboxing, and interactive human-in-the-loop sign-off gate before rollback.
- **Track 03 (Upstream Core Contributions)**: Service Connections v2 connectors for Supabase (Issue #827) and Sentry (Issue #820) in `switch-repo/`. Adheres strictly to maintainer mandates: `read_url` query-level isolation and RFC 7591 dynamic secret retention for Supabase; Petr's pass-through tool rule and single-level write/triage for Sentry; LF line ending enforcement for catalog skills.
- **Side Tracks**:
  - DEV.to Blog Track: 278-line technical deep-dive article ready for direct publishing via DevRelay MCP.
  - Wispr Flow Voice Track: 5 verbatim prompt dictation scripts covering 4,000+ words, desktop scorecard guidelines.
  - Social Media Track: 5 crafted `#HowISwitch` posts and 30-second teaser video storyboard.
- **Submission & Governance**: Team Algo Alchemist (`K8H5DE`, Farhan Mallik `farhanmallik05`). Upstream PR #1397 and PR #1399 open and CLA-signed.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | OpsSwitch Root Template | Switch v1 template copied from `plan/01_FLAGSHIP_PROJECT_BLUEPRINT/` to root and `templates/opsswitch/template.yaml` | M1 | survey 1 |
| 2 | OpsSwitch Incident Simulation CLI | Production-grade `scripts/simulate_incident.py` supporting mock service, triager classification, investigator repro sandbox, remediator PR & human gate | M1 | survey 1 |
| 3 | OpsSwitch Pytest Integration Suite | `tests/test_incident_flow.py` with 7 testing pillars verifying template, endpoints, classification, repro, human gate, async lifecycle, and zero token leakage | M1 | survey 1 |
| 4 | OpsSwitch Showcase README & Config | Root `README.md`, `pyproject.toml`, `requirements.txt`, and `justfile` for one-command test & simulation execution | M1 | survey 1 |
| 5 | Supabase Connection Catalog & Skill | `core/switch_core/connections/catalog/supabase/connection.yaml` and `skill/SKILL.md` with LF line endings | M2 | survey 2 |
| 6 | Supabase Desktop Icon & Attribution | Simple Icons SVG, `NOTICE.md`, and `connection-icon.tsx` color mapping | M2 | survey 2 |
| 7 | Supabase Core Loader & Broker Enhancements | `read_url` on `McpServer`, read grant routing in broker, list indexing `0.id`, and RFC 7591 secret retention | M2 | survey 2 |
| 8 | Supabase Unit & Gateway Test Suite | Updates to `test_loader.py`, `test_registry.py`, `test_connection_catalog.py`, `test_workspace_services.py` | M2 | survey 2 |
| 9 | Supabase Git Branch & PR Preparation | Branch `feat/supabase-connector-827` off upstream/main, committed and pushed to origin, PR opened upstream | M2 | survey 2 |
| 10 | Sentry Connection Catalog & Skill | `core/switch_core/connections/catalog/sentry/connection.yaml` and `skill/SKILL.md` complying with Petr's pass-through rule | M3 | survey 2 |
| 11 | Sentry Desktop Icon & Attribution | Simple Icons SVG, `NOTICE.md`, and `connection-icon.tsx` color mapping | M3 | survey 2 |
| 12 | Sentry Unit & Gateway Test Suite | Updates to `test_loader.py`, `test_registry.py`, `test_connection_catalog.py`, `test_workspace_services.py` | M3 | survey 2 |
| 13 | Sentry Git Branch & PR Preparation | Branch `feat/sentry-connector-820` off upstream/main, committed and pushed to origin, PR opened upstream | M3 | survey 2 |
| 14 | DEV.to Technical Blog Publication | Finalize markdown, generate visual banner, publish draft/article via DevRelay MCP `create_article` | M4 | survey 3 |
| 15 | Wispr Flow Voice Track Finalization | Finalize scorecard readiness checklist, verify 4,000+ word dictation scripts | M4 | survey 3 |
| 16 | Social Media Post Assets Generation | Finalize 5 `#HowISwitch` post copy and generate visual banner cards | M4 | survey 3 |
| 17 | E2E Integration & Verification | Run full OpsSwitch simulation and pytest suite, run upstream connector tests, verify all pass | M5 | survey 1, 2 |
| 18 | Forensic Integrity Audit & Pre-Flight | Run `teamwork_auditor` across all deliverables to verify zero cheating, clean code, and check submission checklist | M5 | survey 3 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | OpsSwitch Flagship Build & Verification | Root template, simulation script, pytest suite, README, runner configs | none | DONE |
| M2 | Supabase Connector (Issue #827) | Catalog entry, skill, core loader/broker updates, tests, git branch/PR | none | DONE |
| M3 | Sentry Connector (Issue #820) | Catalog entry, skill, tests, git branch/PR | none | DONE |
| M4 | Side Tracks (Blog, Wispr, Social) | DEV.to draft creation via MCP, Wispr scripts checklist, social assets | none | DONE |
| M5 | E2E Verification & Forensic Integrity Audit | Full test suite execution, forensic audit check, pre-flight submission verification | M1, M2, M3, M4 | IN_PROGRESS |

## Interface Contracts
### OpsSwitch Simulation ↔ Pytest Suite
- Script: `scripts/simulate_incident.py`
  - Classes: `MockService`, `IncidentCommanderSimulation`, `Triager`, `Investigator`, `Remediator`
  - CLI Flags: `--mode {simulate, serve, inject, interactive}`, `--auto-approve`, `--port`, `--json`
  - Output: Exit code 0 on successful resolution, JSON event stream when `--json` is supplied
- Tests: `tests/test_incident_flow.py` imports simulation classes directly or executes via CLI subprocess, asserting status codes, SEV classification, git diff reproduction, and human approval blocking.

### Switch Core ↔ Connectors
- Catalog YAML: `core/switch_core/connections/catalog/<slug>/connection.yaml`
  - Schema: `ConnectionDefinition` (Pydantic v2) in `loader.py`
  - Skill: `core/switch_core/connections/catalog/<slug>/skill/SKILL.md` with LF line endings and standard YAML frontmatter (`name`, `description`).
- Supabase MCP Server:
  - `url`: `https://mcp.supabase.com/mcp`
  - `read_url`: `https://mcp.supabase.com/mcp?read_only=true`
  - `tools.mode`: `pass_through`
- Sentry MCP Server:
  - `url`: `https://mcp.sentry.dev/mcp`
  - `tools.mode`: `pass_through`
  - Capabilities: `inspect`, `triage`, `seer`

## Code Layout
```
d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\
├── .agents/teamwork/                   # Orchestrator & subagent metadata
├── plan/                               # Master hackathon blueprints
├── template.yaml                       # Root OpsSwitch Switch v1 template
├── templates/opsswitch/template.yaml   # Packaged OpsSwitch template
├── scripts/
│   └── simulate_incident.py            # OpsSwitch incident simulation CLI
├── tests/
│   └── test_incident_flow.py           # OpsSwitch pytest integration suite
├── pyproject.toml                      # OpsSwitch root pyproject
├── requirements.txt                    # OpsSwitch requirements
├── justfile                            # Runner recipes (just simulate, just test)
├── README.md                           # Flagship OpsSwitch showcase README
├── assets/                             # Visual media assets (blog cover, cards)
└── switch-repo/                        # Upstream Switch repository fork
    ├── core/
    │   ├── switch_core/connections/
    │   │   ├── catalog/
    │   │   │   ├── supabase/           # Supabase connector definition & skill
    │   │   │   └── sentry/             # Sentry connector definition & skill
    │   │   ├── loader.py               # McpServer read_url support
    │   │   ├── broker.py               # Read grant routing
    │   │   ├── adapters/oauth.py       # List indexing 0.id
    │   │   └── oauth_clients.py        # RFC 7591 dynamic secret retention
    │   └── tests/switch_core/
    │       ├── connections/test_loader.py
    │       ├── connections/test_registry.py
    │       └── gateway/test_connection_catalog.py
    └── console/apps/switch-console-desktop/src/
        ├── assets/images/connections/  # supabase.svg & sentry.svg
        └── renderer/features/switch-servers/connection-icon.tsx
```
