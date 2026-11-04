# Track 03: Live Target Issues Audit & Intelligence

**Repository:** `sandbox-quantum/switch`  
**Filter:** `is:issue state:open label:hackathon`  
**Audit Date:** November 3, 2026 (Hackathon Eve)

---

## 1. High-Value Connector Issues (`area: connector`)

Connectors follow the **Service Connections v2** architecture (`docs/design/service-connections-v2.md`). Each connector consists of:
1. `core/switch_core/connections/catalog/<name>/connection.yaml`
2. `core/switch_core/connections/catalog/<name>/skill/SKILL.md`
3. Official SVG mark and credit in `NOTICE.md`
4. Test entries in `core/tests/switch_core/connections/test_loader.py`

### Top Picks for Our Pipeline:

#### 1. Issue #827: Add the Supabase connector (Difficulty: Easy | Priority: P2)
- **URL:** `https://github.com/sandbox-quantum/switch/issues/827`
- **Vendor Endpoint:** Official remote MCP server at `https://mcp.supabase.com/mcp`
- **Auth:** OAuth with Dynamic Client Registration (RFC 7591)
- **Key Maintainer Requirement (from @amaudruz):**
  - Retain `client_secret` when returned without explicit auth method.
  - Support `read_url` (`https://mcp.supabase.com/mcp?read_only=true`) for read grants so `execute_sql` cannot mutate in read mode.
  - Allow list indexing (`0.id`) for organization identity with single-entry validation.
- **Blueprint Location:** `plan/02_CORE_CONTRIBUTIONS_TRACK_03/CONNECTOR_IMPLEMENTATION_BLUEPRINTS/SUPABASE_CONNECTOR_BLUEPRINT.md`

#### 2. Issue #820: Add the Sentry connector (Difficulty: Easy | Priority: P1)
- **URL:** `https://github.com/sandbox-quantum/switch/issues/820`
- **Vendor Endpoint:** Official remote MCP server at `https://mcp.sentry.dev/mcp`
- **Auth:** OAuth or API Key pass-through token header.
- **Blueprint Location:** `plan/02_CORE_CONTRIBUTIONS_TRACK_03/CONNECTOR_IMPLEMENTATION_BLUEPRINTS/SENTRY_CONNECTOR_BLUEPRINT.md`

#### 3. Issue #829: Add the Stripe connector (Difficulty: Easy | Priority: P2)
- **URL:** `https://github.com/sandbox-quantum/switch/issues/829`
- **Vendor Endpoint:** `https://mcp.stripe.com`
- **Auth:** OAuth or Agent-tagged keys.
- **Notes:** Default to read-only; recommend test-mode in description.

#### 4. Issue #837: Add the Trello connector (Difficulty: Easy | Priority: P3)
- **URL:** `https://github.com/sandbox-quantum/switch/issues/837`
- **Vendor Endpoint:** Atlassian Trello remote MCP server / REST API adapter.
- **Notes:** Very few participants targeting this; low competition.

#### 5. Issue #828: Add the Cloudflare connector (Difficulty: Easy | Priority: P2)
- **URL:** `https://github.com/sandbox-quantum/switch/issues/828`
- **Vendor Endpoint:** Cloudflare Workers / DNS MCP server (`https://mcp.cloudflare.com`).

---

## 2. High-Impact Documentation Issues (`area: docs`)

Documentation PRs are among the highest-leverage contributions because they are deeply appreciated by maintainers and have clear, objective acceptance criteria.

#### 1. Issue #808: Five-minute quickstart for new contributors (Difficulty: Easy | Priority: P2)
- **URL:** `https://github.com/sandbox-quantum/switch/issues/808`
- **Goal:** Add `docs/contributing/quickstart.md` and link from `CONTRIBUTING.md`.
- **Maintainer Clarifications (from @petr-sandbox):**
  - Must use `just init-env` (not `cp .env.example .env`) to generate fresh secrets.
  - Mention Windows CRLF handling (`* text=auto eol=lf`).
  - Cover full stack startup: `just up`, `just run`, `just gateway-dev`, Switch Console connection, and first room reply.
- **Blueprint Location:** `plan/02_CORE_CONTRIBUTIONS_TRACK_03/CONNECTOR_IMPLEMENTATION_BLUEPRINTS/CONTRIBUTOR_QUICKSTART_GUIDE_PR808.md`

#### 2. Issue #807: Write the agent controller guide (Difficulty: Easy | Priority: P2)
- **URL:** `https://github.com/sandbox-quantum/switch/issues/807`
- **Goal:** Add official user guide for headless daemon under `docs/official/deploy/agent-controller.md` and link in `docs/official/TOC.md`.
- **Sources:** `console/packages/agent-controller/README.md` and `docs/design/agent-controllers-v1.md`.
- **Blueprint Location:** `plan/02_CORE_CONTRIBUTIONS_TRACK_03/CONNECTOR_IMPLEMENTATION_BLUEPRINTS/AGENT_CONTROLLER_GUIDE_PR807.md`

---

## 3. Feature & Platform Issues (`area: feature` / `area: messaging-platform`)

- **Issue #806: Prettify the agent controller CLI output (Difficulty: Easy | Priority: P2)**
  - Clean up formatting in `@switch-console/agent-controller` using chalk / cli-table3.
- **Issue #780: Add Goose as an agent provider (Difficulty: Medium | Priority: P1)**
  - Add Block's Goose CLI to `console/packages/agent-providers/`.
- **Issue #782: Add Qwen Code as an agent provider (Difficulty: Medium | Priority: P1)**
  - Add Alibaba's Qwen Code CLI provider definition.
