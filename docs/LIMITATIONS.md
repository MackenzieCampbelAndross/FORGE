# FORGE v1.0 — Known Limitations & Scope Boundaries

## 1. System Scope

1. **Not an Autonomous Coding Agent:** FORGE v1.0 produces structured, technically defensible engineering blueprints and architecture reports. It does not generate application source code, deploy cloud infrastructure, or commit production software.
2. **Deterministic Validation vs Real-World Execution:** Deterministic validators ensure structural integrity, DAG acyclicity, interface matching, and constraint satisfaction. They do not simulate distributed runtime network latency or cloud outage scenarios.
3. **Model Provider Constraints:** Live Gemini executions depend on upstream API quotas, rate limits, and model behavior. All deterministic benchmarks and tests run offline using `MockModelProvider`.

---

## 2. Benchmark Limitations

1. **Ground Truth Status:** The 100 scenarios in FEB v1.0 are `Programmatically validated`. While strict rubrics and constraint checks are applied, they have not yet been evaluated by a panel of human domain experts.
2. **Cost Estimations:** Token costs are calculated using standard list prices ($0.50 per 1M tokens) and are estimations.
