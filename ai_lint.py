import os
import requests

# ============================
# Automatic endpoint detection
# ============================
def detect_lint_endpoint():
    """
    Determines the correct Lint server endpoint based on environment.
    Priority:
    1. Environment variable LINT_ENDPOINT (manual override)
    2. GitHub/GitLab CI → localhost (assume external server or mock)
    3. Docker on Mac/Windows → host.docker.internal
    4. Local Linux → localhost
    """
    # 1️⃣ Manual override
    endpoint = os.getenv("LINT_ENDPOINT")
    if endpoint:
        return endpoint

    # 2️⃣ GitHub Actions
    if os.getenv("GITHUB_ACTIONS") == "true":
        return "http://192.168.0.103:11434/lint"

    # 3️⃣ GitLab CI
    if os.getenv("GITLAB_CI") == "true":
        return "http://localhost:11434/lint"

    # 4️⃣ Docker macOS/Windows
    if os.getenv("DOCKER") == "true" or os.path.exists("/.dockerenv"):
        if os.name == "nt" or os.uname().sysname == "Darwin":
            return "http://host.docker.internal:11434/lint"

    # 5️⃣ Default local Linux
    return "http://localhost:11434/lint"


LINT_ENDPOINT = detect_lint_endpoint()
print(f"[DEBUG] Using Lint endpoint: {LINT_ENDPOINT}")

# ============================
# Helper functions
# ============================

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
        # Clean leftover markdown if AI returned it
        for mark in ["```", "```javascript", "```python"]:
            result = result.replace(mark, "")
        return result.strip()
    except requests.exceptions.RequestException as e:
        return f"{comment_symbol} Error linting {file_path}: {e}"


def get_all_files():
    files = []
    for root, _, filenames in os.walk("."):
        for f in filenames:
            path = os.path.join(root, f)
            files.append(path)
    return files


def main():
    print("[DEBUG] Starting AI linting process...")

    # ======================
    # GitHub/GitLab CI: only check changed files
    # ======================
    files_to_lint = []

    if os.getenv("GITHUB_ACTIONS") == "true":
        # Example: in real usage, you can get PR changed files
        files_to_lint = ["./buggy_main.py"]
    elif os.getenv("GITLAB_CI") == "true":
        files_to_lint = ["./buggy_main.py"]
    else:
        # Local testing
        files_to_lint = ["./buggy_main.py"]

    print(f"[DEBUG] Files to lint: {files_to_lint}")

    if not files_to_lint:
        print("⚠️ No files found to lint.")
        return

    for file_path in files_to_lint:
        if ".venv" in file_path or "node_modules" in file_path:
            continue

        code = read_file(file_path)
        result = lint_file(file_path, code)
        overwrite_file(file_path, result)
        print(f"✅ Lint results applied to {file_path}")


if __name__ == "__main__":
    main()
