"""Experiment 016: Properly balanced deterministic tiling across full hg38.

For each chromosome, compute n_chrom = round(50_000 * chrom_len / total_len),
then tile each chromosome at uniform step = chrom_len / n_chrom with a
random starting offset. Eliminates the chr-order bias of exp 007.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 16

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
total = int(lens.sum())
# Number of windows per chrom proportional to its length, rounded
n_per = np.array([max(1, round(N * (lens[i] / total))) for i in range(len(names))])
# Fix to sum exactly to N
diff = N - n_per.sum()
order = np.argsort(-lens)  # adjust biggest chroms
for i in range(abs(diff)):
    n_per[order[i % len(order)]] += np.sign(diff)
assert n_per.sum() == N

rng = np.random.default_rng(SEED)
valid = set("ACGT")
out = []
for ci, name in enumerate(names):
    n = int(n_per[ci])
    if n <= 0:
        continue
    seq = chroms[name]
    chrom_len = len(seq)
    # Step so n windows cover the chromosome
    step = max(L, chrom_len // n)
    # Random start offset within [0, step)
    offset = int(rng.integers(0, step))
    got = 0
    for k in range(n * 3):  # try up to 3x positions, skip Ns
        pos = offset + k * step
        if pos + L > chrom_len:
            break
        w = seq[pos:pos + L]
        if set(w) <= valid:
            out.append(w)
            got += 1
        if got >= n:
            break
    # If we ran out, fall back to random sampling on this chrom
    while got < n:
        pos = int(rng.integers(0, chrom_len - L))
        w = seq[pos:pos + L]
        if set(w) <= valid:
            out.append(w)
            got += 1

assert len(out) == N, f"got {len(out)}"
rng.shuffle(out)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")
print(f"Wrote {len(out)} tiled+balanced windows")
