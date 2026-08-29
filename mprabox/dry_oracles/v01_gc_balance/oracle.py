"""
v6_gc_balance — Reward sequences with perfectly balanced composition.

The easiest oracle. A warm-up.

K562:  wants exactly 50% GC content
HepG2: wants exactly 25% of each base (A=C=G=T=50)
SKNSH: wants exactly 50 of the rarest base (min count == 50)

Score drops off as a gaussian around the target.
A random uniform sequence already scores decently here — the agent
just needs to tighten the distribution.
"""

import numpy as np
from eval.oracles import register

_SIGMA = 10.0


@register('v01_gc_balance')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        cA, cC, cG, cT = seq.count('A'), seq.count('C'), seq.count('G'), seq.count('T')
        gc = cG + cC
        out[i, 0] = 4.0 * np.exp(-((gc - 100) ** 2) / (2 * _SIGMA ** 2)) - 1.0

        deviation = abs(cA - 50) + abs(cC - 50) + abs(cG - 50) + abs(cT - 50)
        out[i, 1] = 4.0 * np.exp(-(deviation ** 2) / (2 * (4 * _SIGMA) ** 2)) - 1.0

        min_count = min(cA, cC, cG, cT)
        out[i, 2] = 4.0 * np.exp(-((min_count - 50) ** 2) / (2 * _SIGMA ** 2)) - 1.0
    return out
