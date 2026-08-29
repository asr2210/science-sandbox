"""Experiment 018: replicate 013 (narrow target GC Normal(0.5, 0.02)) with seed=42.

013 gave the best mean_r so far (0.5206). Is it reproducible? Check by
running the same generation with seed=42 instead of seed=0.
"""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
GC_MEAN = 0.50
GC_STD = 0.02
HERE = Path(__file__).resolve()


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))

    seqs = []
    for _ in range(N_SEQS):
        gc = float(np.clip(rng.normal(GC_MEAN, GC_STD), 0.35, 0.65))
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=SEQ_LEN, p=p)
        seqs.append("".join(alphabet[idx]))

    realized_gc = np.array(
        [(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]]
    )
    print(f"realized GC: mean={realized_gc.mean():.3f} std={realized_gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
