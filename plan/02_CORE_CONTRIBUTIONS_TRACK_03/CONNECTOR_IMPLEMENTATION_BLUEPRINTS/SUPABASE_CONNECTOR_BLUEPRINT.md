# Supabase Connector Implementation Blueprint (Issue #827)

**Target Repository Path:** `core/switch_core/connections/catalog/supabase/`  
**Related Issue:** [#827 Add the Supabase connector](https://github.com/sandbox-quantum/switch/issues/827)  
**Shape:** Remote MCP server with OAuth Dynamic Client Registration (RFC 7591)

---

## 1. Complete `connection.yaml` Specification

Save to: `core/switch_core/connections/catalog/supabase/connection.yaml`

```yaml
slug: supabase
name: Supabase
category: Database
description: Inspect and manage Supabase databases, schemas, edge functions, and project telemetry.
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
    url: https://api.supabase.com/v1/profile
    account_id: id
    label: email
token:
  kind: pass_through
  max_lifetime: 86400
mcp:
  servers:
    - name: supabase
      url: "https://mcp.supabase.com/mcp"
      read_url: "https://mcp.supabase.com/mcp?read_only=true"
access:
  read:
    scopes:
      - "all"
  write:
    scopes:
      - "all"
tools:
  mode: pass_through
```

---

## 2. Complete `skill/SKILL.md` Specification

Save to: `core/switch_core/connections/catalog/supabase/skill/SKILL.md`

```markdown
---
name: supabase
description: Inspect database schemas, execute queries, audit logs, and manage Supabase projects acting with the connected user's permissions.
---

# Supabase

The `supabase` MCP server provides access to your Supabase projects, tables, migrations, and logs.

## How to Work Safely With Supabase

- **Read Before Writing:** Always inspect table schemas (`list_tables`, `execute_sql` with `SELECT` queries) before proposing migrations or schema changes.
- **Enforce Read-Only Boundaries:** When granted read-only access, mutations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`) are rejected at the connection endpoint via the read-only MCP URL.
- **Explicit Confirmation for Destructive SQL:**
  - Before running `DROP TABLE`, `ALTER TABLE`, or bulk `DELETE`, state the intended change in the chat room and obtain confirmation from an authenticated team member.
- **Data Privacy & Redaction:**
  - Database queries may return customer PII or encrypted tokens. Never post raw row dumps containing sensitive personal information directly into shared chat channels. Summarize row counts and structural schemas instead.
- **Project Scope Awareness:**
  - Tools operate across projects accessible to the authenticated account. Always specify the target `project_ref` to avoid accidental cross-project operations.
```

---

## 3. Maintainer-Mandated Architectural Enhancements (from @amaudruz)

In the issue discussion, Switch lead developer Louis Amaudruz (@amaudruz) mandated three specific loader enhancements for Supabase:

### (a) RFC 7591 Dynamic Client Secret Retention
In `core/switch_core/connections/adapters/oauth.py`:
When the OAuth dynamic client registration response includes a `client_secret` but omits `token_endpoint_auth_method`, default to storing and utilizing the secret as specified in RFC 7591 Section 2:
```python
# In oauth registration parser:
if "client_secret" in reg_data and not reg_data.get("token_endpoint_auth_method"):
    client_config["client_secret"] = reg_data["client_secret"]
    client_config["token_endpoint_auth_method"] = "client_secret_post"
```

### (b) Support for `read_url` on MCP Servers
In `core/switch_core/connections/loader.py`:
Allow an optional `read_url` on server definitions:
```python
# Validation rule:
if server.read_url:
    parsed_main = urlparse(server.url)
    parsed_read = urlparse(server.read_url)
    if (parsed_main.scheme, parsed_main.netloc, parsed_main.path) != (
        parsed_read.scheme, parsed_read.netloc, parsed_read.path
    ):
        raise CatalogError(f"read_url must share origin and path with url for server {server.name}")
```

### (c) List Index Support in Identity Paths
Allow single-element list indexing (e.g. `0.id` or `organizations.0.id`) when resolving account identity from API responses, returning a clean error if the list has zero or multiple items to prevent ambiguity.

---

## 4. Loader Unit Tests

Add to `core/tests/switch_core/connections/test_loader.py`:

```python
def test_supabase_catalog_entry():
    loader = ConnectionCatalogLoader()
    entry = loader.load_entry("supabase")
    assert entry.slug == "supabase"
    assert entry.enabled is True
    assert entry.adapter == "oauth"
    assert entry.mcp.servers[0].url == "https://mcp.supabase.com/mcp"
    assert entry.mcp.servers[0].read_url == "https://mcp.supabase.com/mcp?read_only=true"
```
