"""Unit tests for FastAPI embedded static dashboard endpoint."""

from fastapi.testclient import TestClient

from forge.api.main import app

client = TestClient(app)


def test_root_serves_dashboard_html() -> None:
    """Verify GET / returns 200 with static dashboard HTML."""
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "FORGE Engineering Intelligence Platform" in res.text
    assert "Benchmark Scenarios" in res.text
    assert 'href="/docs"' in res.text
    assert 'href="/redoc"' in res.text
    assert 'href="/health"' in res.text


def test_dashboard_alias_endpoint() -> None:
    """Verify GET /dashboard serves the same dashboard HTML."""
    res = client.get("/dashboard")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "Specialized Agents" in res.text
