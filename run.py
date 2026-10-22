"""
Lumina Industrial Synthetic Dataset Swarm - Main CLI Entrypoint
Usage:
  python run.py --agents 8 --backend gemini --model gemini-2.5-pro
  python run.py --agents 6 --backend openai --model gpt-4o
  python run.py --agents 4 --backend ollama --model qwen2.5-coder:14b
  python run.py --dry-run
  python run.py --export
  python run.py --validate-all
"""

import sys
import os
import asyncio
import signal
import argparse
import logging
from pathlib import Path

# Ensure root directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import config
from core.engine import SwarmOrchestrator
from core.storage import storage
from core.exporter import exporter
from core.validator import validator
from core.domains import domain_manager


def setup_logging(verbose: bool = False):
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    level = logging.DEBUG if verbose else logging.INFO
    log_file = config.log_dir / "swarm_engine.log"

    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout) if not verbose else logging.NullHandler()
        ]
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Autonomous Industrial AI Synthetic Dataset Swarm Engine (IEC 61131-3)"
    )
    parser.add_argument(
        "--backend",
        type=str,
        default=config.default_backend,
        choices=["gemini", "openai", "anthropic", "groq", "openrouter", "ollama", "mock"],
        help="LLM provider backend (default: from .env or gemini)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=config.default_model,
        help="Model identifier (default: from .env or gemini-2.5-pro)"
    )
    parser.add_argument(
        "--agents",
        type=int,
        default=config.concurrent_agents,
        help="Number of concurrent sub-agent workers to spawn (default: 8)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Stop after generating this many valid records (default: infinite loop)"
    )
    parser.add_argument(
        "--infinite",
        action="store_true",
        default=config.infinite_loop,
        help="Run continuously in an infinite loop until interrupted"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run simulated dry-run using mock client without API keys"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export all raw JSON records to ShareGPT, Alpaca, and OpenAI JSONL"
    )
    parser.add_argument(
        "--validate-all",
        action="store_true",
        help="Audit and validate all records currently stored in data/raw/"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed debug logging"
    )
    return parser.parse_args()


def run_export():
    print("=" * 60)
    print("📦 EXPORTING FINE-TUNING DATASETS")
    print("=" * 60)
    total = storage.get_total_records()
    print(f"Found {total} raw records in {config.save_dir}")
    if total == 0:
        print("No records found to export. Generate data first!")
        return

    res = exporter.export_all()
    for fmt, pth in res.items():
        print(f"✔ Exported [{fmt}]: {pth}")
    print("Export complete!")


def run_validation_audit():
    print("=" * 60)
    print("🔍 AUDITING ALL STORED RAW RECORDS")
    print("=" * 60)
    records = storage.list_all_records()
    print(f"Auditing {len(records)} records in {config.save_dir}...")
    valid_count = 0
    invalid_count = 0

    for pth in records:
        try:
            import json
            with open(pth, "r", encoding="utf-8") as f:
                data = json.load(f)
            code = data["messages"][1]["content"] if "messages" in data else data.get("code", "")
            res = validator.validate(code)
            if res.is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                print(f"❌ {pth.name}: {res.errors}")
        except Exception as e:
            invalid_count += 1
            print(f"❌ Error reading {pth.name}: {e}")

    print("=" * 60)
    print(f"Audit Summary: {valid_count} Valid | {invalid_count} Invalid | Total: {len(records)}")


def main():
    args = parse_args()
    setup_logging(args.verbose)

    if args.export:
        run_export()
        return

    if args.validate_all:
        run_validation_audit()
        return

    backend = "mock" if args.dry_run else args.backend
    orchestrator = SwarmOrchestrator(
        backend=backend,
        model=args.model,
        num_agents=args.agents,
        infinite=args.infinite and (args.count is None),
        target_count=args.count
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Windows & Unix signal registration
    def sig_handler():
        orchestrator.handle_shutdown()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, sig_handler)
        except NotImplementedError:
            # Windows does not support add_signal_handler on ProactorEventLoop
            pass

    try:
        loop.run_until_complete(orchestrator.run())
    except KeyboardInterrupt:
        orchestrator.handle_shutdown()
        print("\nShutdown complete.")
    finally:
        loop.close()


if __name__ == "__main__":
    main()
