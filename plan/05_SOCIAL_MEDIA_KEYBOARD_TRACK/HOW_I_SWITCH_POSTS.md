# Social Media Track: Pre-Drafted Posts (#HowISwitch)

**Prize:** Top 5 posts each win a **Logitech Mechanical Keyboard** shipped to their doorstep!  
**Hashtag:** `#HowISwitch`  
**Official Handles to Tag:**
- X / Twitter: `@sandbox_quantum`, `@wemakedevs`, `@DevToolsAcademy`, `@WisprFlow`
- LinkedIn: Tag *WeMakeDevs*, *DevTools Academy*, and *Switch*

---

## Post 1: The Build-in-Public Hook (Day 1 — Nov 4)

**Platform:** X / Twitter & LinkedIn  
**Media:** Screenshot of Switch Console showing the two linked rooms and agent roster.

```text
AI coding agents are great in your IDE... but what happens when production breaks at 2 AM? 🚨

We’re participating in the Flip the Switch Hackathon by @wemakedevs & @DevToolsAcademy, building OpsSwitch: an autonomous SRE incident squad living directly inside Slack!

Instead of one generic bot, @sandbox_quantum lets us deploy 3 specialized AI teammates across linked channels:
1️⃣ Triager: intercepts alerts & tags SEV levels
2️⃣ Investigator: runs git diffs & creates local repro scripts
3️⃣ Remediator: drafts rollback PRs & enforces human sign-off

And the coolest part? We’re dictating the entire workflow hands-free with @WisprFlow! 🎙️

Here’s #HowISwitch ⚡
[Attach Switch Console Screenshot]
```

---

## Post 2: The Technical Architecture Deep-Dive (Day 2 — Nov 5)

**Platform:** X / Twitter Thread & LinkedIn Article  
**Media:** The dual-room Mermaid diagram (`ARCHITECTURE_DIAGRAMS.md`).

```text
Why most AI agent workflows fail during production outages (and how we solved it with @sandbox_quantum): 🧵👇

1/ The Single Channel Trap ❌
When you put an autonomous agent into a public channel, it floods everyone with 500-line stack traces and git diffs.

2/ Multi-Room Linking ✅
Switch lets you create Room Links. Our #incident-intake channel stays calm with executive updates, while the heavy diagnostic lifting happens inside #incident-war-room.

3/ Zero-Leakage Credential Broker 🛡️
GitHub and Sentry tokens NEVER enter the LLM’s prompt. Switch proxies tool calls over loopback MCP.

4/ Human-in-the-Loop Gate 🛑
The remediator agent stages the rollback PR, but pauses: "Awaiting sign-off from On-Call Lead @Farhan". Only an authorized human message triggers the merge!

Building this with voice using @WisprFlow has been an absolute game changer.

#HowISwitch #WeMakeDevs #DevOps #AI
[Attach Architecture Diagram]
```

---

## Post 3: The 30-Second Live Action Demo Clip (Day 3 — Nov 6)

**Platform:** X / Twitter & LinkedIn Video Post  
**Media:** 30-second split-screen MP4 showing alert arriving in Slack → agent reproducing bug in terminal → human saying "Approved" → green healthcheck.

```text
Watch 3 autonomous AI agents diagnose a live SEV-1 outage in Slack in under 90 seconds! ⚡🤖

Checkout starts throwing 500s. Watch what happens:
- @ops-triager escalates from intake to war room
- @ops-investigator traces the offending commit and runs a local repro test
- @ops-remediator prepares a rollback PR and waits for my sign-off
- I reply "Approved. Roll it back."
- Production restored!

Built with @sandbox_quantum, @wemakedevs, and @WisprFlow.

Drop a comment if your on-call team needs this! 💬

#HowISwitch #DevOps #SRE #OpenSource
[Attach 30-sec Video Clip]
```

---

## Post 4: The Open Source Core Contribution Showcase (Day 3 — Nov 6)

**Platform:** X / Twitter  
**Media:** Screenshot of PR #827 (Supabase Connector) or PR #808 (Quickstart).

```text
Hackathons aren't just about building apps—they're about making the open-source ecosystem better! 🚀

For Track 03 of Flip the Switch, we contributed core pull requests to @sandbox_quantum:
✨ Supabase Connector with OAuth DCR and read-only URL isolation
✨ Five-minute new contributor quickstart guide
✨ Sentry observability MCP connector

Huge thanks to @petr-sandbox and @amaudruz for the lightning-fast PR reviews.

Loving the developer experience of Switch! #HowISwitch @wemakedevs
[Attach GitHub PR Screenshot]
```

---

## Post 5: The Final Submission & Celebration (Day 4 — Nov 7)

**Platform:** X / Twitter & LinkedIn  
**Media:** Devpost submission banner + demo video link.

```text
And that’s a wrap! 🏁 Just submitted OpsSwitch to the Flip the Switch Hackathon!

🏆 What we delivered:
- Complete multi-agent incident war room in Slack
- Dictated 5,000+ words with @WisprFlow voice
- Contributed to @sandbox_quantum open-source core
- Published a full DEV.to architectural deep dive

Huge thank you to @wemakedevs, @DevToolsAcademy, and @sandbox_quantum for hosting such an incredible event!

Check out our full walkthrough and demo here: [Devpost URL]

#HowISwitch #WeMakeDevs #BuildInPublic
[Attach Project Cover Card]
```
