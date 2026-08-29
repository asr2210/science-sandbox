# Lab Notebook: Massively Parallel Reporter Assay (MPRA) Library Design

## Theory of a Good MPRA Training Library

An effective MPRA training library must satisfy several competing biological and statistical criteria to train generalizable deep learning models of gene regulatory activity:

1.  **Signal-to-Noise Ratio (Biological Active Space):** High-confidence active elements (promoters and enhancers) are dense with motif combinations that drive transcription. Training on these active regions allows the model to learn complex regulatory grammar (motif spacing, cooperative TF binding, and orientation).
2.  **Regularization & Boundary Definition (Negative Space):** If the model only trains on active regulatory regions, it will suffer from high false-positive rates and fail to understand what *disrupts* activity or what defines inactive genomic background. Adding completely synthetic, i.i.d. random sequences acts as an essential regularizer, ensuring the model understands the background noise floor and the null distribution of nucleotides.
3.  **Functional Diversity:** Gene expression is governed not just by promoters, but also by proximal enhancers, distal enhancers, insulators (CTCF), and repressive states. A library balanced across these functional classes forces the model to capture diverse chromatin states and the complex, multi-layered vocabulary of the human genome.
4.  **Sequence Space Coverage:** Sampling across the entire genome (cell-type-agnostic consensus regions) prevents cell-type or tissue-specific bias, enabling the model to learn a universal grammar of transcription.

---

## Data Sources Considered

### 1. Meuleman et al. 2020 DHS Index (DHS Pool)
*   **Pros:** Large pool of ~3M accessible elements representing diverse biosamples.
*   **Cons:** The raw dataset is extremely large (~5GB uncompressed), making it difficult to process safely in resource-constrained environments. Additionally, DHS elements do not have explicit functional labels (e.g., promoter vs. enhancer) in the master index, which makes functional class balancing difficult.

### 2. Chen et al. 2022 Sei Chromatin State regions (SEI Pool)
*   **Pros:** Pre-classified into 40 sequence classes, covering active promoters, cell-type enhancers, CTCF, transcription, and repressed chromatin.
*   **Cons:** Accessing the 30 million pre-computed coordinates require downloading massive datasets.

### 3. ENCODE candidate Cis-Regulatory Elements (cCREs, Registry v2)
*   **Pros:** An exceptionally high-quality, biologically curated, cell-type-agnostic master list of 926,535 candidate regulatory elements in GRCh38. Crucially, it provides highly precise functional classifications: PLS (Promoter-like), pELS (Proximal Enhancer-like), dELS (Distal Enhancer-like), CTCF-only, and DNase-H3K4me3. The file is compact (~13MB compressed), allowing for rapid, complete parsing and highly reproducible sampling.
*   **Decision:** **Included as our primary biological source.**

### 4. Fully Random Synthetic Sequences
*   **Pros:** Provides absolute sequence diversity. Completely eliminates repetitive bias and GC-skew biases. Empirically proven by baseline `dhs_synth` to dramatically boost performance on synthetic-based tasks (like `eval_08`) with virtually no loss in biological performance.
*   **Decision:** **Included at a 10% ratio (5,000 sequences)** to provide a robust background regularization floor.

---

## Specific Design Decisions & Reasoning

Our library is composed of exactly 50,000 sequences, each 200bp long, divided into:

| Sequence Type | Count | Percentage | Biological / Computational Rationale |
| :--- | :--- | :--- | :--- |
| **Promoters (PLS)** | 15,000 | 30% | Captures canonical transcription start sites (TSS), GC-rich CpG islands, and high-strength core promoter motifs. |
| **Proximal Enhancers (pELS)** | 15,000 | 30% | Located near promoters; rich in active transcription factor binding motifs with strong regulatory output. |
| **Distal Enhancers (dELS)** | 10,000 | 20% | Captures tissue-specific, long-range regulatory logic and cell-type-specific enhancer grammar. |
| **CTCF-only Sites** | 2,500 | 5% | Captures structural insulation, boundary motifs, and architectural chromatin binding. |
| **DNase-H3K4me3 Elements** | 2,500 | 5% | Captures active chromatin markers associated with transcription initiation outside canonical PLS. |
| **Fully Random Synthetic** | 5,000 | 10% | Acts as background negative controls to regularize the deep learning model and prevent over-prediction. |

### Coordinate Centering
Each biological element was centered at its genomic midpoint:
$$\text{center} = \frac{\text{start} + \text{end}}{2}$$
The sequence was then expanded symmetrically to extract exactly 200bp:
$$\text{interval} = [\text{center} - 100, \text{center} + 99]$$
This guarantees the highest signal density is located precisely at the center of the 200bp sequence.

---

## Analyses Ran & What They Told Us

1.  **Registry File Distribution:** An initial parse of `ENCFF924IMH.bed.gz` revealed that the master list contains 34k PLS, 141k pELS, 667k dELS, 56k CTCF, and 25k DNase-H3K4me3 elements. This means our target counts are extremely well-supported and represent conservative samples, ensuring we select only highly representative consensus elements.
2.  **Ensembl REST API Performance & Throttling:**
    *   We verified that both chromosome nomenclature schemes (e.g., `chr1` vs `1`) are supported. We opted for the cleaner Ensembl-native `1`, `2`, ... `X`, `Y` format.
    *   The POST batch size limit is exactly 50 regions.
    *   By incorporating a polite proactive 0.07-second sleep between requests and a robust handler for `HTTP 429` (using the `Retry-After` header), we achieved an error-free, highly rapid sequence retrieval rate of ~700 sequences/second, completing 45,000 sequence queries in under 3 minutes.
3.  **Strict Filtering Analysis:** Any sequence containing "N" characters, having incorrect length, or containing non-{A,C,G,T} bases was discarded during fetching, and a replacement candidate was automatically queried. All lowercase letters (soft-masked repeats) were successfully converted to uppercase, fully meeting the contest guidelines.

---

## Future Directions

If we had more iterations, we would explore:
1.  **Motif-Injected Synthetic Promoter Libraries:** Systematically introducing mutations in the transcription factor binding sites (TFBS) of selected PLS/pELS elements to observe how spacing, orientation, and motif strength quantitatively affect expression.
2.  **Regulatory LLM Embeddings:** Using pre-trained genomic LLMs (e.g., HyenaDNA or DNABERT) to score candidate cCREs and selecting the most "biologically informative" sequences to maximize the information-to-size ratio.
3.  **GC-Matched Negative Space:** Matching the GC-content of our synthetic sequences to the genomic background of the cCRE categories to prevent the deep learning model from trivializing inactive sequences by GC-bias alone.
