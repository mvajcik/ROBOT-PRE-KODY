Daily log – 2025-09-16

Cieľ dňa
	•	Priblížiť sa k profi workflowu malých IT tímov.
	•	Nastaviť automatické testovanie a využiť Mac Studio na rýchlejšie iterácie.

Čo som spravil
	•	Diskutoval som, ako malým tímom funguje Git + testy + CI → menej ping-pongu.
	•	Pripravil som plán na GitHub Actions (.github/workflows/tests.yml), ktorý bude spúšťať testy pri push/PR.
	•	Ukázal som postup, ako na Mac Studiu zrýchliť testy cez pytest-xdist a aliasy v Makefile.
	•	Vysvetlil som, ako v VS Code zapnúť Autorun on Save pre automatické spúšťanie testov pri uložení kódu.

Zistenia / Poznámky
	•	Už len tieto kroky (autorun v VS Code + Makefile aliasy) by vedeli okamžite zrýchliť prácu na kódoch, aj bez JupyterLab.
	•	JupyterLab môže byť neskôr dobrý doplnok na vizuálne skúšanie dát, ale základ testovania zvládne priamo VS Code.
	•	Najbližší krok je vytvoriť .github/workflows/tests.yml a vyskúšať push do repa, aby sme videli CI ✔/❌.

⸻

Chceš, aby som ti pripravil aj krátku to-do listu na zajtra (3 konkrétne úlohy, čo hneď spraviť)?
