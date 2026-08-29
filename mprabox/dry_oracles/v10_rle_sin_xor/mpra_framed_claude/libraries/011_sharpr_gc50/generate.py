"""Experiment 011: Sharpr-MPRA fragments filtered to GC ∈ [0.45, 0.55].

Tests whether REAL MPRA-tested sequences can win when their composition is
matched to the eval distribution (random uniform GC ≈ 0.5). Sharpr full set
gave 0.4987 — bias was GC=0.572. Filter to keep only fragments with
145bp GC ∈ [0.45, 0.55] and pad with random flanks for overall GC ≈ 0.5.
"""
from pathlib import Path
import numpy as np
import h5py

N_SEQS = 50_000
SEQ_LEN = 200
FRAG_LEN = 145
SEED = 0
GC_LO, GC_HI = 0.45, 0.55
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
        # We want to filter by GC. Read in chunks.
        # one-hot channels: ACGT, channels 1 and 2 are C, G
        # Compute GC content efficiently by loading in chunks
        chunk_size = 50_000
        gc_all = np.zeros(N_total, dtype=np.float32)
        for start in range(0, N_total, chunk_size):
            end = min(start + chunk_size, N_total)
            chunk = X[start:end]  # (c, 145, 4)
            gc_all[start:end] = chunk[:, :, 1:3].sum(axis=(1, 2)) / FRAG_LEN

    mask = (gc_all >= GC_LO) & (gc_all <= GC_HI)
    n_avail = mask.sum()
    print(f"available fragments with GC in [{GC_LO}, {GC_HI}]: {n_avail}")
    if n_avail < N_SEQS:
        raise ValueError(f"Need {N_SEQS} but only {n_avail} available")

    avail_idx = np.where(mask)[0]
    idx = rng.choice(avail_idx, size=N_SEQS, replace=False)
    idx.sort()

    with h5py.File(SHARPR, "r") as f:
        X_sample = f["X/sequence"][idx]  # (50000, 145, 4)

    frag_idx = X_sample.argmax(axis=2).astype(np.int8)
    sums = X_sample.sum(axis=2)
    mask_bad = sums < 0.5
    if mask_bad.any():
        frag_idx[mask_bad] = rng.integers(0, 4, size=mask_bad.sum())
    frag_chars = alphabet[frag_idx]

    left_idx = rng.integers(0, 4, size=(N_SEQS, LEFT_PAD), dtype=np.int8)
    right_idx = rng.integers(0, 4, size=(N_SEQS, RIGHT_PAD), dtype=np.int8)
    left_chars = alphabet[left_idx]
    right_chars = alphabet[right_idx]

    full = np.concatenate([left_chars, frag_chars, right_chars], axis=1)
    seqs = ["".join(row) for row in full]

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)

    gc = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"GC: mean={gc.mean():.3f} std={gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
