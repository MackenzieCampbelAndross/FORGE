"""Transparent multi-criteria technology evaluation framework."""

from typing import Any

from pydantic import BaseModel, Field


class EvaluationCriteria(BaseModel):
    """Normalized criteria scores (1.0 to 10.0 scale)."""

    functional_suitability: float = Field(default=8.0, ge=1.0, le=10.0)
    performance: float = Field(default=8.0, ge=1.0, le=10.0)
    scalability: float = Field(default=8.0, ge=1.0, le=10.0)
    reliability: float = Field(default=8.0, ge=1.0, le=10.0)
    security: float = Field(default=8.0, ge=1.0, le=10.0)
    operational_simplicity: float = Field(
        default=7.0, ge=1.0, le=10.0
    )  # Inverted complexity (higher is simpler)
    ecosystem_maturity: float = Field(default=8.0, ge=1.0, le=10.0)
    licensing_permissiveness: float = Field(default=9.0, ge=1.0, le=10.0)
    cost_efficiency: float = Field(default=7.0, ge=1.0, le=10.0)


class TechnologyAssessment(BaseModel):
    """Evaluation result for an individual technology choice."""

    technology: str
    category: str
    criteria_scores: EvaluationCriteria
    weighted_score: float
    weights_used: dict[str, float]
    justification: str
    is_heuristic: bool = True


class TechnologyEvaluator:
    """Evaluates candidate technologies using transparent weighted multi-criteria scoring."""

    DEFAULT_WEIGHTS: dict[str, float] = {
        "functional_suitability": 0.20,
        "performance": 0.15,
        "scalability": 0.15,
        "reliability": 0.15,
        "security": 0.15,
        "operational_simplicity": 0.05,
        "ecosystem_maturity": 0.05,
        "licensing_permissiveness": 0.05,
        "cost_efficiency": 0.05,
    }

    # Baseline knowledge database of known technologies
    KNOWLEDGE_BASE: dict[str, dict[str, Any]] = {
        "apache kafka": {
            "functional_suitability": 9.5,
            "performance": 9.5,
            "scalability": 10.0,
            "reliability": 9.0,
            "security": 8.5,
            "operational_simplicity": 5.0,
            "ecosystem_maturity": 9.5,
            "licensing_permissiveness": 10.0,
            "cost_efficiency": 6.5,
            "notes": "Industry standard for distributed event streaming; high operational overhead.",
        },
        "postgresql": {
            "functional_suitability": 9.5,
            "performance": 8.5,
            "scalability": 8.0,
            "reliability": 9.5,
            "security": 9.0,
            "operational_simplicity": 8.0,
            "ecosystem_maturity": 10.0,
            "licensing_permissiveness": 10.0,
            "cost_efficiency": 9.0,
            "notes": "Premier open-source relational database with robust ACID guarantees and extensions.",
        },
        "redis": {
            "functional_suitability": 9.0,
            "performance": 10.0,
            "scalability": 8.5,
            "reliability": 8.5,
            "security": 8.0,
            "operational_simplicity": 8.5,
            "ecosystem_maturity": 9.5,
            "licensing_permissiveness": 8.0,
            "cost_efficiency": 8.5,
            "notes": "Ultra-low latency in-memory data store for caching and pub/sub.",
        },
        "fastapi": {
            "functional_suitability": 9.0,
            "performance": 8.5,
            "scalability": 8.5,
            "reliability": 8.5,
            "security": 8.5,
            "operational_simplicity": 9.0,
            "ecosystem_maturity": 8.5,
            "licensing_permissiveness": 10.0,
            "cost_efficiency": 9.5,
            "notes": "Modern, high-performance async Python web framework with native Pydantic validation.",
        },
    }

    @classmethod
    def evaluate(
        cls,
        technology: str,
        category: str,
        custom_weights: dict[str, float] | None = None,
        custom_scores: dict[str, float] | None = None,
    ) -> TechnologyAssessment:
        weights = custom_weights or cls.DEFAULT_WEIGHTS
        # Ensure weights sum to 1.0
        total_w = sum(weights.values())
        norm_weights = {k: v / total_w for k, v in weights.items()}

        kb_entry = cls.KNOWLEDGE_BASE.get(technology.lower())
        scores_dict: dict[str, float] = {}

        for k in cls.DEFAULT_WEIGHTS.keys():
            if custom_scores and k in custom_scores:
                scores_dict[k] = custom_scores[k]
            elif kb_entry and k in kb_entry:
                scores_dict[k] = float(kb_entry[k])
            else:
                scores_dict[k] = 7.5  # Neutral default for uncatalogued technologies

        criteria = EvaluationCriteria(**scores_dict)

        weighted_sum = sum(getattr(criteria, k) * norm_weights[k] for k in norm_weights.keys())

        justification = (
            kb_entry.get("notes", f"Evaluated under standard multi-criteria model for {category}.")
            if kb_entry
            else f"Heuristic multi-criteria score for {technology} in {category}."
        )

        return TechnologyAssessment(
            technology=technology,
            category=category,
            criteria_scores=criteria,
            weighted_score=round(weighted_sum, 2),
            weights_used=norm_weights,
            justification=justification,
            is_heuristic=True,
        )
