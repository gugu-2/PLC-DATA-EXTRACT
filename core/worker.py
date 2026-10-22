"""
Sub-Agent Worker Lifecycle Engine
Drives single worker loop: Domain Evolution -> Prompt Synthesis -> LLM Generation ->
Validation -> Auto-Repair -> Atomic Persistence -> Telemetry Sync.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from core.domains import DomainSpec, domain_manager
from core.evolver import evolver
from core.personas import build_evolution_prompt, SYSTEM_PERSONA_PROMPT, build_repair_prompt
from core.validator import validator, ValidationResult
from core.repair import repair_engine
from core.storage import storage
from core.telemetry import SwarmTelemetry
from core.llm_clients.base import BaseLLMClient
from config import config

logger = logging.getLogger("Worker")


class SubAgentWorker:
    """Represents a single concurrent sub-agent in the generation swarm."""

    def __init__(
        self,
        agent_id: int,
        llm_client: BaseLLMClient,
        telemetry: SwarmTelemetry,
        auto_repair: bool = True
    ):
        self.agent_id = agent_id
        self.llm_client = llm_client
        self.telemetry = telemetry
        self.auto_repair = auto_repair

    async def execute_cycle(self, domain: Optional[DomainSpec] = None) -> bool:
        """Executes a single end-to-end dataset synthesis iteration."""
        # 1. Select & Evolve Domain
        target_domain = domain or domain_manager.get_random()
        evolved_domain = evolver.evolve(target_domain)

        self.telemetry.update_agent(
            self.agent_id,
            status="GENERATING_PROMPT",
            domain=evolved_domain.name
        )

        prompt = build_evolution_prompt(evolved_domain)

        # 2. Invoke LLM with Extreme Token Persona
        self.telemetry.update_agent(
            self.agent_id,
            status="LLM_SYNTHESIS_STREAM",
            domain=evolved_domain.name
        )

        try:
            raw_response = await self.llm_client.generate_response(
                prompt=prompt,
                system_prompt=SYSTEM_PERSONA_PROMPT,
                temperature=0.72
            )
        except Exception as e:
            logger.error(f"Agent #{self.agent_id} generation error: {e}")
            self.telemetry.record_failure(self.agent_id, str(e))
            return False

        char_len = len(raw_response)
        self.telemetry.update_agent(
            self.agent_id,
            status="VALIDATING_SYNTAX",
            domain=evolved_domain.name,
            chars=char_len
        )

        # 3. Validation Phase
        val_result: ValidationResult = validator.validate(raw_response)
        final_code = val_result.extracted_code
        was_repaired = False

        # 4. Auto-Repair Phase if needed
        if not val_result.is_valid and self.auto_repair:
            self.telemetry.update_agent(
                self.agent_id,
                status="AUTO_REPAIRING",
                domain=evolved_domain.name
            )
            # Try deterministic algorithmic repair first
            repaired_ok, repaired_code, repaired_val = repair_engine.try_repair(raw_response)
            if repaired_ok:
                final_code = repaired_code
                val_result = repaired_val
                was_repaired = True
            else:
                # Fallback to LLM targeted repair prompt
                try:
                    repair_prompt = build_repair_prompt(final_code, "\n".join(val_result.errors))
                    llm_repaired = await self.llm_client.generate_response(
                        prompt=repair_prompt,
                        system_prompt="You are an expert IEC 61131-3 syntax repair engine.",
                        temperature=0.2
                    )
                    r_val = validator.validate(llm_repaired)
                    if r_val.is_valid:
                        final_code = r_val.extracted_code
                        val_result = r_val
                        was_repaired = True
                except Exception as ex:
                    logger.warning(f"Agent #{self.agent_id} LLM repair failed: {ex}")

        # 5. Check final validation
        if not val_result.is_valid:
            error_summary = "; ".join(val_result.errors[:2])
            logger.warning(f"Agent #{self.agent_id} validation failed: {error_summary}")
            self.telemetry.record_failure(self.agent_id, error_summary)
            return False

        # 6. Deduplication Check
        if storage.is_duplicate(final_code):
            logger.info(f"Agent #{self.agent_id} duplicate code detected. Skipping save.")
            self.telemetry.record_failure(self.agent_id, "DUPLICATE_CODE_HASH")
            return False

        # 7. Atomic Persistence
        self.telemetry.update_agent(
            self.agent_id,
            status="ATOMIC_SAVING",
            domain=evolved_domain.name
        )

        saved_path, rec_id = storage.save_record(
            prompt=prompt,
            code=final_code,
            domain_id=evolved_domain.id,
            domain_name=evolved_domain.name,
            function_block_name=evolved_domain.function_block_name,
            validation_metrics=val_result.metrics,
            category=evolved_domain.category.lower().replace(" ", "_").replace("&", "and"),
            task_type="cyber_physical_state_space_control"
        )

        logger.info(f"Agent #{self.agent_id} successfully saved record [{rec_id}] -> {saved_path.name}")
        self.telemetry.record_success(self.agent_id, len(final_code), was_repaired=was_repaired)
        return True
