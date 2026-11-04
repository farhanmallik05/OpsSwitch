# Track 03: Core Open Source Contributions — Master Strategy

**Prize Allocation:** $100 × 20 Pull Requests ($2,000 Cash Pool)  
**Rule Limit:** Maximum 5 open pull requests per contributor at any one time  
**Eligibility Window:** Can start immediately (pre-hackathon window is open!) until Nov 7, 2026, 23:59 IST  

---

## 1. The Strategy: Securing up to $500 in Core Bounties

Track 03 offers a cash bounty of **$100 per winning pull request** for the top 20 contributions to `sandbox-quantum/switch`.
Because the maintainers enforce a strict limit of **5 concurrent open PRs**, our optimal strategy is to run a **5-PR Pipeline**:

```
      [Issue Selection] ──► [Petr Assignment Comment] ──► [Implement via Blueprint] ──► [PR & CLA]
             │
             ├── PR 1: Issue #827 — Supabase Connector (OAuth DCR + read_url + identity fix)
             ├── PR 2: Issue #820 — Sentry Connector (Remote MCP server + skill + tests)
             ├── PR 3: Issue #808 — Five-Minute Contributor Quickstart Guide
             ├── PR 4: Issue #807 — Agent Controller Headless User Guide
             └── PR 5: Issue #829 / #837 — Stripe or Trello Connector
```

If all 5 PRs are accepted, this nets **$500 in direct cash** alongside the main track submission!

---

## 2. Core Track Rules & Hard Constraints

1. **Labels:** Only issues with the label `hackathon` qualify. PRs for unlabelled issues will NOT be judged.
2. **Assignment Gate:** You must comment on the issue, tag `@petr-sandbox`, and state in 1–2 lines your concrete solution plan. Maintainer Petr notes that while multiple people may attempt an issue, **only the best-implemented PR per issue will be awarded the $100**.
3. **No Low-Effort / AI-Spam PRs:** Typo fixes, simple formatting, or unreviewed hallucinated AI dumps will be disqualified immediately and could get your team removed from the event.
4. **Link the Issue:** Every PR must include `Closes #<issue_number>` in its description body.
5. **Sign the Contributor License Agreement (CLA):**
   - On opening your first PR, the automated bot comments with a link.
   - Reply to the PR with the exact phrase:
     > *"I have read the CLA Document and I hereby sign the CLA"*
6. **Local Quality Verification:** Every PR must pass all three repository checks before being opened:
   ```bash
   just check       # Ruff linter and formatting
   just typecheck   # Mypy static type verification
   just test        # Pytest test suite in core/tests/
   ```

---

## 3. The 5-PR Priority Matrix

| Issue # | Name | Difficulty | Area | Why We Win It |
| :--- | :--- | :--- | :--- | :--- |
| **#827** | Add the Supabase connector | Easy/Medium | `area: connector` | Lead maintainer Louis Amaudruz specifically detailed 3 architectural requirements in the comments (`read_url`, DCR secret retention, and list index identity). Our blueprint provides all three! |
| **#820** | Add the Sentry connector | Easy | `area: connector` | Clean remote MCP OAuth/API key pattern, fits the standard `service-connections-v2` design, high business value for error debugging. |
| **#808** | Five-minute quickstart for contributors | Easy | `area: docs` | Every first-time contributor needs this. We document `just init-env`, the Windows CRLF git checkout quirk, and Console-to-Core linking. |
| **#807** | Write the agent controller guide | Easy | `area: docs` | High-value official documentation for the headless daemon (`docs/official/deploy/agent-controller.md`). Minimal competition. |
| **#829** | Add the Stripe connector | Easy | `area: connector` | Official remote MCP server at `https://mcp.stripe.com` with OAuth; straightforward read-only customer and payment inspection. |

---

## 4. PR Quality Checklist

Before clicking "Create Pull Request":
- [ ] Working branch named descriptively: `feat/supabase-connector-827`, `docs/contributor-quickstart-808`, etc.
- [ ] No extraneous file edits or formatting changes in unrelated packages.
- [ ] All new files have official vendor SVGs and attribution in `NOTICE.md`.
- [ ] Tests added to `core/tests/switch_core/connections/test_loader.py`.
- [ ] PR description includes a concise summary, test commands, and demo snippet.
- [ ] `Closes #<number>` added to automatically link the issue.
- [ ] CLA sentence ready to paste once the CLA bot comments.
