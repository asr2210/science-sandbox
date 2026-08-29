"""
Experiment 001: Pure uniform random sequences.

Generates 50,000 sequences of 200bp by sampling A/C/G/T uniformly.
This is a baseline - a library with no biological signal. We expect
this to score near zero on all evaluation sets, but it tells us:
  (a) the floor for eval performance, and
  (b) the wall-clock time of one full prepare.py cycle.

No external data dependencies.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 0

def main():
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))
    # Vectorized: draw all indices at once
    idx = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    seqs = alphabet[idx]
    # Join each row
    lines = ["".join(row) for row in seqs]
    with open(OUT, "w") as f:
        f.write("\n".join(lines) + "\n")
    # Sanity check
    with open(OUT) as f:
        lines = f.read().splitlines()
    assert len(lines) == N, f"got {len(lines)} lines"
    for i, l in enumerate(lines[:5]):
        assert len(l) == L, f"line {i} length {len(l)}"
        assert set(l) <= set("ACGT")
    print(f"wrote {len(lines)} sequences to {OUT}")

if __name__ == "__main__":
    main()
