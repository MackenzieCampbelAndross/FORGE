"""Requirement extraction, contradiction detection, and ambiguity analysis."""

import re

from forge.schemas.requirements import (
    RequirementsDoc,
)


class RequirementAnalyzer:
    """Deterministic analyzer for extracted requirements documents."""

    CONTRADICTION_PATTERNS: list[tuple[re.Pattern, re.Pattern, str]] = [
        (
            re.compile(r"strictly\s+synchronous|synchronous\s+only", re.IGNORECASE),
            re.compile(r"asynchronous\s+event|event-driven", re.IGNORECASE),
            "Contradiction: System specifies synchronous-only communication but also mandates asynchronous event-driven flows.",
        ),
        (
            re.compile(r"zero\s+latency|sub-millisecond", re.IGNORECASE),
            re.compile(
                r"multi-region\s+strong\s+consistency|distributed\s+two-phase\s+commit",
                re.IGNORECASE,
            ),
            "Contradiction: Physics constraint violation: sub-millisecond latency claimed with distributed multi-region two-phase commit.",
        ),
        (
            re.compile(r"stateless\s+only|no\s+state\s+storage", re.IGNORECASE),
            re.compile(r"transactional\s+history|audit\s+log\s+persistence", re.IGNORECASE),
            "Contradiction: Stateless architecture required, but persistence of transactional history is mandated.",
        ),
    ]

    AMBIGUITY_KEYWORDS: list[str] = [
        "fast",
        "scalable",
        "user-friendly",
        "robust",
        "secure",
        "high-performance",
        "modern",
        "flexible",
        "efficient",
        "real-time",
    ]

    @classmethod
    def detect_contradictions(cls, doc: RequirementsDoc) -> list[str]:
        """Detect logical contradictions across requirements and constraints."""
        contradictions = list(doc.contradictions)
        combined_text = " ".join(
            [
                doc.executive_summary,
                " ".join(fr.description for fr in doc.functional_requirements),
                " ".join(nfr.description for nfr in doc.non_functional_requirements),
                " ".join(c.description for c in doc.constraints),
            ]
        )

        for p1, p2, explanation in cls.CONTRADICTION_PATTERNS:
            if p1.search(combined_text) and p2.search(combined_text):
                if explanation not in contradictions:
                    contradictions.append(explanation)

        return contradictions

    @classmethod
    def identify_ambiguities(cls, doc: RequirementsDoc) -> list[str]:
        """Identify unquantified or vague non-functional claims."""
        ambiguities = list(doc.ambiguous_requirements)
        for nfr in doc.non_functional_requirements:
            for kw in cls.AMBIGUITY_KEYWORDS:
                if re.search(rf"\b{kw}\b", nfr.measurable_target, re.IGNORECASE) and not re.search(
                    r"\d", nfr.measurable_target
                ):
                    finding = f"Vague target for {nfr.requirement_id} ({nfr.category.value}): '{nfr.measurable_target}' lacks measurable numeric threshold."
                    if finding not in ambiguities:
                        ambiguities.append(finding)
        return ambiguities

    @classmethod
    def validate_requirements_document(cls, doc: RequirementsDoc) -> tuple[bool, list[str]]:
        """Validate structural integrity of requirements document."""
        issues = []
        if not doc.functional_requirements:
            issues.append("Requirements document contains zero functional requirements.")
        if not doc.non_functional_requirements:
            issues.append("Requirements document contains zero non-functional requirements.")

        # Check unique IDs
        req_ids = set()
        for fr in doc.functional_requirements:
            if fr.requirement_id in req_ids:
                issues.append(f"Duplicate requirement ID: {fr.requirement_id}")
            req_ids.add(fr.requirement_id)

        for nfr in doc.non_functional_requirements:
            if nfr.requirement_id in req_ids:
                issues.append(f"Duplicate requirement ID: {nfr.requirement_id}")
            req_ids.add(nfr.requirement_id)

        return (len(issues) == 0, issues)
