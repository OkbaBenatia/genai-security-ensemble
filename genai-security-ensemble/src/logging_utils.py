import json, os, datetime

def log_event(path: str, text: str, decision: str, meta: dict):
    """Append a JSONL entry for the security event."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    entry = {
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "text": text,
        "decision": decision,
        "meta": meta
    }
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")
