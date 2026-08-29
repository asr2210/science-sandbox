import os
import random

IUPAC_MAP = {
    'A': ['A'],
    'C': ['C'],
    'G': ['G'],
    'T': ['T'],
    'R': ['A', 'G'],
    'Y': ['C', 'T'],
    'S': ['G', 'C'],
    'W': ['A', 'T'],
    'K': ['G', 'T'],
    'M': ['A', 'C'],
    'B': ['C', 'G', 'T'],
    'D': ['A', 'G', 'T'],
    'H': ['A', 'C', 'T'],
    'V': ['A', 'C', 'G'],
    'N': ['A', 'C', 'G', 'T']
}

MOTIFS = {
    'CTCF': 'RCCASNAGRKGGCRS',
    'AP1': 'TGANTCA',
    'SP1': 'GGGCGG',
    'CREB': 'TGACGTCA',
    'GATA': 'WGATAR',
    'HNF4A': 'RGGTCANRGGTCA',
    'FOXA': 'TGTTTACY',
    'CEBPA': 'TTGCGCAA',
    'ASCL1': 'CANNTG',
    'SOX': 'CCTTTGWW',
    'NFKB': 'GGGRNYYYCC',
    'p53': 'RRRCWWGYYY',
    'ETS': 'CCGGAA',
    'RFX': 'GTTGCCATGGCAAC',
    'YY1': 'CGCCATNTT',
    'OCT4_SOX2': 'ATGCAAATATTG',
    'TATA': 'TATAAA',
    'Inr': 'YYANWYY',
    'IRF': 'GAAANNGAAA',
    'E2F': 'TTTSSCGC',
    'MEF2': 'YTAWWWWTAR',
    'SRF': 'CCWWWWWWGG',
    'RUNX': 'TGTGGT',
    'KLF4': 'CCACCC'
}

COOPERATING_PAIRS = [
    ('AP1', 'GATA'),
    ('SP1', 'Inr'),
    ('HNF4A', 'FOXA'),
    ('ASCL1', 'SOX'),
    ('OCT4_SOX2', 'KLF4'),
    ('CTCF', 'CTCF'),
    ('ETS', 'CREB'),
    ('p53', 'p53'),
    ('CEBPA', 'AP1'),
    ('NFKB', 'IRF')
]

COOPERATIVE_FACTORS = ['AP1', 'GATA', 'HNF4A', 'ASCL1', 'SP1', 'NFKB', 'p53', 'SOX']

PROMOTER_TRANS = {
    'A': [0.25, 0.25, 0.25, 0.25],
    'C': [0.20, 0.35, 0.25, 0.20],
    'G': [0.20, 0.25, 0.35, 0.20],
    'T': [0.20, 0.25, 0.30, 0.25]
}
PROMOTER_FREQ = [0.20, 0.30, 0.30, 0.20]

ENHANCER_TRANS = {
    'A': [0.35, 0.18, 0.22, 0.25],
    'C': [0.32, 0.25, 0.05, 0.38],
    'G': [0.25, 0.22, 0.25, 0.28],
    'T': [0.25, 0.18, 0.22, 0.35]
}
ENHANCER_FREQ = [0.28, 0.22, 0.22, 0.28]

NEUTRAL_TRANS = {
    'A': [0.40, 0.15, 0.15, 0.30],
    'C': [0.30, 0.20, 0.15, 0.35],
    'G': [0.35, 0.15, 0.20, 0.30],
    'T': [0.30, 0.15, 0.15, 0.40]
}
NEUTRAL_FREQ = [0.32, 0.18, 0.18, 0.32]

def instantiate_motif(motif_str):
    return "".join(random.choice(IUPAC_MAP[c]) for c in motif_str)

def rev_comp(seq):
    rc = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return "".join(rc[b] for b in reversed(seq))

def gen_random_background(length, gc_ratio):
    p_gc = gc_ratio
    p_at = 1.0 - gc_ratio
    p_a = p_at / 2.0
    p_t = p_at / 2.0
    p_c = p_gc / 2.0
    p_g = p_gc / 2.0
    bases = ['A', 'C', 'G', 'T']
    probs = [p_a, p_c, p_g, p_t]
    return "".join(random.choices(bases, weights=probs, k=length))

def gen_markov_background(length, transition_matrix, base_freqs):
    bases = ['A', 'C', 'G', 'T']
    first_base = random.choices(bases, weights=base_freqs, k=1)[0]
    seq = [first_base]
    for _ in range(length - 1):
        prev = seq[-1]
        weights = transition_matrix[prev]
        next_base = random.choices(bases, weights=weights, k=1)[0]
        seq.append(next_base)
    return "".join(seq)

def inject_motif(bg_seq, motif_seq, pos):
    assert len(bg_seq) == 200
    m = len(motif_seq)
    assert 0 <= pos <= 200 - m
    return bg_seq[:pos] + motif_seq + bg_seq[pos+m:]

def place_two_motifs(bg, motif_seq1, motif_seq2, spacing):
    span = len(motif_seq1) + len(motif_seq2) + spacing
    if span > 180:
        spacing = max(0, 180 - len(motif_seq1) - len(motif_seq2))
        span = len(motif_seq1) + len(motif_seq2) + spacing
    start1 = random.randint(10, 200 - span - 10)
    start2 = start1 + len(motif_seq1) + spacing
    seq = bg[:start1] + motif_seq1 + bg[start1+len(motif_seq1):]
    seq = seq[:start2] + motif_seq2 + seq[start2+len(motif_seq2):]
    assert len(seq) == 200
    return seq

def main():
    print("Initializing MPRA library generation...")
    # Set seed for reproducibility
    random.seed(42)
    
    # Sub-Library 1: Random Backgrounds (4,000)
    sub1 = []
    gc_ratios = [0.30, 0.40, 0.50, 0.60, 0.70]
    for gc in gc_ratios:
        for _ in range(800):
            sub1.append(gen_random_background(200, gc))
    print(f"Generated Sub-Library 1 (Random Baselines): {len(sub1)} sequences")
    
    # Sub-Library 2: Markov Backgrounds (4,000)
    sub2 = []
    for _ in range(1500):
        sub2.append(gen_markov_background(200, PROMOTER_TRANS, PROMOTER_FREQ))
    for _ in range(1500):
        sub2.append(gen_markov_background(200, ENHANCER_TRANS, ENHANCER_FREQ))
    for _ in range(1000):
        sub2.append(gen_markov_background(200, NEUTRAL_TRANS, NEUTRAL_FREQ))
    print(f"Generated Sub-Library 2 (Markov Genomic Baselines): {len(sub2)} sequences")
    
    # Sub-Library 3: Single Motif Injections (10,000)
    sub3 = []
    motif_keys = list(MOTIFS.keys())
    for i in range(10000):
        key = motif_keys[i % len(motif_keys)]
        motif_seq = instantiate_motif(MOTIFS[key])
        if random.random() < 0.5:
            motif_seq = rev_comp(motif_seq)
            
        bg_type = random.choice(['gc', 'markov'])
        if bg_type == 'gc':
            gc = random.choice([0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65])
            bg = gen_random_background(200, gc)
        else:
            bg_choice = random.choice([
                (PROMOTER_TRANS, PROMOTER_FREQ),
                (ENHANCER_TRANS, ENHANCER_FREQ),
                (NEUTRAL_TRANS, NEUTRAL_FREQ)
            ])
            bg = gen_markov_background(200, bg_choice[0], bg_choice[1])
            
        pos = random.randint(10, 200 - len(motif_seq) - 10)
        seq = inject_motif(bg, motif_seq, pos)
        sub3.append(seq)
    print(f"Generated Sub-Library 3 (Single Motif Injections): {len(sub3)} sequences")
    
    # Sub-Library 4: Multi-Motif Grammar (18,000)
    sub4 = []
    for i in range(18000):
        if random.random() < 0.5:
            key1, key2 = random.choice(COOPERATING_PAIRS)
        else:
            key1 = random.choice(motif_keys)
            key2 = random.choice(motif_keys)
            
        motif_seq1 = instantiate_motif(MOTIFS[key1])
        motif_seq2 = instantiate_motif(MOTIFS[key2])
        if random.random() < 0.5:
            motif_seq1 = rev_comp(motif_seq1)
        if random.random() < 0.5:
            motif_seq2 = rev_comp(motif_seq2)
            
        spacing = random.choice([2, 5, 10, 15, 20, 30, 40, 50, 80])
        
        bg_type = random.choice(['gc', 'markov'])
        if bg_type == 'gc':
            gc = random.choice([0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65])
            bg = gen_random_background(200, gc)
        else:
            bg_choice = random.choice([
                (PROMOTER_TRANS, PROMOTER_FREQ),
                (ENHANCER_TRANS, ENHANCER_FREQ),
                (NEUTRAL_TRANS, NEUTRAL_FREQ)
            ])
            bg = gen_markov_background(200, bg_choice[0], bg_choice[1])
            
        seq = place_two_motifs(bg, motif_seq1, motif_seq2, spacing)
        sub4.append(seq)
    print(f"Generated Sub-Library 4 (Multi-Motif Grammar): {len(sub4)} sequences")
    
    # Sub-Library 5: Density & Homotypic Clustering (4,000)
    sub5 = []
    for i in range(4000):
        key = COOPERATIVE_FACTORS[i % len(COOPERATIVE_FACTORS)]
        num_copies = random.choice([2, 3, 4])
        
        bg_type = random.choice(['gc', 'markov'])
        if bg_type == 'gc':
            gc = random.choice([0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65])
            bg = gen_random_background(200, gc)
        else:
            bg_choice = random.choice([
                (PROMOTER_TRANS, PROMOTER_FREQ),
                (ENHANCER_TRANS, ENHANCER_FREQ),
                (NEUTRAL_TRANS, NEUTRAL_FREQ)
            ])
            bg = gen_markov_background(200, bg_choice[0], bg_choice[1])
            
        motif_len = len(MOTIFS[key])
        seq = bg
        placed = 0
        current_pos = 10
        for _ in range(num_copies):
            needed_space = (num_copies - placed) * motif_len
            max_spacing = (190 - current_pos - needed_space) // (num_copies - placed)
            if max_spacing < 0:
                break
            spacing = random.randint(0, min(max_spacing, 30))
            pos = current_pos + spacing
            motif_seq = instantiate_motif(MOTIFS[key])
            if random.random() < 0.5:
                motif_seq = rev_comp(motif_seq)
            seq = inject_motif(seq, motif_seq, pos)
            current_pos = pos + motif_len
            placed += 1
            
        sub5.append(seq)
    print(f"Generated Sub-Library 5 (Homotypic Clusters): {len(sub5)} sequences")
    
    # Sub-Library 6: Mutational Landscapes (10,000, 5,000 pairs)
    sub6 = []
    for _ in range(5000):
        bg_type = random.choice(['gc', 'markov'])
        if bg_type == 'gc':
            gc = random.choice([0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65])
            bg = gen_random_background(200, gc)
        else:
            bg_choice = random.choice([
                (PROMOTER_TRANS, PROMOTER_FREQ),
                (ENHANCER_TRANS, ENHANCER_FREQ),
                (NEUTRAL_TRANS, NEUTRAL_FREQ)
            ])
            bg = gen_markov_background(200, bg_choice[0], bg_choice[1])
            
        key = random.choice(motif_keys)
        motif_seq = instantiate_motif(MOTIFS[key])
        m_len = len(motif_seq)
        if random.random() < 0.5:
            motif_seq = rev_comp(motif_seq)
            
        pos = random.randint(15, 200 - m_len - 15)
        ref_seq = bg[:pos] + motif_seq + bg[pos+m_len:]
        assert len(ref_seq) == 200
        
        mut_strategy = random.choice(['knockout', 'point_mutation', 'critical_mutation'])
        if mut_strategy == 'knockout':
            p_gc = ref_seq.count('G') + ref_seq.count('C')
            ref_gc_ratio = p_gc / 200.0
            scrambled_motif = gen_random_background(m_len, ref_gc_ratio)
            mut_seq = ref_seq[:pos] + scrambled_motif + ref_seq[pos+m_len:]
        elif mut_strategy == 'point_mutation':
            mut_idx = random.randint(0, m_len - 1)
            orig_base = motif_seq[mut_idx]
            other_bases = [b for b in ['A', 'C', 'G', 'T'] if b != orig_base]
            new_base = random.choice(other_bases)
            mut_motif_seq = motif_seq[:mut_idx] + new_base + motif_seq[mut_idx+1:]
            mut_seq = ref_seq[:pos] + mut_motif_seq + ref_seq[pos+m_len:]
        else:
            mut_idx = m_len // 2
            orig_base = motif_seq[mut_idx]
            other_bases = [b for b in ['A', 'C', 'G', 'T'] if b != orig_base]
            new_base = random.choice(other_bases)
            mut_motif_seq = motif_seq[:mut_idx] + new_base + motif_seq[mut_idx+1:]
            mut_seq = ref_seq[:pos] + mut_motif_seq + ref_seq[pos+m_len:]
            
        assert len(mut_seq) == 200
        sub6.append(ref_seq)
        sub6.append(mut_seq)
    print(f"Generated Sub-Library 6 (Mutational Landscapes): {len(sub6)} sequences")
    
    # Combine and shuffle to remove batch ordering bias (which could affect SGD learning or evaluation bias)
    all_seqs = sub1 + sub2 + sub3 + sub4 + sub5 + sub6
    assert len(all_seqs) == 50000, f"Expected 50000, got {len(all_seqs)}"
    
    # Let's shuffle all sequences so that different designs are interleaved
    random.shuffle(all_seqs)
    
    # Save to file
    os.makedirs("library", exist_ok=True)
    out_path = "library/sequences.txt"
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s + "\n")
            
    print(f"Successfully wrote {len(all_seqs)} sequences to {out_path}.")
    
    # Self-validation
    print("Running self-validation of generated sequences...")
    with open(out_path, "r") as f:
        lines = f.readlines()
        
    assert len(lines) == 50000, f"Validation Failed: Expected exactly 50000 lines, but found {len(lines)}"
    for idx, l in enumerate(lines):
        seq = l.strip()
        assert len(seq) == 200, f"Validation Failed at line {idx+1}: Length is {len(seq)} (expected 200)"
        for c in seq:
            assert c in ['A', 'C', 'G', 'T'], f"Validation Failed at line {idx+1}: Found invalid character '{c}'"
            
    print("All validation checks passed successfully!")

if __name__ == "__main__":
    main()
