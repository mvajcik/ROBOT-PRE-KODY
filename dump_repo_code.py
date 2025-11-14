from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ktoré priečinky preskakujeme (binárky, venv, cache, git…)
SKIP_DIRS = {
    ".git",
    ".venv",
    ".ruff_cache",
    ".pytest_cache",
    ".github",  # ak nechceš, môžeš zmazať zo zoznamu
    "data_in",
    "data_out",
    "data_stage",
    "data_tmp",
    "__pycache__",
}

# ktoré prípony berieme ako „kód / konfigurák / dokument“
OK_EXT = {
    ".py",
    ".sh",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".md",
    ".txt",
    ".makefile",
    ".mk",
}

# niektoré špeciálne názvy bez prípony (Makefile, LICENSE, atď.)
OK_BASENAME = {"Makefile", "LICENSE", "ROADMAP", "STATUS", "DECISIONS"}

OUT_PATH = ROOT / "data_out" / "repo_code_dump.txt"


def is_ok_file(path: Path) -> bool:
    # preskoč zakázané priečinky v ceste
    for part in path.parts:
        if part in SKIP_DIRS:
            return False

    if path.is_dir():
        return False

    # binárne typy preskočíme podľa prípony
    if path.suffix.lower() in {
        ".xlsx",
        ".xlsm",
        ".xlsb",
        ".duckdb",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
    }:
        return False

    # ak má povolenú príponu, berieme
    if path.suffix.lower() in OK_EXT:
        return True

    # ak sa volá špeciálnym názvom bez prípony, berieme
    if path.name in OK_BASENAME:
        return True

    return False


def count_lines(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def main() -> None:
    files: list[Path] = []

    for root, dirs, filenames in os.walk(ROOT):
        # filtruj priečinky in-place, aby sa do nich nechodilo
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for name in filenames:
            p = Path(root) / name
            if is_ok_file(p):
                files.append(p)

    files = sorted(files, key=lambda p: str(p.relative_to(ROOT)))

    # spočítaj riadky
    file_infos = []
    total_lines = 0
    for p in files:
        n = count_lines(p)
        total_lines += n
        file_infos.append((p, n))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUT_PATH.open("w", encoding="utf-8") as out:
        out.write("# ROBOT-PRE-KODY – súhrn kódu\n\n")
        out.write("## 1) Súhrn súborov a počty riadkov\n\n")
        out.write(f"Celkový počet súborov: {len(file_infos)}\n")
        out.write(f"Celkový počet riadkov (len vybrané typy): {total_lines}\n\n")

        out.write("### Zoznam súborov:\n")
        for p, n in file_infos:
            rel = p.relative_to(ROOT)
            out.write(f"{n:6d}  {rel}\n")

        out.write("\n\n## 2) Plný kód všetkých súborov\n\n")

        for p, n in file_infos:
            rel = p.relative_to(ROOT)
            out.write(f"\n\n# === {rel} ({n} riadkov) ===\n\n")
            try:
                with p.open("r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        out.write(line.rstrip("\n") + "\n")
            except Exception as e:
                out.write(f"\n# [CHYBA] Nepodarilo sa prečítať súbor: {e}\n")

    print(f"[OK] Zapísané do: {OUT_PATH}")


if __name__ == "__main__":
    main()
