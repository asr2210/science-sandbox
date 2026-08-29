"""Experiment 006: random uniform + PWM-sampled JASPAR motifs at lambda=3.

Same design as exp 004 except motifs are sampled from each TF's PWM
(probabilistic instances) rather than the fixed consensus. This gives the
model realistic motif variation — the same TF appears as varied sequences
matching its PWM, not the same fixed string repeated.

Hypothesis: PWM-sampled motifs > consensus motifs because (a) avoids
fixed-string overfitting and (b) better matches eval sequences with natural
motif variation.
"""
import numpy as np
from pathlib import Path
from pyjaspar import jaspardb

N = 50_000
L = 200
SEED = 0
LAMBDA = 3


def pwm_from_motif(m):
    """Return (4, length) probability matrix in ACGT order."""
    A = np.array(m.counts["A"], dtype=float)
    C = np.array(m.counts["C"], dtype=float)
    G = np.array(m.counts["G"], dtype=float)
    T = np.array(m.counts["T"], dtype=float)
    arr = np.stack([A, C, G, T], axis=0)
    col_sum = arr.sum(axis=0, keepdims=True)
    return arr / col_sum  # (4, L)


def main():
    rng = np.random.default_rng(SEED)
    alphabet_str = "ACGT"
    alphabet = np.array(list(alphabet_str))

    # Background: random uniform
    bg = rng.integers(0, 4, size=(N, L))
    bg_chars = alphabet[bg]

    # Load motifs as PWMs
    jdb = jaspardb(release="JASPAR2024")
    motifs = jdb.fetch_motifs(collection="CORE", tax_group=["vertebrates"])
    pwms = []
    for m in motifs:
        try:
            p = pwm_from_motif(m)
            pwms.append(p)
        except Exception:
            continue
    print(f"loaded {len(pwms)} JASPAR PWMs")

    # Sample motif counts per sequence
    ks = rng.poisson(LAMBDA, size=N).clip(0, 10)
    total_injected = 0
    for i in range(N):
        k = int(ks[i])
        if k == 0:
            continue
        m_idx = rng.integers(0, len(pwms), size=k)
        used = []
        for mi in m_idx:
            P = pwms[mi]  # (4, ml)
            ml = P.shape[1]
            if ml > L:
                continue
            placed = False
            for _ in range(20):
                start = int(rng.integers(0, L - ml + 1))
                end = start + ml
                if all(end <= u_s or start >= u_e for u_s, u_e in used):
                    # sample motif instance from PWM, position by position
                    cum = np.cumsum(P, axis=0)  # (4, ml)
                    u = rng.random(ml)
                    # find base index per position
                    idx = (u[None, :] >= cum).sum(axis=0)  # (ml,)
                    instance = alphabet[idx]
                    bg_chars[i, start:end] = instance
                    used.append((start, end))
                    placed = True
                    total_injected += 1
                    break
    print(f"injected {total_injected} motifs total "
          f"(avg {total_injected/N:.2f} per sequence)")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in bg_chars:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"wrote {N} sequences to {out}")


if __name__ == "__main__":
    main()
