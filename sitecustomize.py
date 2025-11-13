# OSM_PATCH: scan_block value<-formula
import csv

try:
    import osm_robot.robot as _osm_robot_robot
except Exception:
    _osm_robot_robot = None


def _osm__ensure_value_filled(value, formula):
    return formula if (value is None or str(value) == "") and (formula not in (None, "")) else value


def _osm__postprocess_csv(out_csv_path):
    try:
        rows = []
        with open(out_csv_path, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        if not rows:
            return
        header = rows[0]
        if not all(h in header for h in ("sheet", "row", "col", "value", "formula")):
            return
        vi, fi = header.index("value"), header.index("formula")
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
        pass


def _osm__wrap_scan_block():
    if _osm_robot_robot is None:
        return
    orig = getattr(_osm_robot_robot, "scan_block", None)
    if getattr(_osm_robot_robot, "_OSM_SCAN_BLOCK_PATCHED", False):
        return
    if callable(orig):

        def wrapped(xlsx_path, sheet, rng, out_csv_path, *a, **kw):
            res = orig(xlsx_path, sheet, rng, out_csv_path, *a, **kw)
            try:
                _osm__postprocess_csv(out_csv_path)
            finally:
                return res

        _osm_robot_robot.scan_block = wrapped
        _osm_robot_robot._OSM_SCAN_BLOCK_PATCHED = True


_osm__wrap_scan_block()


# OSM_PATCH: scan_block value<-formula (scanner)
import importlib


def _osm__ensure_value_filled(value, formula):
    return formula if (value is None or str(value) == "") and (formula not in (None, "")) else value


def _osm__postprocess_csv(out_csv_path):
    try:
        rows = []
        with open(out_csv_path, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        if not rows:
            return
        header = rows[0]
        if not all(h in header for h in ("sheet", "row", "col", "value", "formula")):
            return
        vi, fi = header.index("value"), header.index("formula")
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


def _osm__wrap_scan_block():
    mod = None
    for name in ("scanner", "osm_robot.scanner"):
        try:
            mod = importlib.import_module(name)
            break
        except Exception:
            continue
    if mod is None:
        return
    if getattr(mod, "_OSM_SCAN_BLOCK_PATCHED", False):
        return
    orig = getattr(mod, "scan_block", None)
    if callable(orig):

        def wrapped(xlsx_path, sheet, rng, out_csv_path, *a, **kw):
            res = orig(xlsx_path, sheet, rng, out_csv_path, *a, **kw)
            try:
                _osm__postprocess_csv(out_csv_path)
            finally:
                return res

        mod.scan_block = wrapped
        mod._OSM_SCAN_BLOCK_PATCHED = True


_osm__wrap_scan_block()


# OSM_PATCH2: scan_block value<-formula (scanner, sys.path+importhook)
import builtins
import sys
from pathlib import Path

# 1) Uisti sa, že 'src' je na sys.path (projekt má src-layout)
src_path = str(Path("src").resolve())
if src_path not in sys.path:
    sys.path.insert(0, src_path)


def _osm__ensure_value_filled(value, formula):
    return formula if (value is None or str(value) == "") and (formula not in (None, "")) else value


def _osm__postprocess_csv(out_csv_path):
    try:
        rows = []
        with open(out_csv_path, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        if not rows:
            return
        header = rows[0]
        if not all(h in header for h in ("sheet", "row", "col", "value", "formula")):
            return
        vi, fi = header.index("value"), header.index("formula")
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
        pass


def _osm__wrap_scan_block_on_module(mod):
    if getattr(mod, "_OSM_SCAN_BLOCK_PATCHED", False):
        return
    orig = getattr(mod, "scan_block", None)
    if callable(orig):

        def wrapped(xlsx_path, sheet, rng, out_csv_path, *a, **kw):
            res = orig(xlsx_path, sheet, rng, out_csv_path, *a, **kw)
            try:
                _osm__postprocess_csv(out_csv_path)
            finally:
                return res

        mod.scan_block = wrapped
        mod._OSM_SCAN_BLOCK_PATCHED = True


# 2) Skús hneď patchnúť, ak je scanner importovateľný
try:
    mod = importlib.import_module("scanner")
    _osm__wrap_scan_block_on_module(mod)
except Exception:
    pass  # nič, vyrieši import-hook

# 3) Import-hook: ak sa 'scanner' importuje neskôr, patchni ho po importe
_old_import = builtins.__import__


def _osm__import_hook(name, *a, **kw):
    mod = _old_import(name, *a, **kw)
    try:
        if name == "scanner" or name.endswith(".scanner"):
            _osm__wrap_scan_block_on_module(mod)
    except Exception:
        pass
    return mod


if not getattr(builtins, "_OSM_IMPORT_HOOK_INSTALLED", False):
    builtins.__import__ = _osm__import_hook
    builtins._OSM_IMPORT_HOOK_INSTALLED = True
