"""
028 — 012 recipe + tiny 6bp neural-specific motif planted in random 25% of sequences.

Each sequence gets a 25bp PLS fragment (012 base). In 25% of sequences (12,500), we
ALSO plant a 6bp canonical neural TF motif (one of NEUROD CAGCTG, REST core TCAGCA,
POU3F ATGCAA) at a separate random non-overlapping position. Total bio per "augmented"
sequence: 31bp; per other sequence: 25bp.

Goal: minimally disturb global composition (1.5bp avg added) while injecting neural
motif signal to lift SK-N-SH above 0.065 without K562/HepG2 cost.
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
SEED = 28
AUG_FRAC = 0.25
NEURAL_MOTIFS = ["CAGCTG", "TCAGCA", "ATGCAA", "GCAATG"]  # forward + revcomp variants

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
# Decide which sequences get the augmented neural motif.
aug_mask = rng.random(N) < AUG_FRAC
motif_choice = rng.integers(0, len(NEURAL_MOTIFS), size=N)
# For augmented sequences, pre-compute a non-overlapping motif position.
motif_pos = np.zeros(N, dtype=np.int32)
m_len = len(NEURAL_MOTIFS[0])  # 6bp
for i in range(N):
    if not aug_mask[i]:
        continue
    pls_pos = int(positions[i])
    pls_end = pls_pos + FRAG_LEN
    for _ in range(20):
        mp = int(rng.integers(0, L - m_len + 1))
        if mp + m_len <= pls_pos or mp >= pls_end:
            motif_pos[i] = mp
            break

print(f"augmented sequences: {aug_mask.sum()}")

for i in range(N):
    frag = fragments[i % len(fragments)]
    pos = int(positions[i])
    for j, ch in enumerate(frag):
        seqs[i][pos + j] = ch
    if aug_mask[i]:
        motif = NEURAL_MOTIFS[int(motif_choice[i])]
        mp = int(motif_pos[i])
        if mp > 0:
            for j, ch in enumerate(motif):
                seqs[i][mp + j] = ch

with OUT.open("w") as f:
    for row in seqs:
        f.write("".join(row))
        f.write("\n")
print(f"wrote {N} x {L}bp random + 25bp PLS + 25% neural-motif plant to {OUT}")
