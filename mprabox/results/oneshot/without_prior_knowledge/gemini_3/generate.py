#!/usr/bin/env python3
"""
MPRA Sequence Library Generator
Produces exactly 50,000 sequences of length 200bp for model training.
Implementation of the 5-layer library design:
1. Real Human Promoters (15,000)
2. Real Human Non-Promoters (15,000)
3. Promoter Motif Knockouts (5,000)
4. Synthetic Combinatorial Grammar (10,000)
5. Systematic Motif Scan (5,000)
"""

import os
import re
import random
import sys

# Set random seed for reproducibility
random.seed(42)

# Define core motifs in IUPAC notation
MOTIFS = {
    'AP-1': 'TGASTCA',
    'SP1': 'GGGGYGGGG',
    'MYC': 'CACGTG',
    'NF-kB': 'GGGRNNYYCC',
    'CREB': 'TGACGTCA',
    'YY1': 'CCGCCATNTT',
    'CTCF': 'CCACYAGGGGGCGCY',
    'GATA': 'WGATAR',
    'FOXA1': 'TGTTTACY',
    'SRF': 'CCWWWWWWGG'
}

# IUPAC character to nucleotide options
IUPAC_OPTIONS = {
    'A': ['A'], 'C': ['C'], 'G': ['G'], 'T': ['T'],
    'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'],
    'K': ['G', 'T'], 'M': ['A', 'C'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'],
    'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'], 'N': ['A', 'C', 'G', 'T']
}

IUPAC_MAP = {
    'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T',
    'R': '[AG]', 'Y': '[CT]', 'S': '[GC]', 'W': '[AT]',
    'K': '[GT]', 'M': '[AC]', 'B': '[CGT]', 'D': '[AGT]',
    'H': '[ACT]', 'V': '[ACG]', 'N': '[ACGT]'
}

IUPAC_COMP = {
    'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
    'R': 'Y', 'Y': 'R', 'S': 'S', 'W': 'W',
    'K': 'M', 'M': 'K', 'B': 'V', 'D': 'H',
    'H': 'D', 'V': 'B', 'N': 'N'
}

def iupac_to_regex(pattern):
    return ''.join(IUPAC_MAP.get(c, c) for c in pattern)

def get_combined_regex(pattern):
    fwd = iupac_to_regex(pattern)
    rc_pattern = ''.join(IUPAC_COMP[c] for c in pattern[::-1])
    rc = iupac_to_regex(rc_pattern)
    return re.compile(f'({fwd})|({rc})', re.IGNORECASE)

# Compile regular expressions for all motifs (matches both forward and reverse strands)
COMPILED_MOTIFS = {name: get_combined_regex(pat) for name, pat in MOTIFS.items()}

def reverse_complement(seq):
    rc_map = str.maketrans('ACGTacgt', 'TGCAtgca')
    return seq.translate(rc_map)[::-1]

def instantiate_motif(iupac_pattern):
    return ''.join(random.choice(IUPAC_OPTIONS[c]) for c in iupac_pattern)

def generate_background(length, gc_content):
    g_or_c = int(length * gc_content)
    a_or_t = length - g_or_c
    bases = ['G', 'C'] * (g_or_c // 2) + ['A', 'T'] * (a_or_t // 2)
    while len(bases) < length:
        if random.random() < gc_content:
            bases.append(random.choice(['G', 'C']))
        else:
            bases.append(random.choice(['A', 'T']))
    random.shuffle(bases)
    return ''.join(bases)

def parse_fasta(file_path):
    seqs = []
    with open(file_path, 'r') as f:
        current_seq = []
        for line in f:
            if line.startswith('>'):
                if current_seq:
                    seqs.append(''.join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line.strip().upper())
        if current_seq:
            seqs.append(''.join(current_seq))
    return seqs

def mutate_promoter(seq, compiled_motifs):
    # Find all matches across all motifs
    intervals = []
    for name, regex in compiled_motifs.items():
        for match in regex.finditer(seq):
            intervals.append((match.start(), match.end()))
            
    if not intervals:
        return seq
        
    # Merge overlapping intervals
    intervals.sort(key=lambda x: x[0])
    merged = []
    for current in intervals:
        if not merged:
            merged.append(current)
        else:
            prev = merged[-1]
            if current[0] < prev[1]: # Overlap
                merged[-1] = (prev[0], max(prev[1], current[1]))
            else:
                merged.append(current)
                
    # Mutate merged intervals
    seq_chars = list(seq)
    for start, end in merged:
        length = end - start
        attempts = 0
        while attempts < 100:
            new_sub = ''.join(random.choice(['A', 'C', 'G', 'T']) for _ in range(length))
            # Test if replacement introduces any motifs
            temp_chars = list(seq_chars)
            temp_chars[start:end] = list(new_sub)
            temp_seq = ''.join(temp_chars)
            
            has_overlap_match = False
            for name, regex in compiled_motifs.items():
                for m in regex.finditer(temp_seq):
                    if max(m.start(), start) < min(m.end(), end):
                        has_overlap_match = True
                        break
                if has_overlap_match:
                    break
            
            if not has_overlap_match:
                seq_chars[start:end] = list(new_sub)
                break
            attempts += 1
            
    return ''.join(seq_chars)

def main():
    print("Starting sequence generation...")
    os.makedirs('library', exist_ok=True)
    
    # Check that reference data is present
    promoter_file = 'data/human_non_tata.fa'
    nonpromoter_file = 'data/human_nonprom_big.fa'
    if not os.path.exists(promoter_file) or not os.path.exists(nonpromoter_file):
        print("Error: Reference FASTA files not found in data/.")
        sys.exit(1)
        
    # Parse promoter sequences
    all_promoters_raw = parse_fasta(promoter_file)
    # Parse non-promoter sequences
    all_nonpromoters_raw = parse_fasta(nonpromoter_file)
    
    print(f"Parsed {len(all_promoters_raw)} promoters and {len(all_nonpromoters_raw)} non-promoters.")
    
    # Filter and slice to 200bp
    promoters_sliced = [s[50:250] for s in all_promoters_raw if 'N' not in s[50:250] and len(s) >= 250]
    nonpromoters_sliced = [s[50:250] for s in all_nonpromoters_raw if 'N' not in s[50:250] and len(s) >= 250]
    
    print(f"Clean sliced promoter pool size: {len(promoters_sliced)}")
    print(f"Clean sliced non-promoter pool size: {len(nonpromoters_sliced)}")
    
    # Classify promoters by presence of motifs to select WT sequences to mutate
    promoters_with_motif = []
    promoters_without_motif = []
    
    for p in promoters_sliced:
        has_motif = any(regex.search(p) for regex in COMPILED_MOTIFS.values())
        if has_motif:
            promoters_with_motif.append(p)
        else:
            promoters_without_motif.append(p)
            
    print(f"Promoters with motifs: {len(promoters_with_motif)}, without: {len(promoters_without_motif)}")
    
    # ----------------------------------------------------
    # Layer 3: Genomic Promoter Knockouts (5,000)
    # ----------------------------------------------------
    print("Generating Layer 3 (Promoter Knockouts)...")
    # Take the first 5,000 promoters with motifs for mutation
    wt_promoters_to_mutate = promoters_with_motif[:5000]
    layer3_sequences = []
    for wt_seq in wt_promoters_to_mutate:
        mut_seq = mutate_promoter(wt_seq, COMPILED_MOTIFS)
        layer3_sequences.append(mut_seq)
        
    # ----------------------------------------------------
    # Layer 1: Real Human Promoters (15,000)
    # ----------------------------------------------------
    print("Generating Layer 1 (Promoters)...")
    # To form the causal pairs, Layer 1 MUST include the 5,000 WT promoters we mutated in Layer 3
    layer1_sequences = list(wt_promoters_to_mutate)
    # The remaining 10,000 promoters are filled from the rest of the pool
    remaining_promoters_pool = promoters_with_motif[5000:] + promoters_without_motif
    layer1_sequences.extend(remaining_promoters_pool[:10000])
    
    # ----------------------------------------------------
    # Layer 2: Real Human Non-Promoters (15,000)
    # ----------------------------------------------------
    print("Generating Layer 2 (Non-Promoters)...")
    layer2_sequences = nonpromoters_sliced[:15000]
    
    # ----------------------------------------------------
    # Layer 4: Synthetic Combinatorial Grammar (10,000)
    # ----------------------------------------------------
    print("Generating Layer 4 (Synthetic Combinatorial Grammar)...")
    layer4_sequences = []
    gc_levels = [0.35, 0.45, 0.55, 0.65]
    
    # Subset 4A: Single Motif (2,500)
    print("  4A: Single motifs...")
    for _ in range(2500):
        gc = random.choice(gc_levels)
        bg = generate_background(200, gc)
        motif_name = random.choice(list(MOTIFS.keys()))
        motif_seq = instantiate_motif(MOTIFS[motif_name])
        if random.random() < 0.5:
            motif_seq = reverse_complement(motif_seq)
        
        # Insert at random position (leaving 20bp boundary)
        pos = random.randint(20, 180 - len(motif_seq))
        seq = bg[:pos] + motif_seq + bg[pos + len(motif_seq):]
        layer4_sequences.append(seq)
        
    # Subset 4B: Homotypic Spacing & Density (2,500)
    print("  4B: Homotypic spacing...")
    for _ in range(2500):
        gc = random.choice(gc_levels)
        bg = generate_background(200, gc)
        motif_name = random.choice(list(MOTIFS.keys()))
        
        # Safe fitting search
        attempts = 0
        start = 20
        density = 2
        spacing = 10
        motif_pattern = MOTIFS[motif_name]
        m_len = len(motif_pattern)
        
        while attempts < 100:
            d = random.choice([2, 3])
            s = random.choice([10, 20, 35, 50, 75])
            total_len = d * m_len + (d - 1) * s
            if total_len <= 160:
                density = d
                spacing = s
                start = random.randint(20, 180 - total_len)
                break
            elif total_len <= 190:
                density = d
                spacing = s
                start = random.randint(5, 195 - total_len)
                break
            attempts += 1
            
        seq_list = list(bg)
        for i in range(density):
            m_seq = instantiate_motif(motif_pattern)
            if random.random() < 0.5:
                m_seq = reverse_complement(m_seq)
            pos = start + i * (m_len + spacing)
            seq_list[pos:pos+m_len] = list(m_seq)
            
        layer4_sequences.append(''.join(seq_list))
        
    # Subset 4C: Heterotypic Pairwise Combinations (3,000)
    print("  4C: Heterotypic pairs...")
    cooperative_pairs = [
        ('AP-1', 'NF-kB'), ('AP-1', 'SP1'), ('GATA', 'SP1'),
        ('MYC', 'SP1'), ('AP-1', 'GATA'), ('CREB', 'SP1'),
        ('NF-kB', 'SP1'), ('CTCF', 'AP-1'), ('CTCF', 'SP1')
    ]
    for _ in range(3000):
        gc = random.choice(gc_levels)
        bg = generate_background(200, gc)
        m1_name, m2_name = random.choice(cooperative_pairs)
        
        m1_seq = instantiate_motif(MOTIFS[m1_name])
        if random.random() < 0.5:
            m1_seq = reverse_complement(m1_seq)
            
        m2_seq = instantiate_motif(MOTIFS[m2_name])
        if random.random() < 0.5:
            m2_seq = reverse_complement(m2_seq)
            
        attempts = 0
        spacing = 10
        start = 20
        while attempts < 100:
            s = random.choice([10, 15, 20, 30, 45, 60])
            total_len = len(m1_seq) + len(m2_seq) + s
            if total_len <= 160:
                spacing = s
                start = random.randint(20, 180 - total_len)
                break
            elif total_len <= 190:
                spacing = s
                start = random.randint(5, 195 - total_len)
                break
            attempts += 1
            
        seq_list = list(bg)
        # Place motif 1
        seq_list[start:start+len(m1_seq)] = list(m1_seq)
        # Place motif 2
        pos2 = start + len(m1_seq) + spacing
        seq_list[pos2:pos2+len(m2_seq)] = list(m2_seq)
        
        layer4_sequences.append(''.join(seq_list))
        
    # Subset 4D: High-Density Activator Clusters (2,000)
    print("  4D: High-density clusters...")
    activators = ['AP-1', 'SP1', 'MYC', 'NF-kB', 'GATA', 'CREB', 'YY1']
    for _ in range(2000):
        gc = random.choice(gc_levels)
        bg = generate_background(200, gc)
        
        attempts = 0
        density = 3
        selected_m = []
        spacings = []
        start = 20
        while attempts < 100:
            d = random.choice([3, 4])
            sel = random.sample(activators, d)
            sp = [random.randint(10, 20) for _ in range(d - 1)]
            total_len = sum(len(MOTIFS[m]) for m in sel) + sum(sp)
            if total_len <= 180:
                density = d
                selected_m = sel
                spacings = sp
                start = random.randint(10, 190 - total_len)
                break
            attempts += 1
            
        # If the search failed, fallback to safe default
        if not selected_m:
            selected_m = ['AP-1', 'SP1', 'MYC']
            spacings = [10, 10]
            start = 20
            
        seq_list = list(bg)
        curr_pos = start
        for idx, m_name in enumerate(selected_m):
            m_seq = instantiate_motif(MOTIFS[m_name])
            if random.random() < 0.5:
                m_seq = reverse_complement(m_seq)
            seq_list[curr_pos:curr_pos+len(m_seq)] = list(m_seq)
            if idx < len(selected_m) - 1:
                curr_pos += len(m_seq) + spacings[idx]
                
        layer4_sequences.append(''.join(seq_list))
        
    # ----------------------------------------------------
    # Layer 5: Systematic Motif Scan (5,000)
    # ----------------------------------------------------
    print("Generating Layer 5 (Systematic Motif Scan)...")
    layer5_sequences = []
    positions = [20, 50, 80, 110, 140, 170]
    
    # 10 motifs, each gets 500 sequences
    for m_name in MOTIFS.keys():
        for i in range(500):
            # Balance GC content: cycle through 35%, 45%, 55%, 65%
            gc = gc_levels[i % len(gc_levels)]
            bg = generate_background(200, gc)
            
            # Balance orientation: alternate forward and reverse complement
            m_seq = instantiate_motif(MOTIFS[m_name])
            if i % 2 == 1:
                m_seq = reverse_complement(m_seq)
                
            # Cycle through positions
            pos = positions[i % len(positions)]
            if pos + len(m_seq) > 200:
                pos = 200 - len(m_seq)
                
            seq_list = list(bg)
            seq_list[pos:pos+len(m_seq)] = list(m_seq)
            layer5_sequences.append(''.join(seq_list))
            
    # ----------------------------------------------------
    # Assemble and Validate Library
    # ----------------------------------------------------
    all_sequences = (
        layer1_sequences + 
        layer2_sequences + 
        layer3_sequences + 
        layer4_sequences + 
        layer5_sequences
    )
    
    print(f"Total sequences generated: {len(all_sequences)}")
    print(f"  Layer 1 (Promoters): {len(layer1_sequences)}")
    print(f"  Layer 2 (Non-Promoters): {len(layer2_sequences)}")
    print(f"  Layer 3 (Knockouts): {len(layer3_sequences)}")
    print(f"  Layer 4 (Grammar): {len(layer4_sequences)}")
    print(f"  Layer 5 (Motif Scan): {len(layer5_sequences)}")
    
    # Strictly validate constraints
    assert len(all_sequences) == 50000, f"Error: Library must have exactly 50,000 sequences, got {len(all_sequences)}"
    
    for idx, seq in enumerate(all_sequences):
        assert len(seq) == 200, f"Error: Sequence at index {idx} has length {len(seq)} (expected 200)"
        non_acgt = [c for c in seq if c not in 'ACGT']
        assert not non_acgt, f"Error: Sequence at index {idx} contains invalid characters: {non_acgt}"
        
    print("Library successfully validated! Writing to library/sequences.txt...")
    
    with open('library/sequences.txt', 'w') as out:
        for seq in all_sequences:
            out.write(seq + '\n')
            
    print("Generation complete!")

if __name__ == '__main__':
    main()
