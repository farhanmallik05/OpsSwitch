# Hackathon Master Schedule: Hour-by-Hour Execution Plan

**Event Window:** November 4–7, 2026 (Starts Nov 4, 00:00 IST | Ends Nov 7, 23:59 IST)  
**Timezone:** Indian Standard Time (IST / UTC+5:30)

---

## Phase 0: Hackathon Eve (Nov 3, 18:00 – 23:59 IST) — "Pre-Emptive Assignment & Setup"

| Time | Operational Task | Deliverable |
| :--- | :--- | :--- |
| **18:00 - 19:30** | Comment on target GitHub issues on `sandbox-quantum/switch` tagging `@petr-sandbox` using pre-drafted templates. | Comment on Issues #827, #820, #808, #807, #829 |
| **19:30 - 21:00** | Run environment verification: verify Docker daemon, Node 22+, Python `uv`, and `just`. | Environment checks pass |
| **21:00 - 22:30** | Download and install **Switch Console** and **Wispr Flow Desktop App** (claim 1 month free Pro). | Switch Console & Wispr running |
| **22:30 - 23:59** | Fork `sandbox-quantum/switch` and set up local development branches. | Fork ready with clean `upstream` |

---

## Phase 1: Day 1 (Nov 4) — "Core Contributions & Template Launch"

| Time | Operational Task | Deliverable |
| :--- | :--- | :--- |
| **00:00 - 02:00** | **HACKATHON KICKOFF**: Implement the PRs for assigned issues: PR #808 (Quickstart Guide) and PR #807 (Controller Guide). | PR #808 and PR #807 opened; sign CLA |
| **09:00 - 12:00** | Implement PR #827 (Supabase Connector with DCR & `read_url`) and PR #820 (Sentry Connector). | Run `just test`, open PRs |
| **12:00 - 14:00** | Break & Lunch. Monitor GitHub PR feedback from maintainers. | Resolve any CI or reviewer comments |
| **14:00 - 18:00** | Launch Switch Core locally (`just up`, `just run`). Import `OpsSwitch` template in Switch Console. | Rooms created in Slack/Discord |
| **18:00 - 20:00** | Dictate system instructions and prompts using Wispr Flow (accumulate 2,000+ words). | System instructions locked |
| **20:00 - 21:30** | Publish **Social Post 1** on X and LinkedIn with `#HowISwitch` tagging `@sandbox_quantum`. | First social presence established |

---

## Phase 2: Day 2 (Nov 5) — "Incident Simulation & End-to-End Testing"

| Time | Operational Task | Deliverable |
| :--- | :--- | :--- |
| **09:00 - 12:00** | Build mock incident injector: create a local mock microservice that triggers an unhandled NPE on `/checkout`. | `scripts/simulate_incident.py` working |
| **12:00 - 15:00** | Wire up Switch loopback connectors for GitHub and Sentry. Test commit listing and git revert tools. | Tool calls execute cleanly |
| **15:00 - 18:00** | Test the full multi-agent handoff: Intake alert → Triager SEV-1 classification → War Room escalation → Investigator repro script → Remediator PR draft → Human sign-off. | Zero-failure automated dry run |
| **18:00 - 20:00** | Dictate README and technical specifications by voice with Wispr Flow (surpass 4,000 words). | Word count milestone reached |
| **20:00 - 21:30** | Publish **Social Post 2** (Architecture thread with Mermaid diagram) on X and LinkedIn. | High engagement from community |

---

## Phase 3: Day 3 (Nov 6) — "Blog Publishing & Video Demo Production"

| Time | Operational Task | Deliverable |
| :--- | :--- | :--- |
| **09:00 - 13:00** | **RECORD DEMO VIDEO**: Follow `VIDEO_DEMO_SCRIPT_AND_STORYBOARD.md` (2m 45s target). Record split-screen Slack + terminal. | Raw recording complete |
| **13:00 - 15:00** | Video editing: add captions, zoom effects on agent responses, trim dead pauses, export 1080p MP4. Upload unlisted to YouTube / Loom. | Final demo video URL live |
| **15:00 - 18:00** | **PUBLISH BLOG POST**: Publish `BLOG_POST_COMPLETE_DRAFT.md` on DEV.to with diagrams and tags. | Blog post live on DEV.to (AirPods 5 target) |
| **18:00 - 19:30** | Clip 30-second teaser clip from demo video and publish **Social Post 3** on X/LinkedIn with `#HowISwitch`. | Teaser video viral push |
| **19:30 - 22:00** | Share blog link in WeMakeDevs Discord and Reddit (`r/devops`, `r/programming`). | Drive comments & reactions |

---

## Phase 4: Day 4 (Nov 7) — "Final Audit, Scorecard & Grand Submission"

| Time | Operational Task | Deliverable |
| :--- | :--- | :--- |
| **09:00 - 12:00** | Final polish on repository: verify zero secrets in git history, check all links in `README.md`. | Clean, polished GitHub repo |
| **12:00 - 14:00** | Open Wispr Flow Desktop → Insights tab. Export high-resolution scorecard screenshot. | `wispr-flow-scorecard.png` saved |
| **14:00 - 17:00** | Populate hackathon submission portal: copy text from `SUBMISSION_METADATA_AND_DEVPOST_TEXT.md`. | Form fully populated |
| **17:00 - 19:00** | Run `FINAL_SUBMISSION_AUDIT_CHECKLIST.md` line by line. Verify video plays, repo is public. | 100% audit compliance |
| **19:00 - 20:00** | **CLICK SUBMIT**: Submit project on WeMakeDevs hackathon portal (well ahead of midnight deadline). | Official confirmation receipt |
| **20:00 - 21:30** | Publish **Social Post 5** celebrating submission with `#HowISwitch`. | Final wrap-up and showcase |
| **23:59 IST** | **HACKATHON PORTAL HARD DEADLINE** | Submissions locked |
