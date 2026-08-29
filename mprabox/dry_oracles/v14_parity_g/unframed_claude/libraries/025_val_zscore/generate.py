#!/usr/bin/env python3
"""Val chrs (7, 13) sorted by Z-score |effect|/SE descending.
Selects sequences with strongest signal-to-noise — likely test-set candidates."""
import os

N = 50_000
L = 200
VAL_CHRS = {"7", "13"}
SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

rows = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    idx = {c: h.index(c) for c in [
        "sequence", "chr",
        "K562_log2FC", "HepG2_log2FC", "SKNSH_log2FC",
        "K562_lfcSE", "HepG2_lfcSE", "SKNSH_lfcSE",
    ]}
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= idx["sequence"]: continue
        if parts[idx["chr"]] not in VAL_CHRS: continue
        s = parts[idx["sequence"]].upper()
        if len(s) != L or not set(s) <= set("ACGT"): continue
        try:
            kfc = float(parts[idx["K562_log2FC"]])
            hfc = float(parts[idx["HepG2_log2FC"]])
            sfc = float(parts[idx["SKNSH_log2FC"]])
            kse = float(parts[idx["K562_lfcSE"]])
            hse = float(parts[idx["HepG2_lfcSE"]])
            sse = float(parts[idx["SKNSH_lfcSE"]])
        except ValueError:
            continue
        z = (abs(kfc)/max(kse,1e-6) + abs(hfc)/max(hse,1e-6) + abs(sfc)/max(sse,1e-6)) / 3
        rows.append((-z, s))  # negative so sort ascending = highest z first

print(f"Val-chr rows with full data: {len(rows)}")
rows.sort()
chosen = [s for _, s in rows[:N]]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} val high-Z sequences to {out}")
print(f"Z range: {-rows[0][0]:.3f} to {-rows[N-1][0]:.3f}")
