# Lab Notebook: MPRA Library Design

## 1. Theory of What Makes a Good MPRA Training Library

The primary objective of this Masses Parallel Reporter Assay (MPRA) library is to train a model of gene regulatory activity that generalizes across **ALL cell types**, rather than being specific to any individual cell line. 

To achieve high training performance-to-size ratio (using exactly 50,000 sequences of 200bp), the designed library must satisfy several theoretical criteria:

1. **High Concentration of Functional Sequence Grammar (High Signal-to-Noise):** Fully random synthetic sequences (e.g. uniform i.i.d. {A,C,G,T}) are mostly inactive in eukaryotic cells. While a small fraction of random sequences is helpful to establish the model's baseline "noise/background floor," too much random sequence wastes valuable library capacity. Instead, the library should be enriched for sequences that contain real, functional regulatory elements (promoters and enhancers) with high affinity for human transcription factors (TFs).
2. **Cell-Type/Tissue Program Diversity:** To train a model that generalizes across all tissues, the library must contain sequences that represent a comprehensive and diverse set of regulatory programs. If the library is heavily biased towards ubiquitous, housekeeping, or cell-line-specific elements (e.g., only active in K562), the model will fail to learn the regulatory grammar of tissue-specific transcription factors. A uniform, stratified representation across major developmental lineages and tissue programs is essential.
3. **High Signal Strength & Quality (Robustness):** Highly accessible genomic regions with strong experimental signals have well-defined, robust TF binding site combinations and high-affinity motifs. Training a model on these high-confidence functional peaks is far more effective than training on weak, low-signal, or ambiguous regions that could represent genomic noise.
4. **Precise Sequence Alignment (Center-Alignment on Summits):** Transcription factor binding site clusters are typically located at the center of chromatin accessibility peaks. If we extract arbitrary 200bp windows from open chromatin regions, we risk cutting off or splitting key regulatory motifs. Centering the 200bp window precisely at the **peak summit** maximizes the integrity of the active cis-regulatory element.

---

## 2. Sources of Data and Sequence Types Considered

We comprehensively evaluated public biological datasets available in the environment to choose our source material:

### Included:
* **Meuleman et al. (2020) DHS Index & Vocabulary (hg38):**
  * **Why included:** This dataset is a master list of ~3.59 million DNase Hypersensitivity Sites (DHS) across 733 human biosamples, representing the comprehensive open-chromatin landscape of human biology. Crucially, the authors applied Non-negative Matrix Factorization (NMF) to classify each peak into one of 16 physiological components (tissue/cell-type accessibility programs), including a `Tissue invariant` program (housekeeping) and 15 highly tissue-specific programs (e.g., `Neural`, `Lymphoid`, `Myeloid / erythroid`, `Cardiac`, `Primitive / embryonic`). This allows us to perform precise **physiological stratification**, ensuring the model learns the regulatory grammar of all cell types.
  * **How we use it:** We select the top highest-signal, robust peaks from each of the 16 components to guarantee both active sequence grammar and diverse cellular program coverage.

### Excluded:
* **Fully Random Synthetic Sequences:**
  * **Why excluded:** Analysis of prior baseline strategies (Table 1 & 2) shows that adding 50% synthetic sequences (`dhs_synth`) leads to slightly lower performance than pure DHS-based sequences (`dhs_topic`), and fully random sequences (`synth_oracle`) establish a low coverage floor. Our objective is to maximize the training performance-to-size ratio of 50k sequences, so we dedicate 100% of our capacity to real, high-signal, biological sequences.
* **ENCODE candidate Cis-Regulatory Elements (cCREs):**
  * **Why excluded:** Although ENCODE cCREs are highly curated, they lack the 16-component cell-type program annotations present in the Meuleman et al. DHS Index. Sampling from cCREs without these annotations risks introducing heavy cell-line bias (over-representing well-studied cell lines like K562/GM12878). The Meuleman DHS index is a superior backbone for cell-type program stratification.
* **Prior MPRA Datasets:**
  * **Why excluded:** These datasets represent a constrained subset of the sequence space and have already been selected under the biases of prior experiments, which limits generalization.

---

## 3. Specific Design Decisions and Reasoning

Our library consists of exactly 50,000 sequences of 200bp, designed with the following decisions:

1. **Cell-Type Program Stratified Sampling (16 Components):**
   * We divide the library into 16 balanced cohorts corresponding to the 16 NMF components from the Meuleman et al. dataset.
   * We select exactly **3,125 sequences from each of the 16 components** (16 * 3,125 = 50,000).
   * **Reasoning:** This guarantees that the model receives exactly equal exposure (6.25% of the library) to every major lineage and tissue-specific program (as well as the ubiquitous housekeeping program), preventing bias and maximizing cross-cell-type generalization.
2. **Deterministic High-Signal Selection:**
   * Within each of the 16 components, we sort all candidate peaks by `mean_signal` in descending order and select the top peaks.
   * **Reasoning:** In contrast to random or proportional sampling (which can select weak or inactive peaks), choosing the top peaks ensures that every single sequence in our 50,000 library is a robust, high-affinity functional element with clean sequence grammar.
3. **Peak-Summit Centered Windows (200bp):**
   * For each selected peak, we define the 200bp window as `[summit - 100, summit + 100]` where `summit` is the exact base coordinate of the accessibility peak summit.
   * **Reasoning:** This places the core TF binding site cluster precisely at the center of our 200bp sequence, keeping the functional motifs fully intact.
4. **Strict Genomic Deduplication (Non-Overlapping):**
   * We ensure that no two selected sequences overlap in coordinates. If a candidate peak overlaps with an already selected region, we skip it.
   * **Reasoning:** Wastes no library capacity on duplicate or redundant sequence segments.
5. **Rigorous Quality Control (QC) Filters:**
   * **No 'N' characters:** Any sequence containing 'N' is discarded.
   * **Homopolymer filter:** We discard any sequence containing a homopolymer run of length 13 or greater (e.g., `A*13`, `C*13`, `G*13`, `T*13`).
   * **GC content filter:** We restrict GC content to be between 20% and 80% inclusive.
   * **Reasoning:** These filters eliminate low-complexity noise, and conform to the standard technical constraints of high-throughput DNA synthesis and sequencing.

---

## 4. Analyses Ran and Key Findings

1. **DHS Component Frequencies and Signal Distribution:**
   * We ran an analysis of the ~3.59M DHS peak pool and mapped the distribution of the 16 components.
   * *Finding:* The components range in size from 56,186 peaks (`Stromal A`) to 626,541 peaks (`Primitive / embryonic`). Despite these differences in size, the top peaks in every single component have exceptionally high signal (max signal > 16 across all, and mostly > 40). Thus, taking 3,125 high-signal peaks from each component is fully viable and yields robust peaks even in the smallest component.
2. **Genomic FASTA Extraction and QC Validation:**
   * We verified that the genome chromosome FASTA files are present locally under `mpra_autoresearch/data/` and wrote an on-demand cache reader.
   * *Finding:* Testing our pipeline with the proposed QC filters (GC 20-80%, no homopolymers > 12bp, no 'N' characters) on the entire 3.59M dataset showed that we can extract exactly 3,125 high-quality, non-overlapping, peak-centered sequences for all 16 components successfully, totaling exactly 50,000 sequences.

---

## 5. What We Would Try Next

If we had more trials, we would explore:
1. **Motif-density Optimization:** We would scan the selected sequences with a motif database (like JASPAR) to ensure a high diversity of transcription factor binding motifs within the selected sequences, or to prioritize peaks that have a high density of non-redundant motifs.
2. **Active GC Balancing:** We would tune the GC content of selected sequences to match the GC distribution of highly active promoters and enhancers in MPRAs.
