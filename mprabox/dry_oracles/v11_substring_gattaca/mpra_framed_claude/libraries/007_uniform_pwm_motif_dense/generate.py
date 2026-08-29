"""Experiment 007: random uniform + PWM-sampled JASPAR motifs at lambda=10.

Same as exp 006 except higher motif density (λ=10 per sequence, ~50–100bp of
motif content per 200bp). Tests whether higher motif density extracts more
signal that the model can use.
"""
import numpy as np
from pathlib import Path
from pyjaspar import jaspardb

N = 50_000
L = 200
SEED = 0
LAMBDA = 10


def pwm_from_motif(m):
    A = np.array(m.counts["A"], dtype=float)
    C = np.array(m.counts["C"], dtype=float)
    G = np.array(m.counts["G"], dtype=float)
    T = np.array(m.counts["T"], dtype=float)
    arr = np.stack([A, C, G, T], axis=0)
    return arr / arr.sum(axis=0, keepdims=True)


def main():
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))
    bg = rng.integers(0, 4, size=(N, L))
    bg_chars = alphabet[bg]

    jdb = jaspardb(release="JASPAR2024")
    motifs = jdb.fetch_motifs(collection="CORE", tax_group=["vertebrates"])
    pwms = [pwm_from_motif(m) for m in motifs]
    print(f"loaded {len(pwms)} PWMs")

    ks = rng.poisson(LAMBDA, size=N).clip(0, 25)
    total_injected = 0
    for i in range(N):
        k = int(ks[i])
        if k == 0:
            continue
        m_idx = rng.integers(0, len(pwms), size=k)
        used = []
        for mi in m_idx:
            P = pwms[mi]
            ml = P.shape[1]
            if ml > L:
                continue
            placed = False
            for _ in range(40):
                start = int(rng.integers(0, L - ml + 1))
                end = start + ml
                if all(end <= u_s or start >= u_e for u_s, u_e in used):
                    cum = np.cumsum(P, axis=0)
                    u = rng.random(ml)
                    idx = (u[None, :] >= cum).sum(axis=0)
                    bg_chars[i, start:end] = alphabet[idx]
                    used.append((start, end))
                    placed = True
                    total_injected += 1
                    break
    print(f"injected {total_injected} motifs (avg {total_injected/N:.2f}/seq)")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in bg_chars:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"wrote {N} sequences to {out}")


if __name__ == "__main__":
    main()
