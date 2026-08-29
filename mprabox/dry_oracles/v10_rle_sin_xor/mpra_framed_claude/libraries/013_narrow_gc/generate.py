"""Experiment 013: random sequences with very narrow per-seq GC ~ Normal(0.5, 0.03).

Exp 004 used broad GC (0.10-0.90) and was disastrous. Exp 001 used binomial
GC≈0.5 implicitly via Uniform(ACGT). This tests whether SLIGHT GC tightening
around 0.5 could help — i.e., make the per-seq GC less variable than binomial
random uniform (which has std ≈ 0.035 for 200bp).
"""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
GC_MEAN = 0.50
GC_STD = 0.02
HERE = Path(__file__).resolve()


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))

    seqs = []
    gcs = []
    for _ in range(N_SEQS):
        gc = float(np.clip(rng.normal(GC_MEAN, GC_STD), 0.35, 0.65))
        # Sample with given GC: probabilities A=T=(1-gc)/2, C=G=gc/2
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=SEQ_LEN, p=p)
        seqs.append("".join(alphabet[idx]))
        gcs.append(gc)

    assert len(seqs) == N_SEQS
    gc_arr = np.array(gcs)
    print(f"target GC: mean={gc_arr.mean():.3f} std={gc_arr.std():.3f}")

    realized_gc = np.array(
        [(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]]
    )
    print(f"realized GC (first 1k): mean={realized_gc.mean():.3f} std={realized_gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
