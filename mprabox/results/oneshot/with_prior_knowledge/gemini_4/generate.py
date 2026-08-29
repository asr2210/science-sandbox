#!/usr/bin/env python3
import os
import gzip
import numpy as np
import random
import bisect
import re
from twobitreader import TwoBitFile

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def main():
    set_seed(42)
    print("Initializing MPRA Library Generation...")
    
    # Paths
    dhs_index_path = 'data/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz'
    nmf_mixture_path = 'data/2018-06-08NC16_NNDSVD_Mixture.npy.gz'
    genome_2bit_path = 'data/hg38.2bit'
    output_dir = 'library'
    output_path = os.path.join(output_dir, 'sequences.txt')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load Reference Genome
    print("Loading hg38 reference genome...")
    genome = TwoBitFile(genome_2bit_path)
    
    # Filter for standard chromosomes
    std_chroms = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
    std_chroms = [c for c in std_chroms if c in genome]
    print(f"Standard chromosomes detected: {std_chroms}")
    
    # Chromosome lengths and probabilities (proportional to length)
    chrom_lens = {c: len(genome[c]) for c in std_chroms}
    total_len = sum(chrom_lens.values())
    chrom_probs = [chrom_lens[c] / total_len for c in std_chroms]
    
    # 2. Load DHS Index and NMF Topic Loadings
    print("Loading NMF topic loadings...")
    with gzip.open(nmf_mixture_path, 'rb') as f:
        nmf_matrix = np.load(f) # Shape: (16, 3591898)
    
    print("Loading DHS Index metadata...")
    dhs_index = []
    # Columns: seqname, start, end, identifier, mean_signal, numsamples, summit, core_start, core_end, component
    with gzip.open(dhs_index_path, 'rt') as f:
        header = f.readline().strip().split('\t')
        for line in f:
            parts = line.strip().split('\t')
            # Store essential fields: chrom, start, end, summit, component
            dhs_index.append({
                'chrom': parts[0],
                'start': int(parts[1]),
                'end': int(parts[2]),
                'summit': int(parts[6]),
                'component': parts[9]
            })
    
    num_dhs = len(dhs_index)
    print(f"Loaded {num_dhs} DHS sites.")
    assert nmf_matrix.shape[1] == num_dhs, "DHS Index and NMF loadings length mismatch!"
    
    # 3. Create Fast Binary Lookup Map for Inactive Background (1kb resolution)
    # This map marks regions within 5,000 bp of any DHS as True (forbidden)
    print("Building genomic exclusion map for inactive background (5kb margin around all DHSs)...")
    exclusion_map = {}
    for chrom, clen in chrom_lens.items():
        # Represent chromosome in 1kb bins (boolean array)
        num_bins = (clen // 1000) + 1
        exclusion_map[chrom] = np.zeros(num_bins, dtype=bool)
        
    for dhs in dhs_index:
        chrom = dhs['chrom']
        if chrom not in exclusion_map:
            continue
        start = dhs['start']
        end = dhs['end']
        
        # Calculate exclusion window with 5,000 bp margin
        ex_start = max(0, start - 5000)
        ex_end = end + 5000
        
        # Map to 1kb bin indices
        bin_start = ex_start // 1000
        bin_end = ex_end // 1000
        
        # Set bins to True (forbidden)
        exclusion_map[chrom][bin_start:bin_end + 1] = True
        
    print("Genomic exclusion map built successfully.")
    
    # 4. Initialize Genomic Distance Filter Tracker (2kb exclusion window)
    # Dictionary storing sorted list of selected coordinates for each chromosome
    selected_coords = {c: [] for c in std_chroms}
    
    def is_distance_safe(chrom, pos, window=2000):
        # pos is the center of the 200bp sequence (i.e. summit for DHS, or pos+100 for genomic background)
        coords = selected_coords[chrom]
        if not coords:
            return True
        # Use bisect to find neighbors
        idx = bisect.bisect_left(coords, pos)
        # Check left neighbor
        if idx > 0 and pos - coords[idx-1] < window:
            return False
        # Check right neighbor
        if idx < len(coords) and coords[idx] - pos < window:
            return False
        return True
    
    def add_selected_coord(chrom, pos):
        bisect.insort(selected_coords[chrom], pos)
        
    # Helper to validate and clean DNA sequence
    valid_dna_regex = re.compile(r'^[ACGT]+$')
    
    def fetch_clean_sequence(chrom, start, end):
        # Fetch sequence from 2bit
        try:
            seq = genome[chrom][start:end].upper()
            if len(seq) == 200 and valid_dna_regex.match(seq):
                return seq
        except Exception:
            pass
        return None

    # 5. Part 1: Sample Active DHS Elements (30,000 sequences total, 1,875 per component)
    print("Sampling 30,000 Active DHS Elements (stratified, loading-weighted, centered on summits)...")
    
    # Map components to indices
    components_mapping = {
        0: 'Tissue invariant',
        1: 'Stromal A',
        2: 'Primitive / embryonic',
        3: 'Stromal B',
        4: 'Lymphoid',
        5: 'Renal / cancer',
        6: 'Placental / trophoblast',
        7: 'Neural',
        8: 'Cardiac',
        9: 'Organ devel. / renal',
        10: 'Pulmonary devel.',
        11: 'Musculoskeletal',
        12: 'Digestive',
        13: 'Vascular / endothelial',
        14: 'Myeloid / erythroid',
        15: 'Cancer / epithelial'
    }
    
    # Pre-calculate dominant component for each DHS based on NMF argmax
    print("Calculating dominant NMF components for all DHS sites...")
    dominant_components = np.argmax(nmf_matrix, axis=0)
    
    active_sequences = []
    
    for c_idx in range(16):
        c_name = components_mapping[c_idx]
        print(f"  Processing component {c_idx}: '{c_name}'...")
        
        # Get candidates for this component
        candidates = np.where((dominant_components == c_idx))[0]
        
        # Filter for candidates on standard chromosomes
        candidates = [idx for idx in candidates if dhs_index[idx]['chrom'] in std_chroms]
        
        # Get topic loadings for these candidates
        loadings = nmf_matrix[c_idx, candidates]
        
        # Filter out candidates with zero or negative loadings
        valid_mask = loadings > 0
        candidates = np.array(candidates)[valid_mask]
        loadings = loadings[valid_mask]
        
        # Normalize loadings to form a probability distribution
        probs = loadings / np.sum(loadings)
        
        # Sample an excess of candidates to account for distance and N-character filters
        # 1,875 is the target, we sample 4,000 candidates
        sample_size = min(4000, len(candidates))
        sampled_indices = np.random.choice(candidates, size=sample_size, replace=False, p=probs)
        
        # Iterate and select 1,875 sequences
        num_selected = 0
        for idx in sampled_indices:
            dhs = dhs_index[idx]
            chrom = dhs['chrom']
            summit = dhs['summit']
            
            # 200bp window centered on the summit
            start = summit - 100
            end = summit + 100
            
            if start < 0 or end > chrom_lens[chrom]:
                continue
                
            # Distance filter (2kb from any selected)
            if not is_distance_safe(chrom, summit, window=2000):
                continue
                
            # Fetch and validate sequence (case-insensitive, uppercase, no Ns)
            seq = fetch_clean_sequence(chrom, start, end)
            if seq is not None:
                active_sequences.append(seq)
                add_selected_coord(chrom, summit)
                num_selected += 1
                if num_selected == 1875:
                    break
                    
        print(f"    Selected {num_selected} sequences for component '{c_name}'.")
        if num_selected < 1875:
            print(f"    WARNING: Could only select {num_selected} / 1875 for component '{c_name}'.")
            
    print(f"Finished active DHS sampling. Total active sequences: {len(active_sequences)}")
    
    # 6. Part 2: Sample Inactive Genomic Background (10,000 sequences)
    print("Sampling 10,000 Inactive Genomic Background Sequences...")
    genomic_neg_sequences = []
    num_genomic_neg = 0
    attempts = 0
    
    while num_genomic_neg < 10000:
        attempts += 1
        # Sample a chromosome proportional to its length
        chrom = np.random.choice(std_chroms, p=chrom_probs)
        chrom_len = chrom_lens[chrom]
        
        # Sample a random 200bp interval
        start = np.random.randint(0, chrom_len - 200)
        end = start + 200
        center = start + 100
        
        # 1. Epigenetic Silencing Check: must be at least 5kb away from any DHS
        bin_start = start // 1000
        bin_end = end // 1000
        if np.any(exclusion_map[chrom][bin_start:bin_end + 1]):
            continue
            
        # 2. Distance check: must be at least 2kb away from any already selected sequence
        if not is_distance_safe(chrom, center, window=2000):
            continue
            
        # 3. 'N'-character and canonical check
        seq = fetch_clean_sequence(chrom, start, end)
        if seq is not None:
            genomic_neg_sequences.append(seq)
            add_selected_coord(chrom, center)
            num_genomic_neg += 1
            if num_genomic_neg % 2000 == 0:
                print(f"  Selected {num_genomic_neg} genomic background sequences...")
                
    print(f"Finished genomic background sampling after {attempts} attempts. Total: {len(genomic_neg_sequences)}")
    
    # 7. Part 3: Sample Synthetic Background (10,000 sequences)
    print("Generating 10,000 Synthetic Background Sequences...")
    synthetic_sequences = set()
    bases = ['A', 'C', 'G', 'T']
    
    while len(synthetic_sequences) < 10000:
        seq = "".join(random.choices(bases, k=200))
        synthetic_sequences.add(seq)
        
    synthetic_sequences = list(synthetic_sequences)
    print(f"Finished synthetic background generation. Total: {len(synthetic_sequences)}")
    
    # 8. Merge and Shuffle
    print("Merging and shuffling all library sequences...")
    all_sequences = active_sequences + genomic_neg_sequences + synthetic_sequences
    random.shuffle(all_sequences)
    
    # 9. Final Verification
    print(f"Verifying final library of size {len(all_sequences)}...")
    assert len(all_sequences) == 50000, f"Expected exactly 50,000 sequences, got {len(all_sequences)}"
    for idx, seq in enumerate(all_sequences):
        assert len(seq) == 200, f"Sequence at index {idx} has length {len(seq)} (expected 200)"
        assert valid_dna_regex.match(seq), f"Sequence at index {idx} has invalid characters: {seq}"
        
    # 10. Write Output
    print(f"Writing sequences to {output_path}...")
    with open(output_path, 'w') as f:
        for seq in all_sequences:
            f.write(seq + "\n")
            
    print("MPRA Library Generation Complete! Sequences written successfully.")

if __name__ == '__main__':
    main()
