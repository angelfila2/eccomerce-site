"""Small synthetic fixtures: correctness contracts, never performance claims."""
import math
import random

import numpy as np
import pytest


def test_ML_001():
    from app.recommendations.popularity import popularity

    events = [dict(product_id="old", kind="view", timestamp=0),
              dict(product_id="new", kind="view", timestamp=100),
              dict(product_id="future", kind="purchase", timestamp=200)]
    assert popularity(events, now=100, half_life=100) == ["new", "old"]
    assert popularity([], now=100) == []
    assert popularity(events[:2], now=100, weights={"view": 2}) == ["new", "old"]
    with pytest.raises(ValueError):
        popularity(events, now=100, half_life=0)


def test_ML_002():
    from app.recommendations.content_based import vectorize

    vectorizer, matrix = vectorize(["Desk reading lamp", "Desk reading lamp", "Cotton travel bag"])
    assert matrix.shape[0] == 3 and matrix.shape[1] == len(vectorizer.vocabulary_)
    np.testing.assert_allclose(matrix[0].toarray(), matrix[1].toarray())
    assert (matrix[0] @ matrix[2].T).toarray().item() == 0
    for invalid in ([], ["", "  "]):
        with pytest.raises(ValueError):
            vectorize(invalid)


def test_ML_003():
    from app.recommendations.similarity import similar_indices

    matrix = np.array([[1., 0.], [.9, .1], [0., 1.]])
    assert similar_indices(matrix, seed_index=0, limit=2) == [1, 2]
    assert similar_indices(matrix, seed_index=0, limit=0) == []
    assert similar_indices(matrix[:1], seed_index=0, limit=4) == []
    for index, limit in ((3, 2), (-1, 2), (0, -1)):
        with pytest.raises(ValueError):
            similar_indices(matrix, index, limit)


def test_ML_004():
    from app.recommendations.semantic_store import nearest_vectors

    # Guard tests do not require downloading models or running PostgreSQL.
    for invalid in ([1., 2.], [float("nan")] * 384, [float("inf")] * 384):
        with pytest.raises(ValueError):
            nearest_vectors(None, invalid)
    with pytest.raises(ValueError):
        nearest_vectors(None, [1.] * 384, limit=-1)
    # Valid-query acceptance additionally requires pgvector integration; see task card.


def test_ML_005():
    from scipy.sparse import csr_matrix
    from app.recommendations.collaborative import collaborative_scores

    matrix = csr_matrix([[1., 0., 0.], [1., 1., 0.], [0., 0., 1.], [0., 0., 0.]])
    scores = collaborative_scores(matrix, user_index=0)
    assert len(scores) == 3 and scores[0] == 0 and scores[1] > scores[2]
    assert all(math.isfinite(value) and value >= 0 for value in scores)
    assert collaborative_scores(matrix, user_index=3) == [0., 0., 0.]
    with pytest.raises(ValueError):
        collaborative_scores(csr_matrix([[-1., 0.]]), 0)


def torch_inputs(torch):
    return (torch.tensor([0, 1]), torch.tensor([[1, -1], [-1, -1]]),
            torch.tensor([1, 2]), torch.tensor([0, 1]), torch.tensor([0, 1]),
            torch.tensor([[.2], [.8]]), torch.ones(2, 8))


def test_ML_006():
    torch = pytest.importorskip("torch", reason="Install the optional ml dependency group")
    from app.recommendations.two_tower import build_model

    torch.manual_seed(7)
    model = build_model(users=2, products=4, categories=2, brands=2, text_dim=8, embedding_dim=16)
    assert isinstance(model, torch.nn.Module)
    users, products = model(*torch_inputs(torch))
    assert users.shape == products.shape == (2, 16)
    assert torch.isfinite(users).all() and torch.isfinite(products).all()
    torch.testing.assert_close(users.norm(dim=1), torch.ones(2))
    torch.testing.assert_close(products.norm(dim=1), torch.ones(2))
    (users * products).sum().backward()
    assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in model.parameters())


def test_ML_007():
    from app.recommendations.sampling import sample_negatives

    seen = {0, 1}
    global_state = random.getstate()
    result = sample_negatives(seen, product_count=8, count=4, seed=7)
    assert result == sample_negatives(seen, 8, 4, 7)
    assert len(set(result)) == 4 and not seen.intersection(result)
    assert all(0 <= item < 8 for item in result)
    assert seen == {0, 1} and random.getstate() == global_state
    assert sample_negatives(seen, 8, 0, 7) == []
    with pytest.raises(ValueError):
        sample_negatives({0, 1}, 2, 1, 7)


def test_ML_008(tmp_path):
    torch = pytest.importorskip("torch", reason="Install the optional ml dependency group")
    from app.recommendations.training import load_model, train_model
    from app.recommendations.two_tower import build_model

    torch.manual_seed(7)
    model = build_model(2, 4, 2, 2, 8, 16)
    before = {name: parameter.detach().clone() for name, parameter in model.named_parameters()}
    checkpoint = tmp_path / "synthetic-development.pt"
    batches = [torch_inputs(torch)]
    history = train_model(model, batches, batches, epochs=2, learning_rate=.01,
                          checkpoint=str(checkpoint), seed=7)
    assert checkpoint.is_file()
    assert len(history["train_loss"]) == len(history["validation_loss"]) == 2
    assert all(math.isfinite(loss) for loss in history["train_loss"] + history["validation_loss"])
    assert any(not torch.equal(before[name], value) for name, value in model.named_parameters())
    assert torch.load(checkpoint, weights_only=True)["state_dict"]
    restored = load_model(str(checkpoint))
    assert not restored.training
    assert load_model(str(checkpoint)) is restored
    assert all(torch.equal(value, restored.state_dict()[name])
               for name, value in torch.load(checkpoint, weights_only=True)["state_dict"].items())
    with torch.no_grad():
        user_vectors, product_vectors = restored(*torch_inputs(torch))
    assert user_vectors.shape == product_vectors.shape == (2, 16)
    assert torch.isfinite((user_vectors * product_vectors).sum(dim=1)).all()
    with pytest.raises(FileNotFoundError):
        load_model(str(tmp_path / "missing.pt"))


def test_ML_009():
    from app.recommendations.evaluation import evaluate_rankings, temporal_split

    result = evaluate_rankings({"u1": ["a", "b"], "u2": ["c", "a"]},
                               {"u1": {"a"}, "u2": {"a"}}, {"a", "b", "c", "d"}, k=2)
    assert result["recall"] == 1.
    assert result["precision"] == .5
    assert result["hit_rate"] == 1.
    assert result["coverage"] == .75
    assert result["ndcg"] == pytest.approx((1 + 1 / math.log2(3)) / 2)
    missing = evaluate_rankings({}, {"u1": {"a"}}, {"a"}, k=10)
    assert all(value == 0 for value in missing.values())
    events = [{"timestamp": time} for time in (0, 10, 20, 30)]
    train, validation, test = temporal_split(events, train_end=10, validation_end=20)
    assert [e["timestamp"] for e in train] == [0]
    assert [e["timestamp"] for e in validation] == [10]
    assert [e["timestamp"] for e in test] == [20, 30]
    with pytest.raises(ValueError):
        evaluate_rankings({}, {}, set(), k=0)


def test_ML_010():
    from app.recommendations.hybrid import fuse

    rankings = [["a", "b", "c", "sold", "old"], ["b", "a", "c", "d"]]
    available = {"a", "b", "c", "d", "old"}
    categories = {"a": "Desk", "b": "Desk", "c": "Desk", "d": "Carry"}
    result = fuse(rankings, available, {"old"}, categories, limit=3)
    assert result == ["a", "b", "d"]
    assert fuse([[]], available, set(), categories) == []
    assert fuse([["a", "a", "b"]], available, set(), categories, 4) == ["a", "b"]
    assert fuse(rankings, available, {"old"}, categories, 0) == []
    with pytest.raises(ValueError):
        fuse(rankings, available, set(), categories, -1)


def test_ML_011():
    from app.recommendations.cooccurrence import frequently_bought

    orders = [["lamp", "desk", "desk"], ["lamp", "bag"], ["lamp", "desk"], ["bag", "mat"]]
    assert frequently_bought(orders, "lamp") == ["desk", "bag"]
    assert frequently_bought(orders, "missing") == []
    assert frequently_bought(orders, "lamp", limit=0) == []
    with pytest.raises(ValueError):
        frequently_bought(orders, "lamp", limit=-1)
