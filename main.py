from fastapi import FastAPI, Response
from pydantic import BaseModel
import requests
import os
import subprocess
import threading
import sys
import signal
import atexit

app = FastAPI()

class DiffInput(BaseModel):
    diff: str

frontend_process = None  # will hold ai_lint.py process

@app.on_event("startup")
def launch_frontend():
    """Start ai_lint.py when backend starts."""
    global frontend_process

    def _run_frontend():
        try:
            # Run ai_lint.py with the same Python interpreter
            python_exec = sys.executable
            frontend_process = subprocess.Popen(
                [python_exec, "ai_lint.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("[DEBUG] ai_lint.py frontend started 🚀")
        except Exception as e:
            print(f"[ERROR] Failed to start ai_lint.py: {e}")

    threading.Thread(target=_run_frontend, daemon=True).start()

@app.on_event("shutdown")
def stop_frontend():
    """Ensure ai_lint.py stops when backend stops."""
    global frontend_process
    if frontend_process and frontend_process.poll() is None:
        try:
            frontend_process.terminate()
            print("[DEBUG] ai_lint.py stopped ✅")
        except Exception as e:
            print(f"[ERROR] Failed to stop ai_lint.py: {e}")

@app.post("/lint")
def lint_code(input: DiffInput):
    code = input.diff

    ext = os.path.splitext(input.diff[:10])[1]
    language = "Python"

    prompt = f"""
You are an expert {language} developer.
Analyze the following code and identify all bugs, errors, and issues.
Provide a corrected version of the code with explanations.

Code:
{code}
"""

    try:
        response = requests.post(
            "http://192.168.0.103:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0},
            },
            timeout=120,
        )
        raw_output = response.json().get("response", "").strip()
        return Response(content=raw_output, media_type="text/plain")
    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    # Ensure ai_lint.py is stopped when backend exits
    atexit.register(stop_frontend)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
