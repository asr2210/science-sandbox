"""Experiment 026: narrow GC (013/018 design) with seed=999 (3rd replicate)."""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 999
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
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
