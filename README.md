# ROBOT-PRE-KODY

Helper robot for finance controllers – automating Excel → DuckDB → Excel pipelines.

## CI Status
![tests](https://github.com/mvajcik/ROBOT-PRE-KODY/actions/workflows/tests.yml/badge.svg)

## How to use
- `make install` → setup venv + deps
- `make test` → run tests locally
- `make scan FILE=... SHEET=... RANGE=...` → scan Excel

---

## Project goals (prečo to robíme)
- Nezabíjať 1–3 dni týždenne filingom: kopírovanie reportov, kontrola konzistencie, YTD/Stock výstupy.
- Automatizovať: (1) sken Excel blokov → (2) normalizácia (weeks/months/quarters/halves) → (3) uloženie do DuckDB → (4) generovanie “CEO-friendly” Excelov.
- Udržať “rituál” a formát výstupov, ale mať dátovú základňu vhodnú pre pivoty / PBI.

## Architecture (stručne)

## Make targets (cheatsheet)
- `make install` – venv + deps
- `make test` – všetky testy
- `make test-fast` – smoke + scanner
- `make scan FILE=... SHEET=... RANGE=...` – manuálny scan
- `make validate CSV=...` – validácia výstupu skenera

## Data contract (čo garantujú testy)
- **Scanner**: rozpozná blok, typy buniek (text/číslo/vzorec/None).
- **Transform**: jednotný stĺpcový formát
  `Country, Business, Metric, PeriodType, Period, Value, SourceBlockID, QualityFlag, Notes, PeriodKey`.
- **Normalizácia**: `WEEK / MONTH / QUARTER / HALF` → `PeriodKey` je ISO-friendly.
- **DuckDB IO**: SELECT funguje nad dlhým tvarom (testy `test_duckdb_*`).

## CI (GitHub Actions)
- Quick testy na každý push (smoke + scanner).
- Full testy na PR (všetko, okrem `test_autorun_fail`).
- Badge v hlavičke README ukazuje stav.

## Contributing / workflow
1. `git switch -c feat/krátky-popis`
2. kód + testy
3. `make test` (lokálne zelené)
4. push → PR → CI musí byť zelené → merge
5. commit message: `feat: ... | fix: ... | ci: ... | docs: ...`

## Roadmap (TODO)
- [ ] Export späť do Excelu (CEO formát, “rovnaký ako doteraz”)
- [ ] Stock report generátor (nad DuckDB; zdieľané metriky)
- [ ] Rozšírené kontroly konzistencie (Daily vs Weekly vs Inventory)
- [ ] CLI príkaz `robot export --template ...`
- [ ] Pre-cleaning “country adapters” (názvy hárkov, posuny hlavičiek)
