"""Hybrid: 4x4x4 stratified, but average across 3 random seeds.

Generate 3 independent 4x4x4 stratified samples (different bin seeds AND
within-bin random seeds), take union of all picked sequences. Should give
~50k unique with broader representation than single seed.
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

# Per-seed sample, then union
all_chosen = set()
for seed in [27, 127, 227]:
    rnd = random.Random(seed)
    per = 50000 // (N_BINS**3) + 1
    for seqs in buckets.values():
        seqs2 = list(seqs); rnd.shuffle(seqs2)
        for s in seqs2[:per]:
            all_chosen.add(s)

print(f"Union size: {len(all_chosen)}")
# Now we have ~60-120k uniques. Downsample to 50k preserving bin balance.
# Bucket the chosen back into bins and pick uniformly.
bin_of_chosen = defaultdict(list)
for r in records:
    if r[3] in all_chosen:
        key = (bin_of(r[0],ks), bin_of(r[1],hs), bin_of(r[2],sns))
        bin_of_chosen[key].append(r[3])

per_final = N_SEQS // (N_BINS**3) + 1
final = []
rnd = random.Random(327)
for seqs in bin_of_chosen.values():
    seqs2 = list(set(seqs)); rnd.shuffle(seqs2)
    final.extend(seqs2[:per_final])
rnd.shuffle(final); final = final[:N_SEQS]
print(f"Final: {len(final)}")
out=os.path.join(os.path.dirname(__file__),"sequences_0.txt")
with open(out,"w") as f:
    for s in final: f.write(s+"\n")
