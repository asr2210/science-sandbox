"""4x4x4 stratification on a low-SE filtered subset.

Filter: keep only sequences where K562_lfcSE, HepG2_lfcSE, and SKNSH_lfcSE
are below their respective medians (~25% of data after combining). Then
stratify 4×4×4 = 64 cells. Cleaner labels should give the trained oracle
better signal.
"""
import os, random
import numpy as np
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH=200; N_SEQS=50000; N_BINS=4
random.seed(29)

records=[]
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols)<12: continue
        s = cols[11].upper()
        if len(s)!=LENGTH or any(c not in "ACGT" for c in s): continue
        try:
            k=float(cols[5]); h=float(cols[6]); sn=float(cols[7])
            ks_=float(cols[8]); hs_=float(cols[9]); sns_=float(cols[10])
        except ValueError: continue
        if ks_<=0 or hs_<=0 or sns_<=0: continue
        records.append((k,h,sn,ks_,hs_,sns_,s))

# Compute SE medians
ks_se = np.array([r[3] for r in records])
hs_se = np.array([r[4] for r in records])
sns_se = np.array([r[5] for r in records])
mk, mh, msn = np.median(ks_se), np.median(hs_se), np.median(sns_se)
print(f"SE medians: K={mk:.3f} H={mh:.3f} S={msn:.3f}")

filt = [r for r in records if r[3]<=mk and r[4]<=mh and r[5]<=msn]
print(f"Filtered: {len(filt)} / {len(records)}")

def quantiles(vals,n):
    vs=sorted(vals); return [vs[int(len(vs)*i/n)] for i in range(1,n)]
ks=quantiles([r[0] for r in filt],N_BINS)
hs=quantiles([r[1] for r in filt],N_BINS)
sns=quantiles([r[2] for r in filt],N_BINS)
def bin_of(v,edges):
    for i,e in enumerate(edges):
        if v<e: return i
    return len(edges)

buckets=defaultdict(list)
for r in filt:
    buckets[(bin_of(r[0],ks),bin_of(r[1],hs),bin_of(r[2],sns))].append(r[6])
per = N_SEQS // (N_BINS**3) + 1
print(f"Buckets: {len(buckets)}; per={per}")

chosen=[]
for seqs in buckets.values():
    random.shuffle(seqs); chosen.extend(seqs[:per])
random.shuffle(chosen)
# top up if short
if len(chosen) < N_SEQS:
    used = set(chosen)
    extras = [r[6] for r in records if r[6] not in used]
    random.shuffle(extras)
    chosen.extend(extras[:N_SEQS - len(chosen)])
chosen=chosen[:N_SEQS]
out=os.path.join(os.path.dirname(__file__),"sequences_0.txt")
with open(out,"w") as f:
    for s in chosen: f.write(s+"\n")
print(f"Wrote {len(chosen)}")
