"""Comprehensive evaluation engine computing scorecards across all metrics."""

from forge.evaluation.metrics import (
    calculate_assumption_transparency,
    calculate_component_completeness,
    calculate_constraint_satisfaction,
    calculate_cost_estimate,
    calculate_decision_traceability,
    calculate_dependency_validity,
    calculate_execution_success_rate,
    calculate_expert_assessed_quality,
    calculate_interface_consistency,
    calculate_latency_metric,
    calculate_mitigation_coverage,
    calculate_requirement_coverage,
    calculate_requirement_traceability,
    calculate_retry_overhead,
    calculate_schema_validity_rate,
    calculate_threat_precision_recall_f1,
    calculate_unsupported_claim_rate,
)
from forge.schemas.evaluation import BenchmarkScenario, EvaluationScorecard, MetricResult
from forge.schemas.report import EngineeringReport, FinalStatus, ValidationIssueSeverity


class ForgeEvaluator:
    """Evaluates an EngineeringReport against benchmark rubrics and produces an EvaluationScorecard."""

    @classmethod
    def evaluate_report(
        cls,
        report: EngineeringReport,
        scenario: BenchmarkScenario | None = None,
        execution_latency: float = 0.0,
        total_tokens: int | None = None,
    ) -> EvaluationScorecard:
        metrics: dict[str, MetricResult] = {}

        req_doc = report.requirements
        arch = report.architecture
        tm = report.threat_model

        # 1. Requirement metrics
        total_reqs = len(req_doc.functional_requirements) + len(req_doc.non_functional_requirements)
        mapped_reqs = set(arch.requirement_mapping.keys())
        for c in arch.components:
            mapped_reqs.update(c.related_requirements)

        metrics["requirement_coverage"] = calculate_requirement_coverage(
            addressed_count=len(mapped_reqs),
            total_requirements=total_reqs,
        )
        metrics["requirement_traceability"] = calculate_requirement_traceability(
            mapped_count=len(mapped_reqs),
            total_requirements=total_reqs,
        )

        mandatory_cons = [c for c in req_doc.constraints if c.mandatory]
        satisfied_cons = [c for c in mandatory_cons if c.constraint_id in mapped_reqs]
        metrics["constraint_satisfaction"] = calculate_constraint_satisfaction(
            satisfied_count=len(satisfied_cons),
            total_mandatory=len(mandatory_cons),
        )

        # 2. Architecture metrics
        expected_comps = (
            len(scenario.expected_components)
            if scenario and scenario.expected_components
            else len(arch.components)
        )
        metrics["component_completeness"] = calculate_component_completeness(
            actual_components=len(arch.components),
            expected_components=expected_comps,
        )

        all_comp_ids = {c.component_id for c in arch.components}
        total_deps = sum(len(c.dependencies) for c in arch.components)
        valid_deps = len([d for c in arch.components for d in c.dependencies if d in all_comp_ids])
        metrics["dependency_validity"] = calculate_dependency_validity(
            valid_dependencies=valid_deps,
            total_dependencies=total_deps,
        )

        total_ifaces = sum(len(c.interfaces) for c in arch.components)
        metrics["interface_consistency"] = calculate_interface_consistency(
            valid_interfaces=total_ifaces,
            total_interfaces=total_ifaces,
        )

        metrics["expert_assessed_architecture_quality"] = calculate_expert_assessed_quality(
            score=None
        )

        # 3. Security metrics
        total_threats = len(tm.threats)
        mitigated_threats = len([
            t for t in tm.threats if t.mitigation and len(t.mitigation.description) > 5
        ])
        metrics["mitigation_coverage"] = calculate_mitigation_coverage(
            threats_with_mitigation=mitigated_threats,
            total_threats=total_threats,
        )

        detected_sec_cats: set[str] = {t.category.value for t in tm.threats}
        expected_sec_cats: set[str] = (
            set(scenario.expected_threat_categories)
            if scenario and scenario.expected_threat_categories
            else detected_sec_cats
        )
        prec, rec, f1 = calculate_threat_precision_recall_f1(detected_sec_cats, expected_sec_cats)
        metrics["threat_precision"] = prec
        metrics["threat_recall"] = rec
        metrics["threat_f1_score"] = f1

        # 4. Reliability metrics
        metrics["schema_validity_rate"] = calculate_schema_validity_rate(1, 1)
        metrics["workflow_execution_success_rate"] = calculate_execution_success_rate(
            successful_runs=1 if report.final_status != FinalStatus.FAILED else 0,
            total_runs=1,
        )
        blockers = [
            i for i in report.validation_issues if i.severity == ValidationIssueSeverity.BLOCKER
        ]
        metrics["unsupported_claim_rate"] = calculate_unsupported_claim_rate(
            unsupported_claims_count=len(blockers),
            total_claims_count=max(1, len(arch.components) + len(arch.technology_choices)),
        )

        # 5. Efficiency metrics
        metrics["end_to_end_latency"] = calculate_latency_metric(execution_latency)
        metrics["retry_overhead"] = calculate_retry_overhead(len(report.revision_history))
        metrics["cost_per_objective"] = calculate_cost_estimate(total_tokens)

        # 6. Evidence metrics
        decisions = arch.technology_choices
        decisions_with_rat = len([d for d in decisions if len(d.rationale) >= 10])
        metrics["decision_traceability"] = calculate_decision_traceability(
            decisions_with_rationale=decisions_with_rat,
            total_decisions=len(decisions),
        )
        metrics["assumption_transparency"] = calculate_assumption_transparency(
            len(report.assumptions)
        )

        # Calculate composite score (weighted average of primary normalized percentages)
        pct_metrics = [
            metrics["requirement_coverage"].value or 0.0,
            metrics["constraint_satisfaction"].value or 0.0,
            metrics["dependency_validity"].value or 0.0,
            metrics["mitigation_coverage"].value or 0.0,
            metrics["threat_f1_score"].value or 0.0,
            metrics["decision_traceability"].value or 0.0,
        ]
        composite = round(sum(pct_metrics) / len(pct_metrics), 2)
        passed = report.final_status == FinalStatus.APPROVED and composite >= 70.0

        summary_notes = [
            f"Evaluated against scenario '{scenario.scenario_id if scenario else 'Ad-hoc'}'",
            f"Final Status: {report.final_status.value}",
            f"Composite Score: {composite}/100.0",
            f"Total revisions during run: {len(report.revision_history)}",
        ]

        return EvaluationScorecard(
            run_id=f"RUN-{report.project_id}",
            scenario_id=scenario.scenario_id if scenario else None,
            metrics=metrics,
            composite_score=composite,
            passed=passed,
            summary_notes=summary_notes,
        )
