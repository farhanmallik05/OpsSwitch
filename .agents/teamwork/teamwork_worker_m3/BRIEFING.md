# BRIEFING — 2026-11-04T12:46:00Z

## Mission
Implement Upstream Sentry Connector (Issue #820) in switch-repo/ adhering strictly to maintainer Petr Bauch's mandate, passing all tests, linting, git commit, push, and PR submission.

## 🔒 My Identity
- Archetype: teamwork_worker
- Roles: implementer, qa, specialist
- Working directory: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_worker_m3
- Original parent: 58b8df99-e93b-412c-882c-dcd20cc7ae7c
- Milestone: Milestone 3 (Upstream Sentry Connector #820)

## 🔒 Key Constraints
- DO NOT CHEAT: Genuine implementation only, no dummy/facade implementations or hardcoded test results.
- Maintainer Mandate: tools.mode: listed isn't available for OAuth entries. Pass-through tools required. If OAuth, offer ONE write/triage level honestly stating what it can change. Or adapter: api_key with personal token pass-through (mirroring Datadog pattern).
- Minimal changes: Only touch assigned files.
- Test suites must pass via uv.
- Clean branch feat/sentry-connector-820 based on upstream/main.

## Current Parent
- Conversation ID: 58b8df99-e93b-412c-882c-dcd20cc7ae7c
- Updated: 2026-11-04T12:46:00Z

## Task Summary
- **What to build**: Declarative connection `sentry/connection.yaml`, `skill/SKILL.md`, icon asset `sentry.svg`, `NOTICE.md` attribution, `connection-icon.tsx`, and updated tests.
- **Success criteria**: All core tests pass, ruff passes, branch pushed, PR created or ready.
- **Interface contracts**: `d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\plan\02_CORE_CONTRIBUTIONS_TRACK_03\CONNECTOR_IMPLEMENTATION_BLUEPRINTS\SENTRY_CONNECTOR_BLUEPRINT.md`
- **Code layout**: `switch-repo/core/switch_core/connections/catalog/sentry/`

## Key Decisions Made
- Implemented OAuth dynamic registration with pass-through tools (`tools: { mode: pass_through }`) adhering strictly to maintainer Petr Bauch's mandate.
- Defined honest access levels with read (`event:read`, `project:read`, `org:read`) and write (`event:read`, `event:write`, `event:admin`, `project:read`, `org:read`).
- Configured loopback redirect ports [39231, 39232, 39233, 39234, 39235], prompt: consent, and revocation_discovered: true.
- Authored clear operational guidelines in `SKILL.md` with LF line endings (`\n`) for stack trace inspection and safe issue mutation.
- Successfully created live upstream PR #1471 on `sandbox-quantum/switch`.

## Artifact Index
- DISPATCH.md — assignment details
- progress.md — liveness heartbeat and progress tracking
- pr_body.md — PR body text
- handoff.md — final handoff report

## Change Tracker
- **Files modified**:
  - `core/switch_core/connections/catalog/sentry/connection.yaml` (new declarative Sentry connection)
  - `core/switch_core/connections/catalog/sentry/skill/SKILL.md` (new Sentry operational guidelines skill)
  - `console/apps/switch-console-desktop/src/assets/images/connections/sentry.svg` (vendored Simple Icons mark)
  - `console/apps/switch-console-desktop/src/assets/images/connections/NOTICE.md` (added Sentry Simple Icons attribution)
  - `console/apps/switch-console-desktop/src/renderer/features/switch-servers/connection-icon.tsx` (added sentry mark color)
  - `core/tests/switch_core/connections/test_loader.py` (added sentry to catalog assertions & 2 unit tests)
  - `core/tests/switch_core/connections/test_registry.py` (added sentry to adapters set & 1 unit test)
  - `core/tests/switch_core/gateway/test_connection_catalog.py` (added sentry status pop assertion)
  - `core/tests/switch_core/gateway/test_workspace_services.py` (added sentry to workspace services set)
- **Build status**: Ruff check passed (100%), Pytest loader/registry tests passed (100%)
- **Pending issues**: None

## Quality Status
- **Build/test result**: Pass (8/8 loader tests, 4/4 registry tests, 1375 files ruff checked)
- **Lint status**: 0 violations, clean
- **Tests added/modified**: `test_the_shipped_sentry_entry_signs_in_and_configures_adapter`, `test_sentry_catalog_entry`, `test_sentry_needs_no_settings_and_registers_its_ports_and_scopes`

## Loaded Skills
- None
