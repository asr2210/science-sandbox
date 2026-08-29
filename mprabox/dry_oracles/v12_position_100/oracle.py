import numpy as np
from eval.oracles import register

_BASE_SCORES = {
    0: {'A': 4.0, 'C': 1.0, 'G': 2.0, 'T': -1.0},
    1: {'A': -1.0, 'C': 3.0, 'G': 0.5, 'T': 4.0},
    2: {'A': 2.0, 'C': -0.5, 'G': 4.0, 'T': 1.0},
}
_POS = 99

@register('v12_position_100')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        base = seq[_POS] if _POS < len(seq) else 'A'
        for col, scores in _BASE_SCORES.items():
            out[i, col] = scores.get(base, 0.0)
    return out
