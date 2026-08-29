"""
v7_alternating_purine — Reward alternating purine/pyrimidine patterns.

Purines = {A, G}, Pyrimidines = {C, T}.

K562:  reward strict RYRYRY... alternation (R at even positions,
       Y at odd). Score = fraction of positions following the pattern.
HepG2: reward YRYRYR... (opposite phase).
SKNSH: reward alternation in EITHER phase (best of the two).

The user's original example. Learnable, not trivial — a random
sequence gets ~50% by chance, so the agent needs to push well above.
"""

import numpy as np
from eval.oracles import register

_PURINE = set('AG')
_PYRIMIDINE = set('CT')


def _alternation_score(seq, phase):
    """phase=0: even=R, odd=Y. phase=1: even=Y, odd=R."""
    hits = 0
    for j, base in enumerate(seq):
        if phase == 0:
            expected = _PURINE if j % 2 == 0 else _PYRIMIDINE
        else:
            expected = _PYRIMIDINE if j % 2 == 0 else _PURINE
        if base in expected:
            hits += 1
    return hits / len(seq)


@register('v02_alternating_purine')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        s0 = _alternation_score(seq, 0)
        s1 = _alternation_score(seq, 1)
        out[i, 0] = s0 * 5.0 - 1.5
        out[i, 1] = s1 * 5.0 - 1.5
        out[i, 2] = max(s0, s1) * 5.0 - 1.5
    return out
