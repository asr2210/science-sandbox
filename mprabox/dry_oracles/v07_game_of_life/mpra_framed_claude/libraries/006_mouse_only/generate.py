"""
Experiment 006 — pure mouse natural baseline.

50K random 200bp windows from mm39 primary chromosomes.

Tests whether the model can learn a sequence-to-activity mapping that
transfers across species, using conserved regulatory grammar. Strong
generalization test: if mouse-only ≈ human-only, the model is
learning conserved features. If mouse-only ≪ human-only, the model is
learning human-specific features and library design should stay
human-centric.
"""

import os
import sys
import numpy as np
from pyfaidx import Fasta

L = 200
SEED = 0
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
MM39 = os.path.join(DATA, "mm39.fa")
MM39_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
ALPHABET = set("ACGT")


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(MM39, sequence_always_upper=True)
    chroms = [c for c in MM39_CHROMS if c in fa]
    lens = {c: len(fa[c]) for c in chroms}
    weights = np.array([lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()

    seqs = []
    attempts = 0
    while len(seqs) < 50_000:
        attempts += 1
        c = chroms[rng.choice(len(chroms), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        seqs.append(s)

    print(f"Sampled {len(seqs)} in {attempts} attempts "
          f"(accept {len(seqs)/attempts:.3f})", file=sys.stderr)

    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
