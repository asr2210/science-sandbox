"""
Experiment 024 — noise injection (natural + random uniform).

Tests whether forcing the model to distinguish natural sequences from
random uniform "negative" examples helps the regression generalize.

Design (50K):
  25K natural hg38 (length-weighted)
  25K i.i.d. random uniform DNA (40% GC, matches exp 008)
"""

import os
import sys
import numpy as np
from pyfaidx import Fasta

L = 200
SEED = 0
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
HG38 = os.path.join(DATA, "hg38.fa")
HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
ALPHABET = set("ACGT")


def sample_natural(fa, chroms, n, rng):
    lens = {c: len(fa[c]) for c in chroms if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = cs[rng.choice(len(cs), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        out.append(s)
    return out


def random_uniform(n, rng):
    probs = np.array([0.30, 0.20, 0.20, 0.30])  # A C G T, 40% GC
    bases = np.array(list("ACGT"))
    out = []
    for _ in range(n):
        seq = bases[rng.choice(4, size=L, p=probs)]
        out.append("".join(seq))
    return out


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)

    print("Sampling 25K natural...", file=sys.stderr)
    nat = sample_natural(fa, HG38_CHROMS, 25_000, rng)
    print("Generating 25K random uniform...", file=sys.stderr)
    rand = random_uniform(25_000, rng)

    seqs = nat + rand
    assert len(seqs) == 50_000

    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
