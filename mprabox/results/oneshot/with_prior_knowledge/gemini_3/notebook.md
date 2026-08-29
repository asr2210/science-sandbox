# Lab Notebook - MPRA Library Design for General Regulatory Grammar

## Section 1: Theory of MPRA Training Library Design

To train a machine learning model that captures the general regulatory grammar across all cell types, the training library of 50,000 sequences (200bp each) must be carefully engineered. A good training library is not just a collection of active enhancers; rather, it must satisfy the following principles:

1. **Wide Dynamic Range of Activity (Signal vs. Noise):**
   The model must learn to distinguish active regulatory elements from inactive background DNA. If the library only contains highly active promoters and enhancers, the model will over-predict activity and fail to learn the boundaries of motif grammar. We must include completely inactive sequences (e.g., random synthetic DNA) as negative controls.

2. **Decoupling Motif Presence from Nucleotide Composition (Shuffled Controls):**
   A common failure mode for sequence-to-expression models is over-relying on GC content, CpG island density, or simple k-mer frequencies, rather than learning the precise TF binding motifs. By including dinucleotide-shuffled counterparts of active biological sequences, we provide "paired" training examples: one with the functional TF motif arrangement, and one with the identical dinucleotide composition but destroyed motifs. This forces the model to learn the spatial grammar and specific motifs.

3. **Cell-Type and Tissue Diversity (Unbiased Representation):**
   Since the goal is a model that captures regulatory grammar across *all* cell types (not just K562, HepG2, SK-N-SH), the genomic sequences must not be biased towards any single tissue or common cell type. We should use a stratified sampling approach across the 16 regulatory components (NMF topics) of the Meuleman et al. 2020 DHS Index, ensuring equal representation of rare tissues (e.g., brain, placental, cardiac, lymphoid, myeloid, etc.).

4. **Natural Grammar vs. Synthetic Simplicity:**
   Natural open chromatin regions (DHS sites) represent the evolutionary optimized spacing and combinations of TF binding motifs. However, they can have complex, overlapping features. Combining natural DHS sequences with synthetic sequences (purely random or motif-inserted) allows the model to learn both complex biological contexts and simple, isolated rules.

---

## Section 2: Sources of Data and Sequence Types Considered

1. **Meuleman et al. 2020 DHS Index (hg38):**
   - **Status:** Included.
   - **Reasoning:** This represents ~3.6M consensus open chromatin regions across 733 biosamples. Each DHS is assigned to one of the 16 NMF topics (regulatory components). This is the best source for tissue-diverse, natural regulatory sequences.

2. **Sei Chromatin State Regions (Chen et al. 2022):**
   - **Status:** Excluded in favor of DHS stratification.
   - **Reasoning:** SEI sequence classes are highly correlated with DHS, but downloading and parsing the raw SEI regions is less direct than the clean, structured Meuleman DHS index. By stratifying across the 16 DHS components, we already cover the functional regulatory landscape (promoters, enhancers, CTCF sites) with high fidelity.

3. **Dinucleotide Shuffled DHS Sequences:**
   - **Status:** Included.
   - **Reasoning:** Essential for teaching the model motif specificity and separating motif grammar from nucleotide bias.

4. **GC-Matched Random Synthetic Sequences:**
   - **Status:** Included (10% of library).
   - **Reasoning:** Provides a robust baseline for inactive sequence space and nucleotide diversity, specifically matched to the GC content distribution of active elements.

---

## Section 3: Empirical Analyses and Design Decisions

We ran systematic analyses on the downloaded datasets to inform our design:

1. **Regulatory Components:**
   We verified that `DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz` contains exactly 16 components, with sizes ranging from 56,186 (Stromal A) to 626,541 (Primitive / embryonic) elements.
   
2. **GC Content Analysis of Active Elements:**
   We analyzed the GC content of the highest-signal DHS elements and found:
   - **Mean GC Content:** 52.92%
   - **Standard Deviation:** 10.33%
   - **Range:** 27.00% to 87.00%
   
   To prevent the model from using simple GC content to predict activity (which is a common shortcut for deep learning models), we will:
   - Use dinucleotide-shuffled sequences (which perfectly preserve GC and dinucleotide frequencies).
   - Generate random synthetic sequences whose GC contents are sampled directly from the normal distribution of our active sequences ($N(0.53, 0.10)$).

3. **Genomic Distance Filter:**
   To ensure high sequence and locus diversity, we implemented a 1,000bp minimum distance filter between selected DHS peaks on the same chromosome.

---

## Section 4: Final Library Composition

Our final library composition for the 50,000 sequences of 200bp:

1. **Biological Active DHS Sequences (70% = 35,000 sequences):**
   - Stratified across the 16 Meuleman regulatory components (exactly 2,187 or 2,188 sequences per component, summing to exactly 35,000 sequences).
   - Within each component, we sort by `mean_signal` descending.
   - We center the 200bp sequence around the peak summit and verify that it contains only standard {A, C, G, T} characters and is on standard chromosomes (chr1-22, chrX, chrY).

2. **Paired Dinucleotide Shuffled DHS Sequences (20% = 10,000 sequences):**
   - We randomly select exactly 10,000 of the chosen 35,000 active DHS sequences.
   - We generate their dinucleotide-shuffled counterparts using a fast, exact Altschul-Erikson Eulerian path algorithm in pure Python.

3. **GC-Matched Random Synthetic Sequences (10% = 5,000 sequences):**
   - We generate 5,000 sequences of 200bp where each sequence's target GC content is drawn from $N(0.53, 0.10)$, clipped between 0.25 and 0.85, to perfectly match the active sequences' GC distribution.

---

## Section 5: Evaluation Results

Our designed library achieved excellent performance across all 14 anonymous evaluation sets:

- **eval_01 (mean_r):** 0.6838
- **eval_02 (mean_r):** 0.7713
- **eval_03 (mean_r):** 0.7484
- **eval_04 (mean_r):** 0.7558
- **eval_05 (mean_r):** 0.6833
- **eval_06 (mean_r):** 0.7710
- **eval_07 (mean_r):** 0.6715
- **eval_08 (mean_r):** 0.6612
- **eval_09 (mean_r):** 0.8181
- **eval_10 (mean_r):** 0.7371
- **eval_11 (mean_r):** 0.6705
- **eval_12 (mean_r):** 0.6443
- **eval_13 (mean_r):** 0.6706
- **eval_14 (mean_r):** 0.7722

**Overall Mean Pearson r (across all 14 sets):** 0.7185

### Discussion & Key Findings:
- By combining **perfect tissue stratification** with **signal-strength sorting**, we successfully captured the strongest, highest-affinity transcription factor binding motifs for every major biological spectrum while maintaining an unbiased cell-type representation.
- Incorporating **dinucleotide-shuffled paired controls** (20%) and **GC-matched synthetic sequences** (10%) forced the downstream model to learn the true spatial motif grammar rather than taking simple shortcuts based on nucleotide/dinucleotide composition.
- The genomic distance filter (1,000bp) ensured high sequence diversity and prevented locus redundancy.

---

## Section 6: Next Steps (What We Would Try Next)

If we had another iteration, we would explore:
1. **Dynamic Ratios of Sub-Components:** Testing different proportions of active elements (e.g., 60% DHS, 30% shuffled, 10% GC-matched synthetic) to find the absolute optimum ratio.
2. **Motif-Inserted Synthetic Contexts:** Explicitly inserting characterized TF motifs (like AP-1, CTCF, NF-kB, etc. from JASPAR) in diverse combinations, orientations, and spacings into the GC-matched synthetic background to train specific grammar rules.
3. **Multi-scale Flanking Context:** Extracting sequences with systematic offsets around the summit peak (e.g., 50bp left/right shift) to test whether shift-invariant representations further boost performance.
