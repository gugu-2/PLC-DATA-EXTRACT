# 🖥️ Local GPU Models (Ollama / vLLM) - Qwen2.5-Coder & DeepSeek-Coder-V2

- **Model Engine**: Qwen2.5-Coder (7B & 14B Q4_K_M / Q3_K_M) & DeepSeek-Coder-V2 (16B Lite Instruct).
- **Execution Mode**: 100% offline local generation on consumer/workstation NVIDIA GPUs (e.g. RTX 4060, 4080, 4090, 5050).
- **Dataset Contents**:
  - `github_direct_v2_1555.jsonl`: 1,555 direct industrial codebase extractions.
  - `github_bulk_v3_verified.jsonl`: 2,186 verified open-source programs.
  - `oscat_library_363.jsonl`: 363 standard OSCAT automation algorithm benchmarks.
  - `siemens_lgf_8.jsonl`: Siemens Library of General Functions standard routines.
- **Performance Profile**:
  - 85–115 tokens/sec generation on local 8GB GDDR7 VRAM.
  - High-throughput offline batch processing without external API limits.
