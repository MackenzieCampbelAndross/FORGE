# FORGE v1.0 — Engineering Metrics Reference

Every metric in FORGE is implemented as an independently testable mathematical function with explicit handling for zero denominators.

---

## 1. Requirement Metrics

### 1.1 Requirement Coverage ($C_{req}$)
$$\text{Requirement Coverage (\%)} = \min\left(100.0, \frac{\text{Addressed Requirements}}{\text{Total Requirements}} \times 100\right)$$
- **Zero Denominator:** If $\text{Total Requirements} = 0$, returns $100.0\%$ (vacuously covered).
- **Unit:** Percent (`%`).

### 1.2 Requirement Traceability ($T_{req}$)
$$\text{Requirement Traceability (\%)} = \min\left(100.0, \frac{\text{Traceable Requirements}}{\text{Total Requirements}} \times 100\right)$$
- **Zero Denominator:** If $\text{Total Requirements} = 0$, returns $100.0\%$.
- **Unit:** Percent (`%`).

### 1.3 Constraint Satisfaction ($S_{con}$)
$$\text{Constraint Satisfaction (\%)} = \frac{\text{Satisfied Mandatory Constraints}}{\text{Total Mandatory Constraints}} \times 100$$
- **Zero Denominator:** If $\text{Total Mandatory Constraints} = 0$, returns $100.0\%$.
- **Unit:** Percent (`%`).

---

## 2. Architecture Metrics

### 2.1 Component Completeness ($C_{comp}$)
$$\text{Component Completeness (\%)} = \min\left(100.0, \frac{\text{Actual Components}}{\text{Expected Components}} \times 100\right)$$
- **Unit:** Percent (`%`).

### 2.2 Dependency Validity ($V_{dep}$)
$$\text{Dependency Validity (\%)} = \frac{\text{Valid Existing Dependencies}}{\text{Total Declared Dependencies}} \times 100$$
- **Unit:** Percent (`%`).

### 2.3 Interface Consistency ($C_{iface}$)
$$\text{Interface Consistency (\%)} = \frac{\text{Interfaces with Valid Endpoints}}{\text{Total Declared Interfaces}} \times 100$$
- **Unit:** Percent (`%`).

---

## 3. Security Metrics

### 3.1 Threat Precision, Recall, and F1 Score
$$\text{Precision} = \frac{TP}{TP + FP} \times 100, \quad \text{Recall} = \frac{TP}{TP + FN} \times 100$$
$$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
- Evaluated against canonical STRIDE threat categories.

### 3.2 Mitigation Coverage ($M_{cov}$)
$$\text{Mitigation Coverage (\%)} = \frac{\text{Threats with Valid Mitigation}}{\text{Total Identified Threats}} \times 100$$

---

## 4. Reliability & Efficiency Metrics

- **Schema Validity Rate:** Percentage of agent outputs that validate cleanly against Pydantic schemas.
- **Workflow Execution Success Rate:** Percentage of complete workflow runs concluding without unhandled exceptions.
- **End-to-End Latency:** Wall-clock duration of the complete workflow in seconds.
- **Estimated Cost:** USD inference cost calculated based on token counts.
- **Retry Overhead:** Number of supervisory revision iterations required.
