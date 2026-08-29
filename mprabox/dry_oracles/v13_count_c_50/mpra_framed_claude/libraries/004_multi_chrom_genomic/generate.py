"""Experiment 004: random 200bp windows from multiple hg38 chromosomes.

Tests whether sampling more diverse genomic contexts (varied GC, gene
density, chromatin) improves over chr19-only. 10,000 windows per chromosome
from chr8, chr19, chr21, chr22, chrX.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
PER_CHROM = N // len(CHROMS)
DATA = Path(__file__).resolve().parents[2] / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
valid = set("ACGT")
all_seqs = []

for chrom in CHROMS:
    fa_path = DATA / f"hg38.{chrom}.fa"
    fa = Fasta(str(fa_path), as_raw=True, sequence_always_upper=True)
    chrom_len = len(fa[chrom])
    print(f"{chrom}: length={chrom_len}")
    collected = []
    while len(collected) < PER_CHROM:
        batch = rng.integers(0, chrom_len - L, size=4 * (PER_CHROM - len(collected)))
        for start in batch:
            if len(collected) >= PER_CHROM:
                break
            s = fa[chrom][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
    all_seqs.extend(collected)

assert len(all_seqs) == N, f"got {len(all_seqs)}"
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
print(f"Wrote {N} sequences from {len(CHROMS)} chromosomes.")
