"""Experiment 26: 35K MPRA with 1% random substitutions + 15K natural.

Inject small noise into MPRA sequences (1% subs ~ 2bp per 200) to add
variance while staying close to training distribution. Both predictors,
trained on noisy MPRA data, should be robust to this — but their tiny
disagreements should add useful variance to the library.
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=26)
N, L = 50000, 200
N_MPRA = 35000
N_NAT = 15000
MUT_RATE = 0.01

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
ALPHA = "ACGT"
def mutate(s):
    out = list(s)
    n_mut = rng.binomial(L, MUT_RATE)
    if n_mut == 0:
        return s
    positions = rng.choice(L, size=n_mut, replace=False)
    for p in positions:
        cur = out[p]
        choices = [c for c in ALPHA if c != cur]
        out[p] = choices[rng.integers(0, 3)]
    return "".join(out)

mpra_chosen = [mutate(mpra_seqs[i]) for i in mpra_idx]
print(f"Mutated MPRA: {len(mpra_chosen)}")

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
while len(nat) < N_NAT and attempts < N_NAT * 50:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    attempts += 1
    if valid.match(win):
        nat.append(win)

out = mpra_chosen + nat
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} mutated MPRA + natural")
