"""
Experiment 002: Random genomic windows from hg38.

Sample 50,000 random 200bp windows from the autosomes + X + Y of hg38.
- Restrict to primary chromosomes (chr1..chr22, chrX, chrY) to avoid alt/random contigs.
- Skip any window containing 'N' (assembly gaps / unsequenced).
- 50% chance of taking reverse complement to make the library strand-balanced.
- Seed 0.

Rationale: this is the canonical biology baseline — sequences with real
motif composition and natural sequence context, but not enriched for
regulatory activity. Comparing this to 001 (uniform random) tells us how
much "real biology" matters before we start enriching for active regions.

Generalization argument: the library uses sequences from the actual genome
the test sequences are drawn from. Even if our K562/HepG2/SK-N-SH labels
are cell-type-specific, the *sequences* themselves are from the same
distribution any other cell type's regulatory sequences would be drawn
from. So a model trained on this should learn motifs grounded in real
sequence context, helping it generalize to unseen cell types whose
regulatory elements are also drawn from the same genome.
"""
import os, sys
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 0
FA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "hg38.fa"))
CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]

COMP = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N",
        "a": "t", "t": "a", "g": "c", "c": "g", "n": "n"}

def revcomp(s):
    return "".join(COMP[b] for b in reversed(s))

def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(FA_PATH)
    lengths = {c: len(fa[c]) for c in CHROMS}
    weights = np.array([lengths[c] for c in CHROMS], dtype=np.float64)
    weights /= weights.sum()

    seqs = []
    attempts = 0
    while len(seqs) < N:
        attempts += 1
        # Sample a chromosome by length, then a uniform start position
        chrom = CHROMS[rng.choice(len(CHROMS), p=weights)]
        start = rng.integers(0, lengths[chrom] - L)
        s = str(fa[chrom][start:start + L]).upper()
        if "N" in s:
            continue
        if rng.random() < 0.5:
            s = revcomp(s)
        seqs.append(s)
        if len(seqs) % 10000 == 0:
            print(f"  {len(seqs)} / {N} (attempts {attempts})", flush=True)

    with open(OUT, "w") as f:
        f.write("\n".join(seqs) + "\n")

    # Verify
    with open(OUT) as f:
        lines = f.read().splitlines()
    assert len(lines) == N
    for i, l in enumerate(lines[:5]):
        assert len(l) == L
        assert set(l) <= set("ACGT")
    print(f"wrote {len(lines)} sequences to {OUT} (rejection rate {1 - N/attempts:.3%})")

if __name__ == "__main__":
    main()
