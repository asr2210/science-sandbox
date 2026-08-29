"""
Experiment 001: probe with 6 strata of ~8333 sequences each.
Strata are placed in contiguous blocks so we can see if position-dependent
scoring exists (in case result.json gives per-row info).

Strata:
  A [0:8333]      uniform random
  B [8333:16666]  all '0'
  C [16666:25000] GC-rich (mostly 1 and 2)
  D [25000:33333] AT-rich (mostly 0 and 3)
  E [33333:41666] periodic 0123 repeat
  F [41666:50000] motif-strewn: random with '12102' (proxy 'CACGT') every ~20 bp
"""
import os, random

random.seed(42)

L = 200
N = 50000
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

lines = []

# Stratum A: uniform random
for _ in range(8333):
    lines.append("".join(random.choices(ALPHABET, k=L)))

# Stratum B: constant all '0'
for _ in range(8333):
    lines.append("0" * L)

# Stratum C: GC-rich (1,2 favored, weights chosen heavily)
gc_weights = [1, 4, 4, 1]
for _ in range(8334):
    lines.append("".join(random.choices(ALPHABET, weights=gc_weights, k=L)))

# Stratum D: AT-rich (0,3 favored)
at_weights = [4, 1, 1, 4]
for _ in range(8333):
    lines.append("".join(random.choices(ALPHABET, weights=at_weights, k=L)))

# Stratum E: periodic 0123 repeat
period = "0123"
periodic = (period * (L // 4 + 1))[:L]
for _ in range(8333):
    lines.append(periodic)

# Stratum F: motif-strewn random
motif = "12102"
for _ in range(8334):
    seq = list(random.choices(ALPHABET, k=L))
    # insert motif every 20 bp at positions 0, 20, 40, ...
    for start in range(0, L - len(motif) + 1, 20):
        for j, c in enumerate(motif):
            seq[start + j] = c
    lines.append("".join(seq))

assert len(lines) == N, f"got {len(lines)} expected {N}"
for i, s in enumerate(lines):
    assert len(s) == L, f"line {i} length {len(s)}"
    assert set(s) <= set(ALPHABET), f"bad chars in line {i}"

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {len(lines)} sequences to {OUT}")
