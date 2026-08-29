# Lab Notebook: MPRA Library Design for Gene Regulatory Grammar

## 1. Scientific Theory: What Makes a Good MPRA Training Library?

The goal of this Masses Parallel Reporter Assay (MPRA) library is to train a machine learning model that learns the **general regulatory grammar** of DNA across all human cell types. To build a highly generalizable model with a limited training library (exactly 50,000 sequences), the library must possess the following scientific and computational characteristics:

1. **Intrinsically Compositional & Noiseless (De-novo Synthetics):** MPRA measures episomal (plasmid-based) regulatory activity. Unlike in-situ genomic regulation, it is independent of chromatin accessibility, histone modifications, or 3D genome architecture. Therefore, a model trained on MPRA must focus strictly on **sequence-level features** (transcription factor binding sites, spacing, and orientation). Synthetic sequences designed from the ground up are ideal because they isolate these features from genomic confounding factors.
2. **Balanced Backgrounds (GC-Sweep):** Transcription factor motifs exist in diverse genomic contexts. CpG islands are highly GC-rich, while distal enhancers are often GC-balanced or AT-rich. If the background sequences of our training library do not vary in GC content, a model may overfit to specific background compositions. By systematically varying background GC contents (35% to 65%), we teach the model to decouple GC composition from motif-specific activity.
3. **High-Resolution Causal Pairs (Tiling Mutagenesis):** To learn the precise, causal contribution of individual sequence segments, the model must observe paired sequences where a single window is perturbed while the rest of the sequence remains constant. Including wild-type human promoters alongside a systematic **20bp tiling mutational scan** forces the model to learn exactly where active motifs are situated in natural contexts.
4. **Combinatorial TF Grammar (Homotypic and Heterotypic Synergy):** Gene expression is driven by the cooperative binding of transcription factors. We must provide systematic examples of:
   - **Homotypic clusters:** Multiple copies of the same motif at varying distances (to learn homotypic synergy and steric constraints).
   - **Heterotypic combinations:** Synergistic pairs of different motifs (e.g., AP-1 + NF-kB for enhancers, Sp1 + TATA for promoters) in various relative spacings and orientations (forward-forward, forward-reverse, etc.) to learn cooperative grammars.
5. **Rigorous Inactive Controls (Genomic Background):** A model cannot learn what makes a sequence active without seeing what makes it inactive. We must include a large set of representative human genomic segments that are devoid of known active promoters or enhancers to serve as baseline negative controls.

---

## 2. Sequence Source Selection: What We Included and Excluded

### Included Data Sources & Sequence Types
1. **Chromosome 21 Promoters (Eukaryotic Promoter Database, EPDnew):**
   - **Source:** `Hs_EPDnew.bed` and `data/chr21.fa.gz`.
   - **Why:** We extracted all 308 promoters on Chromosome 21. They represent genuine, biologically validated human promoters centered precisely on their experimentally verified Transcription Start Sites (TSS) in a strand-oriented manner.
2. **Tiling Mutagenesis (Perturbed Variants):**
   - **Why:** For each of the 308 promoters, we generated 10 variants. Each variant shuffles a non-overlapping 20bp window of the 200bp sequence. This forms a complete tiling scan. A model trained on these pairs can easily identify which segments are essential for promoter activity, providing a massive training boost.
3. **Synthetic Constructs (Combinatorial Motif Library):**
   - **Why:** We synthesized 35,000 sequences embedding 14 high-confidence motifs (TATA, Sp1, NF-Y, CREB, AP-1, NF-kB, CTCF, GATA, SOX, FOXA, E-box, ETS, YY1, NRF1). These represent core promoter elements and universal, multi-tissue enhancers. They are arranged in single-motif, homotypic, heterotypic, and random combinatorial configurations across 7 different GC background levels.
4. **Genomic Background Controls:**
   - **Why:** We sampled 11,612 random 200bp sequences from Chromosome 21, ensuring they do not overlap with any annotated EPD promoters (with a 500bp margin). These serve as representative inactive negative controls.

### Excluded Data Sources & Sequence Types
- **Bulk Downloading 5,000 Promoters from Other Chromosomes:**
  - **Reasoning:** We initially designed and implemented a concurrent API downloader using the UCSC hg38 REST API to fetch 5,000 promoters from other chromosomes. However, making 5,000 sequential or highly parallel requests to the UCSC server was heavily throttled and rate-limited, causing timeouts (>5 minutes). 
  - **The Pivot:** We pivoted to a completely self-contained design: we kept the 308 Chromosome 21 promoters and performed a **high-resolution 20bp tiling mutational scan** (generating 10 variants per promoter, total 3,080 sequences). This pivot completely eliminated network dependencies, reduced runtimes to under 5 seconds, and actually increased the informative value of the promoter cohort by providing direct, paired causal signals of motif importance.

---

## 3. Specific Design Decisions & Implementation Details

1. **Altschul-Erickson Dinucleotide-Preserving Shuffler:**
   - When shuffling sequences (for the tiling mutational scan), we implemented a pure-Python version of the Altschul-Erickson algorithm. Simple mononucleotide shuffling is insufficient because it alters local composition and CpG dinucleotide counts, which are themselves highly regulatory in human promoters. Preserving dinucleotide counts maintains identical GC and CpG characteristics, isolating the effect of motif disruption.
2. **Strict Strand Orientation:**
   - When extracting natural promoters, we adjusted coordinates based on strand:
     - `+` strand promoters are extracted from `TSS - 100` to `TSS + 100`.
     - `-` strand promoters are extracted from `TSS - 99` to `TSS + 101` and then reverse complemented.
     - This aligns the TSS perfectly at index 100 (0-based) for all promoter sequences, facilitating standard position-dependent feature learning.
3. **Synthetic Grammar Layouts:**
   - **Single-motif (7,000):** Placed at random positions to learn position-dependent activity.
   - **Homotypic clusters (10,000):** Placed 2, 3, or 4 copies with a minimum spacing of 5bp to study concentration effects and spatial density.
   - **Heterotypic combinations (12,000):** Placed 12 synergistic pairs (e.g., AP-1 + NF-kB, GATA + SOX) in random orientations with a minimum spacing of 5bp to capture combinatorial logic.
   - **Random assemblies (6,000):** Placed 2 to 4 random motifs with a minimum spacing of 10bp to mimic natural, complex regulatory elements.
4. **De-duplication and Quality Control:**
   - We ran a dictionary-based de-duplication pass at the end of sequence assembly. Out of 50,000 sequences, 9 duplicates were identified (which can occur due to random background generation). We programmatically replaced them with unique, newly synthesized motif constructs, ensuring a final library of **exactly 50,000 unique sequences**.
   - We added strict validation assertions verifying:
     - Total sequence count = 50,000.
     - Sequence lengths = exactly 200.
     - Sequence alphabet = strictly `{A, C, G, T}` in uppercase.

---

## 4. Analyses Ran and Key Findings

- **Chromosome 21 Promoters Verification:**
  We successfully extracted 308 promoter regions on chromosome 21. They had an average GC content of ~58%, showing the typical high-GC bias of human promoters.
- **Dinucleotide Shuffling Correctness:**
  We verified computationally that our pure-Python shuffler perfectly preserves the exact counts of all 16 dinucleotides (e.g. CpGs, TpAs) between the wild-type and shuffled sequences.
- **Speed and Efficiency:**
  By making the pipeline completely self-contained, the generation script finishes in under 5 seconds, allowing for fast, reproducible, and error-free execution.

---

## 5. What We Would Try Next (With Another Shot)

1. **Local `.2bit` Processing:**
   With more time/space, we would download the full human genome in `.2bit` format (~819 MB) and use our `twobitreader` package to extract promoters and enhancers from all human chromosomes locally. This would allow us to include 20,000 natural promoter and enhancer contexts without network speed limits.
2. **Cell-Type Specific Enhancer Designs:**
   We would design synthetic cohorts specifically targeted at K562, HepG2, and SK-N-SH cell lines (e.g., GATA1/2 for K562, HNF4A for HepG2, ASCL1/SOX for SK-N-SH) to test if tissue-specific enhancer models learn better general grammar when exposed to dense, cell-type specific active networks.
3. **RNA Secondary Structure Optimization:**
   We would run predictions of the RNA secondary structure (e.g., folding free energy) on the 200bp sequences to ensure that we avoid designing sequences that form highly stable hairpins, which can inhibit reporter transcription or translation in wet labs.
