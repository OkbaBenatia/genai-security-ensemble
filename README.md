# GenAI Security Ensemble (LLM Firewall)

A lightweight **LLM security firewall** that combines:
- Keyword detection
- Embedding-based anomaly detection (IsolationForest)
- Zero-shot intent classification (BART MNLI)
- FastAPI endpoint + JSONL logging

## Features
- `POST /guard/inspect` → returns `ALLOW | FLAG | BLOCK` with metadata
- Pluggable thresholds and seeds
- Easy to extend with guardrails / PII redaction

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.app:app --reload
