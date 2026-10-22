"""
Multi-Format Training Dataset Exporter
Transforms raw generated records into industry-standard LLM fine-tuning datasets:
- ShareGPT (Axolotl, LLaMA-Factory)
- Alpaca (Instruction / Input / Output)
- OpenAI Fine-Tuning JSONL (ChatML / API Fine-Tuning)
- Raw Combined JSONL
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from config import config
from core.storage import DatasetStorage


class DatasetExporter:
    """Exports raw JSON swarm records into fine-tuning ready artifacts."""

    def __init__(self, storage: Optional[DatasetStorage] = None, exports_dir: Optional[Path] = None):
        self.storage = storage or DatasetStorage()
        self.exports_dir = Path(exports_dir or config.exports_dir)
        self.exports_dir.mkdir(parents=True, exist_ok=True)

    def load_all_raw(self) -> List[Dict[str, Any]]:
        records = []
        for file_path in self.storage.list_all_records():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    records.append(data)
            except Exception:
                pass
        return records

    def export_sharegpt(self, output_name: str = "dataset_sharegpt.json") -> Path:
        """Exports in ShareGPT conversations format."""
        raw_records = self.load_all_raw()
        sharegpt_data = []

        for r in raw_records:
            if "messages" in r and len(r["messages"]) >= 2:
                user_msg = r["messages"][0]["content"]
                asst_msg = r["messages"][1]["content"]
                sharegpt_data.append({
                    "id": r.get("id"),
                    "domain": r.get("domain_name"),
                    "conversations": [
                        {"from": "human", "value": user_msg},
                        {"from": "gpt", "value": asst_msg}
                    ]
                })

        out_path = self.exports_dir / output_name
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(sharegpt_data, f, ensure_ascii=False, indent=2)

        return out_path

    def export_alpaca(self, output_name: str = "dataset_alpaca.json") -> Path:
        """Exports in Stanford Alpaca instruction/input/output format."""
        raw_records = self.load_all_raw()
        alpaca_data = []

        for r in raw_records:
            if "messages" in r and len(r["messages"]) >= 2:
                user_msg = r["messages"][0]["content"]
                asst_msg = r["messages"][1]["content"]
                alpaca_data.append({
                    "instruction": user_msg,
                    "input": "",
                    "output": asst_msg,
                    "system": "You are the Lumina Principal Automation Fellow & Cyber-Physical Systems Chair."
                })

        out_path = self.exports_dir / output_name
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(alpaca_data, f, ensure_ascii=False, indent=2)

        return out_path

    def export_openai_jsonl(self, output_name: str = "dataset_openai.jsonl") -> Path:
        """Exports in OpenAI JSONL format for gpt-4o / fine-tuning."""
        raw_records = self.load_all_raw()
        out_path = self.exports_dir / output_name

        with open(out_path, "w", encoding="utf-8") as f:
            for r in raw_records:
                if "messages" in r and len(r["messages"]) >= 2:
                    entry = {
                        "messages": [
                            {"role": "system", "content": "You are the Lumina Principal Automation Fellow & Cyber-Physical Systems Chair."},
                            {"role": "user", "content": r["messages"][0]["content"]},
                            {"role": "assistant", "content": r["messages"][1]["content"]}
                        ]
                    }
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return out_path

    def export_all(self) -> Dict[str, Path]:
        """Exports in all supported formats simultaneously."""
        return {
            "sharegpt": self.export_sharegpt(),
            "alpaca": self.export_alpaca(),
            "openai_jsonl": self.export_openai_jsonl()
        }


exporter = DatasetExporter()
