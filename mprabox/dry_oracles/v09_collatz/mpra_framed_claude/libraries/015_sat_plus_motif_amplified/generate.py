"""015_sat_plus_motif_amplified.

50,000 = 5,000 cCREs × 5 natural tiles (25K, saturating cCRE half)
       + 5,000 cCREs × 5 motif-amplified tiles (25K)

The amplified tiles take the same natural cCRE windows but insert
3 JASPAR vertebrate TF motifs at random non-overlapping positions,
sampling motif instances from each motif's PFM.

Tests the "saturation + OOD additive" hypothesis (T10): can a
distinct distribution paired with a saturating natural half lift
the plateau? Amplified tiles preserve genomic backbone (unlike
006 which used random scaffold) so the model isn't asked to
generalize from synthetic-only context.
"""
import numpy as np
import re
from pathlib import Path
from pyfaidx import Fasta

N_REGIONS = 5_000
TILES_PER = 5
N_MOTIFS_PER_AMP = 3
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"
JASPAR = DATA_DIR / "jaspar2024_vertebrates.txt"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


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
            arr = np.array([counts["A"], counts["C"], counts["G"], counts["T"]])
            arr = arr / arr.sum(axis=0, keepdims=True)
            entries.append((name, arr))
            i += 5
        else:
            i += 1
    return entries


motifs = parse_jaspar(JASPAR)
print(f"Parsed {len(motifs)} motifs")
# Filter to motifs of length <= 20 (most JASPAR vertebrate motifs fit)
motifs = [(n, p) for n, p in motifs if p.shape[1] <= 20]
print(f"Motifs <= 20bp: {len(motifs)}")

rng = np.random.default_rng(SEED)


def sample_motif_instance(pwm):
    w = pwm.shape[1]
    chars = []
    for col in range(w):
        b = rng.choice(4, p=pwm[:, col])
        chars.append("ACGT"[b])
    return "".join(chars)


def amplify(seq):
    """Insert N_MOTIFS_PER_AMP JASPAR motif instances into seq at
    random non-overlapping positions. seq must be length LEN."""
    s = list(seq)
    motif_ids = rng.choice(len(motifs), size=N_MOTIFS_PER_AMP, replace=False)
    placed = []
    for mid in motif_ids:
        _, pwm = motifs[mid]
        inst = sample_motif_instance(pwm)
        w = len(inst)
        for _ in range(30):
            pos = int(rng.integers(0, LEN - w + 1))
            iv = (pos, pos + w)
            if any(not (iv[1] <= a or iv[0] >= b) for a, b in placed):
                continue
            for k, ch in enumerate(inst):
                s[pos + k] = ch
            placed.append(iv)
            break
    return "".join(s)


rows = []
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        rows.append((chrom, (int(start) + int(end)) // 2))
print(f"cCRE midpoints on main chroms: {len(rows)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

region_order = rng.permutation(len(rows))

natural_tiles = []  # 25K
amplified_tiles = []  # 25K
n_regions_used = 0
for idx in region_order:
    if n_regions_used >= N_REGIONS:
        break
    chrom, mid = rows[idx]
    offsets_nat = rng.integers(-OFFSET_MAX, OFFSET_MAX + 1, size=TILES_PER)
    offsets_amp = rng.integers(-OFFSET_MAX, OFFSET_MAX + 1, size=TILES_PER)
    nat_seqs = []
    for off in offsets_nat:
        center = mid + int(off)
        s = center - HALF
        e = s + LEN
        if s < 0 or e > chrom_lens[chrom]:
            continue
        seq = fasta[chrom][s:e]
        if "N" in seq or len(seq) != LEN:
            continue
        nat_seqs.append(seq)
    amp_seqs = []
    for off in offsets_amp:
        center = mid + int(off)
        s = center - HALF
        e = s + LEN
        if s < 0 or e > chrom_lens[chrom]:
            continue
        seq = fasta[chrom][s:e]
        if "N" in seq or len(seq) != LEN:
            continue
        amp_seqs.append(seq)
    if len(nat_seqs) < TILES_PER or len(amp_seqs) < TILES_PER:
        continue
    natural_tiles.extend(nat_seqs)
    amplified_tiles.extend(amplify(s) for s in amp_seqs)
    n_regions_used += 1

print(f"Natural tiles {len(natural_tiles)}; amplified tiles {len(amplified_tiles)}")
assert len(natural_tiles) == 25_000 and len(amplified_tiles) == 25_000

combined = natural_tiles + amplified_tiles
rng.shuffle(combined)
out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for s in combined:
        f.write(s)
        f.write("\n")
print(f"Wrote {len(combined)}")
assert len(combined) == 50_000
