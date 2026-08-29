import os
import gzip
import random
import pandas as pd
from collections import defaultdict, Counter
from Bio import SeqIO
from Bio.Seq import Seq

# Set random seed for reproducibility
random.seed(42)

# Global IUPAC nucleotide dictionary
IUPAC_DICT = {
    'A': ['A'], 'C': ['C'], 'G': ['G'], 'T': ['T'],
    'W': ['A', 'T'], 'S': ['C', 'G'], 'Y': ['C', 'T'], 'R': ['A', 'G'],
    'M': ['A', 'C'], 'K': ['G', 'T'], 
    'H': ['A', 'C', 'T'], 'B': ['C', 'G', 'T'], 'V': ['A', 'C', 'G'], 'D': ['A', 'G', 'T'],
    'N': ['A', 'C', 'G', 'T']
}

# 14 high-confidence motifs (core-promoters & universal enhancers)
MOTIFS = {
    'TATA': 'TATAWAWR',          # TATA-box (Core)
    'SP1': 'GGGGCGGGGC',         # GC-box / Sp1 (Core/Promoter)
    'NFY': 'CCAAT',              # CCAAT-box / NF-Y (Promoter)
    'CREB': 'TGACGTCA',          # CRE (General)
    'AP1': 'TGASTCA',            # TRE / AP-1 (Universal Enhancer)
    'NFKB': 'GGGRNYYYCC',        # NF-kB (Universal Enhancer)
    'CTCF': 'CCACYAGGGGGCGC',    # CTCF (Structural/Enhancer)
    'GATA': 'WGATAR',            # GATA (Enhancer)
    'SOX': 'CCTTTGWW',           # SOX (Enhancer)
    'FOXA': 'TRTTTAY',           # FOXA / Forkhead (Enhancer)
    'EBOX': 'CACGTG',            # Myc E-box (General)
    'ETS': 'CGGAA',              # ETS / GABPA (Promoter/Enhancer)
    'YY1': 'CGCCATNTT',          # YY1 (Core/General)
    'NRF1': 'YGCGCAYGCGC'        # NRF1 (Promoter)
}

def rev_comp(seq):
    """Returns the reverse complement of a sequence."""
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
                  'a': 't', 'c': 'g', 'g': 'c', 't': 'a',
                  'N': 'N', 'n': 'n'}
    return "".join(complement[base] for base in reversed(seq))

def generate_from_iupac(iupac_seq):
    """Generates a random DNA sequence matching an IUPAC consensus string."""
    return "".join(random.choice(IUPAC_DICT[c.upper()]) for c in iupac_seq)

def dinucleotide_shuffle(sequence):
    """
    Shuffles a sequence while exactly preserving dinucleotide counts.
    Uses the Altschul-Erickson Eulerian walk algorithm.
    """
    if len(sequence) < 2:
        return sequence
    
    # Create transition adjacency list
    adj = defaultdict(list)
    for i in range(len(sequence) - 1):
        adj[sequence[i]].append(sequence[i+1])
        
    # Isolate last edge for each nucleotide to maintain Eulerian properties
    last_edges = {}
    for i in range(len(sequence) - 2, -1, -1):
        char = sequence[i]
        if char not in last_edges:
            target = sequence[i+1]
            last_edges[char] = target
            adj[char].remove(target)
            
    # Shuffle the remaining edges
    for char in adj:
        random.shuffle(adj[char])
        
    # Reconstruct the sequence
    new_seq = [sequence[0]]
    current = sequence[0]
    for _ in range(len(sequence) - 1):
        if adj[current]:
            next_char = adj[current].pop()
        else:
            next_char = last_edges.get(current)
            if next_char is None:
                # Graph was disconnected; retry recursively
                return dinucleotide_shuffle(sequence)
        new_seq.append(next_char)
        current = next_char
        
    return "".join(new_seq)

def generate_background(length, gc_content):
    """Generates random DNA sequence of specified length and GC content."""
    bases = ['A', 'C', 'G', 'T']
    p_gc = gc_content / 2.0
    p_at = (1.0 - gc_content) / 2.0
    weights = [p_at, p_gc, p_gc, p_at]
    return "".join(random.choices(bases, weights=weights, k=length))

def get_non_overlapping_positions(bg_len, motif_lengths, min_spacing=5):
    """Samples non-overlapping start positions for multiple motifs."""
    for _ in range(1000):
        positions = []
        occupied = []
        for l in motif_lengths:
            placed = False
            for try_idx in range(100):
                pos = random.randint(0, bg_len - l)
                overlap = False
                for start, end in occupied:
                    if not (pos + l + min_spacing <= start or pos >= end + min_spacing):
                        overlap = True
                        break
                if not overlap:
                    positions.append(pos)
                    occupied.append((pos, pos + l))
                    placed = True
                    break
            if not placed:
                break
        if len(positions) == len(motif_lengths):
            return positions
    return None

def main():
    print("--- STEP 1: Extracting Chromosome 21 Promoters ---")
    # Load chr21 sequence
    with gzip.open('data/chr21.fa.gz', 'rt') as f:
        chr21_seq = str(next(SeqIO.parse(f, 'fasta')).seq).upper()
    print(f"Chromosome 21 length: {len(chr21_seq)}")

    # Load BED annotations
    df = pd.read_csv('data/Hs_EPDnew.bed', sep='\s+', header=None, 
                     names=['chrom', 'start', 'end', 'name', 'score', 'strand', 'thick_start', 'thick_end'])
    
    # Filter and extract chr21 promoters
    chr21_promoters = df[df['chrom'] == 'chr21']
    natural_promoters_chr21 = []
    
    for idx, row in chr21_promoters.iterrows():
        strand = row['strand']
        thick_start = row['thick_start']
        thick_end = row['thick_end']
        
        if strand == '+':
            tss = thick_start
            p_start = tss - 100
            p_end = tss + 100
            seq = chr21_seq[p_start:p_end]
        else:
            tss = thick_end - 1
            p_start = tss - 99
            p_end = tss + 101
            seq = rev_comp(chr21_seq[p_start:p_end])
            
        seq = seq.upper()
        if len(seq) == 200 and 'N' not in seq:
            natural_promoters_chr21.append(seq)
            
    print(f"Extracted {len(natural_promoters_chr21)} wild-type promoters from Chromosome 21.")

    print("\n--- STEP 2: Generating High-Resolution Tiling Mutagenesis (Perturbed Variants) ---")
    # For each of the 308 wild-type promoters, we generate exactly 10 variants.
    # Each variant scrambles a non-overlapping 20bp window of the 200bp sequence.
    # This represents a complete 20bp tiling mutational scan of all promoters.
    perturbed_variants = []
    for seq in natural_promoters_chr21:
        for i in range(10):
            start = i * 20
            end = start + 20
            window = seq[start:end]
            shuffled_window = dinucleotide_shuffle(window)
            mutated_seq = seq[:start] + shuffled_window + seq[end:]
            perturbed_variants.append(mutated_seq)
            
    print(f"Generated {len(perturbed_variants)} tiling mutated variants (10 variants for each of the 308 promoters, total: 3,080).")

    print("\n--- STEP 3: Synthesizing Combinatorial Motif Constructs ---")
    synthetic_constructs = []
    gc_choices = [0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
    motif_keys = list(MOTIFS.keys())

    # Sub-cohort 3.1: Single Motif Insertions (7,000 sequences)
    print("Generating single-motif synthetic constructs...")
    while len(synthetic_constructs) < 7000:
        gc = random.choice(gc_choices)
        bg = generate_background(200, gc)
        motif_key = random.choice(motif_keys)
        motif_seq = generate_from_iupac(MOTIFS[motif_key])
        if random.random() < 0.5:
            motif_seq = rev_comp(motif_seq)
        
        pos = random.randint(30, 170 - len(motif_seq))
        seq = bg[:pos] + motif_seq + bg[pos+len(motif_seq):]
        synthetic_constructs.append(seq)

    # Sub-cohort 3.2: Homotypic Motif Clusters (10,000 sequences)
    print("Generating homotypic cluster synthetic constructs...")
    while len(synthetic_constructs) < 17000:
        gc = random.choice(gc_choices)
        bg = generate_background(200, gc)
        motif_key = random.choice(motif_keys)
        n_copies = random.choice([2, 3, 4])
        
        m_lengths = [len(MOTIFS[motif_key])] * n_copies
        positions = get_non_overlapping_positions(200, m_lengths, min_spacing=5)
        if positions is None:
            continue
            
        seq_chars = list(bg)
        for pos in positions:
            m_seq = generate_from_iupac(MOTIFS[motif_key])
            if random.random() < 0.5:
                m_seq = rev_comp(m_seq)
            seq_chars[pos:pos+len(m_seq)] = list(m_seq)
            
        synthetic_constructs.append("".join(seq_chars))

    # Sub-cohort 3.3: Heterotypic Combinations (12,000 sequences)
    print("Generating heterotypic combination synthetic constructs...")
    synergistic_pairs = [
        # Promoter-specific pairs
        ('SP1', 'TATA'), ('NFY', 'SP1'), ('ETS', 'SP1'), ('YY1', 'TATA'),
        # Enhancer-specific pairs
        ('AP1', 'NFKB'), ('GATA', 'SOX'), ('AP1', 'CTCF'), ('CREB', 'AP1'), ('FOXA', 'GATA'), ('EBOX', 'AP1'),
        # Promoter-Enhancer interaction pairs
        ('SP1', 'AP1'), ('TATA', 'NFKB')
    ]
    while len(synthetic_constructs) < 29000:
        gc = random.choice(gc_choices)
        bg = generate_background(200, gc)
        pair = random.choice(synergistic_pairs)
        
        m_lengths = [len(MOTIFS[pair[0]]), len(MOTIFS[pair[1]])]
        positions = get_non_overlapping_positions(200, m_lengths, min_spacing=5)
        if positions is None:
            continue
            
        seq_chars = list(bg)
        # Place Motif A
        m_seq_a = generate_from_iupac(MOTIFS[pair[0]])
        if random.random() < 0.5:
            m_seq_a = rev_comp(m_seq_a)
        seq_chars[positions[0]:positions[0]+len(m_seq_a)] = list(m_seq_a)
        
        # Place Motif B
        m_seq_b = generate_from_iupac(MOTIFS[pair[1]])
        if random.random() < 0.5:
            m_seq_b = rev_comp(m_seq_b)
        seq_chars[positions[1]:positions[1]+len(m_seq_b)] = list(m_seq_b)
        
        synthetic_constructs.append("".join(seq_chars))

    # Sub-cohort 3.4: Random Motif Assemblies (6,000 sequences)
    print("Generating random motif assembly synthetic constructs...")
    while len(synthetic_constructs) < 35000:
        gc = random.choice(gc_choices)
        bg = generate_background(200, gc)
        n_motifs = random.choice([2, 3, 4])
        selected_motif_keys = random.choices(motif_keys, k=n_motifs)
        
        m_lengths = [len(MOTIFS[k]) for k in selected_motif_keys]
        positions = get_non_overlapping_positions(200, m_lengths, min_spacing=10)
        if positions is None:
            continue
            
        seq_chars = list(bg)
        for k, pos in zip(selected_motif_keys, positions):
            m_seq = generate_from_iupac(MOTIFS[k])
            if random.random() < 0.5:
                m_seq = rev_comp(m_seq)
            seq_chars[pos:pos+len(m_seq)] = list(m_seq)
            
        synthetic_constructs.append("".join(seq_chars))

    print(f"Generated {len(synthetic_constructs)} synthetic constructs (Expected: 35,000)")

    print("\n--- STEP 4: Sampling Genomic Background Controls ---")
    genomic_controls = []
    
    # Define excluded ranges around chromosome 21 promoters to avoid functional elements
    # We will exclude promoter start - 500bp to promoter end + 500bp
    excluded_intervals = []
    for idx, row in chr21_promoters.iterrows():
        excluded_intervals.append((max(0, row['start'] - 500), min(len(chr21_seq), row['end'] + 500)))
        
    def is_excluded(pos):
        for start, end in excluded_intervals:
            if start <= pos < end or start <= pos + 200 < end:
                return True
        return False

    print("Sampling 11,612 background genomic segments...")
    while len(genomic_controls) < 11612:
        # Sample a random coordinate on chr21
        start_coord = random.randint(0, len(chr21_seq) - 200)
        if is_excluded(start_coord):
            continue
            
        bg_seq = chr21_seq[start_coord:start_coord+200]
        if 'N' in bg_seq or 'n' in bg_seq:
            continue
            
        genomic_controls.append(bg_seq)

    print(f"Sampled {len(genomic_controls)} genomic background sequences (Expected: 11,612)")

    # Combine all sequences
    all_sequences = natural_promoters_chr21 + perturbed_variants + synthetic_constructs + genomic_controls
    
    print("\n--- STEP 5: De-duplication and Quality Control ---")
    # Strictly ensure exactly 50,000 unique sequences
    unique_sequences = list(dict.fromkeys(all_sequences))
    print(f"Total sequences: {len(all_sequences)}")
    print(f"Unique sequences: {len(unique_sequences)}")
    
    # If there are duplicates, replace them with new unique synthetic constructs
    duplicates_count = len(all_sequences) - len(unique_sequences)
    if duplicates_count > 0:
        print(f"Replacing {duplicates_count} duplicates with new unique synthetic constructs...")
        unique_set = set(unique_sequences)
        while len(unique_sequences) < 50000:
            gc = random.choice(gc_choices)
            bg = generate_background(200, gc)
            n_motifs = random.choice([2, 3, 4])
            selected_motif_keys = random.choices(motif_keys, k=n_motifs)
            
            m_lengths = [len(MOTIFS[k]) for k in selected_motif_keys]
            positions = get_non_overlapping_positions(200, m_lengths, min_spacing=10)
            if positions is None:
                continue
                
            seq_chars = list(bg)
            for k, pos in zip(selected_motif_keys, positions):
                m_seq = generate_from_iupac(MOTIFS[k])
                if random.random() < 0.5:
                    m_seq = rev_comp(m_seq)
                seq_chars[pos:pos+len(m_seq)] = list(m_seq)
                
            new_seq = "".join(seq_chars)
            if new_seq not in unique_set:
                unique_sequences.append(new_seq)
                unique_set.add(new_seq)
                
    # Final slice to ensure EXACTLY 50,000 sequences
    final_sequences = unique_sequences[:50000]
    
    # Final rigorous validation checks
    assert len(final_sequences) == 50000, f"Error: Library has {len(final_sequences)} sequences instead of 50000"
    for idx, s in enumerate(final_sequences):
        assert len(s) == 200, f"Error: Sequence at index {idx} has length {len(s)} instead of 200"
        invalid_chars = set(s) - {'A', 'C', 'G', 'T'}
        assert not invalid_chars, f"Error: Sequence at index {idx} contains invalid characters: {invalid_chars}"

    print("Success: Passed all validation checks!")
    print(f"Final sequences size: {len(final_sequences)}")

    # Write sequences to the library/sequences.txt file
    os.makedirs('library', exist_ok=True)
    out_path = 'library/sequences.txt'
    with open(out_path, 'w') as f:
        for s in final_sequences:
            f.write(s + '\n')
            
    print(f"Successfully wrote exactly 50,000 sequences to {out_path}")

if __name__ == "__main__":
    main()
