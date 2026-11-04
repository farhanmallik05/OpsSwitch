#!/usr/bin/env python3
"""
OpsSwitch: Autonomous Incident Commander & War Room Simulation Engine.

Simulates an end-to-end production incident lifecycle across two linked Switch rooms:
1. #incident-intake: Ingestion, SEV classification, and executive updates.
2. #incident-war-room: Telemetry inspection, git diff analysis, sandboxed repro execution,
   draft rollback PR, strict human authorization gate, rollback merge, and health check polling.
"""

from __future__ import annotations

import argparse
import dataclasses
from datetime import datetime, timezone
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any, Callable, Dict, List, Optional

import fastapi
from fastapi import FastAPI, HTTPException
import httpx
import pydantic
from pydantic import BaseModel
import uvicorn

# Configure standard streams for UTF-8 compatibility across Windows/Unix
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass



# ============================================================================
# Color & Formatting Utilities
# ============================================================================

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

    @classmethod
    def enabled(cls) -> bool:
        return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        if cls.enabled():
            return f"{color}{text}{cls.RESET}"
        return text


# ============================================================================
# Models & Data Structures
# ============================================================================

class CheckoutRequest(BaseModel):
    item_id: str = "item_premium_subscription"
    quantity: int = 1
    coupon: Optional[str] = None


class CheckoutResponse(BaseModel):
    status: str
    order_id: str
    coupon_applied: Optional[str] = None
    total: float
    message: str


class ServiceHealth(BaseModel):
    status: str
    version: str
    timestamp: str
    endpoints: Dict[str, str]


@dataclasses.dataclass
class SeverityClassification:
    severity: str  # SEV-1, SEV-2, SEV-3, SEV-4
    service: str
    endpoint: str
    symptoms: str
    should_escalate: bool
    rationale: str


@dataclasses.dataclass
class CommitInfo:
    sha: str
    author: str
    timestamp: str
    message: str
    files_changed: List[str]
    diff_snippet: str
    is_offending: bool = False


@dataclasses.dataclass
class ReproResult:
    reproduced: bool
    exit_code: int
    output: str
    error: str
    script_path: str


@dataclasses.dataclass
class RollbackPlan:
    pr_number: int
    title: str
    revert_commit: str
    target_branch: str
    risk_level: str
    blast_radius: str
    authorization_gate: str


# ============================================================================
# Embedded Mock Cart & Checkout Microservice
# ============================================================================

class MockServiceState:
    def __init__(self) -> None:
        self.defective: bool = True
        self.version: str = "v2.14.0"
        self.incident_count: int = 0


def create_mock_app(state: MockServiceState) -> FastAPI:
    app = FastAPI(title="OpsSwitch Mock Cart & Checkout Service", version="2.14.0")

    @app.get("/health", response_model=ServiceHealth)
    def health() -> ServiceHealth:
        status_str = "degraded" if state.defective else "healthy"
        return ServiceHealth(
            status=status_str,
            version=state.version,
            timestamp=datetime.now(timezone.utc).isoformat(),
            endpoints={
                "/health": "GET",
                "/checkout": "POST",
                "/admin/status": "GET",
                "/admin/rollback": "POST",
                "/admin/inject-fault": "POST",
            },
        )

    @app.post("/checkout", response_model=CheckoutResponse)
    def checkout(req: CheckoutRequest) -> CheckoutResponse:
        # Commit f3c8a91 introduced an unhandled NullPointerException when coupon is None or empty
        if state.defective:
            if req.coupon is None or req.coupon.strip() == "":
                state.incident_count += 1
                raise HTTPException(
                    status_code=500,
                    detail=(
                        "NullPointerException in CartService:142: "
                        "Attempted to invoke String.length() on a null object reference. "
                        "Stack trace: at com.acme.cart.CartService.applyCoupon(CartService.java:142) "
                        "at com.acme.cart.CheckoutController.processOrder(CheckoutController.java:88)"
                    ),
                )
            # If coupon was provided, defective build accidentally accepted it
            return CheckoutResponse(
                status="success",
                order_id="ord_mock_10029",
                coupon_applied=req.coupon,
                total=45.0,
                message="Order placed successfully with applied promo discount.",
            )

        # Healthy state: null coupon handled safely without NullPointerException
        discount = 0.15 if req.coupon else 0.0
        final_total = round(50.0 * (1.0 - discount), 2)
        return CheckoutResponse(
            status="success",
            order_id="ord_mock_10030",
            coupon_applied=req.coupon,
            total=final_total,
            message="Order processed cleanly by CartService.",
        )

    @app.get("/admin/status")
    def get_status() -> Dict[str, Any]:
        return {
            "defective": state.defective,
            "version": state.version,
            "incident_count": state.incident_count,
        }

    @app.post("/admin/rollback")
    def rollback() -> Dict[str, Any]:
        state.defective = False
        state.version = "v2.13.2"
        return {
            "status": "rolled_back",
            "active_version": state.version,
            "defective": state.defective,
            "message": "Service restored to stable release v2.13.2. NPE defect removed.",
        }

    @app.post("/admin/inject-fault")
    def inject_fault() -> Dict[str, Any]:
        state.defective = True
        state.version = "v2.14.0"
        return {
            "status": "fault_injected",
            "active_version": state.version,
            "defective": state.defective,
            "message": "Fault injected. Coupon null pointer exception active on /checkout.",
        }

    return app


class MockServerThread:
    """Runs Uvicorn in a background thread for in-process network simulation."""

    def __init__(self, app: FastAPI, host: str = "127.0.0.1", port: int = 8000) -> None:
        self.host = host
        self.port = port
        self.app = app
        self.server: Optional[uvicorn.Server] = None
        self.thread: Optional[threading.Thread] = None

    def start(self) -> None:
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="error",
            access_log=False,
        )
        self.server = uvicorn.Server(config)
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()

        # Poll until socket responds
        timeout = 5.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with socket.create_connection((self.host, self.port), timeout=0.2):
                    break
            except (ConnectionRefusedError, OSError):
                time.sleep(0.05)

    def stop(self) -> None:
        if self.server:
            self.server.should_exit = True
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# ============================================================================
# Autonomous Agent Roles
# ============================================================================

class TriagerAgent:
    """Monitors #incident-intake, classifies severity, and escalates to war room."""

    def __init__(self, team: str = "sre") -> None:
        self.team = team

    def classify_severity(self, alert_text: str) -> SeverityClassification:
        lower = alert_text.lower()

        # Extract service and endpoint heuristics
        service = "checkout-service" if "checkout" in lower else "cart-service"
        endpoint = "/checkout" if "checkout" in lower else "/api"

        # Severity taxonomy rules
        is_revenue = any(w in lower for w in ["checkout", "payment", "purchase", "billing", "auth"])
        is_failure = any(w in lower for w in ["500", "error", "crash", "outage", "exception", "broken", "npe"])

        if is_revenue and is_failure:
            return SeverityClassification(
                severity="SEV-1",
                service=service,
                endpoint=endpoint,
                symptoms="HTTP 500 NullPointerException blocking user purchases",
                should_escalate=True,
                rationale="Core checkout and revenue generation blocked; zero customer workaround.",
            )
        elif is_failure and ("degraded" in lower or "slow" in lower or "latency" in lower):
            return SeverityClassification(
                severity="SEV-2",
                service=service,
                endpoint=endpoint,
                symptoms="High latency and partial service degradation",
                should_escalate=True,
                rationale="Important feature impaired with high error rate.",
            )
        elif "cosmetic" in lower or "typo" in lower or "color" in lower:
            return SeverityClassification(
                severity="SEV-4",
                service=service,
                endpoint=endpoint,
                symptoms="Cosmetic discrepancy in UI",
                should_escalate=False,
                rationale="Low priority cosmetic glitch; no functional impact.",
            )
        else:
            return SeverityClassification(
                severity="SEV-3",
                service=service,
                endpoint=endpoint,
                symptoms="Intermittent minor anomaly",
                should_escalate=False,
                rationale="Non-critical endpoint glitch; tracking ticket opened.",
            )

    def create_intake_acknowledgement(self, classification: SeverityClassification) -> str:
        if classification.should_escalate:
            return (
                f"🚨 Acknowledged by @{self.team}-triager. Classified as {classification.severity} "
                f"(Impact: {classification.rationale}). Escalating immediately to #{self.team}-incident-war-room."
            )
        return (
            f"ℹ️ Acknowledged by @{self.team}-triager. Classified as {classification.severity} "
            f"({classification.rationale}). Ticket logged in tracking backlog."
        )

    def create_war_room_escalation(self, classification: SeverityClassification) -> str:
        now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        return (
            f"🚨 ESCALATION [{classification.severity}]: Service `{classification.service}` "
            f"reported failing at `{now_utc}` with symptoms: `{classification.symptoms}`. "
            f"@{self.team}-investigator please begin diagnostic triage."
        )

    def create_rca_post_mortem(
        self,
        service: str,
        offending_commit: str,
        pr_number: int,
        downtime_minutes: int = 8,
    ) -> str:
        return (
            f"✅ INCIDENT RESOLVED [{service.upper()}]\n"
            f"• Severity: SEV-1 (Critical Revenue Impact)\n"
            f"• Root Cause: Unhandled NullPointerException in coupon parsing logic (commit `{offending_commit}`)\n"
            f"• Remediation: Reverted via GitHub PR #{pr_number}; stable release v2.13.2 verified\n"
            f"• Verification: Healthcheck 200 OK polling passed (100% success rate)\n"
            f"• Total Incident Duration: {downtime_minutes} minutes (MTTR reduced by 72% via OpsSwitch)\n"
            f"• Action Item: Added mandatory null check and negative coupon regression test suite."
        )


class InvestigatorAgent:
    """Inspects commit diffs, isolates defect, and runs deterministic sandboxed repro."""

    def __init__(self, team: str = "sre") -> None:
        self.team = team

    def query_recent_commits(self) -> List[CommitInfo]:
        return [
            CommitInfo(
                sha="f3c8a91",
                author="Alex Dev <alex@acme.corp>",
                timestamp="2026-11-04T09:28:14Z",
                message="feat: coupon code parser and discount calculator",
                files_changed=["src/main/java/com/acme/cart/CartService.java"],
                diff_snippet=(
                    "@@ -139,6 +139,8 @@ public void applyCoupon(Order order, String coupon) {\n"
                    "+    // Missing null check causes NullPointerException\n"
                    "+    if (coupon.length() > 0) {\n"
                    "+        order.setDiscount(calculate(coupon));\n"
                    "+    }"
                ),
                is_offending=True,
            ),
            CommitInfo(
                sha="a18b932",
                author="Ops SRE <sre@acme.corp>",
                timestamp="2026-11-04T08:15:00Z",
                message="chore: update base container image tags",
                files_changed=["Dockerfile"],
                diff_snippet="@@ -1,2 +1,2 @@\n-FROM python:3.12-slim\n+FROM python:3.13-slim",
                is_offending=False,
            ),
            CommitInfo(
                sha="98e011a",
                author="Doc Bot <bot@acme.corp>",
                timestamp="2026-11-04T07:45:22Z",
                message="docs: update API checkout documentation",
                files_changed=["README.md"],
                diff_snippet="@@ -45,2 +45,2 @@\n-v2.13.1\n+v2.13.2",
                is_offending=False,
            ),
        ]

    def find_offending_commit(self, commits: List[CommitInfo], error_trace: str) -> Optional[CommitInfo]:
        for c in commits:
            if c.is_offending:
                return c
            # Semantic search heuristic
            if "CartService" in error_trace and any("CartService" in f for f in c.files_changed):
                return c
        return commits[0] if commits else None

    def execute_sandboxed_repro(self, service_url: str) -> ReproResult:
        """Generates a minimal repro.py script in a temporary directory and executes it."""
        with tempfile.TemporaryDirectory(prefix="opsswitch_repro_") as tmp_dir:
            repro_path = os.path.join(tmp_dir, "repro.py")
            script_code = f"""import sys
import httpx

# Minimal deterministic reproduction script generated by @{self.team}-investigator
url = "{service_url}/checkout"
payload = {{"item_id": "test_repro_item", "quantity": 1, "coupon": None}}

try:
    resp = httpx.post(url, json=payload, timeout=5.0)
    if resp.status_code == 500:
        sys.stderr.write(f"REPRO PROVEN: HTTP 500 returned. Body: {{resp.text}}\\n")
        sys.exit(1)
    else:
        sys.stdout.write(f"UNEXPECTED: HTTP {{resp.status_code}}\\n")
        sys.exit(0)
except Exception as e:
    sys.stderr.write(f"EXECUTION ERROR: {{e}}\\n")
    sys.exit(2)
"""
            with open(repro_path, "w", encoding="utf-8") as f:
                f.write(script_code)

            res = subprocess.run(
                [sys.executable, repro_path],
                capture_output=True,
                text=True,
                timeout=10,
            )

            return ReproResult(
                reproduced=(res.returncode == 1),
                exit_code=res.returncode,
                output=res.stdout,
                error=res.stderr,
                script_path=repro_path,
            )


class RemediatorAgent:
    """Formulates rollback PR, enforces human authorization gate, and executes recovery."""

    def __init__(self, team: str = "sre") -> None:
        self.team = team

    def formulate_rollback_plan(self, commit_sha: str) -> RollbackPlan:
        return RollbackPlan(
            pr_number=412,
            title=f"Revert '{commit_sha}: feat: coupon code parser' [Emergency Hotfix]",
            revert_commit=commit_sha,
            target_branch="main",
            risk_level="Low",
            blast_radius="Scoped strictly to CartService coupon discount helper.",
            authorization_gate='Awaiting sign-off: reply "Approved. Roll it back." to execute.',
        )

    def render_authorization_card(self, plan: RollbackPlan) -> str:
        return (
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️  AUTHORIZATION CARD: EMERGENCY PRODUCTION ROLLBACK\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Pull Request: #{plan.pr_number} — {plan.title}\n"
            f"• Reverting Commit: `{plan.revert_commit}`\n"
            f"• Target Environment: `production` (Branch: `{plan.target_branch}`)\n"
            f"• Risk Level: {plan.risk_level} | Blast Radius: {plan.blast_radius}\n"
            f"• Human Gate: {plan.authorization_gate}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    def evaluate_human_gate(self, response_text: str) -> bool:
        """Strictly validates human authorization approval."""
        clean = response_text.strip().lower()
        # Reject explicit negative or ambiguous tokens
        reject_tokens = ["reject", "deny", "wait", "hold", "stop", "no", "disapproved", "abort", "cancel"]
        if any(token in clean for token in reject_tokens):
            return False

        # Require explicit approval
        return "approved" in clean

    def execute_rollback(self, service_url: str) -> bool:
        """Executes rollback on mock service and verifies restoration to 200 OK."""
        try:
            resp = httpx.post(f"{service_url}/admin/rollback", timeout=5.0)
            if resp.status_code != 200:
                return False

            # Verify healthcheck returns healthy
            health_resp = httpx.get(f"{service_url}/health", timeout=5.0)
            if health_resp.status_code != 200:
                return False

            # Verify null coupon checkout succeeds with 200 OK
            checkout_resp = httpx.post(
                f"{service_url}/checkout",
                json={"item_id": "test_item", "quantity": 1, "coupon": None},
                timeout=5.0,
            )
            return checkout_resp.status_code == 200
        except Exception:
            return False


# ============================================================================
# Main Incident Commander Simulation Engine
# ============================================================================

class IncidentCommanderSimulation:
    """Coordinates the dual-room incident response between Triager, Investigator, Remediator, and Human."""

    def __init__(
        self,
        port: int = 8000,
        team: str = "sre",
        step_delay: float = 0.0,
        auto_approve: bool = False,
        approval_provider: Optional[Callable[[], str]] = None,
        json_output: bool = False,
    ) -> None:
        self.port = port
        self.team = team
        self.step_delay = step_delay
        self.auto_approve = auto_approve
        self.approval_provider = approval_provider
        self.json_output = json_output

        self.service_state = MockServiceState()
        self.app = create_mock_app(self.service_state)
        self.server_thread: Optional[MockServerThread] = None

        self.triager = TriagerAgent(team=team)
        self.investigator = InvestigatorAgent(team=team)
        self.remediator = RemediatorAgent(team=team)

        self.events: List[Dict[str, Any]] = []

    def log_event(self, phase: str, room: str, agent: str, message: str, meta: Optional[Dict[str, Any]] = None) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": phase,
            "room": room,
            "agent": agent,
            "message": message,
            "metadata": meta or {},
        }
        self.events.append(event)

        if not self.json_output:
            prefix = Colors.colorize(f"[{room}]", Colors.CYAN)
            agent_tag = Colors.colorize(f"<{agent}>", Colors.YELLOW if "triager" in agent else (Colors.MAGENTA if "investigator" in agent else Colors.GREEN))
            line = f"{prefix} {agent_tag} {message}"
            try:
                print(line)
            except UnicodeEncodeError:
                print(line.encode("ascii", errors="replace").decode("ascii"))
            if self.step_delay > 0:
                time.sleep(self.step_delay)

    def run(self, alert_text: Optional[str] = None) -> bool:
        if alert_text is None:
            alert_text = "@sre-triager checkout service is throwing HTTP 500 errors since the 09:30 UTC deploy. Users cannot complete purchases."

        service_url = f"http://127.0.0.1:{self.port}"

        # Start mock server in thread
        self.server_thread = MockServerThread(self.app, host="127.0.0.1", port=self.port)
        self.server_thread.start()

        try:
            # ----------------------------------------------------------------
            # Phase 1: Ingestion & Triage (#incident-intake)
            # ----------------------------------------------------------------
            self.log_event(
                phase="ingestion",
                room=f"#{self.team}-incident-intake",
                agent="human-oncall",
                message=alert_text,
            )

            classification = self.triager.classify_severity(alert_text)
            self.log_event(
                phase="triage",
                room=f"#{self.team}-incident-intake",
                agent=f"{self.team}-triager",
                message=self.triager.create_intake_acknowledgement(classification),
                meta={"severity": classification.severity, "escalated": classification.should_escalate},
            )

            if not classification.should_escalate:
                return True

            # ----------------------------------------------------------------
            # Phase 2: Cross-Room Handshake & Escalation (#incident-war-room)
            # ----------------------------------------------------------------
            escalation_msg = self.triager.create_war_room_escalation(classification)
            self.log_event(
                phase="escalation",
                room=f"#{self.team}-incident-war-room",
                agent=f"{self.team}-triager",
                message=escalation_msg,
            )

            # ----------------------------------------------------------------
            # Phase 3: Investigation & Repro (#incident-war-room)
            # ----------------------------------------------------------------
            self.log_event(
                phase="investigation",
                room=f"#{self.team}-incident-war-room",
                agent=f"{self.team}-investigator",
                message="Querying Sentry telemetry and git commit history from deployment window...",
            )

            commits = self.investigator.query_recent_commits()
            offending = self.investigator.find_offending_commit(commits, "NullPointerException in CartService")

            if not offending:
                raise RuntimeError("Failed to isolate offending commit")

            self.log_event(
                phase="investigation",
                room=f"#{self.team}-incident-war-room",
                agent=f"{self.team}-investigator",
                message=(
                    f"Offending commit identified: `{offending.sha}` ({offending.message}) by {offending.author}.\n"
                    f"Affected file: {offending.files_changed[0]}\n"
                    f"Synthesizing minimal deterministic reproduction test in isolated sandbox..."
                ),
                meta={"commit_sha": offending.sha, "author": offending.author},
            )

            # Sandbox reproduction execution
            repro_res = self.investigator.execute_sandboxed_repro(service_url)
            self.log_event(
                phase="repro",
                room=f"#{self.team}-incident-war-room",
                agent=f"{self.team}-investigator",
                message=(
                    f"Sandboxed repro complete (Exit Code: {repro_res.exit_code}). "
                    f"Confirmed defect: NullPointerException on coupon validation. "
                    f"Tagging @{self.team}-remediator to generate rollback PR."
                ),
                meta={"reproduced": repro_res.reproduced, "exit_code": repro_res.exit_code, "error": repro_res.error},
            )

            if not repro_res.reproduced:
                raise RuntimeError("Deterministic reproduction failed to reproduce incident defect")

            # ----------------------------------------------------------------
            # Phase 4: Remediation & Human Sign-off Gate (#incident-war-room)
            # ----------------------------------------------------------------
            rollback_plan = self.remediator.formulate_rollback_plan(offending.sha)
            card_text = self.remediator.render_authorization_card(rollback_plan)

            self.log_event(
                phase="remediation_gate",
                room=f"#{self.team}-incident-war-room",
                agent=f"{self.team}-remediator",
                message=f"\n{card_text}",
                meta={"pr_number": rollback_plan.pr_number, "revert_commit": rollback_plan.revert_commit},
            )

            # Determine human approval
            approval_input = ""
            if self.auto_approve:
                approval_input = "Approved. Roll it back."
            elif self.approval_provider:
                approval_input = self.approval_provider()
            else:
                prompt_text = Colors.colorize("\n[Human Sign-Off Gate] Enter approval response (or 'Approved. Roll it back.'): ", Colors.BOLD)
                try:
                    approval_input = input(prompt_text)
                except (EOFError, KeyboardInterrupt):
                    approval_input = "no"

            self.log_event(
                phase="remediation_gate",
                room=f"#{self.team}-incident-war-room",
                agent="human-oncall-lead",
                message=approval_input,
            )

            is_approved = self.remediator.evaluate_human_gate(approval_input)
            if not is_approved:
                self.log_event(
                    phase="remediation_blocked",
                    room=f"#{self.team}-incident-war-room",
                    agent=f"{self.team}-remediator",
                    message="⛔ Deployment CANCELLED: Approval not granted by authorized human engineer. Standing down.",
                    meta={"approved": False},
                )
                return False

            # Execute Rollback
            self.log_event(
                phase="remediation_execution",
                room=f"#{self.team}-incident-war-room",
                agent=f"{self.team}-remediator",
                message=f"Human sign-off verified. Merging PR #{rollback_plan.pr_number} to {rollback_plan.target_branch}...",
            )

            rollback_ok = self.remediator.execute_rollback(service_url)
            if not rollback_ok:
                raise RuntimeError("Rollback execution or health check verification failed")

            self.log_event(
                phase="remediation_verification",
                room=f"#{self.team}-incident-war-room",
                agent=f"{self.team}-remediator",
                message="✅ Verification successful! /health and /checkout returned HTTP 200 OK. Notifying triager for closure.",
                meta={"health_verified": True},
            )

            # ----------------------------------------------------------------
            # Phase 5: Post-Mortem & Closure (#incident-intake)
            # ----------------------------------------------------------------
            rca_text = self.triager.create_rca_post_mortem(
                service=classification.service,
                offending_commit=offending.sha,
                pr_number=rollback_plan.pr_number,
                downtime_minutes=8,
            )

            self.log_event(
                phase="closure",
                room=f"#{self.team}-incident-intake",
                agent=f"{self.team}-triager",
                message=f"\n{rca_text}",
                meta={"incident_resolved": True},
            )

            return True

        finally:
            if self.server_thread:
                self.server_thread.stop()


# ============================================================================
# CLI Entrypoint
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="OpsSwitch Autonomous Incident Commander & War Room CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["simulate", "serve", "inject", "interactive"],
        default="simulate",
        help="Execution mode",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the embedded Cart & Checkout service",
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Automatically provide human approval for the rollback authorization gate",
    )
    parser.add_argument(
        "--step-delay",
        type=float,
        default=0.0,
        help="Delay in seconds between simulated agent turns",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON telemetry events",
    )

    args = parser.parse_args()

    # Serve mode: run standalone server
    if args.mode == "serve":
        state = MockServiceState()
        app = create_mock_app(state)
        print(f"Starting OpsSwitch Mock Cart Service on http://127.0.0.1:{args.port}...")
        uvicorn.run(app, host="127.0.0.1", port=args.port)
        return 0

    # Inject mode: send fault-triggering checkout request
    if args.mode == "inject":
        url = f"http://127.0.0.1:{args.port}/checkout"
        try:
            resp = httpx.post(url, json={"item_id": "item_123", "quantity": 1, "coupon": None}, timeout=5.0)
            print(f"Status Code: {resp.status_code}")
            print(f"Response: {resp.text}")
            return 0 if resp.status_code == 500 else 1
        except Exception as e:
            print(f"Error injecting fault: {e}", file=sys.stderr)
            return 1

    # Simulate or Interactive mode
    is_interactive = (args.mode == "interactive")
    auto_approve = args.auto_approve or (not is_interactive and args.mode == "simulate")

    # In case port 8000 is in use, find a free port for simulation if needed
    port = args.port
    if args.mode in ["simulate", "interactive"]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
        except OSError:
            port = find_free_port()

    sim = IncidentCommanderSimulation(
        port=port,
        team="sre",
        step_delay=args.step_delay,
        auto_approve=auto_approve,
        json_output=args.json,
    )

    success = sim.run()

    if args.json:
        print(json.dumps({"success": success, "events": sim.events}, indent=2))

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
