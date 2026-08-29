"""Experiment 004: biological-style motifs (assume 0123 -> ACGT).

Insert 4 canonical TF binding motifs into each sequence at random positions.
Background uniform random.

Motifs (consensus, length 6-7):
  TATA-box       TATAAA  -> 3,0,3,0,0,0
  GC-box (Sp1)   GGGCGG  -> 2,2,2,1,2,2
  E-box (Myc)    CACGTG  -> 1,0,1,2,3,2
  AP-1           TGAGTCA -> 3,2,0,2,3,1,0
Total inserted: 6+6+6+7 = 25 bp per sequence = 12.5% coverage.

Positions chosen randomly with no overlap.
"""
import os
import numpy as np

SEED = 4
N = 50_000
L = 200
ALPHA = "0123"

MOTIFS = [
    np.array([3, 0, 3, 0, 0, 0], dtype=np.int8),     # TATA
    np.array([2, 2, 2, 1, 2, 2], dtype=np.int8),     # GC-box
    np.array([1, 0, 1, 2, 3, 2], dtype=np.int8),     # E-box
    np.array([3, 2, 0, 2, 3, 1, 0], dtype=np.int8),  # AP-1
]

def place_nonoverlap(positions_lengths, L, rng, max_tries=100):
    """Place each (len) at a random pos in [0,L-len] with no overlap.
    Returns positions or None if failed."""
    positions = []
    used = []  # list of (start, end)
    for ml in positions_lengths:
        for _ in range(max_tries):
            p = int(rng.integers(0, L - ml + 1))
            overlap = any(not (p + ml <= s or p >= e) for s, e in used)
            if not overlap:
                positions.append(p)
                used.append((p, p + ml))
                break
        else:
            return None
    return positions

def main():
    rng = np.random.default_rng(SEED)
    arr = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    lens = [m.shape[0] for m in MOTIFS]
    fail = 0
    for i in range(N):
        # randomize motif placement order
        order = rng.permutation(len(MOTIFS))
        lengths = [lens[j] for j in order]
        positions = place_nonoverlap(lengths, L, rng)
        if positions is None:
            fail += 1
            continue
        for k, j in enumerate(order):
            p = positions[k]
            arr[i, p:p + lens[j]] = MOTIFS[j]
    print(f"placement failures: {fail}")
    lut = np.array([ord(c) for c in ALPHA], dtype=np.uint8)
    bytes_arr = lut[arr]
    lines = [row.tobytes().decode("ascii") for row in bytes_arr]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {N} sequences to {out_path}")
    # composition check
    flat = np.concatenate([arr[i] for i in range(min(1000, N))])
    counts = np.bincount(flat, minlength=4)
    print(f"base proportions: {(counts / counts.sum()).round(3).tolist()}")

if __name__ == "__main__":
    main()
