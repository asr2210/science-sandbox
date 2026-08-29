"""Experiment 021: Greedy 7-mer coverage maximization.

Generate 250k random hg38 candidate windows, then greedily pick 50k
that maximize unique 7-mer set (16,384 possible 7-mers in canonical
form; ~14k unique 7-mers per 200bp window).

If the scorer benefits from k-mer diversity in training, this should
exceed uniform random (~0.135 ceiling).
"""
import pickle
import numpy as np
from pathlib import Path

CANDIDATES = 250_000
N = 50_000
L = 200
K = 7
SEED = 21

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

rng = np.random.default_rng(SEED)
valid = set("ACGT")

# Generate candidate windows
print("Sampling candidates...")
cands = []
while len(cands) < CANDIDATES:
    ci = int(rng.choice(len(names), p=p))
    c = names[ci]
    pos = int(rng.integers(0, lens[ci] - L))
    w = chroms[c][pos:pos + L]
    if set(w) <= valid:
        cands.append(w)
    if len(cands) % 50_000 == 0:
        print(f"  {len(cands)}/{CANDIDATES}")

# Encode each window's 7-mer set as a frozenset of ints
print("Encoding 7-mers...")
BASE = {"A": 0, "C": 1, "G": 2, "T": 3}
def kmers_of(seq):
    arr = np.array([BASE[ch] for ch in seq], dtype=np.uint32)
    # rolling base-4 encoding
    v = 0
    out = set()
    mask = (1 << (2 * K)) - 1
    for i, b in enumerate(arr):
        v = ((v << 2) | int(b)) & mask
        if i >= K - 1:
            out.add(v)
    return out

cand_kmers = [kmers_of(w) for w in cands]
print(f"Avg {sum(len(k) for k in cand_kmers)/len(cand_kmers):.0f} unique 7-mers per window")

# Greedy selection: pick the window adding the most new k-mers each step
# Faster impl: maintain coverage count vector instead of set lookup
N_KMERS = 4 ** K
covered = np.zeros(N_KMERS, dtype=np.bool_)
selected = []
remaining = list(range(len(cands)))

# Pre-compute kmer arrays for fast scoring
print("Pre-encoding for greedy...")
cand_arrays = [np.fromiter(s, dtype=np.uint32, count=len(s)) for s in cand_kmers]

# Initial round: pick window with max kmers (any will do for first)
import time
t0 = time.time()
for step in range(N):
    best = -1
    best_score = -1
    # Sample 1000 random candidates per step (stochastic greedy — Mirzasoleiman)
    # This makes greedy tractable: 50k * 1k = 50M ops not 250k * 50k = 12.5B
    if not remaining:
        break
    pool = rng.choice(remaining, size=min(1000, len(remaining)), replace=False)
    for idx in pool:
        arr = cand_arrays[idx]
        # Count new k-mers
        gain = int((~covered[arr]).sum())
        if gain > best_score:
            best_score = gain
            best = int(idx)
    selected.append(best)
    covered[cand_arrays[best]] = True
    remaining.remove(best)
    if step % 5000 == 0:
        print(f"  step {step}: coverage={int(covered.sum())}/{N_KMERS} ({covered.sum()/N_KMERS*100:.1f}%) elapsed={time.time()-t0:.0f}s")

print(f"Final coverage: {int(covered.sum())}/{N_KMERS} ({covered.sum()/N_KMERS*100:.2f}%)")
print(f"Total time: {time.time()-t0:.0f}s")

out = [cands[i] for i in selected]
assert len(out) == N
rng.shuffle(out)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {len(out)} greedy-7mer-coverage sequences")
