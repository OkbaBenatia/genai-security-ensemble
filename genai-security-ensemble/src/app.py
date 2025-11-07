import os, numpy as np, datetime
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pathlib import Path

from models import load_embed_model, load_zero_shot
from detectors import AnomalyDetector, keyword_risk
from pipeline import ensemble_decision, postprocess_output
from logging_utils import log_event
from guardrails import redact_pii

load_dotenv()
LOG_PATH = os.getenv("LOG_PATH", "security_events.jsonl")

app = FastAPI(title="GenAI Security Ensemble", version="0.2.0")  # bump version

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

    # run ensemble (with input sanitization & injection detection)
    result = ensemble_decision(text, embed_model, zclf, anom, keyword_risk)
    # log sanitized input (not raw)
    sanitized = redact_pii(text)
    log_event(LOG_PATH, sanitized, result["decision"], result["meta"])

    # If allowed, optionally call the LLM (this app doesn't call an LLM by default)
    return result

@app.post("/guard/generate")
def generate(payload: dict):
    """
    Example endpoint that would call an LLM with safe pipeline:
    - check ensemble decision
    - if ALLOW => call model (user responsible for model integration)
    - run postprocess_output to enforce output policy
    """
    text = payload.get("text","").strip()
    if not text:
        raise HTTPException(400, "text is required")

    result = ensemble_decision(text, embed_model, zclf, anom, keyword_risk)
    sanitized = redact_pii(text)
    log_event(LOG_PATH, sanitized, result["decision"], result["meta"])

    if result["decision"] == "BLOCK":
        raise HTTPException(403, "Request blocked by guardrails")

    # Here: user must integrate their LLM client (OpenAI, vLLM, etc.)
    # For example (pseudocode):
    # llm_output = call_llm_model(sanitized, system_prompt=SAFE_SYSTEM_PROMPT)
    # For this scaffold we'll simulate a safe response:
    llm_output = "SIMULATED LLM ANSWER based on allowed context."

    # postprocess the generated output
    post_res = postprocess_output(llm_output)
    if not post_res["allowed"]:
        log_event(LOG_PATH, "[REDACTED OUTPUT]", "blocked_output", post_res)
        raise HTTPException(500, "Generated output violated output policy")
    # log allowed output (but redacted)
    log_event(LOG_PATH, "[REDACTED OUTPUT]", "allowed_output", post_res)
    return {"answer": llm_output}
