import os, numpy as np, datetime
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pathlib import Path

from models import load_embed_model, load_zero_shot
from detectors import AnomalyDetector, keyword_risk
from pipelines import ensemble_decision
from logging_utils import log_event

load_dotenv()
LOG_PATH = os.getenv("LOG_PATH", "security_events.jsonl")

app = FastAPI(title="GenAI Security Ensemble", version="0.1.0")

# --- bootstrap seeds ---
BENIGN = Path("data/benign_seed.txt").read_text().strip().splitlines()
MAL    = Path("data/malicious_seed.txt").read_text().strip().splitlines()

# load models
embed_model = load_embed_model()
zclf        = load_zero_shot()
anom        = AnomalyDetector(contamination=0.15)
X = embed_model.encode(BENIGN + MAL)
anom.fit(X)

@app.post("/guard/inspect")
def inspect(payload: dict):
    text = payload.get("text","").strip()
    if not text:
        raise HTTPException(400, "text is required")

    result = ensemble_decision(text, embed_model, zclf, anom, keyword_risk)
    log_event(LOG_PATH, text, result["decision"], result["meta"])
    return result

@app.get("/health")
def health():
    return {"ok": True, "time": datetime.datetime.utcnow().isoformat() + "Z"}
