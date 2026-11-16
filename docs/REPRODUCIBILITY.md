# FORGE v1.0 — Reproducibility Guide

Follow these exact steps to reproduce all tests, benchmarks, baselines, and ablation studies in FORGE v1.0.

---

## 1. Environment Setup

```bash
# Clone and enter directory
cd FORGE

# Create and activate Python 3.11+ virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies in editable mode with development packages
pip install -e ".[dev]"
```

---

## 2. Configuration

```bash
# Copy environment configuration
cp .env.example .env

# Verify default offline mock provider
# FORGE_MODEL_PROVIDER=mock (Runs full suite without API key)
```

---

## 3. Database Migration

```bash
# Execute Alembic migration to initialize database schema
alembic upgrade head
```

---

## 4. Running Quality Checks & Tests

```bash
# Run Ruff linting and formatting verification
ruff check .
ruff format --check .

# Run MyPy strict type checking
python -m mypy forge

# Run full Pytest automated test suite (40 tests)
pytest -v
```

---

## 5. Running the FEB v1.0 Benchmark Suite

```bash
# Validate dataset integrity (100 scenarios across 7 categories)
python scripts/validate_dataset.py

# Execute benchmark on 10 scenarios
python scripts/run_benchmark.py --limit 10 --export-json outputs/benchmark.json --export-csv outputs/benchmark.csv

# Execute comparative baseline study (Baseline A vs Baseline B vs FORGE v1.0)
python scripts/run_baselines.py --limit 3

# Execute systematic ablation study across 5 configurations
python scripts/run_ablation.py --scenario-id FEB-BACKEND-001
```

---

## 6. Running the API Server

```bash
# Start FastAPI server on port 8000
uvicorn forge.api.main:app --host 0.0.0.0 --port 8000

# Test health check endpoint in browser or terminal:
curl http://localhost:8000/health
```
