import json
import subprocess
import time
from pathlib import Path

root = Path.cwd()
now = time.strftime("%Y-%m-%d %H:%M:%S")


def count_lines(p: Path):
    try:
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def safe_run(cmd):
    try:
        r = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=root, timeout=60
        )
        return {
            "ok": r.returncode == 0,
            "code": r.returncode,
            "out": (r.stdout or "").strip()[:3000],
        }
    except FileNotFoundError:
        return {"ok": False, "code": None, "out": "command not found"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "code": None, "out": "timeout"}


top = {p.name: p for p in root.iterdir() if p.is_dir()}
key_dirs = ["src", "tests", "data_in", "data_stage", "data_out", ".github", "scripts"]
present_dirs = [d for d in key_dirs if (root / d).exists()]
present_files = [
    f
    for f in [
        "pyproject.toml",
        "requirements.txt",
        "Makefile",
        "pytest.ini",
        ".pre-commit-config.yaml",
    ]
    if (root / f).exists()
]
has_git = (root / ".git").exists()
has_venv = (root / ".venv").exists()

# Per-dir metrics
dir_stats = {}
for d in present_dirs:
    p = root / d
    py_files = list(p.rglob("*.py")) if p.exists() else []
    lines = sum(count_lines(f) for f in py_files)
    dir_stats[d] = {"exists": p.exists(), "py_files": len(py_files), "py_lines": lines}

# Global metrics
EXCLUDE = {".venv", ".git", ".pytest_cache", ".ruff_cache", ".vscode"}
all_py = [p for p in root.rglob("*.py") if not any(part in EXCLUDE for part in p.parts)]
total_lines = sum(count_lines(f) for f in all_py)
tests_py = list((root / "tests").rglob("test_*.py")) if (root / "tests").exists() else []
workflows = (
    list((root / ".github/workflows").glob("*.yml"))
    if (root / ".github/workflows").exists()
    else []
)

# Quick commands (optional)
pytest_res = safe_run(["pytest", "-q"])
ruff_res = safe_run(["ruff", "--version"])
flake8_res = safe_run(["flake8", "--version"])

summary = {
    "meta": {"scanned_at": now, "root": str(root), "git_repo": has_git, "venv_present": has_venv},
    "inventory": {
        "dirs_present": present_dirs,
        "files_present": present_files,
        "ci_workflows": [w.name for w in workflows],
    },
    "metrics": {
        "python_files_total": len(all_py),
        "python_lines_total": total_lines,
        "tests_count": len(tests_py),
        "tests_files": [str(p.relative_to(root)) for p in tests_py][:50],
        "per_dir": dir_stats,
    },
    "health_checks": {"pytest": pytest_res, "ruff": ruff_res, "flake8": flake8_res},
    "repo_health": {
        "scanned_at": now,
        "python_files_total": len(all_py),
        "python_lines_total": total_lines,
        "tests_count": len(tests_py),
        "pytest_ok": pytest_res["ok"],
        "ruff_ok": ruff_res["ok"],
        "flake8_ok": flake8_res["ok"],
    },
    "recommendations": [
        "Add CI in .github/workflows if missing",
        "Ensure tests/ contains at least smoke tests",
        "Add pre-commit with ruff/flake8 and pytest",
        "Document run steps in README",
    ],
}


# Minimal YAML dumper (no external deps)
def to_yaml(obj, indent=0):
    sp = "  " * indent
    if isinstance(obj, dict):
        lines = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{sp}{k}:")
                lines.append(to_yaml(v, indent + 1))
            else:
                if isinstance(v, str):
                    sv = v.replace("\n", "\\n")
                    lines.append(f'{sp}{k}: "{sv}"')
                else:
                    lines.append(f"{sp}{k}: {json.dumps(v)}")
        return "\n".join(lines)
    elif isinstance(obj, list):
        lines = []
        for it in obj:
            if isinstance(it, (dict, list)):
                lines.append(f"{sp}-")
                lines.append(to_yaml(it, indent + 1))
            else:
                if isinstance(it, str):
                    sv = it.replace("\n", "\\n")
                    lines.append(f'{sp}- "{sv}"')
                else:
                    lines.append(f"{sp}- {json.dumps(it)}")
        return "\n".join(lines)
    else:
        return f"{sp}{json.dumps(obj)}"


print("DEBUG: start writing summary ...")
out_path = root / "repo_summary.yml"
out_path.write_text(to_yaml(summary), encoding="utf-8")
print("DEBUG: summary written OK")

print("=== Repo summary (short) ===")
print(f"Root: {root}")
print(f"Dirs: {', '.join(present_dirs) or '-'}")
print(f"Files: {', '.join(present_files) or '-'}")
print(f"Python files: {len(all_py)} | lines: {total_lines}")
print(f"Tests: {len(tests_py)} | CI workflows: {len(workflows)}")

status_line = (
    f"Pytest ok: {summary['health_checks']['pytest']['ok']} | "
    f"Ruff: {summary['health_checks']['ruff']['ok']} | "
    f"Flake8: {summary['health_checks']['flake8']['ok']}"
)
print(status_line)

print(f"Written: {out_path}")
