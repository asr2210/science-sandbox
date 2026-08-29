"""2D stratification on (K562+HepG2 combined, SKNSH) — exploit the fact
that K562 and HepG2 give identical oracle scores.

Approach: average K562 and HepG2 lfc (they're highly correlated, r=0.80)
and treat as one axis; SKNSH as the second axis. Stratify 10x10 = 100
cells × 500 each. More within-bucket diversity than 4x4x4.
"""
import os, random
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH=200; N_SEQS=50000; N_BINS=10
random.seed(28)

records=[]
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols)<12: continue
        s = cols[11].upper()
        if len(s)!=LENGTH or any(c not in "ACGT" for c in s): continue
        try: k=float(cols[5]); h=float(cols[6]); sn=float(cols[7])
        except ValueError: continue
        records.append(((k+h)/2, sn, s))

def quantiles(vals,n):
    vs=sorted(vals); return [vs[int(len(vs)*i/n)] for i in range(1,n)]
kh_edges = quantiles([r[0] for r in records], N_BINS)
sn_edges = quantiles([r[1] for r in records], N_BINS)
def bin_of(v,edges):
    for i,e in enumerate(edges):
        if v<e: return i
    return len(edges)

buckets=defaultdict(list)
for r in records:
    buckets[(bin_of(r[0],kh_edges), bin_of(r[1],sn_edges))].append(r[2])
per = N_SEQS // (N_BINS**2) + 1
print(f"Buckets: {len(buckets)}/{N_BINS**2}; per={per}")
chosen=[]
for seqs in buckets.values():
    random.shuffle(seqs); chosen.extend(seqs[:per])
random.shuffle(chosen)
# top up if short
if len(chosen) < N_SEQS:
    used = set(chosen)
    extra = []
    for seqs in buckets.values():
        for s in seqs:
            if s not in used: extra.append(s); used.add(s)
    random.shuffle(extra)
    chosen.extend(extra[:N_SEQS - len(chosen)])
chosen=chosen[:N_SEQS]
assert len(chosen) == N_SEQS
out=os.path.join(os.path.dirname(__file__),"sequences_0.txt")
with open(out,"w") as f:
    for s in chosen: f.write(s+"\n")
print(f"Wrote {len(chosen)}")
