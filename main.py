from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class DiffInput(BaseModel):
    diff: str

@app.post("/lint")
def lint_code(input: DiffInput):
    prompt = f"""
You are an AI code linter.
You will be given a Git diff. 
Return ONLY valid JSON in this format:

{{
  "fixes": [
    {{
      "file": "FILENAME",
      "old_code": "OLD CODE SNIPPET",
      "new_code": "NEW FIXED CODE SNIPPET",
      "explanation": "WHY THIS FIX WAS MADE"
    }}
  ]
}}

Diff:
{input.diff}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:7b-instruct-q4_k_m",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0},  # make output deterministic
            },
            timeout=60,
        )

        raw_output = response.json().get("response", "").strip()

        # Try to extract JSON only
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        json_str = raw_output[start:end]

        fixes = json.loads(json_str)  # ✅ safe parsing

    except Exception as e:
        fixes = {
            "fixes": [
                {
                    "file": "unknown",
                    "old_code": "",
                    "new_code": "",
                    "explanation": f"Error parsing AI response: {str(e)}. Raw output: {raw_output}",
                }
            ]
        }

    return fixes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)