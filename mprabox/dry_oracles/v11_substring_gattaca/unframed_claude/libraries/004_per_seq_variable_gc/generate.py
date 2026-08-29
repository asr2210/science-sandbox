#!/usr/bin/env python3
"""Per-sequence variable GC content (each seq drawn at a random target GC in
[0.20, 0.80]) but uniform within sequence given that composition. Tests if
inter-sequence composition diversity helps any cell line.
"""
import numpy as np
import os

SEED = 7777
N = 50_000
L = 200
ALPH = np.array(list("ACGT"))

def main():
    rng = np.random.default_rng(SEED)
    # per-sequence target GC
    gc = rng.uniform(0.20, 0.80, size=N)
    # within a seq, P(C)=P(G)=gc/2, P(A)=P(T)=(1-gc)/2
    pA = (1 - gc) / 2
    pC = gc / 2
    pG = gc / 2
    # pT = pA
    seqs = np.empty((N, L), dtype=np.int8)
    for i in range(N):
        probs = np.array([pA[i], pC[i], pG[i], pA[i]])
        seqs[i] = rng.choice(4, size=L, p=probs)
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    flat = seqs.ravel()
    base_pct = np.bincount(flat, minlength=4) / flat.size
    print({"A": float(base_pct[0]), "C": float(base_pct[1]),
           "G": float(base_pct[2]), "T": float(base_pct[3])})
    print(f"Wrote {N} seqs of length {L} to {out_path}")

if __name__ == "__main__":
    main()
