"""Experiment 007: 50% GC random with CpG dinucleotide depletion.

Real human DNA has CpG depleted ~5x relative to expectation. If the
predictors were trained on real human DNA, our i.i.d. uniform baseline
may differ from their training distribution. Test by making sequences
match real-DNA dinucleotide structure while keeping GC=50%.

1st-order Markov chain. Stationary marginal A=T=C=G=0.25, but
transition C->G suppressed (so CpG dinucleotide rate ≈ 0.012 instead of 0.0625).
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

# Build a transition matrix T[i,j] = P(next=j | curr=i).
# Want stationary distribution = uniform [.25,.25,.25,.25]
# Want P(curr=C, next=G) = 0.012 (CpG rate)
# So T[C, G] = 0.012 / 0.25 = 0.048.
# Distribute the "missing" 0.25-0.048 = 0.202 mass from C across other targets
# Keep symmetry: T[C,A]=T[C,T]=T[C,C]=(1-0.048)/3 ≈ 0.3173
# For other rows, keep uniform 0.25.
T = np.full((4, 4), 0.25)
# rows ordered A,C,G,T (indices 0,1,2,3)
C, G = 1, 2
T[C] = (1 - 0.048) / 3
T[C, G] = 0.048

# compute stationary distribution; won't be exactly uniform but close
pi = np.ones(4) / 4
for _ in range(200):
    pi = pi @ T
print(f"stationary distribution (A,C,G,T): {pi}, GC={pi[1]+pi[2]:.3f}")

rng = np.random.default_rng(7)

def sample_chain(length, start_idx=None):
    out = np.empty(length, dtype=np.int8)
    s = int(rng.integers(4)) if start_idx is None else start_idx
    out[0] = s
    for k in range(1, length):
        s = int(rng.choice(4, p=T[s]))
        out[k] = s
    return out

# Vectorized sampling: generate all sequences in a loop (50k x 200 fine)
seqs = []
for _ in range(N):
    idx = sample_chain(L)
    seqs.append("".join(ALPHABET[idx]))

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {len(seqs)} sequences to {OUT}")
print(f"first: {seqs[0][:60]}...")
