from __future__ import annotations

def build_model(users: int, products: int, categories: int, brands: int, text_dim: int, embedding_dim: int = 16):
    """TODO ML-006: Build a PyTorch two-tower module.

    OBJECTIVE: Create a custom nn.Module with user and product encoders.
    CONTEXT: Two towers learn a shared space for fast retrieval.
    YOUR TASK:
      1. Declare your own nn.Module; factory returns it; no prebuilt recommender.
      2. User encoder combines user-ID embedding and mean of product-ID history embeddings, masking -1 padding.
      3. Product encoder combines product, category and brand embeddings, normalized price and text vector via a learned projection.
      4. forward(user_ids, history, product_ids, category_ids, brand_ids, prices, text) returns normalized user/product embeddings [B,D].
    INPUT: IDs [B], padded history [B,H], prices [B,1], text [B,T]
    EXPECTED OUTPUT: Tuple of finite normalized tensors ([B,D], [B,D])
    CONCEPTS AND DOCUMENTATION HINTS: nn.Embedding; nn.Linear; torch.cat; padding masks; F.normalize; autograd
    EDGE CASES: Empty history; batch of one; category/brand cardinalities; zero vectors
    ACCEPTANCE CRITERIA: Features affect representations; gradients reach both towers; shape tests pass
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_006 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-006")
