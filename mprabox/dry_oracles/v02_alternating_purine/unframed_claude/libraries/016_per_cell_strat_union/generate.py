"""Per-cell stratified union: each cell line gets 10 quantiles × 2k = 20k,
then union dedup, truncate/pad to 50k."""
import os, random
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200; N_SEQS = 50000; N_BINS = 10
PER_BIN = 2000
random.seed(16)

records = []
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12: continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s): continue
        try: k=float(cols[5]); h=float(cols[6]); sn=float(cols[7])
        except ValueError: continue
        records.append((k, h, sn, s))

chosen = set()
for idx in [0, 1, 2]:
    recs = sorted(records, key=lambda r: r[idx])
    n = len(recs); chunk = n // N_BINS
    for b in range(N_BINS):
        lo = b*chunk; hi = (b+1)*chunk if b < N_BINS-1 else n
        bucket = recs[lo:hi]; random.shuffle(bucket)
        for r in bucket[:PER_BIN]:
            chosen.add(r[3])

print(f"After union: {len(chosen)}")
chosen = list(chosen); random.shuffle(chosen)

if len(chosen) < N_SEQS:
    pool = [r[3] for r in records if r[3] not in set(chosen)]
    random.shuffle(pool)
    chosen.extend(pool[:N_SEQS - len(chosen)])

chosen = chosen[:N_SEQS]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen: f.write(s + "\n")
print(f"Wrote {len(chosen)}")
