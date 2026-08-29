"""
Experiment 004: 50,000 200bp sequences centered on ENCODE cCREs from chr19+chr22.

Theory:
  Exp 003 (random genomic) gave eval_01 = 0.134. Most random genomic
  windows are non-regulatory and provide weak signal. If active CRE content
  drives MPRA-model informativeness, biasing the library to known CREs
  should improve performance — especially in cell types with high motif
  dependence (K562, where random gave ~0).

Design:
  - Read ENCODE-SCREEN cCRE BED from data/encodeCcreCombined.bb.
  - Use chr19 (~46k cCREs) + chr22 (~17k cCREs) = ~63k cCREs.
  - Sample 50,000 cCREs uniformly.
  - For each cCRE: center 200bp window on the cCRE midpoint.
  - Random orientation (forward / reverse complement) per sample.
  - Skip any window with >5% Ns (replace with random redraw).
  - Seed=42.

Generalization rationale:
  ENCODE cCREs are cell-type-agnostic candidate regulatory elements
  identified by integrating DNase + H3K4me3 + H3K27ac + CTCF data across
  hundreds of cell types. A library centered on cCREs covers real motif
  syntax for many TFs, not just K562/HepG2/SK-N-SH-specific TFs. The
  model should learn a transferable CRE-recognition function.
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

def load_fasta(path, expected_chrom=None):
    parts = []
    chrom = None
    with open(path) as f:
        for line in f:
            if line.startswith(">"):
                chrom = line[1:].strip().split()[0]
            else:
                parts.append(line.strip().upper())
    seq = "".join(parts)
    return chrom, seq

def main():
    rng = random.Random(SEED)
    chr19_name, chr19_seq = load_fasta("data/chr19.fa")
    chr22_name, chr22_seq = load_fasta("data/chr22.fa")
    print(f"{chr19_name}: {len(chr19_seq):,} bp")
    print(f"{chr22_name}: {len(chr22_seq):,} bp")
    chrom_seqs = {chr19_name: chr19_seq, chr22_name: chr22_seq}

    b = bbi.open("data/encodeCcreCombined.bb")
    chrom_size = b.chromsizes
    ccres = []
    for chrom in ("chr19", "chr22"):
        df = b.fetch_intervals(chrom, 0, chrom_size[chrom])
        for _, row in df.iterrows():
            mid = (int(row["start"]) + int(row["end"])) // 2
            ccres.append((chrom, mid))
    print(f"Total cCREs (chr19+chr22): {len(ccres):,}")

    # Sample without replacement
    if len(ccres) >= N_SEQS:
        sampled = rng.sample(ccres, N_SEQS)
    else:
        # sample with replacement if not enough
        sampled = [rng.choice(ccres) for _ in range(N_SEQS)]

    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    written = 0
    skipped = 0
    backup_pool = ccres.copy()
    rng.shuffle(backup_pool)
    backup_idx = 0
    with open(out_path, "w") as f:
        for chrom, mid in sampled:
            tries = 0
            ok = False
            attempts = [(chrom, mid)]
            # if we get an N-rich window, redraw from pool
            while tries < 5 and not ok:
                c, m = attempts[-1]
                seq_full = chrom_seqs[c]
                start = m - SEQ_LEN // 2
                end = start + SEQ_LEN
                if start < 0 or end > len(seq_full):
                    tries += 1
                    while backup_idx < len(backup_pool):
                        candidate = backup_pool[backup_idx]
                        backup_idx += 1
                        if candidate != (c, m):
                            attempts.append(candidate)
                            break
                    continue
                window = seq_full[start:end]
                n_count = sum(1 for b_ in window if b_ not in ALPHABET)
                if n_count > 10:
                    tries += 1
                    while backup_idx < len(backup_pool):
                        candidate = backup_pool[backup_idx]
                        backup_idx += 1
                        if candidate != (c, m):
                            attempts.append(candidate)
                            break
                    continue
                # replace remaining Ns randomly
                if n_count > 0:
                    window = "".join(b_ if b_ in ALPHABET else rng.choice("ACGT")
                                     for b_ in window)
                if rng.random() < 0.5:
                    window = revcomp(window)
                f.write(window + "\n")
                written += 1
                ok = True
            if not ok:
                skipped += 1
    print(f"Wrote {written}, skipped {skipped}")

if __name__ == "__main__":
    main()
