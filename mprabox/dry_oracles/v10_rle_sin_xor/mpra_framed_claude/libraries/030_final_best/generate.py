"""Experiment 030: 4-seed portfolio of narrow-GC random sequences.

027 (2-seed portfolio) gave 0.5231 — best result yet. Test if a 4-seed
portfolio (12,500 each from seeds 0, 42, 999, 2024) further improves.
"""
import numpy as np
from pathlib import Path

N_TOTAL = 50_000
N_PER_SEED = 12_500
SEEDS = [0, 42, 999, 2024]
SEQ_LEN = 200
GC_MEAN = 0.50
GC_STD = 0.02
HERE = Path(__file__).resolve()


def gen_narrow(seed, n):
    rng = np.random.default_rng(seed)
    alphabet = np.array(list("ACGT"))
    seqs = []
    for _ in range(n):
        gc = float(np.clip(rng.normal(GC_MEAN, GC_STD), 0.35, 0.65))
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=SEQ_LEN, p=p)
        seqs.append("".join(alphabet[idx]))
    return seqs


def main() -> None:
    all_seqs = []
    for s in SEEDS:
        all_seqs += gen_narrow(s, N_PER_SEED)
    assert len(all_seqs) == N_TOTAL
    rng_shuffle = np.random.default_rng(0)
    all_seqs = [all_seqs[i] for i in rng_shuffle.permutation(N_TOTAL)]
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(all_seqs) + "\n")
    print(f"wrote {len(all_seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
