"""Experiment 008: Palindrome gradient.

Each string has first 100 chars random. Second 100 chars are a per-position
mix of reverse(first 100) (with probability p_i) and uniform random (with
probability 1-p_i). p_i = i/(N-1).

String 0: random both halves. String N-1: perfect palindrome about midpoint.
Tests if predictor uses long-range reverse-correlation between halves.
"""
import os
import numpy as np

N = 50_000
L = 200
H = L // 2  # 100
SEED = 8

rng = np.random.default_rng(SEED)

first = rng.integers(0, 4, size=(N, H), dtype=np.uint8)
random_second = rng.integers(0, 4, size=(N, H), dtype=np.uint8)
p_palin = np.linspace(0.0, 1.0, N)

use_reverse = rng.random((N, H)) < p_palin[:, None]
reversed_first = first[:, ::-1]
second = np.where(use_reverse, reversed_first, random_second).astype(np.uint8)

chars = np.concatenate([first, second], axis=1)
assert chars.shape == (N, L)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
out = ALPHABET[chars]
lines = out.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

# Quick check: palindrome score = fraction of matched mirror positions
matches_first = (chars[0, :H] == chars[0, H:][::-1]).mean()
matches_last = (chars[-1, :H] == chars[-1, H:][::-1]).mean()
print(f"Wrote {N} sequences. Palindromy: first={matches_first:.2f}, last={matches_last:.2f}")
