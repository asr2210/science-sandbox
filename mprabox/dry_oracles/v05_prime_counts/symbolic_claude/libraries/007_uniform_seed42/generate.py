"""Experiment 007: uniform random with seed=42 (noise diagnostic).

Establishes noise floor of the score across same-distribution different draws.
"""
import os
import numpy as np

SEED = 42
N = 50_000
L = 200
ALPHA = "0123"

def main():
    rng = np.random.default_rng(SEED)
    arr = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    lut = np.array([ord(c) for c in ALPHA], dtype=np.uint8)
    bytes_arr = lut[arr]
    lines = [row.tobytes().decode("ascii") for row in bytes_arr]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {N} sequences to {out_path}")

if __name__ == "__main__":
    main()
