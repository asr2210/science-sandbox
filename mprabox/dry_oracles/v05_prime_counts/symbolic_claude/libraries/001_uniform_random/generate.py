"""Experiment 001: uniform random baseline.

50,000 strings of length 200, each character iid uniform over {0,1,2,3}.
Fixed seed for reproducibility.
"""
import os
import numpy as np

SEED = 0
N = 50_000
L = 200
ALPHA = "0123"

def main():
    rng = np.random.default_rng(SEED)
    # sample integers 0..3 then map to chars
    arr = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    # build strings efficiently
    lut = np.array([ord(c) for c in ALPHA], dtype=np.uint8)
    bytes_arr = lut[arr]  # (N, L) uint8 ascii codes
    lines = [row.tobytes().decode("ascii") for row in bytes_arr]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} sequences to {out_path}")
    # sanity
    assert len(lines) == N
    assert all(len(s) == L for s in lines)
    assert set("".join(lines[:10])) <= set(ALPHA)

if __name__ == "__main__":
    main()
