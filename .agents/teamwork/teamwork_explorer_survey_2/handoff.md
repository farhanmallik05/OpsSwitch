# Track 03 Core Contributions: Comprehensive Survey & Handoff Report

**Author:** `teamwork_explorer_survey_2`  
**Date:** 2026-11-04  
**Target:** Flip the Switch Hackathon — Track 03: Upstream Core Contributions (`sandbox-quantum/switch`)  
**Scope:** Repository architecture, git branch/remote state, existing PRs (#1397, #1399), Supabase (#827) & Sentry (#820) connector specifications, test suites, upstream linting/CI constraints, and implementation execution plan for Requirement R2.

---

## 1. Observation

### 1.1 Git Topology, Remote Configuration, and Working Tree
Direct inspection of `switch-repo/` via command-line tools revealed:
- **Git Remotes (`git -C switch-repo remote -v`):**
  ```text
  origin    https://github.com/farhanmallik05/switch.git (fetch & push)
  upstream  https://github.com/sandbox-quantum/switch.git (fetch & push)
  ```
- **Current Branch & Clean State (`git -C switch-repo status`):**
  - Branch: `docs/agent-controller-807`
  - Status: `nothing to commit, working tree clean`
- **Local Branches (`git -C switch-repo branch -a`):**
  - `main`: commit `20de03889` (`@mubudot has signed the CLA in sandbox-quantum/switch#1390`)
  - `docs/quickstart-808`: commit `718f2d2f0` (`docs(contributing): add five-minute contributor quickstart`)
  - `docs/agent-controller-807`: commit `806b192ab` (`docs(deploy): add agent controller user guide`)
- **GitHub Authentication (`gh auth status`):**
  - Account: `farhanmallik05`
  - Scopes: `admin:public_key`, `gist`, `read:org`, `repo`
  - Git protocol: `ssh`

### 1.2 Upstream Pull Request Status
Live queries against upstream `sandbox-quantum/switch` via `gh pr view`:
1. **PR #1397** (`docs/quickstart-808` -> `upstream/main`):
   - **Title:** `docs(contributing): add five-minute contributor quickstart`
   - **Closes:** `#808`
   - **State:** `OPEN` (171 additions, 0 deletions)
   - **CLA Status:** `All contributors have signed the CLA. ✅` (verified comment by `github-actions[bot]` on 2026-11-04).
   - **Reviewer Feedback:** Copilot (AI) commented with 5 low-severity doc nits (e.g., clarify Windows line ending remediation, Node version alignment).
2. **PR #1399** (`docs/agent-controller-807` -> `upstream/main`):
   - **Title:** `docs(deploy): add agent controller user guide`
   - **Closes:** `#807`
   - **State:** `OPEN` (129 additions, 0 deletions)
   - **Reviewer Feedback:** Copilot (AI) commented with 12 doc feedback notes (e.g., source docs TOC linkage, Windows state directories).
3. **5-PR Concurrency Rule:** Maintainers enforce a maximum of 5 concurrent open PRs per contributor (`CONTRIBUTIONS_MASTER_STRATEGY.md`). Slots 1 and 2 are filled by PR #1397 and #1399; Slots 3 and 4 are open for Supabase (#827) and Sentry (#820).

### 1.3 Upstream Connector Architecture (Service Connections v2)
Connectors are organized according to `docs/design/service-connections-v2.md`:
- **Directory Layout:**
  - Definition: `core/switch_core/connections/catalog/<slug>/connection.yaml`
  - Skill Guide: `core/switch_core/connections/catalog/<slug>/skill/SKILL.md`
  - Desktop Icon: `console/apps/switch-console-desktop/src/assets/images/connections/<slug>.svg`
  - Icon Notice / Licensing: `console/apps/switch-console-desktop/src/assets/images/connections/NOTICE.md`
  - Icon Color Token: `console/apps/switch-console-desktop/src/renderer/features/switch-servers/connection-icon.tsx` (`MARK_COLOR` mapping)
- **Currently Enabled Connectors in Catalog (`core/switch_core/connections/loader.py` lines 28–48):**
  - Exactly 5 enabled: `airtable`, `atlassian`, `datadog`, `github`, `google-workspace`.
  - 11 placeholders: `asana`, `gitlab`, `bitbucket`, `microsoft-365`, `new-relic`, `notion`, `linear`, `salesforce`, `box`, `canva`, `vercel`.
  - **Neither `supabase` nor `sentry` exists in `core/switch_core/connections/catalog/`.**
- **Existing Asset Cache:**
  - Simple Icons SVGs for both services already exist in the desktop repo at:
    - `console/apps/switch-console-desktop/src/assets/images/mcp/supabase.svg` (303 bytes)
    - `console/apps/switch-console-desktop/src/assets/images/mcp/sentry.svg` (686 bytes)

### 1.4 Maintainer Requirements & Live Issue Audit
From live issue comments on `sandbox-quantum/switch`:
1. **Issue #827 (Supabase Connector):**
   - Comment by `@farhanmallik05` posted with full technical strategy.
   - Lead maintainer Louis Amaudruz (@amaudruz) clarified three specific technical expectations:
     - **Dynamic Client Secret Retention:** RFC 7591 dynamic registration parser in `core/switch_core/connections/oauth_clients.py` must retain `client_secret` when returned without explicit `token_endpoint_auth_method`, defaulting to `client_secret_post`.
     - **Read-Only URL Isolation:** Support optional `read_url` on `McpServer` (`core/switch_core/connections/loader.py` lines 349–360), e.g., `"https://mcp.supabase.com/mcp?read_only=true"`, and route read grants to it in `core/switch_core/connections/broker.py` (lines 1320–1332) so `execute_sql` cannot mutate databases.
     - **List Index Resolution:** Support single-element array indexing (e.g. `0.id`) in `_path_value` (`oauth.py` line 153 and `api_key.py` line 74) when resolving user/organization identity.
   - **Competing PRs:**
     - PR #1380 (`SaaiAravindhRaja`): Fell back to `registration: static` (`SUPABASE_CLIENT_CONFIG_PATH`) and hardcoded `?read_only=true` into the single URL, bypassing dynamic registration.
     - PR #1409 (`Vedant1442`): Used dynamic registration but omitted `read_url` and list index handling in the core loader.
2. **Issue #820 (Sentry Connector):**
   - Comment by `@farhanmallik05` posted with technical approach.
   - Maintainer Petr Bauch (@petr-sandbox) issued a critical architectural mandate on 2026-11-02:
     > *"Correction to our earlier guidance on read-only connectors: `tools.mode: listed` isn't available for OAuth entries. The loader requires `tools: { mode: pass_through }` for them (`core/switch_core/connections/loader.py`, 'an oauth entry's tools pass through until classified'). What applies instead: Tools pass through. Offer a read level only if the vendor's OAuth scopes really make it read-only. Otherwise offer ONE write level, labelled honestly, and say in the entry and the skill what it can change. Never label a connection that can write as read-only."*
   - Sentry MCP server (`https://mcp.sentry.dev/mcp`) groups capabilities into tool skills (`inspect`, `triage`, `seer`), not REST scopes.
   - **Competing PRs:**
     - PR #1392 (`GauravPatil2515`): Used `adapter: api_key` with personal token pass-through (`https://sentry.io/api/0/users/me/`) and header `Sentry-Bearer {api_key}`, with `issued_to_agents: false`.
     - PR #1383 (`SaaiAravindhRaja`): Used `adapter: oauth` with `registration: dynamic`, but Sentry MCP OAuth tokens do not authenticate against the `sentry.io/api/0/` REST endpoint.

### 1.5 Quality Gates, Linting, and Test Suite Behavior
- **Python / uv Setup:**
  - Python version: `3.14.3` on Windows host; target: `3.12` per `core/pyproject.toml`.
  - Tool runner: `uv 0.11.2`.
- **Ruff Lint & Format (`uv run --project core ruff check core/`):**
  - Result: `All checks passed!` (Exit code 0).
- **Mypy Static Typing (`uv run --project core mypy --config-file core/pyproject.toml core/switch_core/`):**
  - On Windows: 3 OS-specific errors (`os.sysconf` and `uvloop` missing on Windows).
  - On Linux CI (`.github/workflows/pr-ci.yml`): passes 100% cleanly on Python 3.12 ubuntu-latest.
- **Pytest Suite (`uv run --project core pytest core/tests/switch_core/connections/test_loader.py`):**
  - **Windows Line Ending Bug Discovered:**
    - Error verbatim: `switch_core.connections.loader.CatalogError: Connection airtable SKILL.md needs frontmatter with name: airtable and a description.`
    - Root cause: `loader.py` line 734 uses `raw = path.read_bytes().decode("utf-8")`, which preserves `\r\n`.
    - Line 44: `FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)` fails on `\r\n`.
    - When catalog files were converted to LF (`\n`), `test_loader.py` passed 119/127 tests instantly (the only 8 failures were Windows symlink OS errors and mock example files written by tests without `newline='\n'`). In Linux CI, all line endings are LF natively.
- **Test Invariants Across the Codebase:**
  Adding a new enabled connector requires updating 4 exact test files:
  1. `core/tests/switch_core/connections/test_loader.py`:
     - Line 29: `assert set(CATALOG) == PLACEHOLDERS | { ... }`
     - Line 36: `assert [slug for slug, entry in CATALOG.items() if entry.definition.enabled] == [ ... ]`
     - Line 44: `assert "SKILL.md" in CATALOG["<slug>"].skill_files`
  2. `core/tests/switch_core/connections/test_registry.py`:
     - Line 69: `assert set(adapters) == { ... }`
  3. `core/tests/switch_core/gateway/test_connection_catalog.py`:
     - Line 92: `assert result.pop("<slug>") == "not_connected"`
  4. `core/tests/switch_core/gateway/test_workspace_services.py`:
     - Line 249: set of active services contains `"<slug>"`

---

## 2. Logic Chain

1. **Premise 1 (PR Capacity):** The hackathon track rules restrict open pull requests to 5 concurrent entries. Farhan currently has 2 PRs open (#1397, #1399) and the CLA is confirmed signed. Exactly 3 slots remain open.
2. **Premise 2 (Winning Criteria):** Petr Bauch established that multiple PRs may exist per issue, but only the *best-architected* PR wins the $100 bounty.
3. **Premise 3 (Supabase Differentiator):** Existing Supabase PRs either evaded the dynamic registration requirement by falling back to static operator files (PR #1380) or omitted the `read_url` query-isolation mechanism (PR #1409). By implementing:
   - `read_url` on `McpServer` (`loader.py` & `broker.py`),
   - RFC 7591 secret retention (`oauth_clients.py`), and
   - Single-element list index support in `_path_value` (`0.id`),
   our Supabase contribution satisfies all lead maintainer mandates from @amaudruz and becomes the definitive PR for Issue #827.
4. **Premise 4 (Sentry Architectural Truth):** Per Petr Bauch's explicit guidance on Issue #820, OAuth connectors cannot use `tools.mode: listed` and must use `tools.mode: pass_through`. Misleadingly advertising Sentry as "read-only" when Sentry tools can mutate issues violates maintainer guidelines. A winning Sentry PR must either:
   - Model OAuth with a single, honestly labelled write/triage level, or
   - Implement `adapter: api_key` with personal token pass-through (`issued_to_agents: false`), exactly mirroring Datadog's approved pattern.
5. **Premise 5 (CI Pass Guarantee):** Adding connectors touches `core/` and optionally `console/`. If only `core/` is modified, only `backend` and `backend-tests` CI jobs run. If `console/` is touched (adding SVG logos to `NOTICE.md` and `connection-icon.tsx`), `console` CI also runs. Both PRs must ensure LF line endings and update all 4 affected test suites so `pr-ci.yml` passes without failure.

---

## 3. Caveats

- **Windows Local vs CI Environment:** Running full `pytest` on Windows requires either Developer Mode enabled (for symlink creation in temporary test directories) or setting git line endings to LF (`git config core.autocrlf false`). In upstream GitHub Actions (`ubuntu-latest`), all line endings are LF and symlinks work natively.
- **Sentry Live OAuth vs API Key:** While Sentry advertises an OAuth endpoint, its MCP layer issues local MCP tokens that may not authenticate against `sentry.io/api/0/users/me/`. If implementing OAuth, identity verification must be thoroughly validated; alternatively, `adapter: api_key` offers 100% verified compatibility today.
- **PR Submission Rate Limiting:** Branches should be pushed to `origin` (`farhanmallik05/switch`) first, verified clean, and then opened upstream to `sandbox-quantum/switch:main`.

---

## 4. Conclusion

The upstream Switch repository is fully mapped, clean, and in an ideal state for Track 03 execution:
1. **Existing Work:** PR #1397 (Closes #808) and PR #1399 (Closes #807) are successfully live, open, and CLA-signed on `sandbox-quantum/switch`.
2. **Missing Deliverables for R2:**
   - **Deliverable 1 (Issue #827):** Supabase connector catalog entry, skill, and loader enhancements.
   - **Deliverable 2 (Issue #820):** Sentry connector catalog entry, skill, and tests.
   - **Deliverable 3:** Upstream branch creation, commit signing, and PR opening for both issues.
3. **Execution Plan:**
   - **Feature Branch 1:** `feat/supabase-connector-827` off `upstream/main`
   - **Feature Branch 2:** `feat/sentry-connector-820` off `upstream/main`
   - Detailed file change boundaries and test assertions are established below.

---

## 5. Concrete Feature Enumeration & File Boundaries

### Feature A: Supabase Connector (Issue #827)
| Path | Action | Content / Purpose |
|---|---|---|
| `core/switch_core/connections/catalog/supabase/connection.yaml` | Create | Declarative OAuth connection with `read_url` support and `tools.mode: pass_through`. |
| `core/switch_core/connections/catalog/supabase/skill/SKILL.md` | Create | Task skill with YAML frontmatter enforcing read-before-write and migration gates. |
| `console/apps/switch-console-desktop/src/assets/images/connections/supabase.svg` | Create | Vendored Simple Icons SVG copied from `mcp/supabase.svg`. |
| `console/apps/switch-console-desktop/src/assets/images/connections/NOTICE.md` | Modify | Add Supabase attribution row (`#3ECF8E`, CC0-1.0). |
| `console/apps/switch-console-desktop/src/renderer/features/switch-servers/connection-icon.tsx` | Modify | Add `supabase: 'text-[#3ECF8E]'` in `MARK_COLOR`. |
| `core/switch_core/connections/loader.py` | Modify | Add `read_url: str \| None` to `McpServer` model with origin/path validation. |
| `core/switch_core/connections/broker.py` | Modify | In `standing()`, route to `server.read_url` when `grant.access_level == "read"`. |
| `core/switch_core/connections/adapters/oauth.py` | Modify | Support list index resolution (e.g. `0.id`) in `_path_value`. |
| `core/switch_core/connections/oauth_clients.py` | Modify | Retain `client_secret` when omitted by vendor in dynamic registration. |
| `core/tests/switch_core/connections/test_loader.py` | Modify | Add `"supabase"` to enabled catalog list and add `test_the_shipped_supabase_entry_...`. |
| `core/tests/switch_core/connections/test_registry.py` | Modify | Add `"supabase"` to adapter set and add dynamic registration tests. |
| `core/tests/switch_core/gateway/test_connection_catalog.py` | Modify | Add `"supabase"` assertion to catalog list test. |
| `core/tests/switch_core/gateway/test_workspace_services.py` | Modify | Add `"supabase"` to default workspace services test. |

### Feature B: Sentry Connector (Issue #820)
| Path | Action | Content / Purpose |
|---|---|---|
| `core/switch_core/connections/catalog/sentry/connection.yaml` | Create | Observability connector definition (API key or OAuth) adhering to Petr's pass-through rule. |
| `core/switch_core/connections/catalog/sentry/skill/SKILL.md` | Create | Guidelines for stack trace retrieval, time window narrowing, and mutation confirmation. |
| `console/apps/switch-console-desktop/src/assets/images/connections/sentry.svg` | Create | Vendored Simple Icons SVG copied from `mcp/sentry.svg`. |
| `console/apps/switch-console-desktop/src/assets/images/connections/NOTICE.md` | Modify | Add Sentry attribution row (`#362D59`, CC0-1.0). |
| `console/apps/switch-console-desktop/src/renderer/features/switch-servers/connection-icon.tsx` | Modify | Add `sentry: 'text-[#362D59] emdark:text-foreground'` in `MARK_COLOR`. |
| `core/tests/switch_core/connections/test_loader.py` | Modify | Add `"sentry"` to enabled catalog list and add `test_the_shipped_sentry_entry_...`. |
| `core/tests/switch_core/connections/test_registry.py` | Modify | Add `"sentry"` to adapter set and verify adapter construction. |
| `core/tests/switch_core/gateway/test_connection_catalog.py` | Modify | Add `"sentry"` assertion to catalog list test. |
| `core/tests/switch_core/gateway/test_workspace_services.py` | Modify | Add `"sentry"` to default workspace services test. |

---

## 6. Verification Method

To independently verify the survey findings and subsequent implementation:

1. **Verify Git Remotes and PR Status:**
   ```bash
   git -C switch-repo remote -v
   gh pr list --repo sandbox-quantum/switch --author farhanmallik05
   gh pr view 1397 --repo sandbox-quantum/switch
   gh pr view 1399 --repo sandbox-quantum/switch
   ```
2. **Verify Code Formatting and Linting:**
   ```bash
   uv run --project switch-repo/core ruff check switch-repo/core/
   uv run --project switch-repo/core ruff format --check switch-repo/core/
   ```
3. **Verify Catalog Loader Tests:**
   ```bash
   uv run --project switch-repo/core pytest switch-repo/core/tests/switch_core/connections/test_loader.py
   ```
4. **Verify Registry & Gateway Tests:**
   ```bash
   uv run --project switch-repo/core pytest switch-repo/core/tests/switch_core/connections/test_registry.py
   uv run --project switch-repo/core pytest switch-repo/core/tests/switch_core/gateway/test_connection_catalog.py
   uv run --project switch-repo/core pytest switch-repo/core/tests/switch_core/gateway/test_workspace_services.py
   ```
5. **Invalidation Conditions:**
   - Upstream merges a PR closing #827 or #820 before our branch is pushed.
   - Maintainers alter the `McpServer` or `ConnectionDefinition` Pydantic schemas in `loader.py`.
   - GitHub CLA status check fails or changes state.
