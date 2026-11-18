"""Integration tests for API concurrency and negative boundary cases."""

from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from forge.api.main import app

client = TestClient(app)


def test_concurrent_analysis_requests() -> None:
    """Verify multiple simultaneous analysis requests execute without race conditions."""
    def send_request(idx: int) -> int:
        payload = {
            "objective": f"Concurrent task {idx}: Build scalable distributed message queue",
            "domain": "Distributed Systems",
            "constraints": [f"Cluster {idx} partition tolerance"],
        }
        res = client.post("/api/v1/analyze", json=payload)
        return res.status_code

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(send_request, i) for i in range(4)]
        results = [f.result() for f in futures]

    assert all(code == 202 for code in results)


def test_get_nonexistent_project_returns_404() -> None:
    """Verify querying non-existent project returns 404."""
    res = client.get("/api/v1/projects/non-existent-proj-id-9999")
    assert res.status_code == 404


def test_get_nonexistent_analysis_returns_404() -> None:
    """Verify querying non-existent analysis execution returns 404."""
    res = client.get("/api/v1/analysis/non-existent-analysis-id-9999")
    assert res.status_code == 404


def test_get_report_invalid_format_returns_422() -> None:
    """Verify requesting an unsupported report format returns 422 validation error."""
    # First create an analysis
    payload = {
        "objective": "Build event driven system",
        "domain": "Backend Systems",
    }
    create_res = client.post("/api/v1/analyze", json=payload)
    assert create_res.status_code == 202
    analysis_id = create_res.json()["analysis_id"]

    res = client.get(f"/api/v1/analysis/{analysis_id}/report?format=unsupported_format")
    assert res.status_code == 422


def test_create_project_empty_payload_validation() -> None:
    """Verify empty or missing fields trigger 422 Unprocessable Entity."""
    res = client.post("/api/v1/projects", json={})
    assert res.status_code == 422
