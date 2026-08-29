"""Experiment 006: HIGH-density biological-style motifs (assume 0123 -> ACGT).

Insert MANY motifs per sequence (~80 bp = 40% coverage) into uniform random
backgrounds. Test if motif density matters.
"""
import os
import numpy as np

SEED = 6
N = 50_000
L = 200
ALPHA = "0123"

# Bigger motif library; canonical TF binding consensuses (one mapping guess 0,1,2,3=A,C,G,T).
MOTIFS = [
    np.array([3, 0, 3, 0, 0, 0], dtype=np.int8),         # TATA       (TATAAA)
    np.array([2, 2, 2, 1, 2, 2], dtype=np.int8),         # Sp1 GC-box (GGGCGG)
    np.array([1, 0, 1, 2, 3, 2], dtype=np.int8),         # E-box      (CACGTG)
    np.array([3, 2, 0, 2, 3, 1, 0], dtype=np.int8),      # AP-1       (TGAGTCA)
    np.array([1, 1, 0, 0, 3], dtype=np.int8),            # CCAAT      (CCAAT)
    np.array([2, 2, 2, 2, 1, 3, 3, 3, 1, 1], dtype=np.int8),  # NFkB  (GGGGCTTTCC) approximated
    np.array([3, 2, 0, 1, 2, 3, 1, 0], dtype=np.int8),   # CREB       (TGACGTCA)
    np.array([0, 2, 2, 0, 0, 3, 2, 3], dtype=np.int8),   # p53        (AGGAATGT) approx
]

def place_many(motif_arrs, L, rng, num_inserts, max_tries=300):
    """Place num_inserts motifs (random choices from motif_arrs) at random
    non-overlapping positions. Returns list of (pos, motif_idx)."""
    placements = []
    used = []
    for _ in range(num_inserts):
        idx = int(rng.integers(0, len(motif_arrs)))
        ml = motif_arrs[idx].shape[0]
        for _ in range(max_tries):
            p = int(rng.integers(0, L - ml + 1))
            if not any(not (p + ml <= s or p >= e) for s, e in used):
                placements.append((p, idx))
                used.append((p, p + ml))
                break
        # if no placement found, just skip this insert
    return placements

def main():
    rng = np.random.default_rng(SEED)
    arr = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    # Insert ~12 motifs per sequence (avg motif length ~7 -> ~84 bp = 42% coverage)
    for i in range(N):
        placements = place_many(MOTIFS, L, rng, num_inserts=12)
        for p, idx in placements:
            ml = MOTIFS[idx].shape[0]
            arr[i, p:p + ml] = MOTIFS[idx]
    lut = np.array([ord(c) for c in ALPHA], dtype=np.uint8)
    bytes_arr = lut[arr]
    lines = [row.tobytes().decode("ascii") for row in bytes_arr]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {N} sequences to {out_path}")
    # composition check
    flat = arr[:1000].flatten()
    counts = np.bincount(flat, minlength=4)
    print(f"base proportions: {(counts / counts.sum()).round(3).tolist()}")

if __name__ == "__main__":
    main()
