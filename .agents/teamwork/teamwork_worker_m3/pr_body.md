## Summary

Adds the official Sentry service connection to the Switch connection catalog, closing #820.

### Maintainer Mandate Alignment (Issue #820)
In accordance with maintainer guidance from @petr-sandbox on Issue #820:
- Configures `adapter: oauth` with `registration: dynamic` and `redirect: [loopback]` on ports 39231-39235.
- Uses `tools: { mode: pass_through }` as required for OAuth entries by the loader (`an oauth entry's tools pass through until classified`).
- Offers honest access levels:
  - `read`: strictly read scopes (`event:read`, `project:read`, `org:read`).
  - `write`: triage and mutation scopes (`event:read`, `event:write`, `event:admin`, `project:read`, `org:read`).
- The connection skill (`SKILL.md`) and catalog entry explicitly document what write grants can change (issue triage status, resolving/muting errors) and enforce operational safety rules (scoping queries, narrowing time windows, avoiding mass resolution).

### Changes Included
1. **Catalog Entry:** `core/switch_core/connections/catalog/sentry/connection.yaml`
2. **Connection Skill:** `core/switch_core/connections/catalog/sentry/skill/SKILL.md`
3. **Desktop Assets & Color Tokens:**
   - Vendored Simple Icons SVG logo: `console/apps/switch-console-desktop/src/assets/images/connections/sentry.svg`
   - Attribution notice in `NOTICE.md`
   - Brand color mapping in `connection-icon.tsx` (`sentry: 'text-[#362D59] emdark:text-foreground'`)
4. **Test Suite Enhancements:**
   - `core/tests/switch_core/connections/test_loader.py`: Shipped catalog entry tests, skill validation, scope assertions.
   - `core/tests/switch_core/connections/test_registry.py`: Dynamic client registration and scope configuration tests.
   - `core/tests/switch_core/gateway/test_connection_catalog.py`: Catalog listing status assertion.
   - `core/tests/switch_core/gateway/test_workspace_services.py`: Default workspace service assertion.

Closes #820.
