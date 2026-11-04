# Switch Contributor Quickstart Guide (Ready for PR #808)

*Target location in upstream repo: `docs/contributing/quickstart.md`*

---

# New Contributor Quickstart

Welcome to Switch! This guide walks you from a clean machine to running the complete Switch local development stack, connecting Switch Console, and seeing an AI agent answer you in a chat room in under 15 minutes.

---

## 1. Prerequisites

Before cloning, verify that you have the required toolchains installed for your platform:

| Tool | Required Version | Install Command |
| :--- | :--- | :--- |
| **Git** | 2.40+ | `brew install git` / `winget install Git.Git` |
| **Docker & Docker Compose** | Docker Desktop 24+ | [docker.com/get-docker](https://docs.docker.com/get-docker/) |
| **uv** (Fast Python package manager) | 0.5.0+ | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **just** (Task runner) | 1.14+ | `brew install just` / `winget install Casey.Just` |
| **Node.js & pnpm** (for Console & Gateway) | Node 22+, pnpm 9+ | `corepack enable && corepack prepare pnpm@latest --activate` |

> [!IMPORTANT]
> **Windows Note on Line Endings (CRLF vs LF):**  
> Switch requires LF line endings for connection skills and YAML configurations. If checking out on Windows, ensure git line endings are normalized:
> ```bash
> git config --global core.autocrlf false
> git clone https://github.com/sandbox-quantum/switch.git
> cd switch
> git checkout -f
> ```

---

## 2. Setting Up the Local Stack (5 Minutes)

Switch is composed of **Switch Core** (Python backend), **Supporting Services** (PostgreSQL & Mattermost running in Docker), and **Gateway / Console** (Node/Vite).

Open your terminal in the repository root:

```bash
# 1. Generate local environment file with fresh secrets
just init-env

# 2. Synchronize Python virtual environment and dependencies
uv sync --project core

# 3. Start the Docker supporting stack (PostgreSQL & Mattermost)
just up

# 4. Apply database migrations
just migrate

# 5. Run Switch Core (Backend on http://localhost:8000)
just run
```

When Switch Core starts successfully, you will see:
```text
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

In a separate terminal, launch the Gateway frontend (optional):
```bash
just gateway-install   # First time only
just gateway-dev       # Runs Vite dev server on http://localhost:5173
```

---

## 3. Connecting Switch Console & Your First Agent

You can connect either the pre-built desktop **Switch Console** or run the console development server.

### Option A: Using Pre-Built Switch Console (Recommended)
1. Download Switch Console for your platform from [Releases](https://github.com/sandbox-quantum/switch/releases).
2. Launch Console. On initial setup, choose **Connect to Custom Server** and enter `http://localhost:8000`.

### Option B: Running Console from Source
```bash
cd console
pnpm install
pnpm dev
```

### Creating Your First Room and Agent:
1. In Switch Console, open the sidebar and click **New Room**.
2. Name your room `quickstart-lounge`.
3. Select an AI Agent harness you already have installed (e.g. `claude`, `codex`, or `opencode`).
4. Type in the room:
   > *"Hello @agent! Are you alive and connected to Switch?"*
5. Your local agent will pick up the event over Server-Sent Events, execute its turn, and reply in the channel!

---

## 4. Repository Tour & Where Things Live

| Path | Purpose & Tech Stack |
| :--- | :--- |
| `core/switch_core/` | Main Python backend: Room protocol, SSE dispatcher, WebSocket hub, database models, and service connection broker. |
| `core/switch_core/connections/catalog/` | Service connector catalog (GitHub, Datadog, Supabase, Slack, Sentry, etc.). |
| `core/tests/` | Comprehensive test suite using `pytest` and `pytest-asyncio`. |
| `console/` | Switch Console desktop application (Electron, TypeScript, React, Tailwind). |
| `gateway/` | Operator management dashboard (Node.js, Vite). |
| `docs/` | Official synced documentation and architecture design docs. |
| `justfile` | Canonical repository commands for formatting, testing, and service orchestration. |

---

## 5. Mandatory Quality Gates Before Opening a PR

Always run these three commands locally before pushing code:

```bash
# 1. Code formatting & lint check (Ruff)
just check

# 2. Static typecheck (Mypy)
just typecheck

# 3. Backend test suite
just test
```

---

## 6. Submitting Your Contribution

1. Fork the repository and create your feature branch: `git checkout -b feat/my-new-feature`.
2. Commit your changes using Conventional Commits (`feat: ...`, `fix: ...`, `docs: ...`).
3. Open your Pull Request against `sandbox-quantum/switch:main`.
4. Link the relevant issue in your PR description: `Closes #123`.
5. **Sign the CLA:** The automated CLA assistant will comment on your PR. Reply with the exact sentence:
   > *I have read the CLA Document and I hereby sign the CLA*

---

> [!NOTE]
> **Switch Changes Fast:**  
> Switch is under active, high-velocity open source development. If you pull upstream changes and encounter dependency or migration mismatches, simply run:
> ```bash
> uv sync --project core
> just migrate
> ```
> Have questions or got stuck? Join the community on [Discord](https://discord.com/invite/E6a2Jnb6G)!
