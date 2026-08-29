"""Experiment 8: 50K natural sequences centered on ENCODE cCREs (chr1 + chr22).

cCREs = candidate cis-regulatory elements (~1M elements, ENCODE V3). Each
sequence: 200bp window centered on the midpoint of a randomly-chosen cCRE.

Hypothesis: Sequences from regulatory regions are closer to MPRA training
distribution than random genomic windows → higher agreement → higher r.
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=8)
N, L = 50000, 200

DATA = Path(__file__).resolve().parents[2] / "data"

def load_fa(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return "".join(line for line in lines if not line.startswith(">")).upper()

print("Loading chromosomes...")
chrom_seq = {"chr1": load_fa(DATA / "chr1.fa"), "chr22": load_fa(DATA / "chr22.fa")}
print(f"  chr1 {len(chrom_seq['chr1']):,}, chr22 {len(chrom_seq['chr22']):,}")

# Parse cCREs (chr1, chr22 only)
print("Parsing cCREs...")
records = []
with open(DATA / "cCREs.bed") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        chrom, start, end = parts[0], int(parts[1]), int(parts[2])
        if chrom in chrom_seq:
            records.append((chrom, start, end))
print(f"  {len(records):,} cCREs on chr1+chr22")

records = np.array(records, dtype=object)
idx = rng.choice(len(records), size=N * 2, replace=False)  # 2x buffer for N rejects

out = []
attempts = 0
for i in idx:
    chrom, start, end = records[i]
    mid = (start + end) // 2
    half = L // 2
    s = mid - half
    e = s + L
    if s < 0 or e > len(chrom_seq[chrom]):
        continue
    win = chrom_seq[chrom][s:e]
    attempts += 1
    if len(win) == L and set(win) <= set("ACGT"):
        out.append(win)
        if len(out) == N:
            break

out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} cCRE-centered sequences.")

# Stats
arr = np.array([[ord(b) for b in s] for s in out[:5000]], dtype=np.int8)
C, G = ord('C'), ord('G')
gc = ((arr == C) | (arr == G)).mean(axis=1)
print(f"GC% (first 5k): mean={gc.mean():.3f}, std={gc.std():.3f}")
