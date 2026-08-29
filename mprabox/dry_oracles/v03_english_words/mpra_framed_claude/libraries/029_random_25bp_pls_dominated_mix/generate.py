"""
029 — Random + 25bp fragments: 80% PLS, 10% pELS, 10% TF.

PLS-majority mix. PLS dominates to preserve K562/HepG2; small fractions of pELS+TF
add diverse motif content that may boost SK-N-SH. Tests Theory v17 from a different
angle: if 80% PLS preserves K562/HepG2 fitting (vs 50/50 mix in 019 which dragged it
down), the threshold for composition damage is somewhere between 50% and 80%.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N = 50_000
N_PLS = 40_000
N_PELS = 5_000
N_TF = 5_000
FRAG_LEN = 25
SEED = 29

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

bg = alphabet[rng.integers(0, 4, size=(N, L), dtype=np.int8)]
seqs = [list(row) for row in bg]

pls, pels, tf = [], [], []
with (DATA / "GRCh38-cCREs.V4.bed").open() as fh:
    for line in fh:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 6:
            continue
        chrom, start, end, _, _, etype = fields[:6]
        if chrom not in CHROMS_OK:
            continue
        if etype == "PLS":
            pls.append((chrom, int(start), int(end)))
        elif etype == "pELS":
            pels.append((chrom, int(start), int(end)))
        elif etype == "TF":
            tf.append((chrom, int(start), int(end)))

print(f"PLS: {len(pls)}, pELS: {len(pels)}, TF: {len(tf)}")
fa = Fasta(str(DATA / "hg38.fa"), as_raw=True, sequence_always_upper=True)

def sample(pool, n_target, seed_offset):
    rng2 = np.random.default_rng(SEED + seed_offset)
    out = []
    chosen = rng2.integers(0, len(pool), size=n_target + 5000)
    for i in chosen:
        chrom, start, end = pool[i]
        mid = (start + end) // 2
        ws, we = mid - 100, mid + 100
        if ws < 0 or we > len(fa[chrom]):
            continue
        full = str(fa[chrom][ws:we]).upper()
        if len(full) != 200 or not set(full).issubset(ALPHA):
            continue
        f_start = int(rng2.integers(0, 200 - FRAG_LEN + 1))
        frag = full[f_start:f_start + FRAG_LEN]
        if set(frag).issubset(ALPHA):
            out.append(frag)
        if len(out) >= n_target:
            break
    return out

fragments = sample(pls, N_PLS, 1) + sample(pels, N_PELS, 2) + sample(tf, N_TF, 3)
print(f"total fragments: {len(fragments)}")
rng.shuffle(fragments)

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
print(f"wrote {N} x {L}bp random + 80% PLS / 10% pELS / 10% TF mix to {OUT}")
