#!/usr/bin/env python3
"""Gosai sequences with HIGHEST RATIO of signal/SE (most reliable measurements).
Score = sum_cell |log2FC_cell| / SE_cell (a kind of z-score sum).
Picks sequences whose effects are most confidently nonzero across cell lines.
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
    iKse = h.index("K562_lfcSE")
    iHse = h.index("HepG2_lfcSE")
    iSse = h.index("SKNSH_lfcSE")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        s = parts[iseq].upper()
        if len(s) != L or not set(s) <= set("ACGT"): continue
        try:
            k = float(parts[iK]); h_ = float(parts[iH]); sn = float(parts[iS])
            kse = float(parts[iKse]); hse = float(parts[iHse]); sse = float(parts[iSse])
            if kse <= 0 or hse <= 0 or sse <= 0: continue
        except (ValueError, ZeroDivisionError):
            continue
        z = abs(k)/kse + abs(h_)/hse + abs(sn)/sse
        rows.append((z, s))

print(f"Valid rows: {len(rows)}")
rows.sort(reverse=True, key=lambda x: x[0])
chosen = [s for _, s in rows[:N]]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} high-confidence Gosai sequences to {out}")
print(f"Top z-sum: {rows[0][0]:.2f}, 50000th: {rows[N-1][0]:.2f}")
