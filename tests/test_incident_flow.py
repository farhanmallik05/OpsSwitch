"""
OpsSwitch Integration Test Suite.

Covers the 7 Core Architectural Pillars:
1. Template Syntax & Switch v1 Specification Compliance
2. Mock Microservice Fault Injection & Recovery Endpoints
3. Triager Severity Classification & Escalation Logic
4. Investigator Semantic Diff & Sandboxed Repro Execution
5. Remediator Human Authorization Gate Strict Enforcement
6. End-to-End Async Multi-Agent Lifecycle Across Linked Rooms
7. Security & Zero-Token Leakage Verification
"""

import os
import re
import socket
import sys
from typing import Any, Dict, List
import pytest
import yaml

from fastapi.testclient import TestClient

# Ensure scripts directory is importable
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.simulate_incident import (
    CheckoutRequest,
    IncidentCommanderSimulation,
    InvestigatorAgent,
    MockServerThread,
    MockServiceState,
    RemediatorAgent,
    SeverityClassification,
    TriagerAgent,
    create_mock_app,
    find_free_port,
)


# ============================================================================
# Pillar 1: Template Syntax & Switch v1 Specification Compliance
# ============================================================================

def test_template_syntax_and_structure() -> None:
    """Verifies template.yaml and packaged templates satisfy Switch v1 specification."""
    template_paths = [
        os.path.join(REPO_ROOT, "template.yaml"),
        os.path.join(REPO_ROOT, "templates", "opsswitch", "template.yaml"),
        os.path.join(REPO_ROOT, "plan", "01_FLAGSHIP_PROJECT_BLUEPRINT", "TEMPLATE_YAML_SPECIFICATION.yaml"),
    ]

    for path in template_paths:
        assert os.path.exists(path), f"Template file missing at {path}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert isinstance(data, dict), f"Root of {path} must be a dictionary"
        assert data.get("version") == 1, "Switch template must declare version: 1"

        # Check required top-level keys
        for key in ["params", "agents", "group", "rooms", "links"]:
            assert key in data, f"Missing required top-level key '{key}' in {path}"

        # Check parameter definitions
        params = data["params"]
        assert "team" in params and params["team"]["type"] == "string"
        assert "provider" in params and params["provider"]["type"] == "provider"
        assert "location" in params and params["location"]["type"] == "location"
        assert "directory" in params and params["directory"]["type"] == "directory"
        assert "bridge" in params and params["bridge"]["type"] == "bridge"

        # Check 3 agents
        agents = data["agents"]
        assert len(agents) == 3, f"Expected 3 agents, found {len(agents)}"
        agent_names = [a["name"] for a in agents]
        assert "{team}-triager" in agent_names
        assert "{team}-investigator" in agent_names
        assert "{team}-remediator" in agent_names

        # Check addressing modes
        for a in agents:
            assert "instructions" in a and len(a["instructions"].strip()) > 50
            if a["name"] == "{team}-triager":
                assert a["addressing"] == "anyone"
            else:
                assert a["addressing"] == "owner-agents"

        # Check group
        assert data["group"]["name"] == "{team} Incident Command"

        # Check 2 rooms and link
        rooms = data["rooms"]
        assert len(rooms) == 2
        room_names = [r["name"] for r in rooms]
        assert "{team}-incident-intake" in room_names
        assert "{team}-incident-war-room" in room_names

        links = data["links"]
        assert len(links) >= 1
        escalation_link = next((l for l in links if l.get("label") == "escalations"), None)
        assert escalation_link is not None, "Missing 'escalations' link between intake and war room"
        assert escalation_link["from"] == "{team}-incident-intake"
        assert escalation_link["to"] == "{team}-incident-war-room"


# ============================================================================
# Pillar 2: Mock Microservice Fault Injection & Recovery Endpoints
# ============================================================================

def test_mock_service_behavior() -> None:
    """Verifies that the mock Cart & Checkout service reproduces NPE defect and rollback recovery."""
    state = MockServiceState()
    app = create_mock_app(state)
    client = TestClient(app)

    # 1. Health check during degraded/defective state
    res = client.get("/health")
    assert res.status_code == 200
    health_data = res.json()
    assert health_data["status"] == "degraded"
    assert health_data["version"] == "v2.14.0"

    # 2. Normal checkout with valid coupon works in defective build
    res = client.post("/checkout", json={"item_id": "test_item", "quantity": 1, "coupon": "DISCOUNT10"})
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # 3. Checkout with null or empty coupon crashes with HTTP 500 NullPointerException
    res_null = client.post("/checkout", json={"item_id": "test_item", "quantity": 1, "coupon": None})
    assert res_null.status_code == 500
    assert "NullPointerException in CartService:142" in res_null.json()["detail"]

    res_empty = client.post("/checkout", json={"item_id": "test_item", "quantity": 1, "coupon": "   "})
    assert res_empty.status_code == 500
    assert "NullPointerException" in res_empty.json()["detail"]

    # 4. Trigger administrative rollback
    res_rollback = client.post("/admin/rollback")
    assert res_rollback.status_code == 200
    assert res_rollback.json()["active_version"] == "v2.13.2"
    assert res_rollback.json()["defective"] is False

    # 5. Verify service is now healthy and null coupon is handled cleanly
    res_health_after = client.get("/health")
    assert res_health_after.status_code == 200
    assert res_health_after.json()["status"] == "healthy"

    res_checkout_after = client.post("/checkout", json={"item_id": "test_item", "quantity": 1, "coupon": None})
    assert res_checkout_after.status_code == 200
    assert res_checkout_after.json()["status"] == "success"

    # 6. Re-inject fault and verify degraded behavior returns
    res_inject = client.post("/admin/inject-fault")
    assert res_inject.status_code == 200
    assert res_inject.json()["defective"] is True
    res_null_again = client.post("/checkout", json={"item_id": "test_item", "quantity": 1, "coupon": None})
    assert res_null_again.status_code == 500


# ============================================================================
# Pillar 3: Triager Severity Classification & Escalation Logic
# ============================================================================

def test_triager_severity_classification() -> None:
    """Verifies Triager correctly classifies SEV-1 through SEV-4 and triggers room escalation."""
    triager = TriagerAgent(team="sre")

    # SEV-1: Critical outage on core revenue/checkout
    sev1 = triager.classify_severity("500 errors on /checkout endpoint, payments are failing for all users!")
    assert sev1.severity == "SEV-1"
    assert sev1.should_escalate is True
    ack1 = triager.create_intake_acknowledgement(sev1)
    assert "SEV-1" in ack1
    assert "Escalating immediately to #sre-incident-war-room" in ack1
    esc1 = triager.create_war_room_escalation(sev1)
    assert "@sre-investigator please begin diagnostic triage" in esc1

    # SEV-2: High latency / degraded service
    sev2 = triager.classify_severity("Service is heavily degraded and slow with 500 latency spikes")
    assert sev2.severity == "SEV-2"
    assert sev2.should_escalate is True

    # SEV-3: Non-critical glitch
    sev3 = triager.classify_severity("Minor search filter anomaly on dashboard table")
    assert sev3.severity == "SEV-3"
    assert sev3.should_escalate is False
    ack3 = triager.create_intake_acknowledgement(sev3)
    assert "Ticket logged in tracking backlog" in ack3

    # SEV-4: Cosmetic UI defect
    sev4 = triager.classify_severity("Cosmetic button color discrepancy on settings screen")
    assert sev4.severity == "SEV-4"
    assert sev4.should_escalate is False

    # Executive RCA generation
    rca = triager.create_rca_post_mortem(
        service="checkout-service",
        offending_commit="f3c8a91",
        pr_number=412,
        downtime_minutes=8,
    )
    assert "INCIDENT RESOLVED [CHECKOUT-SERVICE]" in rca
    assert "commit `f3c8a91`" in rca
    assert "PR #412" in rca


# ============================================================================
# Pillar 4: Investigator Semantic Diff & Sandboxed Repro Execution
# ============================================================================

def test_investigator_repro_generation() -> None:
    """Verifies that the investigator isolates commit f3c8a91 and executes sandbox repro."""
    investigator = InvestigatorAgent(team="sre")

    # Query commits and verify offending commit isolation
    commits = investigator.query_recent_commits()
    assert len(commits) >= 3
    offending = investigator.find_offending_commit(commits, "NullPointerException in CartService:142")
    assert offending is not None
    assert offending.sha == "f3c8a91"
    assert "feat: coupon code parser" in offending.message
    assert "CartService.java" in offending.files_changed[0]

    # Spin up mock service on ephemeral port to test live sandbox reproduction
    port = find_free_port()
    state = MockServiceState()
    state.defective = True
    app = create_mock_app(state)
    server = MockServerThread(app, host="127.0.0.1", port=port)
    server.start()

    try:
        service_url = f"http://127.0.0.1:{port}"
        repro = investigator.execute_sandboxed_repro(service_url)

        # Repro script must have run in external subprocess and exited with code 1
        assert repro.reproduced is True
        assert repro.exit_code == 1
        assert "REPRO PROVEN: HTTP 500 returned" in repro.error
        assert "NullPointerException" in repro.error
    finally:
        server.stop()


# ============================================================================
# Pillar 5: Remediator Human Authorization Gate Strict Enforcement
# ============================================================================

def test_remediator_gate_enforcement() -> None:
    """Verifies that the Remediator strictly blocks rollback without human approval."""
    remediator = RemediatorAgent(team="sre")

    plan = remediator.formulate_rollback_plan("f3c8a91")
    assert plan.pr_number == 412
    assert plan.revert_commit == "f3c8a91"
    assert plan.target_branch == "main"

    card = remediator.render_authorization_card(plan)
    assert "AUTHORIZATION CARD: EMERGENCY PRODUCTION ROLLBACK" in card
    assert "Pull Request: #412" in card
    assert "Human Gate" in card

    # Valid approval expressions
    assert remediator.evaluate_human_gate("Approved. Roll it back.") is True
    assert remediator.evaluate_human_gate("Approved") is True
    assert remediator.evaluate_human_gate("Yes, approved. Proceed with merge.") is True

    # Rejection or ambiguous tokens MUST be blocked
    assert remediator.evaluate_human_gate("No, wait.") is False
    assert remediator.evaluate_human_gate("Hold on, let me check Sentry first.") is False
    assert remediator.evaluate_human_gate("Denied.") is False
    assert remediator.evaluate_human_gate("Reject this change.") is False
    assert remediator.evaluate_human_gate("Not approved yet.") is False
    assert remediator.evaluate_human_gate("Disapproved.") is False
    assert remediator.evaluate_human_gate("Abort deployment.") is False
    assert remediator.evaluate_human_gate("") is False


# ============================================================================
# Pillar 6: End-to-End Async Multi-Agent Lifecycle Across Linked Rooms
# ============================================================================

def test_end_to_end_lifecycle() -> None:
    """Verifies complete incident lifecycle from intake alert to RCA resolution."""
    port = find_free_port()

    # Case A: Approved execution completes 100%
    sim = IncidentCommanderSimulation(
        port=port,
        team="sre",
        step_delay=0.0,
        auto_approve=True,
        json_output=True,
    )
    success = sim.run("@sre-triager checkout service is throwing HTTP 500 errors since the 09:30 UTC deploy!")
    assert success is True

    # Check event stream across both rooms
    events = sim.events
    assert len(events) >= 8

    phases = [e["phase"] for e in events]
    assert "ingestion" in phases
    assert "triage" in phases
    assert "escalation" in phases
    assert "investigation" in phases
    assert "repro" in phases
    assert "remediation_gate" in phases
    assert "remediation_execution" in phases
    assert "remediation_verification" in phases
    assert "closure" in phases

    rooms = set(e["room"] for e in events)
    assert "#sre-incident-intake" in rooms
    assert "#sre-incident-war-room" in rooms

    # Case B: Human rejection cancels deployment and blocks rollback
    port_b = find_free_port()
    sim_rejected = IncidentCommanderSimulation(
        port=port_b,
        team="sre",
        step_delay=0.0,
        auto_approve=False,
        approval_provider=lambda: "Wait, do not touch production yet!",
        json_output=True,
    )
    result_rejected = sim_rejected.run("@sre-triager checkout service broken!")
    assert result_rejected is False

    rejected_phases = [e["phase"] for e in sim_rejected.events]
    assert "remediation_blocked" in rejected_phases
    assert "remediation_execution" not in rejected_phases


# ============================================================================
# Pillar 7: Security & Zero-Token Leakage Verification
# ============================================================================

def test_security_zero_token_leakage() -> None:
    """Verifies that no secrets or raw bearer tokens leak into chat payloads or codebase."""
    # Forbidden patterns for cloud API keys and tokens
    forbidden_patterns = [
        re.compile(r"ghp_[A-Za-z0-9_]{36}"),
        re.compile(r"github_pat_[A-Za-z0-9_]{22}_[A-Za-z0-9_]{59}"),
        re.compile(r"sntrys_[A-Za-z0-9_]{40,}"),
        re.compile(r"sk-[A-Za-z0-9]{32,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
    ]

    # Check simulation script and test file for hardcoded API keys
    files_to_scan = [
        os.path.join(REPO_ROOT, "scripts", "simulate_incident.py"),
        os.path.join(REPO_ROOT, "tests", "test_incident_flow.py"),
        os.path.join(REPO_ROOT, "template.yaml"),
        os.path.join(REPO_ROOT, "README.md"),
    ]

    for fpath in files_to_scan:
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            for pattern in forbidden_patterns:
                matches = pattern.findall(content)
                assert len(matches) == 0, f"Found leaked token pattern in {fpath}: {matches}"

    # Check simulated event stream messages for token leakage
    sim = IncidentCommanderSimulation(port=find_free_port(), auto_approve=True, json_output=True)
    sim.run()
    for ev in sim.events:
        msg = ev.get("message", "")
        for pattern in forbidden_patterns:
            matches = pattern.findall(msg)
            assert len(matches) == 0, f"Found leaked token in event {ev['phase']}: {matches}"
