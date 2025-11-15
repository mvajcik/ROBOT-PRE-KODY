from pathlib import Path

import yaml


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


# ------- načítame repo_summary.yml -------
summary_path = Path("repo_summary.yml")
summary = load_yaml(summary_path)

repo_health = summary.get("repo_health", {})

print("=== APPLY UPDATE: repo_health => project_status.yml ===")
for k, v in repo_health.items():
    print(f"{k}: {v}")

# ------- načítame project_status.yml -------
status_path = Path("project_status.yml")
status = load_yaml(status_path)

if "status" not in status:
    status["status"] = {}

status["status"]["repo_health"] = repo_health

# ------- uložíme späť -------
save_yaml(status_path, status)

print("\nUPDATED project_status.yml ✓")
