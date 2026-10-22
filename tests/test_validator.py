import pytest
from core.validator import validator, IECValidator
from core.repair import repair_engine
from core.llm_clients.mock_client import MOCK_IEC_BLOCK


def test_validator_with_valid_block():
    val = validator.validate(MOCK_IEC_BLOCK)
    assert val.is_valid, f"Expected valid, got errors: {val.errors}"
    assert val.char_count > 1000
    assert val.metrics["has_state_space"] is True
    assert val.metrics["has_voting"] is True
    assert val.metrics["has_alarms"] is True


def test_validator_detects_parity_mismatch():
    broken_code = """
    FUNCTION_BLOCK FB_Broken
    VAR_INPUT
        x : REAL;
    END_VAR
    VAR_OUTPUT
        y : REAL;
    END_VAR
    VAR
        z : REAL;
    END_VAR
    IF x > 10.0 THEN
        y := 20.0;
    (* Missing END_IF *)
    END_FUNCTION_BLOCK
    """
    custom_val = IECValidator(min_char_count=50)
    res = custom_val.validate(broken_code)
    assert not res.is_valid
    assert any("Parity mismatch for IF / END_IF" in err for err in res.errors)


def test_repair_engine_fixes_missing_end_if():
    broken_code = """
    FUNCTION_BLOCK FB_BrokenRepair
    VAR_INPUT
        x : REAL;
    END_VAR
    VAR_OUTPUT
        y : REAL;
    END_VAR
    VAR
        z : REAL;
    END_VAR
    IF x > 10.0 THEN
        y := 20.0;
    END_FUNCTION_BLOCK
    """
    custom_val = IECValidator(min_char_count=50)
    repair_eng = repair_engine.__class__(validator=custom_val)
    repaired = repair_eng.algorithmic_repair(broken_code)
    res = custom_val.validate(repaired)
    assert res.is_valid, f"Repaired code still invalid: {res.errors}"
