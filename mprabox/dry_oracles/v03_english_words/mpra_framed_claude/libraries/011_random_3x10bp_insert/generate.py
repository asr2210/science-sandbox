"""
011 — Random + 3x10bp cCRE fragments distributed per sequence.

Tests distributed vs concentrated biology. Total bio = 30bp (vs 25bp in 008).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N = 50_000
FRAG_LEN = 10
N_FRAGS = 3
SEED = 11

TARGETS = {"dELS": 30_000, "pELS": 10_000, "PLS": 5_000, "TF": 5_000}
CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

bg = alphabet[rng.integers(0, 4, size=(N, L), dtype=np.int8)]
seqs = [list(row) for row in bg]

records = {k: [] for k in TARGETS}
with (DATA / "GRCh38-cCREs.V4.bed").open() as fh:
    for line in fh:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 6:
            continue
        chrom, start, end, _, _, etype = fields[:6]
        if chrom in CHROMS_OK and etype in records:
            records[etype].append((chrom, int(start), int(end)))

fa = Fasta(str(DATA / "hg38.fa"), as_raw=True, sequence_always_upper=True)
fragments = []
for etype, n_target in TARGETS.items():
    pool = records[etype]
    idx = rng.choice(len(pool), size=n_target, replace=False)
    for i in idx:
        chrom, start, end = pool[i]
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

print(f"fragments pool: {len(fragments)}")

for i in range(N):
    # Pick 3 fragments and 3 random positions (non-overlapping when possible).
    chosen = rng.choice(len(fragments), size=N_FRAGS, replace=True)
    used = []
    for fi in chosen:
        frag = fragments[int(fi)]
        for _ in range(10):
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
print(f"wrote {N} x {L}bp random+3x{FRAG_LEN}bp fragment sequences to {OUT}")
