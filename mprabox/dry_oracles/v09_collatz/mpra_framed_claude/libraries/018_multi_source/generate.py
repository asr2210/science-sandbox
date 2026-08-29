"""018_multi_source.

50K = 1,000 regions x 10 tiles from each of 5 orthogonal sources:
  1. cCREs (broad ENCODE V3)
  2. K562 DNase peaks
  3. HepG2 DNase peaks
  4. SK-N-SH DNase peaks
  5. cCREs that overlap phastCons conserved elements

At saturating total region count (5K), each source contributes
equally. Tests whether SOURCE DIVERSITY (orthogonal evidence
streams converging) lifts the plateau when count and density are
held fixed.

Generalization: multi-evidence regulatory regions are the
convergence of orthogonal annotations — most defensible and most
likely universal across cell types.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
from collections import defaultdict
from bisect import bisect_left

PER_SOURCE = 1_000
TILES_PER = 10
LEN = 200
HALF = LEN // 2
OFFSET_MAX = 100
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
GENOME = DATA_DIR / "hg38.fa"
KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_bed_midpoints(path, has_header):
    out = []
    with open(path) as f:
        for ln in f:
            if has_header and ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) < 3:
                continue
            chrom = parts[0]
            if chrom not in KEEP_CHROMS:
                continue
            try:
                mid = (int(parts[1]) + int(parts[2])) // 2
            except ValueError:
                continue
            out.append((chrom, mid))
    return out


print("Loading sources...")
ccres = load_bed_midpoints(DATA_DIR / "GRCh38-cCREs.bed", has_header=False)
k562_dhs = load_bed_midpoints(DATA_DIR / "k562_dnase.bed", has_header=True)
hepg2_dhs = load_bed_midpoints(DATA_DIR / "hepg2_dnase.bed", has_header=True)
sknsh_dhs = load_bed_midpoints(DATA_DIR / "sknsh_dnase.bed", has_header=False)
print(f"cCREs {len(ccres)}, K562 {len(k562_dhs)}, HepG2 {len(hepg2_dhs)}, SKNSH {len(sknsh_dhs)}")

# Build cCRE-conserved subset
print("Loading phastCons...")
phast = defaultdict(list)
with open(DATA_DIR / "phastConsElements100way.txt") as f:
    for ln in f:
        parts = ln.rstrip().split("\t")
        chrom = parts[1]
        if chrom not in KEEP_CHROMS:
            continue
        phast[chrom].append((int(parts[2]), int(parts[3])))
for c in phast:
    phast[c].sort()
phast_starts = {c: [s for s, _ in v] for c, v in phast.items()}


def conserved_bases(chrom, qs, qe):
    if chrom not in phast:
        return 0
    starts = phast_starts[chrom]
    arr = phast[chrom]
    lo = bisect_left(starts, qs - 4000)
    total = 0
    i = lo
    while i < len(arr) and arr[i][0] < qe:
        s, e = arr[i]
        a = max(s, qs)
        b = min(e, qe)
        if b > a:
            total += b - a
        i += 1
    return total


# Top conservation cCREs (top 5K by conservation density)
print("Scoring cCREs by conservation...")
scored_cons = []
for chrom, mid in ccres:
    qs = mid - HALF
    qe = mid + HALF
    scored_cons.append((conserved_bases(chrom, qs, qe), chrom, mid))
scored_cons.sort(reverse=True)
conserved_ccres = [(c, m) for _, c, m in scored_cons[:5000]]
print(f"Conserved cCRE pool: {len(conserved_ccres)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)


def tile_region(chrom, mid):
    """Return TILES_PER tiles or None if can't make all clean."""
    offsets = rng.integers(-OFFSET_MAX, OFFSET_MAX + 1, size=TILES_PER)
    tiles = []
    for off in offsets:
        center = mid + int(off)
        s = center - HALF
        e = s + LEN
        if s < 0 or e > chrom_lens[chrom]:
            return None
        seq = fasta[chrom][s:e]
        if "N" in seq or len(seq) != LEN:
            return None
        tiles.append(seq)
    return tiles


def sample_from(source, n):
    """Sample n regions and produce n*TILES_PER clean tiles."""
    idx = rng.permutation(len(source))
    selected = []
    out_tiles = []
    for i in idx:
        if len(selected) >= n:
            break
        c, m = source[i]
        tiles = tile_region(c, m)
        if tiles is None:
            continue
        selected.append((c, m))
        out_tiles.extend(tiles)
    return out_tiles


all_tiles = []
for src_name, src in [
    ("cCRE", ccres),
    ("K562 DHS", k562_dhs),
    ("HepG2 DHS", hepg2_dhs),
    ("SKNSH DHS", sknsh_dhs),
    ("conserved cCRE", conserved_ccres),
]:
    tiles = sample_from(src, PER_SOURCE)
    print(f"  {src_name}: {len(tiles)} tiles")
    all_tiles.extend(tiles)

assert len(all_tiles) == 50_000, f"Got {len(all_tiles)}"
rng.shuffle(all_tiles)

out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for s in all_tiles:
        f.write(s)
        f.write("\n")
print(f"Wrote {len(all_tiles)}")
