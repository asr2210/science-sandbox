"""Experiment 013: GC=0.60 background + PWM-sampled JASPAR motifs at λ=3.

Direct A/B test:
- vs exp 009 (GC=0.6, no motifs): does motif injection add value at GC=0.6?
- vs exp 006 (GC=0.5, PWM motifs λ=3 = 0.842): does the GC shift help motifs?
"""
import numpy as np
from pathlib import Path
from pyjaspar import jaspardb

N, L, SEED, GC, LAMBDA = 50_000, 200, 0, 0.60, 3


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
    probs = np.array([(1 - GC) / 2, GC / 2, GC / 2, (1 - GC) / 2])
    cum = np.cumsum(probs)
    u = rng.random(size=(N, L))
    idx = (u[..., None] >= cum).sum(axis=-1)
    bg_chars = alphabet[idx]

    jdb = jaspardb(release="JASPAR2024")
    motifs = jdb.fetch_motifs(collection="CORE", tax_group=["vertebrates"])
    pwms = [pwm_from_motif(m) for m in motifs]

    ks = rng.poisson(LAMBDA, size=N).clip(0, 10)
    total = 0
    for i in range(N):
        k = int(ks[i])
        if k == 0:
            continue
        m_idx = rng.integers(0, len(pwms), size=k)
        used = []
        for mi in m_idx:
            P = pwms[mi]; ml = P.shape[1]
            if ml > L:
                continue
            for _ in range(20):
                start = int(rng.integers(0, L - ml + 1)); end = start + ml
                if all(end <= u_s or start >= u_e for u_s, u_e in used):
                    cum_m = np.cumsum(P, axis=0)
                    uu = rng.random(ml)
                    bidx = (uu[None, :] >= cum_m).sum(axis=0)
                    bg_chars[i, start:end] = alphabet[bidx]
                    used.append((start, end))
                    total += 1
                    break
    print(f"injected {total} motifs avg {total/N:.2f}")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in bg_chars:
            f.write("".join(row.tolist())); f.write("\n")
    print(f"wrote {N} sequences")


if __name__ == "__main__":
    main()
