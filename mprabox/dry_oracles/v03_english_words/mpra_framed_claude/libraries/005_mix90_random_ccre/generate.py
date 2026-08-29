"""
005 — 90% random + 10% cCRE.

Tests whether a small biology dose preserves random's K562/HepG2 advantage
while picking up some SK-N-SH lift.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N = 50_000
N_RANDOM = 45_000
N_CCRE = 5_000
SEED = 5

CCRE_TARGETS = {
    "dELS":     2_500,
    "pELS":     1_000,
    "PLS":        700,
    "TF":         300,
    "CA-CTCF":    200,
    "CA":         300,
}
assert sum(CCRE_TARGETS.values()) == N_CCRE

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))

print("Generating random sequences...")
rand_idx = rng.integers(0, 4, size=(N_RANDOM, L), dtype=np.int8)
rand_seqs = ["".join(alphabet[row].tolist()) for row in rand_idx]

print("Loading cCRE BED...")
records = {k: [] for k in CCRE_TARGETS}
with (DATA / "GRCh38-cCREs.V4.bed").open() as fh:
    for line in fh:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 6:
            continue
        chrom, start, end, _, _, etype = fields[:6]
        if chrom in CHROMS_OK and etype in records:
            records[etype].append((chrom, int(start), int(end)))

selected = []
for etype, n_target in CCRE_TARGETS.items():
    pool = records[etype]
    idx = rng.choice(len(pool), size=n_target, replace=False)
    for i in idx:
        chrom, start, end = pool[i]
        mid = (start + end) // 2
        selected.append((chrom, mid - L // 2, mid + L // 2))

print(f"Extracting {len(selected)} cCRE windows from hg38...")
fa = Fasta(str(DATA / "hg38.fa"), as_raw=True, sequence_always_upper=True)
ccre_seqs = []
for chrom, ws, we in selected:
    if ws < 0 or we > len(fa[chrom]):
        continue
    seq = str(fa[chrom][ws:we]).upper()
    if len(seq) != L:
        continue
    if not set(seq).issubset(ALPHA):
        non_acgt = sum(1 for c in seq if c not in ALPHA)
        if non_acgt > 5:
            continue
        seq = "".join(c if c in ALPHA else "ACGT"[rng.integers(0, 4)] for c in seq)
    ccre_seqs.append(seq)

while len(ccre_seqs) < N_CCRE:
    pool = records["dELS"]
    i = int(rng.integers(0, len(pool)))
    chrom, start, end = pool[i]
    mid = (start + end) // 2
    ws, we = mid - L // 2, mid + L // 2
    if ws < 0 or we > len(fa[chrom]):
        continue
    seq = str(fa[chrom][ws:we]).upper()
    if len(seq) != L or not set(seq).issubset(ALPHA):
        continue
    ccre_seqs.append(seq)

ccre_seqs = ccre_seqs[:N_CCRE]
print(f"random: {len(rand_seqs)}, cCRE: {len(ccre_seqs)}")

all_seqs = rand_seqs + ccre_seqs
rng.shuffle(all_seqs)

with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
print(f"wrote {len(all_seqs)} x {L}bp sequences to {OUT}")
