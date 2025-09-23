Daily log – 2025-09-20

Cieľ dňa
	•	Ujasniť Krok 0: robot na efektívnejšiu tvorbu kódu (Dev Robot), ktorý odstráni ping-pong pri vývoji.
	•	Prejsť, čo používa profi freelancer (IT/finance) pri práci s dátami v Exceli.
	•	Rozhodnúť sa pre Úroveň 2 robota: auto-loop s whitelist fixmi + paralelné testy.

Čo sme spravili
	•	Vyjasnili rozdiel medzi hotové kocky (open-source nástroje ako pytest, ruff, mypy, pandera, DuckDB) a naše custom roboty (Dev Robot, Filing Robot, Audit Robot, Checks Robot, Export Robot).
	•	Pripravili sme Dev Robot v0.2: spúšťa testy, generuje report, rozpoznáva typické chyby a navrhuje patche (requirements.diff, config.diff).
	•	Diskutovali sme Úroveň 2: robot spustí testy, ak spadnú → aplikuje len bezpečné fixy (balíčky, config, aliasy) → znovu testuje (max 3 iterácie).
	•	Zhodnotili sme výhody Mac Studia: rýchle paralelné testy (pytest -n auto), veľké Excel súbory, plynulý watch mód.
	•	Identifikovali sme, čo ešte freelancer pridáva: CLI (Typer), config validácie (pydantic-settings), logging (structlog), Pandera schémy, golden testy, snapshoty, pre-commit hooks.

Zistenia / poznámky
	•	„Plne autonómne“ skúšanie 100 verzií kódu bez dozoru je nebezpečné → bezpečná cesta je auto-loop s whitelist fixmi + človek schvaľuje zmeny logiky.
	•	Najväčší „killer“ ping-pongu: golden fixtures + Dev Robot loop → robot vie hneď ukázať rozdiel medzi očakávaným a skutočným výstupom.
	•	Mac Studio má reálny prínos až pri veľkých dátach a paralelných testoch – inak je workflow rovnaký aj na slabšom stroji.

Problémy / rozhodnutia
	•	Rozhodnuté: ideme cestou Úroveň 2 (auto-loop + whitelist fixy + paralelné testy).
	•	Budeme používať anonymizované dáta pre golden testy, aby robot mohol testovať aj bez reálnych firemných dát.
	•	Do pipeline doplníme CLI štruktúru, Pandera schémy a golden testy, aby sme stavali na profesionálnych praktikách.

Ďalšie kroky (zajtra)
	1.	Implementovať Dev Robota v0.3 (auto-loop N=3 s whitelist fixmi).
	2.	Vytvoriť skeleton cli.py (Typer) a schema.py (Pandera) + prvý test schémy.
	3.	Pripraviť golden fixture (JAN vstup/výstup) a anonymizovaný AUG vstup → test golden porovnania.
	4.	Otestovať paralelné behy (pytest -n auto) na Macu s väčším súborom.
	5.	Nastaviť pre-commit hooky (ruff, mypy, quick pytest).

Čas
	•	Diskusia / špecifikácia: cca 2h
	•	Kódové príklady Dev Robota: pripravené v0.2 (upgrade na v0.3 zajtra).
