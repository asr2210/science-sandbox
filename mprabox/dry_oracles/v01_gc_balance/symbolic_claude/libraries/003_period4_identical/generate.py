"""003_period4_identical — 50,000 identical copies of "0123"*50 (length 200).
Diagnostic: per-string r vs across-string column-wise r.
"""
import os
N, L = 50_000, 200
pat = ("0123" * (L // 4))[:L]
assert len(pat) == L
line = pat + "\n"
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write(line * N)
print(f"Wrote {N} copies of {pat[:20]}... to {out}")
