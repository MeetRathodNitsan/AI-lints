import subprocess
import requests


try:
    diff = subprocess.check_output(["git", "diff", "HEAD~1", "HEAD"]).decode()
except subprocess.CalledProcessError:
    # Fallback: just check current working directory changes
    diff = subprocess.check_output(["git", "diff"]).decode()

if not diff.strip():
    print("No changes found to lint.")
    exit()

resp = requests.post("http://localhost:8000/lints", json={"diff": diff})
result = resp.json()

print("===AI Lint Suggestions====")
for fix in result["fixes"]:
    print(f"\nFile: {fix['file']}")
    print("Old Code:\n", fix["old_code"])
    print("New Code:\n", fix["new_code"])
    print("Explanation:", fix["explanation"])