"""006_synth_jaspar_motifs.

Synthetic library: 50,000 200bp random scaffolds with 2-5 JASPAR
vertebrate TF motifs planted at random non-overlapping positions.

Tests whether motif content alone (no genomic context) gives the
model enough signal to predict activity. If yes, motif identity is
the dominant determinant of MPRA activity and natural genomic context
is redundant. If no, context matters.

Each planted motif is a probabilistic sample from the motif's PFM
(not just the consensus), so motif diversity is preserved.
"""
import numpy as np
from pathlib import Path
import re

N_SEQS = 50_000
LEN = 200
MIN_MOTIFS = 2
MAX_MOTIFS = 5
SEED = 0
GC_RANGE = (0.40, 0.55)

DATA = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
JASPAR = DATA / "jaspar2024_vertebrates.txt"

# Parse JASPAR jaspar-format file into list of (name, pwm)
# Each entry: ">MA0004.1\tArnt" then 4 lines A,C,G,T  [ counts... ]
def parse_jaspar(path):
    entries = []
    with open(path) as f:
        lines = [ln.rstrip() for ln in f if ln.strip()]
    i = 0
    while i < len(lines):
        if lines[i].startswith(">"):
            name = lines[i][1:].strip()
            counts = {}
            for j in range(4):
                ln = lines[i + 1 + j]
                m = re.match(r"\s*([ACGT])\s*\[(.+)\]\s*$", ln)
                if not m:
                    raise ValueError(f"Bad line: {ln!r}")
                base = m.group(1)
                vals = [float(x) for x in m.group(2).split()]
                counts[base] = vals
            # convert to PWM (rows in ACGT order)
            arr = np.array([counts["A"], counts["C"], counts["G"], counts["T"]])
            arr = arr / arr.sum(axis=0, keepdims=True)
            entries.append((name, arr))
            i += 5
        else:
            i += 1
    return entries

motifs = parse_jaspar(JASPAR)
print(f"Parsed {len(motifs)} motifs from JASPAR")

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

def sample_motif_instance(pwm):
    # pwm is shape (4, w); columns sum to 1
    w = pwm.shape[1]
    chars = []
    for col in range(w):
        b = rng.choice(4, p=pwm[:, col])
        chars.append("ACGT"[b])
    return "".join(chars)

def random_scaffold(length):
    # GC sampled uniformly within GC_RANGE
    gc = rng.uniform(*GC_RANGE)
    probs = [0.5 * (1 - gc), 0.5 * gc, 0.5 * gc, 0.5 * (1 - gc)]  # A,C,G,T
    idx = rng.choice(4, size=length, p=probs)
    return "".join(bases[idx])

out_path = Path(__file__).parent / "sequences_0.txt"
n_written = 0
with open(out_path, "w") as f:
    while n_written < N_SEQS:
        seq = list(random_scaffold(LEN))
        n_motifs = int(rng.integers(MIN_MOTIFS, MAX_MOTIFS + 1))
        # choose motif identities (without replacement within sequence)
        motif_ids = rng.choice(len(motifs), size=n_motifs, replace=False)
        # place each motif at a random non-overlapping position
        placed_intervals = []
        for mid in motif_ids:
            _, pwm = motifs[mid]
            inst = sample_motif_instance(pwm)
            w = len(inst)
            if w > LEN:
                continue
            # try up to 30 positions to find non-overlapping
            ok = False
            for _ in range(30):
                pos = int(rng.integers(0, LEN - w + 1))
                interval = (pos, pos + w)
                # check non-overlap with placed
                overlap = any(not (interval[1] <= a or interval[0] >= b) for a, b in placed_intervals)
                if not overlap:
                    for k, ch in enumerate(inst):
                        seq[pos + k] = ch
                    placed_intervals.append(interval)
                    ok = True
                    break
            # if not placed, just skip (rare)
        line = "".join(seq)
        if len(line) != LEN or any(c not in "ACGT" for c in line):
            continue
        f.write(line)
        f.write("\n")
        n_written += 1
        if n_written % 10000 == 0:
            print(f"  wrote {n_written}")
print(f"Wrote {n_written} synthetic motif sequences")
