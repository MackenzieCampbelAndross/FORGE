"""Aggregation and summary scoring across multiple evaluation runs."""

from typing import Any

import pandas as pd

from forge.schemas.evaluation import EvaluationScorecard


class ScorecardAggregator:
    """Aggregates scorecards across multiple scenarios or benchmark iterations."""

    @classmethod
    def aggregate(cls, scorecards: list[EvaluationScorecard]) -> dict[str, Any]:
        """Aggregate metric distributions using Pandas and NumPy."""
        if not scorecards:
            return {"total_runs": 0, "pass_rate_pct": 0.0, "metrics": {}}

        total_runs = len(scorecards)
        passed_runs = sum(1 for s in scorecards if s.passed)

        records: list[dict[str, float]] = []
        for s in scorecards:
            row: dict[str, float] = {"composite_score": s.composite_score}
            for m_name, m_val in s.metrics.items():
                if m_val.value is not None:
                    row[m_name] = m_val.value
            records.append(row)

        df = pd.DataFrame(records)

        summary: dict[str, Any] = {
            "total_runs": total_runs,
            "passed_runs": passed_runs,
            "pass_rate_pct": round((passed_runs / total_runs) * 100.0, 2),
            "metrics_mean": df.mean().round(2).to_dict(),
            "metrics_std": df.std().round(2).fillna(0.0).to_dict(),
            "metrics_min": df.min().round(2).to_dict(),
            "metrics_max": df.max().round(2).to_dict(),
        }
        return summary
