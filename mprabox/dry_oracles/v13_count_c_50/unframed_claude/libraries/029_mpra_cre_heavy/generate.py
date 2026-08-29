"""Experiment 29: Heavy CRE oversample + balanced GTEx/UKBB + natural.

Exp 025 (balanced 12K each + 14K natural) gave 0.5747. Push further by
heavy oversampling of CRE (with replacement) to fill 18K, while keeping
GTEX 12K, UKBB 5K (down-weight) — total 35K MPRA. + 15K natural.

Hypothesis: CRE-class sequences are direct regulatory measurements that
both models particularly agree on.
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=29)
N, L = 50000, 200

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

N_CRE, N_GTEX, N_UKBB = 18000, 12000, 5000
mpra_chosen = []
# CRE: oversample with replacement
seqs = buckets["CRE"]
idx = rng.choice(len(seqs), size=N_CRE, replace=True)
mpra_chosen.extend(seqs[i] for i in idx)
# GTEX
seqs = buckets["GTEX"]
idx = rng.choice(len(seqs), size=N_GTEX, replace=False)
mpra_chosen.extend(seqs[i] for i in idx)
# UKBB
seqs = buckets["UKBB"]
idx = rng.choice(len(seqs), size=N_UKBB, replace=False)
mpra_chosen.extend(seqs[i] for i in idx)
print(f"MPRA total: {len(mpra_chosen)} (CRE={N_CRE} GTEX={N_GTEX} UKBB={N_UKBB})")

N_NAT = N - len(mpra_chosen)
def load_fa(p):
    with open(p) as f:
        return "".join(l for l in f.read().splitlines() if not l.startswith(">")).upper()

chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in ["chr1", "chr7", "chr18", "chr19", "chr22"]}
chroms = list(chrom_seq.keys())
chrom_lens = np.array([len(chrom_seq[c]) for c in chroms])
weights = chrom_lens / chrom_lens.sum()
valid = re.compile(r"^[ACGT]+$")
nat = []
while len(nat) < N_NAT:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    if valid.match(win):
        nat.append(win)

out = mpra_chosen + nat
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} (CRE-heavy)")
