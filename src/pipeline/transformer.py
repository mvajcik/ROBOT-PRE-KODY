from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .loader import LoadedBlock


@dataclass
class TransformResult:
    """
    Výsledok transformácie jedného bloku:
    - rows: normalizované riadky do tabuľky
    - audit_rows: záznamy o problémoch špecifických pre transformáciu
    """

    rows: List[Dict]
    audit_rows: List[Dict]


def transform_loaded_block(loaded: LoadedBlock) -> TransformResult:
    """
    Placeholder transformer.

    Teraz ešte NEROBÍ skutočnú logiku – všetko beží v src/transform.py.
    V ďalších krokoch sem postupne presunieme vnútro transform_block tak,
    aby:
      - kontrakt výstupu ostal rovnaký,
      - loader/validator/transformer boli čisté moduly.
    """
    return TransformResult(rows=[], audit_rows=[])


def extract_metric_rows(loaded: LoadedBlock) -> tuple[list[dict], list[dict]]:
    """
    Prvý modul transformera: extrahuje riadky metrík a hodnoty období.
    Zatiaľ nerealizuje žiadnu logiku – v ďalších krokoch budeme prenášať
    vnútro transform_block sem.
    """
    return [], []
