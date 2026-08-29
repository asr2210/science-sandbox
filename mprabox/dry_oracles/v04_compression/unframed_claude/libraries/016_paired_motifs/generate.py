"""Experiment 016: 17 TFs, 3 motifs/seq, with 2 of 3 placed as a PAIR.

Composite elements (paired TFBSs with short spacing) often drive synergistic
activity in MPRAs. Place 2 motifs within 0-8bp of each other; the 3rd is
random-position standalone.
"""
import numpy as np
import os
from pyjaspar import jaspardb

N_SEQ = 50000
LEN = 200
ALPHABET = list("ACGT")

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

rng = np.random.default_rng(20260616)
COMP = bytes.maketrans(b"ACGT", b"TGCA")


def rc(s):
    return s.translate(COMP)[::-1]


def sample_motif(rng, pwm):
    L = pwm.shape[1]
    return "".join(ALPHABET[rng.choice(4, p=pwm[:, i])] for i in range(L))


def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def insert_at(seq, m, pos):
    seq[pos:pos + len(m)] = m


def gen_sequence(rng):
    idx = rng.integers(0, 4, size=LEN)
    seq = bytearray("".join(ALPHABET[i] for i in idx), "ascii")
    # PAIR: two motifs placed close together (spacer 0-8bp)
    _, pwm_a = motifs[int(rng.integers(0, len(motifs)))]
    _, pwm_b = motifs[int(rng.integers(0, len(motifs)))]
    ma = sample_motif(rng, pwm_a).encode()
    mb = sample_motif(rng, pwm_b).encode()
    if rng.random() < 0.5:
        ma = rc(ma)
    if rng.random() < 0.5:
        mb = rc(mb)
    spacer = int(rng.integers(0, 9))
    pair_len = len(ma) + spacer + len(mb)
    pair_pos = int(rng.integers(0, LEN - pair_len + 1))
    insert_at(seq, ma, pair_pos)
    insert_at(seq, mb, pair_pos + len(ma) + spacer)
    used = [(pair_pos, pair_pos + pair_len)]
    # STANDALONE third motif
    _, pwm_c = motifs[int(rng.integers(0, len(motifs)))]
    mc = sample_motif(rng, pwm_c).encode()
    if rng.random() < 0.5:
        mc = rc(mc)
    for _try in range(20):
        pos = int(rng.integers(0, LEN - len(mc) + 1))
        if all(not overlaps((pos, pos + len(mc)), u) for u in used):
            insert_at(seq, mc, pos)
            break
    return seq.decode("ascii")


seqs = [gen_sequence(rng) for _ in range(N_SEQ)]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} paired-motif sequences")
