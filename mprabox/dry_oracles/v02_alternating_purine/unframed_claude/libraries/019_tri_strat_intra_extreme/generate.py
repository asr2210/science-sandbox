"""Tri-stratified 5×5×5 but within each cube cell pick the sequences
with highest combined |z-score| (clean signal).

Hypothesis: keep joint coverage but bias toward clean / strong-signal
sequences within each bin → cleaner training signal for oracle.
"""
import os, random
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200; N_SEQS = 50000; N_BINS = 5
random.seed(19)

records = []
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12: continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s): continue
        try:
            k=float(cols[5]); h=float(cols[6]); sn=float(cols[7])
            ks_=float(cols[8]); hs_=float(cols[9]); sns_=float(cols[10])
        except ValueError: continue
        if ks_<=0 or hs_<=0 or sns_<=0: continue
        z = abs(k)/ks_ + abs(h)/hs_ + abs(sn)/sns_
        records.append((k, h, sn, z, s))

def quantiles(vals, n):
    vs = sorted(vals); return [vs[int(len(vs)*i/n)] for i in range(1,n)]
ks = quantiles([r[0] for r in records], N_BINS)
hs = quantiles([r[1] for r in records], N_BINS)
sns = quantiles([r[2] for r in records], N_BINS)
def bin_of(v, edges):
    for i, e in enumerate(edges):
        if v < e: return i
    return len(edges)

buckets = defaultdict(list)
for r in records:
    buckets[(bin_of(r[0], ks), bin_of(r[1], hs), bin_of(r[2], sns))].append(r)

per = N_SEQS // (N_BINS**3) + 2
print(f"Buckets: {len(buckets)}; per={per}")

chosen = []
for items in buckets.values():
    items.sort(key=lambda r: -r[3])  # highest z first
    chosen.extend([it[4] for it in items[:per]])

random.shuffle(chosen)
# top up if short
if len(chosen) < N_SEQS:
    used = set(chosen)
    for items in buckets.values():
        for it in items:
            if it[4] not in used:
                chosen.append(it[4]); used.add(it[4])
                if len(chosen) >= N_SEQS: break
        if len(chosen) >= N_SEQS: break
chosen = chosen[:N_SEQS]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen: f.write(s + "\n")
print(f"Wrote {len(chosen)}")
