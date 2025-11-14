# ---------- Makefile (Robot pre kody) ----------
SHELL := /bin/bash

# cesty a nástroje
VENV    := .venv
PYTHON  := $(VENV)/bin/python
PIP     := $(PYTHON) -m pip
ROBOTMOD:= robot_cli.cli        # spúšťame priamo modul cez -m
PYTEST  := $(PYTHON) -m pytest

# predvolené parametre (prepíš pri volaní: FILE=..., SHEET=..., RANGE=..., CSV=...)
FILE  ?= data_in/mini.xlsx
SHEET ?= AT_YTD
RANGE ?= B2:E2
CSV   ?= data_out/scan__mini__AT_YTD.csv

.PHONY: help venv install freeze scan validate test test-one test-fast test-all qa full daily

help:
	@echo "make venv            # vytvor .venv"
	@echo "make install         # pip upgrade + deps + editable install"
	@echo "make scan FILE=... SHEET=... RANGE=...   # robot scan"
	@echo "make validate CSV=...                    # robot validate"
	@echo "make test            # spusti všetky testy"
	@echo "make test-one FILE=...# spusti konkrétny test súbor"
	@echo "make test-fast       # spusti len základné sanity testy"
	@echo "make test-all        # spusti všetky testy paralelne"
	@echo "make daily           # založ denník z daily/template.md"
	@echo "make freeze          # vygeneruj requirements.txt"

# --- prostredie ---
venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	-$(PIP) install -r requirements.txt
	$(PIP) install -e .

freeze:
	$(PIP) freeze > requirements.txt

# --- Robot CLI ---
scan:
	PYTHONPATH=src $(PYTHON) -m $(ROBOTMOD) scan --file "$(FILE)" --sheet "$(SHEET)" --range "$(RANGE)"

validate:
	PYTHONPATH=src $(PYTHON) -m $(ROBOTMOD) validate --csv "$(CSV)"

# --- testy ---
test:
	PYTHONPATH=src $(PYTEST) -q -k "not test_autorun_fail"

test-one:
	PYTHONPATH=src $(PYTEST) -q $(FILE)

test-fast:
	PYTHONPATH=src $(PYTEST) -q tests/test_smoke.py tests/test_scanner.py

test-all:
	PYTHONPATH=src $(PYTEST) -n auto -q -k "not test_autorun_fail"

qa: test
full: test-all

# --- denník ---
daily:
	cp daily/template.md daily/$(shell date +%F).md
# ---------- koniec ----------
