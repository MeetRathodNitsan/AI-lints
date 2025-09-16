import os
import requests

LINT_ENDPOINT = "http://localhost:8000/lint"
OUTPUT_FILE = "lint_results.txt"

def get_all_py_files():
    """Recursively collect all Python files in the repo."""
    py_files = []
    for root, _, files in os.walk("."):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                py_files.append(path)
    return py_files

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def lint_file(file_path, code):
    """Send file content to /lint endpoint."""
    try:
        response = requests.post(LINT_ENDPOINT, json={"diff": code}, timeout=60)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"Error linting {file_path}: {e}"

def main():
    py_files = get_all_py_files()
    if not py_files:
        print("⚠️ No Python files found to lint.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for file_path in py_files:
            code = read_file(file_path)
            out.write(f"\n=== Linting {file_path} ===\n")
            result = lint_file(file_path, code)
            out.write(result + "\n")

    print(f"✅ Lint results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
