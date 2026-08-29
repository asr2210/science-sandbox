"""Focused K562 extremes: 25k highest + 25k lowest K562_log2FC.

Probe: does focused K562 variance lift K562 r (vs the SKNSH-focused
exp 006 which barely moved K562)?
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
        if len(cols) < 12:
            continue
        s = cols[11].upper()
        if len(s) != LENGTH or any(c not in "ACGT" for c in s):
            continue
        try:
            k = float(cols[5])
        except ValueError:
            continue
        records.append((k, s))

records.sort(key=lambda x: x[0])
half = N_SEQS // 2
chosen = records[:half] + records[-half:]
print(f"K562 range: {records[0][0]:.3f} .. {records[half-1][0]:.3f}  |  {records[-half][0]:.3f} .. {records[-1][0]:.3f}")

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for _, s in chosen:
        f.write(s + "\n")
print(f"Wrote {N_SEQS} sequences")
