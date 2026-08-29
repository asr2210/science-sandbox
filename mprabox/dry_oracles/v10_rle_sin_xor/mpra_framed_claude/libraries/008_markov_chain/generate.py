"""Experiment 008: per-sequence Markov chain (dinucleotide-varying random).

For each sequence, sample a 4x4 transition matrix with random Dirichlet rows.
Generate a 200bp sequence from this Markov chain, starting from a random base.
Each sequence has different dinucleotide biases but average GC ~ 0.5 across
sequences (each row of the matrix is Dirichlet(1,1,1,1), so on average
transition probabilities are uniform).

This tests whether dinucleotide-level variation (beyond GC content) carries
predictive signal that the model can use for the harder cell types.
"""
from pathlib import Path
import numpy as np

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0

BASES = np.array(["A", "C", "G", "T"])


def main() -> None:
    rng = np.random.default_rng(SEED)
    # transitions[seq, from_base, to_base] - per-sequence transition matrix
    transitions = rng.dirichlet(np.ones(4), size=(N_SEQS, 4))
    starts = rng.integers(0, 4, size=N_SEQS)

    seqs: list[str] = []
    # Vectorize per-sequence sampling
    # For each sequence: start with starts[i], then iteratively sample next base
    seq_idx = np.zeros((N_SEQS, SEQ_LEN), dtype=np.int8)
    seq_idx[:, 0] = starts
    # cum: cumulative transition matrix [seq, from, 4]
    cum = transitions.cumsum(axis=2)
    rand_buf = rng.random(size=(N_SEQS, SEQ_LEN - 1))
    for pos in range(1, SEQ_LEN):
        prev = seq_idx[:, pos - 1]
        # for each sequence, get cum[i, prev[i], :] -> compare to rand
        rows = cum[np.arange(N_SEQS), prev]
        u = rand_buf[:, pos - 1, None]
        next_idx = (rows < u).sum(axis=1)  # 0..4
        next_idx = np.minimum(next_idx, 3)  # clamp
        seq_idx[:, pos] = next_idx

    chars = BASES[seq_idx]
    seqs = ["".join(row) for row in chars]

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:200])

    # sanity check composition
    gc = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs])
    print(f"GC distribution: mean={gc.mean():.3f} std={gc.std():.3f} min={gc.min():.3f} max={gc.max():.3f}")

    # check per-sequence dinucleotide diversity
    def dinuc_counts(s: str):
        d = np.zeros(16, dtype=int)
        for i in range(len(s) - 1):
            a = "ACGT".index(s[i])
            b = "ACGT".index(s[i + 1])
            d[a * 4 + b] += 1
        return d / d.sum()

    d_first = np.array([dinuc_counts(seqs[i]) for i in range(500)])
    print(f"avg dinuc fraction:\n{d_first.mean(axis=0).reshape(4,4)}")
    print(f"per-seq dinuc std (averaged across 16 dinuc):\n{d_first.std(axis=0).mean():.4f}")

    out = Path(__file__).parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
