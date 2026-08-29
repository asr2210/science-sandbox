"""Tri-stratified: 5 bins × 5 bins × 5 bins in (K562, HepG2, SKNSH) space.

Take up to 400 sequences per cube cell. Should give the most uniform
coverage of the joint activity distribution.
"""
import os, random
from collections import defaultdict

DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200
N_SEQS = 50000
N_BINS = 5
random.seed(14)

records = []
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12: continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s): continue
        try:
            k = float(cols[5]); h = float(cols[6]); sn = float(cols[7])
        except ValueError: continue
        records.append((k, h, sn, s))

# Quantile thresholds per cell line
def quantiles(vals, n):
    vals = sorted(vals)
    return [vals[int(len(vals) * i / n)] for i in range(1, n)]

ks = quantiles([r[0] for r in records], N_BINS)
hs = quantiles([r[1] for r in records], N_BINS)
sns = quantiles([r[2] for r in records], N_BINS)

def bin_of(v, edges):
    for i, e in enumerate(edges):
        if v < e: return i
    return len(edges)

buckets = defaultdict(list)
for r in records:
    k_bin = bin_of(r[0], ks)
    h_bin = bin_of(r[1], hs)
    sn_bin = bin_of(r[2], sns)
    buckets[(k_bin, h_bin, sn_bin)].append(r[3])

per_bucket = N_SEQS // (N_BINS**3) + 1  # ~401
print(f"Buckets occupied: {len(buckets)} / {N_BINS**3}; per_bucket={per_bucket}")

chosen = []
for key, seqs in buckets.items():
    random.shuffle(seqs)
    chosen.extend(seqs[:per_bucket])

random.shuffle(chosen)
if len(chosen) < N_SEQS:
    # top up by repeating from a flat pool
    flat = []
    for seqs in buckets.values():
        flat.extend(seqs)
    random.shuffle(flat)
    used = set(chosen)
    for s in flat:
        if s not in used:
            chosen.append(s); used.add(s)
            if len(chosen) >= N_SEQS: break

chosen = chosen[:N_SEQS]
assert len(chosen) == N_SEQS
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen: f.write(s + "\n")
print(f"Wrote {len(chosen)}")
