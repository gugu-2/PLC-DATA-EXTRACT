"""
Telemetry, Metrics & Live Swarm Dashboard
Displays rich terminal status, worker activities, token consumption, and throughput.
"""

import time
from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text


class SwarmTelemetry:
    """Thread-safe telemetry and metrics aggregator for multi-agent swarm."""

    def __init__(self, num_agents: int = 8):
        self.num_agents = num_agents
        self.start_time = time.time()
        self.total_generated = 0
        self.total_valid = 0
        self.total_repaired = 0
        self.total_failed = 0
        self.total_chars = 0
        self.agent_statuses: Dict[int, Dict[str, Any]] = {
            i: {
                "status": "INITIALIZING",
                "domain": "-",
                "last_active": time.time(),
                "records_done": 0,
                "current_chars": 0
            }
            for i in range(1, num_agents + 1)
        }

    def update_agent(self, agent_id: int, status: str, domain: str = "", chars: int = 0):
        if agent_id in self.agent_statuses:
            self.agent_statuses[agent_id]["status"] = status
            if domain:
                self.agent_statuses[agent_id]["domain"] = domain
            if chars:
                self.agent_statuses[agent_id]["current_chars"] = chars
            self.agent_statuses[agent_id]["last_active"] = time.time()

    def record_success(self, agent_id: int, chars: int, was_repaired: bool = False):
        self.total_generated += 1
        self.total_valid += 1
        self.total_chars += chars
        if was_repaired:
            self.total_repaired += 1
        if agent_id in self.agent_statuses:
            self.agent_statuses[agent_id]["records_done"] += 1
            self.agent_statuses[agent_id]["status"] = "SAVED_SUCCESS"

    def record_failure(self, agent_id: int, error_msg: str):
        self.total_generated += 1
        self.total_failed += 1
        if agent_id in self.agent_statuses:
            self.agent_statuses[agent_id]["status"] = f"FAILED: {error_msg[:24]}"

    def get_summary_table(self) -> Table:
        elapsed = max(time.time() - self.start_time, 1.0)
        rate_hr = (self.total_valid / elapsed) * 3600.0
        chars_per_sec = self.total_chars / elapsed
        est_tokens = int(self.total_chars / 3.8)

        table = Table(title="[LUMINA INDUSTRIAL AI SWARM METRICS]", style="cyan")
        table.add_column("Metric", style="bold white")
        table.add_column("Value", style="bold green")

        table.add_row("Elapsed Time", f"{int(elapsed // 3600)}h {int((elapsed % 3600) // 60)}m {int(elapsed % 60)}s")
        table.add_row("Total Valid Records", str(self.total_valid))
        table.add_row("Auto-Repaired Records", str(self.total_repaired))
        table.add_row("Failed / Rejected", str(self.total_failed))
        table.add_row("Total Characters Generated", f"{self.total_chars:,} chars")
        table.add_row("Estimated Tokens Consumed", f"{est_tokens:,} tokens")
        table.add_row("Throughput Speed", f"{rate_hr:.1f} records/hr ({chars_per_sec:,.0f} chars/sec)")
        return table

    def get_agent_status_table(self) -> Table:
        table = Table(title=f"[ACTIVE SUB-AGENTS ({self.num_agents} CONCURRENT WORKERS)]", style="magenta")
        table.add_column("Agent", style="bold yellow", width=10)
        table.add_column("Status", style="cyan", width=22)
        table.add_column("Assigned Domain", style="white", width=42)
        table.add_column("Completed", style="green", width=12)

        for aid, data in self.agent_statuses.items():
            status_style = "green" if "SAVED" in data["status"] else ("yellow" if "GEN" in data["status"] else "white")
            table.add_row(
                f"Agent #{aid:02d}",
                f"[{status_style}]{data['status']}[/{status_style}]",
                data["domain"][:40] if data["domain"] else "-",
                str(data["records_done"])
            )
        return table
