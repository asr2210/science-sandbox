"""Generate a 50,000-sequence, 200bp MPRA training library.

Composition (rationale in notebook.md):
  28,000  ENCODE cCREs (stratified across PLS / pELS / dELS / CTCF / DNase-H3K4me3)
   7,000  Random genomic windows (broad background)
   5,000  Motif-implanted synthetic (32 TF motifs in varied backgrounds)
   4,000  Dinucleotide-shuffled controls of cCRE windows
   3,000  Pure random sequences with varied GC content
   3,000  Tiled neighbors of cCREs (shifted by +/-100 to capture context)
  ------
  50,000  total

Output: library/sequences.txt with one 200bp sequence per line.
"""

import json
import os
import random
import sys
from pathlib import Path

random.seed(20260526)  # reproducible

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
HG38_RAW = DATA / 'hg38_raw'
CCRE_BED = DATA / 'GRCh38-cCREs.bed'
OUT_PATH = ROOT / 'library' / 'sequences.txt'
META_PATH = ROOT / 'library' / 'metadata.tsv'

SEQ_LEN = 200
TARGET_TOTAL = 50_000

BASES = 'ACGT'

# ---------------------------------------------------------------- helpers

def load_chrom(name):
    return (HG38_RAW / f'{name}.bin').read_bytes()


def clean_or_fix(seq, max_n=4):
    """Return ACGT-only uppercase string, or None if too many ambiguous bases."""
    if isinstance(seq, bytes):
        s = seq.decode('ascii').upper()
    else:
        s = seq.upper()
    n_ambig = sum(1 for c in s if c not in 'ACGT')
    if n_ambig > max_n:
        return None
    if n_ambig == 0:
        return s
    return ''.join(c if c in 'ACGT' else random.choice(BASES) for c in s)


def random_seq(length, gc=None, rng=None):
    if rng is None:
        rng = random
    if gc is None:
        return ''.join(rng.choices(BASES, k=length))
    p_gc = gc / 2.0
    p_at = (1 - gc) / 2.0
    return ''.join(rng.choices(BASES, weights=[p_at, p_gc, p_gc, p_at], k=length))


def altschul_erickson(seq, rng=None):
    """Dinucleotide-preserving shuffle (Eulerian walk on dinucleotide graph).

    Falls back to single-nucleotide shuffle if no valid Eulerian walk found.
    """
    if rng is None:
        rng = random
    if len(seq) < 3:
        return seq
    edges = {b: [] for b in BASES}
    valid = all(c in BASES for c in seq)
    if not valid:
        return None
    for i in range(len(seq) - 1):
        edges[seq[i]].append(seq[i + 1])
    for _ in range(12):
        elists = {b: list(es) for b, es in edges.items()}
        for b in elists:
            rng.shuffle(elists[b])
        out = [seq[0]]
        cur = seq[0]
        ok = True
        for _ in range(len(seq) - 1):
            if not elists[cur]:
                ok = False
                break
            nxt = elists[cur].pop()
            out.append(nxt)
            cur = nxt
        if ok and len(out) == len(seq):
            return ''.join(out)
    # Fallback: simple shuffle
    chars = list(seq)
    rng.shuffle(chars)
    return ''.join(chars)


# ---------------------------------------------------------------- motifs

IUPAC = {
    'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T',
    'R': 'AG', 'Y': 'CT', 'S': 'GC', 'W': 'AT', 'K': 'GT', 'M': 'AC',
    'B': 'CGT', 'D': 'AGT', 'H': 'ACT', 'V': 'ACG', 'N': 'ACGT',
}

# Curated set of well-characterized TF binding consensus motifs spanning
# diverse TF families (zinc finger, bHLH, bZIP, HMG, homeo, forkhead, ETS,
# T-box, IRF, STAT, REL, NR, MADS-box, ...).
MOTIFS = [
    ('CTCF',       'CCGCGNGGNGGCAG'),
    ('CTCF_core',  'CCCTC'),
    ('Ebox_Myc',   'CACGTG'),
    ('Ebox_Snai',  'CAGGTG'),
    ('TATA',       'TATAAA'),
    ('Sp1',        'GGGGCGGGGC'),
    ('NFY',        'CCAATCA'),
    ('AP1',        'TGASTCA'),
    ('NFkB',       'GGGAATTTCC'),
    ('p53',        'RRRCWTGYYY'),
    ('GATA',       'AGATAAG'),
    ('HNF1',       'GTTAATNATTAAC'),
    ('FOXA',       'TGTTTAC'),
    ('ETS',        'CCGGAAGT'),
    ('ELK1',       'ACCGGAAGT'),
    ('HOMEO',      'TAATCC'),
    ('CEBP',       'ATTGCGCAAT'),
    ('IRF',        'GAAANNGAAA'),
    ('STAT',       'TTCCNGGAA'),
    ('TEAD',       'GGAATG'),
    ('RUNX',       'TGTGGT'),
    ('SOX',        'AACAAT'),
    ('OCT',        'ATGCAAAT'),
    ('MEF2',       'CTATAAATAG'),
    ('E2F',        'TTTSSCGC'),
    ('SMAD',       'GTCTAGAC'),
    ('HSF',        'TTCTAGAA'),
    ('KLF',        'CACCC'),
    ('TCF_LEF',    'CTTTGTT'),
    ('NR_DR1',     'AGGTCANAGGTCA'),
    ('REST',       'TCAGCACCNNGGACAG'),
    ('ZNF143',     'ACTGCATNNTGCAGT'),
    ('YY1',        'CGCCATNTT'),
    ('MAF',        'TGCTGACTCAGCA'),
]


def resolve_iupac(code, rng=None):
    if rng is None:
        rng = random
    return ''.join(rng.choice(IUPAC[c]) for c in code)


def implant(background, motif_instance, position):
    L = len(background)
    m = len(motif_instance)
    if position + m > L:
        position = L - m
    return background[:position] + motif_instance + background[position + m:]


# ---------------------------------------------------------------- genome / cCRE

def load_genome():
    print('Loading hg38 chromosomes ...', flush=True)
    chroms = [f'chr{i}' for i in range(1, 23)] + ['chrX']
    g = {}
    for c in chroms:
        g[c] = load_chrom(c)
    total_gb = sum(len(v) for v in g.values()) / 1e9
    print(f'  Loaded {len(g)} chromosomes, {total_gb:.2f} Gb')
    return g


def load_ccres():
    print('Loading cCREs ...', flush=True)
    keep = set([f'chr{i}' for i in range(1, 23)] + ['chrX'])
    rows = []
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if len(parts) < 6:
                continue
            if parts[0] not in keep:
                continue
            rows.append((parts[0], int(parts[1]), int(parts[2]), parts[5]))
    print(f'  {len(rows)} cCREs across major chromosomes')
    return rows


def primary_class(ctype):
    return ctype.split(',')[0]


# ---------------------------------------------------------------- samplers

def window_around(genome, chrom, center, jitter=0):
    if jitter:
        center += random.randint(-jitter, jitter)
    half = SEQ_LEN // 2
    start = center - half
    end = start + SEQ_LEN
    L = len(genome[chrom])
    if start < 0 or end > L:
        return None
    return clean_or_fix(genome[chrom][start:end], max_n=10)


def sample_ccre_windows(genome, ccres, target_per_class, jitter=20):
    print(f'Sampling cCRE-centered windows (target {sum(target_per_class.values())}) ...',
          flush=True)
    by_class = {}
    for r in ccres:
        by_class.setdefault(primary_class(r[3]), []).append(r)
    print('  cCREs per class:')
    for cls, lst in sorted(by_class.items()):
        print(f'    {cls:>20s}: {len(lst):,}')
    out = []
    seen = set()
    for cls, n_target in target_per_class.items():
        pool = list(by_class.get(cls, []))
        random.shuffle(pool)
        kept = 0
        for chrom, start, end, _ in pool:
            if kept >= n_target:
                break
            center = (start + end) // 2
            seq = window_around(genome, chrom, center, jitter=jitter)
            if seq is None or seq in seen:
                continue
            seen.add(seq)
            out.append((f'ccre_{cls}', seq))
            kept += 1
        print(f'    kept {kept}/{n_target} for {cls}')
    return out, seen


def sample_random_genomic(genome, n, seen, label='random_genomic'):
    print(f'Sampling {n} random genomic windows ...', flush=True)
    chroms = list(genome.keys())
    weights = [len(genome[c]) for c in chroms]
    out = []
    attempts = 0
    while len(out) < n and attempts < n * 10:
        attempts += 1
        c = random.choices(chroms, weights=weights, k=1)[0]
        L = len(genome[c])
        start = random.randint(0, L - SEQ_LEN)
        seq = clean_or_fix(genome[c][start:start + SEQ_LEN], max_n=10)
        if seq is None or seq in seen:
            continue
        seen.add(seq)
        out.append((label, seq))
    return out


def sample_ccre_neighbors(genome, ccres, n, seen,
                          shifts=(-300, -200, -150, -100, 100, 150, 200, 300)):
    print(f'Sampling {n} cCRE-neighbor (shifted) windows ...', flush=True)
    out = []
    pool = list(ccres)
    random.shuffle(pool)
    idx = 0
    attempts = 0
    while len(out) < n and attempts < n * 10 and idx < len(pool):
        attempts += 1
        chrom, start, end, _ = pool[idx]
        idx += 1
        center = (start + end) // 2 + random.choice(shifts)
        seq = window_around(genome, chrom, center, jitter=10)
        if seq is None or seq in seen:
            continue
        seen.add(seq)
        out.append(('ccre_neighbor', seq))
    return out


def sample_shuffled_ccres(genome, ccres, n, seen):
    print(f'Sampling {n} dinucleotide-shuffled cCRE windows ...', flush=True)
    out = []
    pool = list(ccres)
    random.shuffle(pool)
    idx = 0
    attempts = 0
    while len(out) < n and attempts < n * 6 and idx < len(pool):
        attempts += 1
        chrom, start, end, _ = pool[idx]
        idx += 1
        center = (start + end) // 2
        src = window_around(genome, chrom, center, jitter=10)
        if src is None:
            continue
        sh = altschul_erickson(src, random)
        if not sh or len(sh) != SEQ_LEN or sh in seen:
            continue
        seen.add(sh)
        out.append(('shuffled_ccre', sh))
    return out


def sample_random_gc(n, seen):
    print(f'Sampling {n} random sequences with varied GC ...', flush=True)
    out = []
    # GC fractions to cover (a broad range — hg38 GC mean ~0.41)
    gc_targets = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
    per_gc = n // len(gc_targets) + 1
    for gc in gc_targets:
        for _ in range(per_gc):
            if len(out) >= n:
                break
            seq = random_seq(SEQ_LEN, gc=gc)
            if seq in seen:
                continue
            seen.add(seq)
            out.append((f'random_gc{int(gc*100)}', seq))
    return out[:n]


def make_background(genome, mode, rng):
    """Background generator for motif-implant sequences."""
    if mode == 'shuffled_genomic':
        # Random genomic window, then shuffle (preserve dinuc) to detach motifs
        chroms = list(genome.keys())
        weights = [len(genome[c]) for c in chroms]
        for _ in range(5):
            c = rng.choices(chroms, weights=weights, k=1)[0]
            L = len(genome[c])
            start = rng.randint(0, L - SEQ_LEN)
            src = clean_or_fix(genome[c][start:start + SEQ_LEN], max_n=5)
            if src is None:
                continue
            sh = altschul_erickson(src, rng)
            if sh and len(sh) == SEQ_LEN:
                return sh
        return random_seq(SEQ_LEN, gc=0.45, rng=rng)
    if mode == 'random_gc':
        gc = rng.choice([0.35, 0.40, 0.45, 0.50, 0.55])
        return random_seq(SEQ_LEN, gc=gc, rng=rng)
    if mode == 'genomic':
        chroms = list(genome.keys())
        weights = [len(genome[c]) for c in chroms]
        for _ in range(5):
            c = rng.choices(chroms, weights=weights, k=1)[0]
            L = len(genome[c])
            start = rng.randint(0, L - SEQ_LEN)
            src = clean_or_fix(genome[c][start:start + SEQ_LEN], max_n=5)
            if src:
                return src
        return random_seq(SEQ_LEN, gc=0.45, rng=rng)
    return random_seq(SEQ_LEN, gc=0.45, rng=rng)


def sample_motif_implanted(genome, n, seen):
    print(f'Sampling {n} motif-implanted synthetic windows ...', flush=True)
    out = []
    bg_modes = ['shuffled_genomic', 'random_gc', 'genomic']
    attempts = 0
    while len(out) < n and attempts < n * 6:
        attempts += 1
        bg_mode = random.choice(bg_modes)
        bg = make_background(genome, bg_mode, random)
        n_copies = random.choices([1, 1, 2, 2, 3], k=1)[0]
        motif_name, motif_code = random.choice(MOTIFS)
        # Use 1-3 distinct motifs occasionally
        if n_copies > 1 and random.random() < 0.3:
            extra = random.sample(MOTIFS, k=min(n_copies, len(MOTIFS)))
            motifs_to_use = [(motif_name, motif_code)] + [(n, c) for n, c in extra
                                                          if n != motif_name][:n_copies - 1]
            motifs_to_use = motifs_to_use[:n_copies]
        else:
            motifs_to_use = [(motif_name, motif_code)] * n_copies

        seq = bg
        positions = []
        for mname, mcode in motifs_to_use:
            instance = resolve_iupac(mcode, random)
            # Maybe reverse-complement (TFs bind both strands)
            if random.random() < 0.5:
                tab = str.maketrans('ACGT', 'TGCA')
                instance = instance.translate(tab)[::-1]
            mlen = len(instance)
            if mlen >= SEQ_LEN - 4:
                continue
            # Choose a non-overlapping position if possible
            for _ in range(10):
                pos = random.randint(0, SEQ_LEN - mlen)
                if all(abs(pos - p) > mlen + 2 for p in positions):
                    positions.append(pos)
                    seq = seq[:pos] + instance + seq[pos + mlen:]
                    break
        if len(seq) != SEQ_LEN:
            continue
        if any(c not in BASES for c in seq):
            continue
        if seq in seen:
            continue
        seen.add(seq)
        label_motifs = '+'.join(m[0] for m in motifs_to_use)
        out.append((f'motif_{label_motifs}__bg_{bg_mode}', seq))
    return out


# ---------------------------------------------------------------- main

def main():
    out_dir = OUT_PATH.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    genome = load_genome()
    ccres = load_ccres()

    # ----- Stratified cCREs: 28,000 total
    # Approximate weighting that favors enhancer-like (most numerous and most
    # diverse) but ensures all classes well-represented.
    ccre_targets = {
        'PLS':            4000,
        'pELS':           5500,
        'dELS':          12000,
        'CTCF-only':      3000,
        'DNase-H3K4me3':  2500,
        # Also pull a small extra batch by including category as-is
    }
    # If totals less than 28000, top up dELS
    needed = 28000 - sum(ccre_targets.values())
    if needed > 0:
        ccre_targets['dELS'] += needed

    ccre_seqs, seen = sample_ccre_windows(genome, ccres, ccre_targets, jitter=25)

    # ----- Random genomic background: 7,000
    random_seqs = sample_random_genomic(genome, 7000, seen)

    # ----- cCRE neighbors (shifted windows): 3,000
    neighbor_seqs = sample_ccre_neighbors(genome, ccres, 3000, seen)

    # ----- Shuffled cCRE controls: 4,000
    shuffled_seqs = sample_shuffled_ccres(genome, ccres, 4000, seen)

    # ----- Motif implanted synthetic: 5,000
    motif_seqs = sample_motif_implanted(genome, 5000, seen)

    # ----- Random GC-varied: 3,000
    random_gc_seqs = sample_random_gc(3000, seen)

    buckets = [
        ('ccre_stratified', ccre_seqs),
        ('random_genomic',  random_seqs),
        ('ccre_neighbor',   neighbor_seqs),
        ('shuffled_ccre',   shuffled_seqs),
        ('motif_implanted', motif_seqs),
        ('random_gc',       random_gc_seqs),
    ]

    print('\nBucket sizes:')
    total = 0
    for name, lst in buckets:
        print(f'  {name:>20s}: {len(lst):>6,}')
        total += len(lst)
    print(f'  {"TOTAL":>20s}: {total:>6,}')

    if total != TARGET_TOTAL:
        # Pad or trim to exactly TARGET_TOTAL
        all_seqs = [s for _, lst in buckets for s in lst]
        if len(all_seqs) > TARGET_TOTAL:
            random.shuffle(all_seqs)
            all_seqs = all_seqs[:TARGET_TOTAL]
        else:
            short = TARGET_TOTAL - len(all_seqs)
            print(f'Short by {short}; padding with extra random genomic windows', flush=True)
            extra = sample_random_genomic(genome, short, seen, label='random_genomic_fill')
            all_seqs = all_seqs + extra
        # rebuild buckets summary
    else:
        all_seqs = [s for _, lst in buckets for s in lst]

    random.shuffle(all_seqs)
    assert len(all_seqs) == TARGET_TOTAL, f'Got {len(all_seqs)} expected {TARGET_TOTAL}'

    # Final validation
    for label, seq in all_seqs:
        if len(seq) != SEQ_LEN:
            raise RuntimeError(f'bad length {len(seq)} for {label}')
        if any(c not in BASES for c in seq):
            raise RuntimeError(f'non-ACGT in {label}: {seq[:50]}...')

    print(f'\nWriting {len(all_seqs)} sequences to {OUT_PATH} ...', flush=True)
    with open(OUT_PATH, 'w') as f:
        for _, seq in all_seqs:
            f.write(seq + '\n')

    with open(META_PATH, 'w') as f:
        f.write('idx\tlabel\n')
        for i, (label, _) in enumerate(all_seqs):
            f.write(f'{i}\t{label}\n')

    print('Done.')


if __name__ == '__main__':
    main()
