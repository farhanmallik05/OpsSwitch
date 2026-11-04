# Sentry Connector Implementation Blueprint (Issue #820)

**Target Repository Path:** `core/switch_core/connections/catalog/sentry/`  
**Related Issue:** [#820 Add the Sentry connector](https://github.com/sandbox-quantum/switch/issues/820)  
**Shape:** Remote MCP server with OAuth Dynamic Registration & API Key support

---

## 1. Complete `connection.yaml` Specification

Save to: `core/switch_core/connections/catalog/sentry/connection.yaml`

```yaml
slug: sentry
name: Sentry
category: Observability
description: Query Sentry error issues, stack traces, tags, and releases acting with your Sentry credentials.
enabled: true
adapter: oauth
auth:
  type: oauth
  refresh: rotating
  oauth:
    registration: dynamic
    redirect: [loopback]
    loopback_ports: [39231, 39232, 39233, 39234, 39235]
    prompt: consent
  identity:
    url: https://sentry.io/api/0/users/me/
    account_id: id
    label: email
token:
  kind: pass_through
  max_lifetime: 28800
mcp:
  servers:
    - name: sentry
      url: "https://mcp.sentry.dev/mcp"
access:
  read:
    scopes:
      - "event:read"
      - "project:read"
      - "org:read"
  write:
    scopes:
      - "event:read"
      - "event:write"
      - "event:admin"
      - "project:read"
      - "org:read"
tools:
  mode: pass_through
```

---

## 2. Complete `skill/SKILL.md` Specification

Save to: `core/switch_core/connections/catalog/sentry/skill/SKILL.md`

```markdown
---
name: sentry
description: Investigate software defects and crashes through Sentry's official MCP tools — issues, stack traces, breadcrumbs, tags, and release health.
---

# Sentry

The `sentry` MCP server provides access to error events, crash reports, and issue tracking.

## Operational Guidelines

- **Narrow Time Windows First:**
  - Always specify an organization, project slug, and time window (e.g. `last 1 hour` or `since deploy`) when searching events to avoid hitting rate limits.
- **Isolate Stack Traces & Culprits:**
  - When analyzing an issue, retrieve the stack trace frames and highlight the in-app application files rather than third-party vendor dependencies.
- **Summarize Rather Than Paste:**
  - Raw Sentry traces can contain customer cookies, IP addresses, or request headers. Extract only the exception type, message, and file:line culprits into room messages.
- **Safe Issue Management:**
  - Resolving or ignoring an issue affects the entire engineering team's dashboard. Only mark issues as resolved when explicitly asked by the on-call engineer or after verified deployment.
```

---

## 3. Loader Unit Tests

Add to `core/tests/switch_core/connections/test_loader.py`:

```python
def test_sentry_catalog_entry():
    loader = ConnectionCatalogLoader()
    entry = loader.load_entry("sentry")
    assert entry.slug == "sentry"
    assert entry.enabled is True
    assert entry.category == "Observability"
    assert entry.adapter == "oauth"
    assert entry.mcp.servers[0].url == "https://mcp.sentry.dev/mcp"
    assert "event:read" in entry.access.read.scopes
```
