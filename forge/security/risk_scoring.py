"""Deterministic security risk scoring engine."""

from forge.schemas.security import ImpactLevel, LikelihoodLevel, SeverityLevel


class RiskScoringEngine:
    """
    Deterministic risk calculation based on standard Likelihood x Impact matrix.
    Numeric score on 0.0 - 10.0 scale, mapped deterministically to SeverityLevel.
    """

    LIKELIHOOD_WEIGHTS = {
        LikelihoodLevel.LOW: 1.0,
        LikelihoodLevel.MEDIUM: 2.0,
        LikelihoodLevel.HIGH: 3.0,
    }

    IMPACT_WEIGHTS = {
        ImpactLevel.LOW: 1.0,
        ImpactLevel.MEDIUM: 2.2,
        ImpactLevel.HIGH: 3.33,
    }

    @classmethod
    def calculate_score(
        cls, likelihood: LikelihoodLevel, impact: ImpactLevel
    ) -> tuple[float, SeverityLevel]:
        """
        Calculates deterministic numeric risk score and maps to SeverityLevel.
        Max raw score: 3.0 * 3.33 = 9.99 ~ 10.0
        """
        l_val = cls.LIKELIHOOD_WEIGHTS.get(likelihood, 2.0)
        i_val = cls.IMPACT_WEIGHTS.get(impact, 2.0)
        raw_score = l_val * i_val

        score = min(round(raw_score, 1), 10.0)

        if score >= 8.0:
            severity = SeverityLevel.CRITICAL
        elif score >= 6.0:
            severity = SeverityLevel.HIGH
        elif score >= 3.5:
            severity = SeverityLevel.MEDIUM
        else:
            severity = SeverityLevel.LOW

        return score, severity

    @classmethod
    def calculate_residual_risk(
        cls,
        initial_severity: SeverityLevel,
        mitigation_provided: bool,
        has_verification: bool = True,
    ) -> SeverityLevel:
        """Determines residual risk after applying mitigation."""
        if not mitigation_provided:
            return initial_severity

        # Mitigations reduce severity by 1 to 2 levels depending on verification
        reduction = 2 if has_verification else 1

        levels = [
            SeverityLevel.LOW,
            SeverityLevel.MEDIUM,
            SeverityLevel.HIGH,
            SeverityLevel.CRITICAL,
        ]

        curr_idx = levels.index(initial_severity)
        new_idx = max(0, curr_idx - reduction)
        return levels[new_idx]
