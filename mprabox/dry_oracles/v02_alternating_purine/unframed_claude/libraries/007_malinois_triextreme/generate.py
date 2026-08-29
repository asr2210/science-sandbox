"""Combine extremes across all three cell-line activities.

For each cell line (K562, HepG2, SKNSH), pick ~8333 highest and ~8333 lowest
by log2FC. Union (dedup), then top up to 50k with random Malinois.

Goal: simultaneously give the K562, HepG2, AND SKNSH oracles a wide
activity range across the same library.
"""
import os, random

DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200
N_SEQS = 50000
random.seed(7)

records = []  # (k562, hepg2, sknsh, seq)
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12:
            continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s):
            continue
        try:
            k = float(cols[5]); h = float(cols[6]); sn = float(cols[7])
        except ValueError:
            continue
        records.append((k, h, sn, s))

print(f"Got {len(records)} candidates")
each_extreme = 8334  # 6 extremes * 8334 ≈ 50k

chosen = set()
for idx, name in [(0, "K562"), (1, "HepG2"), (2, "SKNSH")]:
    records.sort(key=lambda x: x[idx])
    bottom = [r[3] for r in records[:each_extreme]]
    top = [r[3] for r in records[-each_extreme:]]
    chosen.update(bottom)
    chosen.update(top)

print(f"After dedup: {len(chosen)} sequences")

if len(chosen) < N_SEQS:
    pool = [r[3] for r in records if r[3] not in chosen]
    random.shuffle(pool)
    needed = N_SEQS - len(chosen)
    chosen.update(pool[:needed])

chosen_list = list(chosen)
random.shuffle(chosen_list)
chosen_list = chosen_list[:N_SEQS]
print(f"Final: {len(chosen_list)} sequences")

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen_list:
        f.write(s + "\n")
