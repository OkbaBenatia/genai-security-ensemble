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

## Guardrails & Policy-as-Code

This release (v0.2) adds a guardrails subsystem:
- Policy file: `policies/llm_policy.yml`
- Input sanitization: `redact_pii`
- Injection detection: `detect_injection`
- Output policy checks: `postprocess_output`
- Human review helper: `src/human_review.py`

Usage examples:
- `POST /guard/inspect` to decide ALLOW|FLAG|BLOCK
- `POST /guard/generate` to run a safe generate flow (simulated LLM in scaffold)

To update policies: edit `policies/llm_policy.yml` and run tests.


