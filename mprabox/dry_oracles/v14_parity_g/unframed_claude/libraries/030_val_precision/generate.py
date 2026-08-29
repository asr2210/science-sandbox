#!/usr/bin/env python3
"""Val chrs sorted by total precision (1/SE^2 summed across cells).
Fisher-style ranking: emphasizes very-low-SE values more than mean.
Top 50K by precision."""
import os

N = 50_000
L = 200
VAL_CHRS = {"7", "13"}
SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

rows = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    ichr = h.index("chr")
    iKse = h.index("K562_lfcSE")
    iHse = h.index("HepG2_lfcSE")
    iSse = h.index("SKNSH_lfcSE")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        if parts[ichr] not in VAL_CHRS: continue
        s = parts[iseq].upper()
        if len(s) != L or not set(s) <= set("ACGT"): continue
        try:
            kse = float(parts[iKse]); hse = float(parts[iHse]); sse = float(parts[iSse])
        except ValueError:
            continue
        prec = 1.0/(kse**2 + 1e-9) + 1.0/(hse**2 + 1e-9) + 1.0/(sse**2 + 1e-9)
        rows.append((-prec, s))  # neg so ascending = highest precision first

print(f"Val rows: {len(rows)}")
rows.sort()
chosen = [s for _, s in rows[:N]]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} val high-precision sequences to {out}")
print(f"Precision range: {-rows[0][0]:.1f} to {-rows[N-1][0]:.1f}")
