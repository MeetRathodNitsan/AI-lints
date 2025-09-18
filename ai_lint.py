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

def run_basic_checks(file_path, language):
    """
    Run basic pre-deployment checks depending on language.
    """
    checks = {
        "Python": [
            "./.venv/bin/flake8 --max-line-length=120",
            "./.venv/bin/mypy",
            "./.venv/bin/pytest --maxfail=1"
        ],
        "JavaScript": ["eslint", "npm test"],
        "TypeScript": ["eslint", "tsc", "npm test"],
        "Java": ["javac {file}", "mvn test"],
        "C++": ["clang-tidy {file}", "g++ -Wall -Werror -o /dev/null {file}"],
        "C": ["clang-tidy {file}", "gcc -Wall -Werror -o /dev/null {file}"],
        "C#": ["dotnet build", "dotnet test"],
        "Ruby": ["rubocop", "rspec"],
        "Go": ["golangci-lint run", "go test ./..."],
        "Rust": ["cargo clippy", "cargo test"],
        "PHP": ["php -l {file}", "phpunit"],
        "Swift": ["swiftlint", "xcodebuild test"],
        "Kotlin": ["ktlint", "./gradlew test"],
        "Scala": ["scalafmt", "sbt test"],
        "Bash": ["shellcheck {file}", "bash -n {file}"],
        "YAML": ["yamllint {file}"],
        "JSON": ["jq empty {file}"],
        "HTML": ["htmlhint {file}"],
        "CSS": ["stylelint {file}"],
    }
    commands = checks.get(language, [])
    commands = [cmd.format(file=file_path) for cmd in commands]
    return commands

def lint_file(file_path, code):
    language, comment_symbol = detect_language(file_path)
    print(f"[DEBUG] Linting {file_path} as {language} using comment '{comment_symbol}'")

    prompt = f"""
    You are an expert {language} developer.
    Correct the following code **only if there are bugs**.

    Rules:
    - If the code has no errors or issues, return the code **exactly as-is**.
    - Do NOT add any headers, language names, or titles.
    - Do NOT add EXPLANATIONS or comments if no changes were made.
    - Only provide explanations **inline** using '{comment_symbol}' if you fixed something.
    - If fixes were applied, add an EXPLANATIONS section at the end using '{comment_symbol}'.
    - Do NOT use Markdown formatting, backticks, or code fences.
    - Do NOT add any other text outside the code.

    Code:
    {code}
    """

    try:
        response = requests.post(LINT_ENDPOINT, json={"diff": prompt}, timeout=120)
        response.raise_for_status()
        result = response.text.strip()

        # Clean leftover markdown if AI returned it
        for mark in ["```", "```javascript", "```python", "```java", "```go", "```c", "```cpp", "```rust", "```php", "```tsx"]:
            result = result.replace(mark, "")

        # Pre-deployment checklist (language-specific)
        checklist = {
            "Python": [
                "Run unit tests: pytest",
                "Lint: flake8 or pylint",
                "Type checks: mypy",
                "Security scan: bandit",
            ],
            "JavaScript": [
                "Run unit tests: jest",
                "Lint: eslint",
                "Type checks (if TS): tsc",
                "Security scan: npm audit",
            ],
            "TypeScript": [
                "Run unit tests: jest",
                "Lint: eslint",
                "Type checks: tsc",
                "Security scan: npm audit",
            ],
            "React": [
                "Run unit tests: jest/react-testing-library",
                "Lint: eslint",
                "Build test: npm run build",
                "Security scan: npm audit",
                "Accessibility check: axe or lighthouse",
            ],
            "PHP": [
                "Run unit tests: phpunit",
                "Lint: php -l",
                "Static analysis: phpstan or psalm",
                "Security scan: php-security-checker",
            ],
            "Go": [
                "Run unit tests: go test",
                "Lint: golangci-lint",
                "Security scan: gosec",
            ],
            "Java": [
                "Run unit tests: mvn test",
                "Lint: checkstyle",
                "Static analysis: spotbugs",
                "Security scan: dependency-check",
            ],
            "Rust": [
                "Run unit tests: cargo test",
                "Lint: cargo clippy",
                "Security scan: cargo audit",
            ],
            "C++": [
                "Run unit tests with gtest/catch2",
                "Lint: clang-tidy",
                "Memory checks: valgrind",
                "Security scan: cppcheck",
            ],
            "C": [
                "Run unit tests",
                "Lint: clang-tidy",
                "Memory checks: valgrind",
                "Security scan: cppcheck",
            ],
            "C#": [
                "Run unit tests: dotnet test",
                "Lint: StyleCop",
                "Static analysis: SonarQube",
                "Security scan: dependency-check",
            ],
            "Ruby": [
                "Run unit tests: rspec",
                "Lint: rubocop",
                "Security scan: brakeman",
            ],
            "Swift": [
                "Run unit tests: xcodebuild test",
                "Lint: swiftlint",
                "Static analysis: swiftformat",
            ],
            "Kotlin": [
                "Run unit tests: ./gradlew test",
                "Lint: ktlint",
                "Static analysis: detekt",
            ],
            "Scala": [
                "Run unit tests: sbt test",
                "Lint: scalafmt",
                "Static analysis: scapegoat",
            ],
            "Bash": [
                "Lint: shellcheck",
                "Test script manually",
                "Check POSIX compliance",
            ],
            "YAML": [
                "Lint: yamllint",
                "Validate schema",
            ],
            "JSON": [
                "Validate JSON syntax",
                "Check schema validation",
            ],
            "HTML": [
                "Lint: htmlhint",
                "Accessibility check: lighthouse",
                "Cross-browser validation",
            ],
            "CSS": [
                "Lint: stylelint",
                "Check responsiveness",
                "Accessibility contrast check",
            ],
        }

        # Append deployment reminder as comments

        extra_section = f"\n\n{comment_symbol} ⚠️ Code has been auto-corrected. Please review before deployment.\n\n"
        extra_section += f"{comment_symbol} ✅ Pre-Deployment Checklist for {language}:\n"
        for item in checklist.get(language, ["Review code manually", "Run tests", "Run security scans"]):
            extra_section += f"{comment_symbol} - {item}\n"
        extra_section += f"\n{comment_symbol} 🚫 Do NOT deploy until all above checks pass successfully.\n"

        return result.strip() + "\n" + extra_section

    except requests.exceptions.RequestException as e:
        return f"{comment_symbol} Error linting {file_path}: {e}"


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

        overwrite_file(file_path, result)
        print(f"✅ Lint results applied to {file_path}")

        # Run basic pre-checks for all languages
        language, _ = detect_language(file_path)
        checks = run_basic_checks(file_path, language)
        for cmd in checks:
            print(f"[CHECK] Running: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Check failed: {e}")
                deployment_blocked = True

        # If the AI inserted fixes, block deployment
        if "Code has been auto-corrected" in result:
            deployment_blocked = True

    if deployment_blocked:
        print("\n🚫 Deployment blocked!")
        print("⚠️ Code had bugs or checks failed.")
        print("✅ Please review the code manually and run the pre-deployment checklist.")
        print("➡️ After verification, rerun deployment.\n")
    else:
        print("\n✅ Code passed without auto-fixes. Safe to deploy!\n")
        # Example: trigger deployment here
        # subprocess.run(["./deploy.sh"])


if __name__ == "__main__":
    main()
