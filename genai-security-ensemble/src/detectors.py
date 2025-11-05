from typing import Tuple
import numpy as np
from sklearn.ensemble import IsolationForest

# Dangerous keywords used by the keyword detector
DANGEROUS_KEYWORDS = [
    "bypass","exfiltrate","disable audit","password","secrets",
    "ignore previous","escalate privileges","dump","brute-force","leak"
]

def keyword_risk(text: str) -> bool:
    """Return True if any dangerous keyword is found in the text."""
    t = text.lower()
    return any(k in t for k in DANGEROUS_KEYWORDS)

class AnomalyDetector:
    """Wrapper around IsolationForest for embedding-based anomaly detection."""
    def __init__(self, contamination: float = 0.15, random_state: int = 42):
        self.clf = IsolationForest(contamination=contamination, random_state=random_state)

    def fit(self, X: np.ndarray):
        """Fit the IsolationForest on embeddings matrix X."""
        self.clf.fit(X)

    def score(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute anomaly decision_function and predictions.
        Returns:
            decision_scores: higher => more normal, lower => more anomalous
            predictions: 1 for normal, -1 for anomaly
        """
        return self.clf.decision_function(X), self.clf.predict(X)  # score, pred
