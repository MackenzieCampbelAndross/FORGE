"""Comprehensive engineering report generator containing all 20 required sections."""

from forge.intelligence.traceability import TraceabilityEngine
from forge.schemas.report import EngineeringReport, FinalStatus


class ReportGenerator:
    """Generates structured Markdown and JSON reports from an EngineeringReport model."""

    @classmethod
    def generate_markdown(cls, report: EngineeringReport) -> str:
        """Render complete 20-section engineering report in Markdown."""
        t_matrix = TraceabilityEngine.generate_matrix(
            report.requirements,
            report.architecture,
            report.threat_model,
        )

        md = []

        # Header
        md.append("# FORGE ENGINEERING BLUEPRINT REPORT")
        md.append(f"**Report ID:** `{report.report_id}` | **Project ID:** `{report.project_id}`")
        md.append(
            f"**Generated At:** {report.generated_at.isoformat()} | **Status:** **{report.final_status.value}**\n"
        )
        md.append("---\n")

        # 1. Executive Summary
        md.append("## 1. Executive Summary")
        md.append(report.executive_summary.overview)
        md.append(
            f"\n- **Architectural Readiness Score:** {report.executive_summary.readiness_score}/100.0"
        )
        if report.executive_summary.key_decisions:
            md.append("\n**Key Architectural Decisions:**")
            for kd in report.executive_summary.key_decisions:
                md.append(f"- {kd}")
        if report.executive_summary.critical_risks:
            md.append("\n**Critical Identified Risks:**")
            for cr in report.executive_summary.critical_risks:
                md.append(f"- {cr}")
        md.append("\n---\n")

        # 2. Original Objective
        md.append("## 2. Original Objective")
        md.append(f"> {report.objective}\n")
        md.append("---\n")

        # 3. Requirements Analysis
        md.append("## 3. Requirements Analysis")
        md.append(report.requirements.executive_summary)
        if report.requirements.missing_information:
            md.append("\n**Identified Missing Information:**")
            for mi in report.requirements.missing_information:
                md.append(f"- [MISSING] {mi}")
        if report.requirements.ambiguous_requirements:
            md.append("\n**Identified Ambiguities:**")
            for ar in report.requirements.ambiguous_requirements:
                md.append(f"- [AMBIGUITY] {ar}")
        if report.requirements.contradictions:
            md.append("\n**Identified Contradictions:**")
            for ct in report.requirements.contradictions:
                md.append(f"- [CONTRADICTION] {ct}")
        md.append("\n---\n")

        # 4. Functional Requirements
        md.append("## 4. Functional Requirements")
        md.append("| ID | Description | Priority | Source | Acceptance Criteria |")
        md.append("|---|---|---|---|---|")
        for fr in report.requirements.functional_requirements:
            crit = (
                "<br>".join(fr.acceptance_criteria)
                if fr.acceptance_criteria
                else "Standard validation"
            )
            md.append(
                f"| `{fr.requirement_id}` | {fr.description} | {fr.priority.value} | {fr.source.value} | {crit} |"
            )
        md.append("\n---\n")

        # 5. Non-Functional Requirements
        md.append("## 5. Non-Functional Requirements")
        md.append("| ID | Category | Description | Measurable Target | Priority |")
        md.append("|---|---|---|---|---|")
        for nfr in report.requirements.non_functional_requirements:
            md.append(
                f"| `{nfr.requirement_id}` | {nfr.category.value} | {nfr.description} | `{nfr.measurable_target}` | {nfr.priority.value} |"
            )
        md.append("\n---\n")

        # 6. Constraints
        md.append("## 6. Constraints")
        md.append("| ID | Category | Description | Mandatory |")
        md.append("|---|---|---|---|")
        for c in report.requirements.constraints:
            md.append(
                f"| `{c.constraint_id}` | {c.category.value} | {c.description} | {'YES' if c.mandatory else 'NO'} |"
            )
        md.append("\n---\n")

        # 7. Proposed Architecture
        md.append("## 7. Proposed Architecture")
        md.append(f"### {report.architecture.title}")
        md.append(f"**Deployment Model:** `{report.architecture.deployment_model.value}`\n")
        md.append(report.architecture.overview)
        md.append("\n```mermaid")
        md.append("flowchart TD")
        for comp in report.architecture.components:
            md.append(f'    {comp.component_id}["{comp.name}\\n({comp.technology})"]')
        for flow in report.architecture.data_flows:
            md.append(
                f'    {flow.source_component_id} -->|"{flow.protocol}"| {flow.target_component_id}'
            )
        md.append("```\n")
        md.append("---\n")

        # 8. Component Descriptions
        md.append("## 8. Component Descriptions")
        for comp in report.architecture.components:
            md.append(f"### `{comp.component_id}`: {comp.name}")
            md.append(f"- **Technology / Runtime:** `{comp.technology}`")
            md.append(f"- **Primary Responsibility:** {comp.responsibility}")
            deps = ", ".join(f"`{d}`" for d in comp.dependencies) if comp.dependencies else "None"
            md.append(f"- **Dependencies:** {deps}")
            reqs = (
                ", ".join(f"`{r}`" for r in comp.related_requirements)
                if comp.related_requirements
                else "None"
            )
            md.append(f"- **Related Requirements:** {reqs}")
            if comp.interfaces:
                md.append("- **Exposed Interfaces:**")
                for iface in comp.interfaces:
                    md.append(
                        f"  - `{iface.interface_id}`: {iface.name} ({iface.protocol}) - {iface.description}"
                    )
            md.append("")
        md.append("---\n")

        # 9. Technology Decisions
        md.append("## 9. Technology Decisions")
        md.append("| Technology | Category | Rationale | Alternatives Considered | Tradeoffs |")
        md.append("|---|---|---|---|---|")
        for tc in report.architecture.technology_choices:
            alts = ", ".join(tc.alternatives_considered) if tc.alternatives_considered else "None"
            tos = "; ".join(tc.tradeoffs) if tc.tradeoffs else "None"
            md.append(f"| **{tc.technology}** | {tc.category} | {tc.rationale} | {alts} | {tos} |")
        md.append("\n---\n")

        # 10. Architecture Tradeoffs
        md.append("## 10. Architecture Tradeoffs")
        for to in report.architecture.tradeoffs:
            md.append(f"### Dimension: {to.dimension}")
            md.append(f"**Decision:** {to.decision}")
            if to.pros:
                md.append("- **Pros:** " + ", ".join(to.pros))
            if to.cons:
                md.append("- **Cons:** " + ", ".join(to.cons))
            md.append("")
        md.append("---\n")

        # 11. Data Flow
        md.append("## 11. Data Flow")
        md.append("| Flow ID | Source Component | Target Component | Protocol | Description |")
        md.append("|---|---|---|---|---|")
        for df in report.architecture.data_flows:
            md.append(
                f"| `{df.flow_id}` | `{df.source_component_id}` | `{df.target_component_id}` | `{df.protocol}` | {df.description} |"
            )
        md.append("\n---\n")

        # 12. Security Threat Model
        md.append("## 12. Security Threat Model (STRIDE)")
        md.append(f"**Overall Posture:** `{report.threat_model.overall_risk_posture.value}`\n")
        md.append("| Threat ID | Category | Component | Attack Scenario | Severity | Risk Score |")
        md.append("|---|---|---|---|---|---|")
        for t in report.threat_model.threats:
            md.append(
                f"| `{t.threat_id}` | {t.category.value} | `{t.affected_component_id}` | {t.attack_scenario[:60]}... | {t.severity.value} | `{t.risk_score}/10` |"
            )
        md.append("\n---\n")

        # 13. Risk Assessment & Mitigations
        md.append("## 13. Risk Assessment & Mitigations")
        for t in report.threat_model.threats:
            md.append(
                f"### `{t.threat_id}` [{t.category.value}] - Component: `{t.affected_component_id}`"
            )
            md.append(f"- **Attack Scenario:** {t.attack_scenario}")
            md.append(
                f"- **Likelihood / Impact / Severity:** {t.likelihood.value} / {t.impact.value} / **{t.severity.value}** (Score: {t.risk_score}/10)"
            )
            md.append(
                f"- **Mitigation ({t.mitigation.mitigation_id}):** {t.mitigation.description}"
            )
            if t.mitigation.owasp_mapping:
                md.append(f"- **OWASP Alignment:** `{t.mitigation.owasp_mapping}`")
            md.append(f"- **Residual Risk:** `{t.residual_risk.value}`")
            md.append("")
        md.append("---\n")

        # 14. Requirement Traceability Matrix
        md.append("## 14. Requirement Traceability Matrix")
        md.append(f"- **Requirement Coverage:** `{t_matrix.requirement_coverage_pct}%`")
        md.append(f"- **Requirement Traceability:** `{t_matrix.requirement_traceability_pct}%`")
        md.append(f"- **Constraint Satisfaction:** `{t_matrix.constraint_satisfaction_pct}%`\n")
        md.append("| Requirement ID | Type | Mapped Components | Addressed | Traceable |")
        md.append("|---|---|---|---|---|")
        for entry in t_matrix.entries:
            comps = (
                ", ".join(f"`{c}`" for c in entry.mapped_components)
                if entry.mapped_components
                else "None"
            )
            md.append(
                f"| `{entry.requirement_id}` | {entry.requirement_type} | {comps} | {'YES' if entry.is_addressed else 'NO'} | {'YES' if entry.is_traceable else 'NO'} |"
            )
        md.append("\n---\n")

        # 15. Validation Results
        md.append("## 15. Validation Results")
        if report.validation_issues:
            md.append("| Rule ID | Category | Severity | Message |")
            md.append("|---|---|---|---|")
            for vi in report.validation_issues:
                md.append(
                    f"| `{vi.rule_id}` | {vi.category} | **{vi.severity.value}** | {vi.message} |"
                )
        else:
            md.append("✅ All deterministic and architectural checks passed with zero findings.")
        if report.revision_history:
            md.append("\n**Supervisory Revision History:**")
            for rev in report.revision_history:
                md.append(
                    f"- **Iteration {rev.iteration} ({rev.target_agent.value.upper()}):** {rev.reason} -> {rev.requested_correction}"
                )
        md.append("\n---\n")

        # 16. Assumptions
        md.append("## 16. Assumptions")
        for a in report.assumptions:
            md.append(f"- [ASSUMPTION] {a}")
        if not report.assumptions:
            md.append("No explicit assumptions recorded.")
        md.append("\n---\n")

        # 17. Unresolved Issues
        md.append("## 17. Unresolved Issues")
        if report.unresolved_issues:
            for ui in report.unresolved_issues:
                md.append(f"- ⚠️ {ui}")
        else:
            md.append("Zero unresolved issues.")
        md.append("\n---\n")

        # 18. Evidence and References
        md.append("## 18. Evidence and References")
        for ev in report.evidence_notes:
            md.append(f"- {ev}")
        md.append("\n---\n")

        # 19. Confidence Assessment
        md.append("## 19. Confidence Assessment")
        md.append(f"- **Confidence Score:** `{report.confidence_score * 100:.1f}%`")
        md.append(
            f"- **Final Assessment:** {'High confidence based on full deterministic and STRIDE validation.' if report.confidence_score >= 0.8 else 'Moderate/Partial confidence due to unresolved warnings or revision boundaries.'}"
        )
        md.append("\n---\n")

        # 20. Final Status
        md.append("## 20. Final Status")
        status_badge = (
            "🟢 APPROVED"
            if report.final_status == FinalStatus.APPROVED
            else ("🟡 PARTIAL" if report.final_status == FinalStatus.PARTIAL else "🔴 FAILED")
        )
        md.append(f"### {status_badge}")
        md.append(
            f"The engineering blueprint for project `{report.project_id}` has been finalized under status `{report.final_status.value}`."
        )

        return "\n".join(md)
