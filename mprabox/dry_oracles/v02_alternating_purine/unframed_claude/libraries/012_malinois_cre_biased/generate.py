"""Bias toward CRE data_project sequences (likely engineered enhancers).

CRE class has only ~14k 200bp sequences. Take all of them, then fill
the rest with triextreme-style picks from GTEX+UKBB.
"""
import os, random
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200
N_SEQS = 50000
random.seed(12)

cre_seqs = []
other_records = []  # (k, h, sn, seq)
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12: continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s): continue
        try:
            k = float(cols[5]); h = float(cols[6]); sn = float(cols[7])
        except ValueError: continue
        if cols[2] == "CRE":
            cre_seqs.append(s)
        else:
            other_records.append((k, h, sn, s))

print(f"CRE: {len(cre_seqs)}, other: {len(other_records)}")

chosen = set(cre_seqs)
# Oversample per-cell extremes to cover overlaps
for idx in [0, 1, 2]:
    other_records.sort(key=lambda r: r[idx])
    for r in other_records[:20000] + other_records[-20000:]:
        chosen.add(r[3])
        if len(chosen) >= N_SEQS: break
    if len(chosen) >= N_SEQS: break

chosen = list(chosen)
random.shuffle(chosen)
chosen = chosen[:N_SEQS]
assert len(chosen) == N_SEQS, f"Only {len(chosen)}"
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen: f.write(s + "\n")
print(f"Wrote {len(chosen)}")
