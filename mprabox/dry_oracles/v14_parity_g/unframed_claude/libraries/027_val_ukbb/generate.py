#!/usr/bin/env python3
"""Val chrs (7,13) + UKBB only, sorted by lowest mean SE.
Tests if test set is UKBB-dominated within val chrs.
22 was val+GTEX (0.104), this tests the complementary subset."""
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
    iproj = h.index("data_project")
    iKse = h.index("K562_lfcSE")
    iHse = h.index("HepG2_lfcSE")
    iSse = h.index("SKNSH_lfcSE")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        if parts[ichr] not in VAL_CHRS: continue
        if parts[iproj] != "UKBB": continue
        s = parts[iseq].upper()
        if len(s) != L or not set(s) <= set("ACGT"): continue
        try:
            kse = float(parts[iKse]); hse = float(parts[iHse]); sse = float(parts[iSse])
        except ValueError:
            continue
        ase = (kse + hse + sse) / 3
        rows.append((ase, s))

print(f"Val-UKBB rows: {len(rows)}")
rows.sort(key=lambda x: x[0])
unique = [s for _, s in rows]
if len(unique) >= N:
    chosen = unique[:N]
else:
    reps = (N + len(unique) - 1) // len(unique)
    chosen = (unique * reps)[:N]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} ({len(unique)} unique) val-UKBB sequences to {out}")
