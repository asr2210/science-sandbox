"""Bimodal GC composition library: half AT-rich (20% GC), half GC-rich (80% GC).

Probes whether *spread in GC content* (and the resulting spread in predicted
activity) is what drives the score, by deliberately creating two very different
sub-populations of sequences.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Two halves: 25k @ 20% GC, 25k @ 80% GC
def sample(n, gc):
    pA = pT = (1 - gc) / 2
    pC = pG = gc / 2
    probs = np.array([pA, pC, pG, pT])
    arr = rng.choice(4, size=(n, L), p=probs)
    return bases[arr]

low = sample(N // 2, 0.20)
high = sample(N // 2, 0.80)
all_arr = np.concatenate([low, high], axis=0)
# Shuffle so order isn't structural
order = rng.permutation(N)
all_arr = all_arr[order]
seqs = [''.join(row.tolist()) for row in all_arr]

# Sanity check GC distribution
import statistics
gcs = [sum(c in 'GC' for c in s) / L for s in seqs]
print(f"GC content: min={min(gcs):.3f} mean={statistics.mean(gcs):.3f} max={max(gcs):.3f}")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
