"""
v9_compression — Reward sequences based on their compressibility.

Uses zlib to compress the raw DNA string. The compression ratio
reveals how much structure/repetition exists in the sequence.

K562:  reward HIGH compression ratio (repetitive, patterned sequences).
       The agent must build sequences with internal structure.
HepG2: reward LOW compression ratio (incompressible, maximum entropy).
       The agent must build maximally disordered sequences.
SKNSH: reward compression ratio near exactly 0.5 (medium structure).
       A Goldilocks zone — neither too ordered nor too random.

Different cell types want opposite things, forcing the library to
contain diverse sequences.
"""

import zlib
import numpy as np
from eval.oracles import register

_SIGMA = 0.08


def _compression_ratio(seq):
    raw = seq.encode('ascii')
    compressed = zlib.compress(raw, level=9)
    return len(compressed) / len(raw)


@register('v04_compression')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        ratio = _compression_ratio(seq)
        out[i, 0] = (1.0 - ratio) * 6.0 - 1.0
        out[i, 1] = ratio * 6.0 - 2.0
        target_mid = 0.5
        out[i, 2] = 4.0 * np.exp(-((ratio - target_mid) ** 2) / (2 * _SIGMA ** 2)) - 1.0
    return out
