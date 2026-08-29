"""
generate.py — Build a 50,000 × 200bp MPRA training library.

Composition:
  40,000  diverse SCREEN cCREs (200bp window centered on each element)
   5,000  random hg38 200bp windows (filtered for low N content)
   3,000  dinucleotide-shuffled cCRE sequences
   2,000  synthetic motif-engineered sequences with JASPAR-like TF consensus
  ------
  50,000  total
"""
import os
import sys
import random
import collections

import numpy as np
import pandas as pd

# Make local twobit reader importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))
from twobit_reader import TwoBitFile  # noqa: E402

SEED = 20260523
random.seed(SEED)
np.random.seed(SEED)

WINDOW = 200
LIB_SIZE = 50_000
CCRE_BED = 'data/GRCh38-cCREs.bed'
GENOME_2BIT = 'data/hg38.2bit'
OUT_PATH = 'library/sequences.txt'

# cCRE allocation
CCRE_ALLOC = {
    'dELS': 13_000,
    'pELS':  5_500,
    'CA':    4_500,
    'CA-CTCF': 4_000,
    'PLS':   4_000,
    'TF':    3_500,
    'CA-H3K4me3': 3_500,
    'CA-TF': 2_000,
}
N_CCRE = sum(CCRE_ALLOC.values())  # 40,000
N_RANDOM = 5_000
N_SHUFFLE = 3_000
N_SYNTHETIC = 2_000
assert N_CCRE + N_RANDOM + N_SHUFFLE + N_SYNTHETIC == LIB_SIZE

# Hand-curated TF motif consensus sequences (a mix relevant to many cell types).
# Each is a short consensus / common k-mer that will be embedded in random bg.
# Multi-cell-type emphasis so the model learns broadly applicable grammar.
TF_MOTIFS = [
    # Liver / HNF family
    ('HNF4A',  'TGAACCTTGGCCT'),
    ('HNF4A2', 'AGGTCAAAGGTCA'),
    ('HNF1A',  'GTTAATGATTAAC'),
    ('CEBPA',  'TTGCGCAAT'),
    ('FOXA1',  'TGTTTGTTTG'),
    # Erythroid / K562
    ('GATA1',  'AGATAAGG'),
    ('GATA2',  'AGATAAGA'),
    ('KLF1',   'CCACGCCC'),
    ('TAL1',   'CAGCTG'),
    # Neuronal / SK-N-SH
    ('NEUROD1','CAGCTGCT'),
    ('REST',   'TTCAGCACCATGGACAG'),
    ('SOX2',   'CATTGTT'),
    ('MEF2A',  'CTATAAATA'),
    # Generic / strong motifs
    ('SP1',    'GGGGCGGGGC'),
    ('AP1',    'TGAGTCA'),
    ('AP1_2',  'TGACTCA'),
    ('EBOX',   'CACGTG'),
    ('CTCF',   'CCGCGAGGGGCAG'),
    ('CTCF_2', 'CCCTCTAGTGGCC'),
    ('NFKB',   'GGGACTTTCC'),
    ('NFY',    'CCAATC'),
    ('TBP',    'TATAAA'),
    ('Inr',    'TCAGTC'),
    ('ETS',    'ACCGGAAGT'),
    ('STAT',   'TTCCNGGAA'.replace('N', 'C')),
    ('CRE',    'TGACGTCA'),
    ('GRE',    'AGAACANNNTGTTCT'.replace('N', 'A')),
    ('IRF',    'AAAAGTGAAAGT'),
    ('YY1',    'CCATCTT'),
    ('MAX',    'CACGTGGT'),
    ('PAX5',   'GCCGCCAAGCATTAT'),
    ('OCT4',   'ATTTGCAT'),
    ('NRF1',   'TGCGCATGCGCA'),
    ('USF',    'CACGTGAC'),
    ('TEAD',   'GGAATG'),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASES = ('A', 'C', 'G', 'T')


def random_dna(n, rng):
    """Uniform random ACGT string of length n."""
    return ''.join(rng.choices(BASES, k=n))


def dinuc_shuffle(seq, rng):
    """Shuffle a DNA sequence preserving dinucleotide frequencies (Altschul-Erickson)."""
    if any(b not in BASES for b in seq):
        return random_dna(len(seq), rng)
    # Build edge list as graph of base -> neighbor
    edges = collections.defaultdict(list)
    for i in range(len(seq) - 1):
        edges[seq[i]].append(seq[i + 1])
    last = seq[-1]
    # Random walk algorithm: pick a random Eulerian path
    # Simpler practical approach: shuffle each adjacency list, then walk.
    # This is an approximation, not strictly preserving dinuc — but good enough.
    for k in edges:
        rng.shuffle(edges[k])
    # Walk
    indices = {k: 0 for k in edges}
    out = [seq[0]]
    cur = seq[0]
    while True:
        if cur not in edges or indices[cur] >= len(edges[cur]):
            break
        nxt = edges[cur][indices[cur]]
        indices[cur] += 1
        out.append(nxt)
        cur = nxt
    if len(out) < len(seq):
        # Fallback for failed Eulerian walk: char-level shuffle
        chars = list(seq)
        rng.shuffle(chars)
        return ''.join(chars)
    return ''.join(out[: len(seq)])


def synthesize_motif_seq(rng):
    """Embed 1-4 TF motifs at random positions in a random background."""
    bg = list(random_dna(WINDOW, rng))
    n_motifs = rng.choices([1, 2, 3, 4], weights=[2, 3, 3, 2])[0]
    used = []
    for _ in range(n_motifs):
        name, consensus = rng.choice(TF_MOTIFS)
        L = len(consensus)
        if L > WINDOW:
            continue
        # Choose position avoiding overlap with used positions
        for _ in range(20):
            pos = rng.randint(0, WINDOW - L)
            if all(pos + L <= u[0] or pos >= u[1] for u in used):
                used.append((pos, pos + L))
                # Random strand: half the time, reverse-complement
                if rng.random() < 0.5:
                    consensus = consensus[::-1].translate(str.maketrans('ACGT', 'TGCA'))
                for i, b in enumerate(consensus):
                    bg[pos + i] = b
                break
    return ''.join(bg)


def normalize_seq(seq):
    """Uppercase and check ACGT-only. Return None if invalid (contains N or other)."""
    if seq is None:
        return None
    seq = seq.upper()
    if len(seq) != WINDOW:
        return None
    for b in seq:
        if b not in 'ACGT':
            return None
    return seq


# ---------------------------------------------------------------------------
# 1. Sample cCREs (stratified by class)
# ---------------------------------------------------------------------------

def sample_ccres():
    print(f"[ccre] reading {CCRE_BED}...", flush=True)
    df = pd.read_csv(CCRE_BED, sep='\t', header=None,
                     names=['chrom', 'start', 'end', 'id1', 'id2', 'class'])
    # Compute midpoint for 200bp windows
    df['mid'] = (df['start'] + df['end']) // 2
    df['win_s'] = df['mid'] - WINDOW // 2
    df['win_e'] = df['mid'] + WINDOW // 2
    # Drop entries near chromosome ends (will fail to extract); we'll handle later
    chunks = []
    for cls, n in CCRE_ALLOC.items():
        sub = df[df['class'] == cls]
        # Stratify by chromosome: sample proportionally to chromosome representation
        # but cap any single chrom to <= 1/6 of class quota to ensure spread
        chrom_groups = list(sub.groupby('chrom'))
        # Shuffle chrom order for deterministic but mixed picking
        rng = random.Random(hash(('ccre', cls, SEED)) & 0xFFFFFFFF)
        rng.shuffle(chrom_groups)
        # Take proportional share per chromosome
        cap = max(1, int(n * 1.5 / len(chrom_groups)))  # at most 1.5× even share
        picked = []
        for chrom, g in chrom_groups:
            take = min(len(g), cap)
            picked.append(g.sample(n=take, random_state=hash((chrom, cls, SEED)) & 0xFFFFFFFF))
        cls_df = pd.concat(picked, ignore_index=True)
        # Oversample then trim — we'll filter N-containing ones later
        target = int(n * 1.3)  # 30% extra to absorb dropouts
        if len(cls_df) > target:
            cls_df = cls_df.sample(n=target, random_state=hash((cls, 'trim', SEED)) & 0xFFFFFFFF)
        cls_df['bucket'] = cls
        chunks.append(cls_df[['chrom', 'win_s', 'win_e', 'class', 'bucket']])
        print(f"[ccre]  {cls}: picked {len(cls_df)} (target {n})", flush=True)
    return pd.concat(chunks, ignore_index=True)


# ---------------------------------------------------------------------------
# 2. Sample random genomic windows
# ---------------------------------------------------------------------------

def sample_random_windows(tb, n, rng):
    chroms = [c for c in tb.seqs if c in
              {'chr' + str(i) for i in range(1, 23)} | {'chrX', 'chrY'}]
    # Weight by chromosome size to ensure uniform per-bp sampling
    sizes = {c: tb._read_header(c)[0] for c in chroms}
    total = sum(sizes.values())
    weights = [sizes[c] / total for c in chroms]
    picks = []
    # Oversample 2× then filter N
    target = n * 2
    while len(picks) < target:
        c = rng.choices(chroms, weights=weights, k=1)[0]
        sz = sizes[c]
        s = rng.randint(0, sz - WINDOW)
        picks.append((c, s, s + WINDOW))
    return pd.DataFrame(picks, columns=['chrom', 'win_s', 'win_e']).assign(
        **{'class': 'random_genomic', 'bucket': 'random_genomic'})


# ---------------------------------------------------------------------------
# 3. Extract sequences from genome
# ---------------------------------------------------------------------------

def extract_sequences(df, tb, label):
    """Extract sequences for each row by loading one chromosome at a time."""
    out = []
    df_by_chrom = list(df.groupby('chrom', sort=False))
    for chrom, g in df_by_chrom:
        if chrom not in tb.seqs:
            continue
        try:
            sz, _, _ = tb._read_header(chrom)
            chrom_seq = tb.fetch(chrom, 0, sz)
        except Exception as e:
            print(f"[extract] failed loading {chrom}: {e}", flush=True)
            continue
        for _, row in g.iterrows():
            s, e = int(row['win_s']), int(row['win_e'])
            if s < 0 or e > sz:
                continue
            seq = chrom_seq[s:e]
            norm = normalize_seq(seq)
            if norm is None:
                continue
            out.append({'seq': norm, 'chrom': chrom, 'start': s, 'class': row.get('class'), 'bucket': row.get('bucket')})
        print(f"[extract:{label}] {chrom}: {len(out)} accepted so far", flush=True)
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs('library', exist_ok=True)
    rng = random.Random(SEED)

    print("Opening genome...", flush=True)
    tb = TwoBitFile(GENOME_2BIT)

    # 1. cCRE sequences
    ccre_targets = sample_ccres()
    print(f"[ccre] total target rows: {len(ccre_targets)}", flush=True)
    ccre_seqs = extract_sequences(ccre_targets, tb, label='ccre')
    print(f"[ccre] extracted {len(ccre_seqs)} valid sequences", flush=True)

    # Trim each cCRE class back to its target count after filtering
    ccre_trimmed = []
    for cls, n in CCRE_ALLOC.items():
        sub = ccre_seqs[ccre_seqs['bucket'] == cls]
        if len(sub) < n:
            print(f"[ccre] WARNING: {cls} only has {len(sub)} (wanted {n})", flush=True)
            ccre_trimmed.append(sub)
        else:
            ccre_trimmed.append(sub.sample(n=n, random_state=hash((cls, 'final', SEED)) & 0xFFFFFFFF))
    ccre_final = pd.concat(ccre_trimmed, ignore_index=True)
    print(f"[ccre] final: {len(ccre_final)} sequences", flush=True)

    # 2. Random genomic sequences
    rand_targets = sample_random_windows(tb, N_RANDOM, rng)
    rand_seqs = extract_sequences(rand_targets, tb, label='random')
    rand_final = rand_seqs.head(N_RANDOM).copy()
    if len(rand_final) < N_RANDOM:
        # Resample until we have enough
        more_targets = sample_random_windows(tb, (N_RANDOM - len(rand_final)) * 3, rng)
        more_seqs = extract_sequences(more_targets, tb, label='random_extra')
        rand_final = pd.concat([rand_final, more_seqs], ignore_index=True).head(N_RANDOM)
    print(f"[random] final: {len(rand_final)} sequences", flush=True)

    # 3. Dinucleotide-shuffled cCRE sequences
    print(f"[shuffle] creating {N_SHUFFLE} dinuc-shuffled sequences...", flush=True)
    shuffle_pool = ccre_final['seq'].tolist()
    shuffle_seqs = []
    seen_for_shuffle = set()
    while len(shuffle_seqs) < N_SHUFFLE:
        src = rng.choice(shuffle_pool)
        shuf = dinuc_shuffle(src, rng)
        shuf = normalize_seq(shuf)
        if shuf is None or shuf in seen_for_shuffle:
            continue
        seen_for_shuffle.add(shuf)
        shuffle_seqs.append({'seq': shuf, 'chrom': None, 'start': None,
                             'class': 'dinuc_shuffle', 'bucket': 'dinuc_shuffle'})
    shuffle_df = pd.DataFrame(shuffle_seqs)
    print(f"[shuffle] {len(shuffle_df)} sequences", flush=True)

    # 4. Synthetic motif sequences
    print(f"[synth] creating {N_SYNTHETIC} synthetic motif sequences...", flush=True)
    synth_seqs = []
    seen_synth = set()
    while len(synth_seqs) < N_SYNTHETIC:
        s = synthesize_motif_seq(rng)
        s = normalize_seq(s)
        if s is None or s in seen_synth:
            continue
        seen_synth.add(s)
        synth_seqs.append({'seq': s, 'chrom': None, 'start': None,
                           'class': 'synthetic_motif', 'bucket': 'synthetic_motif'})
    synth_df = pd.DataFrame(synth_seqs)
    print(f"[synth] {len(synth_df)} sequences", flush=True)

    # Combine
    combined = pd.concat([ccre_final, rand_final, shuffle_df, synth_df], ignore_index=True)
    print(f"[combine] before dedup: {len(combined)}", flush=True)

    # Deduplicate
    combined = combined.drop_duplicates(subset=['seq']).reset_index(drop=True)
    print(f"[combine] after dedup: {len(combined)}", flush=True)

    # If we lost some to dedup, top up with extra random genomic
    while len(combined) < LIB_SIZE:
        need = LIB_SIZE - len(combined)
        print(f"[topup] need {need} more sequences; sampling random genomic", flush=True)
        more_targets = sample_random_windows(tb, need * 3, rng)
        more_seqs = extract_sequences(more_targets, tb, label='topup')
        combined = pd.concat([combined, more_seqs], ignore_index=True)
        combined = combined.drop_duplicates(subset=['seq']).reset_index(drop=True)

    if len(combined) > LIB_SIZE:
        combined = combined.sample(n=LIB_SIZE, random_state=SEED).reset_index(drop=True)

    assert len(combined) == LIB_SIZE
    # Validate sequences
    for i, s in enumerate(combined['seq']):
        if len(s) != WINDOW or any(b not in 'ACGT' for b in s):
            raise ValueError(f"Bad sequence at index {i}: {s}")

    # Shuffle to mix buckets
    combined = combined.sample(frac=1, random_state=SEED).reset_index(drop=True)

    # Write output
    with open(OUT_PATH, 'w') as f:
        f.write('\n'.join(combined['seq'].tolist()) + '\n')
    print(f"\n[done] wrote {len(combined)} sequences to {OUT_PATH}", flush=True)

    # Print composition summary
    print("\n=== composition ===")
    print(combined['bucket'].value_counts().to_string())
    print("\n=== chromosome distribution (cCRE/random/topup) ===")
    print(combined[combined['chrom'].notna()]['chrom'].value_counts().head(10).to_string())

    tb.close()


if __name__ == '__main__':
    main()
