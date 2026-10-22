"""
Swarm Orchestrator Engine
Coordinates concurrent sub-agent workers, manages infinite loop generation,
handles graceful signals, and renders live terminal dashboard.
"""

import asyncio
import signal
import sys
import logging
from typing import Optional, List
from rich.console import Console
from rich.live import Live
from rich.layout import Layout

from config import config
from core.llm_clients import create_llm_client
from core.llm_clients.base import BaseLLMClient
from core.telemetry import SwarmTelemetry
from core.worker import SubAgentWorker
from core.domains import domain_manager

logger = logging.getLogger("SwarmOrchestrator")


class SwarmOrchestrator:
    """Master controller orchestrating concurrent sub-agents in a continuous swarm loop."""

    def __init__(
        self,
        backend: Optional[str] = None,
        model: Optional[str] = None,
        num_agents: Optional[int] = None,
        infinite: Optional[bool] = None,
        target_count: Optional[int] = None
    ):
        self.backend = backend or config.default_backend
        self.model = model or config.default_model
        self.num_agents = num_agents or config.concurrent_agents
        self.infinite = infinite if infinite is not None else config.infinite_loop
        self.target_count = target_count

        self.telemetry = SwarmTelemetry(num_agents=self.num_agents)
        self.llm_client: BaseLLMClient = create_llm_client(self.backend, self.model)
        self.workers: List[SubAgentWorker] = [
            SubAgentWorker(
                agent_id=i,
                llm_client=self.llm_client,
                telemetry=self.telemetry,
                auto_repair=config.auto_repair
            )
            for i in range(1, self.num_agents + 1)
        ]
        self._shutdown_event = asyncio.Event()

    def handle_shutdown(self):
        """Signals workers to stop cleanly on user interrupt."""
        logger.info("\n[!] Shutdown signal received. Halting swarm gracefully...")
        self._shutdown_event.set()

    async def _worker_loop(self, worker: SubAgentWorker):
        """Continuous execution loop for an individual sub-agent worker."""
        while not self._shutdown_event.is_set():
            if self.target_count and self.telemetry.total_valid >= self.target_count:
                break

            try:
                await worker.execute_cycle()
            except Exception as e:
                logger.error(f"Worker #{worker.agent_id} unhandled loop exception: {e}")
                await asyncio.sleep(2.0)

            # Check termination
            if not self.infinite and not self.target_count:
                break

            # Brief stagger to prevent exact simultaneous network bursts
            await asyncio.sleep(0.5)

    async def run(self):
        """Starts the multi-agent concurrent swarm and live dashboard."""
        console = Console()
        console.print(
            f"[bold green]>> INITIALIZING LUMINA AI DATASET SWARM[/bold green] "
            f"([cyan]{self.num_agents} Sub-Agents[/cyan] | "
            f"Provider: [yellow]{self.backend.upper()}[/yellow] | "
            f"Model: [white]{self.model}[/white])"
        )

        def make_layout() -> Layout:
            layout = Layout()
            layout.split_column(
                Layout(self.telemetry.get_summary_table(), name="summary", size=10),
                Layout(self.telemetry.get_agent_status_table(), name="agents")
            )
            return layout

        worker_tasks = [asyncio.create_task(self._worker_loop(w)) for w in self.workers]

        # Dashboard refresh loop
        async def dashboard_loop():
            with Live(make_layout(), refresh_per_second=2, console=console) as live:
                while not self._shutdown_event.is_set():
                    if all(t.done() for t in worker_tasks):
                        break
                    live.update(make_layout())
                    await asyncio.sleep(0.5)
                live.update(make_layout())

        dash_task = asyncio.create_task(dashboard_loop())

        try:
            await asyncio.gather(*worker_tasks)
        except asyncio.CancelledError:
            pass
        finally:
            self._shutdown_event.set()
            await dash_task

        console.print("[bold green][OK] Swarm run finished cleanly.[/bold green]")
        console.print(self.telemetry.get_summary_table())
