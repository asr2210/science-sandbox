"""4x4x4 stratification with REPLACEMENT: equal samples per bin.

Off-diagonal bins (uncorrelated activities across cells) are rare — by
oversampling them with replacement we force the library to cover those
combinations. Each of the 64 bins contributes exactly 50000/64 ≈ 782
sequences (with repeats if bin too small).
"""
import os, random
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH=200; N_SEQS=50000; N_BINS=4
random.seed(25)

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

bucket_sizes = sorted([len(v) for v in buckets.values()])
print(f"Bucket sizes: min={bucket_sizes[0]} med={bucket_sizes[len(bucket_sizes)//2]} max={bucket_sizes[-1]}")

per = N_SEQS // (N_BINS**3) + 1  # 782
chosen=[]
for seqs in buckets.values():
    if len(seqs) >= per:
        random.shuffle(seqs)
        chosen.extend(seqs[:per])
    else:
        # oversample with replacement
        chosen.extend(random.choices(seqs, k=per))
random.shuffle(chosen); chosen=chosen[:N_SEQS]
out=os.path.join(os.path.dirname(__file__),"sequences_0.txt")
with open(out,"w") as f:
    for s in chosen: f.write(s+"\n")
print(f"Wrote {len(chosen)}")
