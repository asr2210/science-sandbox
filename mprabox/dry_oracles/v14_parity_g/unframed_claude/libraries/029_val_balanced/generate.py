#!/usr/bin/env python3
"""Val chrs balanced: 20K lowest-SE chr7 + 20K lowest-SE chr13 + 10K random val.
Test if eval test set uses balanced chr representation."""
import numpy as np
import os

N = 50_000
L = 200
N7 = 20_000
N13 = 20_000
N_RAND = 10_000
SEED = 42
SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

chr7 = []
chr13 = []
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
        ch = parts[ichr]
        if ch not in ("7", "13"): continue
        s = parts[iseq].upper()
        if len(s) != L or not set(s) <= set("ACGT"): continue
        try:
            kse = float(parts[iKse]); hse = float(parts[iHse]); sse = float(parts[iSse])
        except ValueError:
            continue
        ase = (kse + hse + sse) / 3
        if ch == "7": chr7.append((ase, s))
        else: chr13.append((ase, s))

chr7.sort(); chr13.sort()
print(f"chr7: {len(chr7)}, chr13: {len(chr13)}")
top7 = [s for _, s in chr7[:N7]]
top13 = [s for _, s in chr13[:N13]]
remaining = [s for _, s in chr7[N7:]] + [s for _, s in chr13[N13:]]
rng = np.random.default_rng(SEED)
fill_idx = rng.choice(len(remaining), size=N_RAND, replace=False)
fill = [remaining[i] for i in fill_idx]
chosen = top7 + top13 + fill
rng.shuffle(chosen)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} balanced val sequences to {out}")
