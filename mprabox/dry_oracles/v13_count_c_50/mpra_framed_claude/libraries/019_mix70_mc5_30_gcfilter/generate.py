"""Experiment 019: 70/30 mix with GC-FILTERED genomic supplement.

35k multi-chrom-5 + 15k random windows from mc5 chroms, filtered to
GC ∈ [0.50, 0.80]. Synthesizes a cCRE-like high-GC distribution without
any annotation curation. Tests whether composition-only (no functional
annotation) recovers the cCRE supplement benefit.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
CHROMS = ["chr8", "chr19", "chr21", "chr22", "chrX"]
N_GENOMIC = 35_000
N_SUPP = N - N_GENOMIC
GC_LO, GC_HI = 0.50, 0.80
DATA = Path(__file__).resolve().parents[2] / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
valid = set("ACGT")

# mc5 baseline
per_chrom = N_GENOMIC // len(CHROMS)
genomic = []
for c in CHROMS:
    chrom_len = len(fas[c][c])
    collected = []
    while len(collected) < per_chrom:
        batch = rng.integers(0, chrom_len - L, size=4 * (per_chrom - len(collected)))
        for start in batch:
            if len(collected) >= per_chrom:
                break
            s = fas[c][c][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
    genomic.extend(collected)

# GC-filtered supplement from same chroms (rejection sample)
supp = []
chrom_keys = CHROMS
chrom_lens = {c: len(fas[c][c]) for c in CHROMS}
chrom_weights = np.array([chrom_lens[c] for c in CHROMS], dtype=float)
chrom_weights /= chrom_weights.sum()
attempts = 0
while len(supp) < N_SUPP:
    batch_size = 4 * (N_SUPP - len(supp))
    chrom_choices = rng.choice(len(CHROMS), size=batch_size, p=chrom_weights)
    for ci in chrom_choices:
        if len(supp) >= N_SUPP:
            break
        c = chrom_keys[ci]
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = fas[c][c][start:start + L]
        if len(s) != L or not set(s).issubset(valid):
            continue
        gc = (s.count("G") + s.count("C")) / L
        if GC_LO <= gc <= GC_HI:
            supp.append(s)
    attempts += 1
    if attempts > 100:
        raise RuntimeError(f"only got {len(supp)} after {attempts} batches")

supp_gcs = np.array([(s.count("G") + s.count("C")) / L for s in supp])
print(f"supp GC: mean={supp_gcs.mean():.3f}, std={supp_gcs.std():.4f}, "
      f"n_attempts={attempts}")

all_seqs = genomic + supp
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"Wrote {N}: 35k mc5 + 15k GC-filtered ({GC_LO}-{GC_HI}) genomic.")
