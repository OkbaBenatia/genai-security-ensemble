from sentence_transformers import SentenceTransformer
from transformers import pipeline

def load_embed_model(name: str = "all-MiniLM-L6-v2"):
    """Load and return a SentenceTransformer model for embeddings."""
    return SentenceTransformer(name)

def load_zero_shot(model: str = "facebook/bart-large-mnli"):
    """Load and return a zero-shot classification pipeline."""
    return pipeline("zero-shot-classification", model=model)
