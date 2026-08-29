import os
import random
import sys

# Fixed random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Define a comprehensive set of human transcription factor (TF) consensus motifs using IUPAC codes
MOTIFS = {
    'AP-1': 'TGASTCA',
    'CREB': 'TGACGTCA',
    'NF-kB': 'GGGRNYYYCC',
    'GATA': 'WGATAR',
    'ETS': 'CCGGAA',
    'CTCF': 'CCACAGGGGGAGGC',
    'Oct': 'ATGCAAAT',
    'Sox': 'AACAAT',
    'Fox': 'TGTTTAC',
    'E-box': 'CACGTG',
    'MyoD': 'CAGCTG',
    'IRF': 'GAAASYGAAASY',
    'Sp1': 'CCGCCC',
    'HNF4A': 'RGGDCA',
    'p53': 'RRRCWWGYYY',
    'Stat': 'TTCCNGGAA',
    'YY1': 'CCGCCATNTT',
    'E2F': 'TTTCCCGC',
    'Runx': 'TGTGGTW',
    'NFAT': 'AGGAAA',
    'SMAD': 'AGAC',
    'MEF2': 'CTAWWWATAG',
    'Nrf2': 'TGANTNNNCTA',
    'TCF_LEF': 'CTTTGWW',
    'SRF': 'CCWWWWWWGG',
    'Tead': 'CATTCCA',
    'CEBP': 'ATTGCGCAAT',
    'HNF1A': 'GTTAATNATTAAC',
    'EGR1': 'GCGGGGGCG',
    'Klf4': 'GGGTGGTG',
    'NRF1': 'TGCGCATGCG',
    'RFX5': 'GTTRCCATGGYAAC',
    'AP-2': 'GCCNNNGGC',
    'ARE': 'AGAACANNNTGTTCT',
    'ERE': 'AGGTCANNNTGACCT',
    'GRE': 'AGAACANNNTGTTCT',
    'NFY': 'CCAAT',
    'Pbx1': 'TGATTDAT',
    'Pax5': 'GGCAGCCA',
    'Pit1': 'TATNCAT',
    'Prrx2': 'TAATYA',
    'Rfx1': 'GTTGCCATGGCAAC',
    'Rxra': 'AGGTCA',
    'Sox9': 'CATTGTT',
    'Sox17': 'AACAAT',
    'Sp1_2': 'GGGGYGGG',
    'SREBP': 'ATCACCCCAC',
    'Srf_2': 'CCATATATGG',
    'Taf1': 'TCAGTT',
    'TBP': 'TATAAA',
    'Tcf7l2': 'CTTTGAT',
    'Tead4': 'GGAATG',
    'Usf2': 'CACGTG',
    'Xbp1': 'TGACGT',
    'Zic1': 'CCCTCNNNCCCT',
    'Znf143': 'GCCCAT',
    'AhR': 'TGCGTG',
    'Arnt': 'CACGTG',
    'Atf1': 'TGACGTCA',
    'Atf3': 'TGACGTCA',
    'Bcl6': 'TTCCTAGAA',
    'Cbfb': 'TGTGGT',
    'Cebpb': 'TTGCGCAA',
    'Clock': 'CACGTG',
    'E2f4': 'TTTSSCGC',
    'Egr2': 'GCGGGGGCG',
    'Elk1': 'ACTTCCTG',
    'Elk4': 'ACTTCCTG',
    'Foxa2': 'TGTTTAC',
    'Foxm1': 'TAAACA',
    'Gata2': 'AGATAA',
    'Gata3': 'AGATAA',
    'Gata4': 'AGATAA',
    'Hif1a': 'RCGTG',
    'Hnf4b': 'TGACCT',
    'Irf4': 'GAAANYGAAANY',
    'Jun': 'TGASTCA',
    'Jund': 'TGASTCA',
    'Klf5': 'GGGYGKGGC',
    'Mef2c': 'YTAWWWATAR',
    'Nfe2': 'TGANTCA',
    'Nfe2l2': 'TGANTNNNCTA',
    'Nfia': 'TTGGCNNNNNGCCAA',
    'Nfya': 'CCAAT',
    'Pax6': 'TCACGC',
    'Pou2f1': 'ATGCAAAT',
    'Rela': 'GGGRNYYYCC',
    'Rfx2': 'GTTRCCATGGYAAC',
    'Runx2': 'TGTGGT',
    'Sox2_Oct4': 'ATGCAAATNNCATTGTT',
    'TATA': 'TATAWAW',
    'Inr': 'YYANWYY',
    'DPE': 'RGWYV'
}

IUPAC_MAP = {
    'A': ['A'], 'C': ['C'], 'G': ['G'], 'T': ['T'],
    'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'],
    'K': ['G', 'T'], 'M': ['A', 'C'], 'B': ['C', 'G', 'T'],
    'D': ['A', 'G', 'T'], 'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'],
    'N': ['A', 'C', 'G', 'T']
}

def resolve_iupac(iupac_seq, rng=random):
    """Converts an IUPAC degenerate sequence into a random concrete nucleotide sequence."""
    return "".join(rng.choice(IUPAC_MAP[c.upper()]) for c in iupac_seq)

def reverse_complement(seq):
    """Returns the reverse complement of a nucleotide sequence."""
    rc_map = str.maketrans('ACGTacgt', 'TGCAtgca')
    return seq.translate(rc_map)[::-1]

def generate_background(length, gc_content, rng=random):
    """Generates a random DNA sequence of exact length and approximate GC content."""
    num_gc = int(round(length * gc_content))
    num_at = length - num_gc
    elements = ['G', 'C'] * (num_gc // 2 + 1) + ['A', 'T'] * (num_at // 2 + 1)
    elements = elements[:length]
    rng.shuffle(elements)
    return "".join(elements)

def insert_motif(background, motif_seq, pos):
    """Inserts a motif into a background sequence at the given 0-indexed position."""
    return background[:pos] + motif_seq + background[pos + len(motif_seq):]

# ---------------------------------------------------------
# Tier Generators
# ---------------------------------------------------------

def generate_tier1_single_motif_scans(count, rng):
    """
    Tier 1: Single Motif Scans
    Goal: Learn motif identity, position bias, and orientation.
    """
    sequences = []
    # Select 60 highly diverse motifs from the dictionary (exclude core promoters)
    excluded_keys = {'TATA', 'Inr', 'DPE'}
    motif_keys = [k for k in MOTIFS.keys() if k not in excluded_keys]
    rng.shuffle(motif_keys)
    selected_keys = motif_keys[:60]
    
    positions = [20, 55, 90, 125, 160]
    orientations = ['forward', 'reverse']
    gc_contents = [0.40, 0.55]
    
    # 60 motifs * 5 positions * 2 orientations * 2 GCs = 1,200 combinations.
    # To get `count` sequences, we generate multiple different backgrounds per combination.
    combos = []
    for m in selected_keys:
        for p in positions:
            for o in orientations:
                for gc in gc_contents:
                    combos.append((m, p, o, gc))
                    
    # Generate sequences
    multiplier = count // len(combos)
    remainder = count % len(combos)
    
    for m, p, o, gc in combos:
        num_to_gen = multiplier
        if remainder > 0:
            num_to_gen += 1
            remainder -= 1
            
        for _ in range(num_to_gen):
            motif_seq = resolve_iupac(MOTIFS[m], rng)
            if o == 'reverse':
                motif_seq = reverse_complement(motif_seq)
            
            bg = generate_background(200, gc, rng)
            # Ensure the motif fits
            if p + len(motif_seq) <= 200:
                seq = insert_motif(bg, motif_seq, p)
                sequences.append(seq)
            else:
                # Fallback to position 100 if it doesn't fit
                seq = insert_motif(bg, motif_seq, 100)
                sequences.append(seq)
                
    return sequences

def generate_tier2_homotypic_clusters(count, rng):
    """
    Tier 2: Homotypic Clusters
    Goal: Learn motif density, dosage, and cooperativity.
    """
    sequences = []
    excluded_keys = {'TATA', 'Inr', 'DPE'}
    motif_keys = [k for k in MOTIFS.keys() if k not in excluded_keys]
    rng.shuffle(motif_keys)
    selected_keys = motif_keys[:40]
    
    copies_opts = [2, 3, 4]
    spacing_opts = [5, 15, 30]
    gc_contents = [0.45, 0.55]
    
    combos = []
    for m in selected_keys:
        for k in copies_opts:
            for spacing in spacing_opts:
                for gc in gc_contents:
                    combos.append((m, k, spacing, gc))
                    
    # 40 motifs * 3 densities * 3 spacings * 2 GCs = 720 combinations.
    multiplier = count // len(combos)
    remainder = count % len(combos)
    
    for m, k, spacing, gc in combos:
        num_to_gen = multiplier
        if remainder > 0:
            num_to_gen += 1
            remainder -= 1
            
        for _ in range(num_to_gen):
            motif_raw = MOTIFS[m]
            motif_instances = [resolve_iupac(motif_raw, rng) for _ in range(k)]
            
            # Randomly orient each instance
            for i in range(k):
                if rng.random() < 0.5:
                    motif_instances[i] = reverse_complement(motif_instances[i])
                    
            # Create the homotypic cluster
            cluster_seq = ""
            for i in range(k):
                cluster_seq += motif_instances[i]
                if i < k - 1:
                    cluster_seq += generate_background(spacing, gc, rng)
                    
            span = len(cluster_seq)
            if span > 180:
                # If too long, truncate copies or spacer
                cluster_seq = cluster_seq[:180]
                span = len(cluster_seq)
                
            start_pos = rng.randint(10, 190 - span)
            bg = generate_background(200, gc, rng)
            seq = insert_motif(bg, cluster_seq, start_pos)
            sequences.append(seq)
            
    return sequences

def generate_tier3_heterotypic_clusters(count, rng):
    """
    Tier 3: Heterotypic Clusters
    Goal: Learn TF-TF interactions, order-dependence, and cooperative rules.
    """
    sequences = []
    excluded_keys = {'TATA', 'Inr', 'DPE'}
    motif_keys = [k for k in MOTIFS.keys() if k not in excluded_keys]
    
    # Define biologically significant or high-probability pairs, and augment with random pairs
    known_pairs = [
        ('AP-1', 'NF-kB'), ('Sox', 'Oct'), ('GATA', 'ETS'), ('ETS', 'AP-1'),
        ('Fox', 'NF-kB'), ('CREB', 'AP-1'), ('E-box', 'ETS'), ('p53', 'AP-1'),
        ('Stat', 'IRF'), ('Sp1', 'E-box'), ('Oct', 'Sox2_Oct4'), ('YY1', 'E2F'),
        ('Runx', 'NFAT'), ('SMAD', 'AP-1'), ('CEBP', 'AP-1'), ('Klf4', 'Oct'),
        ('EGR1', 'Sp1'), ('NRF1', 'ETS'), ('Tead', 'AP-1'), ('Foxa2', 'GATA')
    ]
    
    # Generate random pairs to reach 50 total pairs
    all_pairs = list(known_pairs)
    while len(all_pairs) < 50:
        a = rng.choice(motif_keys)
        b = rng.choice(motif_keys)
        if a != b and (a, b) not in all_pairs and (b, a) not in all_pairs:
            all_pairs.append((a, b))
            
    spacing_opts = [5, 15, 30, 50]
    orders = ['A_B', 'B_A']
    orientations = ['++', '+-', '-+', '--']
    gc_contents = [0.45, 0.55]
    
    combos = []
    for pair in all_pairs:
        for spacing in spacing_opts:
            for order in orders:
                for orient in orientations:
                    for gc in gc_contents:
                        combos.append((pair[0], pair[1], spacing, order, orient, gc))
                        
    # 50 pairs * 4 spacings * 2 orders * 4 orientations * 2 GCs = 3,200 combinations.
    multiplier = count // len(combos)
    remainder = count % len(combos)
    
    for ma, mb, spacing, order, orient, gc in combos:
        num_to_gen = multiplier
        if remainder > 0:
            num_to_gen += 1
            remainder -= 1
            
        for _ in range(num_to_gen):
            motif_a_seq = resolve_iupac(MOTIFS[ma], rng)
            motif_b_seq = resolve_iupac(MOTIFS[mb], rng)
            
            # Orient
            if orient[0] == '-':
                motif_a_seq = reverse_complement(motif_a_seq)
            if orient[1] == '-':
                motif_b_seq = reverse_complement(motif_b_seq)
                
            # Order
            if order == 'B_A':
                motif_1, motif_2 = motif_b_seq, motif_a_seq
            else:
                motif_1, motif_2 = motif_a_seq, motif_b_seq
                
            spacer = generate_background(spacing, gc, rng)
            cluster_seq = motif_1 + spacer + motif_2
            
            span = len(cluster_seq)
            if span > 180:
                cluster_seq = cluster_seq[:180]
                span = len(cluster_seq)
                
            start_pos = rng.randint(10, 190 - span)
            bg = generate_background(200, gc, rng)
            seq = insert_motif(bg, cluster_seq, start_pos)
            sequences.append(seq)
            
    return sequences

def generate_tier4_enhancer_promoter(count, rng):
    """
    Tier 4: Enhancer-Promoter Interactions
    Goal: Learn promoter specificity and distal activation rules.
    """
    sequences = []
    excluded_keys = {'TATA', 'Inr', 'DPE'}
    motif_keys = [k for k in MOTIFS.keys() if k not in excluded_keys]
    rng.shuffle(motif_keys)
    selected_tfs = motif_keys[:50]
    
    positions = [20, 50, 80]
    orientations = ['forward', 'reverse']
    promoters = ['TATA_only', 'Inr_DPE', 'Minimal']
    
    combos = []
    for tf in selected_tfs:
        for pos in positions:
            for orient in orientations:
                for prom in promoters:
                    combos.append((tf, pos, orient, prom))
                    
    # 50 TFs * 3 positions * 2 orientations * 3 promoters = 900 combinations.
    multiplier = count // len(combos)
    remainder = count % len(combos)
    
    for tf, pos, orient, prom in combos:
        num_to_gen = multiplier
        if remainder > 0:
            num_to_gen += 1
            remainder -= 1
            
        for _ in range(num_to_gen):
            # Create promoter background (GC content 0.45 or 0.55 depending on choice)
            gc = rng.choice([0.45, 0.55])
            bg = generate_background(200, gc, rng)
            
            # Place promoter elements at the 3' end
            if prom == 'TATA_only':
                tata = resolve_iupac(MOTIFS['TATA'], rng)
                inr = resolve_iupac(MOTIFS['Inr'], rng)
                bg = insert_motif(bg, tata, 135)
                bg = insert_motif(bg, inr, 165)
            elif prom == 'Inr_DPE':
                inr = resolve_iupac(MOTIFS['Inr'], rng)
                dpe = resolve_iupac(MOTIFS['DPE'], rng)
                bg = insert_motif(bg, inr, 145)
                bg = insert_motif(bg, dpe, 175)
            elif prom == 'Minimal':
                # high GC CpG island background at 3' end
                cpg = generate_background(50, 0.65, rng)
                bg = bg[:150] + cpg
                
            # Now insert the TF enhancer motif at the 5' end
            tf_seq = resolve_iupac(MOTIFS[tf], rng)
            if orient == 'reverse':
                tf_seq = reverse_complement(tf_seq)
                
            seq = insert_motif(bg, tf_seq, pos)
            sequences.append(seq)
            
    return sequences

def generate_tier5_sentences(count, rng):
    """
    Tier 5: Multi-Motif "Sentences"
    Goal: High-complexity combinatorics and deep grammar.
    """
    sequences = []
    excluded_keys = {'TATA', 'Inr', 'DPE'}
    filtered_motifs = {k: v for k, v in MOTIFS.items() if k not in excluded_keys}
    
    for _ in range(count):
        gc = rng.choice([0.35, 0.45, 0.55, 0.65])
        num_motifs = rng.choice([3, 4, 5, 6])
        
        motif_keys = rng.sample(list(filtered_motifs.keys()), num_motifs)
        bg = generate_background(200, gc, rng)
        
        # Distribute them inside the sequence
        slot_len = 200 // num_motifs
        for i, key in enumerate(motif_keys):
            motif_seq = resolve_iupac(filtered_motifs[key], rng)
            if rng.random() < 0.5:
                motif_seq = reverse_complement(motif_seq)
                
            m_len = len(motif_seq)
            if m_len >= slot_len - 10:
                motif_seq = motif_seq[:slot_len - 10]
                m_len = len(motif_seq)
                
            slot_start = i * slot_len
            slot_end = (i + 1) * slot_len
            padding = 5
            
            if slot_end - slot_start - m_len - padding > padding:
                pos = rng.randint(slot_start + padding, slot_end - m_len - padding)
            else:
                pos = slot_start + padding
                
            bg = insert_motif(bg, motif_seq, pos)
            
        sequences.append(bg)
        
    return sequences

def generate_tier6_saturated_mutagenesis(count, rng):
    """
    Tier 6: Saturated Mutagenesis & Affinities
    Goal: Learn fine-grained motif weight matrices and single-nucleotide mutation effects.
    """
    sequences = []
    # Pick 20 core transcription factors
    core_tfs = [
        'AP-1', 'CREB', 'NF-kB', 'GATA', 'ETS', 'Oct', 'Sox', 'Fox', 'E-box',
        'IRF', 'Sp1', 'HNF4A', 'p53', 'Stat', 'YY1', 'E2F', 'Runx', 'NFAT',
        'Tead', 'CEBP'
    ]
    
    # Generate mutant libraries for each
    mutant_pools = {}
    total_mutants = 0
    for tf in core_tfs:
        wt_seq = resolve_iupac(MOTIFS[tf], rng)
        pool = [wt_seq] # First is wild-type
        
        # Single-nucleotide mutants
        for i in range(len(wt_seq)):
            orig = wt_seq[i]
            for mutant_char in ['A', 'C', 'G', 'T']:
                if mutant_char != orig:
                    mutant_seq = wt_seq[:i] + mutant_char + wt_seq[i+1:]
                    pool.append(mutant_seq)
                    
        mutant_pools[tf] = pool
        total_mutants += len(pool)
        
    # We want exactly `count` sequences.
    # We will embed the mutants into multiple distinct random backgrounds.
    multiplier = count // total_mutants
    remainder = count % total_mutants
    
    for tf in core_tfs:
        pool = mutant_pools[tf]
        for mutant_seq in pool:
            num_to_gen = multiplier
            if remainder > 0:
                num_to_gen += 1
                remainder -= 1
                
            for _ in range(num_to_gen):
                gc = rng.choice([0.40, 0.55])
                bg = generate_background(200, gc, rng)
                # Place mutant at a fixed, clean middle position (e.g., 90)
                pos = 90
                seq = insert_motif(bg, mutant_seq, pos)
                sequences.append(seq)
                
    return sequences

def generate_tier7_controls(count, rng):
    """
    Tier 7: Neutral and Negative Controls
    Goal: Learn background GC biases and k-mer frequencies.
    """
    sequences = []
    # 1. GC content curve (2,000 sequences)
    # We distribute them across a wide range of GC contents from 0.20 to 0.80
    gc_steps = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
    num_per_step = 2000 // len(gc_steps)
    remainder = 2000 % len(gc_steps)
    
    for gc in gc_steps:
        num_to_gen = num_per_step
        if remainder > 0:
            num_to_gen += 1
            remainder -= 1
        for _ in range(num_to_gen):
            sequences.append(generate_background(200, gc, rng))
            
    # 2. Purely random background sequences at general mammalian GC contents (remaining count)
    remaining_count = count - len(sequences)
    for _ in range(remaining_count):
        gc = rng.choice([0.40, 0.45, 0.50, 0.55])
        sequences.append(generate_background(200, gc, rng))
        
    return sequences

# ---------------------------------------------------------
# Main Generation Orchestrator
# ---------------------------------------------------------

def main():
    print("Initializing MPRA sequence generation...")
    rng = random.Random(RANDOM_SEED)
    
    # Core target numbers for each tier
    tier_counts = {
        'tier1': 6000,
        'tier2': 6000,
        'tier3': 10000,
        'tier4': 5000,
        'tier5': 15000,
        'tier6': 4000,
        'tier7': 4000
    }
    
    all_sequences = []
    
    print("Generating Tier 1 (Single Motif Scans)...")
    t1 = generate_tier1_single_motif_scans(tier_counts['tier1'], rng)
    all_sequences.extend(t1)
    
    print("Generating Tier 2 (Homotypic Clusters)...")
    t2 = generate_tier2_homotypic_clusters(tier_counts['tier2'], rng)
    all_sequences.extend(t2)
    
    print("Generating Tier 3 (Heterotypic Clusters)...")
    t3 = generate_tier3_heterotypic_clusters(tier_counts['tier3'], rng)
    all_sequences.extend(t3)
    
    print("Generating Tier 4 (Enhancer-Promoter)...")
    t4 = generate_tier4_enhancer_promoter(tier_counts['tier4'], rng)
    all_sequences.extend(t4)
    
    print("Generating Tier 5 (Multi-Motif Sentences)...")
    t5 = generate_tier5_sentences(tier_counts['tier5'], rng)
    all_sequences.extend(t5)
    
    print("Generating Tier 6 (Saturated Mutagenesis)...")
    t6 = generate_tier6_saturated_mutagenesis(tier_counts['tier6'], rng)
    all_sequences.extend(t6)
    
    print("Generating Tier 7 (Neutral & Negative Controls)...")
    t7 = generate_tier7_controls(tier_counts['tier7'], rng)
    all_sequences.extend(t7)
    
    # ---------------------------------------------------------
    # Post-processing: Validation, De-duplication, & Formatting
    # ---------------------------------------------------------
    print(f"Total sequences generated so far: {len(all_sequences)}")
    
    # Ensure uppercase and correct length
    all_sequences = [s.upper()[:200] for s in all_sequences]
    
    # De-duplicate while maintaining the exact sequence count
    unique_seqs = set(all_sequences)
    duplicate_count = len(all_sequences) - len(unique_seqs)
    print(f"Duplicates identified: {duplicate_count}")
    
    all_sequences = list(unique_seqs)
    
    # If we have less than 50,000 unique sequences, fill the remainder with Tier 5 (Multi-motif) or random Tier 7
    target_total = 50000
    while len(all_sequences) < target_total:
        needed = target_total - len(all_sequences)
        print(f"Regenerating {needed} unique sequences to reach 50,000...")
        # Fill half with Tier 5 and half with Tier 7
        t5_fill = generate_tier5_sentences(needed // 2 + 1, rng)
        t7_fill = generate_tier7_controls(needed // 2 + 1, rng)
        
        fill_pool = [s.upper()[:200] for s in (t5_fill + t7_fill)]
        for s in fill_pool:
            if s not in unique_seqs:
                unique_seqs.add(s)
                all_sequences.append(s)
                if len(all_sequences) == target_total:
                    break
                    
    # In the unlikely event of over-generation, truncate to exactly 50,000
    if len(all_sequences) > target_total:
        print(f"Truncating from {len(all_sequences)} to exactly 50,000...")
        all_sequences = all_sequences[:target_total]
        
    # Shuffle finally to prevent block ordering biases
    print("Shuffling final sequence library...")
    rng.shuffle(all_sequences)
    
    # Comprehensive checks
    print("Running final sanity checks...")
    assert len(all_sequences) == target_total, f"Error: Total count is {len(all_sequences)}, should be {target_total}!"
    
    valid_chars = set("ACGT")
    for idx, seq in enumerate(all_sequences):
        assert len(seq) == 200, f"Error: Sequence at index {idx} has length {len(seq)} instead of 200!"
        invalid_chars = set(seq) - valid_chars
        assert not invalid_chars, f"Error: Sequence at index {idx} contains invalid characters: {invalid_chars}!"
        
    # Ensure the directory exists
    os.makedirs("library", exist_ok=True)
    
    # Save the output file
    output_path = "library/sequences.txt"
    print(f"Saving exactly 50,000 validated sequences to {output_path}...")
    with open(output_path, "w") as f:
        for seq in all_sequences:
            f.write(seq + "\n")
            
    print("Generation completed successfully!")

if __name__ == "__main__":
    main()
