"""Experiment 009: real Sharpr-MPRA sequences (K562/HepG2 enhancer-tiling library).

Sharpr-MPRA is the canonical MPRA training library: 914,348 145bp fragments
tiling 15,720 DNase-peak regions in K562/HepG2 (+ HUVEC, H1-hESC), measured
under both minP and SV40P promoters. Used by MPRA-DragoNN and many other
sequence-to-activity models.

Sampling 50,000 fragments uniformly at random from the training set. Each
145bp fragment is padded to 200bp by adding ~27.5 bp of RANDOM UNIFORM flanks
on each side (preserving the eval-matching binomial GC=0.5 in flanks).
"""
from pathlib import Path
import numpy as np
import h5py

N_SEQS = 50_000
SEQ_LEN = 200
FRAG_LEN = 145
SEED = 0
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
SHARPR = REPO / "data" / "sharpr_train.hdf5"

LEFT_PAD = (SEQ_LEN - FRAG_LEN) // 2  # 27
RIGHT_PAD = SEQ_LEN - FRAG_LEN - LEFT_PAD  # 28


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet = np.array(["A", "C", "G", "T"])

    with h5py.File(SHARPR, "r") as f:
        X = f["X/sequence"]  # (N, 145, 4)
        N_total = X.shape[0]
        idx = rng.choice(N_total, size=N_SEQS, replace=False)
        idx.sort()
        X_sample = X[idx]  # (50000, 145, 4)

    # One-hot to int
    frag_idx = X_sample.argmax(axis=2).astype(np.int8)  # (50000, 145)
    # detect any zero-only positions (no one-hot)
    sums = X_sample.sum(axis=2)
    mask_bad = sums < 0.5
    if mask_bad.any():
        # replace bad positions with random
        frag_idx[mask_bad] = rng.integers(0, 4, size=mask_bad.sum())
    frag_chars = alphabet[frag_idx]  # (50000, 145)

    # Generate random flanks
    left_idx = rng.integers(0, 4, size=(N_SEQS, LEFT_PAD), dtype=np.int8)
    right_idx = rng.integers(0, 4, size=(N_SEQS, RIGHT_PAD), dtype=np.int8)
    left_chars = alphabet[left_idx]
    right_chars = alphabet[right_idx]

    full = np.concatenate([left_chars, frag_chars, right_chars], axis=1)
    seqs = ["".join(row) for row in full]

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:200])

    gc = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"GC: mean={gc.mean():.3f} std={gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
