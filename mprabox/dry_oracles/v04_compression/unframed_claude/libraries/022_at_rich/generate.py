"""Experiment 022: same as 010 but AT-rich scaffold (GC=20%).

exp 002 showed GC60 random was terrible (0.12). Was that the GC bias or
correlated effect? Try opposite: GC=20% scaffold + 17 TFs 3/seq PWM-sampled.
"""
import numpy as np
import os
from pyjaspar import jaspardb

N_SEQ = 50000
LEN = 200
ALPHABET = list("ACGT")
N_MOTIFS = 3
P_GC = 0.20  # P(C)=P(G)=0.10, P(A)=P(T)=0.40

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

rng = np.random.default_rng(20260622)
COMP = bytes.maketrans(b"ACGT", b"TGCA")
NUC_P = np.array([(1 - P_GC) / 2, P_GC / 2, P_GC / 2, (1 - P_GC) / 2])  # A,C,G,T


def rc(s):
    return s.translate(COMP)[::-1]


def sample_motif(rng, pwm):
    L = pwm.shape[1]
    return "".join(ALPHABET[rng.choice(4, p=pwm[:, i])] for i in range(L))


def gen_sequence(rng):
    idx = rng.choice(4, size=LEN, p=NUC_P)
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
print(f"Wrote {N_SEQ} AT-rich sequences (GC={P_GC})")
