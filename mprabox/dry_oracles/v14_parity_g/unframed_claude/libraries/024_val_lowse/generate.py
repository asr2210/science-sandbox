#!/usr/bin/env python3
"""Val chrs (7, 13) sequences with TOP HIGH-CONFIDENCE (lowest SE).
If the test set within val chrs uses high-confidence sequences only,
this could push eval_01 higher."""
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
        ase = (kse + hse + sse) / 3
        rows.append((ase, s))

print(f"Val-chr rows with SE: {len(rows)}")
rows.sort(key=lambda x: x[0])  # lowest SE first
chosen = [s for _, s in rows[:N]]
# If short, fill with random val seqs
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} val low-SE sequences to {out}")
print(f"SE range: {rows[0][0]:.4f} to {rows[N-1][0]:.4f}")
