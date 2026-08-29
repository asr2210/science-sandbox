"""Experiment 25: 35K MPRA balanced across projects + 15K natural.

Original MPRA dist: GTEX 446K, UKBB 338K, CRE 14K (~57/43/2 of valid).
Random sampling under-represents CRE. Force balanced sampling so CRE,
GTEx, UKBB each contribute equally — adds diversity across data sources.

12K per project (capping CRE which has ~14K), + 15K natural hg38.
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=25)
N, L = 50000, 200
N_PROJ = 12000  # per project (CRE only has ~14K so cap here)
N_NAT = 15000  # 50000 - 3*12000 = 14000 left, use 14k natural

DATA = Path(__file__).resolve().parents[2] / "data"
src = DATA / "mpra_dataset.txt"

print("Reading MPRA dataset...")
buckets = {"GTEX": [], "UKBB": [], "CRE": []}
with open(src) as f:
    h = f.readline().rstrip("\n").split("\t")
    si, pi = h.index("sequence"), h.index("data_project")
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) <= si:
            continue
        s = p[si].upper()
        if len(s) != L or set(s) - set("ACGT"):
            continue
        proj = p[pi]
        if proj in buckets:
            buckets[proj].append(s)
for k, v in buckets.items():
    print(f"  {k}: {len(v):,}")

# Sample 12K from each (with replacement for CRE if needed)
mpra_chosen = []
for proj in ["GTEX", "UKBB", "CRE"]:
    seqs = buckets[proj]
    if len(seqs) >= N_PROJ:
        idx = rng.choice(len(seqs), size=N_PROJ, replace=False)
    else:
        idx = rng.choice(len(seqs), size=N_PROJ, replace=True)
        print(f"  WARNING: {proj} oversampling with replacement")
    mpra_chosen.extend(seqs[i] for i in idx)
print(f"MPRA balanced: {len(mpra_chosen)}")

# Natural part (fill to N)
N_NAT_actual = N - len(mpra_chosen)
def load_fa(p):
    with open(p) as f:
        return "".join(l for l in f.read().splitlines() if not l.startswith(">")).upper()

chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in ["chr1", "chr7", "chr18", "chr19", "chr22"]}
chroms = list(chrom_seq.keys())
chrom_lens = np.array([len(chrom_seq[c]) for c in chroms])
weights = chrom_lens / chrom_lens.sum()
valid = re.compile(r"^[ACGT]+$")
nat = []
attempts = 0
while len(nat) < N_NAT_actual and attempts < N_NAT_actual * 50:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    attempts += 1
    if valid.match(win):
        nat.append(win)
print(f"Natural: {len(nat)}")

out = mpra_chosen + nat
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} balanced-MPRA + natural")
