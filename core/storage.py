"""
Atomic Storage and Persistence Layer
Saves validated records atomically to disk with SHA-256 deduplication and index tracking.
"""

import os
import json
import uuid
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from config import config


class DatasetStorage:
    """Manages raw dataset persistence, index cataloging, and deduplication."""

    def __init__(self, save_dir: Optional[Path] = None):
        self.save_dir = Path(save_dir or config.save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.seen_hashes = set()
        self._load_existing_hashes()

    def _load_existing_hashes(self):
        """Scans existing JSON files in save_dir to populate deduplication hashes."""
        for file_path in self.save_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Hash code content
                    content = ""
                    if "messages" in data and len(data["messages"]) > 1:
                        content = data["messages"][1].get("content", "")
                    elif "code" in data:
                        content = data["code"]
                    if content:
                        h = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()
                        self.seen_hashes.add(h)
            except Exception:
                pass

    def compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

    def is_duplicate(self, content: str) -> bool:
        return self.compute_hash(content) in self.seen_hashes

    def save_record(
        self,
        prompt: str,
        code: str,
        domain_id: str,
        domain_name: str,
        function_block_name: str,
        validation_metrics: Dict[str, Any],
        record_id: Optional[str] = None
    ) -> Tuple[Path, str]:
        """
        Atomically saves a record using a temporary file to avoid partial writes.
        """
        code_hash = self.compute_hash(code)
        rec_id = record_id or f"agent_{uuid.uuid4().hex[:8]}"
        final_path = self.save_dir / f"{rec_id}.json"
        temp_path = self.save_dir / f".tmp_{rec_id}.json"

        # Format assistant content in markdown code fence if not already enclosed
        formatted_code = code.strip()
        if not formatted_code.startswith("```"):
            formatted_code = f"```iec-st\n{formatted_code}\n```"

        record_data = {
            "id": rec_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domain_id": domain_id,
            "domain_name": domain_name,
            "function_block_name": function_block_name,
            "char_count": len(code),
            "sha256": code_hash,
            "validation": validation_metrics,
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": formatted_code}
            ]
        }

        # Atomic write: write to .tmp then rename
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(record_data, f, ensure_ascii=False, indent=2)

        temp_path.replace(final_path)
        self.seen_hashes.add(code_hash)

        return final_path, rec_id

    def get_total_records(self) -> int:
        return len(list(self.save_dir.glob("*.json")))

    def list_all_records(self) -> List[Path]:
        return sorted(list(self.save_dir.glob("*.json")))


storage = DatasetStorage()
