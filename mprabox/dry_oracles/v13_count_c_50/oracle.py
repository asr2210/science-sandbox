import numpy as np
from eval.oracles import register

_TARGETS = {0: ('C', 50), 1: ('A', 55), 2: ('G', 45)}
_SIGMA = 8.0

@register('v13_count_c_50')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        for col, (base, target) in _TARGETS.items():
            count = seq.count(base)
            out[i, col] = 4.0 * np.exp(-((count - target) ** 2) / (2 * _SIGMA ** 2)) - 1.0
    return out
