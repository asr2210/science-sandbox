#!/usr/bin/env python3
import os
import sys
import gzip
import json
import time
import random
import requests

# Set random seed for reproducibility
random.seed(42)

# Define constants
CCRE_FILE = "data/ENCFF924IMH.bed.gz"
OUTPUT_DIR = "library"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "sequences.txt")

# Category target counts
TARGETS = {
    "PLS": 15000,
    "pELS": 15000,
    "dELS": 10000,
    "CTCF": 2500,
    "DNase-H3K4me3": 2500
}

# Supported chromosomes (exclude patches/scaffolds)
VALID_CHRS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

def parse_ccre_regions():
    """Reads cCRE elements from the compressed bed file and groups them by category."""
    print(f"Parsing ENCODE cCRE registry file: {CCRE_FILE}...")
    
    categories = {
        "PLS": [],
        "pELS": [],
        "dELS": [],
        "CTCF": [],
        "DNase-H3K4me3": []
    }
    
    with gzip.open(CCRE_FILE, "rt") as f:
        for idx, line in enumerate(f):
            parts = line.strip().split("\t")
            if len(parts) < 10:
                continue
                
            chrom = parts[0]
            if chrom not in VALID_CHRS:
                continue
                
            # Strip 'chr' for Ensembl compatibility
            ensembl_chrom = chrom.replace("chr", "")
            
            try:
                start = int(parts[1])
                end = int(parts[2])
            except ValueError:
                continue
                
            ccre_type = parts[9]
            
            # Map sub-classes to their parent category
            if "PLS" in ccre_type:
                categories["PLS"].append((ensembl_chrom, start, end))
            elif "pELS" in ccre_type:
                categories["pELS"].append((ensembl_chrom, start, end))
            elif "dELS" in ccre_type:
                categories["dELS"].append((ensembl_chrom, start, end))
            elif "CTCF-only" in ccre_type:
                categories["CTCF"].append((ensembl_chrom, start, end))
            elif "DNase-H3K4me3" in ccre_type:
                categories["DNase-H3K4me3"].append((ensembl_chrom, start, end))
                
    for cat, regions in categories.items():
        print(f"  - Category '{cat}': found {len(regions)} eligible elements")
        
    return categories

def create_candidate_regions(regions, count_needed):
    """Shuffles and creates 200bp region coordinates centered on each cCRE element."""
    random.shuffle(regions)
    
    # We take a buffer of candidate regions to account for filtering/errors
    buffer_factor = 1.25
    candidates_to_take = int(count_needed * buffer_factor)
    selected_regions = regions[:candidates_to_take]
    
    formatted_regions = []
    for chrom, start, end in selected_regions:
        center = (start + end) // 2
        seq_start = center - 100
        seq_end = center + 99
        if seq_start < 1:
            continue
        formatted_regions.append(f"{chrom}:{seq_start}..{seq_end}:1")
        
    return formatted_regions

def is_valid_sequence(seq):
    """Validates that a sequence is exactly 200bp and contains only A, C, G, T."""
    if len(seq) != 200:
        return False
    # Only allow uppercase canonical bases
    return all(char in "ACGT" for char in seq)

def fetch_sequences_batch(regions_batch):
    """Sends a batch of coordinates to the Ensembl REST API and returns sequences."""
    server = "https://rest.ensembl.org"
    ext = "/sequence/region/human"
    headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json"
    }
    data = {"regions": regions_batch}
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(server + ext, headers=headers, data=json.dumps(data), timeout=30)
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = float(response.headers.get("Retry-After", 1.0))
                print(f"    [Rate Limited] Sleeping for {retry_after}s...", file=sys.stderr)
                time.sleep(retry_after)
                continue
                
            if not response.ok:
                print(f"    [Warning] Request failed (HTTP {response.status_code}): {response.text}", file=sys.stderr)
                return []
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"    [Exception] Connection error: {e}. Retrying {attempt+1}/{max_retries}...", file=sys.stderr)
            time.sleep(2.0)
            
    print("    [Error] Maximum retries exceeded for this batch.", file=sys.stderr)
    return []

def retrieve_sequences_for_category(category, candidates, target_count):
    """Fetches sequences for a category until the target count is satisfied."""
    print(f"Retrieving {target_count} sequences for category '{category}'...")
    
    valid_sequences = []
    batch_size = 50
    candidate_idx = 0
    
    while len(valid_sequences) < target_count and candidate_idx < len(candidates):
        batch = candidates[candidate_idx : candidate_idx + batch_size]
        candidate_idx += batch_size
        
        if not batch:
            break
            
        # Fetch batch
        results = fetch_sequences_batch(batch)
        time.sleep(0.07)  # Proactive polite throttling
        
        added_count = 0
        for item in results:
            seq = item.get("seq", "").upper()
            if is_valid_sequence(seq):
                if len(valid_sequences) < target_count:
                    valid_sequences.append(seq)
                    added_count += 1
                    
        print(f"  Progress: {len(valid_sequences)}/{target_count} retrieved ({added_count} added from current batch)")
        
    if len(valid_sequences) < target_count:
        print(f"  [Warning] Could only retrieve {len(valid_sequences)} valid sequences for '{category}' (target: {target_count})", file=sys.stderr)
        
    return valid_sequences

def generate_synthetic_sequences(count):
    """Generates random i.i.d. uniform 200bp synthetic sequences."""
    print(f"Generating {count} synthetic random sequences...")
    synthetic = []
    for _ in range(count):
        seq = "".join(random.choice("ACGT") for _ in range(200))
        synthetic.append(seq)
    return synthetic

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Step 1: Parse the ENCODE cCRE file
    ccre_by_cat = parse_ccre_regions()
    
    # Step 2: Retrieve biological sequences across all categories
    all_biological_sequences = []
    for category, target in TARGETS.items():
        candidates = create_candidate_regions(ccre_by_cat[category], target)
        fetched = retrieve_sequences_for_category(category, candidates, target)
        all_biological_sequences.extend(fetched)
        
    # Check if we have enough biological sequences (45,000)
    expected_biological_count = sum(TARGETS.values())
    if len(all_biological_sequences) < expected_biological_count:
        deficit = expected_biological_count - len(all_biological_sequences)
        print(f"[Warning] Deficit of {deficit} biological sequences. Will compensate with extra synthetic sequences.")
        synthetic_count = 5000 + deficit
    else:
        synthetic_count = 5000
        
    # Step 3: Generate synthetic random sequences
    synthetic_sequences = generate_synthetic_sequences(synthetic_count)
    
    # Step 4: Combine and shuffle
    final_sequences = all_biological_sequences + synthetic_sequences
    random.shuffle(final_sequences)
    
    # Step 5: Assertions and validation
    print("Validating final sequence library...")
    assert len(final_sequences) == 50000, f"Error: Library size is {len(final_sequences)}, expected exactly 50,000."
    
    for i, seq in enumerate(final_sequences):
        assert len(seq) == 200, f"Error: Sequence at index {i} has length {len(seq)}, expected exactly 200."
        assert all(c in "ACGT" for c in seq), f"Error: Sequence at index {i} contains invalid characters: {seq}"
        
    unique_count = len(set(final_sequences))
    print(f"Validation successful:")
    print(f"  - Total sequences: {len(final_sequences)}")
    print(f"  - Unique sequences: {unique_count} ({unique_count/len(final_sequences)*100:.2f}%)")
    print(f"  - Sequence length: 200 bp")
    
    # Step 6: Save sequences
    print(f"Writing sequences to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w") as f:
        for seq in final_sequences:
            f.write(seq + "\n")
            
    print("Sequence generation complete!")

if __name__ == "__main__":
    main()
