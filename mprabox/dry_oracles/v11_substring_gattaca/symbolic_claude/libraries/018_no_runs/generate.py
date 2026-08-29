"""[43,57] composition + greedy arrangement with NO same-char adjacent positions.
Tests if anti-autocorrelation (opposite of Markov runs) helps.
Per-position distribution stays uniform across library (good for a, b).
Dinucleotide distribution changes (no same-char dinucleotides).
"""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 43, 57

valid = []
for c0 in range(LO, HI + 1):
    for c1 in range(LO, HI + 1):
        for c2 in range(LO, HI + 1):
            c3 = L - c0 - c1 - c2
            if LO <= c3 <= HI:
                valid.append((c0, c1, c2, c3))
valid = np.array(valid)
print(f"# valid count tuples: {len(valid)}")


def arrange_no_runs(counts, rng):
    """Greedy: at each step, pick a random char != prev with highest remaining count."""
    remaining = list(counts)
    out = np.empty(sum(counts), dtype=np.int8)
    prev = -1
    for i in range(len(out)):
        # available chars: those with remaining > 0 AND != prev
        avail = [c for c in range(4) if remaining[c] > 0 and c != prev]
        if not avail:
            # fallback (shouldn't happen for [43,57])
            avail = [c for c in range(4) if remaining[c] > 0]
        # weight by remaining count to avoid running out
        weights = np.array([remaining[c] for c in avail], dtype=float)
        weights /= weights.sum()
        ch = rng.choice(avail, p=weights)
        out[i] = ch
        remaining[ch] -= 1
        prev = ch
    return out


OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
chars = np.array(list("0123"))
with open(OUT, "w") as f:
    for i in range(N):
        c = valid[rng.integers(0, len(valid))]
        idx = arrange_no_runs(tuple(c), rng)
        f.write("".join(chars[idx]) + "\n")
print(f"wrote {N} no-runs sequences")
