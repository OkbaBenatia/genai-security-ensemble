from typing import Dict, Tuple
import numpy as np

# Thresholds — tune these in your experiments
SCORE_THRESH_MALICIOUS = 0.70     # zero-shot: malicious high confidence
IFOREST_SCORE_THRESH   = -0.05    # lower => more anomalous

def classify_intent(zclf, text: str) -> Tuple[str, float]:
    """Use zero-shot classifier to infer intent label and score."""
    labels = ["benign", "suspicious", "malicious"]
    res = zclf(text, candidate_labels=labels, multi_label=False)
    return res["labels"][0], float(res["scores"][0])

def ensemble_decision(text: str, embed_model, zclf, anomaly_detector, keyword_fn) -> Dict:
    """
    Combine keyword detector, zero-shot intent, and anomaly detector
    to return a decision dict: { decision: ALLOW|FLAG|BLOCK, meta: {...} }.
    """
    kw = keyword_fn(text)
    emb = embed_model.encode([text])
    iso_score, iso_pred = anomaly_detector.score(emb)
    iso_score, iso_pred = float(iso_score[0]), int(iso_pred[0])

    intent, intent_score = classify_intent(zclf, text)

    if intent == "malicious" and intent_score >= SCORE_THRESH_MALICIOUS:
        decision = "BLOCK"; reason = "intent_malicious_high_conf"
    elif kw and iso_pred == -1:
        decision = "BLOCK"; reason = "keyword_and_anomaly"
    elif intent == "suspicious" or iso_score < IFOREST_SCORE_THRESH:
        decision = "FLAG";  reason = "suspicious_or_iso"
    else:
        decision = "ALLOW"; reason = "low_risk"

    return {
        "decision": decision,
        "meta": {
            "intent_label": intent,
            "intent_score": round(intent_score, 3),
            "iso_score": round(iso_score, 3),
            "keyword": kw,
            "reason": reason
        }
    }
