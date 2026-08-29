"""Experiment 003: Compositional gradient — 4 groups by dominant char.

Each group is biased toward one character (70%) with the others at 10%.
4 groups of 12,500 sequences each = 50,000 total.

Hypothesis: composition is the most basic feature most models learn.
Strong compositional bias should produce wider variance in predictions
than uniform random. If the model and target agree on composition,
Pearson r goes up. If they diverge, r goes down (or stays similar).
"""
import os
import numpy as np

N_PER_GROUP = 12_500
SEQ_LEN = 200
RNG = np.random.default_rng(seed=3)


def gen_group(dominant: int) -> list[str]:
    probs = np.full(4, 0.10)
    probs[dominant] = 0.70
    arr = RNG.choice(4, size=(N_PER_GROUP, SEQ_LEN), p=probs)
    return ["".join(chr(48 + b) for b in row) for row in arr]


def main():
    seqs: list[str] = []
    for dom in range(4):
        seqs.extend(gen_group(dom))
    assert len(seqs) == 50_000
    # Shuffle so groups are interleaved (in case any eval depends on order)
    RNG.shuffle(seqs)
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        f.write("\n".join(seqs) + "\n")
    print(f"Wrote {len(seqs)} sequences to {out_path}")


if __name__ == "__main__":
    main()
