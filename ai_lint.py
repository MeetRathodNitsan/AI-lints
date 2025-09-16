import os
import requests
import sys

# --- Collect all Python files in the project
files_to_check = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            files_to_check.append({"file": path, "code": code})

if not files_to_check:
    print("⚠️ No Python files found to lint.")
    sys.exit(0)

# --- Send files to FastAPI lint endpoint
try:
    resp = requests.post("http://localhost:8000/lint", json={"files": files_to_check})
    resp.raise_for_status()
except requests.exceptions.RequestException as e:
    print("❌ Failed to contact lint service:", e)
    sys.exit(1)

result = resp.json()

# --- Print AI lint results
fixes = result.get("fixes", [])
if not fixes:
    print("✅ No fixes suggested by AI.")
else:
    print("=== AI Lint Suggestions ===")
    for fix in fixes:
        print(f"\nFile: {fix['file']}")
        print("----- Old Code -----\n", fix["old_code"])
        print("----- New Code -----\n", fix["new_code"])
        print("Explanation:", fix["explanation"])
