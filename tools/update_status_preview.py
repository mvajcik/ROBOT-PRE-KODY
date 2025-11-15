from pathlib import Path

import yaml


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


# načítame repo_summary.yml
summary_path = Path("repo_summary.yml")
summary = yaml.safe_load(summary_path.read_text())

# vezmeme len blok repo_health
repo_health = summary.get("repo_health", {})

# pekný výpis
print("=== PREVIEW: repo_health ===")
for k, v in repo_health.items():
    print(f"{k}: {v}")

# načítame project_status.yml a pozrieme, čo je tam v status.repo_health
status_path = Path("project_status.yml")
status = yaml.safe_load(status_path.read_text())

status_repo_health = (status.get("status") or {}).get("repo_health", {})

print("\n=== PREVIEW: status.repo_health (v project_status.yml) ===")
for k, v in status_repo_health.items():
    print(f"{k}: {v}")

# --- UPDATE PROJECT_STATUS.YML (preview only, no save yet) ---
status_path = Path("project_status.yml")
status_data = load_yaml(status_path)

print("\n=== PREVIEW: values in project_status.yml (before update) ===")
for k, v in status_data.get("status", {}).get("repo_health", {}).items():
    print(f"{k}: {v}")

# pripravíme aktualizované hodnoty
updated_health = {
    "scanned_at": summary["meta"]["scanned_at"],
    "python_files_total": summary["metrics"]["python_files_total"],
    "python_lines_total": summary["metrics"]["python_lines_total"],
    "tests_count": summary["metrics"]["tests_count"],
    "pytest_ok": summary["health_checks"]["pytest"]["ok"],
    "ruff_ok": summary["health_checks"]["ruff"]["ok"],
    "flake8_ok": summary["health_checks"]["flake8"]["ok"],
}

print("\n=== PREVIEW: values that WOULD be written ===")
for k, v in updated_health.items():
    print(f"{k}: {v}")
# --- APPLY UPDATE: zapíšeme hodnoty do project_status.yml ---
status_data.setdefault("status", {})["repo_health"] = updated_health
save_yaml(status_path, status_data)
print("\nUPDATED: project_status.yml -> status.repo_health")
