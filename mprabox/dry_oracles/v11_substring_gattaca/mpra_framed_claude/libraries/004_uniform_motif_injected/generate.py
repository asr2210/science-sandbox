"""Experiment 004: random uniform background with JASPAR motif consensus injected.

Background: 50k random uniform 200bp sequences.
For each sequence: inject k ~ Poisson(lambda=3) JASPAR vertebrate motifs at
random non-overlapping positions. Motifs are the consensus sequence of a
uniformly-sampled motif from JASPAR2024 CORE vertebrates (879 motifs).

Hypothesis: explicit motif signal on top of broad k-mer coverage beats random
uniform alone. Motif vocabulary covers ~700+ TFs from many tissues, so signal
generalizes beyond the 3 measured cell types.
"""
import numpy as np
from pathlib import Path
from pyjaspar import jaspardb

N = 50_000
L = 200
SEED = 0
LAMBDA = 3


def main():
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))

    # Background: random uniform
    bg = rng.integers(0, 4, size=(N, L))
    bg_chars = alphabet[bg]  # (N, L) of chars

    # Load motifs and convert consensus to char arrays
    jdb = jaspardb(release="JASPAR2024")
    motifs = jdb.fetch_motifs(collection="CORE", tax_group=["vertebrates"])
    motif_consensus = []
    for m in motifs:
        s = str(m.consensus).upper()
        # filter to ACGT-only (consensus letters)
        if set(s).issubset(set("ACGT")):
            motif_consensus.append(np.array(list(s)))
    print(f"loaded {len(motif_consensus)} JASPAR motifs (consensus, ACGT-only)")

    # Inject motifs
    sample_ks = rng.poisson(LAMBDA, size=N)
    sample_ks = np.clip(sample_ks, 0, 10)

    motif_count_total = 0
    for i in range(N):
        k = int(sample_ks[i])
        if k == 0:
            continue
        # pick k motifs
        m_idx = rng.integers(0, len(motif_consensus), size=k)
        # place greedily without overlap
        used = []  # list of (start, end)
        attempts = 0
        for mi in m_idx:
            m = motif_consensus[mi]
            ml = len(m)
            if ml > L:
                continue
            placed = False
            for _ in range(20):
                start = int(rng.integers(0, L - ml + 1))
                end = start + ml
                if all(end <= u_start or start >= u_end for u_start, u_end in used):
                    bg_chars[i, start:end] = m
                    used.append((start, end))
                    placed = True
                    motif_count_total += 1
                    break
                attempts += 1
            # if not placed after 20 tries, skip
    print(f"injected {motif_count_total} motifs total "
          f"(avg {motif_count_total/N:.2f} per sequence)")

    out = Path(__file__).parent / "sequences_0.txt"
    with out.open("w") as f:
        for row in bg_chars:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"wrote {N} sequences to {out}")


if __name__ == "__main__":
    main()
