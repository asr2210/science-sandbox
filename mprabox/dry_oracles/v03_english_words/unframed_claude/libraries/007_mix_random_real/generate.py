"""Experiment 007: 50% random uniform + 50% random real MPRA.

Hypothesis (from exp 005 vs 001): the K562/HepG2 r is limited by prediction
agreement (random uniform is near-optimal at ~0.59/0.62) and SKNSH r is
limited by prediction variance (random real lifts to ~0.12).

Mixing should:
- Keep K562/HepG2 close to random-uniform agreement (random half contributes).
- Boost SKNSH via the real half (variance from the real sequences).

If the cross-population covariance is favourable, the mix could clear 0.42
mean_r for the first time.
"""
import os
import random
import numpy as np

SOURCE = "/tmp/mpra_data.txt"
N_RAND = 25_000
N_REAL = 25_000
LEN = 200
ALPHABET = np.array(list("ACGT"))
RNG_SEED = 1007


def load_real(seed):
    seqs = []
    with open(SOURCE) as fh:
        next(fh)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 12:
                continue
            seq = parts[11].upper()
            if len(seq) != LEN or any(c not in "ACGT" for c in seq):
                continue
            seqs.append(seq)
    rng = random.Random(seed)
    return rng.sample(seqs, N_REAL)


def gen_random_uniform(seed, n, length):
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, 4, size=(n, length), dtype=np.int8)
    return ["".join(ALPHABET[row]) for row in idx]


def main():
    rng_shuffle = random.Random(RNG_SEED)
    real = load_real(RNG_SEED + 1)
    print(f"real loaded: {len(real)}")
    uni = gen_random_uniform(RNG_SEED + 2, N_RAND, LEN)
    print(f"random loaded: {len(uni)}")
    all_seqs = real + uni
    rng_shuffle.shuffle(all_seqs)
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(all_seqs))
        f.write("\n")
    print(f"wrote {len(all_seqs)} sequences (mix 50/50)")


if __name__ == "__main__":
    main()
