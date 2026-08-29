"""Marginally uniform: pick 50k such that each cell line's activity
distribution is approximately uniform. Independent rejection sampling.

For each candidate, accept it with probability inversely proportional to
the local density of its activity vector in each dimension.
"""
import os, random
import numpy as np
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH=200; N_SEQS=50000
random.seed(24)
np.random.seed(24)

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

ks = np.array([r[0] for r in records])
hs = np.array([r[1] for r in records])
sns = np.array([r[2] for r in records])

NB = 20
def density_weights(arr, n_bins):
    """For each value, weight = 1 / (count in its bin). Encourages uniform sampling."""
    edges = np.quantile(arr, np.linspace(0,1,n_bins+1))
    edges[0] -= 1; edges[-1] += 1
    bins = np.digitize(arr, edges) - 1
    bins = np.clip(bins, 0, n_bins-1)
    counts = np.bincount(bins, minlength=n_bins)
    return 1.0 / counts[bins]

w_k = density_weights(ks, NB)
w_h = density_weights(hs, NB)
w_sn = density_weights(sns, NB)
# combined weight: geometric mean approximates uniform marginals
w = (w_k * w_h * w_sn) ** (1/3)
w = w / w.sum()

idx = np.random.choice(len(records), size=N_SEQS, replace=False, p=w)
chosen = [records[i][3] for i in idx]
random.shuffle(chosen)
out=os.path.join(os.path.dirname(__file__),"sequences_0.txt")
with open(out,"w") as f:
    for s in chosen: f.write(s+"\n")
print(f"Wrote {len(chosen)}")
