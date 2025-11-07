import json
from pathlib import Path

LOG_PATH = "security_events.jsonl"

def fetch_flags(limit: int = 50):
    p = Path(LOG_PATH)
    if not p.exists():
        print("No logs found.")
        return []
    flags = []
    with p.open() as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("decision") == "FLAG":
                flags.append(obj)
    return flags[-limit:]

if __name__ == "__main__":
    flags = fetch_flags()
    if not flags:
        print("No FLAG events.")
    else:
        for f in flags:
            print("TIME:", f["time"])
            print("TEXT:", f["text"])
            print("META:", f["meta"])
            print("-" * 40)
