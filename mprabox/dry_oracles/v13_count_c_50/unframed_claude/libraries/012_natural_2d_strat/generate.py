"""Experiment 12: Natural hg38 GC-stratified + synthetic GC tails.

40K natural hg38 sequences stratified on [0.20, 0.80] (30 bins of ~1333 each)
+ 5K synthetic at very LOW GC (target uniform in [0.02, 0.18])
+ 5K synthetic at very HIGH GC (target uniform in [0.82, 0.98]).

Tests whether extending GC range beyond natural availability via synthetic
tails increases compositional variance and therefore r.
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=12)
N, L = 50000, 200
N_NAT = 40000
N_LOW = 5000
N_HIGH = 5000

# Natural part
GC_LO, GC_HI = 0.20, 0.80
N_BINS = 30
per_bin = N_NAT // N_BINS  # 1333

DATA = Path(__file__).resolve().parents[2] / "data"
def load_fa(p):
    with open(p) as f:
        lines = f.read().splitlines()
    return "".join(l for l in lines if not l.startswith(">")).upper()

print("Loading chromosomes...")
chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in ["chr1", "chr22"]}
chroms = list(chrom_seq.keys())
chrom_lens = np.array([len(chrom_seq[c]) for c in chroms])
weights = chrom_lens / chrom_lens.sum()

valid = re.compile(r"^[ACGT]+$")
buckets = [[] for _ in range(N_BINS)]
bin_width = (GC_HI - GC_LO) / N_BINS

attempts = 0
filled = 0
while filled < N_BINS:
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
print(f"Natural stratified: {sum(len(b) for b in buckets)} from {attempts} attempts")

nat_seqs = []
for b in buckets:
    nat_seqs.extend(b)
# Pad to N_NAT if any bin underfilled
while len(nat_seqs) < N_NAT:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    if valid.match(win):
        gc = (win.count("G") + win.count("C")) / L
        if GC_LO <= gc < GC_HI:
            nat_seqs.append(win)
nat_seqs = nat_seqs[:N_NAT]

# Synthetic low-GC and high-GC
def synth_iid(N, L, gc_lo, gc_hi, rng):
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

low_seqs = synth_iid(N_LOW, L, 0.02, 0.18, rng)
high_seqs = synth_iid(N_HIGH, L, 0.82, 0.98, rng)
print(f"Synthetic low: {len(low_seqs)}, high: {len(high_seqs)}")

all_seqs = nat_seqs + low_seqs + high_seqs
rng.shuffle(all_seqs)
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(all_seqs) + "\n")
print(f"Wrote {len(all_seqs)} total sequences.")

arr = np.array([[ord(b) for b in s] for s in all_seqs[:10000]], dtype=np.int8)
gc = ((arr == ord('C')) | (arr == ord('G'))).mean(axis=1)
print(f"GC (10k sample): mean={gc.mean():.3f}, std={gc.std():.3f}, "
      f"range=[{gc.min():.3f}, {gc.max():.3f}]")
