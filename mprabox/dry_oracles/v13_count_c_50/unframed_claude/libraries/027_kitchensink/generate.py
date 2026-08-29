"""Experiment 27: maximally-diverse mixture, 5 sources of 10K each.

10K MPRA-random + 10K MPRA-balanced-proj + 10K natural-random + 10K
GC-stratified natural + 10K extreme-GC synthetic.

Tests whether heterogeneity itself (5 distributions) drives r higher than
2 sources (35K MPRA + 15K natural at 0.5739).
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=27)
N, L = 50000, 200
N_EACH = 10000

DATA = Path(__file__).resolve().parents[2] / "data"
src = DATA / "mpra_dataset.txt"

# 1. MPRA random + 2. MPRA balanced project
print("Reading MPRA dataset...")
all_mpra = []
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
        all_mpra.append(s)
        proj = p[pi]
        if proj in buckets:
            buckets[proj].append(s)

mpra_rand_idx = rng.choice(len(all_mpra), size=N_EACH, replace=False)
mpra_rand = [all_mpra[i] for i in mpra_rand_idx]

n_per_proj = N_EACH // 3 + 1  # ~3334
mpra_bal = []
for proj in ["GTEX", "UKBB", "CRE"]:
    seqs = buckets[proj]
    take = min(n_per_proj, len(seqs))
    idx = rng.choice(len(seqs), size=take, replace=(take > len(seqs)))
    mpra_bal.extend(seqs[i] for i in idx)
mpra_bal = mpra_bal[:N_EACH]
print(f"MPRA random: {len(mpra_rand)}, MPRA balanced: {len(mpra_bal)}")

# 3 & 4 natural
def load_fa(p):
    with open(p) as f:
        return "".join(l for l in f.read().splitlines() if not l.startswith(">")).upper()

print("Loading chromosomes...")
chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in ["chr1", "chr7", "chr18", "chr19", "chr22"]}
chroms = list(chrom_seq.keys())
chrom_lens = np.array([len(chrom_seq[c]) for c in chroms])
weights = chrom_lens / chrom_lens.sum()
valid = re.compile(r"^[ACGT]+$")

nat_rand = []
while len(nat_rand) < N_EACH:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    if valid.match(win):
        nat_rand.append(win)

# 4. GC-stratified natural (5K, broader GC)
GC_LO, GC_HI = 0.20, 0.80
N_BINS = 20
per_bin = N_EACH // N_BINS  # 500
bin_width = (GC_HI - GC_LO) / N_BINS
buckets_gc = [[] for _ in range(N_BINS)]
filled = 0
attempts = 0
while filled < N_BINS and attempts < 1_500_000:
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
    if len(buckets_gc[b]) < per_bin:
        buckets_gc[b].append(win)
        if len(buckets_gc[b]) == per_bin:
            filled += 1
nat_strat = []
for b in buckets_gc:
    nat_strat.extend(b)
nat_strat = nat_strat[:N_EACH]
while len(nat_strat) < N_EACH:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    if valid.match(win):
        nat_strat.append(win)
nat_strat = nat_strat[:N_EACH]
print(f"Natural random: {len(nat_rand)}, GC-strat: {len(nat_strat)}")

# 5. extreme-GC synthetic
def synth(N, gc_lo, gc_hi):
    out = []
    for _ in range(N):
        gc = rng.uniform(gc_lo, gc_hi)
        is_gc = rng.random(L) < gc
        gc_choice = rng.integers(0, 2, size=L)
        at_choice = rng.integers(0, 2, size=L)
        arr = np.where(is_gc,
                       np.where(gc_choice == 0, 1, 2),
                       np.where(at_choice == 0, 0, 3)).astype(np.int8)
        out.append("".join("ACGT"[b] for b in arr))
    return out

# 5K low-GC and 5K high-GC
synth_seqs = synth(N_EACH // 2, 0.05, 0.20) + synth(N_EACH // 2, 0.80, 0.95)
print(f"Synthetic extreme-GC: {len(synth_seqs)}")

out = mpra_rand + mpra_bal + nat_rand + nat_strat + synth_seqs
rng.shuffle(out)
assert len(out) == N
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)} sequences (kitchen sink)")
