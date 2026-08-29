"""Distal enhancers vs random genomic null.

25k active: random sample of dELS (distal enhancer-like) cCREs from
ENCODE V4, 200bp centered on midpoint.
25k null: random 200bp windows from hg38 chr1-22, sampled uniformly.

Two changes from exp 009:
- Active half restricted to dELS only (exclude PLS/pELS which include
  promoters; promoters seem to hurt K562 score per exp 010).
- Null is real genomic (not shuffled), which preserves natural
  background statistics that the model expects.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
import random

ROOT = Path(__file__).resolve().parents[2]
BED = ROOT / "data" / "cCRE_v4.bed"
FASTA = ROOT / "data" / "hg38.fa"
OUT = Path(__file__).parent / "sequences_0.txt"

N_TOTAL = 50_000
L = 200
N_ACTIVE = N_TOTAL // 2

ACTIVE_CLASSES = {"dELS"}  # distal enhancer-like only

py_rng = random.Random(404)
np_rng = np.random.default_rng(404)

# 1) Load dELS cCREs
peaks = []
with open(BED) as fh:
    for line in fh:
        parts = line.rstrip("\n").split("\t")
        chrom, start, end, cls = parts[0], int(parts[1]), int(parts[2]), parts[5]
        if cls not in ACTIVE_CLASSES:
            continue
        if "_" in chrom or chrom in {"chrM", "chrEBV"}:
            continue
        mid = (start + end) // 2
        peaks.append((chrom, mid))
print(f"dELS peaks: {len(peaks):,}")

fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)
half = L // 2
chrom_lens = {c: len(fa[c]) for c in fa.keys() if not ("_" in c or c in {"chrM", "chrEBV"})}

# 2) Sample active dELS
py_rng.shuffle(peaks)
active = []
i = 0
while len(active) < N_ACTIVE and i < len(peaks):
    chrom, mid = peaks[i]; i += 1
    s, e = mid - half, mid + half
    if s < 0 or e > chrom_lens[chrom]:
        continue
    seq = fa[chrom][s:e]
    if len(seq) != L or "N" in seq:
        continue
    active.append(seq)
print(f"Active dELS extracted: {len(active):,}")

# 3) Sample random genomic 200bp windows (most will NOT be in any cCRE)
# Use only autosomes for cleanliness
autos = [c for c in chrom_lens if c.startswith("chr") and c[3:].isdigit()]
lens_arr = np.array([chrom_lens[c] for c in autos], dtype=np.int64)
probs = lens_arr / lens_arr.sum()

null = []
while len(null) < N_ACTIVE:
    chrom_idx = np_rng.choice(len(autos), p=probs)
    chrom = autos[chrom_idx]
    s = np_rng.integers(0, chrom_lens[chrom] - L)
    seq = fa[chrom][s:s + L]
    if len(seq) != L or "N" in seq:
        continue
    null.append(seq)
print(f"Null genomic windows: {len(null):,}")

combined = active + null
py_rng.shuffle(combined)
OUT.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} sequences")
