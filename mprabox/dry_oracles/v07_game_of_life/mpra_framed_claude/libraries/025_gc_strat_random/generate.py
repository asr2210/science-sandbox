"""
Experiment 025 — GC-stratified random uniform DNA.

Critical test of T8: does motif/syntax content matter at all once
GC is controlled?

Design (50K):
  10K random uniform sequences per GC bin, generated with i.i.d.
  bases sampled from a per-bin GC-targeted distribution:
    bin 0 (GC<35%):  P(A)=P(T)=0.35, P(C)=P(G)=0.15
    bin 1 (35-45%):  P(A)=P(T)=0.30, P(C)=P(G)=0.20
    bin 2 (45-55%):  P(A)=P(T)=0.25, P(C)=P(G)=0.25
    bin 3 (55-65%):  P(A)=P(T)=0.20, P(C)=P(G)=0.30
    bin 4 (GC>65%):  P(A)=P(T)=0.15, P(C)=P(G)=0.35

Random sequences with controlled GC distribution. NO motif content,
NO natural syntax.

If reaches ceiling (~0.394): GC is everything; library design is
entirely about composition.
If stays low (<0.385): motifs/syntax matter even under GC control.
"""

import os
import sys
import numpy as np

L = 200
SEED = 0
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

BIN_PROBS = [
    [0.35, 0.15, 0.15, 0.35],  # A C G T for GC=0.30 (bin 0)
    [0.30, 0.20, 0.20, 0.30],  # GC=0.40 (bin 1)
    [0.25, 0.25, 0.25, 0.25],  # GC=0.50 (bin 2)
    [0.20, 0.30, 0.30, 0.20],  # GC=0.60 (bin 3)
    [0.15, 0.35, 0.35, 0.15],  # GC=0.70 (bin 4)
]
PER_BIN = 10_000
BASES = np.array(list("ACGT"))


def gen_bin(rng, probs, n):
    out = []
    for _ in range(n):
        seq = BASES[rng.choice(4, size=L, p=probs)]
        out.append("".join(seq))
    return out


def main():
    rng = np.random.default_rng(SEED)
    seqs = []
    for i, probs in enumerate(BIN_PROBS):
        print(f"  bin {i}, target GC={(probs[1]+probs[2]):.2f}", file=sys.stderr)
        seqs.extend(gen_bin(rng, probs, PER_BIN))
    assert len(seqs) == 50_000

    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
