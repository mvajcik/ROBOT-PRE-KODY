.PHONY: venv install test scan

venv:
	python3 -m venv .venv

install:
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

test:
	. .venv/bin/activate && pytest -q

# ukážkový scan – použijeme mini.xlsx z testu
scan:
	. .venv/bin/activate && python src/osm_robot/robot.py \
	  --file tests/fixtures/mini.xlsx --sheet AT_YTD --range B2:E2 --out data_out/cells.csv

.PHONY: qa full

qa:
	. .venv/bin/activate && pytest -q

# full = priprav actual výstupy + testy + report (keď budeš mať render)
full:
	. .venv/bin/activate && pytest -q

.PHONY: daily

# vytvorí nový denník podľa šablóny
daily:
	cp daily/template.md daily/$$(date +%F).md



freeze:
	. .venv/bin/activate && pip freeze > requirements.txt


# predvolené hodnoty (vieš ich prepísať pri volaní)
SHEET ?= AT_YTD
RANGE ?= B2:E20

.PHONY: scan_file
scan_file:
	@test -n "$(FILE)" || (echo "Použitie: make scan_file FILE=Subor.xlsx [SHEET=NazovListu] [RANGE=A1:D10]"; exit 1)
	. .venv/bin/activate && python src/osm_robot/robot.py \
	  --file data_in/$(FILE) --sheet $(SHEET) --range $(RANGE) --out data_out/cells.csv
robot:
\tpython dev_robot_v03.py --tests tests --whitelist whitelist.yml --pytest-args='-k "not test_autorun_fail"' --max-iter 3

# Makefile (pridaj do projektu)

test-fast:
	pytest -q tests/test_smoke.py tests/test_scanner.py

test-all:
	pytest -n auto -q
