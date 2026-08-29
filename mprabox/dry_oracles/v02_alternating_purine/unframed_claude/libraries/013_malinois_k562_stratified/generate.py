"""Stratified sample across K562 activity range: 5k from each of 10 quantiles.

Tests whether uniform coverage of activity space beats extremes-only
(extremes = bimodal, this = uniform).
"""
import os, random
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200
N_SEQS = 50000
random.seed(13)
N_BINS = 10
PER_BIN = N_SEQS // N_BINS

records = []
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12: continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s): continue
        try: k = float(cols[5])
        except ValueError: continue
        records.append((k, s))

records.sort(key=lambda x: x[0])
n = len(records)
chunk = n // N_BINS
chosen = []
for b in range(N_BINS):
    lo = b * chunk
    hi = (b+1) * chunk if b < N_BINS-1 else n
    bucket = records[lo:hi]
    random.shuffle(bucket)
    chosen.extend([s for _, s in bucket[:PER_BIN]])

random.shuffle(chosen)
chosen = chosen[:N_SEQS]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen: f.write(s + "\n")
print(f"Wrote {len(chosen)} (K562 stratified)")
