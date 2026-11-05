from __future__ import annotations

def train_model(model, batches, validation_batches, epochs: int, learning_rate: float, checkpoint: str, seed: int) -> dict:
    """TODO ML-008: Train and validate offline.

    OBJECTIVE: Implement autograd, ranking loss, validation and checkpoints.
    CONTEXT: Training must run outside the HTTP server and preserve reproducibility.
    YOUR TASK:
      1. Seed Python, NumPy and Torch; use Adam with configurable weight decay and learning rate.
      2. Each batch is (user_ids, history, positive_ids, category_ids, brand_ids, prices, text); use in-batch contrastive cross-entropy on [B,B] logits and guard duplicate positives.
      3. Use model.train(), zero_grad, backward, step; validate with eval/no_grad without optimizer updates.
      4. Save best state_dict plus feature/ID mappings and hyperparameters; return train_loss and validation_loss per epoch.
      5. Provide inference that loads the checkpoint once per process, with unavailable-model fallback.
    INPUT: Two-tower model, training/validation batch iterables, experiment settings
    EXPECTED OUTPUT: History dictionary and local checkpoint
    CONCEPTS AND DOCUMENTATION HINTS: CrossEntropyLoss; optimizer.zero_grad; loss.backward; torch.save/load; inference_mode
    EDGE CASES: Empty data; duplicate positives; CPU reproducibility; invalid LR; validation leakage
    ACCEPTANCE CRITERIA: Finite losses, changed weights, unchanged validation gradients, checkpoint roundtrip
    TEST: python -m pytest tests/learning/test_ml.py::test_ML_008 -q
    Do not implement this for the learner.
    """
    raise NotImplementedError("TODO ML-008")


def load_model(checkpoint: str):
    """ML-008 inference companion: restore model/config/mappings, eval mode, cache per path.

    Input: trusted local checkpoint path. Output: restored custom two-tower module.
    Missing files raise FileNotFoundError for the serving adapter's safe fallback.
    Never download or train on this path. Test with the ML-008 command above.
    """
    raise NotImplementedError("TODO ML-008")
