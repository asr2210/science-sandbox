# MPRA Library Design — Lab Notebook

## 2026-04-27 — Initial theory

**Goal:** design a 50K MPRA library that, after training a sequence-to-activity
model on it (measured in K562, HepG2, SK-N-SH), produces a model that
generalizes to held-out sequences AND to unmeasured cell types.

**Initial theory (T0):** A library is informative if it (a) covers diverse
cis-regulatory motifs and (b) samples sequence space without the confounding
homology/repetitive-element structure of the genome. Following de Boer &
Taipale 2024 ("Hold out the genome", Nature 625:41–50), random/synthetic
sequences may generalize *better* than natural genomic sequences because:
1. They are i.i.d. — no inter-sequence homology that inflates train/test
   correlations.
2. They probe a much larger sequence space than the human genome contains.
3. They avoid the ~60% repetitive-element fraction of the human genome
   (LINE/SINE/etc.) that dominates many "natural" libraries.

The competing intuition is that real regulatory sequences carry signal that
random sequences lack — so a library of cCREs/DHSs would teach the model
real motif grammar that random data cannot.

These two views are testable. Experiment 001 establishes the random-DNA floor.

**What "generalize beyond labeled cell types" requires:** the model must
learn TF-motif → activity mappings that operate similarly across cell types,
not memorize cell-type-specific regulatory programs. So a library should
expose the model to a wide breadth of motif content/contexts.

## 2026-04-27 — Plan: experiment 001 (uniform random baseline)

**Type:** exploring (no priors — first experiment).

**Hypothesis:** uniform random 200bp DNA, 50K sequences, will produce a
*non-trivial* sequence-to-activity model. Random DNA contains chance
matches to TF motifs (a 200bp sequence has ~196 6-mer windows; many will
match common TFs by chance), so the model can learn motif → activity even
from a random library. Per de Boer 2024, this approach generalized in yeast.

**Generalization justification:** uniform random sequences have no
cell-type-specific bias in their composition. Whatever the model learns from
them is by definition not cell-type-program memorization — it must be
sequence-feature → activity mapping. So in principle, the learned features
should transfer.

**What I'd predict if T0 is right:** mean_r > 0 across all 14 eval sets,
with K562/HepG2/SK-N-SH correlations roughly comparable (no cell-type-program
confound). If T0 is wrong (random produces a near-zero model), I'll learn
that real regulatory context is essential and pivot to natural sequences.

**Design:** 50,000 sequences × 200 bp × 3 seeds, each base i.i.d. uniform
from {A, C, G, T}. Seeds 0/1/2 → sequences_0.txt / 1 / 2.

## 2026-04-27 — Result: 001 uniform random

**Headline:** eval_01 = **0.6954**, mean across 14 evals ≈ **0.732**.

Per-eval (mean over seeds):
01=0.6954 02=0.7848 03=0.7612 04=0.7494 05=0.6951 06=0.7853 07=0.6684
08=0.7841 09=0.8115 10=0.7564 11=0.6833 12=0.6553 13=0.6584 14=0.7851

Per-cell-type (averaged across evals): K562=0.731, HepG2=0.715, SK-N-SH=0.745.
SK-N-SH > K562 > HepG2 in almost every eval.

Across-seed SD on eval_01 ≈ 0.003 — tight, so future inter-experiment
comparisons can detect sub-percent effects.

**What this updates in T0:** confirmed random DNA produces a non-trivial
model — but ~0.7 correlation is much higher than I'd predicted as a
"floor". Two plausible explanations:
1. Chance motif occurrences in 50K × 200bp random DNA give the model
   enough signal to learn motif → activity (de Boer 2024 hypothesis).
2. Composition (GC%, dinucleotide freq) alone explains a meaningful chunk.

**Refined theory T1:** A library is informative not because it contains
"correct" sequences but because it spans enough sequence space for the
model to discover features that map to activity. Random DNA already spans
that space coarsely. The marginal value of any improvement comes from
sampling MORE of the relevant feature space — either by using natural
elements (which contain more dense, longer motifs) or by enriching for
specific functional classes. The bar is high: anything I do must beat
0.6954 on eval_01.

**Next-experiment plan:** experiment 002 will test natural genomic
regulatory elements (ENCODE cCREs) — same count, same length. This
directly contrasts "random with chance motifs" vs. "natural with
designed-by-evolution motifs but homology bias". The result will tell us
whether real cis-regulatory grammar is irreplaceable or whether random
already captures the learnable signal.

## 2026-04-27 — Plan: experiment 002 (cCRE uniform sample)

**Type:** exploring (testing the random-vs-natural axis).

**Hypothesis:** real ENCODE cCREs (V4, 2.35M elements: dELS 63%, pELS 11%,
CA 10%, CA-CTCF 5%, TF 4%, CA-H3K4me3 3%, PLS 2%, CA-TF 1%) contain
denser/longer TF motif content than uniform random DNA. If the model is
motif-driven, it should learn faster and generalize better. Predicted
direction: eval scores improve over 001's 0.6954.

**Counter-hypothesis (de Boer 2024):** natural sequences carry repetitive
elements (LINE/SINE etc.) and homology that violate i.i.d. and inflate
training-set patterns the model overfits to. Could fail to improve
over random — or hurt. cCREs are *somewhat* selected against repeats
(they're regulatory elements), so this risk is moderate but not zero.

**Generalization justification:** unmeasured cell types share TF
repertoires with K562/HepG2/SK-N-SH; if the model learns motif-level
features from cCREs (pTFs that operate broadly), those should transfer.
The risk for cell-type generalization is if cCREs over-represent
K562/HepG2/SK-N-SH-active programs and the model latches onto them.
But cCREs are derived from ENCODE pan-tissue data, so this is mild.

**Design:** 50K cCREs sampled uniformly without replacement from the
2.35M V4 set, per seed. Extract a 200bp window centered on each cCRE
midpoint from hg38.2bit. Replace any soft-masked or N bases with
uppercase ACGT (uniform random for N). Three independent seeds = three
independent uniform samples.

## 2026-04-27 — Result: 002 cCRE uniform

**Headline:** eval_01 = **0.7263**, mean across 14 evals ≈ **0.762**.
That's **+0.031 on eval_01 / +0.030 on mean** vs 001 random.

Per-eval delta vs 001:
01:+0.031 02:+0.035 03:+0.045 04:+0.011 05:+0.031 06:+0.035 07:**+0.105**
08:**−0.096** 09:+0.011 10:+0.034 11:+0.031 12:+0.038 13:**+0.113** 14:+0.034

cCRE wins 13/14. eval_07 (+0.105) and eval_13 (+0.113) are huge wins;
eval_08 (−0.096) is a substantial loss. Across-seed SD on eval_01 ≈ 0.027
(~10× higher than 001) — cCRE sampling has more variance because each
seed draws a different 50K-cCRE subset.

Cell-type spread compresses under cCRE training: K562/HepG2/SK-N-SH
within 0.01 vs random where SK-N-SH had a clear lead.

**T1 → T2:** Confirmed that natural regulatory elements give the model
~+0.03 average lift over uniform random, but the mechanism is unclear
and there's a non-trivial COST: natural sequences sacrifice some
sequence-space coverage that random covered (eval_08, −0.096). So
"more realistic" is not strictly better — it's better *in expectation*.

T2 hypothesis: A library is informative to the extent it (a) contains
real cis-regulatory motif content AND (b) covers enough sequence space
that the model can extrapolate. There is a tradeoff: pure natural
sequences max out (a) but compromise (b); pure random max out (b) but
compromise (a). Optimal libraries should balance.

**Open mechanism question:** is the +0.03 from (a) real TF motifs or
(b) natural compositional bias (GC, dinucleotide freq, k-mer enrichment)?
Random has uniform composition; cCREs do not. A model that primarily
learns "natural composition → activity" would partially explain the gain
without invoking motif grammar.

**Next-experiment plan (003):** dinucleotide-shuffled cCREs. Same
sequences, shuffled to preserve dinucleotide frequencies but destroy
motifs. Compare to 001 (random uniform) and 002 (real cCREs):
- 003 ≈ 002 → gain is compositional, not motif-driven
- 003 ≈ 001 → motifs are the entire story
- 003 between → both contribute
This is a single, mechanism-discriminating experiment that maximally
informs how to spend the remaining budget.

## 2026-04-27 — Plan: experiment 003 (dinuc-shuffled cCREs)

**Type:** refining (mechanism question for the natural-element gain in 002).

Sample same kind of 50K cCREs as 002, then dinucleotide-shuffle each
sequence using Hierholzer's Eulerian-walk algorithm (preserves the
dinucleotide multiset exactly; destroys motifs). Per-sequence shuffle
seeded by (global_seed, sequence_index) for reproducibility.

**T2 prediction:** 003 should fall BETWEEN 001 and 002, closer to 002.
Reasoning: dinucleotide composition (especially CpG, GC%) carries a
substantial chunk of the "natural sequence" signal — chromatin
accessibility correlates with GC and CpG, and many TF binding sites are
GC-rich. So preserving dinucs preserves much of the compositional
predictive signal, but destroys actual motif-grammar information.

**Generalization argument:** if motifs are essential, models trained on
shuffled sequences won't have learned transferable TF grammar. If
composition is sufficient, shuffled may transfer surprisingly well —
but only to evals where compositional features dominate.

## 2026-04-27 — Result: 003 dinuc-shuffled cCREs

**Headline:** eval_01 = **0.6189**, mean ≈ **0.660**.
That's **−0.077 vs 001 random** and **−0.107 vs 002 cCREs** on eval_01.

003 is BELOW 001 on **13/14 evals** (eval_13 tied). Big losses everywhere.

This **falsifies** the "T2 compositional gain" hypothesis. The cCRE
gain in 002 was NOT from compositional features (GC, CpG, dinuc bias).
It was entirely from real motifs. AND, removing motifs while keeping
composition makes things WORSE than random.

**Key insight:** natural compositional bias is HARMFUL in isolation
because it narrows sequence-space coverage relative to uniform random,
without compensating signal once motifs are gone.

**T2 → T3 (current theory):** Library informativeness has two
components: (a) sequence-space COVERAGE, max'd by uniform random;
(b) MOTIF content, max'd by real cis-regulatory elements. Real cCREs
trade some (a) for big (b) gain — net positive. Dinuc-shuf cCREs lose
(a) and don't gain (b) — net negative. Library quality = motif gain −
coverage cost.

Predictions of T3:
- A library that combines random scaffolds with embedded real motifs
  should beat both 001 and 002 (high coverage + real motifs).
- Cell-type generalization should benefit most from libraries that
  expose the model to MOTIFS that operate broadly across cell types
  (e.g., shared TF families) — not from cell-type-specific cCRE selections.

**Next-experiment plan (004):** embed TF motifs into uniform random
scaffolds. 50K x 200bp uniform random sequences, each with 1–3 TF
motifs (from HOCOMOCO/JASPAR human core) randomly embedded at random
positions. If 004 > 002, the win is from motif identity alone (real
positional context is dispensable). If 004 < 002, real cCRE context
matters beyond just motif presence.

## 2026-04-27 — Plan: experiment 004 (motifs embedded in random)

**Type:** refining (testing T3's "best library = motifs + coverage").

**Design:** 50K x 200bp uniform random scaffolds. Per sequence, embed
1-3 motif instances. Each instance: pick a random PWM from JASPAR 2024
CORE vertebrate non-redundant (n=2346, length 4-33bp, median 9bp), sample
a concrete sequence from that PWM (probabilistic per-position), choose a
random non-overlapping position, randomly orient (50% reverse-complement).
Three independent seeds.

**T3 prediction:** 004 should beat 001 (motifs added), and is plausibly
≥ 002 (cCREs) because:
- Motifs are present in real-PWM-sampled instances (covers (b))
- Background is uniform random, max coverage of (a)
The risk: motifs in random scaffolds may not "look like" real
regulatory elements — TFs bind cooperatively in clusters with specific
spacing. If positional grammar matters, 004 may underperform 002.

**Generalization argument:** if 004 > 002, then a model can learn
transferable motif → activity rules from any background (broad coverage
helps). If 004 < 002, real cCRE arrangements (cooperative motif clusters,
linker spacing, TSS proximity) carry information that bare motif
embedding doesn't capture.

## 2026-04-27 — Result: 004 motifs-in-random

**Headline:** eval_01 = **0.6397**, mean ≈ **0.682**.
That's **−0.056 vs 001 random** and **−0.087 vs 002 cCREs** on eval_01.

Order on most evals: **003 < 004 < 001 < 002**.
Notable exception: eval_08 — 004=0.7110 is close to 001=0.7841 (much
higher than 002=0.6880). So eval_08 favors broad-coverage libraries.

**T3 falsified.** Adding real motifs to random scaffolds HURT, not
helped. So motif content alone is not the cCRE advantage; real
regulatory CONTEXT carries information beyond just motif identity.

**T3 → T4:** A library is informative when sequences contain real
motifs embedded in REALISTIC REGULATORY CONTEXT. Bare motif insertion
into random scaffolds creates "out-of-context" motif effects the model
mis-learns (single-motif → activity), failing to generalize. The
"context" likely includes co-occurring motifs, spacing, and chromatin-
relevant features captured implicitly in genomic sequence.

This redirects the strategy: don't try to synthesize regulatory
sequences de novo (yet); learn to USE real genomic content optimally.

**Next-experiment plan (005):** random 200bp genomic windows (not
cCRE-selected). Separates "genomic context" from "regulatory
selection":
- 005 ≈ 001 → genomic context per se doesn't help; cCRE selection matters
- 005 ≈ 002 → any genomic context is sufficient; cCRE selection
  is unnecessary
- 005 between → both contribute
This decisively localizes the cCRE benefit.

## 2026-04-27 — Plan: experiment 005 (random genomic windows)

**Type:** refining (pinpointing source of cCRE benefit).

**Design:** 50K random 200bp windows from hg38, sampled by chrom-length-
weighted random position on chr1-22, X, Y. Skip windows with >10% N.
Replace remaining Ns with random ACGT. Three independent seeds.

**Expected genomic content:** the genome is ~2% coding, ~10% regulatory
(cCREs cover ~7% of genome but biased), ~50% repetitive. So a uniform
window will mostly hit intergenic/intronic territory, with a small
fraction of windows overlapping cCREs by chance.

**T4 prediction:** I expect 005 to land between 001 and 002, but closer
to 001 — most windows will be regulatory-content-poor. A small fraction
will hit real REs by chance and provide some signal. So a small lift
over 001, much less than 002's lift.

**Generalization argument:** random genomic windows expose the model to
the FULL genomic distribution including repetitive elements, intronic
sequences, etc. — which is what an unmeasured cell type's input to a
sequence model would actually look like in practice. So 005 may
generalize differently from cCRE-trained models even if scores look
similar.

## 2026-04-27 — Result: 005 random genomic

**Headline:** eval_01 = **0.6636**, mean ≈ **0.702**.

Random genomic landed BELOW 001 (random uniform) — opposite of the T4
prediction. This is significant:

5-way mean ranking:
- 002 cCREs            0.762
- 001 random uniform   0.732
- 005 random genomic   0.702
- 004 motifs in random 0.682
- 003 dinuc-shuf cCRE  0.660

**T4 → T5 (current theory):**
A library is informative when sequences come from regions evolution
selected to contain real TF motifs in functional arrangements
(= REGULATORY genomic segments). Both "real motifs alone" (004) and
"real generic genomic context alone" (005) are worse than uniform
random; only the combination in real cis-regulatory elements wins.

This means the "context" doing the work in 002 is specifically
*regulatory* context — not generic genomic context. Random uniform
beats random genomic on most evals because uniform genomic is mostly
intergenic/intronic/repetitive: bias-rich but signal-poor.

Sub-pattern: eval_07 and eval_13 favor genomic-derived libraries
(cCRE > genomic > uniform); eval_08 favors uniform random (and is
worst with genomic). Eval sets clearly probe different distributions.

**Open question:** which cCRE class(es) drive the cCRE benefit? PLS
(promoter-like, 2% of cCREs) and dELS (distal enhancer-like, 63%) may
contribute very differently per element.

**Next-experiment plan (006):** stratified cCRE sampling. Equal counts
per cCRE class (~6.25K from each of PLS, pELS, dELS, CA-CTCF, CA-H3K4me3,
CA-TF, CA, TF). Compare to 002:
- 006 > 002 → class diversity matters; rare classes (PLS) carry signal
- 006 ≈ 002 → natural class distribution is fine
- 006 < 002 → dELS dominance is actually informative (as in 002)

## 2026-04-27 — Plan: experiment 006 (cCRE class-stratified)

**Type:** refining (variant of 002 — what role does class composition play?)

**Design:** equal counts per cCRE class (6,250 each from PLS, pELS, dELS,
CA-CTCF, CA-H3K4me3, CA-TF, CA, TF = 50K total). 200bp centered on
midpoint, same as 002. Three seeds, each picks fresh subsets per class.

**T5 prediction:** plausibly slight improvement over 002. By boosting
PLS (47K available, was ~1K in 002) and CA-CTCF (was ~2.7K), I add
distinctive regulatory contexts the model didn't see much of before.
Down-weighting dELS (1.47M → 6.25K) loses some redundant examples but
shouldn't hurt because dELS were over-represented to start with.

**Risk:** if dELS-rich was actually the right composition for these
evals, 006 will underperform.

## 2026-04-27 — Result: 006 cCRE class-stratified

**Headline:** eval_01 = **0.7368**, mean ≈ **0.775**.
+0.011 vs 002 on eval_01, +0.013 on mean. **New best library.**

Wins on 11/14 evals. Biggest gains: eval_04 (+0.028), eval_09 (+0.034).
Small losses on eval_07/08/10/13 (≤0.006, within seed SD).
eval_08 remains the natural-library outlier (still −0.10 vs random).

**T5 refined:** motif-context diversity exposed to the model matters
independently of natural class distribution. Up-weighting rare classes
(PLS, CA-CTCF, CA-TF) adds informative examples. cCRE class is a
useful proxy for regulatory-context diversity.

Cumulative ranking (mean across 14 evals):
006 stratified cCRE      0.7754  ← best
002 cCRE uniform         0.7619
001 random uniform       0.7321
005 random genomic       0.7016
004 motifs in random     0.6824
003 dinuc-shuf cCRE      0.6595

**Next-experiment plan (007):** mix 40K stratified cCREs + 10K uniform
random. Tests the coverage-vs-signal tradeoff identified across 003-005:
random has broad coverage (and dominates eval_08), cCREs have signal.
Can we have both?
- 007 > 006 → strict improvement; mixing recovers coverage hole
- 007 ≈ 006 → mix gains balance dilution losses
- 007 < 006 → cCRE composition matters; dilution outweighs coverage gain

## 2026-04-27 — Result: 007 cCRE strat + random mix

**Headline:** eval_01 = **0.7276**, mean ≈ **0.767**.
−0.009 vs 006 on eval_01, −0.008 on mean.

eval_08 recovered from 0.682 → 0.702 (+0.019), but every other eval
lost ~0.01. Net loss.

**T5/T6:** Library quality is roughly proportional to fraction of
real regulatory elements. Random dilutes signal. The eval_08 hole is
real but should be tolerated, not chased by adding random — it costs
more than it returns. eval_08 is likely measuring different sequence-
space content than the other 13 evals.

**Next-experiment plan (008):** switch annotation source — DHS Index
(Meuleman 2020, ~3.5M DNase-hypersensitive sites with NMF cell-type
loadings). Different regulatory annotation may capture different/more
diverse regulatory contexts than ENCODE cCREs.
- 008 ≈ 002 → annotation source neutral
- 008 > 006 → DHS captures more useful diversity (consider switching base)
- 008 < 002 → cCREs are the better curation for ML training













## 2026-04-27 — Result: 008 DHS Index uniform

**Headline:** eval_01 = **0.6914**, mean ≈ **0.7297**.
**−0.035 vs 002** on eval_01, **−0.037 on mean**. Loses on **all 14**
evals by 0.031–0.051. Strong, uniform signal.

DHS uniform across-seed SD ≈ 0.012 (lower than 002's ≈ 0.025) — so
this is well-resolved, not noise. 008 is firmly worse than 002.

**T7 (new):** Annotation curation matters more than annotation breadth.
ENCODE cCREs apply multi-mark filtering (DNase + H3K4me3 + H3K27ac +
CTCF) and class assignment; DHS uniform sampling is biased toward weak
sites called in 1-2 samples. cCREs are a better curation for MPRA
training at equal sequence count.

**T6 (refined):** "Real regulatory content" is not monolithic. The
quality of the regulatory annotation is a first-order driver of library
informativeness — uniform DHS sampling underperforms uniform cCRE
sampling by ~0.04, comparable in magnitude to the cCRE-vs-random
gap (~0.03).

Cumulative ranking (mean across 14 evals):
006 stratified cCRE      0.7754  ← best
002 cCRE uniform         0.7619
007 cCRE strat + random  0.7672
001 random uniform       0.7321
008 DHS uniform          0.7297
005 random genomic       0.7016
004 motifs in random     0.6824
003 dinuc-shuf cCRE      0.6595

**Next-experiment plan (009):** filter DHS by signal strength. Take
top-quartile mean_signal × numsamples ≥ 5, sample 50K uniformly. Tests
whether the curation effect (T7) is the active variable.
- 009 ≈ 002 → filtering recovers cCRE-level performance; the difference
  was peak-strength noise.
- 009 > 008 (gap ≥ 0.02) but < 002 → filtering helps but cCRE
  class-typing adds independent value (T7 partially supported).
- 009 ≈ 008 → filtering doesn't help; cCRE curation does something
  qualitatively different (regulatory-class assignment).

This isolates ONE axis (peak quality) from the cCRE-vs-DHS gap and
distinguishes "noise" from "annotation design" as the cause.

## 2026-04-27 — Result: 009 DHS filtered by signal strength

**Headline:** eval_01 = **0.7106**, mean ≈ **0.7500**.
+0.020 vs 008, −0.017 vs 002. **Filtering closed ~55% of the
cCRE-DHS gap.**

Per-eval delta vs 008: +0.019 +0.021 +0.016 +0.033 +0.019 +0.021
+0.001 +0.043 +0.038 +0.034 +0.018 +0.014 −0.014 +0.022. Helps 13/14.
Strongest gains: eval_08 (+0.043) and eval_09 (+0.038).

vs 002 cCRE uniform, still loses on 12/14 evals but margin halved.

**T7 (refined):** Annotation curation has two separable axes:
(a) peak-quality filtering accounts for ~55% of the cCRE-DHS gap.
(b) regulatory class-typing + multi-mark filtering accounts for ~45%
beyond peak strength. Both contribute; neither alone is sufficient.

Across-seed SD = 0.038 (higher than 008's 0.012). Filtering shrinks
the pool 5x and increases seed variability — sampling matters more
when the pool is smaller.

Cumulative ranking (mean across 14 evals):
006 stratified cCRE      0.7754  ← best
007 cCRE strat + random  0.7672
002 cCRE uniform         0.7619
009 DHS filtered         0.7500
001 random uniform       0.7321
008 DHS uniform          0.7297
005 random genomic       0.7016
004 motifs in random     0.6824
003 dinuc-shuf cCRE      0.6595

**Next-experiment plan (010):** TF-aware stratification within cCRE.
006 stratified by 8 cCRE classes; sub-stratify by **dominant JASPAR
motif family** within each class. Plan: scan each cCRE for top-scoring
JASPAR motif (FIMO-style threshold), bin sequences as
(cCRE_class × motif_family); sample 50K with capped per-bin counts to
upweight rare TF combinations.

- 010 > 006 → TF diversity helps beyond class diversity (extends T5)
- 010 ≈ 006 → cCRE class already captures the relevant axis
- 010 < 006 → forcing TF balance dilutes natural cCRE composition
  (mirrors the 007 lesson at the motif scale)

This directly probes whether motif-level diversity is a separate
informativeness axis, refining T5.

## 2026-04-27 — Result: 010 cCRE TF×class stratified

**Headline:** eval_01 = **0.7122**, mean ≈ **0.7493**.
**−0.026 vs 006 on mean. LOSES on all 14 evals.** Only weak gains
on eval_04 and eval_09 vs 002 (mirroring 006's strengths).

168 (class × top-motif) bins. Per-bin cap 320. PWM scoring with 20
archetypal TF motifs from JASPAR. Top bins: PLS-SP1, CA-TF-FOS,
dELS-RUNX1.

**T8 (new):** Diversity-by-stratification has diminishing — and
eventually negative — returns:
- cCRE class (8 bins, 006): +0.013 vs uniform
- cCRE class × TF (168 bins, 010): −0.026 vs class-only

Too-fine stratification creates bins of biologically-noisy
sequences (e.g., dELS with strong TP53 motif, or CA-CTCF without
strong CTCF motif) and dilutes the signal-rich majority.
**Optimal stratification = the coarsest axis that still captures
meaningful biological diversity.** This is the same lesson as 007's
random dilution, applied at the within-cCRE motif scale.

**T5 (refined):** Class-level diversity helps because rare classes
still represent **well-formed regulatory units**. Sub-typing by motif
identity shifts mass to atypical (class × motif) combinations that
are not representative training material.

Cumulative ranking (mean across 14 evals):
006 stratified cCRE      0.7754  ← best, holds
007 cCRE strat + random  0.7672
002 cCRE uniform         0.7619
010 cCRE TF-strat        0.7493
009 DHS filtered         0.7500
001 random uniform       0.7321
008 DHS uniform          0.7297
005 random genomic       0.7016
004 motifs in random     0.6824
003 dinuc-shuf cCRE      0.6595

**Next-experiment plan (011):** Test the OPPOSITE direction —
**coarser stratification**. Collapse 8 cCRE classes into 3
super-classes:
- promoters: PLS + pELS + CA-H3K4me3
- distal-enhancers: dELS + CA + TF
- insulators/TF-only: CA-CTCF + CA-TF
50K with equal counts per super-class.
- 011 ≈ 006 → granularity neutral; what matters is having buckets
- 011 > 006 → coarser is strictly better (T8 strong reading)
- 011 < 006 → 8-class is the right unit; coarser is too coarse

Together with 010 this brackets the right stratification scale.

## 2026-04-28 — Result: 011 cCRE 3-superclass

**Headline:** eval_01 = **0.7286**, mean ≈ **0.7715**.
−0.004 vs 006 on mean. Wins on **eval_07/08/10/13** (the four evals
006 was weakest on); loses on the other 10 by small margins.

Eval-range narrower: 011 spans 0.692–0.840 (=0.147), 006 spans
0.682–0.857 (=0.175). 011 is more uniform, 006 has higher peak.

**T8 (refined):** Stratification has a sweet spot near 8 cCRE classes.
Bracketing:
- 3 super-classes (011): mean 0.7715  (−0.004 vs 006)
- 8 cCRE classes (006): mean 0.7754   ← best
- 168 (class × motif) (010): mean 0.7493 (−0.026 vs 006)

8-class is at or very near optimum. Coarsening gives near-zero loss
plus uniformity gain; fine-graining causes substantial loss.

**T9 (new):** Eval-set heterogeneity → Pareto trade-off. The eval-cluster
{07, 08, 10, 13} responds to broader sequence coverage (random,
super-classes); the cluster {01-06, 09, 11, 12, 14} responds to
fine-grained class-aware curation. There appear to be two evaluation
modes; the "best" library depends on the weighting we care about.

Cumulative ranking (mean across 14 evals):
006 stratified cCRE      0.7754  ← best, holds
011 cCRE 3-superclass    0.7715
007 cCRE strat + random  0.7672
002 cCRE uniform         0.7619
009 DHS filtered         0.7500
010 cCRE TF-strat        0.7493
001 random uniform       0.7321
008 DHS uniform          0.7297
005 random genomic       0.7016
004 motifs in random     0.6824
003 dinuc-shuf cCRE      0.6595

**Next-experiment plan (012):** rare-class up-weighting within 8-class
scheme. Use 8K each for the 4 rare classes (PLS, CA-CTCF, CA-TF,
CA-H3K4me3) and 4.5K each for the 4 abundant (pELS, dELS, CA, TF).
Total 50K. Tests whether per-class learning is information-limited at
6,250 examples per class (006).

- 012 > 006 → rare-class info bottleneck; INVERSE-frequency weighting
  beats equal weighting (extends T8)
- 012 ≈ 006 → 6,250 saturating per-class
- 012 < 006 → rare class pools lack 8K-deep unique signal; redundant

## 2026-04-28 — Result: 012 cCRE rare-class upweighted

**Headline:** eval_01 = **0.7391**, mean ≈ **0.7819**.
**+0.002 vs 006 on eval_01, +0.0065 on mean. WINS ON ALL 14 EVALS.**
New best library, strictly Pareto-dominates 006.

Per-eval delta vs 006: +0.002 +0.004 +0.005 +0.012 +0.003 +0.004
+0.009 +0.010 +0.014 +0.010 +0.003 +0.003 +0.011 +0.004. Strongest
gains on eval_04, 07, 08, 09, 10, 13.

Critically, the eval_07/08/10/13 cluster (T9 broad-coverage) ALSO
improves — so inverse-frequency weighting closes the Pareto gap from
011, getting both clusters at once.

**T8 (further refined):** Equal-class stratification (006) was
suboptimal — rare classes still under-represented at 6,250 examples
relative to their unique signal. Inverse-frequency weighting (~1/sqrt
pool size) strictly beats equal weighting. The optimum class count is
NOT uniform; it slopes inversely against pool size.

Cumulative ranking (mean across 14 evals):
**012 cCRE rare-upweight    0.7819  ← NEW BEST**
006 stratified cCRE        0.7754
011 cCRE 3-superclass      0.7715
007 cCRE strat + random    0.7672
002 cCRE uniform           0.7619
009 DHS filtered           0.7500
010 cCRE TF-strat          0.7493
001 random uniform         0.7321
008 DHS uniform            0.7297
005 random genomic         0.7016
004 motifs in random       0.6824
003 dinuc-shuf cCRE        0.6595

**Next-experiment plan (013):** push the gradient further. Try
**10K rare / 2.5K abundant** — extends the inverse-frequency direction
that already paid off (006 6.25K equal → 012 8K/4.5K → 013 10K/2.5K).
- 013 > 012 → curve still rising; rare upweighting still gaining
- 013 ≈ 012 → 8K is at the per-class saturation point
- 013 < 012 → abundant classes contribute meaningfully even at 4.5K;
  reducing them to 2.5K is too aggressive

## 2026-04-28 — Result: 013 cCRE extreme rare-upweight (10K/2.5K)

**Headline:** eval_01 = **0.7477**, mean ≈ **0.7900**.
**+0.009 vs 012 on eval_01, +0.008 on mean. WINS ON ALL 14 EVALS.**
NEW BEST. Curve still climbing.

Cross-seed SD (eval_01) = 0.008 — much lower than 006's 0.030.
Extreme rare-upweighting is more stable AND higher mean.

Cumulative gain over 006 baseline: +0.011 to +0.022 per eval, average
**+0.015**. Largest gains: eval_07 (+0.019), eval_08 (+0.022),
eval_09 (+0.022).

**T8 (further refined):** Per-class learning curve for rare cCRE
classes still rising at 10K. Abundant classes at 2.5K still retain
core signal. Optimum is more extreme than 1/sqrt-pool weighting.

**T10 (new):** rare cCRE classes have higher unique-information-
per-sample than abundant ones. dELS (1.47M) is highly redundant;
CA-TF (26K) is information-dense. Information density slope is
STEEPER than 1/N would suggest.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← NEW BEST**
012 cCRE rare-upweight       0.7819
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
001 random uniform           0.7321
008 DHS uniform              0.7297
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

**Next-experiment plan (014):** push to the **rare-only LIMIT**.
12.5K each from PLS, CA-CTCF, CA-TF, CA-H3K4me3 (50K total). No
abundant classes at all. Pinpoints whether the optimum is "rare-only"
or whether abundant classes contribute irreducibly.
- 014 > 013 → rare-only is the limit; abundant classes add nothing
- 014 ≈ 013 → abundant near-negligible at 2.5K
- 014 < 013 → abundant classes contribute irreducible signal even
  at 2.5K; can't drop entirely

## 2026-04-28 — Result: 014 cCRE rare-only

**Headline:** eval_01 = **0.6856**, mean ≈ **0.7155**.
**−0.075 vs 013 on mean. LOSES on all 14 evals by 0.053-0.112.**
Largest losses on broad-coverage cluster: eval_07 (-0.102),
eval_08 (-0.112), eval_13 (-0.100). Falsifies "rare-only is the limit".

**T11 (new):** Abundant cCRE classes have a FLOOR count below which
performance collapses. 2.5K (013) was near floor; 0K collapses by
0.075. Hypothesis: abundant classes contribute genomic-context
diversity (intergenic enhancer variants, distal-promoter mixing)
that rare regulatory classes alone cannot supply.

**T12 (new):** The broad-coverage eval cluster (T9: 07/08/13) requires
distal-enhancer abundance specifically. Each lost ≥0.10 — the largest
deltas in the experiment.

**T8 (final form):** Inverse-frequency optimum is BETWEEN 006 (equal
6.25K) and 014 (rare-only). 013 (10K rare, 2.5K abundant) is best
seen so far; the optimum is plausibly very close to 013, perhaps
slightly toward 11K rare / 1.5K abundant.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← best, holds**
012 cCRE rare-upweight       0.7819
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
001 random uniform           0.7321
008 DHS uniform              0.7297
014 cCRE rare-only           0.7155
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

**Next-experiment plan (015):** tighten the bracket. **11K rare / 1.5K
abundant** — between 013 (10K/2.5K, 0.7900) and 014 (12.5K/0K, 0.7155).
- 015 > 013 → optimum is closer to rare-only than 013; sharper peak
- 015 ≈ 013 → 10K rare saturating; 1.5K abundant still enough
- 015 < 013 → 2.5K is the floor for abundant; 1.5K collapses

## 2026-04-28 — Result: 015 cCRE bracket 11K/1.5K

**Headline:** eval_01 = **0.7391**, mean ≈ **0.7802**.
**−0.010 vs 013 on mean. Loses on all 14 evals.** Modest collapse,
not catastrophic — confirms 013 (10K/2.5K) is the optimum and the
abundant-class floor is graduated, not cliff-like.

Notable: 015 mean ≈ 012 mean (0.7802 vs 0.7819, within seed-SD).
Different rare/abundant split, same total info — there's a continuous
Pareto frontier with 013 at the peak.

**T8 (closed):** Optimum cCRE class-balance for N=50K is ~10K rare
/ 2.5K abundant. Five experiments bracket this tightly.

**T11 (refined):** Abundant-class floor is graduated:
- 4.5K (012): mean 0.7819
- 2.5K (013): mean 0.7900 ← peak
- 1.5K (015): mean 0.7802 (−0.010)
- 0K (014):   mean 0.7155 (−0.075)
Effective floor near 2K-2.5K per abundant class.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← best, holds**
012 cCRE rare-upweight       0.7819
015 cCRE bracket 11K/1.5K    0.7802
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
001 random uniform           0.7321
008 DHS uniform              0.7297
014 cCRE rare-only           0.7155
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

**Next-experiment plan (016):** new axis — **principled
1/sqrt(pool_size) per-class weighting**. 013 used uniform-within-rare
+ uniform-within-abundant. The 1/sqrt scheme weights CA-TF (26K pool)
highest and dELS (1.47M pool) lowest:
PLS=9400, CA-CTCF=5700, CA-TF=12600, CA-H3K4me3=7300,
pELS=4100, dELS=1700, CA=4100, TF=6300 (sum=50K).
- 016 > 013 → 1/sqrt-pool is the right principle for class info density
- 016 ≈ 013 → 013's coarse split is sufficient
- 016 < 013 → CA-CTCF info is high even with large pool; pool-size
  alone doesn't predict per-class informativeness

## 2026-04-28 — Result: 016 cCRE 1/sqrt(pool) weighting

**Headline:** eval_01 = **0.7294**, mean ≈ **0.7694**.
**−0.021 vs 013 on mean. LOSES on all 14 evals by 0.015-0.032.**
Largest losses on broad-coverage cluster (07/08/13). Falsifies the
1/sqrt-pool principle.

Per-class count change (013 → 016):
- PLS:        10K → 9.1K (−9%)
- CA-CTCF:    10K → 5.6K (**−44%**)  ← biggest single change
- CA-TF:      10K → 12.3K (+23%)
- CA-H3K4me3: 10K → 7.1K (−29%)
- pELS:       2.5K → 4.0K (+60%)
- dELS:       2.5K → 1.6K (−34%)
- CA:         2.5K → 4.0K (+61%)
- TF:         2.5K → 6.1K (+146%)

Across-seed SD on eval_01 ≈ 0.030 (vs 013's 0.008) — smaller pool
fractions inject more sampling noise.

**T10 (revised):** Class info-density is NOT a function of pool size.
CA-CTCF (126K pool) is as information-dense as CA-TF (26K pool);
dropping CA-CTCF by 44% costs the most. dELS (1.47M pool) is
information-sparse — it covers a heterogeneous mix of distal contexts.

**T13 (new — functional specificity > pool size):** Stratification
weights should reflect **functional specificity**, not pool size. The
013 partition was lucky-correct because its "rare" cluster {PLS,
CA-CTCF, CA-TF, CA-H3K4me3} happens to align with functionally
specific cCRE classes (promoter-like, CTCF, TF-only, H3K4me3-marked
CA), and its "abundant" cluster {pELS, dELS, CA, TF} happens to be
heterogeneous-enhancer-like + generic-CA/TF. Coincidence reveals the
true principle.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← best, holds**
012 cCRE rare-upweight       0.7819
015 cCRE bracket 11K/1.5K    0.7802
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
016 cCRE 1/sqrt-pool         0.7694
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
001 random uniform           0.7321
008 DHS uniform              0.7297
014 cCRE rare-only           0.7155
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

**Next-experiment plan (017):** switch to a fundamentally orthogonal
axis — **motif augmentation on top of 013**. Take 013-style cCRE
samples (10K rare / 2.5K abundant) and for each, insert one
randomly-sampled JASPAR archetype motif at a random position
(overwriting 6-15 native bases). Tests whether motif density adds
independent signal on top of the optimal class-balance.
- 017 > 013 → motif density is a separate informative axis (extends T5)
- 017 ≈ 013 → cCRE motif content is already saturated
- 017 < 013 → forced motif insertion disrupts native cCRE grammar
  (consistent with 004's "motif in random scaffold" failure)

## 2026-04-28 — Result: 017 cCRE 013 + motif augmentation

**Headline:** eval_01 = **0.7200**, mean ≈ **0.7595**.
**−0.031 vs 013 on mean. LOSES on all 14 evals by 0.024-0.043.**
Largest losses on broad-coverage cluster (07, 13). Across-seed
SD = 0.026, 3× higher than 013 (random insert position adds noise).

Same shape as 004: forced motif insertion in non-native context
hurts. Even when the cCRE base library is the strongest known, random
motif placement breaks the local sequence grammar enough to lose
0.031.

**T5 (refined → context-dependence law):** Motif-axis informativeness
is NOT independent of context. Three failed motif-augmentation
experiments form a pattern:
- 004: motif in random scaffold (0.6824) << random (0.7321)  Δ=−0.050
- 010: motif-balanced cCRE (0.7493) << uniform cCRE (0.7619)  Δ=−0.013
- 017: motif in 013 (0.7595) << 013 (0.7900)                  Δ=−0.031

Pattern: ANY non-native motif placement hurts, regardless of base
library quality.

**T14 (new — context-dependence is paramount):** For cell-type-
generalizing models, motif informativeness derives from native
context co-occurrence, not raw motif density. Library design must
preserve native sequence grammar; constructing or augmenting
sequences artificially discards the conditional dependencies the
model needs to learn.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← best, holds**
012 cCRE rare-upweight       0.7819
015 cCRE bracket 11K/1.5K    0.7802
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
016 cCRE 1/sqrt-pool         0.7694
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
017 cCRE 013 + motif aug     0.7595
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
001 random uniform           0.7321
008 DHS uniform              0.7297
014 cCRE rare-only           0.7155
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

**Next-experiment plan (018):** test whether the rare-class
upweighting principle (T8) generalizes from cCRE to DHS. The Meuleman
DHS Index labels each site with a primary NMF component (16 broad
cell-type vocabularies). Component sizes are skewed — the abundant
ones cover broad housekeeping accessibility, rare ones (e.g., specific
tissue types) cover more functionally specific accessibility. Apply
013's principle: upweight rare components.
- 018 > 013 → rare-class principle is universal across atlases
- 018 ≈ 013 → DHS works equally well with same principle
- 018 < 013 → DHS is intrinsically less informative than cCRE (echoes
  002 vs 008); cCRE class boundaries are more meaningful

## 2026-04-28 — Result: 018 DHS rare-component upweighted

**Headline:** eval_01 = **0.6911**, mean ≈ **0.7331**.
**−0.057 vs 013 on mean. LOSES on all 14 evals by 0.029-0.078.**
The cCRE rare-class principle does NOT generalize to DHS.

Comparison among DHS recipes:
- 008 DHS uniform:        0.7297
- 009 DHS filtered:       0.7500
- 018 DHS rare-component: 0.7331  (≈ 008, *worse* than 009)

The principle that gained +0.028 (006→013) in cCRE LOSES 0.017
(009→018) in DHS. Striking asymmetry.

**T13 (strongly reinforced):** Functional specificity, not pool size,
drives upweighting gains. cCRE classes are *regulatory-mechanism*
labels; DHS NMF components are *cell-type-loading* labels. Two DHS
sites in different components can have nearly identical regulatory
sequence; two cCREs in different classes likely cannot.

**T15 (new — atlas labels matter):** Stratification gains depend on
whether labels partition along the *axis the model needs to learn*.
cCRE class boundaries align with regulatory-mechanism syntax (what
the model needs); DHS components align with tissue activity (what
sequence + cell-type input already encodes). Wrong-axis upweighting
adds noise, not signal.

**T7 (refined):** cCRE > DHS holds even under matched preprocessing
(same q75 + ≥5 samples filter, same 4:1 upweighting). The cCRE atlas
inherently provides a more informative partition for this task.

Process note: spark06 NFS hang blocked the multi-seed pipeline;
ran each seed sequentially via single-seed mode on local GPU and
assembled averaged result.json manually. 2057s for 3 seeds.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← best, holds**
012 cCRE rare-upweight       0.7819
015 cCRE bracket 11K/1.5K    0.7802
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
016 cCRE 1/sqrt-pool         0.7694
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
017 cCRE 013 + motif aug     0.7595
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
018 DHS rare-component up    0.7331
001 random uniform           0.7321
008 DHS uniform              0.7297
014 cCRE rare-only           0.7155
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

**Next-experiment plan (019):** mix cCRE (013) with filtered DHS
(009-style). 25K from 013 (5K each rare class, 1.25K each abundant)
+ 25K from filtered-DHS uniform pool. Tests whether DHS adds any
*independent* signal on top of cCRE — different from 018 which tested
whether the same upweighting *principle* generalizes.
- 019 > 013 → DHS atlas adds independent signal even though atlas-
  level rebalancing is weak (atlases are complementary)
- 019 ≈ 013 → DHS redundant given cCRE
- 019 < 013 → DHS dilutes cCRE quality (echoes 007 mix-with-random
  failure); pure 013 is best

## 2026-04-28 — Result: 019 cCRE 013 + filtered DHS mix (50/50)

**Headline:** eval_01 = **0.7339**, mean ≈ **0.7768**.
**−0.014 vs 013 on mean. LOSES on all 14 evals by 0.002-0.023.**
DHS dilutes cCRE quality, but only modestly.

Per-eval delta vs 013:
01:−0.014 02:−0.013 03:−0.015 04:−0.012 05:−0.014 06:−0.013 07:−0.023
08:−0.002 09:−0.014 10:−0.003 11:−0.013 12:−0.005 13:−0.022 14:−0.013

Smallest deltas on eval_08 (−0.002) and eval_10 (−0.003) — broad-
coverage benchmarks where DHS's tissue-spanning sites help. Largest
deltas on eval_07 (−0.023) and eval_13 (−0.022) — likely
regulatory-mechanism-heavy benchmarks where DHS adds non-cCRE noise.

Per-seed eval_01: 0.7278 / 0.7378 / 0.7362 → SD ≈ 0.005
(very stable, cleanly inside 013's noise floor).

**T16 (new — atlas mixing dilutes):** Mixing the best atlas (cCRE +
013 upweighting) with broader-but-less-specific data (DHS) costs
performance on average. Confirms 007's mix-with-random pattern and
extends it: even *another curated atlas* (filtered DHS) is dilutive
when added to a strong cCRE recipe. Two corollaries:
- The cCRE atlas already covers what the model needs to learn — DHS
  doesn't add complementary regulatory grammar.
- Mixing only helps where target eval emphasizes broad-coverage
  recall (eval_08/10); for regulatory-mechanism evals it hurts.

**T7 (further refined):** Even when DHS is *added on top of* cCRE
(rather than substituted), cCRE-only wins. The DHS atlas does not
contain regulatory grammar that the cCRE atlas misses.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← best, holds**
012 cCRE rare-upweight       0.7819
015 cCRE bracket 11K/1.5K    0.7802
019 cCRE 013 + DHS mix       0.7768  ← new
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
016 cCRE 1/sqrt-pool         0.7694
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
017 cCRE 013 + motif aug     0.7595
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
018 DHS rare-component up    0.7331
001 random uniform           0.7321
008 DHS uniform              0.7297
014 cCRE rare-only           0.7155
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

Process note: spark06 still hung; ran each seed via single-seed mode
on local GPU and averaged manually. 2805s.

**Next-experiment plan (020):** test whether the cCRE *element* or
the cCRE + *flanking genomic context* drives 013's performance.
Use only cCREs ≥200bp wide (~1.88M of 2.35M cCREs), crop to central
200bp = pure cCRE sequence with NO flanking genomic context. Apply
013's 10K rare / 2.5K abundant scheme on this width-filtered pool.
- 020 > 013 → flanking context is noise; pure cCRE is more
  informative; cCRE boundaries are where the function lives
- 020 ≈ 013 → flank is neutral
- 020 < 013 → flanking genomic context adds useful signal (cCRE
  boundaries are imperfect; surrounding context helps)

## 2026-04-28 — Result: 020 cCRE 013 width-filtered, no genomic flank

**Headline:** eval_01 = **0.6969**, mean ≈ **0.7317**.
**−0.058 vs 013 on mean. LOSES on all 14 evals by 0.038-0.083.**
**Flanking genomic context contributes substantially to 013's gains.**

The cCRE element alone (no flank) drops to ~008/018 levels. Among all
20 experiments, 020 ranks 15th — between 018 (DHS rare-up, 0.7331)
and 008 (DHS uniform, 0.7297). Removing flank costs more than
swapping atlases.

Per-eval delta vs 013:
01:−0.051 02:−0.056 03:−0.061 04:−0.038 05:−0.051 06:−0.056 07:−0.079
08:−0.083 09:−0.044 10:−0.062 11:−0.050 12:−0.054 13:−0.077 14:−0.056

Largest losses on eval_07, eval_08, eval_13 (−0.077 to −0.083) —
the same evals where 019 lost least. So the eval-set distribution
hints: regulatory-mechanism evals depend on cCRE+flank; broad-
coverage evals (eval_08) are most sensitive to *element vocabulary
breadth*.

Per-seed eval_01: 0.6780 / 0.7341 / 0.6787 → SD ≈ 0.032 (4x 013).
Bimodal: 2 seeds at ~0.68, 1 seed at ~0.73 (with 920s training vs
~500s for the others — early stopping on no-flank libraries hits
worse optima). Even the best-seed result (0.734) is below all cCRE
recipes that include flank.

**T17 (new — flanking genomic context is informative):** The 200bp
window captures more than the cCRE element itself; the ~50bp average
flank around the cCRE peak contributes ≈0.058 mean correlation.
Possible mechanisms: (a) cCRE boundary calls underestimate the true
regulatory element; (b) flanking sequence carries co-binding TF
motifs, nucleosome positioning, or local GC context that completes
the regulatory grammar; (c) flank acts as an implicit class hint
(the surrounding genome differs systematically across cCRE classes).

**T13 (re-refined):** Functional specificity helps, but element
*boundaries are not the unit of function*. cCRE calls are peak
centers, not sharp regulatory boundaries; the model needs ~100bp
around the peak.

**T8 (refined):** Rare-class upweighting is a multiplier on a base
recipe, not a substitute for getting the window right. Strip flank
and the upweighting gain shrinks but doesn't reverse: 020 (0.7317)
> 014 rare-only-with-flank (0.7155), so the 4-class structure still
helps even without flank.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← best, holds**
012 cCRE rare-upweight       0.7819
015 cCRE bracket 11K/1.5K    0.7802
019 cCRE 013 + DHS mix       0.7768
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
016 cCRE 1/sqrt-pool         0.7694
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
017 cCRE 013 + motif aug     0.7595
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
018 DHS rare-component up    0.7331
001 random uniform           0.7321
020 cCRE 013 no-flank        0.7317  ← new
008 DHS uniform              0.7297
014 cCRE rare-only           0.7155
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

**Next-experiment plan (021):** test positional invariance of the
cCRE-centered window. 013's recipe always places the cCRE midpoint
exactly at window center (offset 100bp from each edge). The model
may overfit to this position. 021 keeps 013's class counts but
*off-centers* the extraction: cCRE midpoint is placed uniformly at
random in the window's central ±50bp (still leaving the cCRE inside
the 200bp).
- 021 > 013 → off-center forces position-invariant features that
  generalize better
- 021 ≈ 013 → model already learns position-invariant features
- 021 < 013 → centered training is optimal; the position is a
  consistent inductive prior the model exploits

## 2026-04-28 — Result: 021 cCRE 013 off-center extraction

**Headline:** eval_01 = **0.7240**, mean ≈ **0.7617**.
**−0.028 vs 013 on mean. LOSES on all 14 evals by 0.021-0.044.**
Positional jitter dilutes — model exploits centered cCRE prior.

Per-eval delta vs 013:
01:−0.024 02:−0.026 03:−0.028 04:−0.021 05:−0.024 06:−0.026 07:−0.039
08:−0.044 09:−0.022 10:−0.035 11:−0.023 12:−0.025 13:−0.036 14:−0.026

Largest losses on the same evals as 020 (eval_07/08/13) — the
flank-sensitive ones — which is unsurprising since off-centering
is a milder form of context perturbation than flank removal.

Per-seed eval_01: 0.729 / 0.693 / 0.750 → SD ≈ 0.024.
Same high-variance / training-length coupling as 020.

**T18 (new — positional prior matters, half as much as flank):**
Model is not fully position-invariant. Centered-cCRE prior
contributes ~0.028 mean correlation; flank content ~0.058 (T17).
Both effects appear additive (independent mechanisms).

**T8 ablation breakdown of 013's gain over 006 stratified:**
- Rare-class upweighting (T8 itself):     +0.015
- Cognate flank context (T17, est):       +0.058
- Centered positional prior (T18, est):   +0.028
- (Functional class specificity baked in)
Recipe gains are multiplicative-additive; flank+position dominate.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight  0.7900  ← best, holds**
012 cCRE rare-upweight       0.7819
015 cCRE bracket 11K/1.5K    0.7802
019 cCRE 013 + DHS mix       0.7768
006 stratified cCRE          0.7754
011 cCRE 3-superclass        0.7715
016 cCRE 1/sqrt-pool         0.7694
007 cCRE strat + random      0.7672
002 cCRE uniform             0.7619
021 cCRE 013 off-center      0.7617  ← new
017 cCRE 013 + motif aug     0.7595
009 DHS filtered             0.7500
010 cCRE TF-strat            0.7493
018 DHS rare-component up    0.7331
001 random uniform           0.7321
020 cCRE 013 no-flank        0.7317
008 DHS uniform              0.7297
014 cCRE rare-only           0.7155
005 random genomic           0.7016
004 motifs in random         0.6824
003 dinuc-shuf cCRE          0.6595

Process note: spark06 NFS hang persists. Multi-seed prepare.py
exited(1) after spark06 hang despite spark01/03 succeeding —
re-ran via single-seed local mode (seed 0 result matches the
spark01 reading exactly, confirming model_seed=0 determinism).

**Next-experiment plan (022):** isolate T17 mechanism. Take 013
cCREs, extract 200bp centered on midpoint, then *replace* the outer
50bp on each side with random hg38 main-chrom windows. The middle
100bp = cognate cCRE region; outer 100bp = random-genome flank.
- 022 ≈ 013 → flank is scaffold; specific content doesn't matter
- 022 ≈ 020 → cognate flank specifically matters (co-binding TFs,
  nucleosome positioning, cell-type-specific local context)
- 022 between → both mechanisms contribute partially

This cleanly separates "flank as receptive-field-filler" from
"flank as regulatory-grammar-component".

## 2026-04-28 — Result: 022 cCRE 013 with random-genomic flank

**Headline:** eval_01 = **0.7447**, mean ≈ **0.7873**.
**−0.003 vs 013 on mean — essentially indistinguishable.**
Random flank ≈ cognate flank. **T17 was wrong about the mechanism.**

Per-eval delta vs 013:
01:−0.003 02:−0.004 03:−0.005 04:−0.012 05:−0.003 06:−0.004 07:−0.019
08:**+0.049** 09:−0.014 10:−0.002 11:−0.003 12:−0.002 13:−0.012 14:−0.004

Most evals within +-0.005 of 013. eval_08 actually GAINS +0.049 with
random flanks — broader-coverage eval benefits from genome-spread
background. eval_07 loses most (−0.019). Net: 022 ≈ 013.

**T17 (REVISED — flank is scaffold, not regulatory signal):**
The cCRE element itself carries the signal; surrounding ~50bp×2
acts as receptive-field context for the convnet. ANY DNA there
works. The earlier T17 interpretation (cognate flank → co-binding
TFs / nucleosome / cell-type context) is overturned.

**T19 (new — 020's loss was selection bias):** Width-filter
to ≥200bp cCREs selects broader, less-sharp regulatory regions.
Sharp narrow cCREs (<200bp, ~20% of pool) carry concentrated
regulatory content; removing them loses signal. The flank-removal
interpretation was confounded.

**T13 (strengthened):** cCRE midpoint IS the regulatory unit.
~100bp around the called peak captures nearly all of 013's signal.
ENCODE's midpoint annotations are well-aligned to true peaks;
boundary calls are loose.

**T8 ablation REVISED:** 013's gain over random comes from:
- cCRE element (~100bp around midpoint): MOST of the gain
- Class composition (rare upweighting): +0.015 over 006
- Centered positional prior: +0.028 (T18)
- Flank content: ~0.003 (negligible — was thought to be 0.058)

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight   0.7900  ← best, holds**
**022 cCRE 013 random-flank   0.7873  ← effectively tied with 013**
012 cCRE rare-upweight        0.7819
015 cCRE bracket 11K/1.5K     0.7802
019 cCRE 013 + DHS mix        0.7768
006 stratified cCRE           0.7754
011 cCRE 3-superclass         0.7715
016 cCRE 1/sqrt-pool          0.7694
007 cCRE strat + random       0.7672
002 cCRE uniform              0.7619
021 cCRE 013 off-center       0.7617
017 cCRE 013 + motif aug      0.7595
009 DHS filtered              0.7500
010 cCRE TF-strat             0.7493
018 DHS rare-component up     0.7331
001 random uniform            0.7321
020 cCRE 013 no-flank         0.7317
008 DHS uniform               0.7297
014 cCRE rare-only            0.7155
005 random genomic            0.7016
004 motifs in random          0.6824
003 dinuc-shuf cCRE           0.6595

**Next-experiment plan (023):** find the minimum cCRE region size
that preserves 013's signal. Take ALL cCREs (013 composition, no
width filter), extract 50bp around midpoint, pad with 75bp random
hg38 flank each side = 200bp.
- 023 ≈ 013 → 50bp cCRE peak is enough; even smaller regulatory unit
- 023 between 022 and 020 → ~100bp cCRE needed; can pinpoint
- 023 ≈ 020 → cCRE region needs >100bp; we hit the limit at 022

This both refines the regulatory-unit-size estimate and
cross-checks T19 (020's loss was selection bias).

## 2026-04-28 — Result: 023 cCRE 013 with 50bp cognate + 150bp random flank

**Headline:** eval_01 = **0.7351**, mean across 14 = **0.7784**.
**−0.012 vs 013, −0.009 vs 022 on mean.** Real but modest loss.
50bp cognate is enough for most signal but not all.

Per-eval delta vs 013:
01:−0.013 02:−0.013 03:−0.013 04:−0.030 05:−0.013 06:−0.013 07:−0.027
08:**+0.061** 09:−0.036 10:−0.012 11:−0.012 12:−0.010 13:−0.019 14:−0.013

Tight pattern. Most evals lose 0.010-0.013, three lose 0.019-0.036
(04, 07, 09 — same evals 022 also dipped). **eval_08 gains +0.061**,
even bigger than 022's +0.049 (013→022→023: 0.7044→0.7529→0.7649).

Per-seed eval_01: 0.7463 / 0.7222 / 0.7369 (SD ≈ 0.012, tighter than 022).

**Cognate-region size gradient (T20, new):**
| cognate | random flank | mean across 14 | delta vs 013 |
|---|---|---|---|
| 200bp (013) | 0bp   | 0.7900 |  0.000 |
| 100bp (022) | 100bp | 0.7873 | −0.003 |
|  50bp (023) | 150bp | 0.7784 | −0.012 |
|   0bp (020*)| n/a   | 0.7317 | −0.058 |
*020 has width-filter selection bias on top of no-flank loss.

The regulatory-unit boundary is not a step. Useful signal extends
to ~+/-50bp of midpoint, with steeply higher density inside the
inner ~25-50bp. T17 / T19 confirmed: random flank really IS just
receptive-field padding; the 0.058 of 020 was mostly width-filter bias.

**T21 (new — eval_08 likes random sequence):** Random-flank libraries
consistently outperform cCRE-only libraries on eval_08 by +0.05 to
+0.06, scaling with random-sequence content. eval_08 must test
broader-coverage / non-cCRE sequences. Optimal library mix depends
on whether we prioritize peak-only or coverage-broad evals.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight   0.7900  ← still best**
022 cCRE 013 random-flank     0.7873
012 cCRE rare-upweight        0.7819
015 cCRE bracket 11K/1.5K     0.7802
023 cCRE 013 50bp core        0.7784
019 cCRE 013 + DHS mix        0.7768
006 stratified cCRE           0.7754
011 cCRE 3-superclass         0.7715
016 cCRE 1/sqrt-pool          0.7694
007 cCRE strat + random       0.7672
002 cCRE uniform              0.7619
021 cCRE 013 off-center       0.7617
017 cCRE 013 + motif aug      0.7595
009 DHS filtered              0.7500
010 cCRE TF-strat             0.7493
018 DHS rare-component up     0.7331
001 random uniform            0.7321
020 cCRE 013 no-flank         0.7317
008 DHS uniform               0.7297
014 cCRE rare-only            0.7155
005 random genomic            0.7016
004 motifs in random          0.6824
003 dinuc-shuf cCRE           0.6595

## 2026-04-28 — Plan: experiment 024 (013 cCRE + 20% uniform random mix)

**Type:** investigating (T21 says random sequence is asymmetrically
useful — it specifically helps eval_08 a lot; we should mix and check
for free wins).

**Design:** 40K from the 013 recipe (8K each rare + 2K each abundant)
+ 10K uniform random hg38 main-chrom 200bp windows (>=10kb from any
cCRE — same source as 022/023 flank pool). Single concatenated 50K
library, shuffled. ALL cCREs eligible (no width filter).

**Hypothesis:** the eval_08 boost from random sequence is mostly
free if we keep enough cCRE bulk. Mixing 80% cCRE + 20% random should
preserve most of 013's per-eval performance while pulling eval_08 up.
A small loss on the cCRE-strong evals is expected from dilution.

**Pre-experiment branches:**
- 024 mean > 013's 0.7900 → mixing wins outright; explore the
  optimal cCRE/random ratio (e.g. 90/10, 70/30) in 025
- 024 mean ≈ 013, eval_08 strongly up → tradeoff confirmed; need
  to weigh which evals matter for the final library
- 024 mean < 013, eval_08 only marginally up → diluting cCRE costs
  more than coverage helps; abandon mix and try other axes

**Why this over more T20 gradient probing (e.g., 25bp cognate):**
T20 already gives a clean monotone gradient (200→100→50bp = -0.000
→ -0.003 → -0.012). Pushing to 25bp would polish theory but won't
improve the best library. T21's coverage-vs-peak tradeoff is the
first signal we've seen of a "free-axis" — different evals want
different sequence sources. Mix-libraries are the most action-relevant
follow-up.

## 2026-04-28 — Result: 024 cCRE 013 + 20% uniform random hg38 mix

**Headline:** eval_01 = **0.6894**, mean across 14 = **0.7235**.
**−0.067 vs 013 mean. Big negative. Every eval lost.**
eval_08 lost **−0.085** (vs +0.061 in 023!). T21 was wrong.

Per-eval delta vs 013:
01:−0.058 02:−0.064 03:−0.069 04:−0.051 05:−0.058 06:−0.064 07:−0.086
08:**−0.085** 09:−0.060 10:−0.074 11:−0.057 12:−0.060 13:−0.080 14:−0.064

Per-seed eval_01: 0.6885 / 0.6897 / 0.6900 (SD ≈ 0.0008 — bizarre,
much tighter than 013/022/023 which had SD ≈ 0.012-0.018).

**T21 (REVISED):** The eval_08 boost from 022 (+0.049) and 023
(+0.061) is NOT because the library contains random sequence — it
is because the chimeric DESIGN (cCRE peak embedded in random
context) trains the model on "regulatory signal in inactive flank".
Standalone random sequences provide the wrong signal.

**T22 (new — label-divergent mixing under-fits):** 100% cCRE → 0.7900,
100% random hg38 → 0.7016. Linear interpolation says 80/20 mix should
be 0.7723. Actual 0.7235, **−0.049 below interpolation**. The model
under-fits when it's asked to regress two sources with very different
activity-label distributions (high-activity cCREs vs near-zero random).
Tight per-seed agreement is the tell — model collapses to a similar
bland solution every time.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight   0.7900  ← still best**
022 cCRE 013 random-flank     0.7873  (eval_08 boost — alt best)
012 cCRE rare-upweight        0.7819
015 cCRE bracket 11K/1.5K     0.7802
023 cCRE 013 50bp core        0.7784
019 cCRE 013 + DHS mix        0.7768
006 stratified cCRE           0.7754
011 cCRE 3-superclass         0.7715
016 cCRE 1/sqrt-pool          0.7694
007 cCRE strat + random       0.7672
002 cCRE uniform              0.7619
021 cCRE 013 off-center       0.7617
017 cCRE 013 + motif aug      0.7595
009 DHS filtered              0.7500
010 cCRE TF-strat             0.7493
018 DHS rare-component up     0.7331
001 random uniform            0.7321
020 cCRE 013 no-flank         0.7317
008 DHS uniform               0.7297
024 cCRE 013 + random mix     0.7235  ← worse than no-flank
014 cCRE rare-only            0.7155
005 random genomic            0.7016
004 motifs in random          0.6824
003 dinuc-shuf cCRE           0.6595

## 2026-04-28 — Plan: experiment 025 (013 with reverse-complement augmentation)

**Type:** investigating (testing standard ML practice we've not yet tried).

**Design:** Use the 013 recipe (10K each rare + 2.5K each abundant)
but for each per-class sampling pass, take half the cCREs as forward
strand and half as reverse-complement of the same 200bp window.
Same per-class counts as 013, just half are RC. 50K total. ALL
cCREs eligible (no width filter).

**Hypothesis:** Standard genomic CNN training benefits modestly from
RC augmentation (+0.005-0.015 typical) by teaching the model that
TF motifs work on either strand. If prepare.py's _train doesn't
already do RC augmentation, this should give a free lift.

**Pre-experiment branches:**
- 025 mean > 013 (>0.7905) → RC helps; new best library; 026 should
  push the augmentation idea further (e.g., RC + position jitter)
- 025 mean ≈ 013 (within 0.003) → RC neutral (model is already
  strand-invariant from training); 026 should pivot to dual-library
  (mixing 013 with 022 chimeric for eval_08 boost without dilution)
- 025 mean < 013 (more than 0.005 worse) → RC actively hurts (rare
  but possible if effective library diversity halves); confirms 013
  is robust and 026 should explore other axes

**Why this over more cCRE-engineering:** We've extensively probed
class composition (012-018) and cCRE-region geometry (020-023);
nothing beats 013. RC augmentation is a known orthogonal lever from
ML practice, not yet tested. Cheap to try, easy to interpret.

## 2026-04-28 — Result: 025 cCRE 013 with reverse-complement augmentation

**Headline:** eval_01 = **0.7103**, mean across 14 = **0.7466**.
**−0.043 vs 013.** RC augmentation hurts.

Per-eval delta vs 013:
01:−0.037 02:−0.040 03:−0.043 04:−0.031 05:−0.038 06:−0.040 07:−0.059
08:−0.064 09:−0.037 10:−0.049 11:−0.037 12:−0.039 13:−0.053 14:−0.040

Uniformly negative ~−0.040. Per-seed eval_01: 0.7004/0.6899/0.7405
(SD ≈ 0.022).

**T23 (new — library-level RC augmentation hurts):** Three plausible
mechanisms (cannot distinguish without inspecting prepare.py, which
is a black box): (1) prepare.py training already RC-augments, so
adding library RC duplicates with possibly inconsistent class labels;
(2) the oracle/surrogate that generates training labels is strand-
sensitive (oracle(S) ≠ oracle(RC(S))); (3) cCRE class assignment is
strand-asymmetric, so RC sequences carry mis-labeled class context.
The model is at minimum NOT helped by RC augmentation here.

T17, T19, T20 unchanged — this is a pipeline-interaction result.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight   0.7900  ← still best**
022 cCRE 013 random-flank     0.7873  (eval_08 boost — alt best)
012 cCRE rare-upweight        0.7819
015 cCRE bracket 11K/1.5K     0.7802
023 cCRE 013 50bp core        0.7784
019 cCRE 013 + DHS mix        0.7768
006 stratified cCRE           0.7754
011 cCRE 3-superclass         0.7715
016 cCRE 1/sqrt-pool          0.7694
007 cCRE strat + random       0.7672
002 cCRE uniform              0.7619
021 cCRE 013 off-center       0.7617
017 cCRE 013 + motif aug      0.7595
009 DHS filtered              0.7500
010 cCRE TF-strat             0.7493
025 cCRE 013 RC aug           0.7466  ← RC hurts
018 DHS rare-component up     0.7331
001 random uniform            0.7321
020 cCRE 013 no-flank         0.7317
008 DHS uniform               0.7297
024 cCRE 013 + random mix     0.7235
014 cCRE rare-only            0.7155
005 random genomic            0.7016
004 motifs in random          0.6824
003 dinuc-shuf cCRE           0.6595

## 2026-04-28 — Plan: experiment 026 (013 + 022 chimeric dual-library)

**Type:** investigating (T22 says mixing label-divergent sources hurts;
test if mixing two cCRE-anchored designs is OK).

**Design:** 50K = 25K from 013 (full 200bp cCRE windows centered on
midpoint) + 25K from 022 (100bp cCRE + 50bp random hg38 flanks each
side). Both halves use the 013 class-composition recipe scaled to 25K
(5K each rare + 1.25K each abundant). All shuffled together. ALL
cCREs eligible (no width filter).

**Hypothesis:** 022's eval_08 boost (+0.049) comes from training on
"cCRE peak in random context" sequences. If we keep 25K of those AND
25K full-cCRE (013-style), the chimeric half should provide the
eval_08 lift while the cCRE-only half preserves the cCRE-strong evals.
T22's failure mode (label divergence) doesn't apply: both halves are
cCRE-anchored with similar activity distributions.

**Pre-experiment branches:**
- 026 mean > 0.7900 AND eval_08 > 0.73 → genuinely bridges; new alt-best
- 026 ≈ 022 (~0.787) → mix dominated by chimeric character; minor lift
- 026 < 013 mean by more than 0.005 → even cCRE-anchored mixing hurts;
  rules out all mix strategies; pivot to single-design refinements

## 2026-04-28 — Result: 026 cCRE 013 + 022 chimeric dual library

**Headline:** eval_01 = **0.7297**, mean across 14 = **0.7716**.
**−0.018 vs 013 mean. Mixing two cCRE-anchored designs also hurts.**
eval_08 only +0.004 — chimeric boost vanished when halved.

Per-eval delta vs 013:
01:−0.018 02:−0.019 03:−0.020 04:−0.014 05:−0.018 06:−0.019 07:−0.032
08:**+0.004** 09:−0.018 10:−0.020 11:−0.017 12:−0.019 13:−0.029 14:−0.019

Per-seed eval_01: 0.7467 / 0.7632 / 0.6793 (SD ≈ 0.044, very wide
— 2-3x normal variance, training instability tell).

**T24 (new — chimeric boost is whole-library, not additive):** 022's
+0.049 eval_08 boost and 023's +0.061 don't shrink linearly with
chimeric proportion. Halving the chimeric fraction → eval_08 boost
basically disappears (+0.004 here). The model needs uniform design
across the library to learn "regulatory peak in random scaffold".

**T22 generalized:** Mixing hurts ALSO when both halves are cCRE-
anchored (similar label distributions). The earlier label-divergence
explanation (T22 from 024) was incomplete — design heterogeneity
matters too. The model trains best on a homogeneous library design.

**Decision-relevant updates:**
- All mix strategies are off the table (024 and 026 both lose).
- 022 stays as the alt-best for eval_08-priority use cases.
- 013 stays as the universal best on mean-across-evals.

**Process note:** spark03 also broke (exit 255 ssh). Now both
spark03 and spark06 unreliable; only spark01 + local viable.
Re-ran seed 2 locally to recover the 3rd point.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight   0.7900  ← still best**
022 cCRE 013 random-flank     0.7873  (eval_08 boost — alt best)
012 cCRE rare-upweight        0.7819
015 cCRE bracket 11K/1.5K     0.7802
023 cCRE 013 50bp core        0.7784
019 cCRE 013 + DHS mix        0.7768
006 stratified cCRE           0.7754
011 cCRE 3-superclass         0.7715
026 cCRE 013 + 022 dual       0.7716
016 cCRE 1/sqrt-pool          0.7694
007 cCRE strat + random       0.7672
002 cCRE uniform              0.7619
021 cCRE 013 off-center       0.7617
017 cCRE 013 + motif aug      0.7595
009 DHS filtered              0.7500
010 cCRE TF-strat             0.7493
025 cCRE 013 RC aug           0.7466
018 DHS rare-component up     0.7331
001 random uniform            0.7321
020 cCRE 013 no-flank         0.7317
008 DHS uniform               0.7297
024 cCRE 013 + random mix     0.7235
014 cCRE rare-only            0.7155
005 random genomic            0.7016
004 motifs in random          0.6824
003 dinuc-shuf cCRE           0.6595

## 2026-04-28 — Plan: experiment 027 (013 with DHS-quality cCRE filter)

**Type:** investigating (untried angle: filter cCREs to those that
overlap a high-quality DHS, enriching for active regulatory units).

**Design:** Use 013 class composition (10K rare + 2.5K abundant =
50K). For each cCRE in the BED, check whether it overlaps any DHS
with mean_signal >= q75 AND numsamples >= 5 (same filter that
worked well in 009). Only sample from the filtered pool. If a class
loses too much pool size to fill its quota, fall back to unfiltered
for that class (with a printed warning so we can interpret).

Quality filter is the same one that gave 009 its lift over 008
(unfiltered DHS): q75 mean_signal + numsamples >= 5 selects DHSs
that are accessible across many cell types and have strong signal
— likely real regulatory elements with cross-cell-type activity.

**Hypothesis:** ENCODE cCRE class assignment relies on chromatin
state (DNase + H3K4me3 + CTCF) but doesn't gate on signal strength.
Many class-tagged cCREs may be weak/borderline calls. Filtering to
only DHS-supported cCREs should enrich for true active regulatory
elements and improve cross-cell-type generalization.

**Pre-experiment branches:**
- 027 > 013 → DHS-quality filter adds info beyond cCRE class label;
  new best library; 028 should explore stricter quality thresholds
- 027 ≈ 013 (within 0.003) → cCRE class label already captures
  activity sufficiently; DHS adds nothing; 028 pivots elsewhere
- 027 < 013 → filter too restrictive, loses class breadth/diversity;
  abandon DHS quality filter

## 2026-04-28 — Result: 027 cCRE 013 with DHS-quality filter

**Headline:** eval_01 = **0.7432**, mean across 14 = **0.7859**.
**−0.004 vs 013.** Filter is essentially neutral.

Per-eval delta vs 013:
01:−0.005 02:−0.005 03:−0.005 04:−0.003 05:−0.005 06:−0.004 07:−0.007
08:+0.000 09:−0.002 10:−0.002 11:−0.004 12:−0.004 13:−0.007 14:−0.004

Per-seed eval_01: 0.7523 / 0.7150 / 0.7623 (SD ≈ 0.025).

**Filter outcomes per class:**
- PLS, CA-CTCF, pELS, dELS, CA: filtered (sufficient pool)
- CA-TF: 6,108 < 10,000 → fallback unfiltered
- CA-H3K4me3: 9,696 < 10,000 → fallback unfiltered
- TF: 195 < 2,500 → fallback unfiltered (only 0.2% of TF cCREs
  overlap broad-active DHSs!)

**T25 (new — cCRE class label and DHS signal-quality are largely
redundant):** Filtering cCREs to those overlapping high-quality DHSs
adds no signal beyond what cCRE class assignment already provides.
The model can't extract a meaningful "DHS-supported PLS" subclass
from the data given the training pipeline's classifier head.

**T26 (incidental — cCRE classes have very different DHS overlap
rates):** Pure-TF cCREs almost never overlap broad-active DHSs
(0.2%). CA-TF and CA-H3K4me3 ~6-10%. PLS / CA-CTCF / pELS higher.
The cCRE class label correlates strongly with expected accessibility
breadth — confirming the redundancy in T25.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight   0.7900  ← still best**
022 cCRE 013 random-flank     0.7873  (eval_08 boost — alt best)
027 cCRE 013 DHS-quality       0.7859  (≈ 013, no marginal info)
012 cCRE rare-upweight        0.7819
015 cCRE bracket 11K/1.5K     0.7802
023 cCRE 013 50bp core        0.7784
019 cCRE 013 + DHS mix        0.7768
006 stratified cCRE           0.7754
011 cCRE 3-superclass         0.7715
026 cCRE 013 + 022 dual       0.7716
016 cCRE 1/sqrt-pool          0.7694
007 cCRE strat + random       0.7672
002 cCRE uniform              0.7619
021 cCRE 013 off-center       0.7617
017 cCRE 013 + motif aug      0.7595
009 DHS filtered              0.7500
010 cCRE TF-strat             0.7493
025 cCRE 013 RC aug           0.7466
018 DHS rare-component up     0.7331
001 random uniform            0.7321
020 cCRE 013 no-flank         0.7317
008 DHS uniform               0.7297
024 cCRE 013 + random mix     0.7235
014 cCRE rare-only            0.7155
005 random genomic            0.7016
004 motifs in random          0.6824
003 dinuc-shuf cCRE           0.6595

## 2026-04-28 — Plan: experiment 028 (013 with cCRE width-quartile stratification)

**Type:** investigating (last untested cCRE-engineering axis).

**Design:** Use 013 class composition (10K rare + 2.5K abundant).
Within each class, divide cCREs into 4 width quartiles (cCRE
end - start). Sample n_take/4 from each quartile uniformly. Forces
width-breadth within each class.

**Hypothesis:** cCRE width may carry information orthogonal to class
(narrow vs broad regulatory regions may have different functional
content). Forcing width-breadth within each class would expose the
model to both regimes.

**Counter-evidence from 020:** filtering to >=200bp-wide cCREs lost
0.058. T19 attributed this to width-filter SELECTION BIAS. But
sampling across ALL width quartiles (rather than filtering away
narrow) is fundamentally different — should not exhibit selection
bias.

**Pre-experiment branches:**
- 028 > 013 (>0.7905) → width is informative, stratifying helps;
  new best library
- 028 ≈ 013 (within 0.003) → width carries no marginal info; class
  alone is sufficient
- 028 < 013 by 0.005+ → forcing width breadth hurts (e.g., narrow
  cCREs are more informative and now get less weight than they
  would in class-uniform sampling)

## 2026-04-28 — Result: 028 cCRE 013 with width-quartile stratification

**Headline:** eval_01 = **0.7115**, mean across 14 = **0.7486**.
**−0.041 vs 013 mean.** Width-stratification HURTS.

Per-eval delta vs 013:
01:−0.036 02:−0.039 03:−0.042 04:−0.032 05:−0.036 06:−0.040 07:−0.054
08:−0.057 09:−0.035 10:−0.045 11:−0.036 12:−0.036 13:−0.053 14:−0.039

Per-seed eval_01: 0.6779 / 0.7315 / 0.7251 (SD ≈ 0.029).

**T27 (new — cCRE width carries information; narrow > broad
per-instance):** Natural per-class pool sampling (013) is biased
toward whatever width regime is most common, which turns out to
be approximately optimal. Forcing equal counts across width
quartiles HURTS because it lifts up broad cCREs at the expense of
narrow ones. Per-instance, narrow cCREs are sharper peaks with
more concentrated regulatory content and are more informative.

**Combined T19 + T27 picture:** Both extremes hurt — width-FILTERING
to remove narrow cCREs (020) AND forcing equal width breadth (028)
both lose ~0.04-0.06 vs natural sampling. Width is informative,
the natural class-pool distribution captures it, and 013's design
is at the sweet spot.

**T13 strengthened (3rd time):** cCRE midpoints carry concentrated
regulatory content; the more narrowly the cCRE was called, the
more concentrated and informative its centered window. Maps onto
T20's cognate-region gradient — the scale at which regulation
operates is well below 200bp.

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight   0.7900  ← still best**
022 cCRE 013 random-flank     0.7873  (eval_08 boost — alt best)
027 cCRE 013 DHS-quality       0.7859
012 cCRE rare-upweight        0.7819
015 cCRE bracket 11K/1.5K     0.7802
023 cCRE 013 50bp core        0.7784
019 cCRE 013 + DHS mix        0.7768
026 cCRE 013 + 022 dual       0.7716
006 stratified cCRE           0.7754
011 cCRE 3-superclass         0.7715
016 cCRE 1/sqrt-pool          0.7694
007 cCRE strat + random       0.7672
002 cCRE uniform              0.7619
021 cCRE 013 off-center       0.7617
017 cCRE 013 + motif aug      0.7595
009 DHS filtered              0.7500
028 cCRE 013 width-strat      0.7486  ← width strat hurts
010 cCRE TF-strat             0.7493
025 cCRE 013 RC aug           0.7466
018 DHS rare-component up     0.7331
001 random uniform            0.7321
020 cCRE 013 no-flank         0.7317
008 DHS uniform               0.7297
024 cCRE 013 + random mix     0.7235
014 cCRE rare-only            0.7155
005 random genomic            0.7016
004 motifs in random          0.6824
003 dinuc-shuf cCRE           0.6595

## 2026-04-28 — Plan: experiment 029 (022-style chimera with 160bp cognate + 20bp random flank each side)

**Type:** investigating (probe upper end of cognate-region gradient
T20; test if T24's "whole-library chimeric design" effect kicks in
even with very small flank).

**Design:** Same 013 class composition (10K rare + 2.5K abundant
= 50K). Each sequence is built as:
  [20bp random hg38 main-chrom flank]
  [160bp cognate cCRE region centered on cCRE midpoint]
  [20bp random hg38 main-chrom flank]
Random flanks from positions >=10kb from any cCRE (same scaffold
pool as 022/023). ALL cCREs eligible (no width filter).

**Hypothesis:** T20 gradient says smaller cognate = lower mean.
T24 says chimeric DESIGN (any random flank) gives the eval_08
boost. If T24's mechanism is whole-library design rather than
flank fraction, even 20bp flank should trigger it. If yes:
- Mean ≈ 0.79 (very close to 013 since 90% cognate)
- eval_08 > 0.73 (chimeric boost)
This would be the best-of-both library.

**Pre-experiment branches:**
- 029 mean >= 0.788 AND eval_08 > 0.73 → minimal-flank chimeric is
  best of both; new top library; very strong recommendation
- 029 mean ~0.79 AND eval_08 ~0.71 → 20bp flank too small to trigger
  the boost; gradient is smooth, not threshold
- 029 mean < 0.78 → cognate fraction effect is sharper than expected;
  even ~10% flank costs noticeable mean

**Why this over alternatives:** This is the only remaining
configuration that could plausibly beat both 013 (on mean) and 022
(by combining 013's mean with 022's eval_08 boost). All other
axes (mixing, RC, filtering, width-strat) have been ruled out.

## 2026-04-28 — Result: 029 cCRE 013 chimera 160bp cognate + 20bp flank

**Headline:** eval_01 = **0.6946**, mean across 14 = **0.7291**.
**−0.061 vs 013 mean. Surprise negative — every eval lost, eval_08
also lost (−0.069).** Falls below 013, 022, AND 023.

Per-eval delta vs 013:
01:−0.053 02:−0.058 03:−0.062 04:−0.045 05:−0.053 06:−0.058 07:−0.086
08:**−0.069** 09:−0.051 10:−0.069 11:−0.052 12:−0.054 13:−0.084 14:−0.058

Per-seed eval_01: 0.6986 / 0.6902 / 0.6951 (SD ≈ **0.004** — bizarre,
much tighter than typical ~0.012-0.018; same fingerprint as 024).
Training time: 527s vs typical 1200-2000s — fast convergence.

**T28 (new — cognate-flank ratio is non-monotone):** Updated table:

| cognate | flank | mean   | eval_08 | exp |
|---------|-------|--------|---------|-----|
| 200bp   |   0bp | 0.7900 | 0.7044  | 013 |
| 160bp   |  20bp | **0.7291** | 0.6357  | 029 |
| 100bp   |  50bp | 0.7873 | 0.7529  | 022 |
|  50bp   |  75bp | 0.7784 | 0.7649  | 023 |
|   0bp   | 100bp | 0.7321 | 0.7841  | 001 |

**029 sits BELOW its neighbors on every metric.** The function is
NOT monotone in flank fraction — there's a degenerate dip when the
flank is too small to be a real "scaffold" but big enough to disrupt
the cCRE boundary region. Combined with 024's catastrophe and tight
seed-SD, this suggests these chimeric configurations have a "broken"
regime where the model converges fast to a degenerate fit.

**T29 (consequence):** chimeric construction has a minimum-effective
flank-fraction. Below threshold (~10-15% per side?) the construction
is harmful, not neutral. T22's chimeric eval_08 boost (022, 023)
requires flanks of meaningful size relative to the cognate.

**T28b (mechanistic conjecture):** A 50/75bp random flank acts as a
"context-clearing scaffold" — model learns to ignore the flank and
focus on the central cognate region. A 20bp flank is too short to
read as scaffold, but long enough to disrupt the cCRE's natural
boundary (cCRE widths are ~150-300bp, so a 160bp window is approx
one cCRE width but the 20bp flank lands close to the cCRE edge in
many cases). This creates a weak/conflicting signal the model
overfits to (fast, uniform across seeds, generalizes badly).

Cumulative ranking (mean across 14 evals):
**013 cCRE extreme upweight   0.7900  ← still best**
022 cCRE 013 random-flank     0.7873  (eval_08 boost — alt best)
027 cCRE 013 DHS-quality       0.7859
012 cCRE rare-upweight        0.7819
015 cCRE bracket 11K/1.5K     0.7802
023 cCRE 013 50bp core        0.7784
019 cCRE 013 + DHS mix        0.7768
006 stratified cCRE           0.7754
026 cCRE 013 + 022 dual       0.7716
011 cCRE 3-superclass         0.7715
016 cCRE 1/sqrt-pool          0.7694
007 cCRE strat + random       0.7672
002 cCRE uniform              0.7619
021 cCRE 013 off-center       0.7617
017 cCRE 013 + motif aug      0.7595
009 DHS filtered              0.7500
028 cCRE 013 width-strat      0.7486
010 cCRE TF-strat             0.7493
025 cCRE 013 RC aug           0.7466
018 DHS rare-component up     0.7331
001 random uniform            0.7321
020 cCRE 013 no-flank         0.7317
008 DHS uniform               0.7297
**029 cCRE 013 160bp/20bp chim 0.7291  ← surprise negative**
024 cCRE 013 + random mix     0.7235
014 cCRE rare-only            0.7155
005 random genomic            0.7016
004 motifs in random          0.6824
003 dinuc-shuf cCRE           0.6595

## 2026-04-28 — Plan: experiment 030 (final — chimera 022 with narrow cCRE filter)

**Type:** synthesizing two best-supported insights into a single
candidate that could plausibly beat 022 on mean and approach 013.

**Design:** 022-style chimera (100bp cognate cCRE + 50bp random
hg38 flank each side, exactly like 022) BUT with cCREs filtered
to width <250bp ("narrow only"). Same 013 class composition (10K
rare + 2.5K abundant = 50K). Per-class fall-back to unfiltered if
the narrow pool is too small to fill the target.

**Why this design:** Combines two strong signals:
- T22/T24: chimeric design (100/50 flank) gives +0.049 on eval_08
  (whole-library effect, not additive — see 026 failure)
- T27: narrow cCREs (<250bp) are more informative per-instance —
  013's natural sampling is biased toward narrow and that's optimal
- T13: cCRE midpoints concentrate regulatory content; narrow cCREs
  have the most concentrated midpoints

If T22 and T27 act on independent axes (one improves cross-cell-type
signal use, the other improves per-instance information density),
combining them should be strictly additive: 022's mean (0.7873) +
T27's narrow-bias signal (~+0.005-0.015 hypothesis) → mean ~0.79+
with eval_08 still ~0.75.

**Why not other candidates:**
- 029's surprise negative kills "minimal-flank" chimera variants
- All other axes have been tested: mixing (024, 026), RC (025),
  DHS filtering (027 neutral), width strat (028 hurts),
  off-center (021 hurts), motif aug (017 hurts), no-flank (020 hurts),
  rare-only (014 hurts), DHS-rare upweight (018 hurts)
- The remaining unexplored cell is: chimeric x narrow cCREs

**Pre-experiment branches:**
- 030 mean ≥ 0.79 AND eval_08 ≥ 0.74 → narrow x chimera is the new
  top library; T22 and T27 act independently
- 030 mean ≈ 022 (0.787) AND eval_08 ≈ 022 (0.753) → narrow filter is
  redundant with chimeric design (chimera already uses cCRE midpoints
  effectively, narrow filter adds nothing)
- 030 mean < 022 by 0.005+ → chimeric design uses cCRE EDGE info
  that narrow cCREs don't carry; narrow x chimera hurts

This is the FINAL experiment of the 30-experiment loop.

## 2026-04-28 — Result: 030 cCRE 013 chimera with narrow cCRE filter (FINAL)

**Headline:** eval_01 = **0.6990**, mean across 14 = **0.7369**.
**−0.050 vs 022 mean. −0.053 vs 013. Anti-synergy confirmed.**
eval_08 also lost: 0.6901 (−0.063 vs 022).

Per-eval delta vs 022:
01:−0.046 02:−0.048 03:−0.050 04:−0.053 05:−0.046 06:−0.048 07:−0.053
08:**−0.063** 09:−0.060 10:−0.049 11:−0.045 12:−0.045 13:−0.055 14:−0.048

Per-seed eval_01: 0.7270 / 0.6983 / 0.6716 (SD ≈ 0.028 — normal,
NOT the degenerate fingerprint of 024/029). Time 817s — also normal.
Model trained healthily on less-informative data.

**T30 (new — narrow-extreme cCRE selection hurts even with chimera):**
Combining T22 (chimera eval_08 boost) with T27 (narrow more
informative per-instance) does NOT compose. Aggressive narrow
selection costs 0.05 even when chimera scaffolding is preserved.

**T27 (REVISED — width is a sweet spot, not monotone):** 028
showed forcing equal counts across width quartiles HURT (-0.041) —
I read this as "narrow > broad per-instance." But 030 now shows
that going to the narrow EXTREME also hurts (-0.050 vs 022). Both
width extremes hurt; the natural per-class width distribution that
013/022 capture is at a sweet spot. Narrow cCREs (~150-200bp) are
well-localized but may be weakly-called/atypical; broad cCREs
dilute signal; the natural mix is approximately optimal.

**T22 mechanism (refined by 030):** 022's chimera works by
REPLACING natural flank context with random scaffold while
preserving a 100bp cognate window — at natural cCRE width
(median ~250-320bp), 100bp samples the cCRE peak. With
forced-narrow cCREs (<200bp), the 100bp window may overshoot
the cCRE entirely. Narrow + chimera = leakage of the wrong kind.

**T31 (new — feature interactions in library design are common
and usually anti-synergistic):**
- 026: chimera + full-cCRE 50/50 mix → eval_08 boost vanished
- 030: chimera + narrow filter → mean lost 0.05 + eval_08 lost 0.063
- 024: cCRE + uniform random mix → catastrophic
Modifications to 013/022 that work alone do NOT compose. Library
design is a NON-additive optimization landscape.

---

## 2026-04-28 — Final summary (after 30 experiments)

**Best library:**
- **013 (cCRE extreme upweight)**: mean **0.7900** across 14 evals
  (best). 50K = 10K each rare class {PLS, CA-CTCF, CA-TF,
  CA-H3K4me3} + 2.5K each abundant {pELS, dELS, CA, TF}. 200bp
  centered on cCRE midpoint. No flanks, no aug, no filter.
- **022 (chimera variant)** alt-best for eval_08: mean 0.7873,
  eval_08 0.7529 (+0.049 vs 013's 0.7044). Trade 0.003 mean for
  +0.05 on eval_08. Same class composition, but 100bp cognate
  cCRE + 50bp random hg38 flank each side.

**Theory accumulated (T-numbers — collected):**
- **T1-T6 (early data-source comparisons):** cCRE > DHS > random;
  motif-only insertion is much worse than real cCRE; dinuc-shuffled
  cCRE strips most signal.
- **T7-T8 (composition):** rare cCRE classes (PLS, CA-CTCF, CA-TF,
  CA-H3K4me3) carry disproportionate generalization signal —
  inverse-frequency upweighting consistently helps.
- **T9-T11 (saturation of upweight):** monotone improvement up to
  013's extreme weighting (10K rare / 2.5K abundant). 014 (rare-only)
  loses badly — the abundant classes still contribute breadth.
- **T12 (super-class collapse):** rolling 8 classes into 3 (promoter
  / distal / insul-tf) loses 0.018 — class granularity matters.
- **T13:** cCRE midpoints concentrate regulatory content; centered
  windows are optimal.
- **T14 (DHS):** Meuleman DHS is a worse data source than cCRE for
  this task even with quality filters — likely because cell-type
  coverage of DHS doesn't match the eval's cell types.
- **T15-T16:** TF-stratified and 1/sqrt-pool per-class weightings
  underperform 013's piecewise rare/abundant weighting.
- **T17:** flanking ~50-100bp around the cCRE midpoint adds modest
  signal versus a pure 100bp cognate window — receptive-field padding
  matters at the model level even if the flank is genomically random.
- **T18:** motif augmentation (017) hurts — disturbs natural cCRE
  context.
- **T19:** width-FILTERING away narrow cCREs (020) hurts; narrow
  cCREs are informative.
- **T20:** cognate-region size gradient (200/100/50/0bp = 0.79/
  0.787/0.778/0.732). Mean degrades smoothly as cognate shrinks
  but stays high until ~50bp.
- **T21 (initial):** eval_08 likes random sequence
  - **T21 (REVISED):** the eval_08 boost is from CHIMERIC DESIGN,
    not random sequence per se. Pure random hurts; chimera helps.
- **T22 (chimera mechanism):** random flanks act as
  "context-clearing scaffold" — model focuses on cognate window
  and the loss flattens — this is what helps eval_08.
- **T23:** library-level RC augmentation (025) hurts ~0.043 —
  conflicts with strand-aware training/oracle.
- **T24:** chimera eval_08 boost is whole-library, not additive.
  Mixing 50% chimera + 50% full-cCRE (026) loses both gains.
- **T25:** cCRE class label and DHS quality are largely redundant
  info (027 essentially neutral).
- **T26 (incidental):** cCRE class type correlates with DHS overlap
  rate (TF cCREs only 0.2% overlap broad-active DHSs).
- **T27:** narrow cCREs are informative per-instance; forcing equal
  counts across width quartiles (028) hurts.
  - **T27 (REVISED by 030):** width has a SWEET SPOT — both width-
    stratification (028) AND narrow-extreme selection (030) hurt
    by ~0.04-0.05. The natural per-class width distribution
    captured by 013 is at the optimum.
- **T28:** cognate-flank ratio is NON-MONOTONE — 029 (160bp/20bp)
  fell catastrophically below both endpoints. The chimera regime
  has a "broken" region with too-small flank.
- **T29:** chimera needs a minimum-effective flank fraction; below
  the threshold the construction is harmful.
- **T30:** narrow-cCRE x chimera anti-synergy.
- **T31 (meta):** feature interactions in library design are
  usually anti-synergistic. Modifications to 013/022 that work
  alone usually do NOT compose. Library design is non-additive.

**Negative results that ruled out major axes:**
- Off-center extraction (021) — slightly hurts
- Width filtering / stratification / narrow-extreme (020, 028, 030)
- Random / DHS mixing (024, 018)
- Library-level RC augmentation (025)
- Motif augmentation (017)
- Chimera + full-cCRE mixing (026)
- DHS-quality cCRE filter (027 ≈ neutral)
- Smaller cognate regions (023, 029 — 023 is OK, 029 catastrophic)

**Most surprising findings:**
1. T21 inversion — random flank looked like the eval_08 source
   but is actually destructive when used standalone (024).
2. T28 — non-monotone cognate-flank tradeoff. 160/20 chimera lands
   below both endpoints with degenerate fast-converging seed agreement.
3. T31 — almost every "two good ideas combined" fails.

**Theoretical synthesis:** A cross-cell-type-generalizing MPRA
library wants:
- HIGH-INFORMATION samples (cCREs, esp. rare classes — T1-T11)
- CONCENTRATED per-instance signal (cCRE midpoints, natural width
  distribution — T13, T17, T20, T27 revised)
- INTACT NATURAL CONTEXT (no aug, no mixing, no filtering — T18,
  T22-T25, T31)
- STABLE SCAFFOLD (chimeric design adds to eval_08 by giving the
  model an "ignorable" context to push regulatory signal into
  the cognate window — T22, T24)

The optimal library lives at the unstable boundary between
"informative selection" and "natural distribution" — too aggressive
in either direction (more rare-only, less abundant, narrower,
broader, off-center, mixed sources) hurts.

**Final library recommendation: 013** for mean (0.7900), or
**022** if eval_08 is critical (mean 0.7873, eval_08 0.7529).
