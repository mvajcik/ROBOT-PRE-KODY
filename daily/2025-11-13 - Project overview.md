Project Overview: Robot pre kódy

🎯 Cieľ projektu
	1.	Vytvoriť šablónu a framework, ktorý umožní efektívne, bez ping-pongového ladenia, vytvárať nové nástroje pre automatizáciu reportov a rutinných úloh finančného manažéra.
	2.	Automatizovať celé controllingové procesy (zber dát, validácia, transformácia, YTD/stock výstupy, exporty pre CEO a PBI) tak, aby namiesto 6 dní manuálnej práce trval celý cyklus 1 deň.

📂 Štruktúra projektu
	•	data_in/ – vstupné Excel reporty
	•	data_stage/ – medzivýstupy a štandardizované bloky
	•	data_out/ – YTD, stock, audity
	•	src/ – všetky roboty a moduly
	•	tests/ – pytest testy
	•	.github/ – CI workflowy
	•	repo_summary.yml – automatický audit projektu
	•	project_status.yml – stav projektu a roadmap

🧠 Aktuálny technický stav
	•	Počet Python súborov: 37
	•	Počet riadkov kódu: 2645
	•	Testy: 15 (cca 7 prechádza, 8 padá – najmä DuckDB/transform)
	•	Funkčné moduly auditu Excelov
	•	Pre-commit opravený a funkčný
	•	GitHub SSH funguje na Macu aj Delli
	•	CI workflow existuje

🧱 Kde sme
	•	Máme stabilný základ, modulárnu štruktúru, audity, diagnostiku a čiastočne transformácie.
	•	Projekt už pôsobí ako framework, nie len sada skriptov.
	•	Kľúčové časti (transform → duckdb → tests) čakajú na zosúladenie.

🚧 Ďalšie kroky
	•	Opraviť DuckDB schému a transform testy
	•	Prepojiť scan_repo.py → automatická aktualizácia project_status.yml
	•	Modularizovať pipeline (loader/validator/transformer/exporter)
	•	Rozšíriť o šablóny WR/DR/Inventory/Daily
	•	Exporty pre Power BI

💡 Odporúčania projektového manažéra
	•	Zaviesť pravidelný rytmus releasov
	•	Používať changelog + test evidence pri každom commite
	•	Automatizovať QA (make qa / CI)
	•	Budovať framework, nie jednorazové skripty

## 🌱 Čo si má pamätať AI

- Projekt má dva hlavné ciele:
  1) šablóna/flow, ktorý minimalizuje ping-pong pri tvorbe nástrojov,
  2) postupná automatizácia celého controllingu (WR/DR/Inventory/Daily, YTD, CEO reporty).
- Pracovné prostredie: Mac Studio (primárne) + Dell ako záloha.
- Aktívna vetva: `master` (feature `feat/contract-safety` je mergnutá a stabilná).
- Testy: 14/14 prechádza, CI (quick + full) je zapojené.
- Aktuálny fokus: krok A – rozbiť `transform_block` na pipeline **loader → validator → transformer → exporter** bez zmeny kontraktu výstupu.
