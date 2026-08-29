"""Experiment 004: Random background with embedded TF motifs.

Each sequence = 200bp random background + 1-6 embedded consensus
TF motifs at random positions/orientations. Uses ~25 well-characterized
TFs spanning the three cell types and ubiquitous regulators.

Rationale: tests whether the MPRA simulator/model responds to TF
motif content. If yes -> motifs matter and we should design libraries
around motif diversity. If no -> the simulator measures something else.

For generalization: motif vocabulary is shared across cell types — a
model that learns motif effects in K562/HepG2/SKNSH should transfer.
"""
import os
import numpy as np

SEED = 42
N = 50_000
L = 200

# Consensus sequences for well-characterized TFs (forward strand)
# Curated from JASPAR/Hocomoco for major regulators across cell types
TF_MOTIFS = {
    # K562 (erythroid/myeloid)
    "GATA1":  "AGATAAGA",
    "KLF1":   "CACACCC",
    "SPI1":   "AAAGAGGAAGT",     # PU.1
    "TAL1":   "CAGCTGCT",
    "RUNX1":  "TGTGGTTT",
    "MYB":    "YAACTGC".replace("Y","C"),
    # HepG2 (liver)
    "HNF4A":  "CAAAGTCCA",
    "HNF1A":  "GTTAATNATTAAC".replace("N","A"),
    "FOXA1":  "TGTTTGC",
    "CEBPA":  "ATTGCGCAAT",
    "NR1H4":  "AGTTCAATGACCT",
    # SK-N-SH (neural)
    "NEUROD1":"CAGCTGCC",
    "ASCL1":  "CAGCTG",
    "REST":   "TTCAGCACCATGGACAG",
    "ZIC":    "GGGTGGTC",
    "POU3F2": "ATGCAAAT",
    # Ubiquitous
    "SP1":    "GGGGCGGGG",
    "AP1":    "TGASTCA".replace("S","C"),  # AP-1: TGA(C/G)TCA
    "CREB":   "TGACGTCA",
    "NFKB":   "GGGAATTTCC",
    "CTCF":   "CCGCGNGGNGGCAG".replace("N","A"),
    "YY1":    "CCATNTT".replace("N","T"),
    "MYC":    "CACGTG",
    "ELK1":   "ACCGGAAGT",
    "NRF1":   "GCGCATGCGC",
}
MOTIFS = list(TF_MOTIFS.values())
print(f"motif pool: {len(MOTIFS)} motifs, lengths {sorted(set(len(m) for m in MOTIFS))}")

rng = np.random.default_rng(SEED)
ABC = np.array(list("ACGT"))

def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def random_bg(length):
    return "".join(ABC[rng.integers(0, 4, size=length)])

seqs = []
for n in range(N):
    bg = list(random_bg(L))
    # Sample 1-6 motifs to embed
    k = int(rng.integers(1, 7))
    motif_indices = rng.integers(0, len(MOTIFS), size=k)
    chosen = [MOTIFS[i] for i in motif_indices]
    # Try to place them without overlap
    placed = []
    for m in chosen:
        # pick orientation
        if rng.random() < 0.5:
            m = revcomp(m)
        ml = len(m)
        # pick position, avoid overlap with already placed
        for _ in range(20):
            pos = int(rng.integers(0, L - ml + 1))
            if not any(not (pos + ml <= ps or pos >= ps + len(ms)) for ps, ms in placed):
                placed.append((pos, m))
                break
    for pos, m in placed:
        for i, c in enumerate(m):
            bg[pos + i] = c
    seqs.append("".join(bg))

assert len(seqs) == N
assert all(len(s) == L for s in seqs)
assert all(set(s) <= set("ACGT") for s in seqs)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {N} seqs to {out}")
