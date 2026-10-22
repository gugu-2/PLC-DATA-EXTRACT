"""
Mock LLM Client for Testing and Dry Runs
Simulates complete, mathematically rigorous IEC 61131-3 Function Blocks
without consuming external API tokens.
"""

import uuid
import time
from typing import Optional
from core.llm_clients.base import BaseLLMClient


MOCK_IEC_BLOCK = """```iec-st
FUNCTION_BLOCK FB_Simulated_CyberPhysical_Benchmark
VAR_INPUT
    rPressure_ChA : REAL; (* [bar] Primary hydraulic pressure *)
    rPressure_ChB : REAL; (* [bar] Redundant channel B *)
    rPressure_ChC : REAL; (* [bar] Redundant channel C *)
    rTemperature : REAL; (* [deg C] Fluid temperature *)
    rFlowRate : REAL; (* [m3/h] Volumetric mass flow *)
    bEmergencyStop : BOOL; (* SIL-3 active low interlock *)
    bManualOverride : BOOL; (* Maintenance mode enable *)
    rSetPoint : REAL; (* Target operating pressure [bar] *)
END_VAR
VAR_OUTPUT
    rControlEffort : REAL; (* Actuator valve position [0..100%] *)
    bAlarmHighHigh : BOOL; (* Critical overpressure trip *)
    bAlarmHigh : BOOL; (* Warning high pressure *)
    bDiscrepancyAlarm : BOOL; (* 2oo3 sensor failure *)
    wStatusWord : WORD; (* State word *)
    rStateEstimate_X1 : REAL; (* Filtered state estimate *)
    bSystemHealthy : BOOL; (* Ready state *)
END_VAR
VAR
    (* Discrete State-Space Matrices *)
    A_11 : REAL := 0.982; A_12 : REAL := 0.015;
    A_21 : REAL := -0.008; A_22 : REAL := 0.975;
    B_11 : REAL := 0.045; B_21 : REAL := 0.120;
    C_11 : REAL := 1.000; C_12 : REAL := 0.000;
    x1_k : REAL := 0.0; x2_k : REAL := 0.0;
    x1_next : REAL; x2_next : REAL;
    u_k : REAL := 0.0;

    (* 2oo3 TMR Voting *)
    rVotedPressure : REAL;
    bChA_Valid : BOOL; bChB_Valid : BOOL; bChC_Valid : BOOL;
    rDiffAB : REAL; rDiffBC : REAL; rDiffCA : REAL;
    tDiscrepancyTimer : TON;

    (* ISA-18.2 Alarms *)
    rLimitHH : REAL := 120.0;
    rLimitH : REAL := 105.0;
    rDeadband : REAL := 2.5;

    (* FSM *)
    nState : INT := 10;
END_VAR

// Phase 1: 2oo3 TMR Voting
rDiffAB := ABS(rPressure_ChA - rPressure_ChB);
rDiffBC := ABS(rPressure_ChB - rPressure_ChC);
rDiffCA := ABS(rPressure_ChC - rPressure_ChA);

IF (rDiffAB < 5.0) AND (rDiffBC < 5.0) THEN
    rVotedPressure := (rPressure_ChA + rPressure_ChB + rPressure_ChC) / 3.0;
    bDiscrepancyAlarm := FALSE;
ELSIF rDiffAB < 5.0 THEN
    rVotedPressure := (rPressure_ChA + rPressure_ChB) / 2.0;
    bDiscrepancyAlarm := TRUE;
ELSIF rDiffBC < 5.0 THEN
    rVotedPressure := (rPressure_ChB + rPressure_ChC) / 2.0;
    bDiscrepancyAlarm := TRUE;
ELSE
    rVotedPressure := rPressure_ChA;
    bDiscrepancyAlarm := TRUE;
END_IF;

// Phase 2: Discrete State-Space Propagation
x1_next := (A_11 * x1_k) + (A_12 * x2_k) + (B_11 * u_k);
x2_next := (A_21 * x1_k) + (A_22 * x2_k) + (B_21 * u_k);
x1_k := x1_next;
x2_k := x2_next;
rStateEstimate_X1 := (C_11 * x1_k) + (C_12 * x2_k);

// Phase 3: Receding-Horizon Control Effort
u_k := (rSetPoint - rVotedPressure) * 1.85;
IF u_k > 100.0 THEN
    u_k := 100.0;
ELSIF u_k < 0.0 THEN
    u_k := 0.0;
END_IF;
rControlEffort := u_k;

// Phase 4: ISA-18.2 Alarms
IF rVotedPressure >= rLimitHH THEN
    bAlarmHighHigh := TRUE;
    bAlarmHigh := TRUE;
ELSIF rVotedPressure >= rLimitH THEN
    bAlarmHigh := TRUE;
    bAlarmHighHigh := FALSE;
ELSIF rVotedPressure < (rLimitH - rDeadband) THEN
    bAlarmHigh := FALSE;
    bAlarmHighHigh := FALSE;
END_IF;

// Phase 5: Finite State Machine
CASE nState OF
    10: (* INITIALIZE *)
        wStatusWord := 16#0001;
        bSystemHealthy := FALSE;
        IF NOT bEmergencyStop THEN
            nState := 20;
        END_IF;
    20: (* RUNNING *)
        wStatusWord := 16#0002;
        bSystemHealthy := TRUE;
        IF bAlarmHighHigh OR bEmergencyStop THEN
            nState := 99;
        END_IF;
    99: (* EMERGENCY TRIP *)
        wStatusWord := 16#00FF;
        rControlEffort := 0.0;
        bSystemHealthy := FALSE;
        IF NOT bEmergencyStop AND NOT bAlarmHighHigh THEN
            nState := 10;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""


class MockClient(BaseLLMClient):
    """Simulated LLM client for rapid local validation and test suites."""

    def __init__(self, model_name: str = "mock-generator"):
        super().__init__(model_name)

    def get_provider_name(self) -> str:
        return "mock"

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 16384
    ) -> str:
        # Inject unique signature to test deduplication and hash uniqueness
        sig = f"// Mock Cycle {uuid.uuid4().hex[:12]} at {time.time()}\n"
        return MOCK_IEC_BLOCK.replace("FUNCTION_BLOCK FB_Simulated_CyberPhysical_Benchmark", f"{sig}FUNCTION_BLOCK FB_Simulated_CyberPhysical_Benchmark")
