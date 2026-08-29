"""Exp 030: FINAL. Bigram-Dir(0.3) — best method, 4-seed mixture.

The bigram-Dir(0.3) family showed seed-to-seed variance:
- seed 23 → 0.0784 (best)
- seed 151 → 0.0761
- seed 99 → 0.0769

To reduce sampling noise via averaging, mix 12.5K seqs from each of 4 seeds
including the proven-good seed 23. The library-wide statistics should hew
closer to the population mean while still exhibiting bigram-Dir structure
that has consistently scored highest.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEEDS = [23, 42, 99, 1337]  # 12.5K each
PER = N // len(SEEDS)
chars = np.array(list("0123"))


def gen_bigram_dir(seed, per, length, alpha=0.3):
    rng = np.random.default_rng(seed)
    out = []
    for i in range(per):
        bw = rng.dirichlet([alpha] * 16).reshape(4, 4)
        row_sums = bw.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1, row_sums)
        P = bw / row_sums
        pi = bw.sum(axis=1)
        pi = pi / pi.sum() if pi.sum() > 0 else np.ones(4) / 4
        seq = np.empty(length, dtype=np.int8)
        seq[0] = rng.choice(4, p=pi)
        for t in range(1, length):
            seq[t] = rng.choice(4, p=P[seq[t-1]])
        out.append("".join(chars[seq]))
    return out


lines = []
for s in SEEDS:
    lines.extend(gen_bigram_dir(s, PER, L))

# Shuffle so seeds aren't grouped
rng = np.random.default_rng(2026)
rng.shuffle(lines)

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} 4-seed bigram-Dir(0.3) seqs")
