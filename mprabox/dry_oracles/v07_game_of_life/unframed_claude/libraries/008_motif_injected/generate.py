"""Random uniform scaffolds with 5 randomly-chosen TF motifs inserted per sequence.

Tests whether injecting strong, well-defined transcription factor motifs into
otherwise-random 50% GC backgrounds boosts the score. Uses a curated subset
of cell-line-relevant motifs from JASPAR 2024 (K562, HepG2, SK-N-SH TFs).
"""
import os
import re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

N = 50000
L = 200
SEED = 42
N_INSERTS = 5

# Selected motifs (a mix targeting K562, HepG2, SK-N-SH plus universal CTCF/AP1)
TARGET_TFS = {
    'CTCF', 'GATA1', 'GATA2', 'GATA3', 'KLF1', 'TAL1', 'NFE2', 'RUNX1',
    'HNF4A', 'HNF1A', 'FOXA1', 'FOXA2', 'CEBPA', 'HNF4G',
    'ASCL1', 'NEUROD1', 'POU3F2', 'REST',
    'JUN', 'FOS', 'SP1', 'MYC', 'MAX', 'YY1', 'NFKB1', 'TBP', 'ELK1', 'E2F1',
}

def parse_jaspar(path):
    """Return list of (tf_name, consensus_seq) for matching TFs."""
    motifs = {}
    with open(path) as f:
        name = None
        rows = {}
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('>'):
                if name is not None and len(rows) == 4:
                    consensus = build_consensus(rows)
                    if consensus is not None:
                        motifs.setdefault(name, []).append(consensus)
                _, name_part = line[1:].split('\t', 1)
                name = name_part.strip().split('::')[0]  # take first TF of dimer
                rows = {}
            else:
                m = re.match(r'^([ACGT])\s*\[(.*)\]', line)
                if m:
                    base = m.group(1)
                    nums = [int(x) for x in m.group(2).split()]
                    rows[base] = nums
        if name is not None and len(rows) == 4:
            consensus = build_consensus(rows)
            if consensus is not None:
                motifs.setdefault(name, []).append(consensus)
    return motifs


def build_consensus(rows):
    """Argmax consensus from PFM rows dict {A,C,G,T: counts}."""
    bases = ['A', 'C', 'G', 'T']
    L = len(rows['A'])
    out = []
    for i in range(L):
        col = [(rows[b][i], b) for b in bases]
        col.sort(reverse=True)
        out.append(col[0][1])
    return ''.join(out)


print("Parsing JASPAR motifs...")
all_motifs = parse_jaspar(os.path.join(ROOT, 'data', 'jaspar2024_core_vert_pfms.txt'))
selected = []
for tf in TARGET_TFS:
    if tf in all_motifs:
        for cons in all_motifs[tf]:
            selected.append((tf, cons))
print(f"Found {len(selected)} consensus sequences for {len(set(tf for tf, _ in selected))} TFs")
for tf, cons in selected[:8]:
    print(f"  {tf}: {cons}")

motif_seqs = [cons for _, cons in selected]
motif_lens = [len(m) for m in motif_seqs]
print(f"Motif lengths: min={min(motif_lens)} max={max(motif_lens)} mean={np.mean(motif_lens):.1f}")

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])


def generate_one():
    # Choose 5 motifs and place them non-overlapping in a 200bp seq.
    motif_idx = rng.choice(len(motif_seqs), size=N_INSERTS, replace=False)
    selected_motifs = [motif_seqs[i] for i in motif_idx]
    total_motif_len = sum(len(m) for m in selected_motifs)
    spacer_budget = L - total_motif_len
    if spacer_budget < 0:
        # Skip if too long; recurse
        return generate_one()
    # Random non-negative spacer lengths that sum to spacer_budget across N+1 slots
    # Use random multinomial
    slots = N_INSERTS + 1
    # Use Dirichlet-like sampling: draw N_INSERTS cut points from [0, spacer_budget]
    cuts = sorted(rng.integers(0, spacer_budget + 1, size=slots - 1).tolist())
    cuts = [0] + cuts + [spacer_budget]
    spacers = [cuts[i+1] - cuts[i] for i in range(slots)]
    # Random base for spacers, uniform
    out = []
    for i, m in enumerate(selected_motifs):
        if spacers[i] > 0:
            sp = bases[rng.integers(0, 4, size=spacers[i])].tolist()
            out.extend(sp)
        out.extend(list(m))
    if spacers[-1] > 0:
        sp = bases[rng.integers(0, 4, size=spacers[-1])].tolist()
        out.extend(sp)
    assert len(out) == L, (len(out), L)
    return ''.join(out)


print(f"Generating {N} sequences with {N_INSERTS} motif insertions each...")
seqs = []
for i in range(N):
    seqs.append(generate_one())
    if (i + 1) % 10000 == 0:
        print(f"  {i+1}/{N}")

import statistics
gcs = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
print(f"GC (first 2k): min={min(gcs):.3f} mean={statistics.mean(gcs):.3f} max={max(gcs):.3f}")

out_path = os.path.join(HERE, 'sequences_0.txt')
with open(out_path, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out_path}")
