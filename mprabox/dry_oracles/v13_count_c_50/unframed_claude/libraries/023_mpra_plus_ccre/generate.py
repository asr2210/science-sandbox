"""Experiment 23: 35K MPRA + 15K cCRE-centered hg38 sequences.

Replace the natural-random portion with cCRE-centered windows. cCREs are
ENCODE-annotated regulatory elements; sequences are GC-rich and have
TF-binding motifs. Both predictors might agree even more strongly on
regulatory content than on random natural.
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=23)
N, L = 50000, 200
N_MPRA = 35000
N_NAT = 15000

DATA = Path(__file__).resolve().parents[2] / "data"
src = DATA / "mpra_dataset.txt"

print("Reading MPRA dataset...")
mpra_seqs = []
with open(src) as f:
    h = f.readline().rstrip("\n").split("\t")
    si = h.index("sequence")
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) <= si:
            continue
        s = p[si].upper()
        if len(s) == L and set(s) <= set("ACGT"):
            mpra_seqs.append(s)
mpra_idx = rng.choice(len(mpra_seqs), size=N_MPRA, replace=False)
mpra_chosen = [mpra_seqs[i] for i in mpra_idx]
print(f"MPRA: {len(mpra_chosen)}")

# Load all chrom seqs for cCRE extraction
def load_fa(p):
    with open(p) as f:
        return "".join(l for l in f.read().splitlines() if not l.startswith(">")).upper()

print("Loading chromosomes...")
chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in ["chr1", "chr7", "chr18", "chr19", "chr22"]}

# Parse cCRE bed: chr, start, end, ...
print("Parsing cCREs...")
ccres = []
with open(DATA / "cCREs.bed") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        c = parts[0]
        if c not in chrom_seq:
            continue
        start = int(parts[1]); end = int(parts[2])
        ccres.append((c, start, end))
print(f"Loaded {len(ccres):,} cCREs on covered chroms")

valid = re.compile(r"^[ACGT]+$")
nat = []
attempts = 0
# Sample cCREs and extract 200bp centered window
while len(nat) < N_NAT and attempts < N_NAT * 50:
    i = rng.integers(0, len(ccres))
    c, st, en = ccres[i]
    center = (st + en) // 2
    pos = center - L // 2
    if pos < 0 or pos + L > len(chrom_seq[c]):
        attempts += 1
        continue
    win = chrom_seq[c][pos:pos + L]
    attempts += 1
    if valid.match(win):
        nat.append(win)
print(f"cCRE-centered: {len(nat)} from {attempts} attempts")

out = mpra_chosen + nat
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} (MPRA + cCRE mix)")
