# FORGE v1.0 — Technical Specification

## 1. Specifications & Schemas

### 1.1 Project Objective Schema
```json
{
  "project_id": "string",
  "objective": "string (min_length=5)",
  "domain": "string (optional)",
  "context": "string (optional)",
  "constraints": ["string"],
  "created_at": "ISO-8601 DateTime"
}
```

### 1.2 Requirements Document Schema
```json
{
  "document_id": "string",
  "project_id": "string",
  "executive_summary": "string",
  "functional_requirements": [
    {
      "requirement_id": "string (e.g. FR-001)",
      "description": "string",
      "priority": "CRITICAL | HIGH | MEDIUM | LOW",
      "acceptance_criteria": ["string"],
      "source": "EXPLICIT | INFERRED | ASSUMPTION | UNKNOWN"
    }
  ],
  "non_functional_requirements": [
    {
      "requirement_id": "string (e.g. NFR-001)",
      "category": "PERFORMANCE | SECURITY | SCALABILITY | RELIABILITY | COMPLIANCE | OPERATIONAL | USABILITY",
      "description": "string",
      "measurable_target": "string",
      "priority": "CRITICAL | HIGH | MEDIUM | LOW",
      "source": "EXPLICIT | INFERRED | ASSUMPTION | UNKNOWN"
    }
  ],
  "constraints": [
    {
      "constraint_id": "string (e.g. CON-001)",
      "category": "REGULATORY | TECHNICAL | BUDGET | TIMELINE | INFRASTRUCTURE",
      "description": "string",
      "mandatory": true,
      "source": "EXPLICIT | INFERRED | ASSUMPTION | UNKNOWN"
    }
  ]
}
```

### 1.3 Architecture Blueprint Schema
```json
{
  "architecture_id": "string",
  "title": "string",
  "overview": "string",
  "deployment_model": "CLOUD_NATIVE | HYBRID | ON_PREMISE | SERVERLESS | EDGE | CONTAINERIZED",
  "components": [
    {
      "component_id": "string (e.g. COMP-001)",
      "name": "string",
      "responsibility": "string",
      "technology": "string",
      "interfaces": [
        {
          "interface_id": "string",
          "name": "string",
          "protocol": "string",
          "description": "string"
        }
      ],
      "dependencies": ["string"],
      "related_requirements": ["string"]
    }
  ],
  "data_flows": [
    {
      "flow_id": "string",
      "source_component_id": "string",
      "target_component_id": "string",
      "protocol": "string",
      "data_payload": "string",
      "description": "string"
    }
  ],
  "technology_choices": [
    {
      "technology": "string",
      "category": "string",
      "rationale": "string",
      "alternatives_considered": ["string"],
      "tradeoffs": ["string"]
    }
  ],
  "requirement_mapping": {
    "FR-001": ["COMP-001", "COMP-002"]
  }
}
```

### 1.4 Threat Model Schema
```json
{
  "threat_model_id": "string",
  "project_id": "string",
  "threats": [
    {
      "threat_id": "string (e.g. THR-001)",
      "category": "SPOOFING | TAMPERING | REPUDIATION | INFORMATION_DISCLOSURE | DENIAL_OF_SERVICE | ELEVATION_OF_PRIVILEGE",
      "affected_component_id": "string",
      "attack_scenario": "string",
      "likelihood": "HIGH | MEDIUM | LOW",
      "impact": "HIGH | MEDIUM | LOW",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "risk_score": 7.5,
      "mitigation": {
        "mitigation_id": "string",
        "description": "string",
        "owasp_mapping": "string",
        "verification_method": "string"
      },
      "residual_risk": "LOW"
    }
  ],
  "attack_surfaces": [
    {
      "surface_id": "string",
      "name": "string",
      "exposure_type": "string",
      "description": "string",
      "protected_by": ["string"]
    }
  ]
}
```

---

## 2. Risk Calculation Algorithm

Risk score $R \in [0.0, 10.0]$ is computed as:
$$R = \min(10.0, L \times I)$$

Where Likelihood weights $L$:
- $\text{LOW} = 1.0$
- $\text{MEDIUM} = 2.0$
- $\text{HIGH} = 3.0$

And Impact weights $I$:
- $\text{LOW} = 1.0$
- $\text{MEDIUM} = 2.2$
- $\text{HIGH} = 3.33$

Mapping to Severity:
- $R \ge 8.0 \implies \text{CRITICAL}$
- $R \ge 6.0 \implies \text{HIGH}$
- $R \ge 3.5 \implies \text{MEDIUM}$
- $R < 3.5 \implies \text{LOW}$
