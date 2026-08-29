"""
Experiment 005: 8 strata of 6250 each (50000 total).

Tests whether more "anchor" points + diverse compositional spread improves
correlation. Strata:
  A: all-0 (constant anchor)
  B: all-1 (constant anchor)
  C: all-2 (constant anchor)
  D: all-3 (constant anchor)
  E: uniform random (unique per seq)
  F: GC-rich (unique per seq, chars 1,2 heavy)
  G: AT-rich (unique per seq, chars 0,3 heavy)
  H: 0123 periodic (constant anchor)

Hypothesis: 4 letter-constants + 1 periodic = 5 anchor points spanning
extreme positions in (f, g) space. If they're roughly collinear with the
natural data line, including them elongates the cloud and raises r.

Random strata still provide diverse "filling".
"""
import os, random

random.seed(5)
L = 200
N = 50000
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

lines = []

# 4 constant letter anchors
lines += ["0"*L] * 6250
lines += ["1"*L] * 6250
lines += ["2"*L] * 6250
lines += ["3"*L] * 6250

# Stratum E: uniform random
for _ in range(6250):
    lines.append("".join(random.choices(ALPHABET, k=L)))

# Stratum F: GC-rich (1,2 favored)
for _ in range(6250):
    lines.append("".join(random.choices(ALPHABET, weights=[1,4,4,1], k=L)))

# Stratum G: AT-rich (0,3 favored)
for _ in range(6250):
    lines.append("".join(random.choices(ALPHABET, weights=[4,1,1,4], k=L)))

# Stratum H: 0123 periodic
periodic = ("0123" * (L // 4 + 1))[:L]
lines += [periodic] * 6250

assert len(lines) == N
for i, s in enumerate(lines):
    assert len(s) == L

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {len(lines)} sequences")
