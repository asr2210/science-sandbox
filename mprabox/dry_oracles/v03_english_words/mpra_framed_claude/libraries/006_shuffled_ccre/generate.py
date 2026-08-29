"""
006 — Mononucleotide-shuffled cCRE library.

Same 50K cCRE windows as 003, but each sequence is shuffled (preserves
mononucleotide composition exactly, destroys all motifs and dinucleotide
structure).

Diagnostic: disentangle whether the K562/HepG2 drop and SK-N-SH lift
in 003 (real cCRE) come from compositional shift or from real motifs.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N = 50_000
SEED = 6

TARGETS = {
    "dELS":       25_000,
    "pELS":       10_000,
    "PLS":         7_000,
    "TF":          3_000,
    "CA-CTCF":     2_000,
    "CA":          3_000,
}
assert sum(TARGETS.values()) == N

CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}
ALPHA = set("ACGT")

rng = np.random.default_rng(SEED)

print("Loading cCRE BED...")
records = {k: [] for k in TARGETS}
with (DATA / "GRCh38-cCREs.V4.bed").open() as fh:
    for line in fh:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 6:
            continue
        chrom, start, end, _, _, etype = fields[:6]
        if chrom in CHROMS_OK and etype in records:
            records[etype].append((chrom, int(start), int(end)))

selected = []
for etype, n_target in TARGETS.items():
    pool = records[etype]
    idx = rng.choice(len(pool), size=n_target, replace=False)
    for i in idx:
        chrom, start, end = pool[i]
        mid = (start + end) // 2
        selected.append((chrom, mid - L // 2, mid + L // 2))

rng.shuffle(selected)

print(f"Extracting {len(selected)} cCRE windows from hg38...")
fa = Fasta(str(DATA / "hg38.fa"), as_raw=True, sequence_always_upper=True)
raw_seqs = []
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
    raw_seqs.append(seq)

while len(raw_seqs) < N:
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
    raw_seqs.append(seq)

raw_seqs = raw_seqs[:N]
print("Shuffling each sequence (mononucleotide shuffle)...")
shuffled = []
for s in raw_seqs:
    arr = np.frombuffer(s.encode(), dtype=np.uint8).copy()
    rng.shuffle(arr)
    shuffled.append(arr.tobytes().decode())

with OUT.open("w") as f:
    for s in shuffled:
        f.write(s)
        f.write("\n")
print(f"wrote {len(shuffled)} x {L}bp shuffled cCRE sequences to {OUT}")
