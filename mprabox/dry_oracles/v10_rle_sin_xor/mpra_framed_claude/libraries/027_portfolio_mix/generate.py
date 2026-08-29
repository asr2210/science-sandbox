"""Experiment 027: portfolio mix — 25k narrow-GC s=999 + 25k narrow-GC s=42.

The 2 best narrow-GC seeds were 026 (s=999, 0.5226) and 018 (s=42, 0.5210).
Test if mixing them gives the model more diverse seed-noise exposure.
Hypothesis: seed-mixing yields broader feature coverage without changing
composition statistics.
"""
import numpy as np
from pathlib import Path

N_SEQS_PER = 25_000
SEQ_LEN = 200
GC_MEAN = 0.50
GC_STD = 0.02
HERE = Path(__file__).resolve()


def gen_narrow(rng, n):
    alphabet = np.array(list("ACGT"))
    seqs = []
    for _ in range(n):
        gc = float(np.clip(rng.normal(GC_MEAN, GC_STD), 0.35, 0.65))
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=SEQ_LEN, p=p)
        seqs.append("".join(alphabet[idx]))
    return seqs


def main() -> None:
    rng1 = np.random.default_rng(999)
    rng2 = np.random.default_rng(42)
    a = gen_narrow(rng1, N_SEQS_PER)
    b = gen_narrow(rng2, N_SEQS_PER)
    seqs = a + b
    # shuffle
    rng_shuffle = np.random.default_rng(0)
    seqs = [seqs[i] for i in rng_shuffle.permutation(len(seqs))]
    assert len(seqs) == 50_000
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
