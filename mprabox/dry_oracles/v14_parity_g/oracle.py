import numpy as np
from eval.oracles import register

@register('v14_parity_g')
def label_sequences(sequences, batch_size=512):
    n = len(sequences)
    out = np.zeros((n, 3), dtype=np.float32)
    for i, seq in enumerate(sequences):
        g_count = seq.count('G')
        c_count = seq.count('C')
        t_count = seq.count('T')
        out[i, 0] = 3.0 if g_count % 2 == 0 else -1.0
        out[i, 1] = 3.0 if c_count % 2 == 0 else -1.0
        out[i, 2] = 3.0 if t_count % 2 == 0 else -1.0
    return out
