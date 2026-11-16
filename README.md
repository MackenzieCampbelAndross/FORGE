# 🔥 FORGE: Multi-Agent AI System for Automated System Design and Engineering Analysis

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/MackenzieCampbelAndross/FORGE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-40%20passed-brightgreen.svg)]()
[![Code%20Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type%20Check](https://img.shields.io/badge/types-mypy%20verified-blue.svg)](http://mypy-lang.org/)

---

## 1. Project Description & Problem Statement

Modern software system design requires rigorous requirement engineering, component boundary decomposition, technology tradeoff assessment, and threat modeling. When performed manually, architecture reviews can be slow, inconsistent, and error-prone. Conversely, naive single-prompt LLMs produce vague, unvalidated prose with broken dependencies, hallucinated components, and missing security mitigations.

**FORGE** is a multi-agent engineering intelligence platform that transforms high-level software objectives into structured, technically defensible, and validated system blueprints. Through specialized Strategy, System Architecture, Security, and Supervisory agents orchestrated via LangGraph, FORGE enforces deterministic integrity checks, requirement traceability matrices, STRIDE threat models, and bounded revision loops.

> **Important:** FORGE is an engineering design, analysis, and validation platform. It is NOT an autonomous coding or deployment agent; its primary deliverable is a validated engineering blueprint.

---

## 2. Core Philosophy

1. **Engineering correctness** over impressive language.
2. **Structured outputs** over unrestricted text.
3. **Traceability** over unsupported recommendations.
4. **Evidence** over fabricated confidence.
5. **Reproducibility** over unverifiable claims.
6. **Measurable performance** over subjective demonstrations.

---

## 3. Architecture & Orchestration

FORGE implements a cyclic, stateful multi-agent architecture powered by **LangGraph**:

```mermaid
flowchart TD
    OBJ["Project Objective<br>(Objective, Domain, Context, Constraints)"] --> STRAT["Strategy Agent<br>(Requirements Extraction & Ambiguity Audit)"]
    STRAT --> REQ_VAL{"Requirement<br>Integrity"}
    
    REQ_VAL -->|Passed| ARCH["System Architect<br>(Topology, DAG, Technologies, Tradeoffs)"]
    REQ_VAL -->|Failed| STRAT_REV["Strategy Revision"]
    STRAT_REV --> STRAT
    
    ARCH --> ARCH_VAL{"Architecture<br>Integrity"}
    ARCH_VAL -->|Passed| SEC["Security Architect<br>(STRIDE Threat Modeling & OWASP Mitigations)"]
    ARCH_VAL -->|Failed| ARCH_REV["Architect Revision"]
    ARCH_REV --> ARCH
    
    SEC --> SEC_VAL{"Security<br>Integrity"}
    SEC_VAL -->|Passed| SUP["Supervisor Agent<br>(Multi-Layer Audit & Traceability Matrix)"]
    SEC_VAL -->|Failed| SEC_REV["Security Revision"]
    SEC_REV --> SEC
    
    SUP --> AUDIT{"Supervisory<br>Quality Audit"}
    AUDIT -->|Blocker Issues Detected| TARGET["Targeted Revision<br>(Strategy / Architect / Security)"]
    TARGET --> SUP
    AUDIT -->|Approved / Budget Exhausted| FINAL["Comprehensive Engineering Report<br>(20 Structured Sections)"]
```

---

## 4. The Four Specialized Agents

| Agent | Role | Primary Responsibility |
|---|---|---|
| **Strategy Agent** | Chief Strategy Officer | Elicits functional and non-functional requirements, classifies mandatory constraints, extracts acceptance criteria, detects logical contradictions, and flags vague claims. |
| **System Architect** | Principal System Architect | Decomposes requirements into component topologies, defines communication interfaces, enforces dependency DAG validity, designs data flows, and structures technology decisions. |
| **Security Architect** | Chief Information Security Officer | Executes STRIDE threat modeling across attack surfaces, calculates deterministic risk scores (0–10 scale), and specifies OWASP-aligned mitigations and residual risks. |
| **Supervisor Agent** | Quality Control & Audit Director | Performs multi-layer static and semantic audits, computes bidirectional requirement traceability matrices, triggers bounded revision loops, and compiles the final 20-section report. |

---

## 5. Technology Stack

- **Core Runtime:** Python 3.11+ / 3.12
- **Agent Orchestration:** LangGraph, LangChain Core
- **Data Validation:** Pydantic v2
- **API Framework:** FastAPI, Uvicorn
- **AI Integration:** Google Gemini API (`google-genai`), deterministic `MockModelProvider`
- **Database & Storage:** PostgreSQL, SQLite, SQLAlchemy 2.0, Alembic
- **Testing & Quality:** Pytest, Ruff, MyPy
- **Evaluation & Benchmarks:** Pandas, NumPy, MLflow
- **Containerization:** Docker, Docker Compose

---

## 6. Installation & Quickstart

### 6.1 Prerequisites
- Python 3.11 or 3.12
- Git

### 6.2 Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/MackenzieCampbelAndross/FORGE.git
cd FORGE

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies in editable mode
pip install -e ".[dev]"
```

### 6.3 Configuration
```bash
cp .env.example .env
# By default, FORGE_MODEL_PROVIDER=mock allows 100% offline, deterministic execution.
# For live Gemini calls, set FORGE_MODEL_PROVIDER=gemini and provide GOOGLE_API_KEY.
```

### 6.4 Initialize Database
```bash
alembic upgrade head
```

---

## 7. Command Line Interface (CLI)

### Run Analysis on an Objective
```bash
python scripts/run_forge.py --objective "Design a real-time event streaming pipeline with Kafka and PostgreSQL"
```

### Run Analysis from an Input JSON
```bash
python scripts/run_forge.py --input examples/healthcare.json --output-dir outputs
```

### Validate Benchmark Dataset (FEB v1.0)
```bash
python scripts/validate_dataset.py
```

### Execute Benchmark Suite
```bash
python scripts/run_benchmark.py --limit 10 --export-json outputs/benchmark.json --export-csv outputs/benchmark.csv
```

### Execute Baseline Comparative Experiments
```bash
python scripts/run_baselines.py --limit 3
```

### Execute Systematic Ablation Studies
```bash
python scripts/run_ablation.py --scenario-id FEB-BACKEND-001
```

---

## 8. REST API

Start the FastAPI application:
```bash
uvicorn forge.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive Documentation:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Primary Endpoints
- `GET /health` — System status and active provider
- `POST /api/v1/projects` — Create project record
- `POST /api/v1/analyze` — Trigger engineering analysis
- `GET /api/v1/analysis/{analysis_id}` — Check status and metrics
- `GET /api/v1/analysis/{analysis_id}/report` — Retrieve report in JSON or Markdown format
- `POST /api/v1/evaluation/run` — Run benchmark evaluation suite
- `GET /api/v1/benchmark/summary` — View FEB dataset statistics

---

## 9. FORGE Engineering Benchmark (FEB) v1.0

The FORGE Engineering Benchmark (FEB) v1.0 consists of **100 standardized scenarios** across 7 categories:
1. **Backend Systems:** 20 scenarios
2. **Distributed Systems:** 15 scenarios
3. **AI and ML Systems:** 15 scenarios
4. **Database Systems:** 15 scenarios
5. **Cloud Infrastructure:** 15 scenarios
6. **Security Critical Systems:** 10 scenarios
7. **General Software Architecture:** 10 scenarios

Total: **100 Scenarios**.

---

## 10. Automated Testing & Verification

All automated tests execute without external API keys:
```bash
# Run test suite
pytest -v

# Run code style & linting
ruff check .
ruff format --check .

# Run strict type checking
python -m mypy forge
```

---

## 11. Documentation Index

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — Comprehensive architectural relationships and diagrams.
- [TECHNICAL_SPECIFICATION.md](docs/TECHNICAL_SPECIFICATION.md) — Schemas, data models, and algorithms.
- [AGENT_DESIGN.md](docs/AGENT_DESIGN.md) — Agent responsibilities and revision loops.
- [BENCHMARK_METHODOLOGY.md](docs/BENCHMARK_METHODOLOGY.md) — FEB dataset construction and scoring.
- [METRICS.md](docs/METRICS.md) — Mathematical definitions for all 25+ metrics.
- [API_REFERENCE.md](docs/API_REFERENCE.md) — Complete REST endpoint documentation.
- [EXPERIMENTS.md](docs/EXPERIMENTS.md) — Baselines and ablation studies.
- [LIMITATIONS.md](docs/LIMITATIONS.md) — System boundaries and scope definitions.
- [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) — Exact steps to reproduce all experiments.

---

## 12. Roadmap

- [x] v1.0.0 — Multi-Agent System Design Engine, FEB 100 Dataset, STRIDE Modeling, Traceability Matrix, FastAPI, SQLite/PostgreSQL persistence.
- [ ] v1.1.0 — Interactive Human-in-the-Loop review pane via WebSockets.
- [ ] v1.2.0 — Multi-cloud cost estimator integration (AWS/GCP/Azure pricing APIs).
- [ ] v1.3.0 — Automated Infrastructure-as-Code (Terraform) blueprint scaffolding export.

---

## 13. License

Apache-2.0 License. Developed by Mackenzie Campbel Andross.
