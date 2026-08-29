"""Experiment 023: variable N_MOTIFS per seq in {0,1,2,3,4,5} - more predicted variance.

If predictor scores correlate with motif density, library with WIDER density
distribution may yield higher Spearman (more spread → easier to rank).
"""
import numpy as np
import os
from pyjaspar import jaspardb

N_SEQ = 50000
LEN = 200
ALPHABET = list("ACGT")
NMOT_CHOICES = [0, 1, 2, 3, 4, 5]
NMOT_WEIGHTS = [1, 1, 1, 1, 1, 1]  # uniform mixture

TF_NAMES = [
    "SP1", "MYC", "MAX", "USF1", "USF2", "CREB1", "JUN", "FOS",
    "NRF1", "YY1", "NFYA", "NFYB", "GATA1", "GATA2", "ELF1", "ELK1",
    "ETS1", "KLF4", "EGR1", "TBP",
]

j = jaspardb(release="JASPAR2024")
motifs = []
for name in TF_NAMES:
    ms = j.fetch_motifs(species="9606", collection="CORE", tf_name=name)
    if ms:
        m = ms[0]
        counts = np.array([m.counts[b] for b in ALPHABET], dtype=float)
        probs = counts / counts.sum(axis=0, keepdims=True)
        motifs.append((name, probs))
print(f"Loaded {len(motifs)} PWMs")

rng = np.random.default_rng(20260623)
COMP = bytes.maketrans(b"ACGT", b"TGCA")
WP = np.array(NMOT_WEIGHTS, dtype=float)
WP = WP / WP.sum()


def rc(s):
    return s.translate(COMP)[::-1]


def sample_motif(rng, pwm):
    L = pwm.shape[1]
    return "".join(ALPHABET[rng.choice(4, p=pwm[:, i])] for i in range(L))


def gen_sequence(rng):
    idx = rng.integers(0, 4, size=LEN)
    seq = bytearray("".join(ALPHABET[i] for i in idx), "ascii")
    n_mot = int(rng.choice(NMOT_CHOICES, p=WP))
    used = []
    for _ in range(n_mot):
        _, pwm = motifs[int(rng.integers(0, len(motifs)))]
        m = sample_motif(rng, pwm).encode()
        if rng.random() < 0.5:
            m = rc(m)
        L = len(m)
        for _try in range(20):
            pos = int(rng.integers(0, LEN - L + 1))
            if all(not (pos < ue and pos + L > us) for us, ue in used):
                seq[pos:pos + L] = m
                used.append((pos, pos + L))
                break
    return seq.decode("ascii")


seqs = [gen_sequence(rng) for _ in range(N_SEQ)]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} variable-density sequences")
