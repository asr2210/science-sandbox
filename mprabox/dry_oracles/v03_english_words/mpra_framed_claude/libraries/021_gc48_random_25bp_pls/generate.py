"""
021 — Random background at 48% GC + 1x25bp PLS fragment.

PLS fragments are CpG-rich (~60% GC). In 012, embedding 25bp PLS in 50% GC random
gives net composition ~51.25% GC, slightly above eval target. Compensate by
lowering background to 48% GC so net composition is ~49.5%.
Tests whether tiny composition tuning recovers HepG2 (which dropped 0.004 in 012 vs random).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N = 50_000
FRAG_LEN = 25
SEED = 21
GC_FRAC = 0.48  # background GC fraction; A,T,C,G = 0.26, 0.26, 0.24, 0.24 if we want 48% GC

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

rng = np.random.default_rng(SEED)

# Weighted sampling of bases for 48% GC background.
at_each = (1 - GC_FRAC) / 2
gc_each = GC_FRAC / 2
weights = np.array([at_each, gc_each, gc_each, at_each])  # A, C, G, T
alphabet = np.array(list("ACGT"))

bg_idx = rng.choice(4, size=(N, L), p=weights)
bg = alphabet[bg_idx]
seqs = [list(row) for row in bg]

pls = []
with (DATA / "GRCh38-cCREs.V4.bed").open() as fh:
    for line in fh:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 6:
            continue
        chrom, start, end, _, _, etype = fields[:6]
        if chrom in CHROMS_OK and etype == "PLS":
            pls.append((chrom, int(start), int(end)))

print(f"PLS pool size: {len(pls)}")

fa = Fasta(str(DATA / "hg38.fa"), as_raw=True, sequence_always_upper=True)

fragments = []
chosen = rng.integers(0, len(pls), size=N + 5000)
for i in chosen:
    chrom, start, end = pls[i]
    mid = (start + end) // 2
    ws, we = mid - 100, mid + 100
    if ws < 0 or we > len(fa[chrom]):
        continue
    full = str(fa[chrom][ws:we]).upper()
    if len(full) != 200 or not set(full).issubset(ALPHA):
        continue
    f_start = int(rng.integers(0, 200 - FRAG_LEN + 1))
    frag = full[f_start:f_start + FRAG_LEN]
    if set(frag).issubset(ALPHA):
        fragments.append(frag)
    if len(fragments) >= N:
        break

print(f"PLS fragments collected: {len(fragments)}")

positions = rng.integers(0, L - FRAG_LEN + 1, size=N)
for i in range(N):
    frag = fragments[i % len(fragments)]
    pos = int(positions[i])
    for j, ch in enumerate(frag):
        seqs[i][pos + j] = ch

with OUT.open("w") as f:
    for row in seqs:
        f.write("".join(row))
        f.write("\n")
print(f"wrote {N} x {L}bp 48% GC random + 25bp PLS fragments to {OUT}")
