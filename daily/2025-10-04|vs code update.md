ZHRNUTIE 2 – Nastavenie VS Code + workflow (Ty ↔ ChatGPT ↔ Copilot)

🔹 Cieľ

Maximálna efektivita pri vývoji medzi Macom a Dellom bez chaosu, s čistým kódom a rýchlym feedbackom.

⸻

🧩 1. Rozdelenie rolí
	•	Ty: píšeš testy, definuješ logiku a ciele.
	•	ChatGPT: návrhy architektúry, kontrakty, edge cases, SQL logika.
	•	Copilot: dopĺňa malé bloky kódu z komentárov/TODO.
	•	Black + Ruff: automatická čistota kódu.
	•	pytest autorun: okamžitá spätná väzba.

⸻
⚙️ 2. VS Code nastavenia

V .vscode/settings.json maj minimálne toto:
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["-q", "tests"],
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "editor.codeActionsOnSave": {"source.organizeImports": "explicit"},
  "testing.automaticallyOpenPeekView": "failure",
  "testing.gutterEnabled": true,
  "testExplorer.onSave": "test-file"
}

"ruff.enable": true

Ak chceš mať linty (Ruff).

⸻

💡 3. Denný loop
	1.	Napíš test (malý, konkrétny).
	2.	Pridaj kostru funkcie + komentár, čo má robiť.
	3.	Copilot nech doplní detaily.
	4.	Ulož → Black a testy sa spustia.
	5.	Fixni len to, čo padne.
	6.	Commit malých krokov → push.

⸻

🔄 4. Synchronizácia Dell ↔ Mac

Najčistejšie cez GitHub:
	•	Na oboch PC máš robot-pre-kody klonovaný.
	•	Pracuj na vetve (napr. feat/transform-mvp),
	•	Commit → push → pull na druhom stroji.
	•	Testy sa spustia automaticky (CI workflow).

Výhoda: vždy rovnaké prostredie, žiadne kopírovanie súborov.

⸻

🧠 5. Kedy koho použiť
	•	ChatGPT (ja): plán, architektúra, SQL logika, test scenáre.
	•	Copilot: doplňujúcich 5–10 riadkov, regexy, pandas drobnosti.
	•	Ty: definuješ, čo má byť výsledok, ako to má vyzerať (logika financného kontrolóra).

⸻

👉 Výsledok:
	•	Mac a Dell pracujú s rovnakým kódom cez GitHub,
	•	Black + pytest + CI ti garantujú stabilitu,
	•	ChatGPT + Copilot ti výrazne skracujú čas,
	•	Vývoj je rozdelený na malé, bezpečné kroky.
