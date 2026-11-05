"""Product text construction and semantic embedding generation."""

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from app.catalog.schemas import ProductResponse


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load and reuse one transformer model instance."""
    return SentenceTransformer(MODEL_NAME)


def build_product_text(product: ProductResponse) -> str:
    """Combine fields into the text encoded by the embedding model."""
    details = ". ".join(product.details)

    return (
        f"Product: {product.name}. "
        f"Category: {product.category}. "
        f"Description: {product.description}. "
        f"Details: {details}."
    )


def encode_product_texts(texts: list[str]) -> list[list[float]]:
    """Return one normalized semantic vector per product text."""
    if not texts:
        return []
    model = get_embedding_model()

    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return np.asarray(vectors, dtype=np.float32).tolist()
