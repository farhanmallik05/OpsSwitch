# Track 03: Pre-Formatted Assignment Request Templates

*Copy-paste these comments directly into the corresponding issues on `sandbox-quantum/switch` to be assigned by maintainer `@petr-sandbox`.*

---

## 1. Assignment Comment for Issue #827 (Supabase Connector)

**Target Issue:** https://github.com/sandbox-quantum/switch/issues/827  
**Action:** Paste into the issue comment box.

```markdown
Hi @petr-sandbox @amaudruz 👋

I would like to work on **Issue #827: Add the Supabase connector** for the Flip the Switch Hackathon.

### Proposed Implementation Plan:
1. **Catalog Entry & Skill:** Add `core/switch_core/connections/catalog/supabase/connection.yaml` and `skill/SKILL.md` targeting Supabase's official remote MCP server at `https://mcp.supabase.com/mcp` with OAuth and Dynamic Client Registration (RFC 7591).
2. **Read-Only Enforcement:** In accordance with @amaudruz's guidance, support the `read_url` property (`https://mcp.supabase.com/mcp?read_only=true`) so read grants prevent `execute_sql` mutations at the connection endpoint.
3. **Client Secret Handling:** Ensure RFC 7591 compliance where client secrets returned without an explicit auth method are preserved.
4. **Identity & Scoping:** Map user/organization identity cleanly, set account-wide scoping with explicit documentation, and enforce zero credential exposure to coding tools.
5. **Assets & Validation:** Add official SVG mark credited in `NOTICE.md`, add loader unit tests in `core/tests/switch_core/connections/test_loader.py`, verify against `just check`, `just typecheck`, and `just test`, and record the connect → grant → room task → revoke verification flow.

Could you please assign me to this issue? Thank you!
```

---

## 2. Assignment Comment for Issue #820 (Sentry Connector)

**Target Issue:** https://github.com/sandbox-quantum/switch/issues/820  
**Action:** Paste into the issue comment box.

```markdown
Hi @petr-sandbox @amaudruz 👋

I'd like to implement **Issue #820: Add the Sentry connector** for the hackathon.

### Proposed Implementation Plan:
1. **Catalog Configuration:** Add `core/switch_core/connections/catalog/sentry/connection.yaml` pointing to the official remote MCP endpoint at `https://mcp.sentry.dev/mcp`.
2. **Authentication Flow:** Support both OAuth PKCE S256 and personal auth token pass-through via Switch's session host broker.
3. **Skill Guidelines:** Author `skill/SKILL.md` enforcing safe observability workflows: narrow query bounds by project/environment, summarize logs/stack traces rather than pasting raw tokens, and default to read-only issue inspection.
4. **Verification & Tests:** Add unit tests to `test_loader.py`, verify full linter/test pass (`just test`), add official logo attribution in `NOTICE.md`, and record the verification video.

Could you please assign me to this issue? Thanks!
```

---

## 3. Assignment Comment for Issue #808 (Five-Minute Quickstart)

**Target Issue:** https://github.com/sandbox-quantum/switch/issues/808  
**Action:** Paste into the issue comment box.

```markdown
Hi @petr-sandbox @amaudruz 👋

I'd like to take on **Issue #808: Five-minute quickstart for new contributors**.

### Proposed Implementation Plan:
1. **Up-to-Date Commands:** Author `docs/contributing/quickstart.md` and link it from `CONTRIBUTING.md`. Follow current `main` using `just init-env` (for fresh generated secrets), `uv sync`, `just up`, and `just run`.
2. **Cross-Platform & Windows Handling:** Include exact prerequisites across macOS, Linux, and Windows (mentioning Windows Git CRLF handling and `.gitattributes` normalization).
3. **Console to Room Walkthrough:** Document building/running Switch Console from `console/`, pointing it at `http://localhost:8000`, creating an agent and room, and verifying the first response.
4. **Repository Tour & Quality Gates:** Provide a concise map of `core/`, `console/`, and `gateway/`, and document the mandatory checks (`just check`, `just typecheck`, `just test`).
5. **Dry-Run Validation:** I will validate every single command on a clean environment and report timing and exact steps in the PR.

Please assign this issue to me. Thank you!
```

---

## 4. Assignment Comment for Issue #807 (Agent Controller Guide)

**Target Issue:** https://github.com/sandbox-quantum/switch/issues/807  
**Action:** Paste into the issue comment box.

```markdown
Hi @petr-sandbox @amaudruz 👋

I would like to work on **Issue #807: Write the agent controller guide**.

### Proposed Implementation Plan:
1. **Official User Guide:** Author `docs/official/deploy/agent-controller.md` and link it into `docs/official/TOC.md`, following the established official documentation tone and formatting.
2. **Core Coverage:**
   - Architecture & prerequisites (Node 22+, provider CLIs, OS support).
   - One-line install and enrollment using codes from the gateway's Machines page.
   - Managing as a system service: `status`, `doctor`, `update`, and logs.
   - Shared vs. isolated agent host execution models.
   - Provider authentication and credential isolation.
   - Diagnostic troubleshooting table covering common failure reason codes.
3. **Validation:** Synthesize from `console/packages/agent-controller/README.md` and design specifications, verify against a live clean instance, and ensure all commands reflect the current release.

Could you please assign this to me? Thanks!
```

---

## 5. Assignment Comment for Issue #829 (Stripe Connector)

**Target Issue:** https://github.com/sandbox-quantum/switch/issues/829  
**Action:** Paste into the issue comment box.

```markdown
Hi @petr-sandbox @amaudruz 👋

I'd like to work on **Issue #829: Add the Stripe connector**.

### Proposed Implementation Plan:
1. **Catalog Entry:** Add `core/switch_core/connections/catalog/stripe/connection.yaml` using Stripe's official remote MCP server at `https://mcp.stripe.com` with OAuth PKCE.
2. **Safe Defaults:** Configure read-only as the default permission level (customer, payment, and subscription read-only queries), with explicit in-app guidance recommending Stripe test-mode keys for evaluation.
3. **Skill Specification:** Add `skill/SKILL.md` providing bounded customer/charge queries, masking sensitive PII/payment tokens, and disallowing balance mutations or refunds without explicit user sign-off.
4. **Tests & Attribution:** Add test cases in `core/tests/switch_core/connections/test_loader.py`, credit the official SVG mark in `NOTICE.md`, and record the Console connect/grant/query demo.

Could you please assign this to me? Thank you!
```
