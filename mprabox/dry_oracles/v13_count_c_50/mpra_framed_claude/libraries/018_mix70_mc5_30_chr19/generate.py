"""Experiment 018: 70/30 mix with chr19-only high-GC genomic supplement.

35k multi-chrom-5 + 15k random chr19 windows. chr19 has GC ~0.48 (vs the
mc5 average ~0.42), so this is a pure compositional augmentation: no
curation, no functional annotation, just biasing toward higher GC.

Test: if 018 ≈ 013/017, composition fully explains the supplement value;
the cCRE / PhastCons machinery was just an expensive way to achieve a
GC shift.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
HALF = L // 2
MC5 = ["chr8", "chr19", "chr21", "chr22", "chrX"]
SUPP_CHROM = "chr19"
N_GENOMIC = 35_000
N_SUPP = N - N_GENOMIC
DATA = Path(__file__).resolve().parents[2] / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in MC5}
valid = set("ACGT")

# mc5 baseline
per_chrom = N_GENOMIC // len(MC5)
genomic = []
for c in MC5:
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

# chr19 supplement
chr19_len = len(fas[SUPP_CHROM][SUPP_CHROM])
supp = []
while len(supp) < N_SUPP:
    batch = rng.integers(0, chr19_len - L, size=4 * (N_SUPP - len(supp)))
    for start in batch:
        if len(supp) >= N_SUPP:
            break
        s = fas[SUPP_CHROM][SUPP_CHROM][int(start):int(start) + L]
        if len(s) == L and set(s).issubset(valid):
            supp.append(s)

all_seqs = genomic + supp
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
gcs = np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
supp_gcs = np.array([(s.count("G") + s.count("C")) / L for s in supp])
print(f"Library GC: mean={gcs.mean():.3f}, std={gcs.std():.4f}")
print(f"chr19 supp GC: mean={supp_gcs.mean():.3f}")
print(f"Wrote {N}: 35k mc5 + 15k chr19-only genomic.")
