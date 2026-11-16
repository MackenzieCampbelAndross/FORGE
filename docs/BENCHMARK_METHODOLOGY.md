# FORGE Engineering Benchmark (FEB) v1.0 — Methodology

## 1. Dataset Construction

The FORGE Engineering Benchmark (FEB) v1.0 comprises **100 standardized software engineering scenarios** designed to evaluate multi-agent reasoning, architectural synthesis, and threat modeling across distinct software engineering domains.

### 1.1 Category Distribution (100 Scenarios)
1. **Backend Systems:** 20 scenarios (`FEB-BACKEND-001` to `FEB-BACKEND-020`)
2. **Distributed Systems:** 15 scenarios (`FEB-DISTRIB-001` to `FEB-DISTRIB-015`)
3. **AI and ML Systems:** 15 scenarios (`FEB-AIML-001` to `FEB-AIML-015`)
4. **Database Systems:** 15 scenarios (`FEB-DB-001` to `FEB-DB-015`)
5. **Cloud Infrastructure:** 15 scenarios (`FEB-CLOUD-001` to `FEB-CLOUD-015`)
6. **Security Critical Systems:** 10 scenarios (`FEB-SEC-001` to `FEB-SEC-010`)
7. **General Software Architecture:** 10 scenarios (`FEB-GEN-001` to `FEB-GEN-010`)

Total: **100 Scenarios**.

---

## 2. Dataset Integrity & Ground Truth Labeling

To ensure scientific honesty and prevent benchmark contamination:
- No synthetic LLM output is ever represented as expert human review.
- Every scenario carries a validated `ground_truth_status`:
  - `Draft`: Initial drafted scenario specification.
  - `Programmatically validated`: Schema-verified, constraint-checked, and cross-referenced programmatically.
  - `Expert reviewed`: Formally audited and signed off by a human principal engineer.
- All 100 current FEB v1.0 scenarios are **Programmatically validated**.

---

## 3. Evaluation Procedure

Each scenario execution evaluates:
1. **Requirement Extraction:** Precision and recall against expected functional and non-functional requirements.
2. **Architecture Integrity:** Valid components, interface consistency, dependency validity, and absence of broken references.
3. **STRIDE Threat Modeling:** Precision and recall against expected STRIDE attack vectors.
4. **Traceability:** Completeness of requirement-to-component mappings.
5. **Composite Score:** Weighted aggregate of normalized metrics according to the domain rubric.
