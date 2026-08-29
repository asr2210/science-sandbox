"""
oracle.py — Malinois inference oracle.

Wraps the pretrained Malinois model (BassetBranched) into a single clean function:

    label_sequences(sequences, batch_size=512) -> np.ndarray shape (N, 3)

Input:  list of N raw DNA strings (expected ~200bp; shorter strings are padded,
        longer strings are rejected)
Output: (N, 3) float32 array of log2FC predictions [K562, HepG2, SKNSH]

Handles one-hot encoding, MPRA flank padding, batching, and reverse-complement
averaging internally. Requires a GPU (falls back to CPU if unavailable).

Usage
-----
    from eval.oracle import label_sequences
    preds = label_sequences(["ACGT..." * 50, ...])  # list of 200bp strings
    # preds.shape == (N, 3)
    # preds[:,0] = K562 log2FC, preds[:,1] = HepG2, preds[:,2] = SKNSH
"""

import os
import sys
import warnings

import numpy as np
import torch
import torch.nn as nn

# boda2 submodule at repo root
_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'boda2')
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

import boda.common.constants as _constants
import boda.common.utils as _utils
from boda.model.basset import BassetBranched

_ARTIFACT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'data', 'malinois', 'artifacts'
)
_CHECKPOINT = os.path.join(_ARTIFACT_DIR, 'torch_checkpoint.pt')

_model = None
_flanker = None
_device = None


def _load_model_from_checkpoint(ckpt_path: str, device: torch.device) -> BassetBranched:
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model_cls = globals().get(ckpt['model_module'])
    if model_cls is None:
        raise RuntimeError(f"Unknown model_module '{ckpt['model_module']}' in checkpoint.")
    model = model_cls(**vars(ckpt['model_hparams']))
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()
    model.to(device)
    return model


def _build_flanker(input_len: int, device: torch.device) -> nn.Module:
    pad_total = input_len - 200
    left_len  = pad_total // 2
    right_len = pad_total - left_len

    left_flank  = _utils.dna2tensor(_constants.MPRA_UPSTREAM[-left_len:]).unsqueeze(0)
    right_flank = _utils.dna2tensor(_constants.MPRA_DOWNSTREAM[:right_len]).unsqueeze(0)
    flanker = _utils.FlankBuilder(left_flank, right_flank)
    flanker.to(device)
    return flanker


def _ensure_loaded():
    global _model, _flanker, _device

    if _model is not None:
        return

    if not os.path.isfile(_CHECKPOINT):
        raise FileNotFoundError(
            f"Checkpoint not found at {_CHECKPOINT}.\n"
            "Run setup.sh to download it:\n"
            "  bash setup.sh"
        )

    _device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"[oracle] Loading Malinois on {_device}...", flush=True)

    _model   = _load_model_from_checkpoint(_CHECKPOINT, _device)
    _flanker = _build_flanker(_model.input_len, _device)

    n_params = sum(p.numel() for p in _model.parameters())
    print(f"[oracle] Loaded BassetBranched — {n_params:,} params, input_len={_model.input_len}", flush=True)


def label_sequences(sequences: list, batch_size: int = 512) -> np.ndarray:
    """
    Predict log2FC activity for a list of raw DNA sequences.

    Parameters
    ----------
    sequences : list[str]
        Raw DNA strings. Expected length ~200bp. Strings shorter than 200bp
        are zero-padded on the right before adding MPRA flanks. Strings longer
        than 200bp raise ValueError.
    batch_size : int
        Number of sequences per forward pass. Default 512.

    Returns
    -------
    np.ndarray, shape (N, 3), dtype float32
        Predicted log2FC per cell type:
          col 0 = K562
          col 1 = HepG2
          col 2 = SK-N-SH (SKNSH)
        Predictions are the mean of forward and reverse-complement passes.
    """
    _ensure_loaded()

    if len(sequences) == 0:
        return np.zeros((0, 3), dtype=np.float32)

    tensors = []
    for i, seq in enumerate(sequences):
        if len(seq) > 200:
            raise ValueError(
                f"Sequence {i} has length {len(seq)} > 200bp. "
                "Malinois expects sequences of at most 200bp."
            )
        if len(seq) < 200:
            seq = seq + 'A' * (200 - len(seq))
        tensors.append(_utils.dna2tensor(seq))

    all_preds = []

    with torch.no_grad():
        for start in range(0, len(tensors), batch_size):
            batch_seqs = torch.stack(tensors[start : start + batch_size]).to(_device)
            padded = _flanker(batch_seqs)
            preds_fwd = _model(padded)
            preds_rc  = _model(padded.flip(dims=[1, 2]))
            preds = (preds_fwd + preds_rc) / 2.0
            all_preds.append(preds.cpu().float().numpy())

    return np.concatenate(all_preds, axis=0).astype(np.float32)
