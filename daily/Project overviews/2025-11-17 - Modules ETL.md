meta:
  project_name: Robot pre kódy
  version: v1.0-RC
  author: Michal Vajcik
  last_update: '2025-11-14'
  path: /Users/michalvajcik/Documents/robot-pre-kody
  description: Framework na automatizáciu dátových procesov vo finančnom controllingu
    (retail, CEE).
status:
  environment:
    git_repo: true
    venv_present: true
    ci_workflows:
    - tests.yml
  codebase:
    python_files_total_estimate: 40
    python_lines_total_estimate: 3000
    main_dirs:
    - src
    - tests
    - data_in
    - data_stage
    - data_out
    - .github
  tests:
    total: 14
    passed: 14
    failed: 0
    pytest_ok: true
    ruff_ok: true
    flake8_ok: false
  repo_health:
    scanned_at: '2025-11-17 04:54:34'
    python_files_total: 46
    python_lines_total: 3278
    tests_count: 18
    pytest_ok: true
    ruff_ok: true
    flake8_ok: false
quality_summary:
- Transformačný robot má jednotný kontrakt výstupu (Country, Week, Metric, Value +
  meta).
- Všetky aktuálne testy (14) prechádzajú lokálne aj v CI (quick + full).
- Dummy test_autorun bol odstránený, pipeline je čistá.
- DuckDB IO a výbery (YTD) majú vlastné testy.
- repo_summary.yml generuje objektívny prehľad cez scan_repo.py.
current_focus:
  step: A
  name: Modularizácia transform_block na pipeline
  description: Rozdeliť transformáciu na moduly loader → validator → transformer →
    exporter a udržať kontrakt výstupu stabilný.
  success_criteria:
  - Existujú samostatné funkcie/ triedy pre loader, validator, transformer, exporter.
  - Všetky existujúce transform_* testy stále prechádzajú bez úpravy vstupov/výstupov.
  - Pridáme aspoň 1 nový test, ktorý skúša celý chain loader→validator→transformer→exporter.
next_steps:
  short_term:
  - Identifikovať aktuálnu funkciu transform_block a navrhnúť rozbitie na 4 moduly.
  - Vytvoriť minimálny loader + validator bez zmeny kontraktu výstupu.
  - Doplniť testy, ktoré kontrolujú, že kontrakt zostal rovnaký.
  mid_term:
  - Oddeliť exporter (DuckDB/CSV/Excel) od transformácie.
  - Prepojiť scan_repo.py → automatickú aktualizáciu repo_summary.yml.
  - Pripraviť šablóny WR/DR/Inventory/Daily nad novou pipeline.
  long_term:
  - Rozšíriť robotov o YTD a Stock reporty v CEO formáte.
  - Zjednotiť krajinové šablóny WR, DR, Inventory, Daily.
  - Prepojiť výstupy s Power BI.
lessons_learned:
- Ping-pong pri opravovaní skriptov sa dá minimalizovať kombináciou testov a jasného
  kontraktu výstupu.
- Konzistentný kontext (repo_summary + project_status + overview) šetrí čas pri každom
  novom chate.
- Každý commit má mať krátky popis zmeny a info o testoch.
- Projekt už funguje ako framework – cieľ je mať stabilnú pipeline, nie jednorazové
  skripty.
ai_guidelines:
- Vždy najprv over aktuálny stav repozitára z repo_summary.yml.
- 'Používaj formát promptu: Kontext → Cieľ → Vstup → Výstup → Test.'
- Nemeň funkčné časti bez explicitného súhlasu – najprv navrhni diff.
- Vždy validuj prostredie pred novým kódom (venv, PYTHONPATH, pytest).
- 'Aktuálny fokus: krok A – modularizácia transform_block na pipeline loader→validator→transformer→exporter.'


meta:
  scanned_at: "2025-11-17 04:54:34"
  root: "/Users/michalvajcik/Documents/robot-pre-kody"
  git_repo: true
  venv_present: true
inventory:
  dirs_present:
    - "src"
    - "tests"
    - "data_in"
    - "data_stage"
    - "data_out"
    - ".github"
  files_present:
    - "pyproject.toml"
    - "requirements.txt"
    - "Makefile"
    - "pytest.ini"
    - ".pre-commit-config.yaml"
  ci_workflows:
    - "tests.yml"
metrics:
  python_files_total: 46
  python_lines_total: 3278
  tests_count: 18
  tests_files:
    - "tests/test_transform.py"
    - "tests/test_loader.py"
    - "tests/test_duckdb_io.py"
    - "tests/test_scan_cli.py"
    - "tests/test_scanner.py"
    - "tests/test_period_normalization.py"
    - "tests/test_robot.py"
    - "tests/test_smoke.py"
    - "tests/test_period_normalization_weeks.py"
    - "tests/test_scan_edge_cases.py"
    - "tests/test_transform_perf.py"
    - "tests/test_period_normalization_quarters_halves.py"
    - "tests/test_validator.py"
    - "tests/test_duckdb_select.py"
    - "tests/test_transform_months.py"
    - "tests/test_transform_contract_min.py"
    - "tests/test_transformer_basic.py"
    - "tests/test_pipeline_chain.py"
  per_dir:
    src:
      exists: true
      py_files: 18
      py_lines: 1696
    tests:
      exists: true
      py_files: 20
      py_lines: 786
    data_in:
      exists: true
      py_files: 0
      py_lines: 0
    data_stage:
      exists: true
      py_files: 0
      py_lines: 0
    data_out:
      exists: true
      py_files: 0
      py_lines: 0
    .github:
      exists: true
      py_files: 0
      py_lines: 0
health_checks:
  pytest:
    ok: true
    code: 0
    out: "..................                                                       [100%]\n18 passed in 0.48s"
  ruff:
    ok: true
    code: 0
    out: "ruff 0.14.0"
  flake8:
    ok: false
    code: null
    out: "command not found"
repo_health:
  scanned_at: "2025-11-17 04:54:34"
  python_files_total: 46
  python_lines_total: 3278
  tests_count: 18
  pytest_ok: true
  ruff_ok: true
  flake8_ok: false
recommendations:
  - "Add CI in .github/workflows if missing"
  - "Ensure tests/ contains at least smoke tests"
  - "Add pre-commit with ruff/flake8 and pytest"
  - "Document run steps in README"
