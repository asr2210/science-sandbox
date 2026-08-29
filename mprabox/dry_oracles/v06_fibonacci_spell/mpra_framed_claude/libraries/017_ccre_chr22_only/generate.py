"""
Experiment 017: chr22-only cCRE-centered 200bp windows.

Theory:
  004 (chr19+chr22 cCRE-centered) gave eval_01 = 0.1256, worse than
  003 (chr22 random) = 0.1341. But 015 established that chr19 inclusion
  is BAD for this eval. So 004's loss may be entirely chr19's fault.

  This experiment isolates the FUNCTIONAL ENRICHMENT effect by using
  chr22-only cCREs (~17k available; resample with replacement to 50k).

  Hypothesis: chr22-only cCRE-centered should beat chr22 random (003)
  if functional enrichment helps. If not, the model learns from
  COMPOSITION not from functional content, and we should stop trying
  function-based selection.

Design:
  - chr22 cCREs only (~17k positions; resample with replacement to 50k)
  - 200bp window centered on cCRE midpoint
  - Random orientation
  - Replace any Ns with random ACGT
  - Seed=42
"""

import os
import random
import bbi

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42

ALPHABET = set("ACGT")
COMPL = str.maketrans("ACGTNacgtn", "TGCANtgcan")
def revcomp(s): return s.translate(COMPL)[::-1]

def load_fasta(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip().upper())
    return "".join(parts)

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    L = len(chr22)

    b = bbi.open("data/encodeCcreCombined.bb")
    chrom_size = b.chromsizes
    df = b.fetch_intervals("chr22", 0, chrom_size["chr22"])
    ccres = []
    for _, row in df.iterrows():
        mid = (int(row["start"]) + int(row["end"])) // 2
        start = mid - SEQ_LEN // 2
        end = start + SEQ_LEN
        if 0 <= start and end <= L:
            ccres.append(mid)
    print(f"chr22 valid cCREs: {len(ccres):,}")

    # Sample with replacement to 50k (since only ~17k cCREs)
    sampled = [rng.choice(ccres) for _ in range(N_SEQS)]

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for mid in sampled:
            start = mid - SEQ_LEN // 2
            window = chr22[start:start + SEQ_LEN]
            # Replace Ns with random
            if any(c not in ALPHABET for c in window):
                window = "".join(c if c in ALPHABET else rng.choice("ACGT")
                                 for c in window)
            if rng.random() < 0.5:
                window = revcomp(window)
            f.write(window + "\n")
    n_written = sum(1 for _ in open(out))
    print(f"Total written: {n_written}")
    # GC stats
    gcs = []
    for line in open(out):
        s = line.strip()
        gcs.append((s.count("G") + s.count("C")) / SEQ_LEN)
    print(f"Mean GC = {sum(gcs)/len(gcs):.3f}, min={min(gcs):.3f}, max={max(gcs):.3f}")

if __name__ == "__main__":
    main()
