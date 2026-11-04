# OpsSwitch: Video Demo Script & Storyboard

**Target Duration:** 2 minutes 45 seconds (Optimal for hackathon judging)  
**Tone:** Confident, crisp, senior engineering walkthrough  
**Visual Style:** High-definition split-screen (Slack/Discord on left, Switch Console & terminal on right)

---

## Storyboard Timeline Overview

| Timestamp | Visual Screen | Voiceover Narrative |
| :--- | :--- | :--- |
| **0:00 - 0:25** | High-level title slide + Real-world problem | The High Cost of Downtime & Context-Switching |
| **0:25 - 0:50** | Switch Console Setup & Template Import | Introducing OpsSwitch & Multi-Room Architecture |
| **0:50 - 1:20** | Slack/Discord `#incident-intake` | Live Alert Ingestion & Severity Classification |
| **1:20 - 1:55** | `#incident-war-room` (Split Screen) | Automated Git Commit Diffing & Local Repro |
| **1:55 - 2:20** | War Room Interactive Sign-Off | The Human-in-the-Loop Gate & Automated Rollback |
| **2:20 - 2:45** | Back to `#incident-intake` + Outro | Executive Post-Mortem & The Power of Switch |

---

## Detailed Minute-by-Minute Script

### Act 1: The Hook & The Problem (0:00 - 0:25)
* **Visual:** Fullscreen camera or high-contrast title card: *OpsSwitch: Autonomous Incident Commander with Human-in-the-Loop Governance*. Then cut to a quick split screen showing 7 chaotic browser tabs: Datadog, Sentry, GitHub, PagerDuty, Slack, Docker logs.
* **Speaker:**
  > *"When production breaks at 2 AM, every minute of downtime costs thousands of dollars. But what really slows teams down isn't writing the fix—it's context-switching. Engineers waste 20 minutes jumping between monitoring alerts, git commit histories, reproducing bugs locally, and arguing in noisy Slack channels.*  
  > *Meet **OpsSwitch**—an autonomous SRE incident response squad built on **Switch**, turning your Slack or Discord channels into an intelligent, multi-agent war room."*

### Act 2: Architecture & Setup in Switch Console (0:25 - 0:50)
* **Visual:** Screen capture of **Switch Console**. Show the imported `OpsSwitch` template. Highlight the two rooms (`#incident-intake` and `#incident-war-room`) and the three specialized AI teammates (`ops-triager`, `ops-investigator`, `ops-remediator`).
* **Speaker:**
  > *"OpsSwitch isn't a single naive chatbot. It uses Switch's Room Linking to split incident management cleanly: a public intake room for alerts and executive status, and a private war room for deep technical investigation.  
  > Switch connects our agents—running on Claude Code and Codex—directly into our Slack workspace via the Switch Agent Protocol."*

### Act 3: Live Incident Ingestion & Triage (0:50 - 1:20)
* **Visual:** Switch to Slack channel `#sre-incident-intake`. The user types a simulated alert:
  `@sre-triager checkout service is throwing HTTP 500 errors since the 09:40 UTC deploy. Cart purchases failing.`
* **Visual Effect:** Highlight the immediate response from `@sre-triager`.
* **Speaker:**
  > *"Watch what happens when an alert arrives. The triager intercepts it, parses the blast radius, and classifies it as a SEV-1 outage because it affects payments. Notice how it acknowledges the report in intake, but doesn't dump messy logs here. Instead, it escalates directly across the room link into `#sre-incident-war-room`."*

### Act 4: Diagnostic Investigation & Local Repro (1:20 - 1:55)
* **Visual:** Seamlessly transition to `#sre-incident-war-room`. Show `@sre-triager` posting the escalation notice to `@sre-investigator`.
* **Visual Effect:** Show the terminal window next to Slack where the agent's background workspace runs the reproduction script.
* **Speaker:**
  > *"In the war room, `ops-investigator` immediately gets to work. Using Switch's GitHub connector, it pulls recent commits from the deploy window. It isolates commit `f3c8a91` which modified the coupon parser.  
  > But it doesn't stop at guessing: in its local directory, it synthesizes a 4-line reproduction script, runs it, and reproduces the exact NullPointerException in seconds. It hands the verified evidence straight to `ops-remediator`."*

### Act 5: Remediation & Human-in-the-Loop Gate (1:55 - 2:20)
* **Visual:** In the war room, `@sre-remediator` posts an interactive Change Request Card:
  - Action: Revert commit `f3c8a91` (PR #412 created).
  - Risk Level: Low.
  - Text: *"Awaiting sign-off from On-Call Lead @Farhan. Reply 'Approved. Roll it back.' to execute."*
* **Visual:** User (@Farhan) replies: *"Approved. Roll it back."*
* **Speaker:**
  > *"Here is the most critical feature: strict human governance. OpsSwitch will never make production changes autonomously. `ops-remediator` prepares the rollback PR and pauses for human sign-off.  
  > As the On-Call Lead, I reply 'Approved. Roll it back.' The agent verifies the authorization, merges the PR, triggers deployment, and confirms health checks return 200 OK."*

### Act 6: Post-Mortem & Wrap-Up (2:20 - 2:45)
* **Visual:** Cut back to `#sre-incident-intake`. Show `@sre-triager` posting the completed post-mortem with total resolution time (8 minutes vs usual 45 minutes) and PR link. Show Wispr Flow scorecard and GitHub repo.
* **Speaker:**
  > *"Within 8 minutes, the outage is resolved, and an automated root-cause post-mortem is published to the company. OpsSwitch was built 100% by voice using Wispr Flow, and powered by Switch's open-source multi-agent infrastructure.  
  > Check out our repo to try it today. Thank you!"*

---

## Production & Recording Tips

1. **Resolution:** Record at 1080p (1920x1080) at 60fps.
2. **Font Size:** Bump Slack/Discord font size to `125%` (Ctrl + `+`) so text is crystal clear on mobile screens.
3. **Audio:** Use a clean USB microphone or headset; apply gentle noise suppression.
4. **Captions:** Use auto-captioning (e.g. CapCut, Descript, or Premiere Pro) with bold keywords to keep viewers hooked even without headphones.
5. **Hosting:** Upload as unlisted on YouTube and provide direct MP4 link on Devpost.
