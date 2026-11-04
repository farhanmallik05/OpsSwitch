# Progress: Milestone 2 — Supabase Connector (Issue #827)

Last visited: 2026-11-04T12:35:00Z
Status: Completed

## Completed Tasks
- [x] Branch `feat/supabase-connector-827` checked out clean based on `upstream/main`.
- [x] Created `core/switch_core/connections/catalog/supabase/connection.yaml`.
- [x] Created `core/switch_core/connections/catalog/supabase/skill/SKILL.md` with strict LF line endings.
- [x] Copied `console/apps/switch-console-desktop/src/assets/images/connections/supabase.svg` from `mcp/supabase.svg`.
- [x] Updated `console/apps/switch-console-desktop/src/assets/images/connections/NOTICE.md` with Supabase attribution row.
- [x] Updated `console/apps/switch-console-desktop/src/renderer/features/switch-servers/connection-icon.tsx` with `supabase: 'text-[#3ECF8E]'`.
- [x] Enhanced `core/switch_core/connections/loader.py`: added optional `read_url` field to `McpServer` with origin/path validation.
- [x] Enhanced `core/switch_core/connections/broker.py`: routed `read` access level to `server.read_url` in `grants_for_agent()`.
- [x] Enhanced `core/switch_core/connections/adapters/oauth.py`: supported single-element list index resolution (`0.id`) in `_path_value` with strict single-element enforcement.
- [x] Enhanced `core/switch_core/connections/oauth_clients.py`: default `token_endpoint_auth_method` to `client_secret_post` when returned with `client_secret` without explicit method per RFC 7591.
- [x] Updated upstream test suites:
  - `core/tests/switch_core/connections/test_loader.py`
  - `core/tests/switch_core/connections/test_registry.py`
  - `core/tests/switch_core/gateway/test_connection_catalog.py`
  - `core/tests/switch_core/gateway/test_workspace_services.py`
- [x] Ran ruff lint and format check via uv: 100% clean.
- [x] Ran pytest on `test_loader.py` and `test_registry.py`: all 122 + 20 unit tests passed.
- [x] Committed changes with conventional commit: `feat(connections): add supabase service connection (#827)` (commit `3a65271d3`).
- [x] Pushed branch to `origin`: `git -C switch-repo push -u origin feat/supabase-connector-827`.
- [x] Opened live PR upstream: PR #1467 at `https://github.com/sandbox-quantum/switch/pull/1467`.
