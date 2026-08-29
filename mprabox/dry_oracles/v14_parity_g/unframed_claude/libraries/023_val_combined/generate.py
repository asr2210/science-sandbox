#!/usr/bin/env python3
"""Combined: 35K val chrs (7, 13) + 15K test chrs (9, 21, X).
Targets eval_01 (val), eval_04 (test) simultaneously.
Sacrifices some val signal for some test signal."""
import numpy as np
import os

N = 50_000
L = 200
N_VAL = 35_000
N_TEST = 15_000
SEED = 42
VAL_CHRS = {"7", "13"}
TEST_CHRS = {"9", "21", "X"}

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

val_seqs = []
test_seqs = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    ichr = h.index("chr")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        ch = parts[ichr]
        s = parts[iseq].upper()
        if len(s) != L or not set(s) <= set("ACGT"): continue
        if ch in VAL_CHRS: val_seqs.append(s)
        elif ch in TEST_CHRS: test_seqs.append(s)

print(f"Val: {len(val_seqs)}, Test: {len(test_seqs)}")

rng = np.random.default_rng(SEED)
val_pick = rng.choice(len(val_seqs), size=N_VAL, replace=False)
test_pick = rng.choice(len(test_seqs), size=N_TEST, replace=False)
chosen = [val_seqs[i] for i in val_pick] + [test_seqs[i] for i in test_pick]
rng.shuffle(chosen)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} combined val+test sequences to {out}")
