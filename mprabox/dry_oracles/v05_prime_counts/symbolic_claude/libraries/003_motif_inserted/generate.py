"""Experiment 003: motif insertion into uniform random background.

Generate 50K uniform-random sequences (good baseline), then insert one of 4
candidate motifs at a random position in each. 12500 sequences per motif.

The motifs all have ~uniform composition so global library composition stays
close to uniform — isolating the effect of LOCAL STRUCTURE / motif presence.
"""
import os
import numpy as np

SEED = 2
N = 50_000
L = 200
ALPHA = "0123"

MOTIFS = [
    "010101010101",  # dinucleotide repeat M1
    "001100110011",  # M2
    "121212121212",  # M3
    "012301230123",  # cyclic M4
]
ML = len(MOTIFS[0])  # 12

def main():
    rng = np.random.default_rng(SEED)
    arr = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    # assign motif index per sequence
    motif_idx = np.repeat(np.arange(4), N // 4)
    rng.shuffle(motif_idx)
    # position of motif within sequence
    positions = rng.integers(0, L - ML + 1, size=N)
    # convert motifs to int arrays
    motif_arrs = [np.array([int(c) for c in m], dtype=np.int8) for m in MOTIFS]
    for i in range(N):
        p = int(positions[i])
        arr[i, p:p + ML] = motif_arrs[motif_idx[i]]
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
    print(f"sampled base proportions: {(counts / counts.sum()).round(3).tolist()}")

if __name__ == "__main__":
    main()
