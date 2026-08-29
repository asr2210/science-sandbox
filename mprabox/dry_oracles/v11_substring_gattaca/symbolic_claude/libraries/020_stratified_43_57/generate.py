"""Stratified [43,57] uniform-tuples: each tuple appears exactly ~22 times.
Removes sampling noise on compositions while keeping shuffle randomness.

Goal: reduce variance vs 009. If 020 > 009 reliably, stratification helps.
With 2255 tuples and 50000 seqs: ceil(50000/2255)=23, so 1310 tuples get 23
and 945 get 22."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 43, 57

valid = []
for c0 in range(LO, HI + 1):
    for c1 in range(LO, HI + 1):
        for c2 in range(LO, HI + 1):
            c3 = L - c0 - c1 - c2
            if LO <= c3 <= HI:
                valid.append((c0, c1, c2, c3))
valid = np.array(valid)
T = len(valid)
print(f"# valid count tuples: {T}")

# How many copies per tuple
base = N // T  # 22
extra = N - base * T  # number of tuples that get an extra copy
copies = np.full(T, base, dtype=int)
copies[:extra] += 1
print(f"copies: base={base}, extra={extra}; min={copies.min()}, max={copies.max()}")

# Shuffle tuple-order so the extras are random
perm = rng.permutation(T)
copies = copies[perm]
valid = valid[perm]

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
chars = np.array(list("0123"))
with open(OUT, "w") as f:
    for i in range(T):
        c = valid[i]
        for _ in range(copies[i]):
            seq = np.concatenate([np.full(c[k], chars[k]) for k in range(4)])
            rng.shuffle(seq)
            f.write("".join(seq) + "\n")
print(f"wrote {N} stratified [{LO},{HI}] sequences")
