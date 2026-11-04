# OpsSwitch: Architectural Diagrams & Topology

This document details the system design, communication protocols, and sequence interactions powering OpsSwitch.

---

## 1. System Topology & Dual-Room Architecture

The multi-room model ensures that sensitive investigation details, high-volume stack traces, and experimental reproduction scripts are contained within the `#incident-war-room`, while clean status updates and resolution notices flow back to `#incident-intake`.

```mermaid
graph TD
    subgraph Chat_Platform ["Team Chat Workspace (Slack / Discord / Teams)"]
        subgraph Intake_Channel ["#incident-intake (Public Channel)"]
            User["Human Engineer / On-Call Lead"]
            AlertBot["Alert Webhook / Monitoring"]
            TriagerIntake["ops-triager"]
        end

        subgraph WarRoom_Channel ["#incident-war-room (Restricted Channel)"]
            TriagerWar["ops-triager (Bridge Liaison)"]
            Investigator["ops-investigator"]
            Remediator["ops-remediator"]
            LeadEngineer["On-Call Approval Lead"]
        end
    end

    subgraph Switch_Infrastructure ["Switch Open Source Core (Docker / Local Host)"]
        SwitchBridge["Switch Bridge Layer"]
        RoomIntake["Room: incident-intake"]
        RoomWar["Room: incident-war-room"]
        RoomLink["Room Link: 'escalations'"]
        SessionHost["Switch Session Host & Broker"]
    end

    subgraph External_Integrations ["Connected Services (via Switch Connectors)"]
        GitHubConn["GitHub Connector (Commits, PRs, Reverts)"]
        SentryConn["Sentry / Datadog Connector (Logs, Traces)"]
        LocalSandbox["Agent Local Workspace (Repro Sandbox)"]
    end

    AlertBot -->|Alert Event| Intake_Channel
    User -->|Chat / Question| Intake_Channel
    Intake_Channel <--> SwitchBridge
    WarRoom_Channel <--> SwitchBridge

    SwitchBridge <--> RoomIntake
    SwitchBridge <--> RoomWar
    RoomIntake <-->|Cross-Room Context| RoomLink
    RoomLink <--> RoomWar

    RoomWar <--> SessionHost
    SessionHost <--> GitHubConn
    SessionHost <--> SentryConn
    Investigator <--> LocalSandbox
```

---

## 2. End-to-End Incident Resolution Sequence Diagram

The following sequence illustrates the exact turn-by-turn workflow during a live SEV-1 production failure.

```mermaid
sequenceDiagram
    autonumber
    actor Engineer as Human Engineer (@Farhan)
    participant Intake as #incident-intake
    participant Triager as ops-triager
    participant WarRoom as #incident-war-room
    participant Investigator as ops-investigator
    participant Remediator as ops-remediator
    participant SwitchHost as Switch Session Host
    participant GitHub as GitHub API

    Note over Engineer, Intake: Step 1: Alert Ingestion & Classification
    Engineer->>Intake: @ops-triager 500 errors on checkout since 09:40 deploy!
    Intake->>Triager: SSE: message_created
    Triager->>Triager: Analyze scope: payment/checkout affected -> Classify SEV-1
    Triager->>Intake: Acknowledged. Classifying as SEV-1. Escalating to war room.
    
    Note over Triager, WarRoom: Step 2: Cross-Room Handshake & Escalation
    Triager->>WarRoom: 🚨 ESCALATION: Checkout 500s reported. @ops-investigator begin triage.
    WarRoom->>Investigator: SSE: message_created

    Note over Investigator, SwitchHost: Step 3: Diagnostic Investigation
    Investigator->>WarRoom: Examining commit diffs and Sentry error logs...
    Investigator->>SwitchHost: MCP Call: github.list_recent_commits()
    SwitchHost->>GitHub: GET /repos/acme/cart-service/commits
    GitHub-->>SwitchHost: Returns commit f3c8a91 ("feat: coupon code parser")
    SwitchHost-->>Investigator: Sanitized commit payload
    Investigator->>Investigator: Run local repro.py --payload '{"coupon": null}'
    Investigator-->>WarRoom: Repro confirmed! NullPointerException in CartService:142. Tagging @ops-remediator.

    Note over Remediator, Engineer: Step 4: Remediation Plan & Human Gate
    WarRoom->>Remediator: SSE: message_created
    Remediator->>SwitchHost: MCP Call: github.create_pull_request(revert_commit="f3c8a91")
    SwitchHost-->>Remediator: PR #412 created (Revert f3c8a91)
    Remediator->>WarRoom: ⚠️ CHANGE REQUEST: Rollback PR #412 ready.<br/>@Farhan please reply "Approved. Roll it back." to execute.

    Engineer->>WarRoom: Approved. Roll it back.
    WarRoom->>Remediator: SSE: message_created (Approval confirmed)

    Note over Remediator, Intake: Step 5: Execution, Verification & Post-Mortem
    Remediator->>SwitchHost: MCP Call: github.merge_pull_request(412)
    SwitchHost-->>Remediator: Merged to main. Deploy triggered.
    Remediator->>Remediator: Poll healthcheck endpoint -> HTTP 200 OK verified
    Remediator->>WarRoom: Rollback complete. Health restored to 100%. Handing off to @ops-triager.
    Remediator->>Triager: Incident marked resolved.
    Triager->>Intake: ✅ INCIDENT RESOLVED: Checkout restored. Root cause: NPE in commit f3c8a91. Reverted in PR #412. Total downtime: 8 minutes.
```

---

## 3. Data Flow & Zero-Leakage Credential Architecture

Security is guaranteed through Switch's isolated broker architecture:

```mermaid
flowchart LR
    subgraph Agent_Process ["Agent Runtime (Untrusted LLM Context)"]
        AgentPrompt["Agent System Prompt & Instructions"]
        MCPClient["Local MCP Tool Invocation"]
    end

    subgraph Switch_Local ["Switch Session Host (Trusted Local Broker)"]
        AuthFilter["Header & Credential Filter"]
        TokenCache["Encrypted Key Store (Pass-Through)"]
        AuditLog["Immutable Session Audit Log"]
    end

    subgraph External_API ["Target Cloud Provider"]
        VendorAPI["GitHub / Sentry / Datadog API"]
    end

    AgentPrompt -->|Invokes Tool| MCPClient
    MCPClient -->|"github.revert(sha='f3c8a91')"| AuthFilter
    TokenCache -->|Injects Bearer Token| AuthFilter
    AuthFilter -->|"POST /repos/... (with auth header)"| VendorAPI
    VendorAPI -->|"200 OK Response"| AuthFilter
    AuthFilter -->|Strips Auth & Sanitizes| MCPClient
    MCPClient -->|Returns Clean Result| AgentPrompt
```

### Key Security Safeguards
1. **Agent Ignorance**: The agent has no access to environment variables containing API tokens.
2. **Strict Loopback**: Tool execution occurs over local Unix sockets or loopback HTTP (`127.0.0.1`).
3. **Audit Trail**: Every tool invocation and human approval is immutably logged in the session transcript.
