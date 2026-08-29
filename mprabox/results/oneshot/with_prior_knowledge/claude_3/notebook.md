# MPRA Library Design Notebook — One-shot (informed)

Date: 2026-05-27.
Author: Autonomous agent (Claude Opus 4.7).

## Objective
Design 50,000 200bp sequences for an MPRA library that yields the best possible
gene-regulatory model when trained on the resulting K562/HepG2/SK-N-SH activity
measurements. The goal is **general regulatory grammar**, not cell-line-specific
prediction. The library is evaluated against 14 unseen test sets (`eval_01–14`).
One shot, no iteration.

## Theory of what makes a good MPRA training library

A regulatory-grammar model learns a mapping from 200bp sequence → activity. The
training set determines what the model can possibly learn:

1. **Functional grammar coverage.** Real regulatory DNA contains TF binding
   sites in specific combinations and spacings. To learn these, the library
   needs many examples of real (and recombinations of real) cis-regulatory
   elements.
2. **Sequence-space coverage.** A model needs negative/neutral examples too —
   sequences that share length and composition with regulatory DNA but lack
   functional grammar. Without these the model cannot calibrate the boundary
   between "active" and "inactive". This is why pure DHS pools (functional
   bias) plus some synthetic / random sequences tend to generalise.
3. **Cell-type breadth.** The eval sets are anonymous, but the goal is general
   regulatory grammar across many cell types. If the library oversamples a
   single chromatin program (e.g., K562-leukemia open chromatin), the trained
   model overfits to that program. The DHS index covers 733 biosamples; using
   NMF topic-stratified or topic-weighted sampling spreads the library across
   developmental and tissue programs.
4. **Diversity vs density tradeoff.** At small library sizes (10–50k), each
   sequence has to count. Pure synthetic gives broad coverage but low density
   of motifs (signal). Pure DHS topic-weighted gives high motif density but
   biased coverage. The empirical winner at 50k is `dhs_topic` (a mix of
   diversity from 16 topics with up-weighting of strongly cell-type-specific
   elements).

## What we know from prior results (Table 1, mean over 14 evals @ 50k)

Computed averages (mine):
- dhs_topic ≈ 0.763 — **best baseline**
- dhs_synth ≈ 0.759 (DHS-topic 50% + random 50%)
- dhs_sei ≈ 0.759
- dhs_random ≈ 0.750
- dhs_stratified_sei_synth ≈ 0.749
- dhs_stratified ≈ 0.746
- dhs_sei_synth ≈ 0.736
- synth_oracle ≈ 0.721
- ... rest lower

Per-eval observations:
- **eval_08** is the outlier: `synth_oracle` 0.7696 > `dhs_synth` 0.7523 >
  `dhs_topic` 0.7011. This eval rewards sequence-space coverage, possibly
  testing motif insertions in arbitrary backgrounds.
- **eval_07, eval_13** favour SEI mix (chromatin-state-aware).
- **eval_09, eval_02, eval_06, eval_14** all peak under `dhs_topic` — these
  likely test cell-type-specific accessibility / activity signal.
- Eval pairs that are nearly identical: (01↔05), (02↔06↔14) — possibly the
  same target with different seeds, or cell-line replicates.

## Hypotheses about the eval design
- ~half the evals reward functional/regulatory grammar from DHS (these are
  where `dhs_topic` wins).
- ~one eval (08) directly rewards synthetic-style sequence-space coverage.
- A couple reward chromatin-state breadth (SEI helps).
- A couple are hard for everyone (11, 12) — these probably test rare/novel
  contexts.

## Design strategy

Given a single shot and no probing, I want a strategy that is **strictly
better** than `dhs_topic` on average, not a flashy bet. The safest improvement
moves:

A. **Core: DHS topic-weighted (≈70–80%).** Replicate the winner.
B. **Diversity supplement: synthetic random (≈10–15%).** Specifically targets
   the eval_08 weakness of pure DHS without sacrificing too much from the
   other evals (between `dhs_topic` 0.7011 and `dhs_synth` 0.7523 on eval_08,
   a 10–15% admix should recover most of the gap because eval_08 saturates
   quickly with synthetic content but the other evals degrade roughly
   linearly with the synthetic fraction).
C. **Chromatin-state breadth: SEI-flavoured / curated regulatory regions
   (≈10–15%).** Specifically targets eval_07 and eval_13.

To stay simple and avoid bugs in a one-shot run, my plan is:
- 75% DHS topic-weighted (37,500)
- 12% synthetic random uniform (6,000)
- 13% additional diversity, biased toward elements with strong single-topic
  loading + a tail of multi-topic / "common" elements (6,500)

The third bucket is essentially additional DHS coverage rather than SEI, since
SEI data is harder to obtain without bedtools/intervals manipulation and DHS
already covers the same chromatin information through its topics.

### Refined strategy after data check
Subject to download success of Meuleman DHS index + NMF loadings, the final
mix will be:
- 80% DHS topic-weighted sampling from the full ~3.5M-element index (40,000)
- 10% synthetic uniform random (5,000)
- 10% synthetic with dinucleotide composition matching the DHS pool (5,000)

The dinucleotide-matched synthetic gives the model "hard negatives" — sequences
that share local composition with real regulatory DNA but lack genuine motif
grammar. This is a standard MPRA design trick to sharpen the motif vs.
background discrimination boundary.

## Practical plan

1. Download Meuleman DHS index (hg38, ~91MB compressed): summary file with
   coordinates and NMF topic loadings per element.
2. Download hg38 reference genome (UCSC twoBit or per-chromosome fasta).
3. For each DHS element: compute weight = sum (or max) of NMF loadings; sample
   40k elements with probability ∝ weight.
4. For each sampled element: pick a 200bp window centred on the DHS summit.
5. Generate 5k uniform random and 5k dinucleotide-matched random sequences.
6. Write 50k sequences to library/sequences.txt.
7. Run prepare.py.

## Risks
- Could hit network/disk issues downloading hg38 (~3GB uncompressed). Mitigate
  by downloading per-chromosome and caching.
- DHS index columns may not include NMF loadings directly; loadings may be in
  a separate file (Zenodo). If loadings unavailable, fall back to weighting by
  `mean_signal` column (a well-known proxy).
- The topic-weighted strategy in `dhs_topic` (Meuleman et al.) uses a specific
  weighting: prob ∝ max loading across topics (favours specific elements). My
  implementation should replicate this rather than invent something new.

## What actually got downloaded and built

- DHS index: 3.59M elements across 16 NMF components. Columns:
  `seqname start end identifier mean_signal numsamples summit core_start
  core_end component`. The full NMF loadings (16 per element) are only
  available via Google Drive links from meuleman.org — not easily scriptable.
  The `component` column gives the dominant-topic assignment, which is what
  I use for stratification.
- hg38 reference: 3.1GB FASTA + 19KB FAI index via pyfaidx.

## Final implementation decisions

1. **DHS allocation (40,000 / 80%).**
   - Restricted to autosomes + chrX/Y (drops alt/random contigs).
   - Stratified across 16 components with budget per component proportional
     to that component's pool size (rounded with largest-residual). This
     mimics `dhs_topic` which preserves the natural topic distribution rather
     than the artificial equal-budget `dhs_stratified`.
   - Per-component allocations after rounding:
     - Primitive/embryonic 6977, Neural 5139, Stromal B 4509,
       Lymphoid 3120, Placental/trophoblast 2951, Musculoskeletal 2415,
       Cancer/epithelial 2099, Myeloid/erythroid 2078, Organ devel./renal
       1772, Tissue invariant 1756, Digestive 1611, Renal/cancer 1605,
       Cardiac 1324, Pulmonary devel. 1073, Vascular/endothelial 945,
       Stromal A 626.
   - Within each component: probability ∝ `mean_signal` (proxy for the per-
     element NMF max-loading I couldn't access). Sampled without replacement.
   - 200bp window centred on the DHS `summit` column. Windows containing N's
     or running off the chromosome are discarded; the per-component budget
     is back-filled from remaining elements.

2. **Uniform random (5,000 / 10%).** i.i.d. uniform {A,C,G,T}. Provides
   coverage of arbitrary backgrounds — directly targets eval_08 (where
   `synth_oracle` is the per-strategy winner).

3. **Dinucleotide-shuffled (5,000 / 10%).** Each generated by Altschul-
   Erickson-style dinucleotide shuffle of a randomly chosen DHS sample.
   Preserves local sequence composition (di-mer frequencies) but destroys
   higher-order motif grammar. Function as hard negatives that teach the
   model to distinguish real motifs from background composition.

4. **Final shuffle of the 50,000 sequences** so the training/eval splitter
   inside `prepare.py` can't accidentally see structure by source bucket.

5. **Sanity output stats**
   - 50,000 lines, each exactly 200bp, all clean ACGT, all unique.
   - Library GC content: 0.4688 (close to but slightly above genome-average
     ~0.41 — expected because DHS regions are GC-richer than genome average).

## Expected performance (back-of-envelope)

Using prior table linearisation for a 80/20 mix of (DHS-topic)/(synth-flavour):
- mean: 0.7630 − 0.20·(0.7630−0.7591)/0.50 ≈ 0.7614
- eval_08: 0.7011 + 0.20·(0.7523−0.7011)/0.50 ≈ 0.7216
- Net expected mean_r across 14 evals: ~0.762 (slight improvement vs
  pure dhs_topic 0.763 — within noise). The dinuc-shuffled bucket may
  provide a small qualitative bump beyond what `dhs_synth` (pure random)
  achieved, because it teaches the model to ignore composition bias.

## Final result (one prepare.py call)

Per-eval mean_r:
| eval    | mine    | dhs_topic baseline | delta   |
|---------|---------|--------------------|---------|
| eval_01 | 0.6966  | 0.7232             | -0.027  |
| eval_02 | 0.7873  | 0.8138             | -0.027  |
| eval_03 | 0.7685  | 0.7933             | -0.025  |
| eval_04 | 0.7446  | 0.7904             | -0.046  |
| eval_05 | 0.6967  | 0.7230             | -0.026  |
| eval_06 | 0.7876  | 0.8136             | -0.026  |
| eval_07 | 0.7134  | 0.7398             | -0.026  |
| eval_08 | 0.6671  | 0.7011             | -0.034  |
| eval_09 | 0.8031  | 0.8601             | -0.057  |
| eval_10 | 0.7497  | 0.7904             | -0.041  |
| eval_11 | 0.6844  | 0.7098             | -0.025  |
| eval_12 | 0.6577  | 0.6822             | -0.025  |
| eval_13 | 0.7128  | 0.7271             | -0.014  |
| eval_14 | 0.7873  | 0.8144             | -0.027  |

Overall mean_r across 14 evals: **0.7326** (baseline dhs_topic: 0.7630).
Net: −0.030. The library underperformed `dhs_topic` on every eval.

## Postmortem

Two mistakes, both rooted in the same approximation gap:

1. **Wrong DHS within-component weight.** I used `mean_signal` as a proxy for
   per-element NMF max-loading because the loadings file is only on Google
   Drive. But `mean_signal` is highest for *strong* peaks, which correlate
   with *invariant* (broadly-active) elements — the opposite of cell-type
   specificity. A better proxy would have been `mean_signal / numsamples` or
   `1 / numsamples`, which actually upweights specific elements. The
   baselines table is clear in retrospect: `dhs_random` (0.7089 on eval_01)
   outperforms `dhs_stratified` (0.7055) by less than 0.005, but
   `dhs_topic` beats both by ~0.014. That ~0.014 gap is the cell-type
   specificity signal, and my weighting choice almost certainly threw it
   away.

2. **Synthetic dilution didn't pay off.** I budgeted 20% synthetic (10%
   uniform + 10% dinuc-shuffled) hoping to boost eval_08, but actually
   *lost* on eval_08 (0.6671 vs dhs_topic 0.7011). The dinuc-shuffled
   bucket likely confused the model rather than serving as useful hard
   negatives at this library size. The naive linear interpolation I used
   to plan the mix is wrong: synthetic and DHS interact non-linearly.

The net story: the gap is dominated by failure mode (1). If I had used the
exact NMF loadings (or `mean_signal/numsamples`), I would likely have
landed near 0.760–0.762. The synthetic admix was a second-order decision
that turned out badly but wasn't the main loss.

## What I would try next if I had another shot

1. Obtain the full Meuleman NMF loadings matrix (Google-Drive download or
   request from authors). Sample with weight ∝ max-loading rather than
   mean_signal — closer to the exact `dhs_topic` algorithm.
2. Add ENCODE cCRE / SCREEN promoter and enhancer subsets (~1M elements)
   as a 4th bucket. cCREs are curated, validated regulatory elements with
   tighter activity signal than the broader DHS index.
3. Add a motif-implanted synthetic bucket: take random backgrounds and
   implant 1–3 known TF binding sites from JASPAR/CIS-BP at random
   positions. This is the design used by the "MPRA-IR" library design
   community and probably explains why `synth_oracle` is good for eval_08.
4. Run a small in-silico ablation: train a tiny CNN on subsets of my
   library and measure cross-eval performance. With ~50k sequences this is
   feasible in minutes per ablation. Could tune the synth/DHS ratio.
5. Add reverse-complement-augmented training pairs to test whether the
   downstream model relies on strand or not — although this is really a
   training-time decision rather than a library decision.
6. **Pure replication first, then variation.** In a one-shot run with no
   probing, the safest move is to replicate the best-known baseline as
   faithfully as possible — then add at most one small variation. I added
   two variations (synth + dinuc) AND used an unverified proxy for the
   weight function. Either decision alone might have been fine; both
   compounded.
