"""Experiment 025: balanced per-TF allocation, 3 motifs/seq from 17 TFs.

exp 010 had ~0.05 seed noise. Reduce variance: force EACH TF to appear in
roughly equal seqs, and each sequence draws 3 motifs WITHOUT REPLACEMENT from
the bank (3 distinct TFs). Same 17 TFs as exp 010.
"""
import numpy as np
import os
from pyjaspar import jaspardb

N_SEQ = 50000
LEN = 200
ALPHABET = list("ACGT")
N_MOTIFS = 3

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
n_tf = len(motifs)
print(f"Loaded {n_tf} PWMs")

rng = np.random.default_rng(20260625)
COMP = bytes.maketrans(b"ACGT", b"TGCA")


def rc(s):
    return s.translate(COMP)[::-1]


def sample_motif(rng, pwm):
    L = pwm.shape[1]
    return "".join(ALPHABET[rng.choice(4, p=pwm[:, i])] for i in range(L))


def gen_sequence(rng, tf_indices):
    idx = rng.integers(0, 4, size=LEN)
    seq = bytearray("".join(ALPHABET[i] for i in idx), "ascii")
    used = []
    for ti in tf_indices:
        _, pwm = motifs[ti]
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


# distinct TFs per seq, balanced overall
seqs = []
for s in range(N_SEQ):
    tf_indices = rng.choice(n_tf, size=N_MOTIFS, replace=False)
    seqs.append(gen_sequence(rng, tf_indices))

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} sequences (distinct-TF allocation)")
