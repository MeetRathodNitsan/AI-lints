from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class DiffInput(BaseModel):
    diff: str

@app.post("/lints")
def lint_code(input: DiffInput):
    prompt = f"""
    You are an AI code linter.
    Given the following Git diff, detect issues and return JSON strictly in the following format:
        {{
        "fixes": [
        {{
        "file": "FILENAME",
        "old_code": "OLD CODE SNIPPET",
        "new_code": "NEW CODE SNIPPET",
        "explanation": "WHY THIS FIX WAS MADE"
        }}
      ]
    }}
    Diff:
    {input.diff}"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b-instruct-q4_k_m",
            "prompt": prompt,
            "stream": False
        },
    )
    output = response.json()["response"]
    try:
        fixes = eval(output)
    except Exception:
        fixes = {"fixes":[{"file":"unknown", "old_code":"", "new_code":"", "explanation":output}]}

    return fixes