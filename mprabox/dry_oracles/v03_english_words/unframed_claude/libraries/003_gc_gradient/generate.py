"""Experiment 003: 50k sequences with GC content uniformly spread.

Hypothesis: r is limited by the variance of model predictions across the
library. A uniform spread in a known robust correlate (GC content from 0.15
to 0.85) should give both scoring methods strong, agreeing variation.

For each sequence i, draw a target GC fraction g_i ~ Uniform(0.15, 0.85),
then draw 200 bases i.i.d. with P(G)=P(C)=g_i/2, P(A)=P(T)=(1-g_i)/2.
"""
import os
import numpy as np

RNG_SEED = 1003
N_SEQS = 50_000
LEN = 200
GC_LO, GC_HI = 0.15, 0.85
ALPHABET = np.array(list("ACGT"))


def main():
    rng = np.random.default_rng(RNG_SEED)
    gc = rng.uniform(GC_LO, GC_HI, size=N_SEQS)
    # base probabilities per sequence: P(A,C,G,T)
    p_at = (1.0 - gc) / 2.0
    p_gc = gc / 2.0
    probs = np.stack([p_at, p_gc, p_gc, p_at], axis=1)  # A,C,G,T
    # vectorised per-row multinomial-like sampling:
    # use cumulative probabilities + uniform draws
    cum = np.cumsum(probs, axis=1)
    u = rng.random((N_SEQS, LEN))
    idx = (u[:, :, None] >= cum[:, None, :]).sum(axis=2).astype(np.int8)
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in idx:
            f.write("".join(ALPHABET[row]))
            f.write("\n")
    print(f"wrote {N_SEQS} sequences; GC range [{GC_LO}, {GC_HI}]")


if __name__ == "__main__":
    main()
