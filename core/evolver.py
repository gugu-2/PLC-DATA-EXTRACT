"""
Evol-Instruct Style Complexity Mutation Engine
Mutates and evolves cyber-physical domains to generate increasingly rigorous,
complex, and challenging edge-case synthetic training data over time.
"""

import random
import time
from typing import List, Dict, Any, Optional
from copy import deepcopy
from core.domains import DomainSpec


FAILURE_MODES = [
    "Severe sensor drift on Channel B exceeding 3-sigma tolerance",
    "Actuator partial stiction with 450 ms hydraulic slew latency",
    "Abrupt downstream pipe blockage causing severe hydraulic fluid hammer surge",
    "Loss of primary cooling loop forcing degraded passive convective fallback",
    "Cyber-physical sensor packet spoofing / stuck-at fault on high-speed fieldbus",
    "Simultaneous power bus brownout with battery reserve voltage droop",
    "Extreme thermal exotherm approaching runaway degradation threshold",
    "High-vibration resonant frequency excitation near structural flutter limit",
    "Cavitation bubble collapse micro-jets eroding impeller blades under low NPSH",
    "High-temperature creep fatigue induced micro-cracking across high-pressure containment",
    "Transient gas slug entrapment in high-viscosity liquid process fluid stream",
    "Electromagnetic field interference (EMI) injecting common-mode voltage spikes into ADC channel"
]

COMPLEXITY_ENHANCERS = [
    "Incorporate discrete-time Kalman Filter prediction-update state observer matrices",
    "Add non-linear friction compensation (Stribeck / Coulomb model) to actuator output",
    "Implement anti-windup integrator clamping with bumpless auto-to-manual transfer",
    "Incorporate real-time dynamic matrix inversion approximation for receding horizon MPC",
    "Add 2oo3 discrepancy accumulation with automated degradation to 1oo2 fail-safe",
    "Include high-frequency low-pass Butterworth filter state update equations",
    "Incorporate MIMO cross-coupling decoupling gain matrix with feedforward compensation",
    "Implement sliding mode boundary layer chattering reduction algorithm",
    "Add adaptive gain scheduling based on estimated process non-linearity index",
    "Integrate fast Fourier transform (FFT) harmonic distortion threshold detection logic"
]

SAFETY_DIRECTIVES = [
    "Mandate strict IEC 61508 SIL-3 diagnostic coverage (> 99%) logic",
    "Enforce ISA-18.2 multi-tiered alarm shelving, suppress-by-design, and state-based alarm masking",
    "Incorporate dual-watchdog cyclic timing verification with fail-safe de-energization",
    "Implement zero-trust boundary verification on all fieldbus communication packets",
    "Add emergency trip interlock with automated nitrogen inerting purge sequence"
]


class DomainEvolver:
    """
    Applies stochastic and progressive evolutionary mutations to domains.
    Automatically escalates complexity over successive generation iterations.
    """

    def __init__(self, mutation_rate: float = 0.85):
        self.mutation_rate = mutation_rate
        self.generation_count = 0

    def get_difficulty_tier(self) -> str:
        """Dynamically scales difficulty tier as generation count increases."""
        if self.generation_count < 20:
            return "TIER_1_ADVANCED_CYBER_PHYSICAL"
        elif self.generation_count < 60:
            return "TIER_2_MULTI_FAILURE_COUPLING"
        elif self.generation_count < 120:
            return "TIER_3_MIMO_NONLINEAR_KALMAN_MPC"
        else:
            return "TIER_4_GOD_TIER_CATASTROPHIC_RESILIENCE"

    def evolve(self, domain: DomainSpec) -> DomainSpec:
        """Returns an evolved copy of the domain with escalated edge cases."""
        self.generation_count += 1
        evolved = deepcopy(domain)
        tier = self.get_difficulty_tier()

        # Scale number of injected mutations based on difficulty tier
        num_failures = 1 if "TIER_1" in tier else (2 if "TIER_2" in tier else 3)
        num_enhancers = 1 if "TIER_1" in tier else (2 if "TIER_2" in tier else 3)

        failures = random.sample(FAILURE_MODES, k=num_failures)
        enhancers = random.sample(COMPLEXITY_ENHANCERS, k=num_enhancers)
        safety = random.sample(SAFETY_DIRECTIVES, k=1)

        evolved.description += (
            f" [DIFFICULTY: {tier} | CYCLE #{self.generation_count:04d}] "
            f"[INJECTED EDGE CASES: {'; '.join(failures)}]"
        )
        evolved.physics_principles.extend(enhancers)
        evolved.control_objectives.extend(safety)

        return evolved


evolver = DomainEvolver()
