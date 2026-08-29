"""Experiment 004: broad-GC random sequences.

50,000 random sequences of length 200 where each sequence has a per-sequence
GC content sampled uniformly from [0.10, 0.90]. Each base is then drawn iid
with P(C)=P(G)=GC/2, P(A)=P(T)=(1-GC)/2.

This pushes per-sequence composition variance far beyond what binomial-uniform
random gives (which concentrates around 50% GC with std ~3.5%). If K562 is
composition-driven, this should match or exceed the random-uniform K562 score.
If the eval set contains broad-GC sequences, mean_r will exceed 0.5177.
"""
from pathlib import Path
import numpy as np

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
GC_LO = 0.10
GC_HI = 0.90


def main() -> None:
    rng = np.random.default_rng(SEED)
    gc = rng.uniform(GC_LO, GC_HI, size=N_SEQS)
    # base probs per sequence: [A, C, G, T] = [(1-gc)/2, gc/2, gc/2, (1-gc)/2]
    p_a = (1 - gc) / 2
    p_c = gc / 2
    # Per-sequence multinomial sampling. Vectorize via cumulative bands.
    u = rng.random(size=(N_SEQS, SEQ_LEN))
    # bands: A in [0, p_a), C in [p_a, p_a+p_c), G in [p_a+p_c, p_a+2*p_c), T in [p_a+2*p_c, 1)
    b1 = p_a[:, None]
    b2 = (p_a + p_c)[:, None]
    b3 = (p_a + 2 * p_c)[:, None]
    bases = np.where(u < b1, 0,
              np.where(u < b2, 1,
                np.where(u < b3, 2, 3)))
    alphabet = np.array(["A", "C", "G", "T"])
    seqs = ["".join(alphabet[row]) for row in bases]

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:200])

    # Sanity: print observed GC distribution
    gc_obs = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"observed GC (first 1000): mean={gc_obs.mean():.3f} std={gc_obs.std():.3f} "
          f"min={gc_obs.min():.3f} max={gc_obs.max():.3f}")

    out = Path(__file__).parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
