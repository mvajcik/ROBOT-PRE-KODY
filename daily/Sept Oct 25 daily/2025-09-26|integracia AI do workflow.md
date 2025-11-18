🎯 Cieľ dňa

Nastaviť VS Code tak, aby nám čo najviac pomáhal znižovať ping-pong pri ladení kódu a zvyšoval efektivitu práce na projekte Robot pre kódy (v04).

⸻

✅ Čo sme spravili
	•	Black:
	•	Nainštalovaný do lokálneho .venv.
	•	Otestovaný – pri uložení alebo manuálne vie preformatovať kód.
	•	Pylance:
	•	Už beží, ukazuje varovania/chyby a typové nezrovnalosti.
	•	Jupyter:
	•	Správne nainštalovaný od Microsoftu.
	•	Do prostredia doplnený ipykernel.
	•	Overené, že notebook (.ipynb) vie bežať na lokálnom .venv interpreteri a zobrazuje výsledky priamo v editore.
	•	settings.json:
	•	Zlúčené nastavenia do jedného objektu.
	•	Teraz obsahuje:
	•	Black (formatOnSave),
	•	Pylance (basic checks),
	•	Pytest autorun (tests priečinok),
	•	Interpreter nastavený na .venv/bin/python,
	•	EasyCode AI API key.

⸻

📌 Kde sa nachádzame v projekte
	•	Máme základnú infraštruktúru robota v4.
	•	VS Code je pripravené na efektívnejší workflow:
	•	Black → čistý kód,
	•	Pylance → odhalenie chýb ešte pred spustením,
	•	Pytest → automatické testovanie,
	•	Jupyter → interaktívne testovanie blokov kódu.

⸻

🚀 Ďalší krok (nový log)
	•	Otestovať autorun testov v tests/ priečinku (či sa spúšťajú automaticky pri uložení).
	•	Rozhodnúť, či budeme pre workflow používať radšej Jupyter bloky alebo čisté .py súbory s testami (možno kombináciu).
	•	Pokračovať na časti Transform (DuckDB) – začať pripravovať knižnicu opakovane použiteľných SQL view šablón.

⸻

👉 Takto máme pripravené prostredie, aby ďalší kód netrval mesiac, ale dni.
