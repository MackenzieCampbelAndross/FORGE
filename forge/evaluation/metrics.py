"""Comprehensive engineering metrics framework for FORGE.

Every metric is an independently callable, testable function with explicit
zero-denominator handling and typed MetricResult output.
"""

from forge.schemas.evaluation import MetricResult

# ==============================================================================
# 1. REQUIREMENT METRICS
# ==============================================================================


def calculate_requirement_coverage(
    addressed_count: int,
    total_requirements: int,
) -> MetricResult:
    """
    Mathematical definition:
        Requirement Coverage (%) = (Addressed Requirements / Total Requirements) * 100
    Validity: total_requirements >= 0
    Zero denominator: returns 100.0% if total is 0 (vacuously covered).
    """
    if total_requirements == 0:
        return MetricResult(
            name="requirement_coverage",
            category="Requirement",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
            details={"note": "Total requirements is 0"},
        )
    val = min(100.0, (addressed_count / total_requirements) * 100.0)
    return MetricResult(
        name="requirement_coverage",
        category="Requirement",
        value=round(val, 2),
        unit="percent",
        status="VALID",
        details={"addressed": addressed_count, "total": total_requirements},
    )


def calculate_requirement_traceability(
    mapped_count: int,
    total_requirements: int,
) -> MetricResult:
    """
    Mathematical definition:
        Requirement Traceability (%) = (Requirements with Valid Component Mappings / Total Requirements) * 100
    """
    if total_requirements == 0:
        return MetricResult(
            name="requirement_traceability",
            category="Requirement",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = min(100.0, (mapped_count / total_requirements) * 100.0)
    return MetricResult(
        name="requirement_traceability",
        category="Requirement",
        value=round(val, 2),
        unit="percent",
        status="VALID",
        details={"mapped": mapped_count, "total": total_requirements},
    )


def calculate_constraint_satisfaction(
    satisfied_count: int,
    total_mandatory: int,
) -> MetricResult:
    """
    Mathematical definition:
        Constraint Satisfaction (%) = (Satisfied Mandatory Constraints / Total Mandatory Constraints) * 100
    """
    if total_mandatory == 0:
        return MetricResult(
            name="constraint_satisfaction",
            category="Requirement",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (satisfied_count / total_mandatory) * 100.0
    return MetricResult(
        name="constraint_satisfaction",
        category="Requirement",
        value=round(val, 2),
        unit="percent",
        status="VALID",
        details={"satisfied": satisfied_count, "total_mandatory": total_mandatory},
    )


def calculate_contradiction_precision_recall(
    detected_contradictions: set[str],
    ground_truth_contradictions: set[str],
) -> tuple[MetricResult, MetricResult]:
    """
    Precision = TP / (TP + FP)
    Recall = TP / (TP + FN)
    """
    tp = len(detected_contradictions.intersection(ground_truth_contradictions))
    fp = len(detected_contradictions - ground_truth_contradictions)
    fn = len(ground_truth_contradictions - detected_contradictions)

    precision = (
        (tp / (tp + fp) * 100.0)
        if (tp + fp) > 0
        else (100.0 if not ground_truth_contradictions else 0.0)
    )
    recall = (tp / (tp + fn) * 100.0) if (tp + fn) > 0 else 100.0

    m_prec = MetricResult(
        name="contradiction_detection_precision",
        category="Requirement",
        value=round(precision, 2),
        unit="percent",
        status="VALID" if (tp + fp) > 0 else "ZERO_DENOMINATOR",
        details={"tp": tp, "fp": fp, "fn": fn},
    )
    m_rec = MetricResult(
        name="contradiction_detection_recall",
        category="Requirement",
        value=round(recall, 2),
        unit="percent",
        status="VALID" if (tp + fn) > 0 else "ZERO_DENOMINATOR",
        details={"tp": tp, "fp": fp, "fn": fn},
    )
    return m_prec, m_rec


# ==============================================================================
# 2. ARCHITECTURE METRICS
# ==============================================================================


def calculate_component_completeness(
    actual_components: int,
    expected_components: int,
) -> MetricResult:
    """
    Mathematical definition:
        Component Completeness (%) = min(100.0, (Actual Components / Expected Components) * 100)
    """
    if expected_components == 0:
        return MetricResult(
            name="component_completeness",
            category="Architecture",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = min(100.0, (actual_components / expected_components) * 100.0)
    return MetricResult(
        name="component_completeness",
        category="Architecture",
        value=round(val, 2),
        unit="percent",
        status="VALID",
        details={"actual": actual_components, "expected": expected_components},
    )


def calculate_interface_consistency(
    valid_interfaces: int,
    total_interfaces: int,
) -> MetricResult:
    """
    Mathematical definition:
        Interface Consistency (%) = (Interfaces with valid endpoints / Total interfaces) * 100
    """
    if total_interfaces == 0:
        return MetricResult(
            name="interface_consistency",
            category="Architecture",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (valid_interfaces / total_interfaces) * 100.0
    return MetricResult(
        name="interface_consistency",
        category="Architecture",
        value=round(val, 2),
        unit="percent",
        status="VALID",
        details={"valid": valid_interfaces, "total": total_interfaces},
    )


def calculate_dependency_validity(
    valid_dependencies: int,
    total_dependencies: int,
) -> MetricResult:
    """
    Mathematical definition:
        Dependency Validity (%) = (Dependencies referencing valid existing components / Total dependencies) * 100
    """
    if total_dependencies == 0:
        return MetricResult(
            name="dependency_validity",
            category="Architecture",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (valid_dependencies / total_dependencies) * 100.0
    return MetricResult(
        name="dependency_validity",
        category="Architecture",
        value=round(val, 2),
        unit="percent",
        status="VALID",
        details={"valid": valid_dependencies, "total": total_dependencies},
    )


def calculate_expert_assessed_quality(
    score: float | None = None,
) -> MetricResult:
    """
    Records human expert evaluation (1.0 to 10.0 scale) if available.
    Returns NOT_MEASURED if expert review has not taken place.
    """
    if score is None:
        return MetricResult(
            name="expert_assessed_architecture_quality",
            category="Architecture",
            value=None,
            unit="score_1_to_10",
            status="NOT_MEASURED",
            details={"note": "Expert evaluation has not been conducted for this run"},
        )
    return MetricResult(
        name="expert_assessed_architecture_quality",
        category="Architecture",
        value=score,
        unit="score_1_to_10",
        status="VALID",
    )


# ==============================================================================
# 3. SECURITY METRICS
# ==============================================================================


def calculate_threat_precision_recall_f1(
    detected_threat_categories: set[str],
    ground_truth_threat_categories: set[str],
) -> tuple[MetricResult, MetricResult, MetricResult]:
    """
    Threat classification Precision, Recall, and F1 score against expected STRIDE categories.
    """
    tp = len(detected_threat_categories.intersection(ground_truth_threat_categories))
    fp = len(detected_threat_categories - ground_truth_threat_categories)
    fn = len(ground_truth_threat_categories - detected_threat_categories)

    prec = (tp / (tp + fp) * 100.0) if (tp + fp) > 0 else 100.0
    rec = (tp / (tp + fn) * 100.0) if (tp + fn) > 0 else 100.0
    f1 = (2 * (prec * rec) / (prec + rec)) if (prec + rec) > 0 else 0.0

    m_p = MetricResult(
        name="threat_precision",
        category="Security",
        value=round(prec, 2),
        unit="percent",
        status="VALID",
    )
    m_r = MetricResult(
        name="threat_recall",
        category="Security",
        value=round(rec, 2),
        unit="percent",
        status="VALID",
    )
    m_f = MetricResult(
        name="threat_f1_score",
        category="Security",
        value=round(f1, 2),
        unit="percent",
        status="VALID",
    )
    return m_p, m_r, m_f


def calculate_mitigation_coverage(
    threats_with_mitigation: int,
    total_threats: int,
) -> MetricResult:
    """
    Mitigation Coverage (%) = (Threats with non-empty mitigation / Total threats) * 100
    """
    if total_threats == 0:
        return MetricResult(
            name="mitigation_coverage",
            category="Security",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (threats_with_mitigation / total_threats) * 100.0
    return MetricResult(
        name="mitigation_coverage",
        category="Security",
        value=round(val, 2),
        unit="percent",
        status="VALID",
        details={"mitigated": threats_with_mitigation, "total": total_threats},
    )


def calculate_severity_agreement(
    matching_severity_count: int,
    total_evaluated_threats: int,
) -> MetricResult:
    """Agreement percentage between model severity and deterministic risk engine severity."""
    if total_evaluated_threats == 0:
        return MetricResult(
            name="severity_agreement",
            category="Security",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (matching_severity_count / total_evaluated_threats) * 100.0
    return MetricResult(
        name="severity_agreement",
        category="Security",
        value=round(val, 2),
        unit="percent",
        status="VALID",
    )


# ==============================================================================
# 4. RELIABILITY METRICS
# ==============================================================================


def calculate_schema_validity_rate(
    valid_outputs: int,
    total_outputs: int,
) -> MetricResult:
    """Percentage of agent outputs adhering cleanly to Pydantic schema."""
    if total_outputs == 0:
        return MetricResult(
            name="schema_validity_rate",
            category="Reliability",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (valid_outputs / total_outputs) * 100.0
    return MetricResult(
        name="schema_validity_rate",
        category="Reliability",
        value=round(val, 2),
        unit="percent",
        status="VALID",
    )


def calculate_execution_success_rate(
    successful_runs: int,
    total_runs: int,
) -> MetricResult:
    """Percentage of workflow runs completing without unhandled exception."""
    if total_runs == 0:
        return MetricResult(
            name="workflow_execution_success_rate",
            category="Reliability",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (successful_runs / total_runs) * 100.0
    return MetricResult(
        name="workflow_execution_success_rate",
        category="Reliability",
        value=round(val, 2),
        unit="percent",
        status="VALID",
    )


def calculate_unsupported_claim_rate(
    unsupported_claims_count: int,
    total_claims_count: int,
) -> MetricResult:
    """Percentage of recommendations lacking architectural or technical rationale."""
    if total_claims_count == 0:
        return MetricResult(
            name="unsupported_claim_rate",
            category="Reliability",
            value=0.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (unsupported_claims_count / total_claims_count) * 100.0
    return MetricResult(
        name="unsupported_claim_rate",
        category="Reliability",
        value=round(val, 2),
        unit="percent",
        status="VALID",
    )


# ==============================================================================
# 5. EFFICIENCY METRICS
# ==============================================================================


def calculate_latency_metric(
    duration_seconds: float,
    metric_name: str = "end_to_end_latency",
) -> MetricResult:
    """Measures execution latency in seconds."""
    return MetricResult(
        name=metric_name,
        category="Efficiency",
        value=round(duration_seconds, 3),
        unit="seconds",
        status="VALID",
    )


def calculate_cost_estimate(
    total_tokens: int | None,
    cost_per_million_tokens: float = 0.50,
) -> MetricResult:
    """Estimates inference cost in USD."""
    if total_tokens is None:
        return MetricResult(
            name="cost_per_objective",
            category="Efficiency",
            value=None,
            unit="usd",
            status="NOT_MEASURED",
        )
    cost = (total_tokens / 1_000_000.0) * cost_per_million_tokens
    return MetricResult(
        name="cost_per_objective",
        category="Efficiency",
        value=round(cost, 6),
        unit="usd",
        status="VALID",
        details={"total_tokens": total_tokens},
    )


def calculate_retry_overhead(
    revision_count: int,
) -> MetricResult:
    """Tracks number of supervisory revision cycles required."""
    return MetricResult(
        name="retry_overhead",
        category="Efficiency",
        value=float(revision_count),
        unit="count",
        status="VALID",
    )


# ==============================================================================
# 6. EVIDENCE METRICS
# ==============================================================================


def calculate_decision_traceability(
    decisions_with_rationale: int,
    total_decisions: int,
) -> MetricResult:
    """Percentage of technology/tradeoff decisions backed by explicit rationale."""
    if total_decisions == 0:
        return MetricResult(
            name="decision_traceability",
            category="Evidence",
            value=100.0,
            unit="percent",
            status="ZERO_DENOMINATOR",
        )
    val = (decisions_with_rationale / total_decisions) * 100.0
    return MetricResult(
        name="decision_traceability",
        category="Evidence",
        value=round(val, 2),
        unit="percent",
        status="VALID",
    )


def calculate_assumption_transparency(
    assumptions_count: int,
) -> MetricResult:
    """Measures the explicitness of identified assumptions."""
    return MetricResult(
        name="assumption_transparency",
        category="Evidence",
        value=float(assumptions_count),
        unit="count",
        status="VALID",
    )
