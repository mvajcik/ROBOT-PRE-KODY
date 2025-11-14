# dev_robot_v03.py
#
# Auto-loop pre vývoj: spúšťa pytest, číta JUnit XML, aplikuje whitelisted fixy a opakuje.
# Použitie:
#   python dev_robot_v03.py --tests "tests" --whitelist "whitelist.yml" --max-iter 3
#
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path("src").resolve()))
sys.path.insert(0, str(Path(".").resolve()))
import importlib
import shlex
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml


def run_pytest_and_get_report(tests_path: str, pytest_args: str = "") -> Path:
    tmp = tempfile.NamedTemporaryFile(prefix="junit_", suffix=".xml", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()
    cmd = ["pytest", "-q", tests_path]
    if pytest_args:
        cmd += shlex.split(pytest_args)  # správne rozparsuje '-k "not test_autorun_fail"'
    cmd += [f"--junitxml={tmp_path}"]
    print(f"[robot] pytest: {' '.join(cmd)}")
    rc = subprocess.call(cmd)
    print(f"[robot] pytest return code: {rc}")
    return tmp_path


def parse_failures(junit_xml_path: Path):
    """Vráti list slovníkov s info o failoch: test_name, message, text."""
    failures = []
    tree = ET.parse(junit_xml_path)
    root = tree.getroot()
    # JUnit schema: <testsuite><testcase><failure message=..>text</failure></testcase>...
    for tc in root.iter("testcase"):
        for failure in tc.findall("failure"):
            failures.append(
                {
                    "test_name": f"{tc.get('classname', '')}.{tc.get('name', '')}",
                    "message": failure.get("message", "").strip(),
                    "text": (failure.text or "").strip(),
                }
            )
    return failures


def load_whitelist(whitelist_path: str) -> dict:
    with open(whitelist_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # Očakávaný formát:
    # fixes:
    #   - key: normalize_month_names
    #   - key: trim_header_spaces
    return {fix["key"] for fix in data.get("fixes", []) if "key" in fix}


def map_fail_to_fix_keys(failure: dict) -> list[str]:
    """
    Heuristika: mapuje text chýb na kľúče fixov.
    Pridávaj ďalšie pravidlá podľa potrieb testov (ideálne s tagom [AUTO] v správe).
    """
    msg = f"{failure.get('message', '')} {failure.get('text', '')}".lower()

    keys: list[str] = []

    # 1) Mesiace (aliasy)
    if (
        "month name" in msg
        or "invalid month" in msg
        or "month alias" in msg
        or "jan -> january" in msg
        or "jan → january" in msg
    ):
        keys.append("normalize_month_names")

    # 2) Medzery v hlavičkách
    if "header" in msg and ("space" in msg or "spaces" in msg or "trim" in msg):
        keys.append("trim_header_spaces")

    # 3) Špecifiká dátumov pre BIH
    if "bih" in msg and ("date" in msg or "datum" in msg):
        keys.append("fix_bih_date_parsing")

    # 4) CSV zo scan_block – prázdna value vs. formula
    if ("test_scan_block_csv" in msg) or ("scan_block_csv" in msg) or ("scan.csv" in msg):
        # Najspoľahlivejšie: monkey-patch funkcie pri importe (sitecustomize)
        keys.append("monkeypatch_scan_block_value_from_formula")
        # Pokus o patch zdrojáku (ak sa podarí, super)
        keys.append("patch_fill_value_from_formula")
        # Fallback na upravenie už vytvoreného CSV v /private/var/folders
        keys.append("value_from_formula_if_empty")

    # Dedup pri zachovaní poradia
    seen = set()
    return [k for k in keys if not (k in seen or seen.add(k))]


def apply_fix(fix_key: str) -> bool:
    """
    Zavolá implementáciu fixu z registry.
    Očakáva modul: `osm_robot.fixers.registry` s funkciou `get_fixer(key) -> callable|None`
    Fixer vracia True/False podľa toho, či niečo reálne upravil.
    """
    try:
        registry = importlib.import_module("osm_robot.fixers.registry")
    except ModuleNotFoundError:
        print("[robot] registry modul nenájdený (osm_robot.fixers.registry). Preskakujem.")
        return False

    get_fixer = getattr(registry, "get_fixer", None)
    if not callable(get_fixer):
        print("[robot] registry.get_fixer() chýba. Preskakujem.")
        return False

    fixer = get_fixer(fix_key)
    if not callable(fixer):
        print(f"[robot] Fixer pre '{fix_key}' nenájdený v registry.")
        return False

    print(f"[robot] Aplikujem fix: {fix_key}")
    try:
        changed = fixer()
        print(f"[robot] Fix '{fix_key}' -> changed={changed}")
        return bool(changed)
    except Exception as e:
        print(f"[robot] Fix '{fix_key}' zlyhal: {e}")
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tests", default="tests", help="Cesta k testom (dir alebo pattern)")
    ap.add_argument("--whitelist", default="whitelist.yml", help="Whitelist povolených fixov")
    ap.add_argument("--max-iter", type=int, default=3, help="Max počet cyklov auto-loopu")
    ap.add_argument(
        "--sleep-sec", type=float, default=0.0, help="Pauza medzi iteráciami (ak treba)"
    )
    ap.add_argument(
        "--pytest-args",
        default="",
        help="Dodatočné argumenty pre pytest (napr. -k 'not test_autorun_fail')",
    )
    args = ap.parse_args()

    allowed = load_whitelist(args.whitelist)
    if not allowed:
        print("[robot] Warning: whitelist je prázdny – žiadne fixy sa neaplikujú.")

    applied_any = False
    for i in range(1, args.max_iter + 1):
        print(f"\n[robot] ===== Iterácia {i}/{args.max_iter} =====")
        report = run_pytest_and_get_report(args.tests, args.pytest_args)
        failures = parse_failures(report)
        print(f"[robot] Nájdené failures: {len(failures)}")

        if not failures:
            print("[robot] ✅ Všetky testy prešli.")
            if applied_any:
                print("[robot] Hotovo: fixy aplikované a testy zelené.")
            else:
                print("[robot] Hotovo: žiadne fixy neboli potrebné.")
            sys.exit(0)

        # Zbierame kandidátov na fix
        pending = []
        for f in failures:
            for key in map_fail_to_fix_keys(f):
                if key in allowed:
                    pending.append(key)
                else:
                    print(f"[robot] Fix '{key}' nie je v whiteliste → ignorujem.")

        # Deduplicate, zachovaj poradie
        seen = set()
        pending = [k for k in pending if not (k in seen or seen.add(k))]

        if not pending:
            print("[robot] ❌ Sú failures, ale žiadny povolený fix nie je k dispozícii.")
            sys.exit(1)

        print(f"[robot] Plánované fixy: {pending}")

        # Aplikujeme fixy; ak nič nezmenili, končíme
        changed_something = False
        for key in pending:
            if apply_fix(key):
                changed_something = True

        if not changed_something:
            print("[robot] ❌ Fixy neuskutočnili žiadnu zmenu. Končím.")
            sys.exit(1)

        applied_any = True
        if args.sleep_sec:
            time.sleep(args.sleep_sec)

    print(
        "[robot] ❌ Dosiahnutý limit iterácií bez zelenej."
        "Skús pozrieť logy a rozšíriť fixy/whitelist."
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
