# MPRA Library Design Notebook

## Problem framing

We design a 50,000-sequence, 200bp MPRA library intended as **training data for
a model of regulatory grammar that generalizes across cell types**. Activity is
measurable in K562, HepG2, SK-N-SH, but the eval is 14 anonymous sets and the
score is mean Pearson `mean_r`. So the library should be optimized to support
broad generalization — sequence and context diversity matter more than
maximizing activity in any single line.

Key principles from the brief:
- Not specific to a set of tissues
- Not only functional elements
- Diverse in sequence space
- High training performance-to-size ratio

## Theory: what makes a good MPRA training library

A model trained on MPRA data learns to predict expression-driving activity
from short DNA. To learn well it needs:

1. **Coverage of TF binding grammar across cell types.** A library that only
   shows enhancers from K562 will teach a model K562-specific patterns. We
   need regulatory regions active in many tissues so the model learns motif
   syntax broadly (TF identity, spacing, copy number, flanking context).

2. **Negative examples.** Inert background and shuffled sequences anchor the
   activity scale. Without them, the model never sees what "no signal" looks
   like and cannot calibrate.

3. **A range of activity levels.** Strong enhancers alone give a saturated
   distribution. Including moderate (e.g. quiescent intergenic) and weak
   elements expands the dynamic range, which improves Pearson correlation
   directly (correlation depends on spread).

4. **Sequence-space coverage.** Real genomes are biased (GC, repeats, CpG
   islands, etc.). Including controlled synthetic sequences (random, shuffled,
   motif-implanted) fills gaps so the model can extrapolate.

5. **Motif-anchored, controlled variation.** Sequences sharing one motif but
   differing in flanks, or sharing flanks but differing in motif content, let
   the model attribute activity to motif features. This dramatically improves
   training signal per sequence.

6. **Multi-scale context.** 200bp is the unit, but the model also benefits
   from sequences spanning promoter-TSS, gene body, intergenic, repeat
   classes — so it learns generic DNA statistics, not just CRE statistics.

## Plan

Composition target (50,000 sequences, 200bp each):

| Bucket | N | Source |
|---|---|---|
| ENCODE cCREs (broad cell types, including but not limited to K562/HepG2/SK-N-SH) | 22,000 | SCREEN cCRE BED + hg38 |
| Multi-tissue DHS index regions (Vierstra or similar broad open chromatin) | 6,000 | ENCODE DHS |
| Promoter regions (gene TSS ± window) | 4,000 | GENCODE TSS |
| Genomic background (random hg38 locations, masked for N) | 5,000 | hg38 |
| Motif-implanted synthetic (insert known TF motifs into varied backgrounds) | 5,000 | JASPAR-like motifs + random/genomic flank |
| Dinucleotide-shuffled controls of regulatory seqs | 4,000 | shuffle of bucket 1 |
| Pure random with varied GC | 2,000 | synthetic |
| Tiled around known regulatory landmarks | 2,000 | hg38 + cCREs |

Will calibrate exact counts as data come in. The principle: ~60–65% real
regulatory sequence from diverse cell types, ~25–30% genomic background and
controls, ~10–15% synthetic motif-anchored sequences.

## Decision: do not look at prepare.py

The brief explicitly says treat it as a black box. So I will not inspect or
import from it. The score will measure what it measures — my job is to make
the broadest, most informative training library I can given the brief.

## Data sources considered

- **UCSC hg38 2bit** — compact reference genome (~800 MB). Required to extract
  any genomic sequence by coordinate.
- **ENCODE SCREEN cCREs** — ~1M candidate cis-regulatory elements across many
  cell types with state labels (PLS, pELS, dELS, CTCF-only, DNase-H3K4me3).
  Direct download from screen.encodeproject.org. PLAN TO USE.
- **ENCODE DHS Index (Meuleman / Vierstra 2020)** — ~3.5M DHS peaks across
  733 samples, with module assignments. Could use if downloadable.
- **GENCODE annotation** — gene model GTF; can derive TSSs for promoter
  sampling.
- **JASPAR motifs** — TF PWMs for motif implantation (will use a small
  curated set of common TFs from many families to avoid bias).

## Sampling principles

- Stratify by cCRE class (PLS/pELS/dELS/CTCF/DNase-H3K4me3) to get diverse
  regulatory contexts.
- Spread across all autosomes plus X (skip Y to avoid tiny-chromosome bias);
  sample roughly proportional to chromosome size.
- Avoid heavy duplication: cluster cCREs by genomic proximity and keep
  representatives.
- Center each 200bp window on the cCRE midpoint (where applicable), or pick
  fixed positions for promoters (TSS-centered).
- Replace any N with a random nucleotide (rare in non-centromeric regions);
  uppercase everything; reject any window not entirely in {A,C,G,T} after
  fix-up if too many Ns.

## Notes during execution

### Data setup
- Downloaded UCSC hg38.2bit (835 MB) and converted each major chromosome
  (chr1..chr22, chrX) to raw ASCII files under `data/hg38_raw/` for fast
  random access. Total resident genome ~3.0 Gb.
- Downloaded SCREEN V3 ENCODE GRCh38 cCRE BED (1,063,878 elements across all
  major chromosomes; 1,062,844 after filtering to major chroms).
- cCRE class counts in this set:
  - dELS (distal enhancer-like): 788,426
  - pELS (proximal enhancer-like): 171,894
  - PLS (promoter-like): 40,848
  - CTCF-only: 35,783
  - DNase-H3K4me3: 25,893

### Final composition (50,000 sequences, 200 bp)
| Bucket | N | Description |
|---|---|---|
| ccre_dELS | 13,000 | distal enhancer-like cCREs |
| random_genomic | 7,000 | random 200 bp windows from autosomes + chrX |
| ccre_pELS | 5,500 | proximal enhancer-like cCREs |
| motif_implanted | 5,000 | 32 TF motifs implanted in random/shuffled/genomic bg |
| ccre_PLS | 4,000 | promoter-like cCREs |
| shuffled_ccre | 4,000 | dinucleotide-shuffled cCRE windows (negative grammar) |
| ccre_neighbor | 3,000 | cCRE windows shifted ±100–300 bp (adjacent context) |
| ccre_CTCF-only | 3,000 | CTCF-bound non-enhancer cCREs |
| random_gc (9 bins) | 3,000 | random sequences at GC ∈ {0.30, 0.35, …, 0.70} |
| ccre_DNase-H3K4me3 | 2,500 | DNase + H3K4me3 cCREs |

GC distribution: mean 0.477, median 0.465, IQR ≈ [0.40, 0.55]. All 50,000
sequences unique. All exactly 200 bp, all in {A,C,G,T}.

### Design decisions
- **Why a multi-bucket library, not just real cCREs?** A model that only sees
  positive regulatory regions cannot calibrate activity: it has no examples
  of "the same sequence statistics, but no functional motifs." Dinucleotide-
  shuffled cCREs and random sequences provide that null. Motif-implanted
  sequences anchor the model's mapping from individual TF motifs to activity
  in a controlled way (motif identity, copy number, flanks all varied).
- **Why use the aggregate SCREEN cCRE set rather than per-cell-type tracks?**
  The brief says "design for general regulatory grammar, not for these
  specific cell lines." The SCREEN aggregate is the union of cCREs called
  across hundreds of biosamples, so it spans regulatory regions active in
  many tissues, not just the three measurement lines. This matches the
  stated goal directly.
- **Why include positional/neighbor windows?** Real enhancers are wider than
  200 bp and have functional spread; shifted windows capture flanking
  context and teach the model that activity is locally distributed, not a
  pixel-perfect point feature.
- **Why a curated motif list rather than full PWMs?** Time budget. The
  curated list of 34 consensus motifs spans most major TF families (bHLH,
  bZIP, HMG, homeo, forkhead, ETS, NR, IRF, STAT, REL, MADS, zinc finger,
  T-box, POU, RUNX). IUPAC degeneracy at insertion gives realistic motif
  variation. Reverse-complement is randomized.
- **Why stratify chromosomes by length when randomly sampling?** Prevents
  small-chromosome over-representation while preserving genome-wide GC and
  repeat composition.
- **Soft-masked bases / Ns:** windows with >10 ambiguous bases are dropped;
  isolated Ns (rare in non-pericentromeric regions) are replaced with a
  random base. Real cCREs almost never overlap N-rich regions in practice.

### Evaluation results

`prepare.py library/sequences.txt` (541 s, 14 eval sets):

| metric | value |
|---|---|
| mean_r (mean across all 14 evals) | **0.7375** |
| mean_r (min across evals) | 0.6456 (eval_08) |
| mean_r (max across evals) | 0.8181 (eval_09) |
| K562 (avg across evals) | 0.7278 |
| HepG2 (avg across evals) | 0.7363 |
| SK-N-SH (avg across evals) | 0.7483 |

The three cell-line metrics are tightly clustered (max-min within ~0.02),
suggesting the library is genuinely cross-cell-type rather than skewed
toward any one line. SK-N-SH is slightly best, K562 slightly worst, but the
differences are small. Per-eval range from ~0.65 to ~0.82 likely reflects
how well each anonymous eval set's target sequences are covered by the
training composition.

### What I would try next
- Use ENCODE DHS Index (Meuleman et al. 2020) to add explicit multi-tissue
  open chromatin samples, weighted to ensure under-represented tissues
  (heart, brain, intestine) are over-sampled relative to easily-cloneable
  blood/cancer lines.
- Sample real MPRA training sequences from prior published libraries
  (Sharpr-MPRA, Agarwal et al., MPRA-DragoNN) and merge — they are known
  to be informative for activity prediction and cover ground the cCRE set
  may miss.
- Use ATAC-seq footprint data to bias backgrounds toward sequences with
  empirical TF binding, rather than relying on consensus IUPAC strings.
- Generate per-motif single-base saturation mutagenesis at small scale
  (~50 motifs × 30 mutants) to give the model gradient information
  directly.
- Tune bucket proportions against a held-out MPRA dataset before commit if
  iteration were allowed.

