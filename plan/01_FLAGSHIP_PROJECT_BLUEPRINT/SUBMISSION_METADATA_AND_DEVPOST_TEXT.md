# OpsSwitch: Official Hackathon Submission Text

*Copy-paste ready for the WeMakeDevs / Flip the Switch Hackathon submission portal.*

---

## Basic Submission Information

- **Project Title:** OpsSwitch — Autonomous Incident Commander & War Room
- **Elevator Pitch (Tagline):** Multi-agent SRE incident response squad in Slack & Discord powered by Switch, featuring automated git commit root-cause diagnosis, local reproduction testing, and human-in-the-loop rollbacks.
- **Primary Track:** Track 01 — Best Business Workflow ($2,000)
- **Side Tracks Entered:** 
  - Code with Wispr ($500)
  - Best Blog (AirPods 5)
  - #HowISwitch (Logitech Mechanical Keyboard)
- **Team Name:** Algo Alchemist
- **Team Code:** `K8H5DE`
- **Team Members:** Farhan Mallik (`@farhanmallik`, Leader)
- **GitHub Repository:** `[Insert Repo URL]`
- **Video Demo URL:** `[Insert Loom / YouTube Link]`
- **Wispr Flow Scorecard Attachment:** `[Attach screenshot from plan/04_WISPR_FLOW_VOICE_TRACK/]`

---

## Detailed Submission Narrative

### 💡 Inspiration
Every software engineer knows the dread of a critical production outage at 2 AM. PagerDuty sounds, error charts spike in Datadog, customer complaints flood Zendesk, and engineering teams frantically scramble across a dozen browser tabs.
The biggest bottleneck during incidents isn't actually writing the fix—it is **context-switching and diagnostic friction**. Engineers waste precious minutes trying to figure out which deploy caused the bug, trying to reproduce it locally, and debating who has permission to trigger a rollback.

When we discovered **Switch**, we realized that AI agents shouldn't just be solitary copilots in an IDE—they should be active teammates participating directly in the incident war room. We built **OpsSwitch** to give engineering teams an autonomous SRE squad that triages alerts, pinpoints root-cause commits, and prepares safe rollbacks, while keeping human engineers firmly in command.

---

### ⚙️ What It Does
OpsSwitch splits incident response across two connected rooms in Slack or Discord:
1. **`#incident-intake` (Public Channel):** 
   - Receives alerts from engineers or monitoring webhooks.
   - The `@ops-triager` agent analyzes symptoms, classifies severity from SEV-1 to SEV-4, filters noise, and escalates serious incidents across a bi-directional Switch room link.
2. **`#incident-war-room` (Restricted Channel):**
   - `@ops-investigator` immediately audits recent deployment commits, runs a git diff against the reported stack traces, and writes a minimal reproduction script inside its local sandbox to confirm the bug deterministically.
   - `@ops-remediator` generates a rollback pull request or patch branch via the Switch GitHub connector, formulates a risk card, and waits for explicit sign-off from the human On-Call Lead.
   - Once a human replies *"Approved. Roll it back."*, the agent merges the PR, monitors health metrics back to 200 OK, and reports an executive post-mortem back to `#incident-intake`.

---

### 🔨 How We Built It
- **Switch Core & Switch Console:** Orchestrated our multi-agent topology using Switch's template specification syntax (`version: 1`), defining granular permissions, working directories, and room links.
- **Switch Agent Protocol:** Powered the real-time agent loop using Server-Sent Events (SSE) for incoming stream events and HTTP for outgoing message turns.
- **Service Connectors:** Leveraged Switch's credential broker for GitHub and Datadog/Sentry integrations, ensuring third-party API tokens never leak into LLM prompts.
- **Wispr Flow Pro:** Dictated all prompts, room instructions, and documentation completely by voice, accelerating development and enabling hands-free engineering.
- **Chat Bridges:** Tested and verified across both Slack and Discord bridges.

---

### 🧗 Challenges We Ran Into
1. **Preventing Information Overload:** Initially, putting all agents into a single Slack channel caused alert fatigue; stack traces and terminal diffs drowned out communication. Solving this with Switch's **linked rooms** (`#incident-intake` -> `#incident-war-room`) kept discussions clean and contextual.
2. **Deterministic Governance:** We had to guarantee that remediation agents would never execute destructive git reverts without human sign-off. We designed strict prompt guards and regex validation on the human lead's identity before allowing write operations.
3. **Zero Token Leakage:** Ensuring that OAuth tokens from GitHub and Sentry stayed inside Switch's session host rather than being reflected in LLM memory required strict adherence to Switch's service connections v2 architecture.

---

### 🏆 Accomplishments That We're Proud Of
- Reduced simulated Mean Time to Diagnose (MTTD) from **35 minutes down to under 90 seconds**.
- Designed a completely reproducible, zero-configuration Switch template that any team can import in 30 seconds.
- Built a truly multi-agent collaborative workflow where three specialized AI teammates pass context seamlessly across linked channels.
- Dictated 100% of instructions and docs using Wispr Flow.

---

### 📚 What We Learned
- How to design effective multi-agent communication patterns with distinct addressing modes (`anyone` vs `owner-agents`).
- The internal workings of the Switch Agent Protocol (SSE transport, loopback MCP execution).
- How much faster developer workflows become when voice dictation (Wispr Flow) is paired with autonomous agent execution.

---

### 🔮 What's Next for OpsSwitch
- **Automated Canary Deployments:** Allowing `@ops-remediator` to deploy to a 5% canary tier and monitor Datadog error rates before full rollout.
- **Jira & PagerDuty Bi-directional Sync:** Updating incident timelines and automatically resolving on-call alerts.
- **Enterprise RBAC:** Integrating Okta / WorkOS OIDC to enforce team-specific sign-off authorization tiers.

---

### 🏷️ Built With
- `switch`
- `switch-console`
- `claude-code`
- `codex`
- `wispr-flow`
- `python`
- `docker`
- `slack-api`
- `discord-api`
- `github-mcp`
- `sentry`
- `fastapi`
