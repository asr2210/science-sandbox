"""Random uniform sequences with no homopolymer run > 3.

Rejection-sample random sequences until no >3-mer run of the same base.
Tests whether the rare long runs in random uniform (e.g., AAAAAA) hurt the score.
Per-sequence GC remains tightly near 50% (binomial), same as random uniform,
but per-position randomness is conditioned on local non-repetition.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42
MAX_RUN = 3

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Markovian generation: at each step, avoid producing a (MAX_RUN+1)-mer run.
def sample_one():
    out = np.empty(L, dtype=np.int8)
    # First MAX_RUN bases: free choice
    out[:MAX_RUN] = rng.integers(0, 4, size=MAX_RUN)
    for i in range(MAX_RUN, L):
        last_run = out[i - MAX_RUN:i]
        if len(set(last_run.tolist())) == 1:
            # Cannot repeat last_run[0]
            forbidden = int(last_run[0])
            options = [b for b in range(4) if b != forbidden]
            out[i] = options[rng.integers(0, 3)]
        else:
            out[i] = rng.integers(0, 4)
    return out

print(f"Generating {N} sequences with max run = {MAX_RUN}...")
seqs = []
for i in range(N):
    arr = sample_one()
    seqs.append(''.join(bases[arr].tolist()))
    if (i + 1) % 10000 == 0:
        print(f"  {i+1}/{N}")

# Verify
def max_run(s):
    best = 1; cur = 1
    for j in range(1, len(s)):
        if s[j] == s[j-1]:
            cur += 1; best = max(best, cur)
        else:
            cur = 1
    return best

import statistics
runs = [max_run(s) for s in seqs[:2000]]
gcs = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
print(f"Max run distribution (first 2k): max={max(runs)} mean={statistics.mean(runs):.2f}")
print(f"GC (first 2k): min={min(gcs):.3f} mean={statistics.mean(gcs):.3f} max={max(gcs):.3f}")
assert max(runs) <= MAX_RUN

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out_path, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out_path}")
