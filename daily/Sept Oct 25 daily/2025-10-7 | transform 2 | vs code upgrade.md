🧭 Denný log – 2025-10-05 | Transform 2 | VS Code upgrade

🎯 Ciele chatu
	•	Nastaviť plnohodnotné VS Code prostredie pre rýchly vývoj na Macu aj Delli.
	•	Dokončiť prepojenie na GitHub (branch workflow).
	•	Spustiť automatické testovanie, formátovanie a linting (pytest autorun + Black + Ruff).
	•	Overiť funkčnosť transform_block a pripraviť pôdu pre try_transform_from_anon.py.

⸻

✅ Čo sme spravili
	1.	GitHub sync Mac ↔ Dell
	•	SSH kľúče nastavené, repo ROBOT-PRE-KODY beží na oboch zariadeniach.
	•	Vetvy (feat/..., fix/..., win-clean) používame na bezpečný vývoj.
	2.	VS Code prostredie
	•	Black → automaticky formátuje pri uložení.
	•	Ruff → kontroluje logické a štýlové chyby.
	•	Pytest → autorun pri uložení testov (testExplorer.onSave).
	•	Pre-commit → spúšťa Black + Ruff + pytest pri commite/pushi.
	•	Pylance → typové kontroly v reálnom čase.
	•	Všetky nástroje fungujú v .venv a sú jednotné pre Mac aj Dell.
	3.	Kód / projekt
	•	transform_block prešiel testami.
	•	pyproject.toml obsahuje Black a Ruff nastavenia.
	•	Pre-commit hook = QA ochrana.
	•	Autorun pytest a lintovanie v editore → okamžitá spätná väzba.

⸻

🔜 Čo bude ďalej
	•	Začať nový log: „2025-10-06 | Transform 3 | Anon → DuckDB test“.
	•	Krok 1: spustiť try_transform_from_anon.py a overiť výstupy CSV.
	•	Krok 2: napojiť výsledky do DuckDB a vytvoriť YTD report.

⸻
