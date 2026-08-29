"""Experiment 027: 3rd reseed of exp 010 (bound noise floor).

010 seed 20260610 → 0.3644
024 seed 424242   → 0.3106
027 seed 99       → ?
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
print(f"Loaded {len(motifs)} PWMs")

rng = np.random.default_rng(99)
COMP = bytes.maketrans(b"ACGT", b"TGCA")


def rc(s):
    return s.translate(COMP)[::-1]


def sample_motif(rng, pwm):
    L = pwm.shape[1]
    return "".join(ALPHABET[rng.choice(4, p=pwm[:, i])] for i in range(L))


def gen_sequence(rng):
    idx = rng.integers(0, 4, size=LEN)
    seq = bytearray("".join(ALPHABET[i] for i in idx), "ascii")
    used = []
    for _ in range(N_MOTIFS):
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
print(f"Wrote {N_SEQ} sequences (seed 99)")
