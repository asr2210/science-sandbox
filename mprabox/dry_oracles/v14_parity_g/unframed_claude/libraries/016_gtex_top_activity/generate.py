#!/usr/bin/env python3
"""GTEX subset, top 50K by activity. Combines two winning strategies:
- GTEX project (best on eval_01)
- High activity magnitude (best on eval_04)
"""
import os

N = 50_000
L = 200

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

rows = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    iproj = h.index("data_project")
    iK = h.index("K562_log2FC")
    iH = h.index("HepG2_log2FC")
    iS = h.index("SKNSH_log2FC")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        if parts[iproj] != "GTEX": continue
        s = parts[iseq].upper()
        if len(s) != L or not set(s) <= set("ACGT"): continue
        try:
            k = float(parts[iK]); h_ = float(parts[iH]); sn = float(parts[iS])
        except ValueError:
            continue
        score = max(abs(k), abs(h_), abs(sn))
        rows.append((score, s))

print(f"GTEX valid rows: {len(rows)}")
rows.sort(reverse=True, key=lambda x: x[0])
chosen = [s for _, s in rows[:N]]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} top-activity GTEX sequences to {out}")
print(f"Top score: {rows[0][0]:.4f}, 50000th: {rows[N-1][0]:.4f}")
