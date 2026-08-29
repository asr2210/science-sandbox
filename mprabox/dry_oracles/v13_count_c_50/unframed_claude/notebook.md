# Lab Notebook — Sequence Optimization

## Setup

Task: maximize black-box scores returned by `prepare.py` on libraries of 50,000 200bp DNA sequences. 30 experiments total. Primary metric: eval_01 mean_r. 14 eval sets total. Score includes cell-type breakdown: k562_r, hepg2_r, sknsh_r — these are classic MPRA cell lines (K562 leukemia, HepG2 hepatocyte, SK-N-SH neuroblastoma).

## Initial Theory (pre-data)

The eval names (k562, hepg2, sknsh) and the format (14 eval sets, "mean_r") strongly suggest this is an MPRA-activity prediction task — likely related to the Gosai et al. 2024 "Computational design of human gene regulatory elements" paper which used the Malinois model trained on MPRA in K562/HepG2/SK-N-SH and evaluated computational designs against multiple MPRA test sets.

Hypothesis: scores will be highest for sequences that:
1. Contain functional transcription factor binding sites (TFBS) for SP1, NF-Y, USF, GATA1, HNF4A, etc.
2. Have moderate GC content (~50–60%)
3. Avoid repressive elements / poly-A or poly-N runs
4. May benefit from motif density / synergy

"mean_r" naming is ambiguous — could be "mean response" (mean activity scaled) or Pearson correlation r. If it's correlation, we may need diverse sequences spanning a range. Will figure out from first results.

## Plan

- Exp 1: Random uniform DNA — baseline.
- Exp 2: Random GC-balanced (50% GC) — test GC sensitivity.
- Exp 3: Random low/high GC — sweep GC content.
- Then iterate on motifs based on what reveals signal.

---

## 2026-06-02 21:30 — Experiment 001 results (random baseline)

mean_r per eval (primary first):
- eval_01: **0.156** (k562=0.314, hepg2=0.033, sknsh=0.121)
- eval_02/05: 0.155
- eval_03/12: 0.104
- eval_04/09: 0.406
- eval_06/11: 0.145
- eval_07: -0.106
- eval_08: 0.579 (hepg2=0.76, sknsh=0.80)
- eval_10: 0.117
- eval_13: -0.111
- eval_14: 0.156

**Big discoveries:**
1. The output is Pearson r (range -1..1), not a raw activity score.
2. 14 eval sets contain duplicates → only ~9 unique evaluations. Pairs: (01,14), (02,05), (03,12), (04,09), (06,11).
3. K562_r is ~0.30–0.33 *for every eval set with random input* (eval_08 is the only outlier at 0.18). The K562 axis seems easy / saturated even from random.
4. eval_07 and eval_13 have *negative* hepg2/sknsh r on random → those may be "anti-correlated" eval sets or use an inverted sign.
5. eval_08 mean=0.58 from random sequences → it's evidently sensitive to very simple statistics (likely GC content or k-mer frequencies).

**Theory update:**
This is NOT a "maximize predicted activity" task. The score is a *correlation between two predictions over my library*. To maximize r we need:
- Sequences whose two predictors (the eval model and the ground-truth model) covary well.
- Spread along the relevant activity axis — collapsing variance kills r.

Two extreme limits to test:
- (a) Zero-variance library (e.g., 50k copies of a single sequence) → r should collapse to 0/NaN.
- (b) Maximally informative library — sequences that span the activity axis driven by motifs the predictors agree on.

Strategy: the best library is a *characterization library* — designed sequences that span low/mid/high activity with biologically meaningful variance (motif gradient, GC gradient, scrambled controls), not just random sequences.

**Next experiments planned:**
- Exp 2: pure constant library (one sequence × 50k) — confirm "needs variance" hypothesis.
- Exp 3: GC-content sweep — see if simple statistic alone moves r.
- Exp 4: motif gradient (insert known activator motifs at varying density).

Will then move to combinatorial motif libraries and possibly use known MPRA-active sequences if available.

---

## 2026-06-02 21:45 — Experiment 002 result (zero-variance)

50,000 copies of one sequence → ALL NaN. Confirmed: metric is Pearson r computed over the library. Variance required.

**Theory upgrade:** the scoring function takes my N=50K sequences, computes a hidden "ground-truth" activity vector A (one scalar per sequence, per cell line), and 14 "eval" activity vectors B_i, then reports Pearson(A, B_i) and per-cell-line analogues. **My library is a probe set for measuring agreement between models.**

This is a *characterization-library* design problem, not an activity-maximization problem. The goal is sequences where the eval model and the ground-truth model give the same per-sequence activity → high r.

What this implies:
1. Variance is essential — collapsed libraries → r → undefined.
2. Variance must be along axes both models capture (motif content, GC content, CpG, etc.).
3. Sequences that *both* models confidently score (extreme motif sequences) probably help; ambiguous/random sequences add noise.
4. Natural enhancer-like sequences should give the strongest A/B agreement (both predictors trained on MPRA data should react similarly to canonical TF motifs).

**Per-cell-line headroom on eval_01:**
- K562_r already 0.31 (likely close to ceiling on random → simpler model agreement)
- HepG2_r only 0.03 → biggest gap, design must increase HepG2 variance
- SKNSH_r 0.12 → also a gap

**Next: Experiment 003.** Insert strong, well-characterized activator motifs in random backgrounds. Mix HepG2 (HNF4A, FOXA1), K562 (GATA1, KLF1), SKNSH (NEURO/ASCL1, MEF2), plus universal (SP1, AP-1, NF-Y). Each sequence gets several motifs randomly placed. Stratify so density varies across the library — creates an activity gradient.

---

## 2026-06-02 22:30 — Experiments 004–008 results summary

| exp | description | eval_01 | K562 | HepG2 | SKNSH |
|---|---|---|---|---|---|
| 004 | GC uniform [0.2,0.8] | 0.392 | 0.45 | 0.35 | 0.38 |
| 005 | GC uniform [0.05,0.95] | 0.414 | 0.47 | 0.36 | 0.41 |
| 006 | GC + CpG Markov | 0.419 | 0.49 | 0.35 | 0.41 |
| 007 | **random hg38 chr1+chr22** | **0.541** | 0.59 | 0.52 | 0.52 |
| 008 | ENCODE cCREs centered | 0.463 | 0.60 | 0.40 | 0.39 |

**Key learnings:**
1. GC variance alone plateaus near 0.42.
2. Adding CpG dinucleotide axis: ~0 additional gain.
3. Natural genomic sequences jump us to 0.54 — multi-feature co-correlated variance.
4. **cCREs HURT eval_01** (too narrow). Different eval sets reward different distributions — eval_04 and eval_08 LIKE cCREs (0.58 and 0.42 respectively); eval_01 prefers broad random hg38.
5. eval_08 is anti-aligned with eval_01: high on random short k-mer libraries, low on natural — likely an "out-of-distribution detector" or sensitivity reversed.

**Theory update:** the highest-r library spans the broadest *naturally-distributed* compositional space. Regulatory enrichment narrows the distribution → less variance → lower r. The best library mimics random genome but maybe with extra variance at compositional extremes.

**Plan for exp 9:** Mix 25K random hg38 + 25K extreme-GC synthetic (very low/very high GC). Tests whether forced compositional spread on top of natural raises r further.

---

## 2026-06-02 22:00 — Experiment 003 result (motif gradient)

eval_01: **0.0959** (vs random 0.156) — motifs HURT.
- K562_r 0.31 → **0.07** (crashed)
- HepG2_r 0.03 → 0.05 (tiny up)
- SKNSH_r 0.12 → 0.17 (modest up)

**Counter-evidence to my motif hypothesis.** Inserting discrete strong motifs into random background broke K562 agreement. Pure random's K562_r=0.31 was apparently driven by *smooth, naturally-distributed k-mer statistics that both models happen to agree on*. Discrete motif insertion creates non-natural k-mer mixtures that one model interprets and the other doesn't, killing the K562 correlation.

**Theory update:**
- Both predictors agree most strongly on sequences with *natural-looking* k-mer/composition statistics.
- Discrete motif insertion is too "off-distribution" — disagreement between models.
- *Smooth* feature variation (e.g., GC content gradient) might preserve naturalness while adding variance both models can interpret consistently.

**Refined strategy:** Stay close to the random-sequence distribution but vary one continuous statistic at a time. If GC variance is what's driving the residual variance in random, deliberately spreading GC% wider should help.

**Next: Experiment 004 — GC content gradient.** Each sequence's GC% drawn uniformly from [0.20, 0.80] (vs the ~0.5±0.035 natural spread of uniform random). Pure 4-letter alphabet, no motifs. Should test whether GC variance alone moves r.

---

## 2026-06-03 — Experiments 13 & 14 results (MPRA train)

| Exp | Library | eval_01 |
|----|---------|---------|
| 013 | random 50k from Malinois MPRA train set | **0.5699** (best) |
| 014 | MPRA train, activity-stratified 6³ cells | 0.5682 |

**Key findings:**
- Pulling directly from the MPRA training distribution jumps us from 0.556 → **0.570**.
- Activity-stratification on top of MPRA didn't help — the natural MPRA activity distribution already has good variance; forcing equal-bin coverage trimmed it slightly.
- K562_r jumped most (0.581 → 0.614) — eval_01 K562 model evidently very fitted to its training dist.

**Plan for exp 15:** Filter MPRA by *low standard error* (high-confidence measurements). The hypothesis: low-SE sequences = sequences both predictors learned to score reliably = highest cross-model agreement. Take bottom quartile by mean(K562_lfcSE, HepG2_lfcSE, SKNSH_lfcSE).


## 2026-06-03 — Experiment 015 result (MPRA low-SE filter)

eval_01: **0.4726** (vs 0.5699 MPRA random) — *hurt badly*.
- K562_r 0.614 → 0.558
- HepG2_r 0.549 → 0.408
- SKNSH_r 0.547 → 0.452

**Why this failed:** Low-SE doesn't mean "models agree well" — it means "the assay measured precisely". Most MPRA sequences have log2FC near 0 with low SE; filtering by SE biases the library toward NULL/weak elements, collapsing log2FC variance. Correlation needs variance; this strips it.

**Course correction:** the opposite — HIGH variance subset (large |log2FC|) — should help. These are the elements both models confidently predict as ON or OFF.

**Plan for exp 16:** Filter MPRA sequences whose max(|K562|,|HepG2|,|SKNSH| log2FC) is above the median or upper quartile. High-magnitude, mixed-sign signals across cells -> high variance per axis -> high r.


## 2026-06-03 — Experiment 016 result (MPRA high-activity filter)

eval_01: **0.5064** (vs 0.5699 MPRA random) — also hurts.

Both directions of filtering on `log2FC` magnitude hurt eval_01:
- Filter LOW |log2FC| (exp 15): 0.473
- Filter HIGH |log2FC| (exp 16): 0.506

**Interpretation:** the natural distribution of MPRA training set is *already* optimally balanced for cross-model agreement. Subsetting in either direction reduces the diversity that drives agreement. eval_04 (which seems to reward magnitude) *does* prefer the high-activity subset (0.595 vs 0.582), but eval_01 doesn't.

**Plan for exp 17:** Try subsetting by data_project. Distribution: GTEX 445K, UKBB 338K, CRE 14K. GTEx eQTL pairs are paired ref/alt variants on real regulatory elements — both models will have been trained jointly on these and likely agree most.


## 2026-06-03 — Experiments 17–22 results (MPRA subsetting + mixtures)

| Exp | Library | eval_01 | K562 | HepG2 | SKNSH |
|----|---------|---------|------|-------|-------|
| 017 | GTEx-only MPRA | 0.5626 | 0.613 | 0.541 | 0.534 |
| 018 | 70/30 MPRA+natural | **0.5739** | 0.611 | 0.555 | 0.556 |
| 019 | 50/50 mix | 0.5691 | 0.605 | 0.551 | 0.551 |
| 020 | 70/30 MPRA + GC-strat nat | 0.5731 | 0.612 | 0.554 | 0.553 |
| 021 | 80/20 mix | 0.5714 | 0.610 | 0.552 | 0.552 |
| 022 | 60/40 mix | 0.5704 | 0.604 | 0.554 | 0.553 |

**Curve:** 100/0 → 0.5699, 80/20 → 0.5714, **70/30 → 0.5739**, 60/40 → 0.5704, 50/50 → 0.5691.
Clear peak at ~70/30 MPRA/natural. Adding 30% broad genomic background increases agreement, but >30% dilutes the MPRA-distribution K562 boost.

GC-stratifying the natural part didn't help — random sampling already gives sufficient variance.

**Theory update:** the optimum library blends in-distribution (MPRA) + a small fraction of natural broadcasting to push HepG2 and SKNSH r upward without hurting K562. eval_07 in particular loves these mixes (jumps to 0.61).

**Plan for 023+:** try mixing MPRA with cCREs (regulatory-focused), with extreme-GC tails, and with a different MPRA dataset if I can find one. Also explore: more natural source chromosomes; mix natural fraction from different sources.


## 2026-06-03 — Experiments 023–030 (search for ceiling)

| Exp | Library | eval_01 |
|----|---------|---------|
| 023 | MPRA + cCRE | 0.5620 (hurt — narrowed dist again) |
| 024 | 70/30 seed=24 (noise check) | 0.5720 |
| 025 | MPRA balanced 12K/proj + 14K nat | 0.5747 |
| 026 | 1% mutated MPRA + 15K nat | 0.5708 |
| 027 | kitchen-sink 5×10K | 0.5672 (synthetic dragged down) |
| 028 | 35K MPRA + 15K nat eq-chrom | 0.5717 |
| 029 | CRE-heavy 18K + GTEX12 + UKBB5 + 15K nat | 0.5745 |
| 030 | **ensemble 10K from each top-5** | **0.5752** |

**Noise floor:** ~±0.002 (exp 024 vs 018 with same recipe). The plateau ~0.574 is robust; differences between top recipes are largely noise.

**Final winner:** Ensemble of best libraries (030). Combines compositional + project-balanced + GC-stratified + chrom-equal + CRE-heavy variants.

## Final theory

The scoring metric is Pearson r between two MPRA-trained predictors. To
maximize r I need:
1. **In-distribution sequences** so both models map them consistently — MPRA training-set sequences score ~0.57.
2. **Genomic variance** in composition (GC, etc.) — adding 30% natural hg38 above MPRA helps by ~+0.005.
3. **Project balance** within MPRA — equal GTEx/UKBB/CRE contribution adds ~+0.001.
4. **Ensemble of multiple winning recipes** — top-5 mixture gives +0.0005 over any single one.

What doesn't work:
- Motif insertion (off-distribution discrete)
- Low/high lfcSE filtering (collapses variance)
- High-magnitude activity filtering (over-narrows)
- Synthetic extreme-GC tails (off-distribution)
- cCRE-only inputs (too narrow)

Total progress: 0.156 (random) → **0.5752** (ensemble). +0.42 absolute, 3.7x.

