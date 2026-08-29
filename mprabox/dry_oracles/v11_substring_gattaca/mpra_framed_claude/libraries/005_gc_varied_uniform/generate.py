"""Experiment 005: random sequences with per-sequence GC content varied.

For each of 50k sequences:
- Draw GC ~ Uniform[0.2, 0.8]
- Sample 200 bases independently with P(G)=P(C)=GC/2, P(A)=P(T)=(1-GC)/2

This broadens the composition coverage of the library beyond fixed GC=50%,
testing whether the model benefits from training on a wider range of compositions.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 0
GC_MIN, GC_MAX = 0.2, 0.8


def main():
    rng = np.random.default_rng(SEED)
    gc = rng.uniform(GC_MIN, GC_MAX, size=N)
    # probs per sequence: [A, C, G, T]
    pA = (1 - gc) / 2
    pC = gc / 2
    pG = gc / 2
    pT = (1 - gc) / 2
    probs = np.stack([pA, pC, pG, pT], axis=1)  # (N, 4)

    alphabet = np.array(list("ACGT"))
    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        # use cumulative sampling per sequence
        cum = np.cumsum(probs, axis=1)  # (N, 4)
        u = rng.random(size=(N, L))
        # base index: smallest j such that u[i, k] < cum[i, j]
        # Vectorized: compare u with cum[:, None, :] (NLx4)
        # To save memory, loop over N in chunks.
        chunk = 5000
        for s in range(0, N, chunk):
            e = min(s + chunk, N)
            u_chunk = u[s:e]
            cum_chunk = cum[s:e, None, :]  # (B, 1, 4)
            idx = (u_chunk[:, :, None] >= cum_chunk).sum(axis=2)  # (B, L)
            chars = alphabet[idx]
            for row in chars:
                f.write("".join(row.tolist()))
                f.write("\n")
    actual_gc = []
    with out.open() as g:
        for i, line in enumerate(g):
            if i >= 1000:
                break
            s = line.strip()
            actual_gc.append((s.count("G") + s.count("C")) / len(s))
    print(f"target GC range [{GC_MIN}, {GC_MAX}], realized in first 1000: "
          f"min={min(actual_gc):.3f} max={max(actual_gc):.3f} "
          f"mean={np.mean(actual_gc):.3f}")
    print(f"wrote {N} sequences to {out}")


if __name__ == "__main__":
    main()
