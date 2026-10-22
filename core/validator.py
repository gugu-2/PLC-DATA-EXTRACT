"""
Rigorous IEC 61131-3 Syntax, Structure & Mathematical Parity Validator
Audits generated Structured Text blocks for industrial compliance, block parity,
variable integrity, and cyber-physical requirements.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    char_count: int = 0
    extracted_code: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)


class IECValidator:
    """Performs deep syntactic and semantic structural auditing of IEC 61131-3 ST."""

    def __init__(self, min_char_count: int = 3500):
        self.min_char_count = min_char_count

    def extract_iec_code(self, raw_text: str) -> str:
        """Extracts Structured Text enclosed in markdown fences, or returns raw if bare."""
        patterns = [
            r"```(?:iec-st|st|pascal|structured-text)?\s*(FUNCTION_BLOCK[\s\S]*?END_FUNCTION_BLOCK)\s*```",
            r"```(?:iec-st|st|pascal|structured-text)?\s*([\s\S]*?)```",
            r"(FUNCTION_BLOCK[\s\S]*?END_FUNCTION_BLOCK)"
        ]
        for pattern in patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return raw_text.strip()

    def count_keywords(self, code: str) -> Dict[str, int]:
        """Counts occurrences of key syntax constructs using word boundaries."""
        # Clean out comments to avoid counting keywords in comments
        clean = re.sub(r"//.*$", "", code, flags=re.MULTILINE)
        clean = re.sub(r"\(\*[\s\S]*?\*\)", "", clean)

        return {
            "IF": len(re.findall(r"\bIF\b", clean, re.IGNORECASE)),
            "END_IF": len(re.findall(r"\bEND_IF\b", clean, re.IGNORECASE)),
            "CASE": len(re.findall(r"\bCASE\b", clean, re.IGNORECASE)),
            "END_CASE": len(re.findall(r"\bEND_CASE\b", clean, re.IGNORECASE)),
            "FOR": len(re.findall(r"\bFOR\b", clean, re.IGNORECASE)),
            "END_FOR": len(re.findall(r"\bEND_FOR\b", clean, re.IGNORECASE)),
            "WHILE": len(re.findall(r"\bWHILE\b", clean, re.IGNORECASE)),
            "END_WHILE": len(re.findall(r"\bEND_WHILE\b", clean, re.IGNORECASE)),
            "FUNCTION_BLOCK": len(re.findall(r"\bFUNCTION_BLOCK\b", clean, re.IGNORECASE)),
            "END_FUNCTION_BLOCK": len(re.findall(r"\bEND_FUNCTION_BLOCK\b", clean, re.IGNORECASE)),
        }

    def validate(self, text: str) -> ValidationResult:
        """Performs full validation check."""
        errors: List[str] = []
        warnings: List[str] = []
        code = self.extract_iec_code(text)
        char_count = len(code)

        # 1. Length check
        if char_count < self.min_char_count:
            errors.append(f"Code length {char_count} chars is below minimum threshold of {self.min_char_count} chars.")

        # 2. Block enclosure check
        if not re.search(r"\bFUNCTION_BLOCK\s+[A-Za-z0-9_]+", code, re.IGNORECASE):
            errors.append("Missing initial 'FUNCTION_BLOCK <Name>' declaration.")

        if not re.search(r"\bEND_FUNCTION_BLOCK\b", code, re.IGNORECASE):
            errors.append("Missing closing 'END_FUNCTION_BLOCK' statement.")

        # 3. Variable sections check
        if not re.search(r"\bVAR_INPUT\b", code, re.IGNORECASE) or not re.search(r"\bEND_VAR\b", code, re.IGNORECASE):
            errors.append("Missing complete 'VAR_INPUT ... END_VAR' declaration block.")

        if not re.search(r"\bVAR_OUTPUT\b", code, re.IGNORECASE):
            errors.append("Missing complete 'VAR_OUTPUT ... END_VAR' declaration block.")

        if not re.search(r"\bVAR\b", code, re.IGNORECASE):
            errors.append("Missing internal 'VAR ... END_VAR' state declaration block.")

        # 4. Parity checks
        counts = self.count_keywords(code)
        if counts["IF"] != counts["END_IF"]:
            errors.append(f"Parity mismatch for IF / END_IF: found {counts['IF']} IF and {counts['END_IF']} END_IF.")

        if counts["CASE"] != counts["END_CASE"]:
            errors.append(f"Parity mismatch for CASE / END_CASE: found {counts['CASE']} CASE and {counts['END_CASE']} END_CASE.")

        if counts["FOR"] != counts["END_FOR"]:
            errors.append(f"Parity mismatch for FOR / END_FOR: found {counts['FOR']} FOR and {counts['END_FOR']} END_FOR.")

        if counts["WHILE"] != counts["END_WHILE"]:
            errors.append(f"Parity mismatch for WHILE / END_WHILE: found {counts['WHILE']} WHILE and {counts['END_WHILE']} END_WHILE.")

        if counts["FUNCTION_BLOCK"] != counts["END_FUNCTION_BLOCK"]:
            errors.append(f"Parity mismatch for FUNCTION_BLOCK: found {counts['FUNCTION_BLOCK']} FUNCTION_BLOCK and {counts['END_FUNCTION_BLOCK']} END_FUNCTION_BLOCK.")

        # 5. Cyber-physical requirements check
        has_state_space = bool(re.search(r"(matrix|state[-_]space|A\[|B\[|C\[|D\[|x_k)", code, re.IGNORECASE))
        has_voting = bool(re.search(r"(2oo3|tmr|voting|discrepancy|channel)", code, re.IGNORECASE))
        has_alarms = bool(re.search(r"(alarm|hh|ll|high_high|trip|deadband)", code, re.IGNORECASE))

        if not has_state_space:
            warnings.append("State-space matrix formulations (A, B, C, D) not explicitly detected.")
        if not has_voting:
            warnings.append("2oo3 TMR voting logic not explicitly detected.")
        if not has_alarms:
            warnings.append("ISA-18.2 multi-tier alarm logic not explicitly detected.")

        metrics = {
            "char_count": char_count,
            "keyword_counts": counts,
            "has_state_space": has_state_space,
            "has_voting": has_voting,
            "has_alarms": has_alarms,
        }

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            char_count=char_count,
            extracted_code=code,
            metrics=metrics
        )


validator = IECValidator()
