"""002_all_zeros — 50,000 identical copies of '0'*200."""
import os
N, L = 50_000, 200
line = "0" * L + "\n"
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write(line * N)
print(f"Wrote {N} copies to {out}")
