"""Experiment 010: PWM-sampled (fuzzy) motif insertion.

Use real JASPAR PWMs for 20 common human TFs. For each sequence:
  - start from uniform random 200bp
  - sample 3 motifs (with replacement) from the bank
  - for each motif, sample a sequence from its PWM and insert at random pos

PWM sampling produces realistic FUZZY matches (different from hardcoded consensus
in exp 003, which was flat at 0.32). Tests whether real PWM-shaped content
moves the score.
"""
import numpy as np
import os
from pyjaspar import jaspardb

N_SEQ = 50000
LEN = 200
ALPHABET = list("ACGT")
ALPHA_IDX = {b: i for i, b in enumerate(ALPHABET)}

# Pick 20 well-studied TFs (broad / multi-tissue activity).
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
        # take first hit (any version)
        m = ms[0]
        # PWM: position frequency matrix normalized
        counts = np.array([m.counts[b] for b in ALPHABET], dtype=float)  # 4 x L
        probs = counts / counts.sum(axis=0, keepdims=True)
        motifs.append((name, probs))

print(f"Loaded {len(motifs)} PWMs:")
for name, p in motifs:
    print(f"  {name} L={p.shape[1]}")

rng = np.random.default_rng(20260610)


def sample_motif(rng, pwm_probs):
    """Sample one realization of length L from a PWM."""
    L = pwm_probs.shape[1]
    out = []
    for i in range(L):
        b = rng.choice(4, p=pwm_probs[:, i])
        out.append(ALPHABET[b])
    return "".join(out)


COMP = bytes.maketrans(b"ACGT", b"TGCA")


def rc(s):
    return s.translate(COMP)[::-1]


def gen_sequence(rng):
    idx = rng.integers(0, 4, size=LEN)
    seq = bytearray("".join(ALPHABET[i] for i in idx), "ascii")
    used = []
    for _ in range(3):
        name, pwm = motifs[int(rng.integers(0, len(motifs)))]
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

print(f"Wrote {N_SEQ} PWM-sampled sequences to {out_path}")
print(f"  Sample: {seqs[0]}")
