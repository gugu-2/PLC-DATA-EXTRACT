"""
Automated Syntax & Parity Repair Engine
Resolves missing closing statements, unterminated blocks, and structural parity mismatches.
"""

import re
from typing import Optional, Tuple
from core.validator import IECValidator, ValidationResult


class CodeRepairEngine:
    """Provides algorithmic and LLM-assisted repair for malformed Structured Text."""

    def __init__(self, validator: Optional[IECValidator] = None):
        self.validator = validator or IECValidator()

    def algorithmic_repair(self, code: str) -> str:
        """
        Attempts fast, deterministic patch-ups for common LLM generation truncations:
        - Missing END_IF;
        - Missing END_CASE;
        - Missing END_FUNCTION_BLOCK;
        - Missing trailing semicolons.
        """
        repaired = code.rstrip()

        # 1. Ensure END_FUNCTION_BLOCK is present if missing
        if "FUNCTION_BLOCK" in repaired and not re.search(r"\bEND_FUNCTION_BLOCK\b", repaired, re.IGNORECASE):
            repaired += "\nEND_FUNCTION_BLOCK\n"

        # 2. Re-balance IF and END_IF
        counts = self.validator.count_keywords(repaired)
        if counts["IF"] > counts["END_IF"]:
            diff = counts["IF"] - counts["END_IF"]
            # Insert before END_FUNCTION_BLOCK
            idx = repaired.rfind("END_FUNCTION_BLOCK")
            if idx != -1:
                padding = "\n" + ("    END_IF;\n" * diff)
                repaired = repaired[:idx] + padding + repaired[idx:]
            else:
                repaired += ("\nEND_IF;" * diff)

        # 3. Re-balance CASE and END_CASE
        counts = self.validator.count_keywords(repaired)
        if counts["CASE"] > counts["END_CASE"]:
            diff = counts["CASE"] - counts["END_CASE"]
            idx = repaired.rfind("END_FUNCTION_BLOCK")
            if idx != -1:
                padding = "\n" + ("    END_CASE;\n" * diff)
                repaired = repaired[:idx] + padding + repaired[idx:]
            else:
                repaired += ("\nEND_CASE;" * diff)

        # 4. Re-balance FOR and END_FOR
        counts = self.validator.count_keywords(repaired)
        if counts["FOR"] > counts["END_FOR"]:
            diff = counts["FOR"] - counts["END_FOR"]
            idx = repaired.rfind("END_FUNCTION_BLOCK")
            if idx != -1:
                padding = "\n" + ("    END_FOR;\n" * diff)
                repaired = repaired[:idx] + padding + repaired[idx:]
            else:
                repaired += ("\nEND_FOR;" * diff)

        return repaired

    def try_repair(self, raw_text: str) -> Tuple[bool, str, ValidationResult]:
        """
        Validates the text; if invalid, attempts algorithmic repair and re-validates.
        Returns: (is_repaired_and_valid, final_code_or_text, validation_result)
        """
        initial_val = self.validator.validate(raw_text)
        if initial_val.is_valid:
            return True, initial_val.extracted_code, initial_val

        # Attempt algorithmic fix
        fixed_code = self.algorithmic_repair(initial_val.extracted_code)
        fixed_val = self.validator.validate(fixed_code)
        if fixed_val.is_valid:
            return True, fixed_code, fixed_val

        return False, fixed_code, fixed_val


repair_engine = CodeRepairEngine()
