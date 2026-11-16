"""Unit tests for independent engineering metrics calculations."""

from forge.evaluation.metrics import (
    calculate_component_completeness,
    calculate_constraint_satisfaction,
    calculate_contradiction_precision_recall,
    calculate_cost_estimate,
    calculate_decision_traceability,
    calculate_dependency_validity,
    calculate_expert_assessed_quality,
    calculate_interface_consistency,
    calculate_latency_metric,
    calculate_mitigation_coverage,
    calculate_requirement_coverage,
    calculate_threat_precision_recall_f1,
)


def test_requirement_coverage_valid_and_zero_denominator():
    # Valid
    m = calculate_requirement_coverage(8, 10)
    assert m.value == 80.0
    assert m.status == "VALID"
    assert m.unit == "percent"

    # Zero denominator
    m_zero = calculate_requirement_coverage(0, 0)
    assert m_zero.value == 100.0
    assert m_zero.status == "ZERO_DENOMINATOR"


def test_constraint_satisfaction():
    m = calculate_constraint_satisfaction(3, 4)
    assert m.value == 75.0

    m_zero = calculate_constraint_satisfaction(0, 0)
    assert m_zero.value == 100.0
    assert m_zero.status == "ZERO_DENOMINATOR"


def test_contradiction_precision_recall():
    detected = {"c1", "c2", "c3"}
    ground_truth = {"c1", "c2", "c4"}

    prec, rec = calculate_contradiction_precision_recall(detected, ground_truth)
    assert prec.value == 66.67  # 2 TP / 3 Detected
    assert rec.value == 66.67  # 2 TP / 3 Expected


def test_architecture_metrics():
    comp = calculate_component_completeness(5, 5)
    assert comp.value == 100.0

    dep = calculate_dependency_validity(4, 5)
    assert dep.value == 80.0

    iface = calculate_interface_consistency(3, 3)
    assert iface.value == 100.0


def test_security_metrics():
    det = {"SPOOFING", "TAMPERING", "DENIAL_OF_SERVICE"}
    exp = {"SPOOFING", "TAMPERING", "ELEVATION_OF_PRIVILEGE"}
    p, r, f1 = calculate_threat_precision_recall_f1(det, exp)
    assert p.value == 66.67
    assert r.value == 66.67
    assert f1.value == 66.67

    mit = calculate_mitigation_coverage(9, 10)
    assert mit.value == 90.0


def test_expert_assessed_quality_not_measured():
    m = calculate_expert_assessed_quality(score=None)
    assert m.value is None
    assert m.status == "NOT_MEASURED"

    m_scored = calculate_expert_assessed_quality(score=8.5)
    assert m_scored.value == 8.5
    assert m_scored.status == "VALID"


def test_efficiency_and_evidence_metrics():
    lat = calculate_latency_metric(1.234)
    assert lat.value == 1.234
    assert lat.unit == "seconds"

    cost = calculate_cost_estimate(total_tokens=1000000, cost_per_million_tokens=0.50)
    assert cost.value == 0.50

    cost_none = calculate_cost_estimate(total_tokens=None)
    assert cost_none.status == "NOT_MEASURED"

    dt = calculate_decision_traceability(5, 5)
    assert dt.value == 100.0
