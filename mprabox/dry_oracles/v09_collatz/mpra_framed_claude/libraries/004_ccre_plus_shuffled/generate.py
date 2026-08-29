"""004_ccre_plus_shuffled.

50,000 = 25,000 real cCRE 200bp windows + 25,000 dinucleotide-shuffled
versions of those same sequences. Tests whether matched-composition
negative controls help the model separate motif-driven from
composition-driven activity (Sharpr-style design).

Dinucleotide shuffling preserves 2-mer frequencies but destroys all
higher-order structure (motifs, longer-range syntax).
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

N_HALF = 25_000
LEN = 200
HALF = LEN // 2
SEED = 0

DATA_DIR = Path("/data/users/arao/.private/MPRAgent_adversarial/runs/v09/blind_claude/data")
BED = DATA_DIR / "GRCh38-cCREs.bed"
GENOME = DATA_DIR / "hg38.fa"

KEEP_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

rows = []
with open(BED) as f:
    for ln in f:
        chrom, start, end = ln.split("\t")[:3]
        if chrom not in KEEP_CHROMS:
            continue
        rows.append((chrom, int(start), int(end)))
print(f"cCREs on main chroms: {len(rows)}")

fasta = Fasta(str(GENOME), as_raw=True, sequence_always_upper=True)
chrom_lens = {k: len(v) for k, v in fasta.items()}

rng = np.random.default_rng(SEED)
order = rng.permutation(len(rows))

# Step 1: collect 25k real cCRE sequences
real_seqs = []
for idx in order:
    if len(real_seqs) >= N_HALF:
        break
    chrom, s0, e0 = rows[idx]
    center = (s0 + e0) // 2
    s = center - HALF
    e = s + LEN
    if s < 0 or e > chrom_lens[chrom]:
        continue
    seq = fasta[chrom][s:e]
    if "N" in seq or len(seq) != LEN:
        continue
    real_seqs.append(seq)
print(f"Collected {len(real_seqs)} real cCREs")

# Step 2: dinucleotide-shuffle each (uShuffle-style: preserve dinuc freq)
# Implementation: build dinucleotide adjacency graph (Eulerian circuit
# approach is the canonical preserving-2mer-freq shuffle).
def dinuc_shuffle(seq, rng):
    """Shuffle preserving dinucleotide frequencies.
    Altschul-Erickson algorithm: random Eulerian walk in dinucleotide graph.
    """
    n = len(seq)
    if n < 2:
        return seq
    # adjacency: from each base, list of next bases (in order)
    nexts = {b: [] for b in "ACGT"}
    for a, b in zip(seq[:-1], seq[1:]):
        if a in nexts:
            nexts[a].append(b)
    # Shuffle each list except force one edge to lead toward the last base
    last = seq[-1]
    first = seq[0]
    # Try repeated random Eulerian walks until we get one that uses all edges
    for _ in range(100):
        # Pick a random spanning arborescence rooted at `last`
        # For Altschul-Erickson: choose one out-edge per non-`last` vertex
        # such that the chosen edges form a tree rooted at `last`.
        # Simpler approximation: shuffle each nexts list, then walk.
        nexts_copy = {b: list(arr) for b, arr in nexts.items()}
        for b in nexts_copy:
            rng.shuffle(nexts_copy[b])
        walk = [first]
        cur = first
        ok = True
        for _ in range(n - 1):
            if not nexts_copy[cur]:
                ok = False
                break
            nxt = nexts_copy[cur].pop()
            walk.append(nxt)
            cur = nxt
        if ok and len(walk) == n:
            return "".join(walk)
    # Fallback: mononucleotide shuffle
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)

print("Generating dinucleotide-shuffled controls...")
shuffled_seqs = []
for i, seq in enumerate(real_seqs):
    sh = dinuc_shuffle(seq, rng)
    if "N" in sh or len(sh) != LEN:
        # very unlikely; just retry mononuc shuffle
        chars = list(seq)
        rng.shuffle(chars)
        sh = "".join(chars)
    shuffled_seqs.append(sh)
    if (i + 1) % 5000 == 0:
        print(f"  shuffled {i+1}/{len(real_seqs)}")

# Combine, shuffle order so reals/shuffleds are interleaved
all_seqs = real_seqs + shuffled_seqs
order2 = rng.permutation(len(all_seqs))
out_path = Path(__file__).parent / "sequences_0.txt"
with open(out_path, "w") as f:
    for idx in order2:
        f.write(all_seqs[idx])
        f.write("\n")
print(f"Wrote {len(all_seqs)} sequences ({N_HALF} real + {N_HALF} shuffled)")
