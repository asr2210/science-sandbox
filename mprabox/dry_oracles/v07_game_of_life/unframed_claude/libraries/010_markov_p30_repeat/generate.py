"""First-order Markov sequences with mild self-repeat bias.

Tests the 'naturalness' direction: random uniform has P(next = prev) = 0.25.
Real DNA has slightly higher (mononucleotide repeats common). Here we set
P(next = prev) = 0.30 with the remaining 0.70 split uniformly among the
other three bases. Library mean GC and per-seq GC distribution match
random uniform; only the transition probabilities differ.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42
P_REPEAT = 0.30
P_OTHER = (1.0 - P_REPEAT) / 3.0

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Precompute transition matrix
T = np.full((4, 4), P_OTHER)
np.fill_diagonal(T, P_REPEAT)
# Each row sums to 1
assert np.allclose(T.sum(axis=1), 1.0)

def sample_one():
    out = np.empty(L, dtype=np.int8)
    out[0] = rng.integers(0, 4)
    for i in range(1, L):
        out[i] = rng.choice(4, p=T[out[i-1]])
    return out

print(f"Generating {N} sequences with P(repeat)={P_REPEAT}...")
seqs = []
for i in range(N):
    seqs.append(''.join(bases[sample_one()].tolist()))
    if (i + 1) % 10000 == 0:
        print(f"  {i+1}/{N}")

# Sanity check
import statistics
def max_run(s):
    best = 1; cur = 1
    for j in range(1, len(s)):
        if s[j] == s[j-1]:
            cur += 1; best = max(best, cur)
        else:
            cur = 1
    return best

gcs = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
runs = [max_run(s) for s in seqs[:2000]]
print(f"GC: min={min(gcs):.3f} mean={statistics.mean(gcs):.3f} max={max(gcs):.3f}")
print(f"Max run: mean={statistics.mean(runs):.2f} max={max(runs)}")

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out_path, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out_path}")
