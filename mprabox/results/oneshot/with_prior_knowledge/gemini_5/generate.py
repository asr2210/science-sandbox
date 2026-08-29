#!/usr/bin/env python3
"""
generate.py - MPRA Library Generator
Generates an optimized, highly functional, and diverse 50,000-sequence MPRA library.
Stratified across 16 biological components (cell-type programs) from the Meuleman et al. (2020) DHS index.
For each component, the top 3,125 highest-signal, non-overlapping, QC-passed peaks are selected.
"""

import os
import sys
import gzip
import pandas as pd
import numpy as np

# Paths
DHS_INDEX_PATH = '/data/users/arao/mpra_autoresearch/data/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz'
GENOME_DIR = '/data/users/arao/mpra_autoresearch/data/'
OUTPUT_DIR = 'library'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'sequences.txt')

# Caching for loaded chromosome sequences
chrom_seqs = {}

def get_sequence(chrom, start, end):
    """Loads and caches chromosome fasta, and returns the requested substring."""
    if chrom not in chrom_seqs:
        fasta_path = os.path.join(GENOME_DIR, f'{chrom}.fa')
        if not os.path.exists(fasta_path):
            print(f'Warning: Chromosome file not found at {fasta_path}. Skipping.', file=sys.stderr)
            return None
        print(f'Loading chromosome {chrom} into memory...', file=sys.stderr)
        with open(fasta_path, 'r') as f:
            f.readline() # Skip header
            # Read sequence, remove newlines, and convert to uppercase
            chrom_seqs[chrom] = f.read().replace('\n', '').upper()
    
    seq = chrom_seqs[chrom][start:end]
    return seq

def passes_qc(seq):
    """Applies biological and technical quality control (QC) filters."""
    # Ensure exact length of 200bp
    if len(seq) != 200:
        return False
        
    # Ensure only standard ACGT characters
    if not all(c in 'ACGT' for c in seq):
        return False
        
    # Limit GC content between 20% and 80% inclusive
    gc_content = (seq.count('C') + seq.count('G')) / 200.0
    if gc_content < 0.20 or gc_content > 0.80:
        return False
        
    # Exclude sequences with long homopolymer runs (>= 13bp) to avoid synthesis errors
    for base in 'ACGT':
        if base * 13 in seq:
            return False
            
    return True

def main():
    print('Starting MPRA library generation...', file=sys.stderr)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load columns of interest from the DHS index
    print('Loading Meuleman et al. (2020) DHS index...', file=sys.stderr)
    cols = ['seqname', 'start', 'end', 'mean_signal', 'summit', 'component']
    with gzip.open(DHS_INDEX_PATH, 'rt') as f:
        df = pd.read_csv(f, sep='\t', usecols=cols)
    print(f'Successfully loaded {len(df):,} total DHS peaks.', file=sys.stderr)
    
    # Sort the peaks by mean_signal descending to prioritize highest active regions
    print('Sorting peaks by mean_signal descending...', file=sys.stderr)
    df_sorted = df.sort_values(by='mean_signal', ascending=False)
    
    # Setup selection trackers
    components = df['component'].unique()
    print(f'Identified {len(components)} biological components for stratification:', file=sys.stderr)
    for comp in sorted(components):
        print(f' - {comp}', file=sys.stderr)
        
    target_per_component = 3125
    selected_by_component = {comp: [] for comp in components}
    
    # Deduplication map to prevent selecting overlapping regions (chrom -> list of selected (start, end))
    selected_regions = {}
    
    def overlaps(chrom, start, end):
        if chrom not in selected_regions:
            return False
        for s, e in selected_regions[chrom]:
            if max(start, s) < min(end, e):
                return True
        return False
        
    print('\nSelecting optimized sequences from each cell-type program...', file=sys.stderr)
    processed_count = 0
    
    for idx, row in df_sorted.iterrows():
        comp = row['component']
        
        # Check if we already reached our quota for this component
        if len(selected_by_component[comp]) >= target_per_component:
            continue
            
        chrom = row['seqname']
        summit = int(row['summit'])
        start = summit - 100
        end = summit + 100
        
        if start < 0:
            continue
            
        # Ensure no overlap with previously selected intervals
        if overlaps(chrom, start, end):
            continue
            
        # Extract sequence
        seq = get_sequence(chrom, start, end)
        if seq is None:
            continue
            
        # Apply QC filters
        if not passes_qc(seq):
            continue
            
        # Add to selected pool
        selected_by_component[comp].append(seq)
        
        # Mark region as occupied
        if chrom not in selected_regions:
            selected_regions[chrom] = []
        selected_regions[chrom].append((start, end))
        
        processed_count += 1
        if processed_count % 1000 == 0:
            print(f'Selected {processed_count} total sequences...', file=sys.stderr)
            
        # Check if all components are full
        all_full = True
        for c in components:
            if len(selected_by_component[c]) < target_per_component:
                all_full = False
                break
        if all_full:
            print('All components successfully filled!', file=sys.stderr)
            break
            
    # Final check of counts
    print('\n--- Selection Summary ---', file=sys.stderr)
    total_sequences = 0
    final_sequences_list = []
    
    for comp in sorted(components):
        count = len(selected_by_component[comp])
        print(f'{comp}: {count:,} sequences selected.', file=sys.stderr)
        total_sequences += count
        final_sequences_list.extend(selected_by_component[comp])
        
    print(f'Total sequences: {total_sequences:,}', file=sys.stderr)
    
    if total_sequences != 50000:
        print(f'Error: Expected exactly 50,000 sequences, but selected {total_sequences}.', file=sys.stderr)
        sys.exit(1)
        
    # Write sequences to the output file (one per line)
    print(f'Saving exactly 50,000 sequences to {OUTPUT_FILE}...', file=sys.stderr)
    with open(OUTPUT_FILE, 'w') as out_f:
        for seq in final_sequences_list:
            out_f.write(f'{seq}\n')
            
    print('MPRA library generation completed successfully!', file=sys.stderr)

if __name__ == '__main__':
    main()
