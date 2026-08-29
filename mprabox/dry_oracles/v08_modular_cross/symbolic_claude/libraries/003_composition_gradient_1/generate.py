"""Experiment 003: Composition gradient in fraction of '1'.

String i (i=0..49999) has exactly n_i = round(200 * i / 49999) ones
and (200 - n_i) zeros, shuffled randomly. No 2s or 3s.

Goal: Test whether the scorer reacts to a monotone-in-i feature.
If condition_a becomes large (positive or negative), the scorer's
hidden target correlates with i and the scorer's feature correlates
with '1' content (or 0/1 ratio). Magnitude tells us how strong.
"""
import os
import numpy as np

N_STRINGS = 50_000
STR_LEN = 200
rng = np.random.default_rng(seed=7)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N_STRINGS):
        n_ones = round(STR_LEN * i / (N_STRINGS - 1))
        arr = np.array([ord('1')] * n_ones + [ord('0')] * (STR_LEN - n_ones),
                       dtype=np.uint8)
        rng.shuffle(arr)
        f.write(arr.tobytes().decode("ascii") + "\n")

print(f"Wrote {N_STRINGS} strings to {out_path}")
