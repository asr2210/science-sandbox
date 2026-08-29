import numpy as np
from eval.oracles import register

_TARGETS = {
    0: 'GATTACA',
    1: 'TATAAA',
    2: 'CCGCGG',
}

@register('v11_substring_gattaca')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        for col, target in _TARGETS.items():
            count = 0
            start = 0
            while True:
                pos = seq.find(target, start)
                if pos == -1:
                    break
                count += 1
                start = pos + 1
            out[i, col] = count * 2.0 - 0.5
    return out
