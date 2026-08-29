"""Experiment 009: motif insertion test.

50K iid random sequences (seed 42). For 25,000 of them (random selection),
replace positions 95-98 (0-indexed) with the 4-mer "1212".

Probes whether inserting a specific shared motif at a fixed position
helps or hurts. Per-position composition at positions 95-98 becomes
non-uniform across the library.
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

# Insert "1212" at positions 95-98 in a random half
motif = np.array([1, 2, 1, 2], dtype=np.uint8)
insert_idx = rng.choice(N, size=N // 2, replace=False)
arr[insert_idx, 95:99] = motif

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}")
print(f"Inserted motif '1212' at positions 95-98 in {len(insert_idx)} seqs")
