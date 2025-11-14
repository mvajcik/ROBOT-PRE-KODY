# sitecustomize: OSM scanner patches
# Tento modul sa načíta automaticky, ak je na sys.path.

from __future__ import annotations

import builtins
import csv
import importlib
import sys
from pathlib import Path
from typing import Any


def _osm__postprocess_csv(out_csv_path: str) -> None:
    """Fill missing 'value' from 'formula' in scanner CSV output."""
    try:
        with open(out_csv_path, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))

        if not rows:
            return

        header = rows[0]
        if not all(h in header for h in ("sheet", "row", "col", "value", "formula")):
            return

        vi = header.index("value")
        fi = header.index("formula")
        changed = False

        for i in range(1, len(rows)):
            r = rows[i]
            if len(r) <= max(vi, fi):
                continue
            if (r[vi] == "" or r[vi] is None) and r[fi]:
                r[vi] = r[fi]
                changed = True

        if changed:
            with open(out_csv_path, "w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerows(rows)
    except Exception:
        # patch nesmie zhodiť beh
        pass


# -----------------------------------------------------------------------------
# 1) Priamy patch na osm_robot.robot.scan_block
# -----------------------------------------------------------------------------


def _patch_osm_robot_scan_block() -> None:
    try:
        import osm_robot.robot as osm_robot_robot  # type: ignore[import]
    except Exception:
        return

    if getattr(osm_robot_robot, "_OSM_SCAN_BLOCK_PATCHED", False):
        return

    orig = getattr(osm_robot_robot, "scan_block", None)
    if not callable(orig):
        return

    def wrapped(xlsx_path: str, sheet: str, rng: str, out_csv_path: str, *a: Any, **kw: Any) -> Any:
        res = orig(xlsx_path, sheet, rng, out_csv_path, *a, **kw)
        try:
            _osm__postprocess_csv(out_csv_path)
        finally:
            return res

    osm_robot_robot.scan_block = wrapped  # type: ignore[attr-defined]
    osm_robot_robot._OSM_SCAN_BLOCK_PATCHED = True  # type: ignore[attr-defined]


# -----------------------------------------------------------------------------
# 2) Spoločný wrapper pre moduly so scan_block (scanner, osm_robot.scanner)
# -----------------------------------------------------------------------------


def _wrap_scan_block_on_module(mod: Any) -> None:
    if getattr(mod, "_OSM_SCAN_BLOCK_PATCHED", False):
        return

    orig = getattr(mod, "scan_block", None)
    if not callable(orig):
        return

    def wrapped(xlsx_path: str, sheet: str, rng: str, out_csv_path: str, *a: Any, **kw: Any) -> Any:
        res = orig(xlsx_path, sheet, rng, out_csv_path, *a, **kw)
        try:
            _osm__postprocess_csv(out_csv_path)
        finally:
            return res

    mod.scan_block = wrapped  # type: ignore[attr-defined]
    mod._OSM_SCAN_BLOCK_PATCHED = True  # type: ignore[attr-defined]


def _patch_scanner_modules() -> None:
    """Skús hneď patchnúť scanner moduly, ak sú importovateľné."""
    for name in ("scanner", "osm_robot.scanner"):
        try:
            mod = importlib.import_module(name)
        except Exception:
            continue
        _wrap_scan_block_on_module(mod)


# -----------------------------------------------------------------------------
# 3) sys.path + import hook pre neskoršie importy scanneru
# -----------------------------------------------------------------------------


def _ensure_src_on_path() -> None:
    """Pridaj src/ na sys.path (src-layout projektu)."""
    src_path = str(Path("src").resolve())
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


_old_import = builtins.__import__


def _osm__import_hook(name: str, *a: Any, **kw: Any):
    mod = _old_import(name, *a, **kw)
    try:
        if name == "scanner" or name.endswith(".scanner"):
            _wrap_scan_block_on_module(mod)
    except Exception:
        # hook nesmie zhodiť beh
        pass
    return mod


def _install_import_hook() -> None:
    if getattr(builtins, "_OSM_IMPORT_HOOK_INSTALLED", False):
        return
    builtins.__import__ = _osm__import_hook  # type: ignore[assignment]
    builtins._OSM_IMPORT_HOOK_INSTALLED = True  # type: ignore[attr-defined]


# -----------------------------------------------------------------------------
# Spusti patche pri importe sitecustomize
# -----------------------------------------------------------------------------


_patch_osm_robot_scan_block()
_ensure_src_on_path()
_patch_scanner_modules()
_install_import_hook()
