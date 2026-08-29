"""Experiment 007: random 200bp windows from all 22 autosomes.

Tests whether broader chromosome coverage breaks the ~0.50 plateau seen
with 6-chromosome sampling (002). Sample 50k windows weighted by
chromosome length, reject N. Random strand.

Why this generalizes: max-entropy natural-human-DNA library — agnostic
to any cell type, regional bias minimized. If the natural-data ceiling
is real, this should sit at ~0.50 regardless of chromosome choice.
"""
import os
import numpy as np
from pathlib import Path

N_SEQ = 50_000
LEN = 200
SEED = 42

HERE = Path(__file__).parent
DATA_DIR = HERE.parents[1] / "data"
CHROMS = [f"chr{i}" for i in range(1, 23)]

def load_chrom(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip())
    return "".join(parts).upper()

def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def main():
    chrom_seqs = {}
    for c in CHROMS:
        chrom_seqs[c] = load_chrom(DATA_DIR / f"{c}.fa")
        print(f"{c}: {len(chrom_seqs[c]):,} bp")
    rng = np.random.default_rng(SEED)
    weights = np.array([len(chrom_seqs[c]) for c in CHROMS], dtype=np.float64)
    weights /= weights.sum()

    seqs = []
    attempts = 0
    while len(seqs) < N_SEQ:
        ci = rng.choice(len(CHROMS), p=weights)
        cs = chrom_seqs[CHROMS[ci]]
        pos = rng.integers(0, len(cs) - LEN)
        window = cs[pos:pos + LEN]
        attempts += 1
        if "N" in window:
            continue
        if rng.random() < 0.5:
            window = revcomp(window)
        seqs.append(window)
    print(f"{len(seqs)} sequences from {attempts} attempts "
          f"({100 * len(seqs) / attempts:.1f}% accept)")

    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"Wrote to {out_path}")

if __name__ == "__main__":
    main()
