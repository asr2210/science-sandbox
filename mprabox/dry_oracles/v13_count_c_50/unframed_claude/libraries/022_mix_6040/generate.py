"""Experiment 22: 30K MPRA + 20K natural hg38 (60/40 mix).

Confirm the optimum mix ratio. Have:
  100/0 -> 0.5699
   80/20 -> 0.5714
   70/30 -> 0.5739 (best)
   50/50 -> 0.5691
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=22)
N, L = 50000, 200
N_MPRA = 30000
N_NAT = 20000

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

print("Loading chromosomes...")
chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in ["chr1", "chr7", "chr18", "chr19", "chr22"]}
chroms = list(chrom_seq.keys())
chrom_lens = np.array([len(chrom_seq[c]) for c in chroms])
weights = chrom_lens / chrom_lens.sum()

valid = re.compile(r"^[ACGT]+$")
nat = []
attempts = 0
while len(nat) < N_NAT and attempts < N_NAT * 50:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    attempts += 1
    if valid.match(win):
        nat.append(win)
print(f"Natural hg38: {len(nat)} from {attempts} attempts")

out = mpra_chosen + nat
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} (60/40)")
