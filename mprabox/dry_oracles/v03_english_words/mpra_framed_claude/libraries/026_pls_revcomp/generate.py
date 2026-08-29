"""
026 — 012 recipe + revcomp augmentation (50% of PLS fragments revcomped before embedding).

DNA motifs work in both orientations. By revcomping half the fragments, we double the
effective motif strand diversity without changing fragment count or composition.
Tests whether the model learns motifs orientation-agnostically; if so, revcomp
augmentation should improve generalization.
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
SEED = 26

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")
COMP = str.maketrans("ACGT", "TGCA")

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

bg = alphabet[rng.integers(0, 4, size=(N, L), dtype=np.int8)]
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

# Revcomp 50% of fragments.
revcomp_mask = rng.integers(0, 2, size=N).astype(bool)
augmented = []
for i, frag in enumerate(fragments[:N]):
    if revcomp_mask[i]:
        augmented.append(frag.translate(COMP)[::-1])
    else:
        augmented.append(frag)

print(f"revcomp count: {revcomp_mask.sum()}")

positions = rng.integers(0, L - FRAG_LEN + 1, size=N)
for i in range(N):
    frag = augmented[i % len(augmented)]
    pos = int(positions[i])
    for j, ch in enumerate(frag):
        seqs[i][pos + j] = ch

with OUT.open("w") as f:
    for row in seqs:
        f.write("".join(row))
        f.write("\n")
print(f"wrote {N} x {L}bp random + 25bp PLS (revcomp augmented) to {OUT}")
