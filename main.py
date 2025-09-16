from fastapi import FastAPI, Response
from pydantic import BaseModel
import requests

app = FastAPI()

class DiffInput(BaseModel):
    diff: str

@app.post("/lint")
def lint_code(input: DiffInput):
    # Create prompt for AI
    prompt = f"""
You are an AI code linter.
You will be given a Git diff.
Return ONLY plain text, in this format:

Mistake:
<the buggy code snippet or issue>

Corrected:
<the fully fixed code>

Explanation:
<the explanation of the corrected code snippet>


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
                "options": {"temperature": 0},  # deterministic
            },
            timeout=60,
        )

        # Get AI output
        raw_output = response.json().get("response", "").strip()

        # Return as plain text
        return Response(content=raw_output, media_type="text/plain")

    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
