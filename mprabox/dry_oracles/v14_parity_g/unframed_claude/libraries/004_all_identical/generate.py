#!/usr/bin/env python3
"""All 50K sequences identical -> zero variance. Tests whether score depends on
per-sequence variability (Pearson r needs variance)."""
import os

N = 50_000
L = 200
SEQ = "ACGT" * 50  # exactly 200bp

assert len(SEQ) == L

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join([SEQ] * N) + "\n")
print(f"Wrote {N} sequences (all identical) to {out}")
