import os
import random
import sys
import requests
from collections import defaultdict

# ----------------------------------------------------------------------
# Configuration and Constants
# ----------------------------------------------------------------------

CELL_LINES = ['K562', 'GM12878', 'HUVEC', 'HeLa-S3']

# Motif Consensus Sequences from JASPAR 2024
# These are represented as IUPAC strings.
MOTIFS = {
    # General / Ubiquitous Activators
    'AP1': 'TGASTCA',        # AP-1 (Fos-Jun)
    'SP1': 'GGGGYGGGG',      # SP1 (GC-box)
    'NFY': 'RRCCAATSR',      # NF-Y (CCAAT-box)
    'ETS': 'MGGAWGY',        # ETS
    'CREB': 'TGACGTCA',      # CREB
    
    # Tissue/Cell-type Specific Activators
    'GATA1': 'WGATAA',       # Myeloid/Blood (K562)
    'PU1': 'AGAGGAAGTG',     # Myeloid/Blood (K562) (SPI1)
    'TAL1': 'AACAGATGGT',    # Myeloid/Blood (K562)
    'HNF4A': 'RGGTCAAAGGTCA', # Liver (HepG2)
    'HNF1A': 'DGTTAATNATTAAC', # Liver (HepG2)
    'FOXA1': 'AAAWTRTTTAY',   # Liver (HepG2)
    'CEBPA': 'RTTKCNGYAAY',   # Liver (HepG2)
    'SOX2': 'CATTGTT',       # Neuronal/Brain (SK-N-SH)
    'ASCL1': 'GCAGCTGC',     # Neuronal/Brain (SK-N-SH)
    'NEUROD1': 'RCAGCTGY',   # Neuronal/Brain (SK-N-SH)
    'POU3F2': 'TATGCAAAT',   # Neuronal/Brain (SK-N-SH)
    
    # Repressors / Structural Elements
    'REST': 'TTCAGCACCWGGACAGCGCC', # Long repressor (REST/NRSF)
    'CTCF': 'CCACYAGGGGGCGCY',     # Chromatin organizer
    'YY1': 'GCCATNTT',             # Dual activator/repressor (initiator)
}

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

RC_MAP = str.maketrans('ACGT', 'TGCA')

CURATED_PAIRS = [
    ('HNF4A', 'FOXA1'), ('HNF1A', 'CEBPA'), ('HNF4A', 'HNF1A'),
    ('GATA1', 'TAL1'), ('PU1', 'GATA1'), ('PU1', 'TAL1'),
    ('SOX2', 'POU3F2'), ('ASCL1', 'SOX2'), ('NEUROD1', 'SOX2'),
    ('AP1', 'SP1'), ('ETS', 'NFY'), ('CREB', 'AP1'),
    ('AP1', 'REST'), ('GATA1', 'YY1'), ('AP1', 'CTCF')
]

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def reverse_complement(seq):
    return seq.translate(RC_MAP)[::-1]

def expand_iupac(seq):
    return "".join(random.choice(IUPAC_MAP[char]) for char in seq.upper())

def generate_background(length, gc_content):
    num_gc = int(round(length * gc_content))
    num_at = length - num_gc
    pool = ['G'] * (num_gc // 2) + ['C'] * (num_gc - num_gc // 2) + ['A'] * (num_at // 2) + ['T'] * (num_at - num_at // 2)
    random.shuffle(pool)
    return "".join(pool)

def insert_motif(bg, motif, pos, rc=False):
    motif_seq = expand_iupac(motif)
    if rc:
        motif_seq = reverse_complement(motif_seq)
    m_len = len(motif_seq)
    if pos + m_len > len(bg):
        pos = len(bg) - m_len
    new_seq = bg[:pos] + motif_seq + bg[pos+m_len:]
    return new_seq

def dinucleotide_shuffle(s):
    # Pure Python implementation of the Altschul-Erickson algorithm
    for _ in range(50):
        if len(s) < 2:
            return s
        edges = defaultdict(list)
        for i in range(len(s) - 1):
            edges[s[i]].append(s[i+1])
        
        last_char = s[-1]
        res_edges = defaultdict(list)
        exit_edges = {}
        
        for u, v_list in list(edges.items()):
            v_list = list(v_list)
            random.shuffle(v_list)
            if u != last_char:
                if len(v_list) > 0:
                    exit_edges[u] = v_list.pop()
                    res_edges[u] = v_list
            else:
                res_edges[u] = v_list

        curr = s[0]
        result = [curr]
        
        while True:
            if res_edges[curr]:
                curr = res_edges[curr].pop()
            elif curr in exit_edges:
                curr = exit_edges.pop(curr)
            else:
                break
            result.append(curr)
            
        if len(result) == len(s):
            return "".join(result)
            
    # Fallback if shuffle fails
    l = list(s)
    random.shuffle(l)
    return "".join(l)

# ----------------------------------------------------------------------
# Core Data Pipeline
# ----------------------------------------------------------------------

def download_data():
    os.makedirs('data', exist_ok=True)
    for cell in CELL_LINES:
        for name in ['enhancers', 'promoters']:
            file_path = f'data/{cell}_{name}.fasta'
            if not os.path.exists(file_path):
                print(f"Downloading {cell} {name}...", flush=True)
                url = f'https://raw.githubusercontent.com/HaoWuLab-Bioinformatics/Enhancer-MDLF/main/EPdata/{cell}/{name}.fasta'
                r = requests.get(url)
                if r.status_code == 200:
                    with open(file_path, 'w') as f:
                        f.write(r.text)
                else:
                    print(f"Failed to download {cell} {name}: {r.status_code}", flush=True)

def load_natural_sequences():
    natural_pool = []
    seen = set()
    for cell in CELL_LINES:
        for name in ['enhancers', 'promoters']:
            file_path = f'data/{cell}_{name}.fasta'
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    lines = f.read().splitlines()
                current_seq = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('>'):
                        if current_seq:
                            seq_str = "".join(current_seq).upper()
                            clean_seq = "".join([c for c in seq_str if c in 'ACGT'])
                            if len(clean_seq) >= 200:
                                start = (len(clean_seq) - 200) // 2
                                cropped = clean_seq[start:start+200]
                                if cropped not in seen:
                                    seen.add(cropped)
                                    natural_pool.append((cell, name, cropped))
                            current_seq = []
                    else:
                        current_seq.append(line)
                if current_seq:
                    seq_str = "".join(current_seq).upper()
                    clean_seq = "".join([c for c in seq_str if c in 'ACGT'])
                    if len(clean_seq) >= 200:
                        start = (len(clean_seq) - 200) // 2
                        cropped = clean_seq[start:start+200]
                        if cropped not in seen:
                            seen.add(cropped)
                            natural_pool.append((cell, name, cropped))
    print(f"Loaded {len(natural_pool)} unique natural sequences.", flush=True)
    return natural_pool

def select_natural_sequences(natural_pool):
    grouped = defaultdict(list)
    for cell, name, seq in natural_pool:
        grouped[(cell, name)].append(seq)
        
    selected = []
    for cell in CELL_LINES:
        for name in ['enhancers', 'promoters']:
            pool = grouped[(cell, name)]
            n_sample = min(2500, len(pool))
            selected.extend(random.sample(pool, n_sample))
            print(f"Sampled {n_sample} from {cell} {name}.", flush=True)
            
    return selected

# ----------------------------------------------------------------------
# Synthetic Library Generators
# ----------------------------------------------------------------------

def generate_shuffled_controls(natural_selected, count=5000):
    sampled = random.sample(natural_selected, count)
    shuffled = []
    for seq in sampled:
        shuffled.append(dinucleotide_shuffle(seq))
    print(f"Generated {len(shuffled)} dinucleotide-shuffled control sequences.", flush=True)
    return shuffled

def generate_positional_scans(count=5000):
    scans = []
    positions = [10, 25, 40, 55, 70, 85, 100, 115, 130, 145, 160, 175]
    motif_keys = list(MOTIFS.keys())
    
    while len(scans) < count:
        motif_key = random.choice(motif_keys)
        motif = MOTIFS[motif_key]
        pos = random.choice(positions)
        rc = random.choice([True, False])
        gc = random.choice([0.3, 0.4, 0.5, 0.6, 0.7])
        bg = generate_background(200, gc)
        seq = insert_motif(bg, motif, pos, rc)
        scans.append(seq)
    print(f"Generated {len(scans)} positional scan sequences.", flush=True)
    return scans

def generate_homotypic_clusters(count=5000):
    clusters = []
    motif_keys = list(MOTIFS.keys())
    
    while len(clusters) < count:
        motif_key = random.choice(motif_keys)
        motif = MOTIFS[motif_key]
        n_copies = random.choice([1, 2, 3, 4, 5])
        spacing = random.choice([5, 10, 15, 20, 25, 30])
        gc = random.choice([0.3, 0.4, 0.5, 0.6, 0.7])
        bg = generate_background(200, gc)
        
        motif_len = len(motif)
        total_len = n_copies * motif_len + (n_copies - 1) * spacing
        if total_len > 180:
            n_copies = max(1, 180 // (motif_len + spacing))
            total_len = n_copies * motif_len + (n_copies - 1) * spacing
            
        start_pos = random.randint(10, max(11, 190 - total_len))
        
        seq = bg
        for i in range(n_copies):
            pos = start_pos + i * (motif_len + spacing)
            rc = random.choice([True, False])
            seq = insert_motif(seq, motif, pos, rc)
            
        clusters.append(seq)
    print(f"Generated {len(clusters)} homotypic cooperativity sequences.", flush=True)
    return clusters

def generate_heterotypic_pairs(count=10000):
    pairs = []
    motif_keys = list(MOTIFS.keys())
    
    while len(pairs) < count:
        if random.random() < 0.5:
            tf_a, tf_b = random.choice(CURATED_PAIRS)
        else:
            tf_a = random.choice(motif_keys)
            tf_b = random.choice(motif_keys)
            while tf_a == tf_b:
                tf_b = random.choice(motif_keys)
                
        motif_a = MOTIFS[tf_a]
        motif_b = MOTIFS[tf_b]
        
        spacing = random.choice([5, 10, 15, 20, 30, 45, 60, 80])
        gc = random.choice([0.3, 0.4, 0.5, 0.6, 0.7])
        bg = generate_background(200, gc)
        
        total_len = len(motif_a) + len(motif_b) + spacing
        if total_len > 180:
            spacing = max(5, 180 - len(motif_a) - len(motif_b))
            total_len = len(motif_a) + len(motif_b) + spacing
            
        start_pos = random.randint(10, max(11, 190 - total_len))
        
        rc_a = random.choice([True, False])
        rc_b = random.choice([True, False])
        
        seq = insert_motif(bg, motif_a, start_pos, rc_a)
        pos_b = start_pos + len(motif_a) + spacing
        seq = insert_motif(seq, motif_b, pos_b, rc_b)
        
        pairs.append(seq)
        
    print(f"Generated {len(pairs)} heterotypic cooperativity sequences.", flush=True)
    return pairs

def generate_billboards(count=5000):
    billboards = []
    motif_keys = list(MOTIFS.keys())
    
    while len(billboards) < count:
        n_motifs = random.choice([3, 4, 5])
        selected_keys = random.sample(motif_keys, n_motifs)
        selected_motifs = [MOTIFS[k] for k in selected_keys]
        
        gc = random.choice([0.3, 0.4, 0.5, 0.6, 0.7])
        bg = generate_background(200, gc)
        
        tot_m_len = sum(len(m) for m in selected_motifs)
        rem_space = 200 - tot_m_len
        if rem_space < n_motifs * 5:
            n_motifs = 3
            selected_keys = random.sample(motif_keys, n_motifs)
            selected_motifs = [MOTIFS[k] for k in selected_keys]
            tot_m_len = sum(len(m) for m in selected_motifs)
            rem_space = 200 - tot_m_len
            
        spacers = []
        for _ in range(n_motifs + 1):
            spacers.append(random.randint(2, 20))
        sum_sp = sum(spacers)
        if sum_sp > 0:
            spacers = [int(s * rem_space / sum_sp) for s in spacers]
        else:
            spacers = [rem_space // (n_motifs + 1)] * (n_motifs + 1)
        
        diff = rem_space - sum(spacers)
        spacers[0] += diff
        
        pos = spacers[0]
        seq = bg
        for i in range(n_motifs):
            rc = random.choice([True, False])
            seq = insert_motif(seq, selected_motifs[i], pos, rc)
            pos += len(selected_motifs[i]) + spacers[i+1]
            
        billboards.append(seq)
        
    print(f"Generated {len(billboards)} billboard enhancer sequences.", flush=True)
    return billboards

# ----------------------------------------------------------------------
# Main Orchestration
# ----------------------------------------------------------------------

def main():
    print("Starting MPRA sequence library generation...", flush=True)
    random.seed(42) # For reproducibility
    
    # 1. Download data
    download_data()
    
    # 2. Load natural promoter/enhancer sequences
    natural_pool = load_natural_sequences()
    natural_selected = select_natural_sequences(natural_pool)
    
    # 3. Generate shuffled controls
    shuffled_controls = generate_shuffled_controls(natural_selected)
    
    # 4. Generate synthetic categories
    positional_scans = generate_positional_scans()
    homotypic_clusters = generate_homotypic_clusters()
    heterotypic_pairs = generate_heterotypic_pairs()
    billboards = generate_billboards()
    
    # Combine all sequences
    all_sequences = []
    all_sequences.extend(natural_selected)
    all_sequences.extend(shuffled_controls)
    all_sequences.extend(positional_scans)
    all_sequences.extend(homotypic_clusters)
    all_sequences.extend(heterotypic_pairs)
    all_sequences.extend(billboards)
    
    print(f"Combined total sequences before deduplication: {len(all_sequences)}", flush=True)
    
    # Deduplicate and filter
    unique_seqs = []
    seen = set()
    for s in all_sequences:
        s = s.upper()
        if len(s) == 200 and all(c in 'ACGT' for c in s):
            if s not in seen:
                seen.add(s)
                unique_seqs.append(s)
                
    print(f"Total unique, valid sequences: {len(unique_seqs)}", flush=True)
    
    # Fill library if less than 50,000
    if len(unique_seqs) < 50000:
        print(f"Filling the library to exactly 50,000 sequences...", flush=True)
        needed = 50000 - len(unique_seqs)
        extra_billboards = generate_billboards(needed * 2)
        for s in extra_billboards:
            s = s.upper()
            if len(s) == 200 and all(c in 'ACGT' for c in s):
                if s not in seen:
                    seen.add(s)
                    unique_seqs.append(s)
                    if len(unique_seqs) == 50000:
                        break
                        
    # Truncate if greater than 50,000
    if len(unique_seqs) > 50000:
        unique_seqs = unique_seqs[:50000]
        
    print(f"Final library size: {len(unique_seqs)}", flush=True)
    
    # Final sanity check on all sequences
    for idx, s in enumerate(unique_seqs):
        if len(s) != 200:
            raise ValueError(f"Sequence {idx} length is {len(s)} instead of 200")
        for char in s:
            if char not in 'ACGT':
                raise ValueError(f"Sequence {idx} contains invalid character {char}")
                
    # Save to library/sequences.txt
    os.makedirs('library', exist_ok=True)
    output_path = 'library/sequences.txt'
    with open(output_path, 'w') as f:
        for s in unique_seqs:
            f.write(s + '\n')
            
    print(f"Successfully generated exactly 50,000 200bp sequences in {output_path}!", flush=True)

if __name__ == '__main__':
    main()
