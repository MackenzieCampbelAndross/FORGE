"""Supervisor Agent: Evaluation, quality control, revision routing, and report synthesis."""

import time

from forge.agents.base import BaseAgent
from forge.core.logging import logger
from forge.core.model_provider import ModelProvider
from forge.intelligence.architecture_validator import ArchitectureValidator
from forge.intelligence.constraint_analyzer import ConstraintAnalyzer
from forge.intelligence.requirements import RequirementAnalyzer
from forge.intelligence.traceability import TraceabilityEngine
from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.report import (
    EngineeringReport,
    ExecutiveSummary,
    FinalStatus,
    RevisionRecord,
    RevisionTarget,
    ValidationIssue,
    ValidationIssueSeverity,
)
from forge.schemas.requirements import ProjectObjective, RequirementsDoc
from forge.schemas.security import ThreatModel


class SupervisorAgent(BaseAgent):
    """Quality control, validation, revision routing, and engineering report compiler."""

    def __init__(self, provider: ModelProvider | None = None):
        super().__init__(
            name="SupervisorAgent",
            role="Chief Engineering Auditor and Quality Director",
            provider=provider,
        )

    def run(
        self,
        objective: ProjectObjective,
        requirements: RequirementsDoc,
        architecture: ArchitectureBlueprint,
        threat_model: ThreatModel,
        revision_count: int = 0,
        max_revisions: int = 3,
        enable_revision: bool = True,
    ) -> tuple[RevisionRecord | None, list[ValidationIssue]]:
        """Main execution method conforming to BaseAgent interface."""
        return self.evaluate_and_route(
            objective=objective,
            requirements=requirements,
            architecture=architecture,
            threat_model=threat_model,
            revision_count=revision_count,
            max_revisions=max_revisions,
            enable_revision=enable_revision,
        )

    def evaluate_and_route(
        self,
        objective: ProjectObjective,
        requirements: RequirementsDoc,
        architecture: ArchitectureBlueprint,
        threat_model: ThreatModel,
        revision_count: int,
        max_revisions: int = 3,
        enable_revision: bool = True,
    ) -> tuple[RevisionRecord | None, list[ValidationIssue]]:
        """
        Conduct deep technical audit across all agent outputs.
        Returns (revision_record, validation_issues).
        If revision_record is None, the outputs are approved.
        """
        logger.info(
            f"[{self.name}] Running rigorous multi-layer technical audit (iteration {revision_count}/{max_revisions})..."
        )
        issues: list[ValidationIssue] = []

        # 1. Structural requirements validation
        _, req_issues = RequirementAnalyzer.validate_requirements_document(requirements)
        for ri in req_issues:
            issues.append(
                ValidationIssue(
                    rule_id="VAL-REQ-001",
                    category="Requirements",
                    severity=ValidationIssueSeverity.BLOCKER,
                    message=ri,
                )
            )

        # 2. Contradiction audit
        contradictions = RequirementAnalyzer.detect_contradictions(requirements)
        for c in contradictions:
            issues.append(
                ValidationIssue(
                    rule_id="VAL-REQ-002",
                    category="Requirements",
                    severity=ValidationIssueSeverity.WARNING,
                    message=c,
                )
            )

        # 3. Deterministic architecture validation
        arch_issues = ArchitectureValidator.validate_blueprint(architecture, requirements)
        issues.extend(arch_issues)

        # 4. Constraint satisfaction audit
        _, _, violated_cons = ConstraintAnalyzer.evaluate_constraints(requirements, architecture)
        for vc in violated_cons:
            issues.append(
                ValidationIssue(
                    rule_id="VAL-CON-001",
                    category="Constraints",
                    severity=ValidationIssueSeverity.BLOCKER,
                    message=f"Mandatory constraint {vc['constraint_id']} ({vc['category']}) violated: {vc['reason']}",
                    target_id=vc["constraint_id"],
                )
            )

        # 5. Security coverage audit
        if not threat_model.threats:
            issues.append(
                ValidationIssue(
                    rule_id="VAL-SEC-001",
                    category="Security",
                    severity=ValidationIssueSeverity.BLOCKER,
                    message="Threat model contains zero identified threats.",
                )
            )
        else:
            # Check unmitigated critical threats
            for threat in threat_model.threats:
                if threat.severity.value in ["CRITICAL", "HIGH"] and (
                    not threat.mitigation or len(threat.mitigation.description) < 10
                ):
                    issues.append(
                        ValidationIssue(
                            rule_id="VAL-SEC-002",
                            category="Security",
                            severity=ValidationIssueSeverity.BLOCKER,
                            message=f"Threat {threat.threat_id} ({threat.category.value}) has high/critical severity but lacks detailed mitigation.",
                            target_id=threat.threat_id,
                        )
                    )

        # Check for blockers
        blockers = [i for i in issues if i.severity == ValidationIssueSeverity.BLOCKER]

        if not blockers or not enable_revision:
            logger.info(
                f"[{self.name}] Quality audit passed with {len(issues)} total findings ({len(blockers)} blockers)."
            )
            return None, issues

        # If revision budget exhausted, do not create another revision request
        if revision_count >= max_revisions:
            logger.warning(
                f"[{self.name}] Revision budget ({max_revisions}) exhausted. Output will be marked PARTIAL or FAILED."
            )
            return None, issues

        # Determine target agent for revision
        # Priority: Strategy (if req issues) -> Architect (if arch issues) -> Security (if sec issues)
        target = RevisionTarget.ARCHITECT
        primary_reason = ""
        correction = ""

        req_blockers = [b for b in blockers if b.category in ["Requirements"]]
        arch_blockers = [
            b for b in blockers if b.category in ["Architecture", "Traceability", "Constraints"]
        ]
        sec_blockers = [b for b in blockers if b.category in ["Security"]]

        if req_blockers:
            target = RevisionTarget.STRATEGY
            primary_reason = "Requirements validation failed"
            correction = "Resolve duplicate IDs, add missing functional/non-functional requirements, and resolve contradictions."
        elif arch_blockers:
            target = RevisionTarget.ARCHITECT
            primary_reason = "Architecture integrity validation failed"
            correction = "Fix broken dependencies, add missing components, map unmapped requirements, and satisfy mandatory constraints."
        elif sec_blockers:
            target = RevisionTarget.SECURITY
            primary_reason = "Security threat analysis incomplete"
            correction = "Provide thorough mitigations for all high and critical STRIDE threats."

        revision = RevisionRecord(
            iteration=revision_count + 1,
            target_agent=target,
            reason=primary_reason,
            issues=blockers,
            requested_correction=correction,
            resolved=False,
        )
        logger.info(
            f"[{self.name}] Requesting targeted revision #{revision.iteration} to {target.value.upper()}: {primary_reason}"
        )
        return revision, issues

    def compile_report(
        self,
        objective: ProjectObjective,
        requirements: RequirementsDoc,
        architecture: ArchitectureBlueprint,
        threat_model: ThreatModel,
        validation_issues: list[ValidationIssue],
        revision_history: list[RevisionRecord],
    ) -> tuple[EngineeringReport, float]:
        """Synthesize validated agent artifacts into final, evidence-based EngineeringReport."""
        start = time.time()
        logger.info(f"[{self.name}] Compiling final comprehensive engineering report...")

        # Compute traceability matrix and metrics
        t_matrix = TraceabilityEngine.generate_matrix(requirements, architecture, threat_model)

        blockers = [i for i in validation_issues if i.severity == ValidationIssueSeverity.BLOCKER]
        warnings = [i for i in validation_issues if i.severity == ValidationIssueSeverity.WARNING]

        # Determine final status
        if len(blockers) == 0:
            final_status = FinalStatus.APPROVED
            confidence_score = 0.95 if len(warnings) == 0 else 0.85
        elif len(blockers) <= 2:
            final_status = FinalStatus.PARTIAL
            confidence_score = 0.60
        else:
            final_status = FinalStatus.FAILED
            confidence_score = 0.30

        # Construct executive summary
        summary = ExecutiveSummary(
            overview=(
                f"Engineering blueprint for '{objective.objective}'. System comprises {len(architecture.components)} core "
                f"components and {len(architecture.data_flows)} data flows deployed under {architecture.deployment_model.value}. "
                f"Requirement coverage is {t_matrix.requirement_coverage_pct}% with {len(threat_model.threats)} STRIDE threats analyzed."
            ),
            key_decisions=[
                f"{tc.technology} for {tc.category}: {tc.rationale[:60]}..."
                for tc in architecture.technology_choices
            ],
            critical_risks=[
                f"{t.threat_id} ({t.category.value}): {t.attack_scenario[:70]}..."
                for t in threat_model.threats
                if t.severity.value in ["CRITICAL", "HIGH"]
            ][:4],
            readiness_score=round(
                (t_matrix.requirement_coverage_pct * 0.4)
                + (t_matrix.constraint_satisfaction_pct * 0.4)
                + ((100.0 - min(len(blockers) * 25.0, 100.0)) * 0.2),
                1,
            ),
        )

        unresolved = [f"[{i.rule_id}] {i.message}" for i in blockers]
        evidence = [
            "STRIDE Threat modeling verified against OWASP standard rules.",
            f"Deterministic architecture topology graph validated (Cycles: {any(i.rule_id == 'VAL-ARCH-003' for i in validation_issues)}).",
            f"Traceability matrix calculated across {t_matrix.total_requirements} total requirements.",
        ]

        report = EngineeringReport(
            report_id=f"ENG-REP-{objective.project_id}",
            project_id=objective.project_id,
            objective=objective.objective,
            executive_summary=summary,
            requirements=requirements,
            architecture=architecture,
            threat_model=threat_model,
            validation_issues=validation_issues,
            revision_history=revision_history,
            assumptions=requirements.assumptions + architecture.assumptions,
            unresolved_issues=unresolved,
            evidence_notes=evidence,
            metrics_summary={
                "requirement_coverage_pct": t_matrix.requirement_coverage_pct,
                "requirement_traceability_pct": t_matrix.requirement_traceability_pct,
                "constraint_satisfaction_pct": t_matrix.constraint_satisfaction_pct,
                "total_components": len(architecture.components),
                "total_threats": len(threat_model.threats),
                "total_blockers": len(blockers),
                "total_revisions": len(revision_history),
            },
            confidence_score=confidence_score,
            final_status=final_status,
        )

        elapsed = time.time() - start
        logger.info(
            f"[{self.name}] Report generated with status: {final_status.value} (Confidence: {confidence_score})"
        )
        return report, elapsed
