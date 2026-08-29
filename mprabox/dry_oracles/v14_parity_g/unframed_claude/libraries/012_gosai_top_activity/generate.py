#!/usr/bin/env python3
"""Top 50K Gosai sequences by activity magnitude — highest signal.

Score = max(|K562_log2FC|, |HepG2_log2FC|, |SKNSH_log2FC|).
These are the most "informative" sequences (strongest predicted/measured
activity), and should give the highest signal-to-noise for the eval.
"""
import os

N = 50_000
L = 200

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

rows = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    iK = h.index("K562_log2FC")
    iH = h.index("HepG2_log2FC")
    iS = h.index("SKNSH_log2FC")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq:
            continue
        s = parts[iseq].upper()
        if len(s) != L or not set(s) <= set("ACGT"):
            continue
        try:
            k = float(parts[iK]); h_ = float(parts[iH]); sn = float(parts[iS])
        except ValueError:
            continue
        score = max(abs(k), abs(h_), abs(sn))
        rows.append((score, s))

print(f"Valid rows: {len(rows)}")
rows.sort(reverse=True, key=lambda x: x[0])
chosen = [s for _, s in rows[:N]]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} top-activity Gosai sequences to {out}")
print(f"Score range: {rows[0][0]:.4f} (top) to {rows[N-1][0]:.4f} (50000th)")
