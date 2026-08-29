"""Experiment 023: Greedy 10-mer coverage from 250k candidates.

4^10 = 1,048,576 unique 10-mers. 50k windows * ~190 unique 10-mers per
window = 9.5M kmer-events. The unique set is bounded by 1M but won't
saturate trivially — many 10-mers are rare or never observed in hg38.

Tests whether high-k coverage maximization helps where 7-mer saturated.
"""
import pickle
import numpy as np
from pathlib import Path
import time

CANDIDATES = 250_000
N = 50_000
L = 200
K = 10
SEED = 23

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

rng = np.random.default_rng(SEED)
valid = set("ACGT")

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

print("Encoding 10-mers...")
BASE = {"A": 0, "C": 1, "G": 2, "T": 3}
mask = (1 << (2 * K)) - 1
def kmers_of(seq):
    v = 0
    out = []
    seen = set()
    for i, ch in enumerate(seq):
        v = ((v << 2) | BASE[ch]) & mask
        if i >= K - 1 and v not in seen:
            out.append(v)
            seen.add(v)
    return np.array(out, dtype=np.uint32)

cand_arrays = [kmers_of(w) for w in cands]
avg_unique = sum(len(a) for a in cand_arrays) / len(cand_arrays)
print(f"Avg {avg_unique:.0f} unique 10-mers per window")

N_KMERS = 4 ** K
covered = np.zeros(N_KMERS, dtype=np.bool_)
selected = []
remaining = set(range(len(cands)))

t0 = time.time()
for step in range(N):
    if not remaining:
        break
    # Stochastic greedy: random pool of 500 per step (Mirzasoleiman et al.)
    pool = rng.choice(list(remaining), size=min(500, len(remaining)), replace=False)
    best, best_score = -1, -1
    for idx in pool:
        arr = cand_arrays[idx]
        gain = int((~covered[arr]).sum())
        if gain > best_score:
            best_score = gain
            best = int(idx)
    selected.append(best)
    covered[cand_arrays[best]] = True
    remaining.discard(best)
    if step % 5000 == 0:
        print(f"  step {step}: cov={int(covered.sum())}/{N_KMERS} "
              f"({covered.sum()/N_KMERS*100:.2f}%) gain={best_score} "
              f"t={time.time()-t0:.0f}s")

print(f"Final coverage: {int(covered.sum())}/{N_KMERS} "
      f"({covered.sum()/N_KMERS*100:.2f}%)")
print(f"Total time: {time.time()-t0:.0f}s")

out = [cands[i] for i in selected]
assert len(out) == N
rng.shuffle(out)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {len(out)} greedy-10mer-coverage sequences")
