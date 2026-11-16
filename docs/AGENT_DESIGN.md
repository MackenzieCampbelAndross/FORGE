# FORGE v1.0 — Agent Design & Communication Protocol

## 1. Agent Design Principles

Every agent in FORGE inherits from `BaseAgent` and interacts through structured typed schemas via LangGraph state passing.

1. **Schema Integrity:** Every agent must output structured, schema-validated Pydantic models. Malformed or hallucinated responses trigger immediate validation errors.
2. **Specialization:** Agents have distinct, non-overlapping roles.
3. **Traceability:** Requirements and architectural choices must be linked explicitly.
4. **Revisability:** Agents must accept targeted feedback from the Supervisor Agent during revision cycles.

---

## 2. Agent Responsibilities

### Agent 1: Strategy Agent (`StrategyAgent`)
- **Role:** Chief Strategy Officer and Principal Requirements Engineer.
- **Input:** `ProjectObjective`.
- **Output:** `RequirementsDoc`.
- **Key Functions:**
  - Extracts atomic functional requirements (`FR-xxx`) with acceptance criteria.
  - Formulates non-functional requirements (`NFR-xxx`) with quantitative thresholds.
  - Classifies constraints (`CON-xxx`) as mandatory or optional.
  - Distinguishes explicit facts from inferred hypotheses and assumptions.
  - Detects contradictions and flags ambiguities.

### Agent 2: System Architect (`ArchitectAgent`)
- **Role:** Principal System Architect and Distributed Systems Engineer.
- **Input:** `RequirementsDoc`.
- **Output:** `ArchitectureBlueprint`.
- **Key Functions:**
  - Decomposes requirements into cohesive components (`COMP-xxx`).
  - Defines exposed communication interfaces (`INT-xxx`) and protocols.
  - Enforces dependency acyclicity (DAG verification).
  - Specifies component-to-component data flows (`FLOW-xxx`).
  - Selects technologies with alternatives and trade-offs.
  - Maps every requirement directly to components.

### Agent 3: Security Architect (`SecurityAgent`)
- **Role:** Chief Information Security Officer and Principal Threat Modeler.
- **Input:** `ArchitectureBlueprint`.
- **Output:** `ThreatModel`.
- **Key Functions:**
  - Performs STRIDE classification across components and interfaces.
  - Assigns likelihood and impact to attack scenarios.
  - Computes deterministic risk scores.
  - Proposes concrete mitigations mapped to OWASP guidance.
  - Evaluates residual risk post-mitigation.

### Agent 4: Supervisor Agent (`SupervisorAgent`)
- **Role:** Chief Engineering Auditor and Quality Director.
- **Input:** `ProjectObjective`, `RequirementsDoc`, `ArchitectureBlueprint`, `ThreatModel`.
- **Output:** `RevisionRecord` (if rejected) or `EngineeringReport` (if approved/exhausted).
- **Key Functions:**
  - Conducts multi-layer technical audits:
    - Requirement completeness and contradiction audit.
    - Component dependency validity and cycle detection.
    - Constraint satisfaction evaluation.
    - Security coverage and critical threat mitigation audit.
  - Generates targeted revision instructions directed to the responsible agent.
  - Enforces bounded revision loops ($\le \text{max\_revisions}$).
  - Compiles comprehensive, evidence-based 20-section Engineering Report.
