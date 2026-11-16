# FORGE v1.0 — Experiments, Baselines & Ablation Studies

## 1. Experimental Methodology

FORGE provides reproducible comparison harnesses across standard baseline configurations and systematic ablation variants.

### 1.1 Baseline Architectures
1. **BASELINE A (Single LLM):** A single monolithic prompt attempting to generate the full architecture and threat analysis in one turn without agent specialization or validation.
2. **BASELINE B (Sequential 4-Agent without Revision):** Sequential execution of Strategy, Architect, Security, and Supervisor without supervisory validation loops or rejection feedback.
3. **FORGE v1.0 (Full Multi-Agent Orchestration):** Full pipeline incorporating deterministic validators, STRIDE modeling, requirement traceability, and bounded supervisory revision loops.

### 1.2 Systematic Ablation Studies
Five modular ablation variants measure component contributions:
- `no_supervisor_revision`: Disables supervisor rejection loops (runs sequentially).
- `no_security_agent`: Omits the Security Architect; demonstrates supervisor detection of missing threat models.
- `no_requirement_traceability`: Bypasses bidirectional requirement-to-component mapping.
- `no_architecture_validation`: Disables static DAG cycle detection and dependency integrity checks.
- `no_structured_output_validation`: Disables schema contract validation.

---

## 2. Reproduction Commands

### 2.1 Running Baselines
```bash
python scripts/run_baselines.py --limit 5
```

### 2.2 Running Systematic Ablations
```bash
python scripts/run_ablation.py --scenario-id FEB-BACKEND-001
```

### 2.3 Running the Full FEB v1.0 Benchmark Suite
```bash
python scripts/run_benchmark.py --limit 20 --export-json outputs/benchmark.json --export-csv outputs/benchmark.csv
```

### 2.4 Tracking Experiments with MLflow
All runs are logged to `./mlruns`. Launch the MLflow UI:
```bash
mlflow ui --backend-store-uri ./mlruns
```
