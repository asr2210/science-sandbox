"""Experiment 004 — synthetic motif-scaffold library.

200 bp sequences built from:
  - random uniform DNA backbone
  - 0–10 inserted TF motifs at random positions, random strand
  - motif pool spans cell-type-specific (HepG2: HNF1/4, FOXA, CEBP;
    K562: GATA1; SK-N-SH: REST repressor) AND universal motifs
    (AP-1, ETS, NRF1, USF1/E-box, KLF/SP1, CTCF, MEF2).

The number of motifs is drawn so the library spans the full activity
spectrum: some sequences with zero motifs (low activity), some with
many (high activity). This produces a wide, predictable
sequence→activity relationship, which prior experiments suggest is
what the model actually needs to learn.

Why this generalizes beyond K562/HepG2/SK-N-SH:
The motif pool is intentionally diverse — it includes universally
expressed TF binding sites that appear in nearly every cell type
(AP-1, ETS, NRF1, USF1, KLF, CTCF). A model that learns to recognize
these motifs and predict their additive effect will have learned the
general grammar of motif → activity, not a cell-type-specific shortcut.

For unmeasured cell types, AP-1/ETS/NRF1/USF1 motifs still tend to
activate; HNF/GATA motifs may be silent (but the motif itself is still
detected). The model's motif library transfers; the *weights* may need
recalibration in a new cell type but the *features* are universal.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 4

# Canonical TF motifs (consensus or top-scoring), all uppercase ACGT
# only. Many drawn from JASPAR/HOCOMOCO; preferred 6–12 bp cores.
MOTIFS = {
    # Universal activators
    "AP1":   "TGACTCA",
    "ETS":   "ACCGGAAGT",       # ELK1/ETS canonical
    "NRF1":  "CGCATGCGCA",
    "USF":   "CACGTG",          # E-box, USF1/MYC
    "KLF":   "GGGGTGGGG",       # KLF/SP1 GC-box
    "CTCF":  "CCCTCTAGTGGCCAGCAGAGGG",  # CTCF canonical 19mer
    "MEF2":  "CTATAAATAG",
    "CREB":  "TGACGTCA",
    "NFY":   "CCAATCAG",
    "YY1":   "CCATCTT",
    # HepG2-biased
    "HNF1":  "GTTAATAATTAAC",
    "HNF4":  "AGGTCAAAGGTCA",
    "FOXA":  "TGTTTGTTT",
    "CEBP":  "ATTGCGCAAT",
    # K562-biased
    "GATA1": "AGATAAG",
    "TAL1":  "CAGCTG",          # E-box variant TAL1
    "RUNX":  "TGTGGTT",
    # Neural / SK-N-SH-relevant
    "NEURO": "CAGCTG",          # bHLH, neural lineage
    "NRSF":  "TTCAGCACCNNGGACAG".replace("N", "A"),  # REST motif
    # Generic repressors / chromatin
    "ZBTB":  "CTCCCC",
    # TATA-box (promoter)
    "TATA":  "TATAAAA",
    # Additional
    "STAT":  "TTCCCGGAA",
    "IRF":   "GAAAGTGAAAGT",
    "NFKB":  "GGGAATTCCC",
    "AR":    "AGAACATATGTTCT",
}

MOTIF_KEYS = list(MOTIFS.keys())
COMP = {ord("A"): "T", ord("C"): "G", ord("G"): "C", ord("T"): "A"}


def revcomp(s: str) -> str:
    return s.translate(COMP)[::-1]


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    alpha = np.array(list("ACGT"))
    backbone_idx = rng.integers(0, 4, size=(N, L))
    backbone = ["".join(alpha[r].tolist()) for r in backbone_idx]

    # number of inserts per sequence; uniform 0..10 to span range
    n_inserts = rng.integers(0, 11, size=N)
    seqs = []
    for i in range(N):
        bb = list(backbone[i])
        for _ in range(int(n_inserts[i])):
            mk = MOTIF_KEYS[rng.integers(0, len(MOTIF_KEYS))]
            motif = MOTIFS[mk]
            if rng.random() < 0.5:
                motif = revcomp(motif)
            if len(motif) >= L:
                continue
            pos = int(rng.integers(0, L - len(motif) + 1))
            bb[pos:pos + len(motif)] = list(motif)
        seqs.append("".join(bb))

    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N} seqs in {time.time()-t0:.1f}s; "
          f"inserts mean={n_inserts.mean():.2f}")


if __name__ == "__main__":
    main()
