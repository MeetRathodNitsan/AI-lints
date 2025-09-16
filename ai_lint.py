import subprocess
import requests
import sys

def get_diff():
    try:
        # Compare last two commits
        return subprocess.check_output(["git", "diff", "HEAD~1", "HEAD"]).decode()
    except subprocess.CalledProcessError:
        try:
            # Fallback: current unstaged changes
            return subprocess.check_output(["git", "diff"]).decode()
        except subprocess.CalledProcessError:
            return ""

diff = get_diff()

if not diff.strip():
    print("⚠️ No changes found to lint.")
    sys.exit(0)

# Send diff to FastAPI lint service
resp = requests.post("http://localhost:8000/lint", json={"diff": diff})
resp.raise_for_status()
result = resp.json()

print("=== AI Lint Suggestions ===")
for fix in result.get("fixes", []):
    print(f"\nFile: {fix['file']}")
    print("Old Code:\n", fix["old_code"])
    print("New Code:\n", fix["new_code"])
    print("Explanation:", fix["explanation"])
