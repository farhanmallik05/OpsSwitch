import os
from pathlib import Path

repo_root = Path(r"d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon\switch-repo")
sentry_dir = repo_root / "core" / "switch_core" / "connections" / "catalog" / "sentry"
sentry_dir.mkdir(parents=True, exist_ok=True)
skill_dir = sentry_dir / "skill"
skill_dir.mkdir(parents=True, exist_ok=True)

yaml_content = """slug: sentry
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
    revocation_discovered: true
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
"""

skill_content = """---
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
- **Safe Issue Management & Mutation:**
  - Resolving, muting, or ignoring an issue affects the entire engineering team's dashboard. A write grant allows modifying issue triage status. Only change issue states or triage metadata when explicitly asked by the on-call engineer or after verified deployment.
"""

(sentry_dir / "connection.yaml").write_bytes(yaml_content.replace("\r\n", "\n").encode("utf-8"))
(skill_dir / "SKILL.md").write_bytes(skill_content.replace("\r\n", "\n").encode("utf-8"))
print("WROTE SENTRY FILES SUCCESSFULLY")
