"""Top 50k Malinois sequences ranked by max(|K562|, |HepG2|, |SKNSH|).

Picks the most strongly-active sequences regardless of which cell line.
Should give wider activity range and stronger motif content per sequence.
"""
import os

DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200
N_SEQS = 50000

records = []  # (rank_metric, seq)
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12:
            continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s):
            continue
        try:
            k = float(cols[5]); h = float(cols[6]); sn = float(cols[7])
        except ValueError:
            continue
        metric = max(abs(k), abs(h), abs(sn))
        records.append((metric, s))

records.sort(key=lambda x: -x[0])
chosen = [s for _, s in records[:N_SEQS]]
print(f"Top metric range: {records[0][0]:.3f} .. {records[N_SEQS-1][0]:.3f}")

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen:
        f.write(s + "\n")
print(f"Wrote {len(chosen)} sequences")
