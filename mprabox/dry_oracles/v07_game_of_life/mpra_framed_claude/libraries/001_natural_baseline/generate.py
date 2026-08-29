"""
Experiment 001 — natural genomic baseline.

50,000 random 200bp windows from hg38 primary chromosomes (chr1-22, X, Y).
Reject windows containing N. Length-weighted chromosome sampling.

Rationale: cleanest naturalness baseline; calibrates v07 against v04
(expected eval_01 ≈ 0.48 if eval distribution is similar).
"""

import os
import sys
import numpy as np
from pyfaidx import Fasta

L = 200
N_SEQS = 50_000
SEED = 0
HG38 = os.path.join(os.path.dirname(__file__), "..", "..", "data", "hg38.fa")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

PRIMARY = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)
    chrom_lens = {c: len(fa[c]) for c in PRIMARY}
    weights = np.array([chrom_lens[c] for c in PRIMARY], dtype=np.float64)
    weights /= weights.sum()

    seqs = []
    attempts = 0
    while len(seqs) < N_SEQS:
        attempts += 1
        c = PRIMARY[rng.choice(len(PRIMARY), p=weights)]
        start = int(rng.integers(0, chrom_lens[c] - L))
        seq = str(fa[c][start:start + L]).upper()
        if "N" in seq:
            continue
        if len(seq) != L:
            continue
        if not set(seq).issubset({"A", "C", "G", "T"}):
            continue
        seqs.append(seq)

    print(f"Sampled {len(seqs)} sequences in {attempts} attempts "
          f"(reject rate {(attempts - len(seqs)) / attempts:.3f})",
          file=sys.stderr)

    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
