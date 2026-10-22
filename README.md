# ⚡ Lumina Industrial AI Synthetic Dataset Engine (IEC 61131-3)

An autonomous, multi-agent AI synthetic data generation engine engineered specifically for synthesizing **high-level, mathematically exhaustive, and cyber-physically rigorous IEC 61131-3 Structured Text datasets**.

Repository: **[https://github.com/gugu-2/PLC-DATA-EXTRACT.git](https://github.com/gugu-2/PLC-DATA-EXTRACT.git)**

This repository includes both the **complete standalone swarm generator engine** and the **entire archive of AI-synthesized datasets** accumulated across months of research (over 188 God-Tier raw cyber-physical blocks, 1,634 synthetic evolutions, enterprise seeds, and pre-compiled fine-tuning exports).

---

## 📂 Multi-Tier Classified Dataset Taxonomy

The `data/` directory is organized into classified folders and subfolders by **Task Type**, **Industrial Domain**, and **Fine-Tuning Format**:

```
data/
├── 01_by_task_type/
│   ├── safety_tmr_voting_and_interlocks/    # 2oo3 TMR voting, discrepancy timers, bumpless degradation
│   ├── isa_18_2_alarm_management/           # High-High, High, Low, Low-Low deadbands & alarm latches
│   ├── cyber_physical_state_space_control/  # Discrete state-space (A,B,C,D) & receding-horizon MPC
│   ├── evol_instruct_adversarial_faults/    # 1,634 evolved edge cases (stiction, drift, hammer)
│   ├── industrial_library_benchmarks/       # OSCAT 363 & Siemens LGF 8 industrial algorithms
│   └── domain_troubleshooting_qa/           # Real-world Stack Overflow & control physics dialogues
│
├── 02_by_industrial_domain/
│   ├── advanced_nuclear_and_fusion/         # Tokamak divertor, MSFR fuel circuit, SFR sodium loops
│   ├── aerospace_and_hypersonics/           # Mach 6+ scramjet, eVTOL DEP, rocket TVC gimbals
│   ├── extreme_cryogenics_and_quantum/      # Superfluid He-II 2.17K, 10mK dilution fridges, gravimeters
│   ├── biopharma_and_life_sciences/         # Continuous TFF UF/DF, mRNA LNPs, spin-freeze lyophilizers
│   ├── hydrogen_and_clean_energy/           # 70-bar PEM TSA, green ammonia loops, DAC VTSA contactors
│   └── heavy_metallurgy_and_manufacturing/  # 150-ton AC EAF slag radar, multi-laser PBF, 5-axis DED
│
├── 03_by_format_and_training_splits/
│   ├── sharegpt_format/                     # dataset_sharegpt.json (Axolotl / LLaMA-Factory / Unsloth)
│   ├── alpaca_format/                       # dataset_alpaca.json (Stanford Alpaca format)
│   ├── openai_chatml_jsonl/                 # dataset_openai.jsonl (OpenAI Fine-Tuning API format)
│   └── train_val_splits/                    # Pre-partitioned train.jsonl and val.jsonl
│
├── 04_verified_industry_corpora/
│   ├── github_bulk_verified/                # High-integrity verified open-source industrial code
│   └── direct_industrial_repos/             # 1,555 direct industrial codebase extractions
│
├── 05_by_ai_model_and_api_role/
│   ├── gemini_current_3_8_pro_flash_antigravity_swarm/   # 188 God-Tier raw blocks + ShareGPT/Alpaca/OpenAI formats
│   ├── gemini_pro_1_5_evol_instruct_and_enterprise_v3/   # 1,634 evolved edge cases + enterprise machinery datasets
│   ├── claude_3_5_sonnet_opus_cloud_architect/           # 5,928 verified datasets + master training splits + safety invariants
│   └── local_ollama_qwen_deepseek_edge_models/           # 1,555 direct codebases + OSCAT & Siemens library benchmarks
│
└── raw/                                     # Flat archive of all 188 raw God-Tier JSON records
```

---

## 🌟 Key Features

1. **6 to 8+ Concurrent Sub-Agents**: Spawns multiple asynchronous workers generating synthetic blocks in parallel.
2. **V7 Max-Persona (Principal Automation Fellow & Cyber-Physical Systems Chair)**:
   - Configured for **Extreme Token Consumption** (45,000 to 85,000+ characters per block).
   - Zero placeholders, zero summary comments—every equation is fully elaborated.
3. **Cyber-Physical Systems Depth**:
   - Discrete State-Space Matrices ($A, B, C, D$) propagation ($x_{k+1} = A x_k + B u_k$).
   - Model Predictive Control (MPC) quadratic cost approximation ($Q, R, P$ matrices) with input slew-rate limiting.
   - 2oo3 Triple Modular Redundancy (TMR) sensor voting with discrepancy timers and bumpless degradation.
   - Multi-tier ISA-18.2 alarm management (HH, H, L, LL, deadband hysteresis, trip latches).
   - Multi-stage Finite State Machines (`CASE State OF ... END_CASE`).
4. **100+ Advanced Industrial Domains**:
   - Nuclear & Fusion (Tokamak Divertors, Molten Salt Fast Reactors, Sodium Fast Reactors, Stellarators)
   - Extreme Cryogenics & Quantum (Superfluid He-II Sub-Lambda 2.17K, 10mK Dilution Fridges, Atom Interferometers)
   - Aerospace & Hypersonics (Mach 6+ Scramjets, Autonomous eVTOL DEP Tilt-Wings, Rocket EHA TVC Gimbals)
   - Deep-Sea & Hadal (8,000m Abyssal Coring Heave Compensators, 3,000m Subsea Multiphase Pumps)
   - Biopharmaceutical Downstream (Continuous TFF UF/DF, mRNA LNP Microfluidics, Spin-Freeze Lyophilizers)
   - Clean Energy & Decarbonization (70-Bar PEM TSA Dewatering, Green Ammonia Synthesis, Direct Air Capture VTSA)
   - Heavy Metallurgy & Additive (150-ton AC EAF Radar Foaming Slag, Quad-Laser PBF, Hybrid 5-axis DED)
   - High-Speed Transport (1,000 km/h Maglev LSM, 60-ton Port AGV 4WID/4WIS Steering)
5. **Evol-Instruct Complexity Mutation**: Dynamically injects sensor drifts, fluid hammer, structural resonance, actuator stiction, and cyber-physical fault modes.
6. **Rigorous Validation & Self-Repair**:
   - Exact keyword balance auditing (`IF`/`END_IF`, `CASE`/`END_CASE`, `FUNCTION_BLOCK`/`END_FUNCTION_BLOCK`).
   - Algorithmic patcher automatically rebalances unclosed blocks.
   - SHA-256 deduplication layer ensures zero redundant datasets.
7. **One-Click Export to Fine-Tuning**:
   - ShareGPT (Axolotl / LLaMA-Factory / Unsloth)
   - Stanford Alpaca (`instruction`, `input`, `output`)
   - OpenAI ChatML Fine-Tuning JSONL

---

## 🚀 Quick Setup on Another Computer

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git

### 2. Copy or Clone Project
Transfer the `plc-synthetic-ai-engine` folder to the target machine:
```bash
git clone https://github.com/gugu-2/PLC-LLM-OS.git
cd PLC-LLM-OS/plc-synthetic-ai-engine
```
*(Or simply copy the standalone `plc-synthetic-ai-engine` directory via USB or network)*

### 3. Create Virtual Environment & Install Dependencies
```bash
# On Linux / macOS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Configure API Keys
Copy `.env.example` to `.env`:
```bash
cp .env.example .env     # Linux / macOS
copy .env.example .env   # Windows
```

Edit `.env` and paste your API key:
```ini
DEFAULT_BACKEND=gemini
DEFAULT_MODEL=gemini-2.5-pro

# Set your provider key:
GEMINI_API_KEY=your_gemini_api_key_here
# or OPENAI_API_KEY=your_openai_key
# or ANTHROPIC_API_KEY=your_anthropic_key
# or GROQ_API_KEY=your_groq_key
# or OPENROUTER_API_KEY=your_openrouter_key

CONCURRENT_AGENTS=8
TOKEN_CONSUMPTION_LEVEL=extreme
INFINITE_LOOP=true
```

---

## 💻 Running the Swarm

### Dry-Run Test (No API keys needed)
Verify that all sub-agents, validation pipelines, and storage engines are working:
```bash
python run.py --dry-run --count 3 --agents 3
```

### 1. Google Gemini (Extreme Context & High-Speed Token Consumption)
Spawns 8 parallel sub-agents consuming maximum tokens in an infinite generation loop:
```bash
python run.py --backend gemini --model gemini-2.5-pro --agents 8 --infinite
```

### 2. OpenAI GPT-4o / o1 / o3-mini
```bash
python run.py --backend openai --model gpt-4o --agents 6 --infinite
```

### 3. Anthropic Claude 3.5 Sonnet
```bash
python run.py --backend anthropic --model claude-3-5-sonnet-20241022 --agents 6 --infinite
```

### 4. Groq / DeepSeek-R1 (Ultra-Fast Cloud Inference)
```bash
python run.py --backend groq --model deepseek-r1-distill-llama-70b --agents 6
```

### 5. 100% Offline Generation with Local GPU (Ollama / vLLM)
If the computer has an NVIDIA GPU (e.g. RTX 3090, 4080, 4090, A6000, Mac Studio):
```bash
# 1. Start Ollama and pull your code model
ollama pull qwen2.5-coder:14b

# 2. Run the swarm pointing to local Ollama
python run.py --backend ollama --model qwen2.5-coder:14b --agents 4 --infinite
```

---

## 📊 Live Terminal Dashboard

When running, the engine displays a real-time status matrix:

```
[LUMINA INDUSTRIAL AI SWARM METRICS]
┌────────────────────────────┬───────────────────────────────────────┐
│ Metric                     │ Value                                 │
├────────────────────────────┼───────────────────────────────────────┤
│ Elapsed Time               │ 1h 24m 12s                            │
│ Total Valid Records        │ 48                                    │
│ Auto-Repaired Records      │ 3                                     │
│ Failed / Rejected          │ 0                                     │
│ Total Characters Generated │ 3,124,580 chars                       │
│ Estimated Tokens Consumed  │ 822,257 tokens                        │
│ Throughput Speed           │ 34.2 records/hr (37,197 chars/sec)    │
└────────────────────────────┴───────────────────────────────────────┘

[ACTIVE SUB-AGENTS (8 CONCURRENT WORKERS)]
┌──────────┬───────────────────┬───────────────────────────────────────────┬───────────┐
│ Agent    │ Status            │ Assigned Domain                           │ Completed │
├──────────┼───────────────────┼───────────────────────────────────────────┼───────────┤
│ Agent #01│ LLM_SYNTHESIS     │ Tokamak Tungsten Divertor Plasma Regime   │ 6         │
│ Agent #02│ VALIDATING_SYNTAX │ Continuous Biopharma Downstream TFF       │ 6         │
│ Agent #03│ LLM_SYNTHESIS     │ 8,000m Abyssal Coring Heave Compensator   │ 6         │
│ Agent #04│ AUTO_REPAIRING    │ Superfluid Helium-II Sub-Lambda 2.17K     │ 6         │
│ Agent #05│ LLM_SYNTHESIS     │ 150-Ton AC EAF Microwave Foaming Slag     │ 6         │
│ Agent #06│ ATOMIC_SAVING     │ Mach 6+ Scramjet Shock Train Positioner   │ 6         │
│ Agent #07│ LLM_SYNTHESIS     │ 70-Bar PEM High-Pressure TSA Dewatering   │ 6         │
│ Agent #08│ LLM_SYNTHESIS     │ 1,000 km/h Maglev LSM Stator Vector Sync  │ 6         │
└──────────┴───────────────────┴───────────────────────────────────────────┴───────────┘
```

---

## 📦 Exporting & Fine-Tuning

### Export Datasets
At any time (even while the swarm is running or after stopping it with `Ctrl+C`):
```bash
python run.py --export
```
This automatically produces 3 ready-to-train datasets in `data/exports/`:
- `data/exports/dataset_sharegpt.json` (for Axolotl, LLaMA-Factory, Unsloth)
- `data/exports/dataset_alpaca.json` (for Stanford Alpaca training)
- `data/exports/dataset_openai.jsonl` (for OpenAI Fine-Tuning API)

### Audit Existing Stored Records
```bash
python run.py --validate-all
```

---

## 🏗️ Architecture

```
plc-synthetic-ai-engine/
├── run.py                 # CLI Launcher & Swarm Loop Runner
├── config.py              # Environment configuration & Settings
├── requirements.txt       # Production dependencies
├── .env.example           # Environment template
├── core/
│   ├── domains.py         # 100+ High-Complexity Industrial Cyber-Physical Domains
│   ├── personas.py        # V7 Max-Persona Extreme Token Consumption Prompts
│   ├── evolver.py         # Evol-Instruct Edge-Case Mutation Engine
│   ├── validator.py       # IEC 61131-3 Syntax, AST & Parity Validator
│   ├── repair.py          # Deterministic Algorithmic & LLM Auto-Repair
│   ├── storage.py         # Atomic JSON persistence & SHA-256 deduplication
│   ├── exporter.py        # ShareGPT, Alpaca & OpenAI JSONL exporters
│   ├── telemetry.py       # Rich terminal dashboard & performance tracking
│   ├── worker.py          # Sub-Agent worker lifecycle
│   ├── engine.py          # Swarm Orchestrator (Multi-agent coordination)
│   └── llm_clients/
│       ├── base.py        # Abstract Base Async LLM Client
│       ├── gemini_client.py   # Google Gemini API
│       ├── openai_client.py   # OpenAI / Groq / OpenRouter / DeepSeek API
│       ├── anthropic_client.py# Anthropic Claude API
│       ├── ollama_client.py   # Local Ollama / vLLM API
│       └── mock_client.py     # Local Dry-Run Simulator
└── tests/
    ├── test_domains.py    # Domain catalog tests
    ├── test_validator.py  # Parity & syntax tests
    ├── test_storage.py    # Atomic save & deduplication tests
    └── test_client.py     # LLM Client integration tests
```

---

## 🛡️ License & Attribution
Part of the Lumina Industrial Cyber-Physical Automation Research Initiative.
Licensed under Apache 2.0.
