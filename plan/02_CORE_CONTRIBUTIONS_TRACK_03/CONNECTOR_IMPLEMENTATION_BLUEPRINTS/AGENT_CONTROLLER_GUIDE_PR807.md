# Agent Controller Headless Deployment Guide (Ready for PR #807)

*Target location in upstream repo: `docs/official/deploy/agent-controller.md`*

---

# Headless Agent Controller Deployment

The **Switch Agent Controller** (`switch-agent-controller`) is a lightweight, headless daemon designed to run on your private servers, VMs, or workstations. It connects to your central Switch instance, enrolls the host machine, and runs managed AI agents as persistent background workers—without needing a graphical desktop or active browser session.

---

## 1. System Requirements

- **Supported Operating Systems:** Linux (Ubuntu/Debian, RHEL/Rocky, Arch), macOS (Sonoma/Sequoia), or Windows 10/11.
- **Node.js Runtime:** Node.js 22.13 or later (uses the native `node:sqlite` module; no external database required).
- **Agent Provider CLIs:** At least one supported AI coding CLI installed on the system `PATH` and authenticated:
  - `claude` (Anthropic Claude Code)
  - `codex` (OpenAI Codex CLI)
  - `opencode` (OpenCode CLI)
  - `cursor-agent` / `antigravity-acp`
- **Central Switch Instance:** A running Switch Core server with the `agent_management` feature flag enabled (`FEATURE_FLAGS_ENABLED=agent_management`).

---

## 2. One-Line Installation & Enrollment

Every Switch Gateway features a **Machines** page that generates a secure, one-time enrollment token.

### Quick Install Command
Run the following script on your target host machine:

```bash
curl -fsSL https://raw.githubusercontent.com/sandbox-quantum/switch/main/console/packages/agent-controller/install.sh \
  | sh -s -- --server https://switch.example.com --code <ENROLLMENT_CODE>
```

### What This Command Does:
1. Installs the `switch-agent-controller` CLI globally (or under `~/.local/` if running as a non-root user).
2. Connects to `https://switch.example.com` and redeems the one-time enrollment code.
3. Generates a secure, cryptographic host credential in the data directory.
4. Registers the host machine in Switch Gateway's **Machines** inventory.
5. Configures and starts a persistent `systemd` user service (on Linux) or `launchd` service (on macOS).

---

## 3. Managing the Service

Once enrolled, the daemon can be managed using the `switch-agent-controller` CLI:

```bash
# Check service and agent health
switch-agent-controller status

# Run comprehensive system diagnostics
switch-agent-controller doctor

# Upgrade to the latest release
switch-agent-controller update

# Inspect daemon logs
journalctl --user -u switch-agent-controller -f
```

---

## 4. Execution Modes: Shared vs. Isolated Agents

When configuring agents in Switch, you can choose between two execution architectures:

### 1. Shared Host Model (Default)
- All assigned agents run inside the controller's main daemon process as co-located agent hosts.
- Low memory footprint; optimal for running multiple lightweight triage, linting, and customer-support agents on a shared VM.
- Communicates with Switch Core over a multiplexed, persistent WebSocket relay.

### 2. Isolated Execution Model (`isolation: "isolated"`)
- The agent runs inside its own dedicated child process with an isolated file system directory and its own event watcher.
- On Linux, if configured with `systemd`, isolated agents execute as separate dedicated system users (`switch-agent-<id>`) with restricted read/write permissions.
- Recommended for untrusted, general-purpose coding agents executing arbitrary third-party bash commands.

---

## 5. Agent Provider Authentication on Headless Hosts

Headless servers lack web browsers for interactive OAuth logins. To authenticate provider CLIs on the host:

### Method A: Environment File (Recommended)
Place vendor API keys in an environment file (e.g. `/etc/switch/controller.env`):
```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...
GEMINI_API_KEY=AIzaSy...
```
Start the controller with `--env-file /etc/switch/controller.env`. The daemon passes these variables strictly to the authorized agent subprocesses.

### Method B: Pre-Authenticated CLI Profiles
Log in once via SSH using the provider's native headless login flow:
```bash
claude login --no-browser
codex auth login
```

---

## 6. Diagnostic Troubleshooting & Error Reason Codes

Run `switch-agent-controller doctor` to diagnose connection errors. Common reason codes include:

| Error Code | Root Cause | Solution |
| :--- | :--- | :--- |
| `ERR_WS_AUTH_FAILED` | Machine enrollment token expired or revoked. | Generate a new enrollment code in Switch Gateway and re-enroll with `switch-agent-controller enroll --code <code>`. |
| `ERR_PROVIDER_NOT_FOUND` | Agent requires `claude` or `codex`, but binary is not found on `$PATH`. | Install the CLI globally (`npm install -g @anthropic-ai/claude-code`) or verify `$PATH` in systemd service configuration. |
| `ERR_SQLITE_VERSION` | Node.js version is below 22.13. | Upgrade Node.js via `nvm install 22` or system package manager. |
| `ERR_RELAY_PORT_COLLISION` | Loopback relay port is already bound by another daemon instance. | Set a custom base port using `--relay-port 39500`. |
