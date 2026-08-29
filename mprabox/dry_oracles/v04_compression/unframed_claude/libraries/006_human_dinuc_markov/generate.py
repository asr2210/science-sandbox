"""Experiment 006: First-order Markov chain with human-genome dinucleotide stats.

Bulk human genome dinucleotide frequencies (Lander et al; well-known):
  AA 9.5%   AC 5.0%   AG 7.0%   AT 7.3%
  CA 7.4%   CC 5.3%   CG 1.0%   CT 7.0%
  GA 5.9%   GC 4.4%   GG 5.3%   GT 5.0%
  TA 5.7%   TC 5.9%   TG 7.4%   TT 9.5%

Generates 50k x 200bp sequences whose first-order statistics match these.
Preserves ~50% GC overall but suppresses CpG and (slightly) TpA, like real
mammalian non-functional genome.
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = list("ACGT")

# joint dinucleotide frequencies (percent)
joint = np.array([
    [9.5, 5.0, 7.0, 7.3],   # AA AC AG AT
    [7.4, 5.3, 1.0, 7.0],   # CA CC CG CT
    [5.9, 4.4, 5.3, 5.0],   # GA GC GG GT
    [5.7, 5.9, 7.4, 9.5],   # TA TC TG TT
], dtype=float)
joint = joint / joint.sum()

# stationary marginal P(base) = row sums of joint
marginal = joint.sum(axis=1)

# transition P(next | prev) = joint[prev, next] / marginal[prev]
transition = joint / marginal[:, None]

rng = np.random.default_rng(20260607)


def gen_sequence(rng):
    out = np.empty(LEN, dtype=np.int8)
    out[0] = rng.choice(4, p=marginal)
    for i in range(1, LEN):
        out[i] = rng.choice(4, p=transition[out[i - 1]])
    return "".join(ALPHABET[b] for b in out)


seqs = [gen_sequence(rng) for _ in range(N_SEQ)]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} sequences (human dinuc Markov) to {out_path}")
print(f"  Sample: {seqs[0]}")
