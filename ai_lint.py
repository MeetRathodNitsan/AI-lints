import os
import requests
import subprocess
import sys

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
    ".html": ("HTML", ""),
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


def run_basic_checks(file_path, language):
    """
    This function is now empty as all language-specific checks have been removed.
    """
    return []


def lint_file(file_path, code):
    language, comment_symbol = detect_language(file_path)
    print(f"[DEBUG] Linting {file_path} as {language} using comment '{comment_symbol}'")

    prompt = f"""
        You are an expert {language} developer.
        Critically analyze the following code for bugs, **including logical errors and flaws in the algorithm**.
        Correct the code **only if there are bugs or issues**.

        Rules:
        - If the code has no errors or issues, return the code **exactly as-is**.
        - Do NOT add any headers, language names, or titles.
        - Do NOT add EXPLANATIONS or comments if no changes were made.
        - If fixes were applied, add an EXPLANATIONS section at the end using '{comment_symbol}'.
        - Do NOT use Markdown formatting, backticks, or code fences.
        - Do NOT add any other text outside the code.

        Code:
        {code}
        """

    # API request and response handling logic
    try:
        response = requests.post(LINT_ENDPOINT, json={"diff": prompt}, timeout=300)
        response.raise_for_status()
        result = response.text.strip()

        # Clean leftover markdown if AI returned it
        for mark in ["```", "```javascript", "```python", "```java", "```go", "```c", "```cpp", "```rust", "```php",
                     "```tsx"]:
            result = result.replace(mark, "")

        # Append deployment reminder as comments
        extra_section = f"\n\n{comment_symbol} ⚠️ Code has been auto-corrected. Please review before deployment.\n\n"
        extra_section += f"{comment_symbol} ✅ Pre-Deployment Checklist:\n"
        extra_section += f"{comment_symbol} - Review code manually\n"
        extra_section += f"{comment_symbol} - Run tests\n"
        extra_section += f"{comment_symbol} - Run security scans\n"
        extra_section += f"\n{comment_symbol} 🚫 Do NOT deploy until all above checks pass successfully.\n"

        return result.strip() + "\n" + extra_section

    except requests.exceptions.RequestException as e:
        print(f"❌ Error linting {file_path}: {e}", file=sys.stderr)
        return None  # Return None on failure


def get_changed_files():
    try:
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

    files_to_lint = ["./buggy_main.py"]  # Replace with your files or use get_changed_files()
    print(f"[DEBUG] Files to lint: {files_to_lint}")

    if not files_to_lint:
        print("⚠️ No files found to lint.")
        return

    deployment_blocked = False

    for file_path in files_to_lint:
        if ".venv" in file_path or "node_modules" in file_path:
            continue

        code = read_file(file_path)
        result = lint_file(file_path, code)

        if result is not None:
            overwrite_file(file_path, result)
            print(f"✅ Lint results applied to {file_path}")

            # If the AI inserted fixes, block deployment
            if "Code has been auto-corrected" in result:
                deployment_blocked = True
        else:
            deployment_blocked = True

    if deployment_blocked:
        print("\n🚫 Deployment blocked!")
        print("⚠️ Code had bugs or checks failed.")
        print("✅ Please review the code manually and run the pre-deployment checklist.")
        print("➡️ After verification, rerun deployment.\n")
        sys.exit(1)
    else:
        print("\n✅ Code passed without auto-fixes. Safe to deploy!\n")


if __name__ == "__main__":
    main()