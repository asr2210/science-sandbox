"""Final: 4x4x4 stratification, with within-bin selection seeded for
diversity AND including sequences from already-good replicates.

Strategy:
- Take union of unique sequences picked by 6 different seed runs of
  4x4x4 stratification.
- From the union, re-stratify 4x4x4 to ensure uniform joint coverage.
- Within each bin, randomize seed for selection.

Hypothesis: the seed-blend approach (027 = 0.191) plus a wider seed pool
gives the most stable, well-covered 4x4x4 sample.
"""
import os, random
from collections import defaultdict
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH=200; N_SEQS=50000; N_BINS=4

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

# Union over 6 seeds: each takes ~per per bin
union = set()
for seed in [18, 100, 27, 127, 227, 42]:
    rnd = random.Random(seed)
    per = N_SEQS // (N_BINS**3) + 1
    for seqs in buckets.values():
        seqs2 = list(seqs); rnd.shuffle(seqs2)
        union.update(seqs2[:per])
print(f"Union of 6 seeds: {len(union)}")

# Bucket the union back
union_buckets = defaultdict(list)
for r in records:
    if r[3] in union:
        union_buckets[(bin_of(r[0],ks),bin_of(r[1],hs),bin_of(r[2],sns))].append(r[3])

# Sample 782 per bin from union
final_rng = random.Random(530)
per_final = N_SEQS // (N_BINS**3) + 1
final = []
for seqs in union_buckets.values():
    seqs2 = list(set(seqs)); final_rng.shuffle(seqs2)
    final.extend(seqs2[:per_final])
final_rng.shuffle(final); final = final[:N_SEQS]

# top-up if short
if len(final) < N_SEQS:
    used = set(final)
    for r in records:
        if r[3] not in used:
            final.append(r[3]); used.add(r[3])
            if len(final) >= N_SEQS: break
final = final[:N_SEQS]
print(f"Wrote {len(final)}")
out=os.path.join(os.path.dirname(__file__),"sequences_0.txt")
with open(out,"w") as f:
    for s in final: f.write(s+"\n")
