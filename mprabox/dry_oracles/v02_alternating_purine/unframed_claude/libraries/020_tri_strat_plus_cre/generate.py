"""Tri-stratified 5×5×5 with CRE-class sequences guaranteed included.

Take all ~14k CRE class first, then fill remaining ~36k by tri-stratified
sampling on non-CRE records.
"""
import os, random
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200; N_SEQS = 50000; N_BINS = 5
random.seed(20)

cre = []
other = []
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12: continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s): continue
        try: k=float(cols[5]); h=float(cols[6]); sn=float(cols[7])
        except ValueError: continue
        if cols[2] == "CRE":
            cre.append((k, h, sn, s))
        else:
            other.append((k, h, sn, s))

print(f"CRE={len(cre)} other={len(other)}")

def quantiles(vals, n):
    vs = sorted(vals); return [vs[int(len(vs)*i/n)] for i in range(1,n)]
ks = quantiles([r[0] for r in other], N_BINS)
hs = quantiles([r[1] for r in other], N_BINS)
sns = quantiles([r[2] for r in other], N_BINS)
def bin_of(v, edges):
    for i, e in enumerate(edges):
        if v < e: return i
    return len(edges)

# CRE: include all
chosen = set(r[3] for r in cre)
need = N_SEQS - len(chosen)
per_bucket = max(1, need // (N_BINS**3) + 1)
print(f"Need {need} more; per_bucket={per_bucket}")

buckets = defaultdict(list)
for r in other:
    buckets[(bin_of(r[0], ks), bin_of(r[1], hs), bin_of(r[2], sns))].append(r[3])
for seqs in buckets.values():
    random.shuffle(seqs)
    for s in seqs[:per_bucket]:
        chosen.add(s)

chosen = list(chosen)
random.shuffle(chosen)
chosen = chosen[:N_SEQS]
print(f"Wrote {len(chosen)}")
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen: f.write(s + "\n")
