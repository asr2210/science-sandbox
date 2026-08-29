"""HepG2 extremes (25k highest + 25k lowest HepG2_log2FC).

Probes whether HepG2 oracle behaves identically to K562 oracle. If yes,
focused HepG2 extremes should reproduce exp 009 (focused K562) results
with K562_r == HepG2_r unchanged in pattern.
"""
import os
DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200
N_SEQS = 50000
records = []
with open(DATA) as f:
    f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12: continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s): continue
        try: h = float(cols[6])
        except ValueError: continue
        records.append((h, s))
records.sort(key=lambda x: x[0])
half = N_SEQS // 2
chosen = records[:half] + records[-half:]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for _, s in chosen: f.write(s + "\n")
print(f"Wrote {N_SEQS}")
