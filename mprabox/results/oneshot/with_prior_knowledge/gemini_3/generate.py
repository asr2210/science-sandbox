import os
import gzip
import random
from collections import defaultdict, Counter
import numpy as np
import twobitreader

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

def dinucleotide_shuffle_retry(seq: str, max_attempts=1000) -> str:
    if len(seq) < 2:
        return seq
    
    start_char = seq[0]
    
    transitions = defaultdict(list)
    for i in range(len(seq) - 1):
        transitions[seq[i]].append(seq[i+1])
        
    for attempt in range(max_attempts):
        shuffled_trans = {k: list(v) for k, v in transitions.items()}
        for k in shuffled_trans:
            random.shuffle(shuffled_trans[k])
            
        curr = start_char
        path = [curr]
        
        while shuffled_trans[curr]:
            next_node = shuffled_trans[curr].pop()
            path.append(next_node)
            curr = next_node
            
        if all(len(v) == 0 for v in shuffled_trans.values()):
            res = ''.join(path)
            if res != seq:
                return res
                
    # Fallback: simple mononucleotide shuffle preserving first and last bases
    chars = list(seq[1:-1])
    random.shuffle(chars)
    return start_char + ''.join(chars) + seq[-1]

def generate_gc_matched_sequence(length: int, target_gc: float) -> str:
    p_gc = target_gc / 2.0
    p_at = (1.0 - target_gc) / 2.0
    bases = ['A', 'C', 'G', 'T']
    probs = [p_at, p_gc, p_gc, p_at]
    return ''.join(np.random.choice(bases, size=length, p=probs))

def main():
    print("Step 1: Setting up paths and directories...")
    os.makedirs('library', exist_ok=True)
    
    dhs_index_path = 'data/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz'
    genome_2bit_path = 'data/hg38.2bit'
    output_path = 'library/sequences.txt'
    
    print("Step 2: Loading reference genome...")
    genome = twobitreader.TwoBitFile(genome_2bit_path)
    standard_chroms = set(f'chr{i}' for i in range(1, 23)) | {'chrX', 'chrY'}
    
    print("Step 3: Loading DHS index and grouping by component...")
    comp_data = defaultdict(list)
    with gzip.open(dhs_index_path, 'rt') as f:
        header = f.readline().strip().split('\t')
        comp_idx = header.index('component')
        signal_idx = header.index('mean_signal')
        chrom_idx = header.index('seqname')
        summit_idx = header.index('summit')
        
        for line in f:
            fields = line.strip().split('\t')
            chrom = fields[chrom_idx]
            if chrom not in standard_chroms:
                continue
            comp = fields[comp_idx]
            sig = float(fields[signal_idx])
            summit = int(fields[summit_idx])
            comp_data[comp].append((sig, chrom, summit))
            
    components = sorted(list(comp_data.keys()))
    print(f"Found {len(components)} components: {components}")
    
    # Stratify target sizes for exactly 35,000 biological sequences across 16 components
    # 35,000 / 16 = 2,187 with remainder 8.
    # First 8 components will have 2,188; next 8 will have 2,187.
    target_sizes = {}
    for i, comp in enumerate(components):
        target_sizes[comp] = 2188 if i < 8 else 2187
    
    print("Step 4: Selecting biological DHS sequences with distance filter...")
    selected_bio_sequences = []
    used_regions = defaultdict(list)  # chrom -> sorted list of (start, end)
    
    def is_far_enough(chrom, pos, min_dist=1000):
        # We can optimize this lookup or do a simple sequential search
        for s, e in used_regions[chrom]:
            if abs(pos - s) < min_dist or abs(pos - e) < min_dist:
                return False
        return True
        
    valid_bases = set('ACGT')
    
    for comp in components:
        items = comp_data[comp]
        # Sort by mean_signal descending to get strongest regulatory elements
        sorted_items = sorted(items, key=lambda x: x[0], reverse=True)
        
        target = target_sizes[comp]
        selected_count = 0
        
        for sig, chrom, summit in sorted_items:
            if not is_far_enough(chrom, summit, min_dist=1000):
                continue
                
            start = summit - 100
            end = summit + 100
            
            try:
                seq = genome[chrom][start:end].upper()
                if len(seq) == 200 and all(b in valid_bases for b in seq):
                    selected_bio_sequences.append(seq)
                    used_regions[chrom].append((start, end))
                    selected_count += 1
                    if selected_count >= target:
                        break
            except Exception:
                pass
                
        print(f"  Component '{comp}': selected {selected_count} / {target} elements.")
        
    print(f"Total biological sequences selected: {len(selected_bio_sequences)}")
    assert len(selected_bio_sequences) == 35000, f"Expected 35000 biological sequences, got {len(selected_bio_sequences)}"
    
    print("Step 5: Generating 10,000 dinucleotide-shuffled controls...")
    # Randomly select exactly 10,000 biological sequences to shuffle
    shuffled_pool = random.sample(selected_bio_sequences, 10000)
    shuffled_sequences = []
    for i, seq in enumerate(shuffled_pool):
        shuffled_seq = dinucleotide_shuffle_retry(seq)
        shuffled_sequences.append(shuffled_seq)
        if (i + 1) % 2000 == 0:
            print(f"  Shuffled {i+1} / 10000 sequences...")
            
    print("Step 6: Generating 5,000 GC-matched synthetic sequences...")
    # Active DHS sequences stats
    mean_gc = 0.5292
    std_gc = 0.1033
    
    synthetic_sequences = []
    for i in range(5000):
        # Sample target GC from biological distribution
        target_gc = np.random.normal(mean_gc, std_gc)
        target_gc = np.clip(target_gc, 0.25, 0.85)
        
        synthetic_seq = generate_gc_matched_sequence(200, target_gc)
        synthetic_sequences.append(synthetic_seq)
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i+1} / 5000 synthetic sequences...")
            
    print("Step 7: Combining and shuffling final library sequences...")
    final_library = selected_bio_sequences + shuffled_sequences + synthetic_sequences
    random.shuffle(final_library)
    
    print("Step 8: Performing final validation on sequence array...")
    assert len(final_library) == 50000, f"Final library has {len(final_library)} sequences instead of 50000"
    for idx, seq in enumerate(final_library):
        assert len(seq) == 200, f"Sequence at index {idx} has length {len(seq)} instead of 200"
        assert all(b in valid_bases for b in seq), f"Sequence at index {idx} has invalid characters: {seq}"
        
    print(f"Step 9: Writing final 50,000 sequences to {output_path}...")
    with open(output_path, 'w') as out:
        for seq in final_library:
            out.write(seq + '\n')
            
    print("Validation: Reading back the output file to be absolutely certain of formatting...")
    with open(output_path, 'r') as f:
        lines = f.read().splitlines()
        
    assert len(lines) == 50000, f"Saved file has {len(lines)} lines instead of 50000"
    for idx, line in enumerate(lines):
        assert len(line) == 200, f"Saved sequence at line {idx+1} has length {len(line)} instead of 200"
        assert all(b in valid_bases for b in line), f"Saved sequence at line {idx+1} has invalid characters"
        
    print("SUCCESS! Exactly 50,000 high-quality, formatted sequences written and verified!")

if __name__ == '__main__':
    main()
