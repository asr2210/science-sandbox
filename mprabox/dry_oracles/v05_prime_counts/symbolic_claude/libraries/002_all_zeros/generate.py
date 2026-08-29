"""Constant library: 50,000 copies of '0' * 200. Probe whether the
scoring depends on within-library variance (correlation requires variance)."""
import os
N = 50_000
L = 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    line = "0" * L + "\n"
    f.writelines([line] * N)
print(f"Wrote {N} sequences (all zeros) of length {L}")
