"""4x4x4 stratification on RESIDUALS (decorrelated cell line axes).

Replace (K562, HepG2, SKNSH) with (K562, HepG2 - aK*K562 - b,
SKNSH - cK*K562 - dH*HepG2_resid - ...). Use a PCA-like decorrelation.
Then stratify in the decorrelated 3D space. This puts each bin in a
"unique combination" subspace rather than correlated bulk.
"""
import os, random
import numpy as np
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH=200; N_SEQS=50000; N_BINS=4
random.seed(26); np.random.seed(26)

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

X = np.array([(r[0], r[1], r[2]) for r in records])
X = X - X.mean(0)
# PCA via SVD
U, S, Vt = np.linalg.svd(X, full_matrices=False)
Y = X @ Vt.T  # principal component scores

def quantiles(vals,n):
    vs=sorted(vals); return [vs[int(len(vs)*i/n)] for i in range(1,n)]
edges = [quantiles(Y[:,d], N_BINS) for d in range(3)]
def bin_of(v,e):
    for i,t in enumerate(e):
        if v<t: return i
    return len(e)

buckets=defaultdict(list)
for i, r in enumerate(records):
    key = tuple(bin_of(Y[i,d], edges[d]) for d in range(3))
    buckets[key].append(r[3])

per = N_SEQS // (N_BINS**3) + 1
print(f"Buckets: {len(buckets)}; per={per}")
chosen=[]
for seqs in buckets.values():
    random.shuffle(seqs)
    chosen.extend(seqs[:per])
random.shuffle(chosen); chosen=chosen[:N_SEQS]
out=os.path.join(os.path.dirname(__file__),"sequences_0.txt")
with open(out,"w") as f:
    for s in chosen: f.write(s+"\n")
print(f"Wrote {len(chosen)}")
