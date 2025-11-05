from src.models import load_embed_model, load_zero_shot
from src.detectors import AnomalyDetector, keyword_risk
from src.pipelines import ensemble_decision

def test_decision_runs():
    embed = load_embed_model()
    zclf  = load_zero_shot()
    anom  = AnomalyDetector(contamination=0.15)
    X = embed.encode(["Deploy Docker", "Exfiltrate secrets"])
    anom.fit(X)

    res = ensemble_decision("How to deploy Docker?", embed, zclf, anom, keyword_risk)
    assert res["decision"] in {"ALLOW","FLAG","BLOCK"}
