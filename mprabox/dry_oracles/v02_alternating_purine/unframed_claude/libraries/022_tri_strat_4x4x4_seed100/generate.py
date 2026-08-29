"""Replicate 018 with seed=100 to estimate noise."""
import os, random
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH=200; N_SEQS=50000; N_BINS=4
random.seed(100)
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
        records.append((k,h,sn,s))
def quantiles(vals,n):
    vs=sorted(vals); return [vs[int(len(vs)*i/n)] for i in range(1,n)]
ks=quantiles([r[0] for r in records],N_BINS)
hs=quantiles([r[1] for r in records],N_BINS)
sns=quantiles([r[2] for r in records],N_BINS)
def bin_of(v,edges):
    for i,e in enumerate(edges):
        if v<e: return i
    return len(edges)
buckets=defaultdict(list)
for r in records:
    buckets[(bin_of(r[0],ks),bin_of(r[1],hs),bin_of(r[2],sns))].append(r[3])
per = N_SEQS // (N_BINS**3) + 1
chosen=[]
for seqs in buckets.values():
    random.shuffle(seqs); chosen.extend(seqs[:per])
random.shuffle(chosen); chosen=chosen[:N_SEQS]
out=os.path.join(os.path.dirname(__file__),"sequences_0.txt")
with open(out,"w") as f:
    for s in chosen: f.write(s+"\n")
print(f"Wrote {len(chosen)}")
