# Dispatch for Worker M2: Track 03 Supabase Connector (Issue #827)
Path to original request: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\ORIGINAL_REQUEST.md
Working directory: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_worker_m2
Explorer Report: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_explorer_survey_2\handoff.md
Project Scope: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\PROJECT.md
Blueprints: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\plan\02_CORE_CONTRIBUTIONS_TRACK_03\

Exclusive File Ownership:
- switch-repo/core/switch_core/connections/catalog/supabase/connection.yaml
- switch-repo/core/switch_core/connections/catalog/supabase/skill/SKILL.md
- switch-repo/console/apps/switch-console-desktop/src/assets/images/connections/supabase.svg
- switch-repo/console/apps/switch-console-desktop/src/assets/images/connections/NOTICE.md
- switch-repo/console/apps/switch-console-desktop/src/renderer/features/switch-servers/connection-icon.tsx
- switch-repo/core/switch_core/connections/loader.py
- switch-repo/core/switch_core/connections/broker.py
- switch-repo/core/switch_core/connections/adapters/oauth.py
- switch-repo/core/switch_core/connections/oauth_clients.py
- switch-repo/core/tests/switch_core/connections/test_loader.py
- switch-repo/core/tests/switch_core/connections/test_registry.py
- switch-repo/core/tests/switch_core/gateway/test_connection_catalog.py
- switch-repo/core/tests/switch_core/gateway/test_workspace_services.py

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## 2026-11-04T12:08:23Z
You are teamwork_worker assigned to Milestone 2: Upstream Supabase Connector (Issue #827) in `switch-repo/`.
Your working directory is: d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\.agents\teamwork\teamwork_worker_m2

Technical Mandates (from Lead Maintainer Louis Amaudruz @amaudruz):
1. Support optional `read_url` on `McpServer` (`core/switch_core/connections/loader.py`), e.g., `"https://mcp.supabase.com/mcp?read_only=true"`, and route read grants to it in `broker.py` (`standing()` method).
2. Support single-element array indexing (e.g. `0.id`) in `_path_value` (`core/switch_core/connections/adapters/oauth.py`) when resolving user/organization identity.
3. RFC 7591 dynamic registration: In `core/switch_core/connections/oauth_clients.py`, retain `client_secret` when returned without explicit `token_endpoint_auth_method`, defaulting to `client_secret_post`.
4. Ensure `SKILL.md` uses LF line endings (required for regex frontmatter parsing).
