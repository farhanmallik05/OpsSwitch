# Final Pre-Submission Audit Checklist

*Execute this audit 3 hours prior to the hard deadline on November 7, 2026.*

---

## 1. Judging Pillar 1: Centrality of Switch (25%)
- [ ] Does the project fundamentally rely on Switch's **linked rooms** (`#incident-intake` ↔ `#incident-war-room`)?
- [ ] Is context cleanly partitioned so public channels don't suffer from log pollution?
- [ ] Does the architecture demonstrate multi-agent collaboration with distinct addressing modes (`anyone` vs `owner-agents`)?
- [ ] Are third-party tools (GitHub, Sentry) brokered through Switch's loopback MCP session host with zero token leakage into LLM prompts?

---

## 2. Judging Pillar 2: Technical Execution & Reproducibility (25%)
- [ ] Can a judge clone the repo and run the project out-of-the-box?
- [ ] Is `TEMPLATE_YAML_SPECIFICATION.yaml` valid Switch schema v1 syntax?
- [ ] Are all mock scripts (`scripts/simulate_incident.py`) included and documented in the README?
- [ ] Does `just test` pass without failures or unhandled exceptions?
- [ ] Are there **zero hardcoded credentials**, private API keys, or sensitive corporate URLs anywhere in the git history?

---

## 3. Judging Pillar 3: Creativity & Real-World Impact (25%)
- [ ] Does the project solve an actual, high-stakes enterprise problem (reducing costly downtime during production outages)?
- [ ] Does it introduce strict **Human-in-the-Loop governance** before executing any production rollback or hotfix?
- [ ] Does it demonstrate deterministic local reproduction before staging fixes?

---

## 4. Judging Pillar 4: Presentation & Video Demo (25%)
- [ ] Is the demo video under 3 minutes (recommended 2m 45s)?
- [ ] Is the video hosted publicly or unlisted on YouTube / Loom (audio and video crisp, 1080p)?
- [ ] Does the video demonstrate the split-screen Slack + terminal interaction clearly?
- [ ] Is the repository `README.md` visually polished with badges, Mermaid architecture diagrams, and a 5-minute quickstart?

---

## 5. Side Tracks & Bonus Checklist

### Track 03: Core Open Source Contributions ($100 × 20)
- [ ] Are all submitted pull requests linked to open issues labeled `hackathon`?
- [ ] Did you comment on each issue and tag `@petr-sandbox`?
- [ ] Does each PR description contain `Closes #<issue_number>`?
- [ ] Did you sign the CLA by replying to the bot comment:
  > *"I have read the CLA Document and I hereby sign the CLA"*
- [ ] Do you have at most 5 PRs open at once?

### Side Track: Code with Wispr ($500 Cash)
- [ ] Did you enter the **Code with Wispr** track in the submission form?
- [ ] Is the authentic Wispr Flow **Insights scorecard screenshot** attached?
- [ ] Does the screenshot demonstrate active word counts and usage across Nov 4–7?

### Side Track: Best Blog (Apple AirPods 5)
- [ ] Is the article published on DEV.to with proper tags (`#switch`, `#ai`, `#devops`, `#opensource`)?
- [ ] Does it link to the GitHub repository and explain the Switch Agent Protocol clearly?
- [ ] Is the blog post URL pasted into the hackathon submission form?

### Social Track: #HowISwitch (Logitech Mechanical Keyboards)
- [ ] Did you post on X/Twitter and LinkedIn using the `#HowISwitch` hashtag?
- [ ] Did you tag `@sandbox_quantum`, `@wemakedevs`, and `@DevToolsAcademy`?
- [ ] Did you attach a screen capture or demo video clip to maximize engagement?
