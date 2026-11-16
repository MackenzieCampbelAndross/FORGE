"""Constraint satisfaction analysis engine."""

from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.requirements import RequirementsDoc


class ConstraintAnalyzer:
    """Evaluates whether architectural choices satisfy specified system constraints."""

    @classmethod
    def evaluate_constraints(
        cls,
        req_doc: RequirementsDoc,
        blueprint: ArchitectureBlueprint,
    ) -> tuple[float, list[dict[str, str]], list[dict[str, str]]]:
        """
        Evaluate constraint satisfaction rate.
        Returns:
            - satisfaction_percentage: float (0 - 100.0)
            - satisfied_constraints: list of satisfied constraint records
            - violated_constraints: list of violated constraint records
        """
        if not req_doc.constraints:
            return 100.0, [], []

        mandatory_constraints = [c for c in req_doc.constraints if c.mandatory]
        if not mandatory_constraints:
            return 100.0, [], []

        satisfied: list[dict[str, str]] = []
        violated: list[dict[str, str]] = []

        # Build corpus of architectural decisions
        arch_corpus = " ".join(
            [
                blueprint.title,
                blueprint.overview,
                blueprint.deployment_model.value,
                " ".join(
                    c.name + " " + c.responsibility + " " + c.technology
                    for c in blueprint.components
                ),
                " ".join(t.technology + " " + t.rationale for t in blueprint.technology_choices),
                " ".join(blueprint.requirement_mapping.keys()),
            ]
        ).lower()

        for c in mandatory_constraints:
            desc = c.description.lower()
            words = [w for w in desc.replace(",", " ").replace(".", " ").split() if len(w) > 3]

            # Direct mapping check in requirement_mapping
            is_mapped = c.constraint_id in blueprint.requirement_mapping

            # Keyword heuristic check in architecture context
            matched_words = [w for w in words if w in arch_corpus]
            coverage_ratio = len(matched_words) / len(words) if words else 1.0

            if is_mapped or coverage_ratio >= 0.4:
                satisfied.append(
                    {
                        "constraint_id": c.constraint_id,
                        "category": c.category.value,
                        "description": c.description,
                        "status": "SATISFIED",
                    }
                )
            else:
                violated.append(
                    {
                        "constraint_id": c.constraint_id,
                        "category": c.category.value,
                        "description": c.description,
                        "status": "UNRESOLVED",
                        "reason": "No component or technology choice references or addresses this mandatory constraint.",
                    }
                )

        total_mandatory = len(mandatory_constraints)
        satisfaction_score = (len(satisfied) / total_mandatory) * 100.0

        return round(satisfaction_score, 2), satisfied, violated
