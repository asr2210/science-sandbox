"""
surrogate.py — Surrogate model training pipeline.

Trains a fresh BassetBranched model (same architecture as Malinois) on
oracle-labeled sequences, then evaluates on held-out test sets.

Public API
----------
    from eval.surrogate import train_and_eval

    metrics = train_and_eval(
        train_sequences = [...],        # list[str], ~200bp DNA
        train_labels    = array,        # (N, 3) float32 log2FC from oracle
        test_sets       = {
            "chr7_13": (test_seqs, test_labels),
        },
        seed = 0,
    )
    # metrics["chr7_13"]["mean_pearson"]  -> float
"""

import os
import sys
import time
import math
import random
import warnings

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from scipy.stats import pearsonr, spearmanr

# boda2 submodule at repo root
_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'boda2')
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from boda.model.basset import BassetBranched
import boda.common.constants as _const
import boda.common.utils as _boda_utils

_CHECKPOINT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'data', 'malinois', 'artifacts', 'torch_checkpoint.pt'
)

# Locked training config — exact values from Malinois checkpoint
BATCH_SIZE          = 512
MAX_EPOCHS          = 200
EARLY_STOP_PATIENCE = 20
VAL_FRACTION        = 0.10

OPTIMIZER_CONFIG = dict(
    lr           = 0.0032658700881052086,
    eps          = 1e-8,
    weight_decay = 0.0003438210249762151,
    amsgrad      = True,
    betas        = (0.8661062881299633, 0.879223105336538),
)

SCHEDULER_T0   = 4096
SCHEDULER_TMUL = 1
SCHEDULER_EMIN = 0.0

CELL_TYPES = ['K562', 'HepG2', 'SKNSH']

_MODEL_HPARAMS = None

def _get_model_hparams() -> dict:
    global _MODEL_HPARAMS
    if _MODEL_HPARAMS is None:
        if not os.path.isfile(_CHECKPOINT):
            raise FileNotFoundError(f"Checkpoint not found: {_CHECKPOINT}\nRun setup.sh first.")
        ckpt = torch.load(_CHECKPOINT, map_location='cpu', weights_only=False)
        _MODEL_HPARAMS = vars(ckpt['model_hparams'])
    return _MODEL_HPARAMS


_NT_TABLE = np.zeros(256, dtype=np.uint8)
for _c, _i in [('A',0),('C',1),('G',2),('T',3),('a',0),('c',1),('g',2),('t',3)]:
    _NT_TABLE[ord(_c)] = _i

_LEFT_FLANK  = None
_RIGHT_FLANK = None

def _get_flanks():
    global _LEFT_FLANK, _RIGHT_FLANK
    if _LEFT_FLANK is None:
        hparams = _get_model_hparams()
        pad_total = hparams['input_len'] - 200
        left_len  = pad_total // 2
        right_len = pad_total - left_len
        _LEFT_FLANK  = _boda_utils.dna2tensor(_const.MPRA_UPSTREAM[-left_len:]).numpy()
        _RIGHT_FLANK = _boda_utils.dna2tensor(_const.MPRA_DOWNSTREAM[:right_len]).numpy()
    return _LEFT_FLANK, _RIGHT_FLANK


def encode_sequences(sequences: list) -> torch.Tensor:
    """Encode DNA strings → (N, 4, 600) one-hot float32 tensor with MPRA flanks."""
    n = len(sequences)
    if n == 0:
        return torch.zeros((0, 4, 600), dtype=torch.float32)

    left_flank, right_flank = _get_flanks()

    padded = [s[:200].ljust(200, 'A') for s in sequences]
    raw_bytes = np.frombuffer(''.join(padded).encode('ascii'), dtype=np.uint8)
    nt_idx = _NT_TABLE[raw_bytes].reshape(n, 200)

    cores = np.eye(4, dtype=np.float32)[nt_idx]
    cores = np.ascontiguousarray(cores.transpose(0, 2, 1))

    left_tiled  = np.broadcast_to(left_flank[None],  (n, 4, 200))
    right_tiled = np.broadcast_to(right_flank[None], (n, 4, 200))
    full = np.concatenate([left_tiled, cores, right_tiled], axis=2)

    return torch.from_numpy(np.ascontiguousarray(full))


def _set_seeds(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark     = False


def _evaluate(model: nn.Module, X: torch.Tensor, Y: np.ndarray,
              device: torch.device) -> dict:
    model.eval()
    preds_list = []
    with torch.no_grad():
        for start in range(0, len(X), BATCH_SIZE):
            batch = X[start : start + BATCH_SIZE].to(device)
            preds_list.append(model(batch).cpu().float().numpy())
    preds = np.concatenate(preds_list, axis=0)

    pearson_r  = {}
    spearman_r = {}
    for i, ct in enumerate(CELL_TYPES):
        mask = np.isfinite(Y[:, i]) & np.isfinite(preds[:, i])
        pr, _  = pearsonr( Y[mask, i], preds[mask, i])
        sr, _  = spearmanr(Y[mask, i], preds[mask, i])
        pearson_r[ct]  = float(pr)
        spearman_r[ct] = float(sr)

    return {
        'pearson':       pearson_r,
        'spearman':      spearman_r,
        'mean_pearson':  float(np.mean(list(pearson_r.values()))),
        'mean_spearman': float(np.mean(list(spearman_r.values()))),
        'n':             int(len(X)),
    }


def train_and_eval(
    train_sequences:  list,
    train_labels:     np.ndarray,
    test_sets:        dict,
    seed:             int  = 0,
    save_checkpoint:  str | None = None,
) -> dict:
    """
    Train a fresh BassetBranched on oracle-labeled sequences, evaluate on test sets.

    Parameters
    ----------
    train_sequences : list[str]
        Raw ~200bp DNA strings for training.
    train_labels : np.ndarray, shape (N, 3)
        Oracle log2FC predictions [K562, HepG2, SKNSH].
    test_sets : dict[str, tuple[list[str], np.ndarray]]
        Named evaluation sets: {name: (sequences, labels)}.
    seed : int
        Controls all randomness. Same seed + same data = identical metrics.
    save_checkpoint : str | None
        If provided, save best model weights to this path.

    Returns
    -------
    dict with training metadata and per-test-set metrics.
    """
    t_start = time.perf_counter()
    _set_seeds(seed)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    train_labels = np.asarray(train_labels, dtype=np.float32)

    X_all = encode_sequences(train_sequences)
    Y_all = torch.from_numpy(train_labels)

    n_total = len(X_all)
    n_val   = max(1, round(n_total * VAL_FRACTION))
    n_train = n_total - n_val

    perm      = torch.randperm(n_total, generator=torch.Generator().manual_seed(seed))
    train_idx = perm[:n_train]
    val_idx   = perm[n_train:]

    X_train = X_all[train_idx].to(device)
    Y_train = Y_all[train_idx].to(device)
    X_val   = X_all[val_idx].to(device)
    Y_val   = Y_all[val_idx].to(device)

    train_loader = DataLoader(TensorDataset(X_train, Y_train), batch_size=BATCH_SIZE,
                              shuffle=True, num_workers=0,
                              generator=torch.Generator().manual_seed(seed))
    val_loader   = DataLoader(TensorDataset(X_val, Y_val), batch_size=BATCH_SIZE,
                              shuffle=False, num_workers=0)

    _set_seeds(seed)
    model = BassetBranched(**_get_model_hparams()).to(device)
    criterion = model.criterion

    optimizer = torch.optim.Adam(model.parameters(), **OPTIMIZER_CONFIG)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer, T_0=SCHEDULER_T0, T_mult=SCHEDULER_TMUL, eta_min=SCHEDULER_EMIN,
    )

    best_val_loss  = float('inf')
    patience_ctr   = 0
    best_state     = None
    best_train_loss= float('nan')
    epoch_log      = []

    for epoch in range(MAX_EPOCHS):
        model.train()
        running_loss = 0.0
        for X_b, Y_b in train_loader:
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(X_b), Y_b)
            loss.backward()
            optimizer.step()
            scheduler.step()
            running_loss += loss.item() * len(X_b)
        train_loss = running_loss / n_train

        model.eval()
        val_running = 0.0
        with torch.no_grad():
            for X_b, Y_b in val_loader:
                val_running += criterion(model(X_b), Y_b).item() * len(X_b)
        val_loss = val_running / n_val

        epoch_log.append((train_loss, val_loss))

        if val_loss < best_val_loss:
            best_val_loss   = val_loss
            best_train_loss = train_loss
            patience_ctr    = 0
            best_state      = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            patience_ctr += 1
            if patience_ctr >= EARLY_STOP_PATIENCE:
                break

    model.load_state_dict(best_state)
    model.eval()

    if save_checkpoint is not None:
        os.makedirs(os.path.dirname(os.path.abspath(save_checkpoint)), exist_ok=True)
        torch.save(best_state, save_checkpoint)

    results = {}
    for name, (seqs, labels) in test_sets.items():
        X_ts = encode_sequences(seqs)
        Y_ts = np.asarray(labels, dtype=np.float32)
        results[name] = _evaluate(model, X_ts, Y_ts, device)

    return {
        'n_epochs':        len(epoch_log),
        'train_loss':      float(best_train_loss),
        'val_loss':        float(best_val_loss),
        'training_time_s': time.perf_counter() - t_start,
        'n_train':         n_train,
        'n_val':           n_val,
        **results,
    }
