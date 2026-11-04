# Blog Track: Visual Assets & Formatting Guide

Rich visuals drastically increase reader retention and judge scoring. Follow these guidelines to prepare graphics for the DEV.to post.

---

## 1. Banner & Cover Graphic (1000 × 420 px)

- **Dimensions:** 1000px width by 420px height (DEV.to recommended aspect ratio).
- **Style:** Dark tech theme (`#0F172A` slate dark background) with vibrant accent glows in Switch Coral (`#FF895E`) and Wispr Purple (`#8A2BE2`).
- **Typography:** Bold sans-serif title: *"Putting AI Agents on Call"*.
- **Sub-badge:** *"Flip the Switch Hackathon 2026 | WeMakeDevs × Switch"*.
- **Logos Included:** Switch logo mark, Slack icon, and Wispr Flow mark.

---

## 2. In-Article Architecture Diagrams

Mermaid diagrams render natively on DEV.to and GitHub:
- **Diagram 1: Dual-Room Linking Topology** (Already included in `BLOG_POST_COMPLETE_DRAFT.md`).
- **Diagram 2: End-to-End Sequence Diagram** (Rendered directly with `mermaid` syntax).

---

## 3. High-Fidelity Screenshots & GIFs

Prepare three animated screen captures (using CleanShot X, ScreenToGif, or Loom):

1. **`gif-01-alert-intake.gif`**:
   - Showing the simulated incident alert arriving in Slack `#sre-incident-intake` and `@sre-triager` immediately classifying it and triggering the war room escalation.
2. **`gif-02-repro-execution.gif`**:
   - Split screen showing `@sre-investigator` generating the minimal `repro.py` script and the terminal window executing it with instant traceback output.
3. **`gif-03-human-signoff.gif`**:
   - Showing `@sre-remediator` presenting the interactive Authorization Card, the human lead replying *"Approved. Roll it back."*, and the health check returning 200 OK.
