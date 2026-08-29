# MPRA Library Design — Lab Notebook

## Goal recap
Design 50,000 × 200bp sequences for an MPRA library. The library is measured
in K562, HepG2, SK-N-SH but the resulting model is evaluated on 14 anonymous
held-out test sets (`eval_01`–`eval_14`). Each test set returns mean_r and
per-cell-type r scores. So the LIBRARY (training data) must teach the model
to predict activity in 3 cell types for held-out sequences drawn from
unknown distributions — likely a mix of promoters, enhancers, synthetic
sequences, variants, etc.

The instructions emphasise:
- not specific to a set of tissues
- not only functional elements
- diverse in sequence space
- high training-performance-to-size ratio (training set efficiency!)

## Theory of a good MPRA training library

Treat this as a supervised-learning training set problem. To train a model
that generalises across many test distributions, the training data needs:

1. **Coverage of the regulatory grammar** — the trained model can only
   predict activity from patterns it has seen. So the library must contain
   the major classes of regulatory elements (promoters, distal/proximal
   enhancers, CTCF/insulator, TF-only sites, accessible chromatin).

2. **Cell-type diversity** — even though only 3 cell types are measured,
   the regulatory grammar (motif syntax, GC content, k-mer composition) of
   enhancers active in *other* cell types may resemble those active in
   K562/HepG2/SK-N-SH. So sampling cCREs derived from ENCODE's full panel
   of hundreds of cell types — rather than only those active in K562/etc.
   — gives the model exposure to many tissue-specific motif compositions.

3. **A wide dynamic range of activity** — both strong elements and
   inactive backgrounds. Random sequences anchor the model around the
   "no motif → no activity" prior. Without negatives, the model has no
   contrast.

4. **Sequence-space diversity** — varied GC content, varied k-mer
   composition, repeat-rich regions. The literature (Iterative Deep
   Learning Design of Human Enhancers, Sahu 2022, lentiMPRA Agarwal 2024)
   consistently finds that *mixed* (natural + synthetic) training data
   outperforms all-natural or all-DHS data.

5. **Controlled redundancy** — duplicates waste assay capacity, but some
   motif redundancy lets the model learn motif rules rather than memorise
   one-off sequences. Avoid identical or near-identical sequences.

6. **No leakage with what the test sets might use** — I have no way to
   know what eval sets contain, but the safe play is to sample broadly
   rather than concentrate on one source.

## Sources considered

### Used
- **hg38 reference genome** (UCSC) — for extracting sequences from
  genomic coordinates. Necessary input.
- **ENCODE cCRE Registry V4** (`https://downloads.wenglab.org/Registry-V4/GRCh38-cCREs.bed`)
  — 2.35M elements classified into PLS, pELS, dELS, CA-CTCF, CA, CA-TF,
  CA-H3K4me3, TF. This is the canonical, high-quality catalogue of human
  regulatory elements. V4 (ENCODE4) builds on data from hundreds of cell
  types so the elements are tissue-agnostic by construction.

  Lengths range 150–350 bp (median 273), so a 200bp window centred on each
  element captures the core regulatory signal. Counts:
  - PLS: 47,532          (promoters)
  - pELS: 249,464        (proximal enhancer-like, ≤2kb from TSS)
  - dELS: 1,469,205      (distal enhancer-like — most diverse pool)
  - CA-CTCF: 126,034     (insulators)
  - CA-H3K4me3: 79,246
  - CA-TF: 26,102
  - CA: 245,985          (DNase-accessible only)
  - TF: 105,286          (TF-bound only)

### Considered and excluded
- **GENCODE TSS-based promoters** — would duplicate cCRE PLS substantially.
  Excluded to avoid redundancy.
- **VISTA enhancers** — well-validated but only ~3K elements; small impact.
  Could have added ~1K but cCRE dELS gives much broader coverage.
- **GTEx eQTL / GWAS variant windows** — could be useful for variant
  prediction tasks but not core regulatory grammar. Skipped to keep scope
  tight.
- **RepeatMasker repeats** — most repeats are inactive but they form a
  large fraction of the genome the model will need to handle. Included
  implicitly via intergenic random sampling (which will hit repeats at the
  genomic frequency).
- **JASPAR / HOCOMOCO motif insertion** — explicitly synthetic sequences
  with planted motifs could be useful. Decided to skip for v1 because (a)
  without testing how the model trains, motif planting is speculative, and
  (b) dinucleotide-shuffled cCREs already test "broken grammar" hypotheses.
- **lentiMPRA pre-trained sequences** — would be perfect to mine but no
  guarantee of availability/url and I have one commit.

## Library composition (50,000 sequences)

Total split decided on:

| Class | N | Rationale |
|---|---|---|
| cCRE PLS (promoter-like) | 6,500 | Promoter cores are non-tissue-specific "on switches" per lentiMPRA — great cross-cell signal |
| cCRE pELS (proximal enhancer-like) | 6,500 | Near-TSS enhancers, often shared across cells |
| cCRE dELS (distal enhancer-like) | 16,000 | Largest pool (1.5M) gives maximum sequence-space coverage; most tissue-specific so rich grammar |
| cCRE CA-CTCF | 3,000 | Insulators / boundary elements |
| cCRE CA (DNase only) | 2,000 | Accessible chromatin without strong marks |
| cCRE CA-H3K4me3 | 2,000 | Active promoter-mark only |
| cCRE CA-TF | 1,000 | DNase + TF binding |
| cCRE TF (TF-only) | 2,000 | TF binding without open chromatin |
| **cCRE-derived subtotal** | **39,000** | |
| Random uniform (50% GC) | 1,500 | Anchor "no signal" prior |
| Random varied GC (30–70%) | 1,500 | Span GC space — many real elements are GC-rich (CGI-like) |
| Dinucleotide-shuffled cCREs | 3,000 | Preserve k-mer composition but break motifs — ideal motif-syntax negatives |
| Intergenic genomic background | 3,000 | "Real" inactive DNA, includes repeats at native frequency |
| Random uniform GC=50% extra | 2,000 | More negatives — DREAM-style random sequences also help the model learn nothing-from-nothing |
| **Controls subtotal** | **11,000** | |
| **Total** | **50,000** | |

(I'll trim later if needed to hit exact counts.)

## Sampling rules
- Stratified-uniform per chromosome within each cCRE class. Avoid
  oversampling chr1 just because it's longer.
- Drop sequences with any N in the 200bp window.
- Deduplicate within and across classes.
- Random seed fixed for reproducibility.

## What I would try next if I had another shot
1. **Iterative active learning**: train a model on a smaller library,
   identify high-uncertainty sequences, prioritise them in the next
   commit. The one-shot constraint prevents this here.
2. **Mine variant effects** (gnomAD common variants × cCRE overlap)
   to add reference/alternate pairs — would help variant-prediction
   eval sets.
3. **Add VISTA enhancers** (validated developmental enhancers) — small
   but high-confidence.
4. **Motif-shuffled sequences** with planted JASPAR cores at controlled
   spacings to learn motif grammar.
5. **Saturation mutagenesis** of a small number of "anchor" elements to
   teach the model fine-grained nucleotide effects.
6. **Cross-species conservation** windows — orthologous regulatory
   elements from mouse / zebrafish to broaden grammar diversity.

## Notes on uncertainty
- I cannot inspect prepare.py so I don't know:
  - How many of my sequences are actually used (it might subsample)
  - Whether it trains a CNN, transformer, or simpler model
  - Train/val split policy
  - Whether reverse-complement is canonicalised
- Conservative choice: assume any sane training pipeline benefits from a
  diverse library with good signal/control balance. That's what I built.

## Results (from prepare.py)

Single run after generating `library/sequences.txt`. 506s wall-clock.

| Eval set | mean_r | K562 | HepG2 | SK-N-SH |
|---|---|---|---|---|
| eval_01 | 0.6938 | 0.6842 | 0.6898 | 0.7075 |
| eval_02 | 0.7835 | 0.7720 | 0.7741 | 0.8043 |
| eval_03 | 0.7660 | 0.7557 | 0.7538 | 0.7887 |
| eval_04 | 0.7429 | 0.7372 | 0.7397 | 0.7519 |
| eval_05 | 0.6939 | 0.6832 | 0.6907 | 0.7079 |
| eval_06 | 0.7832 | 0.7712 | 0.7739 | 0.8044 |
| eval_07 | 0.7050 | 0.6909 | 0.6979 | 0.7260 |
| eval_08 | 0.6432 | 0.6416 | 0.6314 | 0.6567 |
| eval_09 | 0.8028 | 0.7987 | 0.7984 | 0.8113 |
| eval_10 | 0.7351 | 0.7365 | 0.7154 | 0.7535 |
| eval_11 | 0.6812 | 0.6712 | 0.6790 | 0.6934 |
| eval_12 | 0.6567 | 0.6489 | 0.6507 | 0.6705 |
| eval_13 | 0.7019 | 0.6823 | 0.6927 | 0.7305 |
| eval_14 | 0.7832 | 0.7719 | 0.7738 | 0.8039 |

Aggregate: **mean_r 0.7266** (range 0.6432–0.8028);
K562 0.7175, HepG2 0.7187, SK-N-SH 0.7436.

### Reading the results
- SK-N-SH consistently scores ~2.5pp higher than K562/HepG2 across every
  eval set. Possible reasons: SK-N-SH activity distribution may be easier
  to fit, or the trained model captures neural regulatory grammar well.
- eval_02 / eval_06 / eval_14 are essentially identical (~0.78) — they
  may be replicates or near-identical test sets.
- eval_08 (0.64) and eval_12 (0.66) are the hardest. Could be:
  (a) synthetic / out-of-distribution sequences (random, motif-designed)
  (b) variant-effect / saturation mutagenesis tasks
  (c) sequences from a cell type whose grammar is poorly represented in
      my library

### What I would change with another shot
- More dedicated promoter coverage at the cost of dELS — PARM / lentiMPRA
  evidence suggests promoter cores generalise across tissues better than
  enhancers, and might lift the harder eval sets.
- Add explicit motif-grammar synthetic sequences (planted JASPAR motifs
  with controlled spacing/orientation) — this typically helps fine-grained
  variant-effect prediction tasks.
- Build a few hundred saturation-mutagenesis "anchor" elements to teach
  per-nucleotide effects for variant-prediction eval sets.

Decided not to chase prepare.py iteratively after this single run —
treating prepare.py as a wet-lab assay per the instructions. The design
above is principled and yields a stable mean_r of 0.73.
