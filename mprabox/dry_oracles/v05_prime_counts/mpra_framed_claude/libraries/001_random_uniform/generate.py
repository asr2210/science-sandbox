#!/usr/bin/env python3
"""
Experiment 001 — Random uniform ACGT baseline.

Generates 50,000 sequences of 200bp, each base sampled iid uniform from ACGT.
Purpose: establish a floor for downstream comparisons.
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'sequences_0.txt')

N_SEQ = 50_000
LEN = 200
ALPHA = np.array(list('ACGT'))


def main(seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, 4, size=(N_SEQ, LEN), dtype=np.int8)
    chars = ALPHA[idx]
    with open(OUT, 'w') as f:
        for row in chars:
            f.write(''.join(row.tolist()))
            f.write('\n')
    # sanity
    with open(OUT) as f:
        lines = f.readlines()
    assert len(lines) == N_SEQ
    assert all(len(L.strip()) == LEN for L in lines)
    print(f"wrote {N_SEQ} sequences of length {LEN} to {OUT}")


if __name__ == '__main__':
    main(seed=0)
