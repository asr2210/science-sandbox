#!/usr/bin/env python3
"""Experiment 008: same composition distribution as exp 006 (Dir α=1), but arranged in blocks.

Each string: all '0's first, then '1's, '2's, '3's.
Tests whether within-string ORDER matters (vs purely composition-driven features).
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 11  # same as exp 006 for matched composition
ALPHA = np.array([1.0, 1.0, 1.0, 1.0])

rng = np.random.default_rng(SEED)
ps = rng.dirichlet(ALPHA, size=N)

# Convert p to integer counts that sum to L exactly.
# Use multinomial sampling for the counts (so they match the random multinomial that exp 006 would produce).
# But to be fair / make composition match the random-iid library:
# We want the COMPOSITION distribution to match exp 006. Exp 006 sampled L iid from Cat(p),
# so counts ~ Multinomial(L, p). Use that.
chars = ['0', '1', '2', '3']
out_path = os.path.join(os.path.dirname(__file__), 'sequences_0.txt')

with open(out_path, 'w') as f:
    for i in range(N):
        counts = rng.multinomial(L, ps[i])
        # Build string as blocks
        parts = [chars[k] * counts[k] for k in range(4)]
        f.write(''.join(parts))
        f.write('\n')

print(f"Wrote {N} block-structured lines length {L}, composition ~ Dir(α=1) Multinomial")
