import os


def count_lines_by_category(root="."):
    categories = {"project_code": 0, ".venv": 0, "__pycache__": 0, ".git": 0, "other": 0}

    for dirpath, _, files in os.walk(root):
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext not in (".py", ".txt"):
                continue

            path = os.path.join(dirpath, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                lines = sum(1 for _ in file)

            if ".venv" in dirpath:
                categories[".venv"] += lines
            elif "__pycache__" in dirpath:
                categories["__pycache__"] += lines
            elif ".git" in dirpath:
                categories[".git"] += lines
            elif dirpath == root:
                categories["project_code"] += lines
            else:
                categories["other"] += lines

    return categories


if __name__ == "__main__":
    result = count_lines_by_category(".")
    for cat, count in result.items():
        print(f"{cat}: {count} riadkov")
