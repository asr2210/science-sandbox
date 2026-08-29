"""Experiment 20: 35K MPRA + 15K GC-stratified natural hg38.

Better natural part: stratified across 30 GC bins from [0.20, 0.80] so the
natural component adds maximum compositional variance to the MPRA core.
Same MPRA fraction as exp 018 (which was 0.5739, current best).
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=20)
N, L = 50000, 200
N_MPRA = 35000
N_NAT = 15000
GC_LO, GC_HI = 0.20, 0.80
N_BINS = 30
per_bin = N_NAT // N_BINS  # 500

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
print(f"Loaded {len(mpra_seqs):,} MPRA sequences")
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
bin_width = (GC_HI - GC_LO) / N_BINS
buckets = [[] for _ in range(N_BINS)]
attempts = 0
filled = 0
while filled < N_BINS and attempts < 2_000_000:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    attempts += 1
    if not valid.match(win):
        continue
    gc = (win.count("G") + win.count("C")) / L
    if gc < GC_LO or gc >= GC_HI:
        continue
    b = min(int((gc - GC_LO) / bin_width), N_BINS - 1)
    if len(buckets[b]) < per_bin:
        buckets[b].append(win)
        if len(buckets[b]) == per_bin:
            filled += 1
print(f"GC-stratified natural: filled {filled}/{N_BINS} bins in {attempts} attempts")

nat = []
for b in buckets:
    nat.extend(b)
# Pad if any bin underfilled
while len(nat) < N_NAT:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    if valid.match(win):
        gc = (win.count("G") + win.count("C")) / L
        if GC_LO <= gc < GC_HI:
            nat.append(win)
nat = nat[:N_NAT]
print(f"Natural total: {len(nat)}")

out = mpra_chosen + nat
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} sequences")
