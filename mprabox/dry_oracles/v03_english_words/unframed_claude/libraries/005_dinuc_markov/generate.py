"""Dinucleotide Markov chain matching mammalian genomic statistics.
Approximate human-genome dinucleotide frequencies (CpG depleted, AT slightly
biased). Conditional P(next | prev) computed from joint table.
"""
import numpy as np

# Approximate human autosomal dinucleotide frequencies (joint, fractions).
# Source: well-known approximation, CpG depleted.
JOINT = {
    "AA": 0.0987, "AC": 0.0510, "AG": 0.0716, "AT": 0.0731,
    "CA": 0.0732, "CC": 0.0532, "CG": 0.0096, "CT": 0.0723,
    "GA": 0.0596, "GC": 0.0420, "GG": 0.0535, "GT": 0.0510,
    "TA": 0.0566, "TC": 0.0593, "TG": 0.0727, "TT": 0.0992,
}
# normalize and build conditional table P(next | prev)
ALPH = "ACGT"
joint_arr = np.zeros((4, 4))
for i, a in enumerate(ALPH):
    for j, b in enumerate(ALPH):
        joint_arr[i, j] = JOINT[a + b]
joint_arr /= joint_arr.sum()
marg = joint_arr.sum(axis=1, keepdims=True)
cond = joint_arr / marg              # P(next | prev)
start_p = joint_arr.sum(axis=1)      # marginal of "prev"
start_p /= start_p.sum()

N, L = 50000, 200
rng = np.random.default_rng(5)
seqs = []
for _ in range(N):
    s = np.zeros(L, dtype=np.int64)
    s[0] = rng.choice(4, p=start_p)
    for t in range(1, L):
        s[t] = rng.choice(4, p=cond[s[t - 1]])
    seqs.append("".join(ALPH[i] for i in s))

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N} dinucleotide-Markov sequences")
