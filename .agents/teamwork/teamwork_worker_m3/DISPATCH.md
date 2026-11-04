# Dispatch for Worker M3: Track 03 Sentry Connector (Issue #820)
Path to original request: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\ORIGINAL_REQUEST.md
Working directory: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_worker_m3
Explorer Report: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_explorer_survey_2\handoff.md
Project Scope: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\PROJECT.md
Blueprints: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\plan\02_CORE_CONTRIBUTIONS_TRACK_03\CONNECTOR_IMPLEMENTATION_BLUEPRINTS\02_SENTRY_CONNECTOR_BLUEPRINT.md

Exclusive File Ownership:
- switch-repo/core/switch_core/connections/catalog/sentry/connection.yaml
- switch-repo/core/switch_core/connections/catalog/sentry/skill/SKILL.md
- switch-repo/console/apps/switch-console-desktop/src/assets/images/connections/sentry.svg
- switch-repo/console/apps/switch-console-desktop/src/assets/images/connections/NOTICE.md
- switch-repo/console/apps/switch-console-desktop/src/renderer/features/switch-servers/connection-icon.tsx
- switch-repo/core/tests/switch_core/connections/test_loader.py
- switch-repo/core/tests/switch_core/connections/test_registry.py
- switch-repo/core/tests/switch_core/gateway/test_connection_catalog.py
- switch-repo/core/tests/switch_core/gateway/test_workspace_services.py

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## 2026-11-04T12:31:57Z
You are teamwork_worker assigned to Milestone 3: Upstream Sentry Connector (Issue #820) in `switch-repo/`.
Your working directory is: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_worker_m3

Tasks to implement in `switch-repo/`:
1. Check out a clean branch `feat/sentry-connector-820` based on `upstream/main`:
   `git -C switch-repo checkout -b feat/sentry-connector-820 upstream/main`
2. Create:
   - `core/switch_core/connections/catalog/sentry/connection.yaml`:
     - Declarative connection adhering strictly to Petr Bauch's mandate:
       - Either OAuth with pass-through tools (`tools: { mode: pass_through }`) and an honest write/triage access level stating what it can change.
       - Or `adapter: api_key` with personal token pass-through (`https://sentry.io/api/0/users/me/`) and header `Authorization: Bearer {api_key}`, `issued_to_agents: false`, exactly mirroring Datadog's approved pattern.
   - `core/switch_core/connections/catalog/sentry/skill/SKILL.md`:
     - Practical instructions for stack trace triage, issue inspection, time window scoping, and mutation guidelines. Enforce LF line endings (`\n`).
   - Copy `console/apps/switch-console-desktop/src/assets/images/connections/sentry.svg` from `mcp/sentry.svg`.
   - Update `NOTICE.md` with Simple Icons attribution for Sentry.
   - Update `connection-icon.tsx` with `sentry: 'text-[#362D59] emdark:text-foreground'`.
3. Update upstream test suites to assert `"sentry"`:
   - `core/tests/switch_core/connections/test_loader.py`
   - `core/tests/switch_core/connections/test_registry.py`
   - `core/tests/switch_core/gateway/test_connection_catalog.py`
   - `core/tests/switch_core/gateway/test_workspace_services.py`
   - Add unit tests verifying the shipped Sentry entry parses, loads its skill, and configures the adapter properly.
4. Run tests and linting via uv:
   - `uv run --project switch-repo/core ruff check switch-repo/core/`
   - `uv run --project switch-repo/core pytest switch-repo/core/tests/switch_core/connections/test_loader.py`
   - `uv run --project switch-repo/core pytest switch-repo/core/tests/switch_core/connections/test_registry.py`
   Ensure all tests pass.
5. Commit changes with conventional commit: `feat(connections): add sentry service connection (#820)`.
6. Push branch to `origin`: `git -C switch-repo push -u origin feat/sentry-connector-820`.
7. Attempt live PR creation using `gh pr create --repo sandbox-quantum/switch --head farhanmallik05:feat/sentry-connector-820 --base main --title "feat(connections): add sentry service connection" --body "..."` (closes #820). If opened, record PR URL; if not, ensure branch is pushed and ready.
8. Write complete handoff to `handoff.md` in your directory and send completion message.
