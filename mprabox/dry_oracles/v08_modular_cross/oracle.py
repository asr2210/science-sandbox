"""
v3_modular_cross — Reward based on cross-products of nucleotide counts
under modular arithmetic.

K562:  (count_A * count_C) mod 13 == 0
HepG2: (count_G * count_T - count_A) mod 11 == 0
SKNSH: (count_A^2 + count_C^2) mod 17 == 0

The surrogate must learn nonlinear interactions between nucleotide
counts — products and squares, not just individual counts.
A linear model gets nowhere. The modular arithmetic creates a
periodic reward landscape with multiple optima.
"""

import numpy as np
from eval.oracles import register


def _modular_score(value, modulus):
    remainder = value % modulus
    dist = min(remainder, modulus - remainder)
    return np.exp(-(dist ** 2) / 2.0) * 5.0 - 1.0


@register('v08_modular_cross')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        cA, cC, cG, cT = seq.count('A'), seq.count('C'), seq.count('G'), seq.count('T')
        out[i, 0] = _modular_score(cA * cC, 13)
        out[i, 1] = _modular_score(cG * cT - cA, 11)
        out[i, 2] = _modular_score(cA ** 2 + cC ** 2, 17)
    return out
