import re
import yaml
from typing import Dict, Any

# Load policy file (policy-as-code)
def load_policy(path: str = "policies/llm_policy.yml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

POLICY = load_policy()

# Basic sanitizer: redact emails, phone numbers, and AWS keys (example)
RE_PATTERNS = {
    "email": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
    "phone": re.compile(r"(\+?\d{7,15})"),
    "aws_key": re.compile(r"AKIA[0-9A-Z]{16}")
}

def redact_pii(text: str) -> str:
    t = text
    for name, pat in RE_PATTERNS.items():
        t = pat.sub(f"[REDACTED_{name.upper()}]", t)
    return t

# Basic prompt injection heuristics
INJECTION_INDICATORS = POLICY.get("injection_indicators", [])

def detect_injection(text: str) -> Dict[str, Any]:
    t = text.lower()
    found = [ind for ind in INJECTION_INDICATORS if ind in t]
    return {"injection": len(found) > 0, "found": found}

# Post-generation output policy checks (e.g., leak detection)
OUTPUT_RULES = POLICY.get("output_rules", {})

def check_output_policy(output_text: str) -> Dict[str, Any]:
    """Check the generated output against policy rules and return issues."""
    issues = []
    ot = output_text.lower()
    # example rule: do not output emails or secrets
    if OUTPUT_RULES.get("no_pii", True):
        for name, pat in RE_PATTERNS.items():
            if pat.search(output_text):
                issues.append({"type": "pii", "detail": name})
    # example rule: ban some toxic words
    banned = OUTPUT_RULES.get("banned_terms", [])
    for term in banned:
        if term in ot:
            issues.append({"type": "banned_term", "detail": term})
    return {"issues": issues, "blocked": len(issues) > 0}
