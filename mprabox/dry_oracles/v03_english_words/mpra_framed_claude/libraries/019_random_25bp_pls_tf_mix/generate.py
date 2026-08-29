"""
019 — Random + 1x25bp fragment: 50% PLS, 50% TF cCRE.

Each sequence gets ONE 25bp fragment from EITHER PLS or TF cCRE (50/50 split).
Tests whether the two mechanisms (PLS universal + TF cell-type-specific)
can combine to break 012's 0.4248 ceiling.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N = 50_000
N_PLS = 25_000
N_TF = 25_000
FRAG_LEN = 25
SEED = 19

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

bg = alphabet[rng.integers(0, 4, size=(N, L), dtype=np.int8)]
seqs = [list(row) for row in bg]

pls, tf = [], []
with (DATA / "GRCh38-cCREs.V4.bed").open() as fh:
    for line in fh:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 6:
            continue
        chrom, start, end, _, _, etype = fields[:6]
        if chrom in CHROMS_OK:
            if etype == "PLS":
                pls.append((chrom, int(start), int(end)))
            elif etype == "TF":
                tf.append((chrom, int(start), int(end)))

print(f"PLS pool: {len(pls)}, TF pool: {len(tf)}")

fa = Fasta(str(DATA / "hg38.fa"), as_raw=True, sequence_always_upper=True)

def sample_fragments(pool, n_target, seed_offset):
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

pls_frags = sample_fragments(pls, N_PLS, 1)
tf_frags = sample_fragments(tf, N_TF, 2)
print(f"PLS frags: {len(pls_frags)}, TF frags: {len(tf_frags)}")

fragments = pls_frags + tf_frags
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
print(f"wrote {N} x {L}bp random + 25bp 50/50 PLS+TF mix to {OUT}")
