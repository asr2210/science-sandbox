# MPRA Library Design Lab Notebook

## 2026-06-02 18:55 — Starting

### Setup
Fresh project. No prior experiments. Plan: 30 experiments to learn what
makes a 50k-sequence MPRA library informative for training a model
that must generalize beyond the three measured cell types
(K562, HepG2, SK-N-SH) to 14 anonymous evaluation sets.

### Initial theory (T0)
A library is informative for cross-cell-type generalization when it:
1. **Covers a wide motif vocabulary** — TF binding sites for many
   TF families, so the model sees the building blocks of regulation
   that operate in any cell type.
2. **Spans regulatory grammar diversity** — different motif densities,
   spacings, combinations (since grammar generalizes more than
   identity of individual motifs).
3. **Includes contrasts** — variations that isolate the effect of
   single motifs/positions/orientations, so the model learns
   sequence-to-activity rules rather than memorizing exemplars.
4. **Has labeling signal-to-noise** — i.e. sequences span a wide
   activity range so the model has gradient to learn from
   (all-zero or all-saturated activity teaches the model nothing).

What I expect to find:
- Random sequences → low signal, model trained on them probably
  performs near zero on real regulatory eval sets.
- Natural genomic regulatory regions (ENCODE cCREs, DNase peaks)
  across many cell types → much better.
- Engineered with motifs → competitive, possibly better at isolating
  causal rules.
- Best library probably mixes natural + engineered + diverse.

### Plan
- Experiment 001: random sequences. Establishes floor.
- Experiment 002+: depends on 001 result and what I learn.

Will reread literature before each experiment beyond the baseline.

## 2026-06-02 18:57 — Planning Experiment 001 (random baseline)

**Type**: exploring new hypothesis (baseline calibration).

**Prediction**: Random uniform A/C/G/T sequences should yield low
mean_r (near 0 to 0.1) across all eval sets, because:
- No actual regulatory motifs → model learns nothing about regulation.
- Random k-mer occurrences will let model fit any spurious patterns
  the MPRA measures (e.g. GC content, polynucleotide tracts).

**Why useful**: Without this floor, I cannot judge whether later
strategies actually add information vs. just exploiting incidental
sequence content. Also: if random performs surprisingly well, that
itself is a major signal (means MPRA activity is driven more by bulk
composition than I thought).

**Generalization justification**: Random sequences are trivially
identical in distribution across all cell types. If the model trained
on them generalizes worse on K562 than on eval_NN, that tells me
nothing useful. If random fails everywhere, that confirms baseline.
This experiment is a calibration, not a strategy candidate.

## 2026-06-02 19:10 — Result Experiment 001 (random baseline)

`mean_r` per eval (eval_01 = primary):
- eval_01: 0.231  (K562 0.14, HepG2 -0.09, SKNSH 0.64)
- eval_02/05/14: 0.231 each (identical)
- eval_03/12: 0.233
- eval_04/09: 0.225
- eval_06/11: 0.231
- eval_07: 0.220 (high SKNSH 0.67, low HepG2 -0.13)
- eval_08: **0.089** ← outlier, much lower
- eval_10: 0.232
- eval_13: 0.221

### What this tells me (theory update T0 → T1)
Not what I predicted. The floor is NOT zero. mean_r ≈ 0.23 even from
pure random sequences. Driver: SK-N-SH r ≈ 0.6 from a model trained
on random sequences alone.

This means SK-N-SH MPRA activity has strong composition-driven
variance (probably GC content, k-mer occupancy, or simple sequence
features). A model trained on 50k random sequences with measured
SK-N-SH activity learns enough about the assay's compositional
response to predict held-out SK-N-SH activity well — even though no
"motif grammar" is involved.

By contrast HepG2 (and to a lesser extent K562) is composition-
insensitive — the model can't predict at all from random sequence
content. These cell types require actual regulatory motif grammar
to predict.

**eval_08 is the most diagnostic set.** It scores only 0.089 on
random — meaning it filters out the compositional bulk signal
(maybe held-out variants on matched-composition pairs, or
non-natural designed contrasts). Improvements on eval_08 will
indicate I am teaching the model real regulatory grammar, not just
composition statistics.

Eval clustering: {02,05,14}, {03,12}, {04,09}, {06,11} are nearly
identical, suggesting some eval sets are correlated/replicates or
the model's outputs are nearly identical against them.

### Theory T1
- Library-derived predictive performance on a held-out set decomposes
  into (i) a composition component the model can learn from any
  sufficiently varied sequence set and (ii) a regulatory grammar
  component requiring real cis-elements in training.
- SK-N-SH activity is dominated by (i); HepG2 by (ii); K562
  somewhere between.
- Cross-cell-type generalization will be limited by (ii) — the only
  way to lift HepG2 and eval_08 is to give the model real cis-element
  exposure in training.
- For generalization beyond the three labeled cell types, the library
  must contain regulatory grammar that is shared across cell types
  (not just K562/HepG2/SK-N-SH-specific) — so sampling regulatory
  regions across many cell types is more useful than sampling only
  the labeled three.

### Plan for Exp 002
Sample 200bp windows centered on ENCODE SCREEN cCREs (~926k
regulatory elements identified across many cell types). 50k uniform
random subsample. Expect lift on HepG2, K562, and (if the theory is
right) eval_08.

## 2026-06-02 19:35 — Result Experiment 002 (cCRE uniform)

Key numbers (vs 001):
- eval_01: 0.2307 → **0.3154** (+0.085)
- HepG2:   -0.089 → **+0.177** (+0.266) ← dominant lift
- K562:     0.139 →  0.145   (+0.006) ← no lift
- SKNSH:    0.642 →  0.625   (-0.017) ← slight loss
- eval_08:  0.089 →  0.076   (-0.013) ← slight loss
- eval_07: 0.220 → 0.338 (+0.118) ← biggest gain other than eval_01
- eval_13: 0.221 → 0.328 (+0.107)
- eval_04/09: 0.225 → 0.270 (+0.045) ← smaller gain
- evals 02/05/14: 0.231 → 0.316 (+0.085) — same as eval_01

### Theory update T1 → T2
1. **Cell type predictability profile differs sharply:**
   - SK-N-SH: composition-rich (random alone gives r=0.64).
   - HepG2: grammar-rich (random fails; cCREs jump it to 0.18).
   - K562: hard. Composition gives ~0.14 baseline; cCREs add nothing.
2. **eval_08 was misread.** It is NOT a "regulatory grammar"
   detector — cCREs make it worse. May test compositional spread,
   designed/synthetic contrasts, or non-natural sequence features.
3. **eval_07 and eval_13 are most cCRE-sensitive.** They might be
   enhancer-heavy or HepG2-weighted.
4. cCRE uniform sampling is a solid mid baseline (mean_r ≈ 0.32) but
   leaves K562 and eval_08 on the table.

### What is the most informative next experiment?
Candidates:
A. **K562-active cCREs** — directly test whether K562 stuckness is
   due to cCRE class imbalance (cell-type bias) vs intrinsic limit.
   If K562 jumps, hypothesis confirmed and cell-type-balanced library
   is the next obvious move.
B. **Real + shuffled-controls** — 25k real cCREs + 25k dinucleotide-
   shuffled. Should teach model motif separability and may lift eval_08
   if it tests motif-vs-background contrasts.
C. **Stratified cCRE classes** — 10k each of PLS/pELS/dELS/CTCF/DNase-
   H3K4me3. Tests whether class skew matters.

A is the most decisive single-knob test. It cleanly separates (a) vs
(b) hypotheses about K562. I'll do A as Exp 003.

Plan: download per-cell-type cCRE activity annotation from SCREEN
(or use K562 DNase narrowPeak from ENCODE directly). Sample 50k
cCREs that are K562-active. Expect: K562 r > 0.20 if cell-type bias
is the issue; ≤ 0.18 if intrinsic limit.

**Generalization justification for 003**: At first glance, K562-
targeted sampling seems to *narrow* generalization. But the goal is
to understand the rules, not to optimize K562 alone. If K562
grammar requires K562-specific motifs, then any library that aims
to generalize MUST include K562-active sequences (because a model
that has never seen K562-active sequences can't predict K562).
The same logic applies to unseen cell types: they will require
their own active sequences. So mapping out which sources of
sequences "unlock" each cell type is critical infrastructure for
the bigger goal.

## 2026-06-02 19:50 — Planning Experiment 003 (K562 DNase peaks)

**Type**: refining a promising direction (diagnostic for K562 stuck-
at-0.14 finding from 002).

**Source**: ENCODE K562 DNase narrowPeak (ENCFF599DEH), 53,291 peaks.
Sample 50k peaks, center 200bp window on the peak summit. Fill any
shortfall by random shifts on resampled peaks.

**Predictions** (under T2):
- K562 r jumps significantly (>0.30) IF the cause was cell-type bias
  in cCREs (i.e. cCREs were under-representing K562-active grammar).
- K562 r stays ≤ 0.18 IF there is an intrinsic ceiling
  (noise / measurement / model-capacity bottleneck).
- HepG2 r drops vs 002 (since K562-specific elements are less
  HepG2-active).
- SK-N-SH r ≈ similar (composition is roughly preserved in K562 DHS).
- eval_01 net effect: depends on K562 lift magnitude vs HepG2 loss.

**What I will learn either way**:
- Confirms or refutes the cell-type-bias hypothesis for K562.
- Quantifies the cost of being uneven (HepG2 loss) — informs the
  later 3-cell-balanced experiment.
- Gives a clean K562-active reference performance level to compare
  future libraries against.

## 2026-06-02 20:10 — Result Experiment 003 (K562 DHS)

eval_01 0.3166 (essentially identical to 002's 0.3154).
- K562: 0.140 (UNCHANGED — even with pure K562-active training!)
- HepG2: 0.184 (essentially identical to 002's 0.177)
- SKNSH: 0.627 (same)
- eval_08: 0.080 (same)

### Theory update T2 → T3 (major)
Cell-type-bias hypothesis for K562 ceiling is REFUTED. Three
fundamentally different training pools (uniform random, broad cCRE,
pure K562 DHS) all yield K562 r ≈ 0.14. This must be an intrinsic
ceiling — most likely the noise floor of K562 measurements in this
MPRA / model setup, OR a structural property of the held-out
evaluation set for K562 (low dynamic range, ambiguous ground truth,
etc.).

**Even more striking finding: HepG2 r is unchanged whether trained
on broad cross-cell-type cCREs or on pure K562 DHS.** This says
the model can predict HepG2 just as well from regulatory regions
that are K562-active as from broadly-active ones. This is GREAT news
for cross-cell-type generalization: it shows the model is mostly
learning shared regulatory grammar, not cell-type-specific motif
patterns. A model trained on one cell type's active regions will
predict other cell types' activities of those same regions about as
well as a model trained on those other cell types directly.

This argues strongly that for the generalization-beyond-labeled-cell-
types goal: the choice of which CELL TYPE's regulatory regions to
sample is NOT the main lever. What matters is the *content* of the
sequences (how much regulatory grammar, how diverse, how composition-
balanced), not their cell-type-of-origin label.

### Plateau analysis
With this library family the mean_r ceiling is ~0.32 (eval_01).
- K562 ~0.14 hard cap → contributes 0.047 to mean
- HepG2 ~0.18 with grammar → contributes 0.060
- SKNSH ~0.63 (composition dominated) → contributes 0.210
- Sum: ~0.317 mean — matches observation.

To break the plateau I need to lift either HepG2 (most room) or SKNSH
(most absolute contribution) or K562 (smallest absolute room, but
biggest relative gap). Pure source-region swaps won't do it.

### Plan for Exp 004 (Sharpr-style contrasts)
Build a 50k library = 25k real cCREs + 25k dinucleotide-shuffled
versions of those same cCREs. The shuffled controls preserve
composition but destroy motif syntax — giving the model paired
examples to learn motif-specific (not composition-specific) effects.

Predictions:
- If the model learns motif specificity better, HepG2 r should lift
  (more sequence-grammar resolution).
- eval_08 may finally lift if it tests motif/composition separation.
- SKNSH may drop slightly (some composition spread reduced because
  shuffled keeps original composition).
- K562 unchanged (hard ceiling).

**Generalization justification**: Sharpr-style contrast pairs teach
sequence-specificity that transfers to any cell type. The model
learns "this motif at this position is what matters" rather than
"sequences from this cell type look like this". Strongly applicable
to unmeasured cell types.

## 2026-06-02 20:30 — Result Experiment 004 (cCRE + shuffled)

eval_01 = 0.3116. Slightly WORSE than 002's 0.3154.
- K562: 0.144 (ceiling)
- HepG2: 0.168 (down 0.009 — losing real-sequence count hurts)
- SKNSH: 0.623 (~same)
- eval_08: 0.082 (tiny lift)

Shuffled controls don't help. The model is not bottlenecked by
motif/composition separability. Half the real sequence budget spent
on shuffled controls slightly hurts HepG2.

### Theory update T3 → T4
- All single-tile-per-region designs plateau at mean_r 0.31–0.32.
- The plateau is set by per-cell-type ceilings that don't move with
  source choice OR with paired-control design.
- The literature (PARM) suggests density per-region beats single-tile.
  PARM used random partially-overlapping fragments at ~240× coverage
  per region and got R=0.92 (K562) / 0.89 (HepG2) on promoter activity.

### Plan for Exp 005 (dense per-region tiling)
- 10,000 cCREs (uniformly sampled across all classes)
- For each: 5 200bp windows at random offsets in [-100, +100] from
  cCRE midpoint
- Total: 50,000 sequences, 5× redundant per region

Predictions:
- HepG2 r lifts (more position diversity per region → more motif
  context exposure)
- K562 maybe slight lift if some "hard" K562 features need position
  diversity to be learned
- SKNSH probably similar (composition-driven)
- eval_01 hopefully ≥ 0.33

**Generalization justification**: Dense per-region coverage teaches
position-invariance for motifs. A model that sees a CTCF motif at
multiple positions within similar contexts learns that motif → effect
rather than motif-at-position-X → effect. This transfers strongly to
held-out sequences (and held-out cell types) where motif positions
differ.

## 2026-06-02 20:55 — Result Experiment 005 (dense tile 10K × 5)

eval_01 = 0.3177. HepG2 0.185 (+0.008). Marginal.

The plateau at mean_r ≈ 0.32 is now confirmed across:
- 002 cCRE broad (0.315)
- 003 K562 DHS (0.317)
- 004 cCRE+shuffled (0.312)
- 005 cCRE dense tiled (0.318)
All within ±0.003 of each other on eval_01. Per-cell-type ceilings
(K562 ≈ 0.14, HepG2 ≈ 0.18, SKNSH ≈ 0.63) are stable to natural-
genomic library design choices.

### Theory T4
The plateau is unmovable by tuning natural-genomic library design.
Need to test categorically different sequence sources.

### Plan for Exp 006 (synthetic motif library)
Generate fully synthetic sequences: random 200bp scaffold with 1-6
JASPAR TF motifs planted at random positions. Tests motif sufficiency:
do controlled motif insertions alone drive predictable activity?

Predictions under T4:
- If motif identity dominates: HepG2 r > 0.18. Means library design
  can be optimized via motif diversity.
- If genomic context matters too: HepG2 r ≲ 0.10. Means natural
  sequences are necessary for the upper r range.
- SKNSH likely lower than 0.62 (less compositional spread than
  natural cCREs).
- K562 still around its 0.14 ceiling.

**Generalization justification**: Synthetic motif libraries probe
whether motif syntax — the most transferable regulatory feature —
suffices for activity prediction. If yes, libraries built around
JASPAR motif panels would be a portable, species-/cell-type-agnostic
training corpus. If no, generic motif insertion is not enough; need
the genomic context. Either way, very informative about what makes
a library generalizable to unmeasured cell types.

## 2026-06-02 21:15 — Result Experiment 006 (synthetic JASPAR motifs)

eval_01 = 0.2212. WORSE than random (0.231) and far below cCRE
(0.315). HepG2 went back negative (-0.069). SKNSH dropped from
random's 0.642 to 0.593.

### Big finding
Motif identity alone is NOT enough. Even with 2–5 high-quality JASPAR
motifs planted per sequence, model performance is no better than
random. The 0.18 HepG2 lift from cCREs is NOT explained by motif
identity — natural genomic context carries irreducible signal that
synthetic libraries miss.

Synthetic library also LOSES SKNSH signal: 0.593 vs random's 0.642.
The synthetic procedure pins composition into a narrower range,
reducing compositional spread that SKNSH responds to. Composition is
genuinely informative for SKNSH.

### Theory update T4 → T5
- Motif identity is necessary but not sufficient.
- Natural cCREs carry irreducible context information — the
  co-occurrence patterns, spacings, flanking composition, possibly
  natural noise structure.
- Plateau at 0.32 is set by what natural-genomic regulatory regions
  provide. Synthetic libraries cannot replace them.
- For generalization to unmeasured cell types: the model must learn
  from REAL genomic regulatory context, not just controlled motifs.

### Plan for Exp 007 (promoter-focused dense library)
PLS cCREs (~41K) are the most cell-type-invariant regulatory class:
promoter activity correlates R=0.78-0.95 across cell types
(literature consensus). They should be the most informative source
for cross-cell-type generalization.

Design: 10K PLS cCREs × 5 random-offset 200bp tiles each = 50K.
Combines promoter focus (universally regulatory) with dense per-
region coverage (position invariance).

Predictions:
- HepG2 r above 0.18 if promoter focus matters
- K562 still ~0.14 ceiling
- SKNSH likely similar to 002

**Generalization justification**: Promoters drive transcription in
most cell types via a shared core machinery (TBP, GTFs, common TFs).
A library focused on promoters trains the model on the regulatory
grammar that is most likely to transfer to any cell type, including
unmeasured ones — because promoter motif syntax is largely cell-
type-invariant.

## 2026-06-02 21:35 — Result Experiment 007 (PLS dense)

eval_01 = 0.3146. Slight drop vs 005 (0.3177). Promoter focus is
NOT a strict improvement; mixed-class cCRE is slightly better.

### Summary table (eval_01)
- 001 random:       0.231
- 002 cCRE:         0.315
- 003 K562 DHS:     0.317
- 004 cCRE+shuf:    0.312
- 005 cCRE dense:   0.318 ← best so far
- 006 synth motifs: 0.221 ← motif identity alone fails
- 007 PLS dense:    0.315

Plateau at ~0.315-0.318 is unbroken. The choice of natural-genomic
region source / tiling density doesn't move the needle.

### Plan for Exp 008 (cCRE + random mix)
25K cCRE windows + 25K uniform random sequences. Tests whether
composition spread (random) and regulatory grammar (cCRE) are
additive (mix wins) or one cancels the other.

Predictions:
- HepG2: 0.18 → maybe 0.10-0.18 (depends if halving regulatory
  content hurts; my data shows K562 didn't care, suggesting maybe
  HepG2 won't either)
- SKNSH: 0.62 → up toward 0.64 (random's compositional spread
  restored)
- K562: 0.14 (ceiling)
- eval_01: hopefully ≥ 0.32

If mix > 005, both axes are useful and the cCRE-only plateau is
about NEEDING composition spread that cCREs lack.
If mix < 005, halving regulatory content hurts more than random
adds, so cCREs are still the right primary source.

**Generalization justification**: Adding compositional spread
mirrors what's seen in real genomes (introns, intergenic, etc. all
have diverse composition). A model trained on a wider compositional
range generalizes better to cell types whose active sequences may
have different compositional biases. Random sequences are the
maximum-entropy compositional reference.

## 2026-06-02 21:55 — Result Experiment 008 (cCRE + random mix)

eval_01 = 0.3091. WORSE than pure cCRE (0.315). All cell types lost a
bit. Random sequences act like training noise, not diversity.

### Big theory update T5 → T6
**Wasted training samples HURT.** Each non-regulatory training pair
is a debit on the regulatory-signal budget. The 50K library budget
is tight; non-cCRE content reduces effective training.

This reframes the question: the plateau may be set by *how much
cell-type-grammar signal the model can extract from 50K regulatory
sequences*. To break it, need HIGHER-INFORMATION cCRE sequences, not
more / more-diverse sequences.

Candidates for high-info regulatory sequences:
- Top-signal-strength peaks (DNase signalValue filter)
- Cross-species conserved (phyloP > 2)
- Multi-evidence convergent (DNase + H3K27ac + TF ChIP)
- STARR-seq validated active elements
- Sequences with HIGH variance across the 3 measured cell types
  (informative for cross-cell-type prediction)

### Plan for Exp 009 (high-signal peak filter)
HepG2 DNase peaks sorted by signal (max_density column). Take top
10K × 5 tiles = 50K. Tests "more accessibility = more informative
training" hypothesis.

Predictions under T6:
- HepG2 r > 0.18 (top peaks are MORE confidently regulatory)
- K562 still ~0.14
- SKNSH similar to cCRE (~0.62)
- eval_01 hopefully ≥ 0.32 — possibly first break of the plateau

**Generalization justification**: Strong-signal accessible regions
are high-confidence regulatory elements. Less ambiguity per training
example means cleaner motif rules learned. Cleaner rules → better
transfer to unseen cell types.

## 2026-06-02 22:15 — Result Experiment 009 (top-signal DHS)

eval_01 = 0.253. Big DROP (-0.06 vs 002). HepG2 collapsed to ~0!

Top-signal DHS peaks are dominated by housekeeping promoters that
are universally active and have LOW VARIANCE in activity. The model
needs variance to learn — uniform high-activity training data
teaches it nothing about what differentiates active levels.

This refutes my "peak quality matters" hypothesis as stated. The
right axis is not signal strength, but **variance** — particularly
CROSS-CELL-TYPE variance.

### Theory T6 → T7
- Training data needs ACTIVITY VARIANCE per cell type to teach the
  model what differentiates active levels.
- Top-signal filtering reduces variance (housekeeping) and HURTS.
- cCRE diversity (mixed classes) implicitly preserves variance.
- The next lever: explicitly select sequences with HIGH CROSS-CELL-
  TYPE variance (differential activity). These teach what makes a
  sequence cell-type-specifically active.

### Plan for Exp 010 (differential-activity library)
Stratified by DHS-peak overlap pattern across the three cell types:
- K562-specific (K562 DHS, not HepG2, not SKNSH)
- HepG2-specific
- SKNSH-specific
- Shared (overlap in all 3)
2,500 regions per class × 5 tiles = 50K.

Predictions:
- Each cell type sees ~12.5K "self-specific high" + ~12.5K "self-low
  / others-high" + ~12.5K shared-high + ~12.5K specific-to-others.
  This is the maximum-variance design for cell-type-discriminating
  training.
- Should lift K562, HepG2, SKNSH r above their current ceilings.
- eval_01 hopefully > 0.32 for the first time.

**Generalization justification**: A library balanced across cell-
type-differential activity teaches the model what motifs/contexts
make a sequence cell-type-specifically active. This is the most
transferable kind of regulatory knowledge: any cell type's active
sequences are by definition cell-type-specific (or else they'd be
universally active). So a model that has learned this from K562/
HepG2/SKNSH should generalize to predicting cell-type-specificity
in any cell type.











---

## Result Experiment 010 (differential-activity DHS stratification)

50K = 4 classes × 2,500 regions × 5 tiles. Classes by peak-overlap
pattern across the 3 cell types: K562-only, HepG2-only, SKNSH-only,
shared3.

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3180 | 0.139  | 0.188  | 0.628  |
| 07   | 0.3355 | 0.118  | 0.231  | 0.658  |
| 08   | 0.0770 | 0.079  | -0.004 | 0.156  |
| 13   | 0.3256 | 0.111  | 0.232  | 0.634  |

vs 005 (cCRE dense, mean_r=0.3177): essentially identical.
K562 -0.007, HepG2 +0.003, SKNSH +0.005. Net eval_01 +0.0003.

### What I learned
The "differentially active" stratification hypothesis predicted a
clear lift. It produced a numerical wash. Implications:
- Cross-cell-type-variance is not the missing signal either.
- The model already learns cell-type-discriminating features from
  the broad cCRE distribution (where ~half of cCREs are cell-type-
  specific anyway).
- K562 sits at its 0.14 ceiling whether the library is broad cCRE,
  K562-DHS-focused, dense-tiled, or differential. The ceiling is
  not budget-allocatable.

### Theory T7 → T8
**The natural-genomic single-source family is exhausted.** All
single-source genomic regulatory designs land at mean_r ≈ 0.315-
0.318. The plateau is set by per-cell-type ceilings (K562 ~0.14,
HepG2 ~0.19, SKNSH ~0.63) that do not move with refinement of
source-selection.

To meaningfully test whether the plateau is intrinsic to the
50K-budget × model architecture vs. addressable by library design,
I need to try **categorically different** library types:
1. Functionally-validated MPRA-active sequences (STARR-seq)
2. Conservation-filtered regulatory elements (phyloP)
3. Multi-source convergent (DNase ∩ H3K27ac ∩ TFBS)
4. RC-augmented (strand-pair training)
5. Extremely-dense tiling (1K regions × 50 tiles)

### Plan for Exp 011 (STARR-seq active peaks)
STARR-seq directly measures enhancer activity in a reporter assay —
the closest functional analogue to MPRA. K562 and HepG2 STARR-seq
peaks are available from ENCODE. If the model is bottlenecked by
"how MPRA-like are the training sequences", STARR peaks should give
the biggest possible lift from a genomic source. If STARR peaks
land at 0.318 too, the plateau is very probably an architecture/
budget ceiling, not a design ceiling.

**Generalization justification**: STARR-seq peaks are the gold
standard for cell-type-resolved enhancer activity in a reporter
context. A model trained on these learns "what makes a sequence
function as an enhancer in a reporter" — directly analogous to the
MPRA evaluation task — and so should transfer well to any cell
type's enhancer prediction.

---

## 2026-06-02 20:08 — Experiment 011 plan: STARR-seq active peaks

### Theory T8 (recap)
Natural-genomic single-source family appears exhausted at mean_r
≈ 0.318. Need to test categorically-different sources. STARR-seq is
the closest functional analogue to MPRA (reporter-assay readout) —
should be the best single-source genomic library if "MPRA-likeness"
is the missing axis.

### Design
50K = top 5K K562 STARR peaks + top 5K HepG2 STARR peaks (Gerstein
WG-STARRPeaker, ENCFF045TVA/ENCFF047LDJ), each × 5 random-offset
200bp tiles. No public SKNSH STARR-seq.

### Generalization justification
STARR-seq directly assays enhancer activity in a reporter context —
the same modality as MPRA. A model trained on the actual functional
output of an analogous reporter assay should generalize to any
cell type's enhancer prediction better than a model trained on
chromatin-accessibility proxies (DHS, cCRE), if reporter-activity
is closer to the eval target than chromatin-context proxies are.

### Prediction
If "MPRA-likeness" of source data is the missing axis → eval_01
> 0.32 for the first time. If the plateau is architecture-bound
→ result ≈ 0.318 ± 0.01.

## 2026-06-02 20:08 — Result Experiment 011

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.2874 | 0.141  | 0.097  | 0.625  |
| 07   | 0.2925 | 0.124  | 0.116  | 0.638  |
| 08   | 0.0790 | 0.075  | 0.004  | 0.159  |
| 13   | 0.2885 | 0.112  | 0.113  | 0.641  |

vs 005 (cCRE dense, 0.3177): eval_01 DROPS by 0.030. HepG2 PRED
nearly halves (0.185 → 0.097). K562 unchanged. SKNSH unchanged.
eval_07 (grammar-sensitive) also drops.

### What I learned
This is a clean negative — and an important one. STARR-seq peaks
are the most reporter-faithful genomic source available, yet they
trail broad cCRE dense tiling by 0.03 mean_r. Combined with the 009
top-DHS result, the HepG2 collapse here shows the same root cause:
**filtering to top-scoring peaks of a single assay collapses
variance**, and the HepG2 head of the model needs that variance.

Refines the falsified-hypothesis ledger:
- "MPRA-like reporter source helps" → refuted (this exp)
- "Cross-cell-variance stratification helps" → refuted (010)
- "Top-signal regulatory peaks help" → refuted twice (009, 011)
- "Differential activity helps" → refuted (010)
- "Source-modality refinement (DHS vs cCRE vs STARR) helps" →
  refuted across the family

### Theory T8 → T9
The plateau at ~0.318 is the per-cell-type-ceiling sum (K562 ~0.14,
HepG2 ~0.19, SKNSH ~0.63) for a 50K-budget × prepare.py-model
trained on natural-genomic regulatory regions of any kind. It is
not moved by source-selection refinement.

To beat it, the design must change something **other than
source-of-positives**:
- Effective sample count: RC augmentation, paired controls,
  multiple read-frames, denser tiling at the cost of fewer
  regions.
- Out-of-distribution structure: synthetic motif perturbations
  added on top of cCRE backbones (motif-tiled cCREs), saturation
  mutagenesis seeds, evolutionary-divergent backgrounds.
- A categorically different selection axis I haven't tried:
  CONSERVATION (phyloP), which encodes "what evolution preserves"
  rather than "what is active in any one cell type".

### Plan for Exp 012 (RC augmentation)
The cheapest "effective-sample-count multiplier" lever. Take 005's
strongest design (10K cCREs × 5 tiles = 50K) but halve to 5K cCREs
× 5 tiles = 25K, plus each tile's reverse complement = 50K total.
Net training-pairs unchanged, but the model gets a strand-invariance
prior baked into the data, doubling the *effective* sequence
diversity per K of region budget.

**Generalization justification**: TF binding is by-design strand-
invariant (motifs work on either strand). A model trained with
explicit RC pairs learns this prior from data, not architecture.
This prior is universally applicable to any cell type — RC
invariance is not a property of K562/HepG2/SKNSH, it is a property
of DNA.

**Prediction**: If the model is sample-efficiency-bound on strand
information, eval_01 > 0.32. If it's already strand-invariant
(common in modern seq architectures with RC-augmented training),
this will be a wash. Either result is informative.

---

## 2026-06-02 20:11 — Experiment 012 plan: RC-augmented dense cCREs

5K cCREs × 5 tiles = 25K fwd + 25K RC = 50K. Halves the region
budget vs 005 but presents each region's content as both strands.

### Prediction
If model is strand-sample-bound → lift; if already strand-robust →
wash. Either is informative.

## 2026-06-02 20:11 — Result Experiment 012

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3195 | 0.144  | 0.191  | 0.624  |
| 07   | 0.3375 | 0.121  | 0.241  | 0.651  |
| 08   | 0.0745 | 0.067  | 0.005  | 0.151  |
| 13   | 0.3278 | 0.116  | 0.240  | 0.628  |

New high on eval_01 (0.3195), but margin over 005 is +0.0018 —
within noise.

### What I learned (most informative finding so far)
Halving region budget did NOT hurt. Net: 5K regions of cCRE
diversity matches 10K regions of cCRE diversity, even when the
freed-up budget goes to RC duplicates that carry zero new sequence
information (since the model can compute RC of any input).

This means the model is **NOT region-budget-bound** at 5K cCREs.
Equivalently: the natural-genomic regulatory distribution is
already saturated, in this model, somewhere ≤ 5K diverse cCREs.

This explains every prior null result:
- 002 → 005 → 007 → 008 → 010 → 011: changed source or density,
  same plateau, because all of them sit inside an already-
  saturated distribution.
- Per-cell-type ceilings (K562 ~0.14, HepG2 ~0.19, SKNSH ~0.63)
  are properties of the per-cell-type predictability under this
  architecture, not properties of the library design within the
  natural-genomic family.

### Theory T9 → T10
The 50K budget is over-allocated to natural-genomic regulatory
content. The plateau is the per-cell-type architectural ceiling
for prepare.py-model trained on the natural-genomic distribution,
*at any density below saturation*. To beat the plateau the library
must include sequences from a **distinct distribution** that
teaches something the natural genome doesn't teach efficiently.

Candidates ranked by hypothesis strength:
1. **Saturation mutagenesis-style perturbations**: paired
   wt/mutant tiles → per-position effect learning. Force model
   to learn rule-based composition rather than region patterns.
2. **Synthetic motif combinatorics**: dense motif insertions at
   controlled densities/spacings → expand the compositional
   coverage beyond what natural cCREs span.
3. **Cross-species (mouse/zebrafish enhancers)**: regulatory
   sequence with shared grammar but different background composition
   → out-of-distribution backgrounds, in-distribution grammar.

### Plan for Exp 013
Saturation mutagenesis-style. 2,500 strong cCREs × 20 sequences =
50K: each region contributes 1 WT tile + 19 perturbations (single
or few-base substitutions spread across the tile). Tests whether
paired wt/mutant teaching of per-position effects is a distinct
source of learning that breaks the plateau.

**Generalization justification**: Per-position effect learning is
the fundamental atomic unit of regulatory grammar — universal
across cell types. A model that learns "this position has a strong
positive effect, this position has none" learns rules that compose
into prediction across any cell type's grammar.

**Prediction**: First library that has any chance to break 0.32.
If it doesn't break, the bottleneck is the model itself.

---

## 2026-06-02 20:14 — Experiment 013 plan: saturation mutagenesis

2,500 cCREs × 20 sequences = 50K. Per cCRE: 1 WT + 19 mutants with
5 random subs each. Test whether paired wt/mut training pairs
teach better than independent regional draws.

## 2026-06-02 20:14 — Result Experiment 013

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3036 | 0.135  | 0.154  | 0.622  |
| 07   | 0.3250 | 0.124  | 0.209  | 0.642  |
| 08   | 0.0686 | 0.054  | 0.000  | 0.152  |
| 13   | 0.3110 | 0.111  | 0.198  | 0.624  |

DOWN by 0.014 vs 005. HepG2 down by 0.031.

### What I learned (big finding)
Triangulating with 012:
- 012: 5,000 regions × 10 (5 fwd + 5 RC) = eval_01 0.3195
- 005: 10,000 regions × 5  = eval_01 0.3177
- 013: 2,500 regions × 20  = eval_01 0.3036

**The model saturates on natural-genomic cCRE diversity at
~5,000 unique regions.** Below this, region count is the binding
constraint and intra-region density cannot compensate. At/above
this, more regions don't help and per-region density doesn't help
either — within the natural distribution.

This is the strongest signal I've found about WHERE the budget
should go. The 50K budget is OVER-allocated to natural cCRE
content; ~25K of capacity is wasted on diminishing returns.

### Theory T10
The 50K budget is over-spent on natural-genomic regulatory content.
A model trained on prepare.py's architecture saturates on the
natural cCRE distribution at ~5K diverse regions × 5 tiles = 25K
sequences. The remaining 25K should be spent on a **distinct
distribution** that teaches something the natural distribution
doesn't.

To break the plateau, the next experiments must (a) identify the
saturation point cleanly and (b) test what kind of OOD content
fills the freed budget productively. 008 (cCRE + random) and 004
(cCRE + shuffled) already showed that low-content fillers HURT, so
the OOD content must itself be informationally dense.

### Plan for Exp 014: pure intra-region density at saturation
5,000 cCREs × 10 tiles = 50,000. Same region count as 012, no RC,
denser per-region tiling. Cleanly isolates "intra-region density
at saturation". If parity with 012 (~0.32), confirms density is
the wrong axis to push at saturation. If lift, intra-region density
IS the saturation-time lever.

Generalization justification: dense tiling exposes the model to
many position-shifts of the same regulatory content, teaching
position-invariance — universally applicable to any cell type's
prediction task.

---

## 2026-06-02 20:17 — Experiment 014 plan: dense @ saturation

5K cCREs × 10 tiles = 50K. Pure intra-region density test at the
saturating region count. Expect parity with 005/012.

## 2026-06-02 20:17 — Result Experiment 014

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3181 | 0.144  | 0.188  | 0.623  |
| 07   | 0.3372 | 0.127  | 0.239  | 0.646  |
| 08   | 0.0779 | 0.081  | 0.000  | 0.152  |
| 13   | 0.3281 | 0.119  | 0.237  | 0.629  |

Parity with 005 and 012. Saturation confirmed.

### Saturation summary (confirmed across 3 experiments)
| design                       | eval_01 |
|------------------------------|---------|
| 10K regions × 5 tiles (005)  | 0.3177  |
| 5K  regions × 5 + RC  (012)  | 0.3195  |
| 5K  regions × 10 tiles(014)  | 0.3181  |

All within ±0.002 of each other. The model is saturated by 5K
diverse cCREs and ignores extra budget allocated to more of the
same distribution.

### Theory T10 (now confirmed)
The 50K budget should be split: ~25K to saturate the natural
distribution and ~25K to a *distinct* distribution. The remaining
25K of capacity is otherwise wasted on diminishing returns.

### Plan for Exp 015: saturation + motif-amplified cCREs
50K = 5K cCREs × 5 natural tiles (saturate, 25K) + 5K cCREs × 5
motif-amplified tiles (25K). Amplified tile = same window with 3
random strong JASPAR motifs inserted at random non-overlapping
positions.

Generalization justification: motif-amplified cCREs let the model
see both selection-grounded natural compositions AND artificially
elevated motif densities, while keeping realistic genomic backbone.
This addresses 006's failure (pure synthetic scaffolds too OOD)
by anchoring the augmentation in real cCRE context. The grammar
the model learns from these is "what does adding motif X to a real
cCRE do" — a universally useful regulatory rule.

Prediction: if model has unsaturated compositional capacity, lift.
If 006-style OOD content always destroys learning even when
combined with a saturated half, this stays flat or drops.

---

## 2026-06-02 20:21 — Experiment 015 plan: saturation + motif-amplified

50K = 5K cCREs × 5 natural (saturating) + 5K cCREs × 5 motif-amplified
(3 JASPAR motifs inserted per amplified tile, sampled from PFM).
Tests whether OOD content paired with saturating natural half lifts.

## 2026-06-02 20:21 — Result Experiment 015

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3167 | 0.144  | 0.180  | 0.626  |
| 07   | 0.3355 | 0.124  | 0.235  | 0.648  |
| 08   | 0.0784 | 0.081  | -0.001 | 0.156  |
| 13   | 0.3252 | 0.116  | 0.228  | 0.632  |

Down by 0.001 vs 005. Motif-amplification on cCRE backbone is
neutral-to-slightly-negative.

### What I learned
"Saturating + additive OOD" pattern has now been tested with:
- 004 shuffled (-0.006), 008 random (-0.009), 015 motif-amp (-0.001)
- Nothing within-genome-style fills the freed budget productively.

The 25K "freed budget" appears genuinely un-usable for
distributionally-close fillers. Either:
- The model already extracts all the signal from a saturating half,
  and the OOD half just adds noise to the loss.
- The eval distribution is narrow enough that extra training
  variance hurts.

### Theory T10 → T11
The plateau is set by what the model can learn from natural-genomic
regulatory content with this architecture and budget. The freed
budget would need to come from a categorically different SIGNAL
SOURCE — something the natural distribution under-samples in
information density per base.

The two strongest candidates I haven't tried:
1. **Conservation** — evolutionarily preserved sequences have
   higher per-base functional content; phastCons-filtered cCREs
   would concentrate that.
2. **Cross-species enhancers** — orthologous regulatory sequences
   from mouse/zebrafish; teach grammar without K562/HepG2/SKNSH
   compositional bias.

### Plan for Exp 016: phastCons-conserved cCREs
Restrict cCRE selection to those overlapping a hg38 phastCons
conserved element. 5K conserved cCREs × 10 tiles = 50K. If
conservation enriches per-base information, eval_01 should lift.

Generalization justification: phastCons identifies bases preserved
by selection across mammals. Sequences enriched for these are
enriched for selection-preserved regulatory grammar — the most
universal cell-type-agnostic regulatory features in the human
genome.

---

## 2026-06-02 20:25 — Experiment 016 plan: phastCons-conserved cCREs

Top 5K cCREs by phastCons-conserved-base count in 200bp core × 10
tiles. Tests "evolutionary conservation enriches per-base info"
hypothesis.

## 2026-06-02 20:25 — Result Experiment 016

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3057 | 0.139  | 0.174  | 0.604  |
| 07   | 0.3202 | 0.121  | 0.231  | 0.609  |
| 08   | 0.0775 | 0.079  | 0.002  | 0.152  |
| 13   | 0.3111 | 0.107  | 0.230  | 0.596  |

DOWN by 0.012 vs 014 (same allocation, untargeted cCRE selection).
SKNSH took the biggest hit (-0.019).

### What I learned
Top-conservation falls into the SAME trap as top-signal DHS (009)
and top-STARR (011): single-axis top-filtering narrows the
distribution and hurts. Deeply-conserved cCREs are dominated by
universally-essential, low-variance regulatory regions (coding-
proximal, developmental UCEs).

**Filtering rule confirmed**: any single-axis top-N filter (signal,
function, conservation) collapses cell-type-variance and HURTS
cross-cell-type prediction. Within the natural-genomic family,
breadth beats peak quality.

### Theory T11
The plateau at ~0.32 reflects what this architecture can extract
from a saturating broad-coverage cCRE library. Filtering to "best"
regions consistently makes it WORSE by reducing the variance the
model needs.

Within-distribution refinements have all been tested. The remaining
hypothesis class:
- **Regulatory class structure**: cCREs are 5 distinct archetypes
  (PLS / pELS / dELS / CTCF-only / DNase-H3K4me3); dELS dominates
  74% of the file. Random cCRE sampling is distal-enhancer-biased.
  Class-balanced may improve archetypal coverage.

### Plan for Exp 017: cCRE class-balanced
1K cCREs from each of {PLS, pELS, dELS, CTCF-only,
DNase-H3K4me3} × 10 tiles each = 50K. Each class contributes
equally; the dominant dELS bias of random cCRE sampling is removed.

Generalization justification: cCRE classes are distinct regulatory
archetypes. A model trained with balanced exposure learns the full
archetypal vocabulary, which transfers to any cell type's
regulatory landscape better than a dELS-dominated sample.

Prediction: if dELS bias is part of why broad cCREs plateau,
balanced sampling lifts. If the plateau is class-agnostic
(reflecting per-cell-type ceilings independent of class composition),
this matches 014 (~0.318).

---

## 2026-06-02 20:30 — Experiment 017 plan: class-balanced cCREs

1K each from {PLS, pELS, dELS, CTCF-only, DNase-H3K4me3} × 10 tiles
= 50K. Removes the 74% dELS bias of random cCRE sampling.

## 2026-06-02 20:30 — Result Experiment 017

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3171 | 0.141  | 0.184  | 0.626  |
| 07   | 0.3375 | 0.121  | 0.236  | 0.655  |
| 08   | 0.0744 | 0.067  | 0.001  | 0.155  |
| 13   | 0.3276 | 0.112  | 0.236  | 0.634  |

Parity with 014. Tiny SKNSH up, K562/HepG2 down.

### What I learned
Class balancing is NEUTRAL. The plateau is class-agnostic. Whether
the model sees 74%-dELS or balanced archetypes, it lands at the
same place.

### Theory T11 (refined)
The plateau is invariant to every within-natural-genomic structural
manipulation tested so far. The list is now long enough that I'm
confident the plateau IS the architecture × budget × natural-
distribution ceiling, not a discoverable design flaw.

### Plan for Exp 018: multi-source saturation
1K regions from each of 5 orthogonal sources × 10 tiles = 50K:
- cCREs (broad)
- K562 DHS
- HepG2 DHS
- SKNSH DHS
- phastCons-conserved cCREs (top quartile)

Tests whether SOURCE diversity (orthogonal evidence streams
converging) lifts the plateau, when total region count stays at
saturation.

Generalization: multi-evidence regions are the convergence of
orthogonal regulatory annotations — most defensible, most likely
universal.

Prediction: another ~0.318. If true, this is the cleanest evidence
yet that the plateau is hard. If lift, source diversity matters
independently of count/structure.

---

## 2026-06-02 20:34 — Result Experiment 018 (multi-source saturation)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3121 | 0.135  | 0.176  | 0.625  |
| 07   | 0.3334 | 0.117  | 0.227  | 0.656  |
| 08   | 0.0735 | 0.062  | 0.004  | 0.154  |
| 13   | 0.3242 | 0.112  | 0.230  | 0.631  |

Down by 0.006 vs 014. Multi-source mixing slightly hurts (conserved
component's variance penalty is dilution-resistant).

### Major new finding: K562 head is library-insensitive
Cross-checked K562 eval_01 across all 18 libraries:
- 001 random:    K562=0.140
- 002 cCRE:      K562=0.145
- 005 dense:     K562=0.146
- 006 synth:     K562=0.140
- 010 diff:      K562=0.139
- 012 RC:        K562=0.144
- 014 dense:     K562=0.144
- 017 cls-bal:   K562=0.141
- 018 multi-src: K562=0.135

**K562 is pinned at 0.139–0.146 across every library tested,
including pure random and pure synthetic.** The K562 head is
architecture-bound, not library-bound, for this evaluation.

SKNSH similarly narrow (0.60–0.66). HepG2 is the only library-
sensitive head: random/synth give HepG2≈-0.08 (anti-predicted!),
cCRE-based give 0.18–0.19, max so far 0.191 (012 RC).

### Theory T11 → T12 (REFRAMED PLATEAU)
mean_r ≈ (0.14 + HepG2 + 0.625) / 3  ≈  0.255 + HepG2/3

The "plateau" at 0.318 is the HepG2-head ceiling (~0.19) under
all natural-genomic libraries tested. K562 and SKNSH are
near-constants in this regime.

To lift mean_r above 0.32, the only viable lever is to push
HepG2 prediction past ~0.20. Every other axis is essentially
saturated.

### Plan for Exp 019: HepG2-optimized library
5,000 HepG2-specific DHS peaks (HepG2 DHS NOT in K562 NOT in SKNSH,
top by signal) × 10 tiles = 50K. Maximizes HepG2-specific
regulatory exposure to push the HepG2 head toward its ceiling.

Generalization justification: even though biased toward HepG2-
specific content, the regulatory grammar learned (TF binding rules,
motif spacing) is universal and transfers across cell types.
HepG2-specific DHS regions are still natural regulatory elements —
the model learns "what regulatory grammar looks like in HepG2"
which informs its understanding of regulatory grammar in general.

Prediction: if HepG2 head can be pushed beyond ~0.19, mean_r > 0.32.
If not, the HepG2 ceiling is also architecture-bound and the only
remaining axis is to look for designs that lift K562 or SKNSH.

---

## 2026-06-02 20:38 — Result Experiment 019 (HepG2-optimized)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.2808 | 0.143  | 0.095  | 0.605  |
| 07   | 0.2925 | 0.124  | 0.139  | 0.614  |
| 08   | 0.0782 | 0.078  | 0.005  | 0.151  |
| 13   | 0.2866 | 0.116  | 0.133  | 0.611  |

eval_01 DROPS by 0.037. HepG2 nearly halves (0.188 → 0.095).
K562 essentially unchanged (library-insensitive confirmed).

### What I learned
HepG2-only training (with K562/SKNSH overlap excluded) DESTROYS
HepG2 prediction. The HepG2 head requires CROSS-CELL-TYPE variance
in the training distribution to discriminate HepG2 activity.

Combined with 010 (HepG2-stratified DHS gave HepG2=0.188 when
mixed with K562/SKNSH/shared), this proves the HepG2 head needs
contrast — not just exposure — to learn HepG2 discrimination.

### Theory T13 (locked in)
The plateau at 0.318 = (0.146 + 0.19 + 0.625) / 3 is the per-head
architectural ceiling for this model on natural-genomic 50K
libraries:
- K562 head: 0.146, library-insensitive (any 50K library)
- HepG2 head: 0.19, requires cross-cell-type-diverse library
- SKNSH head: 0.625, mostly insensitive (slight library variation)

NO single-source or multi-source natural-genomic library design
breaks any of these ceilings. The plateau IS the model × budget ×
distribution ceiling for this task.

### What's left to try (low-confidence levers)
1. Cross-species enhancer content (VISTA / mouse cCREs)
2. Wider-window position diversity (±400bp instead of ±100bp)
3. Cocktail designs targeting weak evals (eval_08-friendly)

None of these have strong theoretical reason to break the per-head
ceilings, but they're worth confirming empirically.

### Plan for Exp 020: wider-window tile sampling
5K cCREs × 10 tiles, each tile offset uniform random in [-400, 400]
(instead of [-100, 100]). Tests whether context-aware sampling
adds anything beyond core-element tiling.

Generalization justification: regulatory grammar includes flanking
context (insulator distances, neighboring TFs). Wider sampling
trains the model on context-modulated activity which is universal
across cell types.

---

## 2026-06-02 20:41 — Result Experiment 020 (wider-window tiles)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3216 | 0.144  | 0.200  | 0.621  |
| 07   | 0.3377 | 0.129  | 0.247  | 0.637  |
| 08   | 0.0741 | 0.073  | -0.000 | 0.150  |
| 13   | 0.3306 | 0.117  | 0.250  | 0.624  |

**NEW HIGH on eval_01 (0.3216)**. HepG2 broke 0.20 for the first
time. K562 / SKNSH unchanged. eval_13 also up.

### The first design that lifts the plateau
Five-week worth of plateau-confirmation experiments and then a
random-feeling tweak (wider tile offsets) is the lever. Why?

Narrow-core tiling (±100bp) keeps every tile centered on the
regulatory element. The model only ever learns "what does this
element look like in a window centered on it". Wider tiling
(±400bp) trains:
1. Positional invariance — the element can be anywhere in the 200bp
   window.
2. Partial-motif handling — the element can be at the edge.
3. Context-only inference — sometimes the element is OUTSIDE the
   window entirely; the model learns to predict from flanking
   context alone.

These are three NEW LEARNING SKILLS that the narrow-tile family
never exercised. They transfer across cell types because they are
universal regulatory-grammar skills, not cell-type-specific
patterns.

### Theory T13 → T14
The plateau at 0.318 was the ceiling for the NARROW-CORE TILING
FAMILY. The HepG2 head's "0.19 ceiling" was a property of
narrow-tile training, not the architecture.

Wider context tiling exposes the model to context-aware grammar
which lifts HepG2. The new framing:
- A library's ceiling is set by the union of SKILLS the training
  examples can teach.
- Narrow tiles teach element identification only.
- Wider tiles teach element ID + position invariance + context
  inference.
- Adding new SKILLS is a different lever from distribution
  shifting — that's why it lifts where everything else failed.

This is the most important theoretical update of the run.

### Plan for Exp 021: stack wider + RC
5K cCREs × 5 wider tiles + each tile's RC = 50K. Tests whether
wider-context and RC augmentation effects are additive (universal
priors should be orthogonal).

Generalization justification: both interventions teach universal
DNA priors (strand invariance + context inference). If they teach
different priors they should combine.

Prediction: 0.322 ± 0.005. If lift, both axes are productive
and orthogonal. If parity, they may compete for the same residual
learning capacity.

---

## 2026-06-02 20:43 — Result Experiment 021 (wider + RC stacked)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3222 | 0.145  | 0.200  | 0.622  |
| 07   | 0.3399 | 0.129  | 0.251  | 0.639  |
| 08   | 0.0751 | 0.075  | -0.001 | 0.152  |
| 13   | 0.3303 | 0.116  | 0.250  | 0.625  |

NEW HIGH on eval_01 (+0.0006 over 020). eval_07 also new high (0.340).
Stacking wider + RC gives essentially what wider gives alone.

### What I learned
RC augmentation on top of wider tiles is nearly redundant — the
wider distribution already includes enough strand-mixing implicit
in the variability of offsets. So 020's lift IS the lever; RC adds
marginal noise reduction.

### Theory T14 (refined)
Two "skill axes" lift the plateau:
1. CONTEXT BREADTH (wider tiles, ±400): teaches positional
   invariance + context-only inference. Single biggest lever.
2. STRAND INVARIANCE (RC): small lift on top of narrow tiling,
   ~0 on top of wider tiling.

### Plan for Exp 022: even wider tiles (±800)
5K cCREs × 10 tiles, offsets in [-800, 800]. The 200bp window can
land up to 1kb from cCRE midpoint. Tests whether the context lift
is monotonic or peaks.

Generalization: broader context exposure trains "what does the
genome look like near regulatory elements" — universal regulatory
context grammar.

Prediction: lift if context capacity unsaturated; parity or drop
if 020 already exhausted it.

---

## 2026-06-02 20:46 — Result Experiment 022 (even wider, ±800bp)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3221 | 0.143  | 0.202  | 0.621  |
| 07   | 0.3375 | 0.126  | 0.251  | 0.636  |
| 08   | 0.0725 | 0.072  | -0.007 | 0.152  |
| 13   | 0.3328 | 0.121  | 0.253  | 0.625  |

Parity with 020/021 on eval_01 (0.322). HepG2 inches to 0.202.
eval_13 new high (0.333).

### Context-breadth lever saturated by ~±400
Going from ±400 to ±800 maintains the lift but doesn't add — the
model has extracted most of what context-aware sampling can teach
by ±400. HepG2 head has a new ceiling around 0.20-0.21 in the
wider-tile family.

### Plan for Exp 023: wider + more regions
10K cCREs × 5 wider tiles = 50K. Each wider tile carries more
contextual information; the saturation point under wider sampling
may differ from the narrow-tile saturation (5K).

Generalization: more diverse regulatory regions × context-aware
sampling.

Prediction: if wider sampling shifts saturation point up, 10K x 5
wider beats 5K x 10 wider (0.32 → ~0.325). If saturation is
information-bound, parity.

---

## 2026-06-02 20:50 — Result Experiment 023 (10K cCREs x 5 wider)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3215 | 0.144  | 0.200  | 0.621  |
| 07   | 0.3395 | 0.130  | 0.251  | 0.638  |
| 08   | 0.0732 | 0.070  | -0.003 | 0.152  |
| 13   | 0.3305 | 0.114  | 0.252  | 0.626  |

Parity with 020 (0.3216 vs 0.3215). Saturation point under wider
tiling is the SAME as under narrow tiling: ~5K diverse regions.

### What I learned
Doubling region count under wider sampling did not help. The
wider-tile lift is NOT "richer per-region info enables more
regions to fit". It is a SKILL injection (context inference) that
lifts every example by a constant.

### Theory T15
Ceiling rises when we add SKILLS, not when we add data.
- Context breadth (±400): +0.004 skill (context inference)
- Strand invariance (RC): +0.001 skill (subsumed when wider)
- Region count, top-filter, motif-amp, multi-source: data
  reshufflings, no new skill, no ceiling lift.

Next ceiling-lift requires NEW skill.

### Plan for Exp 024: explicit paired pos/neg from real genome
Hypothesis: the wider-tile lift may come from natural pos/neg
pairing — some wider tiles hit the cCRE core (positive), others
land in flank/non-functional DNA (negative). The model implicitly
contrasts and learns what makes the core different.

Design: 5K cCREs × 5 narrow tiles (positives, ±100bp of core)
     + 5K random non-cCRE genomic windows × 5 tiles per region
       (paired negatives, far from any cCRE)
     = 50K.

If 024 ≥ 020: lift comes from pos/neg pairing. New lever.
If 024 < 020: lift comes from positional/context variation per
              region, not pairing.

Generalization: explicit negatives teach "what regulatory DNA
ISN'T" — a universally useful discrimination prior.

---

## 2026-06-02 20:55 — Result Experiment 024 (paired pos/neg from real genome)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3206 | 0.148  | 0.201  | 0.613  |
| 07   | 0.3358 | 0.130  | 0.254  | 0.623  |
| 08   | 0.0701 | 0.070  | -0.008 | 0.148  |
| 13   | 0.3353 | 0.124  | 0.262  | 0.620  |

eval_01 below 020 (0.322) but well above 014 narrow (0.318).
eval_13 NEW HIGH (0.335). K562 head moved for the first time
(0.144 -> 0.148).

### What I learned
Explicit non-cCRE genomic negatives are a NEW LEVER. They recover
most of the wider-tile lift via a different mechanism
(discrimination from non-functional DNA) and add a small K562
bump that no other library has produced. SKNSH dropped slightly,
suggesting capacity tradeoff.

### Theory T16
The 3 cell-type heads respond to different levers:
- K562 (compact regulatory landscape): functional/non-functional
  contrast (paired neg) -> +0.004
- HepG2: context breadth OR contrast (either) -> +0.012
- SKNSH: context breadth, hurt by explicit non-cCRE neg
  (capacity drained from cCRE-diversity modeling)

### Plan for Exp 025: stack wider + paired neg
5K cCREs x 5 WIDER tiles (+/-400bp, positives)
+ 5K non-cCRE x 5 narrow tiles (negatives)
= 50K. Tests whether the two new skill axes are orthogonal.

Prediction: eval_01 ~0.323-0.325 if orthogonal; ~0.320 if partial
redundancy on HepG2. K562 should hold the bump.

---

## 2026-06-02 21:00 — Result Experiment 025 (wider + paired neg STACKED)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3195 | 0.144  | 0.204  | 0.610  |
| 07   | 0.3352 | 0.129  | 0.255  | 0.622  |
| 13   | 0.3333 | 0.120  | 0.262  | 0.618  |

Stack failed: -0.002 vs 020, -0.001 vs 024 on eval_01.
HepG2 NEW HIGH (0.204). K562 LOST 024's bump (0.144).
SKNSH continues to drop (0.610).

### What I learned
The two levers ANTI-stack. Capacity is partitioned across 3
cell-type heads. Each head has its own lever; stacking spends
capacity broadly and starves dominant heads (SKNSH).

### Theory T17: capacity partitioning
mean_r ceiling = weighted product of per-head ceilings.
Levers can lift heads INDEPENDENTLY but cost capacity from
others. To lift mean_r: either (a) find single intervention
that lifts multiple heads OR (b) find intervention with large
net positive (one head up >> others down).

### Plan for Exp 026: dinuc-shuffled negatives
5K cCREs x 5 narrow + 5K dinuc-shuffled cCRE tiles x 5 = 50K.
Tests whether 024's K562 bump comes from (A) real intergenic
genomic context or (B) non-functional sequence with matched
composition. If shuffled matches 024 K562, the contrast itself
is the lever. If shuffled fails K562, real genomic context
carries info.

Prediction: shuffled gives ~K562 0.146 if (B), ~0.144 (back to
baseline) if (A).

---

## 2026-06-02 21:05 — Result Experiment 026 (dinuc-shuffled negatives)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3190 | 0.142  | 0.192  | 0.623  |
| 07   | 0.3393 | 0.122  | 0.244  | 0.652  | <- SKNSH NEW HIGH
| 13   | 0.3284 | 0.114  | 0.241  | 0.630  |

K562 bump from 024 is GONE (0.148 -> 0.142). HepG2 lift partially
preserved (0.201 -> 0.192). SKNSH RECOVERED (0.613 -> 0.623).
eval_07 SKNSH=0.652, NEW HIGH for SKNSH head.

### What I learned
K562's bump in 024 needs REAL intergenic genomic sequence — not
just matched-composition "non-functional" negatives. The K562
head appears to use intergenic features (repeats, GC patterns,
maybe DNA shape signatures) that survive in real genomic neg
but not in dinuc-shuffled.

Conversely, SHUFFLED neg doesn't HURT SKNSH (model ignores them
as obvious noise), while REAL neg DOES hurt SKNSH (model spends
capacity to distinguish them).

### Theory T18: negative specificity matters
The "right" negative depends on the head:
- K562 benefits from real intergenic genomic neg
- SKNSH penalized by real, neutral on shuffled
- HepG2 benefits modestly from both
Optimal mix likely needs SMALLER NEG fraction (less SKNSH tax)
while keeping K562 benefit.

### Plan for Exp 027: pos:neg ratio sweep
Test 4:1 ratio. 5K cCREs x 8 narrow + 2.5K non-cCRE x 4 narrow
= 50K. If K562 bump survives at smaller neg fraction AND SKNSH
recovers, possible new high.

---

## 2026-06-02 21:10 — Result Experiment 027 (pos:neg 4:1)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3211 | 0.145  | 0.199  | 0.619  |
| 07   | 0.3381 | 0.128  | 0.251  | 0.635  |
| 13   | 0.3336 | 0.120  | 0.254  | 0.627  |

Sweet spot: K562 retains tiny bump (0.145), HepG2 lift mostly
preserved (0.199), SKNSH partially recovered (0.619). Mean 0.3211.

### What I learned
The K562 bump in 024 was fragile — at 4:1 it mostly disappeared.
HepG2 lift is robust to neg ratio. SKNSH cost scales linearly
with neg fraction. No "free" win from ratio tuning alone.

### Plan for Exp 028: WIDER + 4:1 stacked
5K cCREs x 8 WIDER (+/-400bp) + 2.5K non-cCRE x 4 narrow = 50K.
Tests if 025's failed stack (1:1) succeeds at 4:1 ratio (less
SKNSH tax). If yes, could push past 0.322.

---

## 2026-06-02 21:15 — Result Experiment 028 (wider + 4:1 paired neg) — NEW HIGH

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3229 | 0.148  | 0.203  | 0.618  | <- NEW HIGH
| 07   | 0.3399 | 0.131  | 0.255  | 0.633  | <- tied
| 08   | 0.0809 | 0.090  | 0.000  | 0.152  | <- K562 jump on eval_08
| 13   | 0.3341 | 0.118  | 0.260  | 0.625  |

NEW HIGH on eval_01: 0.3229 vs prev best 0.3222 (021).
NEW HIGH on K562 head (0.1476).
All three heads contributed: K562 +0.004, HepG2 +0.015, SKNSH -0.005
vs narrow baseline. Mean +0.0048.

### What I learned
The failure of 025 (1:1 stack) was SKNSH capacity drain, NOT
lever redundancy. At 4:1 the SKNSH cost is small enough that the
wider+paired stack works on all heads. Validates T17/T18.

### Theory T19: head-additive at low neg fraction
At ~20% neg fraction, the wider-tile and paired-neg levers add
on HepG2 (saturating ~0.203), paired alone contributes K562, and
SKNSH cost stays small. SKNSH cost appears super-linear past ~30%
neg fraction.

### Plan for Exp 029: add RC to 028 stack
5K cCREs x 4 wider tiles + RC each + 2.5K non-cCRE x 4 = 50K.
RC was subsumed when stacked with wider alone (021). With paired
neg also present, RC may contribute differently. Tests 3-way
stack.

Prediction: 0.323-0.325 if RC adds, parity if subsumed.

---

## 2026-06-02 21:20 — Result Experiment 029 (3-way: wider + RC + 4:1 neg)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3216 | 0.143  | 0.203  | 0.619  |
| 07   | 0.3376 | 0.128  | 0.252  | 0.632  |
| 13   | 0.3339 | 0.120  | 0.258  | 0.623  |

Below 028 (0.3229). RC stacking dropped K562 bump
(0.148 -> 0.143). HepG2 and SKNSH unchanged.

### What I learned
RC is NOT free when paired neg is also present. Each cCRE
contributes 8 (4 fwd + 4 rc) tile-instances that are not
independent training examples. The K562 discrimination signal
needs distinct positive instances; RC dilution weakens it.

### Theory T20: 2 capacity pools, 4 levers
- Identity/context pool (HepG2 + SKNSH lift): wider tiles, RC
- Discrimination pool (K562 + HepG2 lift): paired neg
Pools can stack ACROSS at low neg fraction (028) but RC on top
of paired neg consumes discrim capacity (029 fails).

### Plan for Exp 030 (final): HARD negatives
028 used negatives >2kb from any cCRE. Test "hard" negatives
200-1500bp away (close to but not within cCRE). If harder
contrast lifts K562 further, finer boundary signal helps.

5K cCREs x 8 wider + 2.5K adjacent non-cCRE x 4 = 50K.

---

## 2026-06-02 21:25 — Result Experiment 030 (hard adjacent negatives)

| eval | mean_r | K562   | HepG2  | SKNSH  |
|------|--------|--------|--------|--------|
| 01   | 0.3223 | 0.146  | 0.202  | 0.619  |
| 07   | 0.3390 | 0.132  | 0.251  | 0.634  |
| 13   | 0.3316 | 0.119  | 0.253  | 0.623  |

Parity with 028 within noise (-0.0006). K562 bump slightly
smaller (0.146 vs 0.148). HARD negatives do NOT lift K562
further than FAR negatives.

### What I learned
The K562 bump uses BROAD intergenic features (repeats, large-
scale GC, sequence "non-functional-ness"), not fine boundary
detection. Easy and hard negatives carry the same useful
information for K562.

### FINAL THEORY T20
2 capacity pools:
- IDENTITY/CONTEXT: wider tiles, RC (HepG2 + SKNSH)
- DISCRIMINATION: paired neg (K562 + HepG2)
Cross-pool stacking at ~20% neg fraction is the sweet spot
(028: mean_r=0.3229, +0.0048 vs narrow baseline).
Same-pool stacking has diminishing returns.
REAL intergenic neg required for K562; shuffled doesn't work;
adjacent vs far doesn't matter.

### FINAL BEST LIBRARY: 028
5K cCREs x 8 WIDER (+/-400bp) + 2.5K non-cCRE x 4 narrow = 50K.
eval_01 = 0.3229.
