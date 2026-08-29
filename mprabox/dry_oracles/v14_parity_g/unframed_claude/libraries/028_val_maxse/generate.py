#!/usr/bin/env python3
"""Val chrs (7,13) sorted by MAX-SE (worst cell SE) ascending.
024 used mean SE; this filters by worst cell — sequences confident in ALL 3 cells."""
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
        mse = max(kse, hse, sse)
        rows.append((mse, s))

print(f"Val rows: {len(rows)}")
rows.sort(key=lambda x: x[0])
chosen = [s for _, s in rows[:N]]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} val max-SE filtered sequences to {out}")
print(f"Max-SE range: {rows[0][0]:.4f} to {rows[N-1][0]:.4f}")
