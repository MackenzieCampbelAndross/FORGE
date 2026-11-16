"""Integration tests for FastAPI REST API endpoints."""

from fastapi.testclient import TestClient

from forge.api.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert "version" in data


def test_projects_crud():
    payload = {
        "name": "E-Commerce Gateway",
        "objective": "Build high-throughput e-commerce payment gateway",
        "domain": "Fintech",
        "context": "Retail enterprise client",
    }
    create_res = client.post("/api/v1/projects", json=payload)
    assert create_res.status_code == 201
    prj_data = create_res.json()
    assert "id" in prj_data
    assert prj_data["name"] == payload["name"]

    get_res = client.get(f"/api/v1/projects/{prj_data['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == prj_data["id"]


def test_analyze_and_retrieve_report():
    analyze_payload = {
        "objective": "Design a real-time event streaming pipeline with Kafka and PostgreSQL",
        "domain": "Distributed Systems",
        "constraints": ["Deploy on Kubernetes", "P95 latency < 100ms"],
    }
    res = client.post("/api/v1/analyze", json=analyze_payload)
    assert res.status_code == 202
    data = res.json()
    assert "analysis_id" in data
    analysis_id = data["analysis_id"]

    # Retrieve status
    status_res = client.get(f"/api/v1/analysis/{analysis_id}")
    assert status_res.status_code == 200
    assert status_res.json()["status"] in ["APPROVED", "PARTIAL", "IN_PROGRESS"]

    # Retrieve report (JSON format)
    rep_res = client.get(f"/api/v1/analysis/{analysis_id}/report?format=json")
    assert rep_res.status_code == 200
    rep_data = rep_res.json()
    assert "report_id" in rep_data
    assert "executive_summary" in rep_data

    # Retrieve report (Markdown format)
    rep_md_res = client.get(f"/api/v1/analysis/{analysis_id}/report?format=markdown")
    assert rep_md_res.status_code == 200
    assert "## 1. Executive Summary" in rep_md_res.text


def test_benchmark_summary_and_evaluation_run():
    summary_res = client.get("/api/v1/benchmark/summary")
    assert summary_res.status_code == 200
    summary_data = summary_res.json()
    assert summary_data["validation"]["total_scenarios"] == 100

    eval_payload = {"limit": 1}
    eval_res = client.post("/api/v1/evaluation/run", json=eval_payload)
    assert eval_res.status_code == 200
    eval_data = eval_res.json()
    assert eval_data["total_scenarios_evaluated"] == 1
