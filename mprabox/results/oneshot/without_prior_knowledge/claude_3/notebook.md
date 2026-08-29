# MPRA Library Design — Lab Notebook

**Date:** 2026-05-23
**Goal:** Design a 50,000 × 200bp MPRA library for training a general regulatory-grammar model.

## Problem framing

We get **one shot**. `prepare.py` is a black box that:
- Trains a model on our 50,000 sequences (presumably with measurements it generates)
- Tests on 14 anonymous evaluation sets (eval_01..eval_14)
- Reports per-set mean_r, k562_r, hepg2_r, sknsh_r
- Optimizes across all sets — no single primary metric

What we don't know:
- The model architecture used (CNN? transformer? linear?)
- Whether the activity labels for our sequences come from synthetic ground truth (e.g., a teacher model) or from a real assay
- What the 14 eval sets contain (likely diverse: different cell types, sequence classes, MPRA platforms)

The fact that 3 cell types are mentioned (K562, HepG2, SK-N-SH) but the instructions say "general regulatory grammar across ALL cell types" suggests the eval sets probably span beyond those 3 cell lines. So our training library should support cross-cell-type generalization.

## Theory of what makes a good MPRA training library

To train a model that captures **general regulatory grammar**, the library should provide:

1. **Broad coverage of regulatory sequence space.** TF motifs are the alphabet; the library should expose the model to most of them in varied contexts. Many TFs, many spacings, many compositions.

2. **Wide dynamic range of activity.** A model trained only on weak/silent sequences cannot learn what makes a strong enhancer. We need strong positives AND clean negatives.

3. **Multiple sequence classes.** Promoters, enhancers, silencers, insulators, untranscribed DNA — each has different grammar. Models that see only one class learn class-specific shortcuts.

4. **Cross-cell-type diversity.** Sample regulatory elements from MANY cell types (not just K562/HepG2/SK-N-SH). The model should learn that "this is a HNF4α site" generalizes, not "this is what an active sequence in HepG2 looks like."

5. **Distributional similarity to test sequences.** Whatever the eval sets contain, our training distribution should overlap it. Real genomic regulatory regions are likely the safest bet because they are the most common form of MPRA sequence in the literature.

6. **Negative controls.** Dinucleotide-shuffled and random sequences anchor the model's notion of "inactive" without it relying on local GC quirks.

7. **Sequence diversity, not redundancy.** 50,000 near-duplicates is much worse than 50,000 distinct sequences. We need de-duplication.

## Composition strategy (draft, will refine)

Tentative budget for 50,000 sequences:

| Bucket | Count | Source | Purpose |
|---|---|---|---|
| ENCODE cCREs (diverse cell types) | ~20,000 | SCREEN cCRE registry; mix of dELS, pELS, PLS, CTCF, DNase-H3K4me3 | Real regulatory grammar across many cell types |
| Promoter windows (TSS ± 100) | ~7,500 | GENCODE TSS, diverse genes | Promoter grammar (TATA, Inr, GC-box, CpG) |
| Tissue-specific enhancers | ~5,000 | FANTOM/EnhancerAtlas/VISTA | Enhancer grammar across tissues |
| Random genomic windows | ~5,000 | Random 200bp from accessible-mask genome | Background activity distribution |
| Dinucleotide-shuffled regulatory | ~5,000 | Shuffle of cCREs (di-shuffle preserves GC and dinucleotide freq) | Negative controls preserving composition |
| Pure random sequences | ~2,500 | uniform {A,C,G,T} | Hard negatives, anchor very-low activity |
| Synthetic motif scans | ~5,000 | JASPAR core motifs inserted in random/shuffled backgrounds at varied position/orientation/density | Helps model isolate motif effect from context |

These are starting allocations; I'll adjust based on what data I can actually download.

## What I'll need to download

1. **Reference genome (hg38)** — minimal: maybe just enough chromosomes to sample from. UCSC `hg38.fa.gz` is ~900MB compressed, ~3GB unpacked. May be too large.
   - Alternative: use UCSC `das` API or fetch specific regions via UCSC's `hgsubseq` or REST API.
   - Alternative: download per-chromosome FASTAs as needed.

2. **ENCODE SCREEN cCREs** — BED file of ~1M elements with cell-type classifications.

3. **GENCODE annotations** — for TSS coordinates.

4. **JASPAR motifs** — PWMs of TF binding sites for synthetic generation.

5. **FANTOM5 enhancers** (if accessible).

## Risk: bandwidth / time

Downloading hg38 is slow. I'll first try downloading just chromosomes I need, or use a REST API to fetch sequence by coordinates. The ENCODE/UCSC REST APIs accept range queries.

## Backup plan

If I can't get genomic data:
- Generate purely synthetic sequences using JASPAR motifs embedded in random backgrounds with varied densities and arrangements
- Synthetic sequences alone will train models that learn motif → activity, which has limited transfer to natural sequences but is better than nothing

## Update — environment

- Python 3.12.3 with venv at `venv/`
- Installed: numpy, pandas, scikit-learn, biopython, requests, pyfaidx
- Platform is **aarch64** — UCSC's twoBitToFa x86 binary won't run, py2bit and pyBigWig also fail to build. So I wrote a minimal pure-Python 2bit reader (`data/twobit_reader.py`).
- No GPU needed.

## Data acquired

- `data/hg38.2bit` (800MB) — full hg38 genome
- `data/GRCh38-cCREs.bed` — 2,348,854 SCREEN v4 cCREs across 24 chromosomes
  - dELS: 1.4M; pELS: 249K; CA: 246K; CA-CTCF: 126K; TF: 105K; CA-H3K4me3: 79K; PLS: 47K; CA-TF: 26K
  - Sizes: 150-350bp, median 273bp — perfect for 200bp centered windows
- Pure-python 2bit reader benchmarked: loads chr22 (50MB) in 0.73s

## Final design decisions

After thinking through what `prepare.py` likely does — train a model on (my sequences, labels) and test on 14 held-out eval sets — the priority is **diverse real regulatory DNA** because:

1. The cCRE registry covers ~1500 cell types/biosamples — sampling broadly gives cross-cell-type coverage by construction
2. Real regulatory DNA contains the motifs and grammar the model needs to learn
3. With 50K sequences and a 200bp window matching typical MPRA designs, we have enough room for class diversity

### Final composition (50,000 sequences)

| Bucket | Count | Source | Rationale |
|---|---|---|---|
| Diverse cCREs | 40,000 | SCREEN registry, stratified by class | Core regulatory grammar from many cell types |
| Random genomic 200bp | 5,000 | Random hg38 windows, N-filtered | Background distribution — most genomic DNA is non-regulatory |
| Dinucleotide-shuffled cCREs | 3,000 | Shuffle of sampled cCREs | Negative controls with matched GC/dinuc composition |
| Synthetic motif-engineered | 2,000 | Hand-curated TF motif consensus in random bg | Clean positive signal, motif identification training |

### cCRE sub-allocation (40,000)

Weighted toward smaller classes to ensure all are well-represented:

| Class | n | Frequency in registry |
|---|---|---|
| dELS | 13,000 | 62.6% |
| pELS | 5,500 | 10.6% |
| CA | 4,500 | 10.5% |
| CA-CTCF | 4,000 | 5.4% |
| PLS | 4,000 | 2.0% (oversampled — promoter-like) |
| TF | 3,500 | 4.5% |
| CA-H3K4me3 | 3,500 | 3.4% |
| CA-TF | 2,000 | 1.1% (oversampled — TF-bound chromatin) |
| **Total** | **40,000** | |

Sampling is uniform within class but stratified by chromosome to avoid chr1 dominance.

### Why I'm not adding more

- **JASPAR motif scans:** real cCREs already contain motifs in natural context; adding more synthetic might shift distribution toward unnatural sequences.
- **GENCODE TSS windows:** PLS cCREs already give 47K promoter-like sequences.
- **VISTA enhancers:** ~1500 validated enhancers, too few to materially help — and cCRE dELS already covers enhancer space.
- **eQTL alt alleles:** would require variant data download; complexity not justified.

### Risks of this design

1. **Distribution mismatch with eval sets:** if eval sets contain mostly synthetic or very specific assays, my real-DNA emphasis could miss.
2. **Class imbalance:** dELS dominates; a model might overfit to "average enhancer" features.
3. **No explicit cell-type labeling:** if the eval is K562-specific and we have many SK-N-SH-relevant elements, we lose discrimination.

### What I would try next if I had another shot

- Add cell-type-specific cCRE activity zScores to enforce K562/HepG2/SK-N-SH diversity
- Add a fraction (~5K) of FANTOM5 enhancer-promoter pairs for known-functional sequences
- Include ~2K eQTL ref/alt allele pairs
- Try different class proportions (e.g., higher dELS share if eval set is enhancer-heavy)
- Run a sanity check on a small held-out genomic set before committing

## Results

After generation completed (50,000 sequences, all 200bp ACGT, no duplicates),
ran `python prepare.py library/sequences.txt`. Eval took ~17 min (1040s wall).

Per-eval-set Pearson r (mean across cell types):

| eval | mean_r | k562_r | hepg2_r | sknsh_r |
|---|---|---|---|---|
| eval_01 | 0.740 | 0.738 | 0.740 | 0.742 |
| eval_02 | 0.836 | 0.837 | 0.831 | 0.842 |
| eval_03 | 0.822 | 0.824 | 0.814 | 0.828 |
| eval_04 | 0.783 | 0.784 | 0.779 | 0.785 |
| eval_05 | 0.740 | 0.738 | 0.741 | 0.742 |
| eval_06 | 0.837 | 0.837 | 0.831 | 0.842 |
| eval_07 | 0.784 | 0.789 | 0.780 | 0.783 |
| eval_08 | 0.710 | 0.725 | 0.696 | 0.709 |
| eval_09 | 0.850 | 0.851 | 0.847 | 0.851 |
| eval_10 | 0.800 | 0.810 | 0.787 | 0.803 |
| eval_11 | 0.727 | 0.726 | 0.728 | 0.727 |
| eval_12 | 0.707 | 0.710 | 0.703 | 0.707 |
| eval_13 | 0.780 | 0.781 | 0.775 | 0.783 |
| eval_14 | 0.836 | 0.836 | 0.830 | 0.842 |

**Overall mean across all 14 eval sets: 0.785**

Observations:
- Per-cell-type r is very similar within each eval set → the model
  generalizes uniformly across K562/HepG2/SK-N-SH, no strong cell-type bias
  from the training library.
- Best evals (eval_09, eval_02, eval_06, eval_14 all ~0.84) likely
  correspond to test sets most distributionally similar to my training
  composition (real regulatory DNA, broad cell types).
- Hardest evals (eval_08, eval_12, eval_11 all ~0.71) probably contain
  sequence classes that are under-represented — possibly highly synthetic
  sequences, fine-tuning around known motifs, or saturation mutagenesis
  data where small sequence differences must be discriminated.
- The narrow per-eval cell-type spread (e.g., eval_08: 0.696-0.725)
  suggests the model bottleneck is sequence-class coverage, not cell-type
  representation. Adding more variant-style sequences (single-base
  perturbations of cCREs) would likely lift the lowest scores.
