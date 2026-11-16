"""Deterministic architecture validation engine."""

from typing import Any

from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.report import ValidationIssue, ValidationIssueSeverity
from forge.schemas.requirements import RequirementsDoc


class ArchitectureValidator:
    """Deterministic structural and semantic validator for architecture blueprints."""

    KNOWN_INCOMPATIBLE_PAIRS: list[tuple[str, str, str]] = [
        (
            "sqlite",
            "multi-region distributed cluster",
            "SQLite is single-file serverless and cannot function as a distributed multi-region database.",
        ),
        (
            "redis",
            "durable cold archive storage",
            "Redis is primarily an in-memory datastore; not suitable as durable cold archive storage.",
        ),
    ]

    @classmethod
    def validate_blueprint(
        cls,
        blueprint: ArchitectureBlueprint,
        req_doc: RequirementsDoc | None = None,
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []

        # 1. Missing components check
        if not blueprint.components:
            issues.append(
                ValidationIssue(
                    rule_id="VAL-ARCH-001",
                    category="Architecture",
                    severity=ValidationIssueSeverity.BLOCKER,
                    message="Architecture blueprint contains zero components.",
                )
            )
            return issues

        component_map = {c.component_id: c for c in blueprint.components}
        all_comp_ids = set(component_map.keys())

        # 2. Broken dependency references
        for comp in blueprint.components:
            for dep_id in comp.dependencies:
                if dep_id not in all_comp_ids:
                    issues.append(
                        ValidationIssue(
                            rule_id="VAL-ARCH-002",
                            category="Architecture",
                            severity=ValidationIssueSeverity.BLOCKER,
                            message=f"Component '{comp.name}' ({comp.component_id}) references non-existent dependency '{dep_id}'.",
                            target_id=comp.component_id,
                        )
                    )

        # 3. Cyclic dependency detection using DFS
        has_cycle, cycle_path = cls._detect_cycles(component_map)
        if has_cycle:
            issues.append(
                ValidationIssue(
                    rule_id="VAL-ARCH-003",
                    category="Architecture",
                    severity=ValidationIssueSeverity.WARNING,
                    message=f"Cyclic dependency detected among components: {' -> '.join(cycle_path)}.",
                )
            )

        # 4. Data flow endpoint validation
        for flow in blueprint.data_flows:
            if flow.source_component_id not in all_comp_ids:
                issues.append(
                    ValidationIssue(
                        rule_id="VAL-ARCH-004",
                        category="Architecture",
                        severity=ValidationIssueSeverity.BLOCKER,
                        message=f"Data flow '{flow.flow_id}' has invalid source component '{flow.source_component_id}'.",
                        target_id=flow.flow_id,
                    )
                )
            if flow.target_component_id not in all_comp_ids:
                issues.append(
                    ValidationIssue(
                        rule_id="VAL-ARCH-005",
                        category="Architecture",
                        severity=ValidationIssueSeverity.BLOCKER,
                        message=f"Data flow '{flow.flow_id}' has invalid target component '{flow.target_component_id}'.",
                        target_id=flow.flow_id,
                    )
                )

        # 5. Incompatible technology rules
        combined_tech = " ".join(c.technology.lower() for c in blueprint.components)
        for tech1, tech2, reason in cls.KNOWN_INCOMPATIBLE_PAIRS:
            if tech1 in combined_tech and tech2 in combined_tech:
                issues.append(
                    ValidationIssue(
                        rule_id="VAL-ARCH-006",
                        category="Architecture",
                        severity=ValidationIssueSeverity.WARNING,
                        message=f"Incompatible technology combination: {reason}",
                    )
                )

        # 6. Unmapped requirements validation
        if req_doc and req_doc.functional_requirements:
            mapped_reqs: set[str] = set()
            for comp in blueprint.components:
                mapped_reqs.update(comp.related_requirements)
            for r_id in blueprint.requirement_mapping.keys():
                mapped_reqs.add(r_id)

            for fr in req_doc.functional_requirements:
                if fr.requirement_id not in mapped_reqs:
                    issues.append(
                        ValidationIssue(
                            rule_id="VAL-ARCH-007",
                            category="Traceability",
                            severity=ValidationIssueSeverity.BLOCKER,
                            message=f"Functional requirement '{fr.requirement_id}' ({fr.description[:40]}...) is not mapped to any architecture component.",
                            target_id=fr.requirement_id,
                        )
                    )

        return issues

    @classmethod
    def _detect_cycles(cls, component_map: dict[str, Any]) -> tuple[bool, list[str]]:
        visited: set[str] = set()
        rec_stack: set[str] = set()
        path: list[str] = []

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            comp = component_map.get(node)
            if comp:
                for neighbor in comp.dependencies:
                    if neighbor not in visited:
                        if dfs(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        path.append(neighbor)
                        return True

            rec_stack.remove(node)
            path.pop()
            return False

        for node in component_map.keys():
            if node not in visited:
                if dfs(node):
                    return True, path

        return False, []
