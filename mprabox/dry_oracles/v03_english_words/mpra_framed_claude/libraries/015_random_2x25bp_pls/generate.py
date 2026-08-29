"""
015 — Random + 2x25bp PLS-only fragments at random non-overlapping positions.

Tests whether DOUBLING the PLS payload helps when each fragment still spans
the motif-length sweet spot (25bp). Compare to:
  010 (1x50bp): lost vs 012 (contiguous 50bp is too much)
  012 (1x25bp): winning recipe
If 015 > 012 → more biology is good when fragments stay 25bp wide.
If 015 < 012 → 25bp total biology is the saturation point.
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
N_FRAGS = 2
SEED = 15

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

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

# Generate a pool of PLS fragments using the 012 recipe (random offset).
fragments = []
target_pool = N * N_FRAGS // 2 + 10000  # ~60k fragments
chosen = rng.integers(0, len(pls), size=target_pool + 10000)
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
    if len(fragments) >= target_pool:
        break

print(f"PLS fragments collected: {len(fragments)}")

for i in range(N):
    chosen = rng.choice(len(fragments), size=N_FRAGS, replace=True)
    used = []
    for fi in chosen:
        frag = fragments[int(fi)]
        for _ in range(20):
            pos = int(rng.integers(0, L - FRAG_LEN + 1))
            if all(not (pos < e and pos + FRAG_LEN > s) for s, e in used):
                break
        used.append((pos, pos + FRAG_LEN))
        for j, ch in enumerate(frag):
            seqs[i][pos + j] = ch

with OUT.open("w") as f:
    for row in seqs:
        f.write("".join(row))
        f.write("\n")
print(f"wrote {N} x {L}bp random + 2x{FRAG_LEN}bp PLS fragments to {OUT}")
