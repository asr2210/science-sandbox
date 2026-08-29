"""Experiment 019: per-seq target GC ~ Normal(0.5, 0.04) — wider than 013/018."""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
GC_MEAN = 0.50
GC_STD = 0.04
HERE = Path(__file__).resolve()


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))
    seqs = []
    for _ in range(N_SEQS):
        gc = float(np.clip(rng.normal(GC_MEAN, GC_STD), 0.30, 0.70))
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=SEQ_LEN, p=p)
        seqs.append("".join(alphabet[idx]))
    realized = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"realized GC: mean={realized.mean():.3f} std={realized.std():.3f}")
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
