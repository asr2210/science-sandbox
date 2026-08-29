"""Experiment 28: 35K MPRA + 15K natural with EQUAL chromosome weights.

The best recipe (018) used length-weighted chromosome sampling (chr1
dominates). Try equal weights so each chrom gets 3K → more compositional
diversity from gene-rich short chroms (chr19, chr22) and gene-poor (chr18).
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=28)
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

def load_fa(p):
    with open(p) as f:
        return "".join(l for l in f.read().splitlines() if not l.startswith(">")).upper()

chroms_list = ["chr1", "chr7", "chr18", "chr19", "chr22"]
chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in chroms_list}
chrom_lens = {c: len(chrom_seq[c]) for c in chroms_list}
print(f"Chrom lengths: {chrom_lens}")
valid = re.compile(r"^[ACGT]+$")

per_chrom = N_NAT // len(chroms_list)  # 3000
nat = []
for c in chroms_list:
    chosen = 0
    attempts = 0
    while chosen < per_chrom and attempts < per_chrom * 50:
        pos = int(rng.integers(0, chrom_lens[c] - L))
        win = chrom_seq[c][pos:pos + L]
        attempts += 1
        if valid.match(win):
            nat.append(win)
            chosen += 1
print(f"Natural (equal chrom): {len(nat)}")
while len(nat) < N_NAT:
    c = rng.choice(chroms_list)
    pos = int(rng.integers(0, chrom_lens[c] - L))
    win = chrom_seq[c][pos:pos + L]
    if valid.match(win):
        nat.append(win)
nat = nat[:N_NAT]

out = mpra_chosen + nat
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} (eq-chrom natural)")
