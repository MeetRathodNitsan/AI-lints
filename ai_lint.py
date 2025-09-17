import os
import requests
import subprocess

LINT_ENDPOINT = "http://localhost:8000/lint"

# Mapping of file extensions to languages and their comment symbols
EXT_LANGUAGE_MAP = {
    ".py": ("Python", "#"),
    ".js": ("JavaScript", "//"),
    ".ts": ("TypeScript", "//"),
    ".java": ("Java", "//"),
    ".cpp": ("C++", "//"),
    ".c": ("C", "//"),
    ".cs": ("C#", "//"),
    ".rb": ("Ruby", "#"),
    ".go": ("Go", "//"),
    ".php": ("PHP", "//"),
    ".rs": ("Rust", "//"),
    ".swift": ("Swift", "//"),
    ".kt": ("Kotlin", "//"),
    ".scala": ("Scala", "//"),
    ".sh": ("Bash", "#"),
    ".yaml": ("YAML", "#"),
    ".yml": ("YAML", "#"),
    ".json": ("JSON", "//"),
    ".html": ("HTML", "<!-- -->"),
    ".css": ("CSS", "/* */"),
}

def get_all_files():
    files = []
    for root, _, filenames in os.walk("."):
        for f in filenames:
            path = os.path.join(root, f)
            files.append(path)
    return files

def detect_language(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return EXT_LANGUAGE_MAP.get(ext, ("Text", "#"))

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def overwrite_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content + "\n")

def lint_file(file_path, code):
    language, comment_symbol = detect_language(file_path)
    print(f"[DEBUG] Linting {file_path} as {language} using comment '{comment_symbol}'")

    prompt = f"""
You are an expert {language} developer.
Correct the following code **in-place**.

Rules:
- Only provide the fixed code.
- Do NOT include the original buggy code.
- Each fix must have an explanation inline using the comment symbol '{comment_symbol}'.
- At the end of the code, add a section called "EXPLANATIONS" where all explanations are commented using '{comment_symbol}'.
- Do NOT add any Markdown, headings, or external explanation outside the code.

Code:
{code}
"""
    try:
        response = requests.post(LINT_ENDPOINT, json={"diff": prompt}, timeout=120)
        response.raise_for_status()
        result = response.text.strip()
        # Clean any leftover markdown if AI returned it
        for mark in ["```", "```javascript", "```python"]:
            result = result.replace(mark, "")
        return result.strip()
    except requests.exceptions.RequestException as e:
        return f"{comment_symbol} Error linting {file_path}: {e}"

def get_changed_files():
    """
    # -----------------------------
    # GitHub/GitLab CI usage:
    # This function detects changed files in the last commit (or merge request) using Git.
    # Uncomment this when running in GitLab/GitHub CI.
    # -----------------------------
    """
    try:
        # Get list of changed files from last commit
        diff_output = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~1"]
        ).decode()
        changed_files = [f.strip() for f in diff_output.splitlines()
                         if os.path.splitext(f)[1].lower() in EXT_LANGUAGE_MAP]
        return changed_files
    except Exception as e:
        print(f"[DEBUG] Git diff failed: {e}")
        return []

def main():
    print("[DEBUG] Starting AI linting process...")

    # -----------------------------
    # Local testing: specify files manually
    files_to_lint = ["./buggy_main.py"]
    # -----------------------------

    # -----------------------------
    # GitHub/GitLab CI usage:
    # Uncomment the following lines to automatically lint changed files on push
    # changed_files = get_changed_files()
    # files_to_lint = changed_files
    # -----------------------------

    print(f"[DEBUG] Files to lint: {files_to_lint}")

    if not files_to_lint:
        print("⚠️ No files found to lint.")
        return

    for file_path in files_to_lint:
        if ".venv" in file_path or "node_modules" in file_path:
            continue

        code = read_file(file_path)
        result = lint_file(file_path, code)

        # Overwrite the original file with fixed code + inline comments + final explanation section
        overwrite_file(file_path, result)
        print(f"✅ Lint results applied to {file_path}")

if __name__ == "__main__":
    main()
