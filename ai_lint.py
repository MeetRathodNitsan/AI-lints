import os
import requests

files_to_check = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                code = f.read()
            files_to_check.append({"file": path, "code": code})

# Send all files to your FastAPI lint service
resp = requests.post("http://localhost:8000/lint", json={"files": files_to_check})
resp.raise_for_status()
result = resp.json()

print("=== AI Lint Suggestions ===")
for fix in result.get("fixes", []):
    print(f"\nFile: {fix['file']}")
    print("Old Code:\n", fix["old_code"])
    print("New Code:\n", fix["new_code"])
    print("Explanation:", fix["explanation"])
