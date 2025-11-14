Cieľ dňa
	•	Rozbehať autorun testov (pri uložení alebo pushnutí).
	•	Začať s implementáciou Transform časti (prevod načítaných blokov → jednotný formát).

⸻

Čo sme spravili
	1.	Autorun testov
	•	✅ Pytest v VS Code beží, autorun pri save máme zapnutý.
	•	✅ Testy fungujú aj pre novú funkciu transform_block.
	•	✅ Na GitHube beží workflow tests.yml (CI sa spustí pri každom push/PR).
	•	✅ Nastavený branch protection → každý merge na master musí mať zelený check pytest.
	•	✅ Pridali sme README.md s CI badge.
	•	✅ Pridali sme PR template pre jasný review flow.
	2.	Transform časť
	•	🟡 Zatiaľ sme nedefinovali finálny vstup/výstup.
	•	🟡 Funkciu transform_block máme nachystanú, ale implementácia logiky (Excel blok → normalizovaná tabuľka Country, Week, Metric, Value) sa ešte len začne.
	•	🟡 Testovací súbor test_transform.py je pripravený, čaká na prvú reálnu verziu funkcie.

⸻

Stav
	•	Autorun testov + CI + GitHub ochrany → ✅ hotové.
	•	Transform časť → 🔜 začíname (definícia štruktúry vstupu/výstupu + prvá implementácia).

⸻

Chceš, aby som hneď v novom chate pripravil návrh:
👉 štruktúra vstupu (Excel blok) a výstupu (normalizovaná tabuľka),
tak aby sme mohli rovno začať písať transform_block + test?
