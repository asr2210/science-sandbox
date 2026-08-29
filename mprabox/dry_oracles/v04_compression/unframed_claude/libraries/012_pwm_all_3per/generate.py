"""Experiment 012: ALL 720 JASPAR human CORE PWMs, 3 motifs per seq.

Same density as exp 010 (the winner so far) but maximally diverse TF bank
(720 vs 17). Tests whether TF diversity helps further.
"""
import numpy as np
import os
from pyjaspar import jaspardb

N_SEQ = 50000
LEN = 200
ALPHABET = list("ACGT")
N_MOTIFS = 3

j = jaspardb(release="JASPAR2024")
all_motifs = j.fetch_motifs(species="9606", collection="CORE")
motifs = []
for m in all_motifs:
    counts = np.array([m.counts[b] for b in ALPHABET], dtype=float)
    if counts.sum() == 0:
        continue
    probs = counts / counts.sum(axis=0, keepdims=True)
    # cap PWM length at 20 to fit reasonably; skip very long ones
    if probs.shape[1] > 25:
        continue
    motifs.append((m.matrix_id, probs))

print(f"Loaded {len(motifs)} PWMs from JASPAR (humans, length <=25).")

rng = np.random.default_rng(20260612)
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

print(f"Wrote {N_SEQ} PWM-sampled sequences (3/seq, {len(motifs)} TFs) to {out_path}")
