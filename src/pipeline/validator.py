from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .loader import LoadedBlock


@dataclass
class ValidationIssue:
    level: str  # "ERROR", "WARN", "INFO"
    message: str
    metric: str | None = None
    period: str | None = None


def validate_block(loaded: LoadedBlock) -> List[ValidationIssue]:
    """
    Základný validator bloku.

    Aktuálne kontroluje:
    - prázdne cells/headers,
    - chýbajúci meta.year / year_hint,
    - chýbajúci static.Metric v headers,
    - chýbajúce period headers (weeks/months/quarters/halves).
    """
    issues: List[ValidationIssue] = []

    # základná kontrola: musíme mať cells aj headers
    if not loaded.cells or not loaded.headers:
        issues.append(
            ValidationIssue(
                level="ERROR",
                message="Block has no cells or headers.",
            )
        )

    # kontrola roka v meta: year alebo year_hint
    year = loaded.meta.get("year") or loaded.meta.get("year_hint")
    if year is None:
        issues.append(
            ValidationIssue(
                level="WARN",
                message="Block meta is missing year/year_hint.",
            )
        )

    # kontrola: static.Metric musí existovať
    static_metric = (loaded.headers.get("static") or {}).get("Metric")
    if static_metric is None:
        issues.append(
            ValidationIssue(
                level="ERROR",
                message="Missing static.Metric in headers (cannot locate metric column).",
            )
        )

    # ak metric stĺpec existuje, skontrolujeme prázdne názvy metrík
    if static_metric is not None:
        metric_col = static_metric
        for cell in loaded.cells:
            if cell.get("col") == metric_col:
                name = str(cell.get("value", "")).strip()
                if not name:
                    issues.append(
                        ValidationIssue(
                            level="WARN",
                            message=f"Empty metric name in row {cell.get('row')}.",
                        )
                    )

    # kontrola: musíme mať aspoň jeden period set (weeks/months/quarters/halves)
    if not loaded.period_sets:
        issues.append(
            ValidationIssue(
                level="ERROR",
                message="No period headers found (weeks/months/quarters/halves).",
            )
        )

    return issues
