"""Max-variance SKNSH library: 25k highest + 25k lowest SKNSH_log2FC.

Hypothesis: oracle correlation is largest when our library spans the
SKNSH activity range, since correlation rewards covariance.
"""
import os

DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"
LENGTH = 200
N_SEQS = 50000

records = []  # (sknsh_lfc, seq)
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
            sknsh = float(cols[7])
        except ValueError:
            continue
        records.append((sknsh, s))

print(f"Got {len(records)} candidates")
records.sort(key=lambda x: x[0])
half = N_SEQS // 2
chosen = records[:half] + records[-half:]
print(f"Bottom SKNSH range: {records[0][0]:.3f} .. {records[half-1][0]:.3f}")
print(f"Top    SKNSH range: {records[-half][0]:.3f} .. {records[-1][0]:.3f}")

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for _, s in chosen:
        f.write(s + "\n")
print(f"Wrote {N_SEQS} sequences")
