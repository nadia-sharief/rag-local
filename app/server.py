import os, requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Minimal .env loader (no extra deps)
def load_env():
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
load_env()

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://127.0.0.1:11434")
MODEL = os.getenv("MODEL", "phi3:mini")
PORT = int(os.getenv("RAG_PORT", "5001"))

app = FastAPI(title="RAG Local (Ollama)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskReq(BaseModel):
    q: str

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL, "ollama": OLLAMA_BASE}

@app.post("/api/ask")
def ask(req: AskReq):
    payload = {"model": MODEL, "prompt": req.q, "stream": False}
    r = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return {"answer": data.get("response", ""), "model": data.get("model")}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)

