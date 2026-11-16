# FORGE v1.0 — API Reference

Base URL: `http://localhost:8000`

Interactive OpenAPI Documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 1. Health & Status

### `GET /health`
Returns system health, active environment, and configured provider.

**Response (200 OK):**
```json
{
  "status": "HEALTHY",
  "service": "FORGE Engineering Intelligence Platform",
  "version": "1.0.0",
  "environment": "development",
  "provider": "mock"
}
```

---

## 2. Project Management

### `POST /api/v1/projects`
Creates a new engineering design project.

**Request Body:**
```json
{
  "name": "Cloud Native EHR Platform",
  "objective": "Build a scalable healthcare data exchange platform processing FHIR clinical records.",
  "domain": "Healthcare Systems",
  "context": "Serving 500,000 patients."
}
```

**Response (201 Created):**
```json
{
  "id": "PRJ-B34F12A0",
  "name": "Cloud Native EHR Platform",
  "domain": "Healthcare Systems",
  "objective": "Build a scalable healthcare data exchange platform processing FHIR clinical records.",
  "context": "Serving 500,000 patients.",
  "created_at": "2026-11-17T01:00:00+00:00"
}
```

### `GET /api/v1/projects/{project_id}`
Retrieves existing project by identifier.

---

## 3. Engineering Analysis

### `POST /api/v1/analyze`
Triggers an end-to-end multi-agent system design workflow.

**Request Body:**
```json
{
  "project_id": "PRJ-B34F12A0",
  "objective": "Build an immutable distributed double-entry financial ledger.",
  "domain": "Fintech",
  "constraints": ["Zero discrepancy balance reconciliation", "PCI-DSS Level 1"],
  "max_revisions": 3
}
```

**Response (202 Accepted):**
```json
{
  "analysis_id": "ANL-98A12F3D",
  "project_id": "PRJ-B34F12A0",
  "status": "APPROVED",
  "message": "Analysis completed successfully under status APPROVED."
}
```

### `GET /api/v1/analysis/{analysis_id}`
Retrieves execution status, latency, revision count, and errors.

### `GET /api/v1/analysis/{analysis_id}/report?format=json`
Retrieves the complete validated engineering report in JSON.

### `GET /api/v1/analysis/{analysis_id}/report?format=markdown`
Retrieves the complete 20-section report in rendered Markdown (`text/markdown`).

---

## 4. Evaluation and Benchmark

### `POST /api/v1/evaluation/run`
Executes benchmark evaluations across FEB scenarios.

**Request Body:**
```json
{
  "category": "Backend systems",
  "limit": 5
}
```

### `GET /api/v1/benchmark/summary`
Returns verification statistics and category distributions of the FEB dataset.
