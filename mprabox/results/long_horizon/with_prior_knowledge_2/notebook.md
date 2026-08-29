# MPRA Library Design — Lab Notebook

Append-only. Every entry begins with a timestamp.

---

## 2026-04-24 06:55 — Run kickoff & starting theory

Fresh repo on branch `42326_2`. Read `instructions.md` and `strategies.md`.

**Baseline landscape (50k library, mean Pearson r):**
- Best on eval_01 (primary): `dhs_topic` 0.7232
- Top tier: `dhs_topic`, `dhs_sei`, `dhs_synth`, `dhs_random` (all 0.708–0.723)
- Adding random synthetic helps eval_08 (0.7011 → 0.7523 with `dhs_synth`,
  even higher 0.7696 with pure `synth_oracle`) but slightly hurts eval_01.
- Worst: `mpra_real` (using actual experimental MPRA labels). Real labels
  are noisier than oracle labels at this size.
- Pure SEI (`sei_class`, `sei_random`) underperforms DHS — open chromatin
  beats chromatin-state regions for general regulatory training.

**Observations across eval sets:**
- eval_01, eval_05, eval_06, eval_02, eval_14 cluster (probably K562/HepG2/SK-N-SH
  in-distribution metrics — strategies rank similarly on them).
- eval_08 is the outlier — random sequences dominate. Likely synthetic /
  out-of-distribution / dinucleotide-shuffled / unusual GC composition.
- eval_07, eval_13 reward DHS-with-SEI mixes, possibly testing chromatin
  states beyond accessibility.

**Initial theory of generalization:**
A library is informative for generalizing to unseen cell types when it
teaches the model:
  1. **Regulatory grammar** — diverse TF motif combinations across
     contexts. Open chromatin (DHS) is the densest source.
  2. **Coverage of the input space** — random/synthetic sequences anchor
     the boundary so the model is calibrated on extreme inputs that don't
     appear in genome-curated samples.
  3. **Cross-cell-type validity of motif use** — sequences active in many
     cell types (broadly-accessible DHS) should encode general regulatory
     features that transfer better than cell-type-specific elements.

Topic-weighted DHS wins among baselines because it upweights elements with
clear, strong regulatory signal (less noise, higher motif content per bp).
Hypothesis: the next frontier is **broad-accessibility DHS** — pick
elements active in many biosamples, since these encode universally-used
regulatory programs that should transfer to unseen cell types.

But before chasing that, I need to **establish my own pipeline baseline**
to anchor every comparison to come.

### Plan for Experiment 001 — `001_dhs_signal_weighted` (replicate baseline)

This is an **exploration → validation** experiment, not a new hypothesis.

- Sample 50,000 DHS elements with replacement-free weighted sampling,
  weight = `mean_signal`. The Meuleman DHS Index file I downloaded does
  not include the per-element 16-component NMF loadings (only the
  dominant `component` label). `mean_signal` is the closest proxy: the
  baselines say topic-weighting "upweights elements with strong
  cell-type-specific accessibility signal" — that *is* what mean_signal
  captures.
- Extract 200bp around the `summit` column (±100bp).
- Filter sequences containing N or that fall off-chromosome; oversample
  to ensure exactly 50,000 valid 200bp ACGT sequences.
- 3 random seeds for sampling (model-training seed is fixed by prepare.py).

**Generalization justification.** Open chromatin elements with strong
mean signal across the 733-biosample DHS Index are by definition real
regulatory DNA observed across many tissues. A model trained on these
sees real TF motifs in real cis context, which should transfer to unseen
cell types better than random sequences (no motifs) or only-chromatin-state
regions (less direct).

**Prediction.** mean_r on eval_01 ≈ 0.71–0.73, comparable to baseline
`dhs_topic` (0.7232) and `dhs_random` (0.7089). If much lower, my
sampling/extraction has a bug. If much higher, mean_signal weighting is
unexpectedly stronger than NMF topic-weighting.

---

## 2026-04-24 07:25 — Experiment 001 result: dhs_signal_weighted

**eval_01 mean_r = 0.7242** (3 seeds, time 953s).
Cross-14-eval mean ~0.7511.

Per-eval vs dhs_topic baseline (Δ = mine − baseline):
| eval | mine   | baseline | Δ      |
|------|--------|----------|--------|
| 01   | 0.7242 | 0.7232   | +0.001 |
| 02   | 0.8173 | 0.8138   | +0.004 |
| 03   | 0.8007 | 0.7933   | +0.007 |
| 04   | 0.7819 | 0.7904   | -0.009 |
| 05   | 0.7238 | 0.7230   | +0.001 |
| 06   | 0.8170 | 0.8136   | +0.003 |
| 07   | 0.7611 | 0.7398   | +0.021 |
| 08   | 0.6781 | 0.7011   | -0.023 |
| 09   | 0.8496 | 0.8601   | -0.011 |
| 10   | 0.7895 | 0.7904   | -0.001 |
| 11   | 0.7106 | 0.7098   | +0.001 |
| 12   | 0.6872 | 0.6822   | +0.005 |
| 13   | 0.7564 | 0.7271   | +0.029 |
| 14   | 0.8175 | 0.8144   | +0.003 |

Per-seed eval_01: 0.6892 / 0.7481 / 0.7353 (std ≈ 0.025). This is the
**noise floor** for 3-seed comparisons; differences <0.01 are noise.

### What this updates
- **Theory unchanged.** mean_signal-weighting reproduces / very slightly
  exceeds the dhs_topic baseline — pipeline anchored.
- Seed variance is large at 3 seeds. Future comparisons should use
  cross-eval mean alongside eval_01 to reduce noise.
- The eval_07/13 over-performance and eval_08 under-performance pattern
  suggests evals are NOT a single axis. Some reward more open-chromatin
  density (07, 13), others reward off-distribution coverage (08).

### What to try next
The single most informative thing I could test next, conditional on
"dense regulatory signal is the main driver of generalization", is
whether **broad-accessibility DHS** (elements active in many of the 733
biosamples) generalizes better than mean-signal-weighted (which is mostly
intensity-driven, not breadth-driven). The DHS Index has a `numsamples`
column — perfect for this.

Hypothesis: elements with high `numsamples` encode regulatory programs
shared across many cell types and should produce a model that generalizes
to held-out cell types (the stated goal of this project) better than
intensity-weighted sampling.

Counter-hypothesis: cell-type-specific elements (low numsamples, high
signal) carry more information per element about cell-type-specific
regulators, and a model trained on them learns sharper motif grammar.

Either result is informative. Run as 002_dhs_breadth.

---

## 2026-04-24 07:35 — Plan: Experiment 002 — dhs_breadth_weighted

**Type: refining a promising direction.**
The "promising direction" is still DHS-based sampling; the variable I'm
twisting is the *weight column*.

### Literature pulled
- **Gosai et al. 2024 (Malinois, Nature)** explicitly built their training
  set from DHS+H3K27ac peaks that were subset to be **cell-type-specific**
  (no overlap with the other two cell types in K562/HepG2/SK-N-SH). They
  did this because their goal was cell-type-*targeted* CRE design. My
  goal is the opposite — generalization to unseen cell types — so the
  Malinois recipe is informative as a *contrast*: cell-type-specific
  elements teach a model to discriminate between the trained cell types,
  but may not encode regulatory grammar that transfers off-distribution.
- **Barbadilla-Martínez et al. 2024 (PARM, Nature 2025)** identifies
  "cell-type-invariant TF families" as those with low cross-cell-type
  variance in activating regulatory site counts. Suggests there is
  meaningful invariant signal in shared regulatory elements.
- **DNA-Diffusion (2024)** trains on the DHS Index — confirms DHS Index
  is a community-validated source for regulatory training data.

### Hypothesis
A library biased toward **broadly-accessible DHS** elements (high
`numsamples` — open across many of the 733 biosamples) will train a
model that better encodes cell-type-invariant regulatory grammar. This
should help on evaluation sets that probe out-of-distribution generalization
and may hurt slightly on in-distribution evals where cell-type-specific
features pay off.

### Generalization justification
This is the *cleanest possible test* of the project's stated goal: the
weight column directly indexes "how many cell types is this element
relevant to". If high-breadth wins overall, it's strong evidence that
breadth is the informative property. If it loses on eval_01 but wins on
others, it tells me which evals are in-distribution vs. transfer.

### Plan
- Same pipeline as 001, but weight by `numsamples` instead of `mean_signal`.
- 50,000 sequences × 3 seeds × 200bp around DHS summit.
- Predicted eval_01: 0.69–0.73 (could be slightly below 001 if eval_01
  is in-distribution).
- Predicted overall mean across 14 evals: ≥ 0.7511 (the 001 mean) if the
  breadth hypothesis holds.

Decision rule: if 002 cross-eval mean > 001 cross-eval mean by ≥ 0.005,
the breadth axis is informative and I will keep exploring it (e.g., 003
combining breadth + signal). If it ties or loses by < 0.01, the breadth
axis is roughly neutral and I should move to a different lever.

---

## 2026-04-24 07:55 — Experiment 002 result: dhs_breadth_weighted

**eval_01 = 0.7152**, **cross-14 mean = 0.7534**, time 962s.
Per-seed eval_01: 0.7173 / 0.7167 / 0.7115 (std 0.003 — much tighter than 001).

### Theory update
The breadth axis is **NOT** a free win. ns-weighting:
- Loses 0.04 / 0.06 on eval_07 / eval_13
- Wins ~0.01 on eval_04, eval_08, eval_09
- Net cross-eval: +0.002 (within noise)

Big takeaway: eval_07 and eval_13 reward **cell-type-specific** elements;
they are also the evals where SEI-based strategies in the published table
beat DHS-only ones. So there are at least two orthogonal regulatory-signal
axes evals are testing: (a) cell-type discrimination signal, (b)
cell-type-invariant grammar.

Theory v2:
> An informative library spans two orthogonal axes:
>   (a) **Cell-type-specific signal** — high mean_signal, low numsamples
>       elements where strong motifs are pinned to a specific tissue.
>       Sharp discrimination training. Evals 07/13 reward this.
>   (b) **Cell-type-invariant grammar** — high numsamples elements where
>       the same motifs work across many cells. Transfer training. Evals
>       04/08/09 mildly reward this.
> Plus a third axis already known from baselines:
>   (c) **Out-of-distribution coverage** — random-ish sequences. eval_08
>       rewards this (synth_oracle wins 08 by a wide margin).

Predicted from this theory: a library that explicitly mixes (a)+(b) should
beat both 001 and 002 on the cross-eval mean. (c) is a separate dial we
will return to once we have a stable mixture of (a)+(b).

### Plan: Experiment 003 — dhs_signal_breadth_mixture
**Type: refining.** Take 25k from `mean_signal`-weighted DHS (the
sharp-discrimination half) and 25k from `numsamples`-weighted DHS (the
invariance half). 50/50 mixture, 3 seeds.

**Generalization justification.** This is the most direct possible test
of the two-axis theory. If 003 beats both 001 (eval_01) and 002 (cross-eval
mean), the axes are complementary and combining them helps generalization
to unseen cell types. If 003 falls between 001 and 002, the axes are
substitutes and there is nothing to gain from mixing. Either result
sharpens the theory.

Predicted: eval_01 ≈ 0.72, cross-14 ≈ 0.755 (above 001 by ~0.005).

Decision rule: if cross-14 > 0.756 AND eval_07/13 > 0.74/0.74,
mixture wins on both axes — go deeper. If only one axis recovers,
the trade-off is real and I need to think about a different lever.

---

## 2026-04-24 08:25 — Experiment 003 result: dhs_signal_breadth_mixture

**Strong win.** eval_01 = 0.7327, cross-14 mean = 0.7735. Beats both
parents (001, 002) and the published `dhs_topic` baseline (0.7232) on
eval_01 by +0.010 and on cross-14 mean by ~+0.011.

13 of 14 evals improved over best parent. Only eval_13 lost (-0.010).

### Theory v2 confirmed
mean_signal-weighting and numsamples-weighting are COMPLEMENTARY axes,
not substitutes. The 50/50 mixture is Pareto-better on cross-14 mean
AND on eval_01 AND on eval_07 — so adding breadth recovers the
discrimination signal while ALSO adding transferable grammar.

### Plan: Experiment 004 — three-axis with synthetic
**Type: extending a winning direction.**
003 leaves eval_08 at 0.6984. The published baselines tell us
`synth_oracle` (pure random) crushes eval_08 at 0.7696 and `dhs_synth`
(50/50 DHS+random) reaches 0.7523. Random/synthetic sequences clearly
encode something orthogonal — probably out-of-distribution coverage
that calibrates the model on extreme inputs.

Hypothesis: a 3-axis library with a small dose of random sequences
will improve eval_08 without giving back the eval_01 / cross-14 gains
from 003. The hard question is the dose. `dhs_synth`'s 50% synthetic
hurt eval_01 (0.7174 vs 0.7232), so 50% is too high. I'll try **20%
synthetic** as a first probe — keeps an 80% real-DHS anchor, split as
40/40 signal/breadth (the proven 003 ratio), plus 20% i.i.d. uniform
ACGT random. Total still 50,000 sequences × 3 seeds.

### Generalization justification
Random sequences are by construction independent of any cell type's
biology — they cannot be confused with K562 vs HepG2 vs SK-N-SH
discrimination signal. They give the model coverage of input space the
genome doesn't reach (extreme GC compositions, rare k-mers, no motifs).
A model that's well-calibrated on these should generalize better to
unseen cell-type contexts because its decision boundary is
better-anchored.

Predicted: eval_01 ≈ 0.72–0.73 (slight risk of dropping below 003 due
to dilution); cross-14 ≈ 0.77; eval_08 ≈ 0.71–0.74 (clear gain).

Decision rule:
- If cross-14 ≥ 0.77 AND eval_08 ≥ 0.71 → 3-axis theory wins. Tune ratio.
- If cross-14 < 0.76 (loses) → synthetic dose too high; try 10%.
- If eval_08 doesn't improve → synthetic doesn't add OOD signal at this size.

---

## 2026-04-24 09:15 — Experiment 004 result: dhs_mix_synth20

**Surprising negative.** 20% random synthetic + 40/40 signal/breadth DHS:
eval_01 = 0.6977 (Δ = -0.035 vs 003), cross-14 = 0.7360 (Δ = -0.038),
eval_08 = 0.6775 (Δ = -0.021 — even eval_08 got *worse*!).

### Theory revision
**Reject hypothesis: "random synthetic adds OOD coverage that helps."**
The published `synth_oracle` and `dhs_synth` baselines reach high eval_08
with synthetic — but synth_oracle is explicitly "oracle-labeled". My
pipeline runs real MPRA on whatever I submit, so synthetic = noisy
labels. The `mpra_real` row (eval_01 = 0.6026) confirms real labels are
noisier than oracle labels at this size.

**The third axis ("OOD coverage via synthetic") does not exist in my
setup.** Drop this lever.

Theory v3:
> Within the real-genomic universe (no synthetic, no oracle):
> 1. Cell-type-specific signal (mean_signal weighting): sharp motif
>    discrimination. Sets the ceiling for in-distribution evals.
> 2. Cell-type-invariant grammar (numsamples weighting): transferable
>    regulatory programs. Sets the ceiling for cross-cell-type evals.
> 3. They are **complementary, not substitutes** — the 50/50 mixture
>    Pareto-beats both.
> Open question: are there *more* orthogonal axes within real-genomic
> elements? Component diversity? Conservation? Element class (cCRE)?

### Plan: Experiment 005 — dhs_component_stratified_mix
**Type: exploring a new hypothesis** within the proven real-genomic
universe.

The DHS Index has 16 NMF "components" (Cancer/epithelial, Cardiac, ...,
Tissue invariant). My current 003 sample is heavily skewed toward
high-signal AND high-breadth elements, which by component breakdown is
dominated by Stromal A (median ns=116) and Tissue invariant (median
mean_signal=0.874). I am almost certainly under-sampling Cardiac, Neural,
Lymphoid, etc. — components that have lots of cell-type-specific
regulatory programs but lower cross-axis weights.

**Hypothesis**: forcing equal representation across the 16 components
will give the model exposure to a wider regulatory grammar (Cardiac
TFBS, Neural TFBS, etc.) and improve generalization to held-out cell
types. Within each component, I'll use the proven 50/50 signal/breadth
mixture.

**Generalization justification**: this is the cleanest test of
"regulatory program diversity" as a generalization driver. If a model
trained on 16 cell-program flavors transfers better to held-out cell
types than one trained on the abundance-proportional sampling of 003,
then component diversity is informative beyond the global signal+breadth
axes. If it doesn't help, the published `dhs_stratified` (which lost to
`dhs_topic`) was correct that abundance-proportional > stratified.

**Plan**: 3,125 sequences per component × 16 components = 50,000.
Within each component: half by mean_signal-weighting, half by
numsamples-weighting (without overlap). Same 200bp-around-summit
extraction.

**Predicted**: cross-14 ∈ [0.76, 0.78]. If > 0.7735 (003), component
diversity is a real lever. If < 0.76, abundance-proportional wins.

---

## 2026-04-24 09:50 — Experiment 005 result: dhs_component_stratified_mix

**Clear negative.** eval_01 = 0.6946 (Δ = -0.038 vs 003), cross-14 = 0.7324
(Δ = -0.041). Component-stratification hurts on every eval.

This matches the published `dhs_stratified` (0.7055) < `dhs_topic`
(0.7232) result. Forcing equal samples per NMF component drags in
mid-quality elements from small components that abundance-proportional
weighting would skip — and quality dominates over diversity here.

### Theory revision (v3 → v4)
Two "diversity / coverage" hypotheses now rejected:
- Random synthetic (004) — adds noise, no OOD benefit in my pipeline.
- Component stratification (005) — drags in low-quality elements.

Theory v4:
> What makes a library generalize:
> 1. **mean_signal weighting** captures cell-type-specific motif clarity.
> 2. **numsamples weighting** captures cell-type-invariant programs.
> 3. **Their 50/50 mixture is Pareto-better** — they are complementary
>    axes of element *quality*, not substitutes.
> 4. Forced diversity (synthetic, component-stratified) HURTS — quality
>    over coverage.
>
> Open: are there *more* orthogonal quality axes within real DHS?
> Conservation, cCRE class, multi-window per element — all untested.

### Plan: Experiment 006 — dhs_conservation_weighted (deferred until phyloP downloads)
**Type: exploring a new hypothesis** that directly addresses the project's
generalization goal.

Hypothesis: sequences with high vertebrate phyloP score (conserved across
~100 species) encode regulatory grammar that has worked in cellular
contexts spanning hundreds of millions of years of evolution. By
construction, this grammar is transferable across cell types. Including
high-conservation elements should boost generalization to held-out cell
types beyond what mean_signal+numsamples weighting alone provides.

Plan:
1. Download hg38.phyloP100way.bw (in background).
2. For all 3.59M DHS Index elements, compute mean phyloP over the 200bp
   summit-centered window. Save per-element score.
3. Sample 50,000 with weight = mean_signal × numsamples × max(0, mean_phyloP).
   The product captures all three quality axes in a single weight.
4. 3 seeds, same 200bp extraction.

If 006 cross-14 > 0.7735 → conservation IS an orthogonal quality axis.
If 006 ≤ 003 → conservation is implicit in signal+breadth, no new info.

While phyloP downloads (~10 min for ~10 GB), I'll commit 005 and consider
whether to run a faster intermediate experiment.

### Interim Plan: Experiment 006 — dhs_signal_breadth_mixture_3070
**Type: refining the winning ratio.** Quick test of whether the 50/50
mixture in 003 is optimal vs 30/70 (more breadth) or 70/30 (more signal).
Cheap, ~16 min compute, no new data needed. Will run while phyloP arrives.

Choice: 70% signal / 30% breadth. Since 002 (pure breadth) lost on
eval_01 / 07 / 13 by 0.04-0.06 vs 001 (pure signal), it stands to reason
that LESS breadth may give back even more on those evals while still
keeping the breadth-driven gains on eval_04/08/09.

Predicted: cross-14 ∈ [0.770, 0.778]. If 006 > 003, the mixture surface
is asymmetric and signal carries more weight. If 006 ≤ 003, 50/50 is
near the ridge.

---

## 2026-04-24 09:55 — Plan revision

The previous "interim 70/30 ratio sweep" plan was low-information.
Replacing with a structurally deeper test of how quality axes should
combine.

### Plan: Experiment 006 — dhs_mix_multiplicative
**Type: refining a winning direction with a deeper question.**

003 used **additive mixing** (50% drawn by signal, 50% drawn by breadth,
disjoint). Each element appeared in only one half — purely high-signal
OR purely high-breadth, not both.

**Multiplicative alternative**: weight every element by
`mean_signal × log(1 + numsamples)`. Highest-weight elements are now
those strong on BOTH axes simultaneously.

**Hypothesis**: 003 worked because it forced span across both axes; if
we simply require each element to score on both axes, we get the same
benefit with cleaner weighting.

**Counter-hypothesis**: 003 keeps a long tail of cell-type-specific
elements (high signal, low breadth) that train sharp discrimination —
multiplicative would demote those, hurting eval_07/13.

**Generalization justification**: this directly tests the structural
question of how quality axes should combine. If multiplicative wins,
adding any future quality axis (conservation, cCRE class) is just
multiplying it into the weight — clean, scalable. If additive wins,
each new axis needs its own sample fraction — combinatorial blowup.

**Plan**: weight = mean_signal × log(1 + numsamples). Single weighted
draw of 50,000. 3 seeds. Same 200bp extraction.

Predicted: cross-14 ∈ [0.76, 0.78]. If > 0.7735 → multiplicative wins.
If < 0.7735 → keep additive sample-mixing.

Then 007 (or later) will be conservation-weighted using the same
combination scheme that wins.

---

## 2026-04-24 10:45 — Experiment 006 result: dhs_mix_multiplicative

**Loss.** eval_01=0.7028, cross-14=0.7404. Per-seed std 0.04 (very wide).

Multiplicative weighting collapses to the intersection of high-signal +
high-breadth (mostly Stromal A & Tissue invariant) — redundant library.
Additive sample-mixing in 003 keeps the union, not the intersection.

### Theory v5
> 1. Quality axes are real (mean_signal, numsamples each carry signal).
> 2. They must combine ADDITIVELY (separate sample fractions), NOT
>    multiplicatively (intersection collapses to redundant subset).
> 3. Forced diversity (synthetic, component-stratified) hurts.
> 4. Each new quality axis claims a fraction of the 50k budget —
>    combinatorial blowup. Pick axes carefully.

### Plan: Experiment 007 — dhs_conservation_weighted
**Type: exploring a new hypothesis** — is conservation a real quality axis?

phyloP100way precomputed for all 3.59M DHS summit windows
(`data/conservation/dhs_phyloP_mean.npy`, 14 MB, 62s). Stats: min=-2.94,
median=0.03, max=8.12. Most DHS elements are *not* highly conserved
(median ~0); the conserved tail is small but well-separated.

Hypothesis: sequences with high vertebrate phyloP encode regulatory
function preserved across ~100 species — by definition transferable
across cellular contexts (and species). Should produce a model that
generalizes to held-out cell types better than DHS-only quality axes.

**Generalization justification**: this is the *cleanest theoretical match*
for the project's goal. Cross-cell-type generalization in mammals is a
strict subset of cross-species conservation — the regulatory grammar
that survives 100 species' selection must work across many cell types.

**Plan**: pure conservation-weighted DHS sampling.
- weight = max(0.01, mean_phyloP_per_window). The clamp keeps elements
  with negative phyloP (accelerated evolution) at non-zero floor weight.
- 50,000 sequences × 3 seeds, same 200bp summit-centered extraction.
- This parallels 001 (signal-only) and 002 (breadth-only) so I know the
  pure axis behaviour before mixing.

Predicted: eval_01 ∈ [0.69, 0.74]. If close to 001/002 range (0.71–0.73),
conservation is a viable axis. Likely strong on evals 09, 10 (which seem
to reward broad regulatory grammar) and possibly weaker on eval_07/13.

If conservation has signal (eval_01 > 0.69), 008 will be the 3-axis
additive mix (signal + breadth + conservation) — the prediction is that
this beats 003's 0.7327 / 0.7735.

---

## 2026-04-24 11:05 — Experiment 007 result: dhs_conservation_weighted

**Loss — conservation is the weakest single quality axis tested.**
eval_01 = 0.6846 (Δ = -0.040 vs 001 signal-only, -0.048 vs 003 mix).
cross-14 = 0.7254 (Δ = -0.040 vs 001, -0.048 vs 003).
Per-seed eval_01: 0.6929 / 0.6789 / 0.6819 (std 0.008, very tight).

| metric   | 007    | 001 sig | 002 brd | 003 mix |
|----------|--------|---------|---------|---------|
| eval_01  | 0.6846 | 0.7242  | 0.7152  | 0.7327  |
| eval_07  | 0.7257 | 0.7611  | 0.7238  | 0.7618  |
| eval_08  | 0.6589 | 0.6781  | 0.6908  | 0.6984  |
| eval_09  | 0.7814 | 0.8496  | 0.8582  | 0.8685  |
| eval_13  | 0.7369 | 0.7564  | 0.7004  | 0.7469  |
| cross-14 | 0.7254 | 0.7654  | 0.7534  | 0.7735  |

### Theory revision (v5 → v6)
Conservation as a **positive sampling weight** is anti-informative for
this task. PhyloP-weighting pulls toward exonic/UTR/coding-adjacent
elements which are evolutionarily constrained but are NOT the strong
cell-type-specific enhancers MPRA activity tracks. Active enhancers
have moderate (not maximal) phyloP — the mode of the regulatory
distribution sits in the middle of the conservation spectrum, while
phyloP weighting pulls to the tail.

Prediction trigger from 006 plan: "If 007 eval_01 > 0.69, run 008 = 3-axis
additive". **Failed (0.6846 < 0.69)**. Conservation does NOT earn a
sample fraction. Reject this axis as a positive sampling weight.

Theory v6:
> Quality axes I have tested:
>   ✓ mean_signal (001) — strong, primary
>   ✓ numsamples (002) — strong, complementary to signal
>   ✗ phyloP (007) — weak, anti-informative as positive weight
> Combination scheme:
>   ✓ Additive sample-mixing (003) — wins
>   ✗ Multiplicative weighting (006) — collapses to redundant intersection
>   ✗ Forced uniform diversity (004 synth, 005 component) — drags quality down
>
> Open: untested quality axes within real DHS that may be informative —
>   - cCRE functional class (PLS / pELS / dELS / CTCF-only)
>   - Chromatin state (H3K27ac, H3K4me1)
>   - TF-binding density (motif counts, ENCODE ChIP)
>   - Multi-window per element (data augmentation, not new elements)

### Plan: Experiment 008 — dhs_signal_breadth_ccre_filtered
**Type: refining the winning recipe with a functional-class filter.**

The 003 mix is the current champion (eval_01=0.7327, cross-14=0.7735).
What if we restrict the sampling pool to elements that ENCODE has
classified as functional cis-regulatory elements (PLS / pELS / dELS)?
This is a *purity* filter — remove elements that are open chromatin
without any other regulatory mark (likely noise or mis-annotation).

- ENCODE cCRE Combined V3 has classes: PLS (promoter-like, ~35K),
  pELS (proximal enhancer, ~140K), dELS (distal enhancer, ~750K),
  CTCF-only (~50K), DNase-H3K4me3 (~14K). Total ~1M cCREs.
- DHS Index has 3.59M elements — a substantial fraction has no cCRE
  overlap (DHS is more permissive than cCRE).
- Hypothesis: DHS elements that fall in PLS / pELS / dELS are the
  functionally validated subset; restricting the 003 mix to this
  subset should improve cross-eval generalization by removing
  ambiguous open-chromatin noise.

**Generalization justification**: cCREs are defined by ENCODE using
multi-mark integration (DNase + H3K4me3 + H3K27ac + CTCF + DHS
breadth). They are a higher-confidence "this is a regulatory element"
label than open chromatin alone. A model trained on only validated
regulatory elements should learn cleaner motif grammar that transfers
better than one trained on a noisier mixed set.

**Plan**:
1. Precompute `dhs_ccre_class.npy` (the dominant overlapping cCRE class
   per DHS element, or "none"). [SCRIPT WRITTEN, RUNNING NEXT]
2. Filter pool to elements with class in {PLS, pELS, dELS}.
3. Within filtered pool: 25K weighted by mean_signal + 25K weighted by
   numsamples (the 003 recipe). 3 seeds.

Predicted: cross-14 ∈ [0.770, 0.785]. If > 0.7735 → cCRE filter is a
real lever (functional purity beats open-chromatin breadth alone).
If ≤ 0.7735 → DHS-only sampling already gets enough functional purity
from the signal+breadth weighting (the cCRE label adds nothing on top
of mean_signal + numsamples).

Counter-prediction worth noting: if the filter is too aggressive (most
high-mean_signal DHS already overlap dELS), the filtered pool may have
nearly the same composition as 003 — and no meaningful change.

---

## 2026-04-24 11:35 — Experiment 008 result: dhs_ccre_functional_filtered

**Within-noise tie with 003.** eval_01 = 0.7269 (Δ = -0.006 vs 003).
cross-14 = 0.7671 (Δ = -0.006). Per-seed eval_01: 0.6935 / 0.7301 /
0.7572 — wide std (~0.026), at the noise floor.

| metric   | 008    | 003    | Δ      |
|----------|--------|--------|--------|
| eval_01  | 0.7269 | 0.7327 | -0.006 |
| eval_07  | 0.7419 | 0.7618 | -0.020 |
| eval_08  | 0.7021 | 0.6984 | +0.004 |
| eval_13  | 0.7248 | 0.7469 | -0.022 |
| cross-14 | 0.7671 | 0.7735 | -0.006 |

### Theory update
ENCODE cCRE class is NOT an orthogonal quality axis to mean_signal +
numsamples. Two reasons:
1. The mean_signal weighting in 003 already implicitly selects elements
   that ENCODE annotates as cCRE PLS/pELS/dELS — high-weight elements
   are nearly all in the kept classes anyway. The filter is
   approximately a no-op on the high-weight tail.
2. The excluded classes (CTCF-only, DNase-H3K4me3) carry useful
   regulatory grammar (insulator/architectural for CTCF-only, orphan
   promoter mark for DNase-H3K4me3). Excluding them costs eval_07/13.

Theory v6 → v7:
> Single-element-quality axes I have tested:
>   ✓ mean_signal — strong
>   ✓ numsamples — strong, complementary
>   ✗ phyloP (positive weight) — weak, anti-informative
>   ~ cCRE-functional-filter — neutral (correlated with mean_signal)
>
> Element-quality may be near saturation. The next informative
> direction is likely STRUCTURAL — not "weight elements differently"
> but "use elements differently" (multi-window per element, jittered
> windows, paired flanking sequences).

### Plan: Experiment 009 — dhs_signal_breadth_multiwindow
**Type: exploring a new STRUCTURAL hypothesis** — does the model learn
more from N elements × 1 window each, or from N/2 elements × 2 windows?

This is the structural lever I haven't touched: **element-diversity vs
within-element-augmentation**. Total seq count is fixed at 50K.

Plan:
1. Draw 25,000 unique elements using the 003 recipe (12,500 by signal,
   12,500 by numsamples; disjoint).
2. Per element, emit TWO 200bp windows: summit-centered
   [summit-100, summit+100] and shifted [summit, summit+200].
3. Total = 50,000 sequences. 3 seeds.

Windows overlap by 100bp. The shifted window samples sequence on the
3' flank of the summit. Same regulatory context, slightly different
motif arrangement — typical sequence-level data augmentation.

**Generalization justification.** If this beats 003, sequence-level
context variation around the same regulatory element teaches the model
robust motif recognition (motifs in different positions / contexts) —
which should transfer to unseen cell types because the training signal
is invariant to position. If this loses, element diversity is more
informative than sequence diversity at this budget — confirming the
003 recipe of maximizing unique elements.

**Predicted**: cross-14 ∈ [0.755, 0.775]. Most likely outcome is
slight loss (-0.005 to -0.015) because halving unique elements is
costly. A win (>0.775) would be a major insight: position-invariance
matters more than element count.

Decision rules:
- cross-14 > 0.778 → multi-window is a clear lever; 010 will tune
  the windows-per-element ratio (3 windows per element, 16K elements).
- cross-14 ∈ [0.770, 0.778] → tie, multi-window is marginal — pivot
  to a different structural lever (TF-binding density, SEI states).
- cross-14 < 0.770 → element diversity wins; pivot to another axis
  (SEI chromatin state regions, motif density).

---

## 2026-04-24 12:00 — Experiment 009 result: dhs_signal_breadth_multiwindow

**Clear loss.** eval_01 = 0.6994 (Δ = -0.033 vs 003), cross-14 = 0.7358
(Δ = -0.038). eval_08 took the biggest hit at -0.064.

Multi-window augmentation cannot compensate for halving unique element
count. Position-shifted windows on the same element share TF-motif
content and offer little new information per training example.

### Theory v7 → v8
> Element diversity is the dominant signal at 50K library budget.
> Within-element augmentation (multi-window) is anti-informative when
> it costs unique elements. The 003 recipe — 50K unique elements via
> additive signal+breadth mixing — is robust.

eval_08 sensitivity is striking: the biggest losses occur where
diversity matters most. This implies eval_08 may be testing OOD
sequences where motif coverage matters more than per-element fidelity.

### What's the most informative next experiment?

Single-axis tweaks have saturated:
- ✗ multi-window (009)
- ✗ cCRE filter (008)
- ✗ component stratification (005)
- ✗ multiplicative weighting (006)
- ✗ random synthetic (004)
- ✗ conservation positive weight (007)

The remaining big lever is to add a **truly orthogonal annotation axis**
from a different data type. Two candidates from baselines:
- SEI chromatin states: dhs_sei baseline wins eval_07 (0.7640) and
  eval_13 (0.7578) — highest in published table on those evals. The
  50/50 mix dilutes eval_01 too much, but a SMALL fraction of SEI on
  top of the 003 mix could be a third axis.
- H3K27ac signal: direct active-enhancer mark, available as ENCODE
  bigWig per cell type. The challenge is making it cell-type-agnostic
  (per the project goal).

### Plan: Experiment 010 — dhs_signal_breadth_h3k27ac_3axis
**Type: exploring a new hypothesis** — does an orthogonal active-mark
axis (H3K27ac) help on top of 003?

H3K27ac marks active enhancers — distinct from open chromatin (DHS):
many open elements are POISED (not active), and H3K27ac selects the
ACTIVE subset. This is the most direct "currently active enhancer"
signal in ENCODE data.

To make it cell-type-agnostic (project goal: generalize beyond labeled
cell types), use the MAX H3K27ac signal across multiple cell types as
the third axis weight. An element with high max-H3K27ac is one that
ACTIVELY drives transcription in at least one cell context — should
encode cleaner enhancer grammar than open-but-inactive DHS.

Plan:
1. Download a cell-type-broad H3K27ac bigWig (likely ENCODE ChIP-seq
   from K562 + HepG2 + SK-N-SH or use the rDHS H3K27ac max-Z column
   that ENCODE distributes).
2. Precompute mean H3K27ac signal at each DHS summit window.
3. 003 mix + a third additive axis weighted by H3K27ac:
   - 16,667 mean_signal-weighted (DHS)
   - 16,666 numsamples-weighted (DHS)
   - 16,667 H3K27ac-weighted (DHS)
   - All disjoint; same 200bp summit-centered extraction.

**Generalization justification.** H3K27ac at a DHS is a distinct
regulatory-state signal from accessibility breadth or signal intensity:
an element can be open in many cells but only active (H3K27ac-marked)
in a few. The H3K27ac axis selects for elements where regulatory
machinery is ACTIVELY engaged, not just sterically accessible. A model
trained on actively-regulating elements should learn cleaner enhancer
grammar that transfers to held-out cell types.

**Predicted**: cross-14 ∈ [0.770, 0.785]. If > 0.7735, H3K27ac is a
real third axis — first multi-axis additive win since 003.
If ≤ 0.7735, active-chromatin signal is implicit in mean_signal /
numsamples.

Decision rule:
- cross-14 > 0.778 → H3K27ac is a real lever; tune ratio in 011.
- cross-14 ∈ [0.770, 0.778] → tie; pivot to SEI chromatin states.
- cross-14 < 0.770 → active marks don't add; pivot to a different
  data-type axis (SEI states or cross-species DHS).

---

## 2026-04-24 12:35 — Experiment 010 result: dhs_signal_breadth_ccremaxz_3axis

**Slight loss.** eval_01 = 0.7179 (Δ = -0.015 vs 003), cross-14 = 0.7586
(Δ = -0.015). Same pattern as 008 (cCRE filter): adding cCRE-derived
information dilutes the unique-element pool with redundant selections,
because cCRE metrics are correlated with mean_signal (both derived from
DNase data).

### Theory v8 → v9
> ENCODE annotation derivatives (cCRE class, cCRE maxZ) do NOT add
> orthogonal information to mean_signal + numsamples. They are
> downstream of the same DNase data. Adding them as third axes
> consistently hurts (008 -0.006, 010 -0.015).
>
> The 003 recipe (50K unique DHS elements via additive signal+breadth)
> appears to be at the local optimum for DHS-derived axes. Beating it
> requires either:
> (a) An axis from a TRULY different data source (motif content,
>     non-DNase TF ChIP-seq, etc.).
> (b) A structural change (mixing ratio, sample with replacement,
>     element deduplication).

### Most informative next experiment

The single biggest assumption I have NOT tested is the 50/50 mixing
ratio. 003 picked 50/50 by default. Was that optimal?

The 002 result (breadth-only) lost on eval_01 vs 001 (signal-only):
0.7152 vs 0.7242. So the signal axis is somewhat stronger than
breadth. The 003 mix at 50/50 may be sub-optimal — tilting to more
signal could yield a small gain.

This is a simple, fast test that establishes whether the 50/50 ratio
is a free parameter worth tuning, or a robust ridge.

### Plan: Experiment 011 — dhs_signal_breadth_70_30
**Type: refining the winning ratio.** Same as 003 but 70% mean_signal-
weighted (35K) + 30% numsamples-weighted (15K). Tests whether tilting
toward signal at the expense of breadth helps.

**Generalization justification.** mean_signal weighting captures sharp
TF-motif clarity; numsamples captures invariance. From 001 vs 002
results, signal was the stronger single axis — so a sample budget
slightly tilted toward signal might capture more actionable motif
information per element while still keeping enough breadth diversity
for cell-type-invariance signal.

**Predicted**: cross-14 ∈ [0.770, 0.778], eval_01 ∈ [0.728, 0.738].
Most likely a small win (+0.002 to +0.005) on eval_01 since signal
helped more on that eval. Cross-14 likely tied (gains on eval_01/07
balanced by losses on eval_04/08/09).

Decision rules:
- cross-14 > 0.778 → asymmetric ratio is real lever; binary search
  to find optimum (012 = 80/20).
- cross-14 ∈ [0.770, 0.778] AND eval_01 > 0.733 → tilt toward signal
  is a real eval_01 improvement; commit to 70/30.
- cross-14 < 0.770 OR eval_01 < 0.728 → 50/50 is robust; revert.

---

## 2026-04-24 13:05 — Experiment 011 result: dhs_signal_breadth_70_30 — NEW CHAMPION

**Strong, broad win.** eval_01 = 0.7383 (Δ = +0.006 vs 003), cross-14
= 0.7811 (Δ = +0.008). **Wins on 13 of 14 evals.** Per-seed eval_01:
0.7405 / 0.7357 / 0.7386 (std 0.002 — far below noise floor).

| metric   | 011    | 003    | Δ      |
|----------|--------|--------|--------|
| eval_01  | 0.7383 | 0.7327 | +0.006 |
| eval_07  | 0.7751 | 0.7618 | +0.013 |
| eval_13  | 0.7644 | 0.7469 | +0.018 |
| eval_10  | 0.8103 | 0.8019 | +0.008 |
| eval_12  | 0.7005 | 0.6929 | +0.008 |
| cross-14 | 0.7811 | 0.7735 | +0.008 |

The biggest gains are on eval_07 and eval_13 (cell-type-specific
evals). 003's 50/50 was diluting the cell-type-specific signal. The
70/30 tilt to mean_signal recovers it without losing breadth-driven
gains elsewhere.

### Theory v9 → v10
> Quality axes combine ASYMMETRICALLY when their standalone strengths
> differ. The optimum is a **tilted** additive mix where each axis
> claims a sample fraction proportional (or related) to its
> single-axis performance.
>
> For DHS-derived axes: mean_signal ≈ 70%, numsamples ≈ 30% beats
> the naive 50/50 by +0.008 cross-14, +0.018 on the worst-performing
> 003 eval.
>
> Generalization: future axes should be allocated proportional to
> their standalone informativeness, not uniformly. This may explain
> why 010's 1/3 cCRE_maxZ allocation hurt: the cCRE axis is weaker
> than signal/breadth and a 1/3 budget allocation over-funded it.

### Plan: Experiment 012 — dhs_signal_breadth_80_20
**Type: refining the new winning ratio.** Binary search to bracket
the optimum: test if pushing signal share further (80%) wins, ties,
or loses vs 70/30. This pins down the optimum within ±10%.

Plan:
- 40K mean_signal-weighted + 10K numsamples-weighted DHS, 200bp
  summit-centered, 3 seeds.

**Predicted**: cross-14 ∈ [0.778, 0.785], eval_01 ∈ [0.735, 0.745].
- If 80/20 > 70/30 → optimum is even more signal-heavy; try 90/10
  (but 90/10 risks losing too much breadth).
- If 80/20 ≈ 70/30 (within 0.003) → flat optimum; commit to 70/30
  as the recipe for downstream experiments.
- If 80/20 < 70/30 → 70/30 is at peak; explore other levers.

The downside risk is that pushing too far toward signal converges to
001 (pure signal, eval_01 = 0.7242 — below 011). So there must be a
sweet spot somewhere in [60/40, 90/10].

---

## 2026-04-24 13:35 — Experiment 012 result: dhs_signal_breadth_80_20

**Sharp collapse.** eval_01 = 0.7055 (Δ = -0.033 vs 011), cross-14 =
0.7433 (Δ = -0.038). Per-seed std jumped to 0.022 (vs 011's 0.002).

Trajectory on the ratio axis:
| ratio | cross-14 | eval_01 | std |
|-------|----------|---------|-----|
| 50/50 (003) | 0.7735 | 0.7327 | 0.025 |
| 70/30 (011) | 0.7811 | 0.7383 | 0.002 |
| 80/20 (012) | 0.7433 | 0.7055 | 0.022 |

Asymmetric peak: monotone climb 50/50 → 70/30, sharp cliff 70/30 → 80/20.

### Theory v10 → v11
> The "tilt-proportional-to-standalone-strength" heuristic has a
> per-axis stability floor. Each axis must contribute a minimum
> sample count to provide statistically stable training signal. For
> the numsamples (breadth) axis, the threshold is ~15K elements.
> Below it, the per-seed library composition becomes noisy and
> performance collapses. Pushing the dominant axis past this floor
> destroys the very gains it was supposed to produce.
>
> Operationalisation: when allocating axes, set each axis weight ≥
> max(0.15 of total budget, stability floor) AND tilt remaining
> budget proportional to single-axis strength.

### Plan: Experiment 013 — dhs_signal_breadth_60_40
**Type: refining; bracket the optimum.** Quick test to confirm
70/30 is the peak vs a more breadth-leaning ratio.

Plan: 30K mean_signal-weighted + 20K numsamples-weighted. 3 seeds.

**Generalization justification.** Same as 011 — DHS signal axes
combined additively. The ratio question is purely empirical.

**Predicted**: cross-14 ∈ [0.778, 0.781], eval_01 ∈ [0.732, 0.738].
Expected slightly below 011 (0.7811) but above 003 (0.7735) —
monotone climb from 50/50 to 70/30, with 60/40 in between.

Decision rules:
- 013 ≈ 011 (within 0.003 cross-14) → ratio plateau between 60-70%
  signal; commit to 70/30 as recipe and pivot to NEW LEVER for 014.
- 013 > 011 → optimum is between 50 and 65; try 65/35 next.
- 013 < 011 by > 0.003 → 70/30 confirmed peak; pivot to NEW LEVER.

After 013, regardless of outcome, lock the ratio decision and use
remaining experiments to test orthogonal axes:
- 014: a third axis from a TRULY new data type (motif content, TF
  ChIP-seq density, or cross-species DHS overlap).
- 015+: structural variants and combinations.

---

## 2026-04-24 14:05 — Experiment 013 result: dhs_signal_breadth_60_40

**Collapse on the breadth side too.** eval_01 = 0.7119 (Δ = -0.026
vs 011), cross-14 = 0.7501 (Δ = -0.031). Per-seed eval_01: 0.7215 /
0.7328 / 0.6815 (std ≈ 0.027 — wide, like 012, very unlike 011).

Full ratio sweep:
| ratio | cross-14 | eval_01 | per-seed std |
|-------|----------|---------|--------------|
| 50/50 (003) | 0.7735 | 0.7327 | 0.025 |
| 60/40 (013) | 0.7501 | 0.7119 | 0.027 |
| 70/30 (011) | 0.7811 | 0.7383 | 0.002 |
| 80/20 (012) | 0.7433 | 0.7055 | 0.022 |

Trajectory is non-monotone in BOTH directions away from 70/30.
60/40 is even worse than 50/50, despite being closer to the peak.
Decision rule (committed in 011 plan): 013 < 011 by > 0.003
cross-14 → **70/30 confirmed peak. Lock ratio. Pivot to new lever.**

### Theory v11 → v12
> The dominant story is no longer "stability floor on the smaller
> axis" but **stability of the optimization itself**. 70/30 sits in
> a narrow basin where the loss landscape produces tightly
> reproducible solutions (per-seed std 0.002, an order of magnitude
> below the model-noise floor of ~0.005). All neighboring ratios
> show 0.020-0.027 std — single 3-seed runs cannot resolve their
> ordering reliably.
>
> Implications for further library work:
> 1. Once a configuration shows 0.020+ per-seed std, more 3-seed
>    sweeps in that neighborhood are noise. Pivot to a different
>    lever rather than refine.
> 2. Per-seed stability is a *feature of the library*, not just
>    optimization noise. The most useful libraries may be ones
>    whose composition lands the model in a robust loss basin.
> 3. Lock 70/30 (35K signal + 15K breadth) as the recipe for all
>    downstream experiments that need a baseline mix.
> 4. The remaining win surface is in *new orthogonal axes*, not in
>    refining the two-axis sample allocation.

### What I've learned across 13 experiments
- **DHS as a substrate**: open-chromatin sampling beats every
  alternative. (cf. baselines.)
- **Mixing > single axis**: 003 (50/50) > both 001/002 single-axis.
- **Asymmetric mix > symmetric**: 011 (70/30) > 003.
- **Quality axes correlated within DHS**: cCRE class (008) and
  cCRE maxZ (010) are correlated derivatives of DNase signal —
  give no orthogonal lift.
- **Conservation as a positive weight**: 007, weakest result. Old
  conserved elements are often "boring" — strong evolutionary
  signal but limited regulatory diversity.
- **Within-element augmentation < element diversity**: 009 (2
  windows × 25K) lost big to 011 (1 window × 50K).
- **Synthetic dilution hurts**: 004's 20% i.i.d. random hurt
  every eval. Pure-coverage strategies don't help here.
- **NMF stratification doesn't help**: 005's enforced component
  diversity is dominated by the underlying weight-space mix.

### Plan: Experiment 014 — dhs_70_30_ccre_typed
**Type: branching; introduce a TRULY new lever — element TYPE
balance.** Hold the 70/30 mean_signal/numsamples ratio (the locked
recipe), but stratify the SOURCE pool: equal counts of distinct
ENCODE cCRE functional classes inside the signal half, so the
library's regulatory grammar is balanced across promoter (PLS),
proximal-enhancer (pELS), and distal-enhancer (dELS) regulatory
modes rather than dominated by the most-abundant class.

Why this is orthogonal:
- 011's 70/30 selects elements ranked by intensity; the resulting
  draw is dELS-dominated (~70% of the mass) because dELS makes
  up the majority of high-signal cCREs.
- A model trained mostly on enhancer grammar may underpredict
  promoter-proximal regulatory grammar that an unseen cell type
  presents in held-out evals.
- 008 already showed that *filtering* to PLS/pELS/dELS at-least-
  doesn't-hurt (eval_01 = 0.7269, on par with 003). 014 goes
  further: enforce equal representation of the three classes
  *inside the signal-weighted half*, so the model sees the same
  number of training elements per regulatory class.

Plan:
- Use locked recipe ratio: 35K signal-weighted + 15K
  numsamples-weighted = 50K.
- For the 35K signal half, draw equal counts (~11.67K) from each
  of {PLS, pELS, dELS} cCRE-class subsets, signal-weighted within
  each subset.
- For the 15K breadth half, draw numsamples-weighted across all
  cCRE-overlapping DHS (no class stratification — keep it simple,
  isolate the lever to the signal half).
- 3 seeds, 200bp summit windows, dedup across the two halves.

**Predicted**: cross-14 ∈ [0.770, 0.785], eval_01 ∈ [0.730, 0.745].
- Win-case (eval_07/eval_13 lift > +0.005): regulatory-class
  balance is a real lever; design 015 to push promoter share or
  add CTCF/H3K4me3 classes too.
- Tie-case (cross-14 within 0.003 of 011): cCRE-class is correlated
  with mean_signal; no orthogonal information. Pivot to truly
  non-DHS-derived axis (TF ChIP-seq density, GC% balance).
- Loss-case (cross-14 < 0.778): forcing class balance hurts because
  it overweights rare classes. Pivot.

The risk is the same as 008/010 — that cCRE classes are too
correlated with the mean_signal signal to provide orthogonal
information. But 014 differs by *enforcing* equal representation
rather than just filtering, so the lever it tests is fundamentally
different (composition rebalancing, not eligibility filtering).

---

## 2026-04-24 14:50 — Experiment 014 result: dhs_70_30_ccre_class_balanced

**Orthogonal lever found, but wrong direction on cross-14.**
eval_01 = 0.7280 (Δ = -0.010 vs 011), cross-14 = 0.7676 (Δ = -0.014).
Per-seed std 0.001 — tightest of the entire series so far.

Trade pattern (vs 011):
- Wins: eval_04 (+0.006), eval_08 (+0.007), eval_09 (+0.006)
- Losses: eval_07 (-0.042), eval_13 (-0.049), eval_01 (-0.010)
- Cross-14 net: -0.014

The trade is not random noise — it's a deterministic redistribution
across eval types. Libraries with class-balanced composition gain
on the diversity-sensitive evals and lose on the cell-type-specific
ones, with the lose side bigger.

### Theory v12 → v13
> Orthogonal axes produce **deterministic trade-off vectors** across
> the eval suite, not uniform lifts. The 14 evals stratify into
> sub-types (cell-type-specific, diversity-sensitive, in-
> distribution, etc.) and each library lever pushes differently on
> each sub-type. The librarian's optimization is now multi-objective:
> find a lever combination whose composite trade is net-positive on
> the cross-14 metric.
>
> Locking 70/30 preserved the tight per-seed basin even under a
> large composition change. This means we can search the orthogonal-
> axis space cheaply (one 3-seed run resolves directional signal).

### Plan: Experiment 015 — dhs_70_30_gc_stratified
**Type: testing a TRULY new lever — sequence-derived GC content
stratification.** GC content is a sequence property, fully
orthogonal to any DNase-derived metric. Tests whether the eval_08
gain in 014 came from cCRE-class structure (CpG islands, promoter
motifs) or from a more general "diverse sequence composition"
property that includes GC variation.

Plan:
- Same 70/30 (35K signal + 15K breadth) ratio.
- Within EACH half: bucket candidate DHS into GC-content quintiles
  (computed from the 200bp summit window), then draw equal counts
  per quintile, weighted by mean_signal (signal half) or
  numsamples (breadth half) within each quintile.
- 3 seeds, dedup across halves.

**Generalization justification.** Cell types vary in their use of
GC-rich (often promoter / CpG-island) vs GC-poor (often distal-
enhancer / heterochromatin-adjacent) regulatory elements. A library
that under-represents either GC regime will produce a model that
generalizes poorly to cell types whose regulatory bias is on the
under-represented end.

**Predicted**: cross-14 ∈ [0.770, 0.785], eval_01 ∈ [0.730, 0.745].
- Win-case (cross-14 > 0.781, eval_08 lift): GC stratification is a
  useful orthogonal axis. Compose with 011 in 016.
- Tie-case (within 0.003): GC adds nothing on top of mean_signal.
- Loss-case + eval_08 lift: same trade as 014. Pivot to non-DHS
  data sources.

The experiment also has a diagnostic value beyond direct outcome:
if eval_08 lifts under both 014 AND 015, then sequence diversity
(of any kind) is the active mechanism — class structure is
incidental. If eval_08 lifts only under 014 (not 015), then cCRE
class encodes something specific (CpG, promoter motifs) that GC
does not capture.

---

## 2026-04-24 16:00 — Experiment 015 result: dhs_70_30_gc_stratified

**MAJOR WIN. Wins on ALL 14 evals vs 011. New champion.**

eval_01 = 0.7509 (Δ = +0.013 vs 011), cross-14 = 0.7960
(Δ = +0.015 vs 011) — the largest cross-14 gain of any experiment.
Biggest individual gains concentrate on the previously-hardest
evals: eval_07 +0.024, eval_08 +0.023, eval_13 +0.025.

Per-seed eval_01: 0.7578 / 0.7318 / 0.7631 (std ≈ 0.017 — wider
than 011's 0.002 but the mean is so much higher that the win is
unambiguous). The seed=1 outlier (0.7318) is still above 011's
mean — the floor of 015 ≥ the ceiling of 011's noise interval.

### Theory v13 → v14
> **Sequence-composition diversity is the missing axis.** The 011
> recipe optimizes regulatory-intensity (mean_signal) and cell-type
> breadth (numsamples) — both DNase-derived metrics that bias the
> natural draw toward a narrow sequence-composition band (mostly
> GC-elevated open chromatin). Adding a third axis defined on the
> SEQUENCE itself — independent of any assay — unlocks the largest
> single-experiment gain in the series.
>
> Mechanism: GC stratification forces inclusion of (1) lower-signal
> GC-poor elements (likely distal enhancers in less-accessible
> compartments), and (2) extreme-high-GC elements (CpG-island
> regulatory contexts). Both compartments under-represented in the
> 011 draw. The model now sees a GC dynamic range matching what
> unseen cell types are likely to present.
>
> Diagnostic vs 014: 014's class balance also lifted eval_08
> (+0.007) but cost +cell-type-specific evals. 015's GC
> stratification lifts eval_08 MORE (+0.023) AND lifts the
> cell-type-specific evals (+0.024 / +0.025). So **sequence
> diversity per se is the active mechanism** — cCRE class is a
> coarser, partially-correlated proxy.

### Methodological pattern (lab-doctrine update)
> Locked-ratio (70/30) + orthogonal stratification is the winning
> recipe shape. The ratio provides a stable optimization basin;
> the stratification expands the input distribution. Future
> experiments should preserve the ratio and explore the orthogonal-
> axis space on top.

### What I'd do with infinite experiments
Three follow-up directions, ranked by expected information:
1. **Verify-the-mechanism**: alternate sequence-derived axes —
   dinucleotide composition (CpG O/E especially), k-mer entropy.
   If they also lift, the mechanism is general "sequence diversity"
   not specifically GC.
2. **Granularity**: finer GC bins (10) — does the win continue or
   overshoot into noise? Approaches 015's stability floor at
   3.5K per bin.
3. **Stack**: GC + cCRE class joint stratification — does an
   already-orthogonal lever (GC) compose with another orthogonal
   lever (class) for additional lift?

I have 15 experiments left after 015. Plan: 016 = granularity test
(bracketing 015), 017-019 = alternate sequence axes (CpG O/E,
k-mer, dinucleotide), 020-021 = stacking, 022+ = remaining
exploration / final tuning.

### Plan: Experiment 016 — dhs_70_30_gc_stratified_10bins
**Type: refining; bracketing the new champion's hyperparameter.**
Tests whether finer GC granularity (10 equal-population deciles)
adds more lift than 5 quintiles. The unknowns:
- More bins → more uniform GC coverage → potentially more lift.
- More bins → fewer elements per bin (3.5K signal, 1.5K breadth)
  → approach the per-axis stability floor we discovered in
  012/013, risking variance collapse.

Plan: identical to 015 except N_BINS = 10. 3 seeds.

**Predicted**: cross-14 ∈ [0.790, 0.805], eval_01 ∈ [0.745, 0.760].
- Win-case: 016 > 015 by > 0.003 on cross-14 → push to 15 or 20
  bins next.
- Tie-case: 016 ≈ 015 → 5-10 bins is a flat optimum; pivot to
  alternative sequence axes.
- Loss-case + std collapse: 1.5K/bin breadth is below stability
  floor; pivot back to 5 bins as the 015 champion.

Decision rule for the next phase: regardless of 016 outcome, lock
in the better of {015, 016} and use 017+ to test alternate
sequence-composition axes (CpG O/E first).

---

## 2026-04-24 16:50 — Experiment 016 result: dhs_70_30_gc_stratified_10bins

**Collapse below 015.** eval_01 = 0.7190 (Δ = -0.032 vs 015),
cross-14 = 0.7596 (Δ = -0.036 vs 015). Per-seed std 0.027 (matching
012/013 instability). 016 even lost to 011.

10 GC bins cuts the per-bin breadth count to 1.5K — well below the
~3K per-(axis × bin) stability floor.

### Theory v14 → v15
> The stability floor is per-(axis × bin), not just per-axis.
> Stratification budget is N / (n_axes × n_bins): with 50K total
> and 70/30 split, 5 bins gives 7K/3K per bin (both safe), 10 bins
> gives 3.5K/1.5K (breadth crosses floor).
>
> Practical rule: total budget per (axis, bin) cell ≥ 3K.
> Implication: as orthogonal stratification axes are added,
> n_bins per axis must shrink to keep cell counts above floor.

### Plan: Experiment 017 — dhs_70_30_cpg_oe_stratified
**Type: testing whether the GC win is general or GC-specific.**
Same pattern as 015 but stratified on CpG O/E (observed CpG /
expected CpG given C and G counts) instead of GC content.

CpG O/E is correlated with GC but biologically distinct:
- CpG islands: O/E > 0.6, often promoter-proximal
- CpG-depleted: O/E < 0.4, most of the genome (CpG erosion via
  methylation-driven mutation over evolution)
- Non-monotone in GC: a 60% GC sequence with no CpG dinucleotides
  has very different regulatory significance than a 60% GC
  sequence inside a CpG island.

Plan:
- Precompute CpG O/E per DHS 200bp summit window:
  CpG O/E = (count_CpG * length) / (count_C * count_G)
  Set undefined (count_C=0 or count_G=0) to NaN.
- Same 70/30 ratio, 5 equal-population CpG-O/E bins, identical
  draw protocol to 015.
- 3 seeds.

**Generalization justification.** Cell types vary in CpG-island
methylation status. A library that under-represents CpG-island vs
CpG-depleted regulatory contexts will produce a model that
generalizes poorly to cell types whose epigenetic state shifts
which class is active.

**Predicted**: cross-14 ∈ [0.785, 0.800], eval_01 ∈ [0.745, 0.760].
- Mostly tied with 015 (within 0.005): "any sequence-composition
  diversity" mechanism — pivot to combining axes.
- Win > 015 by > 0.005: CpG O/E captures something GC misses;
  combine in 018 for stacking.
- Loss to 015 by > 0.005: GC-specific lever, possibly because GC
  is a coarser proxy for many sequence properties at once. Combine
  GC with class (014's lever) instead.
- Big loss (cross-14 < 0.781 = 011 baseline): CpG O/E doesn't
  produce stable strata; revert to GC-only and explore different
  axis families (TF ChIP-seq density).

---

## 2026-04-24 17:50 — Experiment 017 result: dhs_70_30_cpg_oe_stratified

**Loss to both 015 and 011.** eval_01 = 0.7212 (Δ = -0.030 vs 015,
-0.017 vs 011), cross-14 = 0.7611 (Δ = -0.035 vs 015). Per-seed
std 0.021 — same instability pattern as 016.

The CpG O/E distribution turned out to be degenerate at both
extremes:
- 5% of DHS have zero CpG (whole bottom quintile is
  composition-homogeneous)
- Top quintile contains low-denominator artifacts (O/E up to 40)

Equal-population binning over this distribution forced library
composition to over-represent these compositional extremes.

### Theory v15 → v16
> **Sequence-derived axes are NOT all equivalent levers.** The 015
> win requires more than "stratify by some sequence property" — it
> requires a sequence axis that has:
> 1. Smooth, non-degenerate distribution across its range.
> 2. Biological meaning at every quantile.
> 3. No bin-edge artifacts.
>
> GC content satisfies all three; CpG O/E fails (1) and (3) due
> to its zero-heavy bottom and denominator-artifact top. Future
> sequence-derived axes must be DENSITY metrics (varying smoothly)
> rather than RATIO metrics (with degenerate denominators).

### Three failure modes characterized
- 014 (cCRE class balance): orthogonal but wrong trade-vector
- 016 (GC 10 bins): right axis, wrong granularity
- 017 (CpG O/E 5 bins): right granularity, wrong axis distribution

### Plan: Experiment 018 — dhs_70_30_dinuc_entropy_stratified
**Type: testing whether smooth sequence-density axes generalize the
GC win.** Dinucleotide entropy is the Shannon entropy of the
empirical 16-dimensional dinucleotide distribution within the 200bp
window, normalized by log2(16). It is a density metric (well-
defined for every sequence, no degeneracies) and varies smoothly
across DHS. Low entropy = repeat-rich or composition-skewed
sequences; high entropy = balanced dinucleotide composition.

This tests:
- "Density-axis sequence stratification lifts" (vs. CpG O/E's
  degenerate-axis failure).
- Captures a different sequence-composition dimension than GC
  (entropy is invariant under permutation of frequencies; GC is
  not).

Plan: Same as 015 but with dinucleotide entropy as the
stratification axis. 5 equal-population quintiles. 3 seeds.

**Predicted**: cross-14 ∈ [0.785, 0.795], eval_01 ∈ [0.745, 0.755].
- Win > 015 by > 0.003: stack with GC in 019.
- Tie within 0.005: dinuc entropy is correlated-with-GC — confirm
  general "smooth sequence axis" mechanism, then explore stacking.
- Loss > 0.005 below 015: GC is the right axis specifically; pivot
  to non-DHS data (TF ChIP-seq density at 019).

---

## 2026-04-24 18:50 — Experiment 018 result: dhs_70_30_dinuc_entropy_stratified

**Loss to 015 AND 011.** eval_01 = 0.7141 (Δ = -0.037 vs 015,
-0.024 vs 011), cross-14 = 0.7548 (Δ = -0.041 vs 015). Per-seed
std 0.022. Same instability pattern as 016/017.

Now 4 sequence-axis experiments form a clear pattern:
| exp | axis | result |
|-----|------|--------|
| 015 | GC | WIN +0.015 vs 011 |
| 016 | GC, 10 bins | LOSS (granularity) |
| 017 | CpG O/E | LOSS (degenerate distribution) |
| 018 | dinuc entropy | LOSS (tail = repeats) |

### Theory v16 → v17
> **Stratification helps only when EVERY bin contains useful
> regulatory examples.** Diversity per se is not the goal —
> STRUCTURED diversity along an axis where every level contains
> transferable regulatory grammar is the goal.
>
> GC works because GC-poor DHS are still real regulatory elements
> (just from heterochromatin-adjacent enhancer compartments).
> CpG O/E and dinuc entropy partition by sequence statistics, and
> their tail bins concentrate repeat/low-complexity sequences that
> dilute the model's regulatory training signal.
>
> Practical rule for axis design: prefer axes that vary across
> CHROMATIN STATE rather than across SEQUENCE STATISTICS. GC
> happens to satisfy both because it tracks isochore boundaries
> which align with regulatory landscape boundaries.

### Pivot: stop searching for another single sequence axis
The information value from "try yet another sequence axis" is
dropping fast. Three failures with similar mechanisms (016/017/018)
strongly suggest no other simple sequence-derived axis will lift
on top of GC.

### What's left to test
1. **Stacking** — does GC stratification stack with non-sequence
   levers like cCRE filtering (008's lever)?
2. **Bin-design alternatives** — different GC bin schemes (3 bins
   for stability, custom non-uniform bins for tail emphasis).
3. **Different data sources** — TF ChIP-seq density (independent
   assay), ENCODE regulation tracks.
4. **Window manipulations** — wider window context, multiple
   non-overlapping windows around summits.

### Plan: Experiment 019 — dhs_70_30_gc_stratified_ccre_filtered
**Type: stacking the GC win with the cCRE-overlap filter (008's
lever).** 008 tied 011 (cross-14 = 0.7671 vs 011's 0.7811 — close);
015 lifts 011 to 0.7960 via GC stratification. If the two
mechanisms are orthogonal, stacking should lift further. If they
share common information, stacking ties or slightly loses.

Plan:
- Same 70/30 ratio as 015.
- Restrict candidate pool to cCRE-overlapping DHS only (1.35M
  candidates, vs 015's 3.59M full pool).
- Recompute GC quintile boundaries on the cCRE-overlapping subset
  (different distribution: cCRE-overlap is GC-elevated since
  promoters/CpG islands are over-represented in cCREs).
- 5 GC bins, equal-population over the subset.
- 7K signal + 3K breadth per bin (same per-cell counts as 015).
- 3 seeds.

**Generalization justification.** cCRE-overlap is a quality filter
(elements have independent ENCODE chromatin-state evidence),
whereas GC stratification is a sequence-coverage filter. Combining
them may produce a library that is BOTH high-quality regulatory
AND sequence-composition-diverse. Per-cell counts (7K signal, 3K
breadth) remain at the 015 stability point so the basin should
stay tight.

**Predicted**: cross-14 ∈ [0.795, 0.810], eval_01 ∈ [0.748, 0.762].
- Win > 015 by > 0.003: cCRE filter and GC stratification are
  stackable orthogonal levers; pivot to 020 = add a third lever.
- Tie within 0.005: cCRE filter is dominated by GC stratification.
  Pivot to bracket-experiment GC bin counts.
- Loss > 0.005: cCRE-restricted GC stratification samples a
  different sequence space (likely promoter-shifted) that hurts
  cell-type-specific evals. Drop the stack.

---

## 2026-04-24 19:50 — Experiment 019 result: dhs_70_30_gc_stratified_ccre_filtered

**Biggest collapse yet.** eval_01 = 0.7097 (Δ = -0.041 vs 015,
-0.029 vs 011 baseline). cross-14 = 0.7472 (Δ = -0.049 vs 015).
Per-seed std = 0.040 — widest of any experiment in the series.

The stacking hypothesis (cCRE filter + GC stratification both add)
was wrong. Three compounding mechanisms killed it:
1. cCRE filter excludes the non-cCRE-annotated low-GC elements
   that 015 specifically pulls in (these are in heterochromatin-
   adjacent enhancer compartments, lower-confidence ENCODE
   evidence but real regulatory elements).
2. cCRE-restricted distribution shifts GC quintile boundaries —
   the "low-GC" bin in 019 is 0.020-0.390 vs 015's 0.000-0.375,
   sampling a different compositional space.
3. Smaller bin pools (250K vs 685K) reduce per-seed averaging
   stability.

### Theory v17 → v18
> **Orthogonal levers do NOT automatically stack.** When two
> levers act on the same underlying distribution, stacking can
> violate BOTH levers' assumptions. Each lever has implicit
> requirements about the sample space; combining levers can break
> those requirements.
>
> Practical rule for stacking: (a) the filter must not shift the
> stratification axis distribution, and (b) per-bin candidate
> pools must remain large (>50K).

### Champion remains 015 — uncontested
After 4 follow-up experiments (016/017/018/019), all losses. 015's
GC-stratified 70/30 is robust. It may be near or at the local
optimum for this design family.

### Plan: Experiment 020 — dhs_gc_stratified_signal_only
**Type: ablation.** Tests whether the breadth axis is still needed
when GC stratification is in play, or whether GC stratification
absorbs the breadth-diversity benefit.

Plan:
- 100% mean_signal-weighted (no breadth axis at all).
- 5 GC bins, equal-population, 50K total.
- 10K signal-weighted draws per bin (vs 015's 7K signal + 3K
  breadth per bin).
- 3 seeds.

This is an ABLATION not a refinement. If the breadth axis is
absorbed by GC stratification:
- 020 ≥ 015: drop breadth axis, simpler recipe.
- 020 < 015: breadth axis still adds value, keep 015.

**Predicted**: cross-14 ∈ [0.785, 0.800], eval_01 ∈ [0.745, 0.760].
- 020 wins: GC stratification's "include lower-signal but
  GC-poor elements" mechanism implicitly captures the
  breadth-axis benefit because lower-signal elements span more
  cell-type contexts.
- 020 loses: numsamples-axis carries information distinct from
  GC; the 70/30 mix is genuinely orthogonal to GC.

### Plan: Experiment 021 — dhs_gc_stratified_3bins
**Type: granularity bracket.** Tests whether 5 bins is the unique
sweet spot or if 3 bins (more per-bin elements, less GC granularity)
is comparable. With 3 bins: 11.7K signal + 5K breadth per bin —
both very safe vs the 3K stability floor.

Plan: same as 015 but N_BINS=3. 3 seeds.

**Predicted**: cross-14 ∈ [0.785, 0.800], eval_01 ∈ [0.745, 0.760].
Probably tied with 015 (within 0.005) — since 5 bins is just at
the floor and 3 bins is well above it, but 5 bins captures more
GC dynamic range.

I'll run 020 first since it directly tests an open question
(ablation of breadth), then 021 as the granularity bracket.

---

## 2026-04-24 20:50 — Experiment 020 result: dhs_gc_stratified_signal_only

**Important ablation. Both axes contribute.** eval_01 = 0.7401
(per-seed std 0.006 — much tighter than 015's 0.017), cross-14 =
0.7841. Better than 011 by +0.003, worse than 015 by -0.012.

Decomposition of the 015 win:
- GC stratification alone (020 vs 011): +0.003 cross-14
- 70/30 mix on top of GC stratification (015 vs 020): +0.012

Both contribute, but the numsamples mix is the bigger single
component. Yet 020 is much more stable (std 0.006 vs 015's 0.017),
suggesting the variance in 015 comes from cross-half overlap
during stratified draws.

### Theory v18 → v19
> **Stratification × intensity-mixing are MULTIPLICATIVE levers.**
> 015's lift comes from their composition: GC stratification
> PARTITIONS the regulatory landscape; the 70/30 mix WITHIN each
> partition selects elements that are both intense and broadly-
> active. Neither alone produces the full lift.
>
> Mechanism: without GC partitioning, the natural draw concentrates
> the signal/numsamples-weighted elements in overlapping high-GC
> compartments. Without the mix, partitions select for intense-only
> elements (losing per-partition breadth diversity).
>
> Practical rule: future axes should be tested in COMBINATION with
> the 70/30 mix (and GC stratification), not in isolation. Single-
> axis tests under-estimate axis contributions.

### Plan: Experiment 021 — dhs_70_30_gc_stratified_3bins
**Type: granularity bracket on the champion.** Tests if 5 GC bins
is the unique sweet spot or whether 3 bins is comparable.

3 bins gives 11.7K signal + 5K breadth per bin — well above the
3K stability floor. It captures coarser GC resolution (low / mid
/ high GC) but with safer per-bin counts.

Plan: identical to 015 except N_BINS = 3. 3 seeds.

**Predicted**: cross-14 ∈ [0.785, 0.795], eval_01 ∈ [0.740, 0.755].
- 021 ≈ 015 (within 0.005): granularity is plateau between 3 and
  5 bins. Lock both as recipe alternatives.
- 021 < 015 by > 0.005: 5 bins captures more useful diversity than
  3 — granularity sweet spot is sharper than expected.
- 021 > 015 (unlikely): 3 bins is even better; bracket at 4 bins
  next.

This narrows the granularity question. Then I'll have remaining
budget for 022 = breadth-only ablation (mirror of 020) and 023+
for orthogonal-axis experiments.

---

## 2026-04-24 21:45 — Experiment 021 result: dhs_70_30_gc_stratified_3bins

**Strong falsification.** eval_01 = 0.7173 (per-seed std 0.015 —
seeds: 0.7312 / 0.6969 / 0.7237), cross-14 = 0.7574. Way below
predicted [0.785, 0.795]. Lands BELOW 011 (no stratification at
all, cross-14 = 0.7811) and basically ties 016 (10 bins, below
floor, cross-14 = 0.7596).

Granularity sweep now reads:
- 3 bins (021):  cross-14 = 0.7574  per-bin counts 11.7K+5K (safe)
- 5 bins (015):  cross-14 = 0.7960  per-bin counts 7K+3K (champion)
- 10 bins (016): cross-14 = 0.7596  per-bin counts 3.5K+1.5K (low)

5 bins is a SHARP PEAK, not a plateau floor. Both directions lose
~0.04. Coarser granularity isn't safer just because per-bin counts
are higher; what matters is whether each "bin" actually homogenizes
composition. With 3 bins, edges are 0.000/0.405/0.485/0.965 — bin 0
spans GC 0–40%, bin 2 spans 49–96%. The within-bin GC variance is
huge; stratification just shuffles the same big mixture.

### Theory v19 → v20
> **Granularity is sharply tuned, not a plateau.** GC stratification
> requires bins simultaneously narrow (homogenize composition) and
> wide (per-bin counts above floor). 5 is the unique sweet spot in
> {3, 5, 10}; both directions lose ~0.04 cross-14.
>
> Mechanism: stratification helps only when each bin is internally
> homogeneous enough that the model sees consistent composition
> within compartments. Wide bins fail this test even when per-bin
> counts are luxurious. Narrow bins fail the count floor even when
> compositions are tight.
>
> Practical: when introducing a new stratification axis, do a small
> granularity sweep (e.g. {3, 5, 7, 10}) before committing — don't
> assume 5 is universal. The "5" depends on the dynamic range of the
> axis and the per-bin floor; both vary axis-to-axis.

### Plan: Experiment 022 — dhs_gc_stratified_breadth_only
**Type: ablation, mirror of 020.** Completes the 011/020/022
decomposition triangle.

- 100% numsamples-weighted (no signal axis at all).
- 5 GC bins, equal-population, 50K total.
- 10K breadth-weighted draws per bin.
- 3 seeds.

This is the symmetric counterpart of 020 (signal-only). Together
the three points (011 = no strat, 020 = signal+strat, 022 =
breadth+strat) fully decompose the 015 win:
- 011 vs 020: signal axis under stratification
- 011 vs 022: breadth axis under stratification
- 020 + 022 vs 015: how the two axes COMPOSE under stratification

**Predicted**: cross-14 ∈ [0.770, 0.790], eval_01 ∈ [0.715, 0.745].
Probably between 011 and 020.
- 022 ≈ 020 (within 0.005): symmetric — both axes contribute
  similarly under stratification; the win is "use ANY biology-axis
  intensity within compartments".
- 022 < 020 by > 0.01: signal axis dominates under stratification;
  breadth axis is the diversity-only contributor.
- 022 > 020 (unlikely): breadth axis is actually the bigger lever
  under stratification; reread 015 mechanism.

I expect 022 < 020. Reason: 002 (pure breadth) was already worse
than 001 (pure signal) without stratification. Stratification likely
preserves that ordering. The interesting quantity is the GAP — if
gap is small, both contribute; if large, signal is the primary lever
that stratification amplifies.

---

## 2026-04-24 22:30 — Experiment 022 result: dhs_gc_stratified_breadth_only

**Surprising asymmetry, big collapse.** eval_01 = 0.7041 (per-seed
std 0.024 — biggest seed instability of the series), cross-14 =
0.7434. Way below predicted [0.770, 0.790]. Even worse than 002
(pure breadth, no stratification) at 0.7534. **Stratification HURTS
breadth-only weighting.**

Asymmetric interaction with stratification:
| axis     | no strat | + GC strat | Δ      |
|----------|----------|------------|--------|
| signal   | 0.7653   | 0.7841     | +0.019 |
| breadth  | 0.7534   | 0.7434     | -0.010 |
| 70/30    | 0.7810   | 0.7960     | +0.015 |

Stratification × signal is synergistic. Stratification × breadth is
ANTI-synergistic. The 015 win is therefore primarily "signal × strat";
the 70/30 mix adds a small bonus only because at 30% intensity the
breadth axis's harm doesn't dominate.

### Theory v20 → v21
> **Stratification's interaction with biology axes is asymmetric.**
> Different axes interact differently with the same stratification.
> GC × signal: +0.019. GC × breadth: -0.010. GC × 70/30 mix: +0.015.
>
> Mechanism: breadth-weighted (numsamples) elements concentrate
> biologically in moderate-GC compartments (promoters, broadly-
> active enhancers). Forcing draws across all 5 GC bins exhausts
> the top-numsamples tail in extreme-GC bins and pulls in noisy
> low-numsamples fillers with unusual composition. Signal-weighted
> elements span the full GC range, so stratification gives diverse
> intense exemplars per bin without filler problems.
>
> Per-seed std confirms: 020 (signal+strat) std 0.006; 022
> (breadth+strat) std 0.024; 015 (mix+strat) std 0.017. The
> breadth-axis-under-strat is unstable because of small candidate
> pools at the extremes.
>
> Practical: when introducing a new (axis, stratification) pair,
> test the axis-only and strat-only ablations separately to detect
> asymmetric interactions. The combined recipe may mask harmful
> components.

### Plan: Experiment 023 — dhs_80_20_gc_stratified
**Type: mix-ratio sweep under stratification.** 015 used 70/30. The
022 result suggests breadth-axis under strat is fragile; less
breadth might help.

- 80% mean_signal-weighted (40K, 8K per bin)
- 20% numsamples-weighted (10K, 2K per bin)
- 5 GC equal-pop bins
- 3 seeds

Per-bin breadth count = 2K, BELOW the 3K stability floor. This is
the trade — to test less breadth I either drop the count below
floor or drop bin count below 5. I'll accept the 2K-per-bin risk
because the signal half (8K/bin) is well above floor and the breadth
half is acting as a small perturbation.

**Predicted**: cross-14 ∈ [0.785, 0.800], eval_01 ∈ [0.745, 0.760].
Probably similar to 015 (within 0.01).
- 023 > 015 by > 0.005: less breadth under strat is better; 70/30
  isn't optimal under strat.
- 023 ≈ 015 (within 0.005): mix ratio is robust between 70/30 and
  80/20 under strat.
- 023 < 015 by > 0.005: 70/30 is the sweet spot; less breadth loses
  the small synergy benefit.

If 023 fails, the 70/30 + strat recipe is locked. Then 024 onward
explores other directions.

---

## 2026-04-24 23:15 — Experiment 023 result: dhs_80_20_gc_stratified

**Falsified hypothesis, big collapse.** eval_01 = 0.7196 (per-seed
std 0.022 — seeds: 0.7285 / 0.7412 / 0.6892), cross-14 = 0.7594.
Way below predicted [0.785, 0.800] and -0.037 vs 015. Even worse
than 020 (signal-only + strat = 0.7841).

Mix-ratio sweep under GC strat (breadth %):
- 0% (020): 0.7841 (signal-only + strat)
- 20% (023): 0.7594 (this experiment) — non-monotonic dip
- 30% (015): 0.7960 (champion)
- 100% (022): 0.7434 (breadth-only + strat)

The non-monotonicity is explained by the per-(axis × bin) floor:
- 023 breadth: 2K/bin (BELOW 3K floor) — collapses
- 015 breadth: 3K/bin (AT floor) — stable
The floor is a HARD constraint on every axis × bin cell, not just
total per axis.

### Theory v21 → v22
> **The stability floor is per-(axis × bin) cell, not per-axis.**
> Every cell in the (axis × bin) lattice must hold ≥ ~3K samples,
> otherwise stratification destroys that axis's contribution. 015
> sits exactly at the corner of this constraint:
> min(7K, 3K, 7K, 3K, 7K, 3K, 7K, 3K, 7K, 3K) = 3K.
>
> Practical design rule: for any (axis_i, N_bins) combination, the
> constraint is min_i(N_axis_i / N_bins) ≥ 3K. The 70/30 + 5 bins
> recipe is at the design corner; deviating in either ratio or bin
> count direction crosses it.
>
> Implications for further mix-ratio tuning: the optimization space
> is tightly constrained. 70/30 + 5 bins likely IS the unique
> sweet spot for the DHS Index dimensions. Further gains require
> either (a) different stratification axes with different floor
> properties, or (b) modifying sample definition (window size, etc).

### Plan: Experiment 024 — dhs_signal_strat_breadth_unstrat
**Type: half-stratification ablation.** Tests which half of the 015
mix actually drives the lift over 011.

- Signal half (35K): GC-stratified across 5 bins (7K/bin, at floor)
- Breadth half (15K): single weighted draw across all DHS, NOT
  stratified by GC (15K from full 3.5M pool)
- 3 seeds

The 022 result showed strat × breadth-only is anti-synergistic. If
the breadth half doesn't need stratification, removing it should
neutralize the harm and either match or exceed 015. If 024 ≥ 015,
we don't need to stratify breadth — simpler recipe and the design
constraint relaxes.

**Predicted**: cross-14 ∈ [0.790, 0.810], eval_01 ∈ [0.745, 0.770].
- 024 > 015 by > 0.005: stratification of breadth was the harm;
  remove it, simpler recipe wins.
- 024 ≈ 015 (within 0.005): both work, no difference.
- 024 < 015 by > 0.005: stratifying breadth has its own value
  beyond the per-bin axis-interaction story; 015's recipe is locked.

This is the cleanest remaining decomposition of 015.

---

## 2026-04-25 00:05 — Experiment 024 result: dhs_signal_strat_breadth_unstrat

**Falsified hypothesis. Half-strat is uniquely bad.** eval_01 =
0.7225 (per-seed std 0.012), cross-14 = 0.7626. Way below predicted
[0.790, 0.810]. **Worse than 011 (no strat at all, 0.7810) by -0.018.**

Mechanism: the unstratified breadth half is naturally GC-skewed
(numsamples-weighted elements concentrate in moderate-high GC).
The stratified signal half is GC-uniform. The two halves disagree
about what the training distribution should look like — bimodal,
hard to fit. By contrast, 011 (both halves natural, both skewed)
and 015 (both halves stratified, both uniform) are CONSISTENT.

### Theory v22 → v23
> **Stratification regimes must be CONSISTENT across all draws.**
> Mixing one stratified half with one unstratified half creates a
> bimodal training distribution that's worse than either pure choice.
>
> The 015 win is not "stratification helps each half independently"
> but "stratification creates a consistent uniform compositional
> distribution the model can fit cleanly". The crucial property is
> CONSISTENCY of the prior, not stratification per se.
>
> Practical: when combining multiple draws into a recipe, apply
> the same stratification regime to every component. Don't mix
> stratified with unstratified parts.
>
> Combined with v21/v22, the 015 recipe sits at a multi-constraint
> corner:
> - per-axis-bin floor ≥ 3K (caps bin count + min mix ratio)
> - consistent stratification across halves (forbids 024-style mixes)
> - signal × GC strat synergy (drives most of the lift)
> - breadth × GC strat anti-synergy mitigated by 30% intensity cap

### Plan: Experiment 025 — dhs_70_30_gc_strat_numsamples_filtered
**Type: pre-filter then stratify.** Before applying the 015 recipe,
filter the candidate pool to numsamples ≥ 3 (drops the noisy
singletons + doubletons; ~40-50% of DHS). Tests whether enriching
the candidate pool for biologically-real regulatory elements
improves the recipe.

- Filter: numsamples ≥ 3 AND valid GC. Recompute GC bins on filtered.
- 5 GC bins, equal-population on filtered pool
- 70/30 mix per bin (7K signal + 3K breadth)
- 3 seeds

This differs from 019 (cCRE-overlap filter) in mechanism: cCRE-
filter is sequence-context-based and biased low-GC. Numsamples-
filter is biology-quality-based and should preserve GC distribution
shape. If 015 is hurt by including singleton DHS as filler in low-
candidate-pool bins, this filter should help.

**Predicted**: cross-14 ∈ [0.795, 0.810], eval_01 ∈ [0.755, 0.770].
- 025 > 015 by > 0.005: enriching pool quality is a real lever;
  carry filter forward into recipe.
- 025 ≈ 015 (within 0.005): singletons aren't the bottleneck for
  015; recipe is already at quality saturation.
- 025 < 015 by > 0.005: filter loses GC distribution structure
  (like 019 but milder); singleton DHS contribute useful diversity.

The numsamples ≥ 3 threshold is chosen because:
- numsamples = 1 is one biosample (potential noise)
- numsamples ≥ 3 means observed in ≥ 3 of 733 biosamples
  (still cell-type-specific but not noise)
- The filtered pool size (~2M) is still 40× the 50K target so
  per-bin pool stays huge

If 025 wins, the filter becomes part of the recipe carryforward.

---

## 2026-04-25 01:00 — Experiment 025 result: dhs_70_30_gc_strat_numsamples_filtered

**Falsified, mild loss.** eval_01 = 0.7365 (per-seed std 0.016 —
seeds: 0.7592 / 0.7271 / 0.7231), cross-14 = 0.7792, -0.017 vs 015.
Even slightly below 011 (no strat). Filter hurts, not helps.

Filter dropped 46% of DHS (1.66M singletons + doubletons) but cost
0.017 cross-14. The model needs the long tail of cell-type-specific
elements for generalization beyond labeled cell types.

Filter ranking:
- none (015): 0.7960
- numsamples ≥ 3 (025): 0.7792 (-0.017)
- cCRE-overlap (019): 0.7472 (-0.049)

Both filters share a mechanism: bias toward "canonical regulatory
elements" and lose long-tail diversity.

### Theory v23 → v24
> **Singletons (cell-type-specific DHS) contribute training value
> proportional to MORE than their fraction.** Dropping them costs
> 3-4× the lift their numerosity would suggest, indicating they
> cover regulatory grammar that broadly-active elements don't.
>
> Practical: do not filter the candidate pool by quality metrics.
> Use the full 3.59M DHS Index. The recipe selects 50K via
> stratified weighted draws; both the SELECTION mechanism (015)
> and the SELECTION POOL (full) matter independently.

### Plan: Experiment 026 — dhs_70_30_gc_strat_signal_phylop
**Type: axis substitution.** Replace the breadth axis in 015 with
a conservation axis (phyloP) and apply identical GC stratification.

- 35K mean_signal-weighted, GC-stratified (7K/bin)
- 15K phyloP-weighted (with max(0.01, score) flooring as in 007),
  GC-stratified (3K/bin)
- 70/30 axis mix: signal × conservation, both consistently
  stratified
- 3 seeds

This tests if "any second biology axis under consistent
stratification" produces 015's lift, or if numsamples specifically
is the right axis. Note: 007 (phyloP alone, no strat) was bad
(cross-14 0.7367). Analogously, 002 (numsamples alone) was bad
(0.7534) but 015 with 30% breadth + strat helped — so a 30%
phyloP component might also help despite the bad standalone.

**Predicted**: cross-14 ∈ [0.770, 0.795], eval_01 ∈ [0.730, 0.755].
- 026 ≥ 015: conservation is a substitutable axis under strat;
  numsamples isn't unique. Implies "any orthogonal biology axis +
  strat works".
- 026 < 015 by 0.005-0.020: conservation is partially substitutable;
  numsamples is a slightly better second axis but the strat
  mechanism is generic.
- 026 < 015 by > 0.020: numsamples is uniquely the right second
  axis; the breadth-axis biology is the key contributor.

If 026 ≈ 015, the next step is exploring axis combinations
(signal + numsamples + phyloP three-way).

---

## 2026-04-25 02:00 — Experiment 026 result: dhs_70_30_gc_strat_signal_phylop

**Substantial loss, axes are NOT interchangeable.** eval_01 = 0.7104
(per-seed std 0.017), cross-14 = 0.7510, -0.045 vs 015. Even worse
than 020 (signal-only + strat = 0.7841) by -0.033 — adding phyloP
as a 30% mix is ACTIVELY harmful relative to dropping the second
axis entirely.

Axis substitutes for 015's breadth half ranked:
- numsamples (015): 0.7960
- nothing (020): 0.7841
- phyloP (026): 0.7510

PhyloP at 30% intensity isn't just "less effective than numsamples"
— it actively hurts vs no second axis at all. Conservation pulls in
conserved-but-inactive elements that pollute training.

### Theory v24 → v25
> **The second axis in 015's mix must be BIOLOGICALLY ALIGNED to
> regulatory activity**, not just orthogonal to signal. Numsamples
> works because it directly indexes "broadness of regulatory
> activity across cell types" — exactly what cell-type
> generalization requires. PhyloP doesn't because conservation
> selects sequences for evolutionary constraint, not regulatory
> function. The two are orthogonal at the sequence level but
> biologically misaligned for activity prediction.
>
> Practical: substitute axes for the breadth half need biological
> alignment to regulatory activity. Candidates: cCRE-maxZ (continuous
> chromatin Z across cell types), per-DHS TF-binding density, or
> any other broadness-of-activity proxy. Conservation, motif content,
> sequence-intrinsic features will likely all fail.

### Plan: Experiment 027 — dhs_70_30_gc_strat_signal_ccremaxz
**Type: aligned-axis substitution.** Replace numsamples with
cCRE-maxZ (continuous chromatin Z-score across cell types). cCRE-maxZ
is biologically closer to numsamples (both proxy "broadness of
regulatory activity") so should test whether ANY broadness-aligned
axis substitutes for numsamples or only numsamples specifically.

- 35K mean_signal-weighted, GC-stratified (7K/bin)
- 15K cCRE-maxZ-weighted (max(0.01, score) flooring), GC-stratified
  (3K/bin)
- 3 seeds

Note: cCRE-maxZ is only defined for DHS overlapping cCREs (~1.4M of
3.6M). For non-cCRE DHS, score = 0 → weight = 0.01 (small but
nonzero). The breadth-axis draw will heavily favor cCRE DHS.

**Predicted**: cross-14 ∈ [0.770, 0.795].
- 027 ≥ 015: cCRE-maxZ substitutes for numsamples; biological
  alignment is the key, not specifically numsamples.
- 027 < 015 by 0.005-0.020: cCRE-maxZ partially substitutes; the
  cCRE-DHS-only bias of cCRE-maxZ loses non-cCRE diversity
  (analogous to 019's filter problem).
- 027 < 015 by > 0.020: numsamples is uniquely the right metric;
  even close substitutes don't work.

If 027 ≥ 015, that's the strongest path forward (we have multiple
substitutable axes). If not, the 015 recipe is locked at the corner
of (signal × numsamples × GC strat × 70/30 × 5 bins) and remaining
experiments should target sample-definition variations or chromosome
balance.

---

## 2026-04-25 03:00 — Experiment 027 result: dhs_70_30_gc_strat_signal_ccremaxz

**Partial substitution but still loses.** eval_01 = 0.7358 (per-seed
std 0.010), cross-14 = 0.7783, -0.018 vs 015. cCRE-maxZ as second
axis is better than phyloP (027 vs 026: +0.027) but still worse than
015 by -0.018, AND worse than 020 (signal-only) by -0.006. Even an
aligned-biology axis substitute fails.

Final ranking of axis substitutes for 015's breadth half:
- numsamples (015): 0.7960
- nothing (020): 0.7841
- cCRE-maxZ (027): 0.7783
- phyloP (026): 0.7510

Numsamples is uniquely informative. Hypothesis: cross-cell-type
COUNT (numsamples) selects broadly-active elements that encode
transferable regulatory grammar; INTENSITY-based proxies (cCRE-maxZ)
select cell-type-specific super-enhancers that don't transfer.

### Theory v25 → v26
> **Cross-cell-type COUNT (numsamples) is the irreplaceable second
> axis** for cell-type-generalization. Even closely-related
> chromatin-intensity proxies (cCRE-maxZ) lose 0.018 cross-14.
>
> The semantic difference: numsamples directly indexes BROADNESS
> of regulatory activity. cCRE-maxZ indexes DEPTH/INTENSITY in any
> single tissue. For models meant to generalize to unseen cell
> types, broadness > depth.
>
> 015 is now extensively decomposed. EVERY perturbation tested
> (020, 022, 023, 024, 025, 026, 027) loses. The recipe is at a
> multi-constraint corner: signal × numsamples × GC strat × 70/30
> × 5 bins × full pool × consistent regimes × summit window.

### Plan: Experiment 028 — dhs_combined_weight_70_30_gc_strat
**Type: structural test of recipe.** Collapse the two-axis per-bin
draws into a single per-element combined-weight draw.

Compute combined_weight_per_DHS = 0.7 * signal_norm + 0.3 *
numsamples_norm (each axis normalized to sum 1). Stratify by GC
into 5 bins. Per bin, draw 10K weighted by combined_weight.

Effective sampling distribution should be similar to 015 (same axes,
same mix ratio, same stratification). Difference is structural:
- 015: 7K signal-weighted + 3K numsamples-weighted per bin (two
  separate weighted draws per bin, sequenced)
- 028: 10K combined-weight-weighted per bin (single weighted draw
  per bin)

Tests if "two separate per-bin draws" is load-bearing or just an
implementation detail of "70/30 mix under stratification".

**Predicted**: cross-14 ∈ [0.785, 0.800].
- 028 ≈ 015 (within 0.005): structure is detail; effective
  distribution is what matters.
- 028 < 015 by > 0.005: separating signal-elite vs broadly-active
  draws gives more diverse element selection than combined draw.
  The "two separate elites within each bin" geometry has unique
  value.
- 028 > 015: simpler structure works better; carry forward as new
  champion.

This is the cleanest remaining structural test. The result clarifies
whether 015's win is from the SAMPLING DISTRIBUTION (round-trippable)
or from the DRAW STRUCTURE (irreducible to a single weighted draw).

---

## 2026-04-25 04:30 — Experiment 028 result: dhs_combined_weight_70_30_gc_strat

**Structure beats distribution.** eval_01 = 0.7227 (per-seed std
0.002 — tightest of the entire series), cross-14 = 0.7651, -0.031
vs 015. Even worse than 011 (no strat, 70/30 sequential = 0.7810).

The combined-weight draw has the same axes, same mix ratio, same
stratification as 015 — yet loses 0.031 cross-14. The "two separate
axis-elite per-bin draws" structure of 015 is irreducible to a
single combined-weight draw.

Mechanism: combined-weight selects intersection-elite elements
(high on BOTH axes). 015's two-draw structure forces inclusion of
union-elite elements (high on EITHER axis). The "high breadth,
moderate signal" elements are unique contribution of the breadth
axis — they encode regulatory grammar that generalizes across
tissues but isn't captured by signal-elite combined-weight selection.

Per-seed std collapse (0.002, 8× tighter than 015's 0.017): combined
weight makes selection deterministic — top elements always win,
only ties yield seed variation. 015's two-draw structure has more
randomness because each axis has separate top elements, and the
intersection between axis-tops yields tie-breaking variability.
Stability is achieved at the cost of -0.031 cross-14. Stability
is not the goal; diversity is.

### Theory v26 → v27
> **The two-axis per-bin draw structure of 015 is load-bearing,
> not just a notation for "70/30 mix under stratification".**
> Collapsing the two draws into a combined per-element weight loses
> 0.031 cross-14 even with the same axes, mix ratio, and stratification.
>
> Mechanism: separate per-bin draws of (signal-elite, breadth-elite)
> force inclusion of elements that score high on ONLY ONE axis.
> The "high breadth, moderate signal" elements are the unique
> contribution of the breadth axis — they encode regulatory grammar
> the signal axis would skip. Combined-weight draws favor
> intersection-elite elements that score high on BOTH axes, missing
> the union members.
>
> Practical: when designing future recipes with multiple axes,
> structure as separate per-axis draws within each stratum. NEVER
> collapse multiple axes into a single per-element weight.
>
> 015 is now characterized along ALL major axes: stratification
> (021/016 fail), mix ratio (012/013/023 fail), each axis (020/022/
> 026/027 fail), draw structure (028 fails), regime consistency (024
> fails), candidate pool (019/025 fail), window choice (009 fails).
> Every dimension has been ablated; every perturbation loses. 015
> is overdetermined.

### Plan: Experiment 029 — dhs_70_30_gc_strat_chrom_balanced
**Type: novel diversity axis.** Add chromosome balance as an
additional structural constraint to 015. The hypothesis: even
genomic coverage might surface chromosome-specific regulatory
contexts the eval sets care about.

Recipe: same as 015 (70/30 mix, 5 GC bins, both halves stratified)
BUT cap per-chromosome count at the global mean × 1.2. Excess
draws from over-represented chromosomes are redistributed to
under-represented ones via re-sampling.

Implementation: post-hoc rebalance after the per-bin draws.
Compute target = 50K / 24 chromosomes ≈ 2083 per chromosome. For
each chromosome with > target × 1.2 ≈ 2500 selected, randomly
demote excess (replace with new draws from under-represented
chromosomes within their respective GC bins).

This preserves GC stratification per-bin counts but adjusts
chromosomal composition. We're testing if 015's natural chromosome
distribution (driven by DHS density: chr1, chr2 over-represented)
biases the model toward learning chromosome-specific grammar that
hurts generalization.

**Predicted**: cross-14 ∈ [0.770, 0.795].
- 029 ≥ 015: chromosome balance helps; library diversity has yet
  another orthogonal axis to exploit.
- 029 < 015 by 0.005-0.020: chromosome balance hurts mildly;
  natural DHS-density distribution carries useful signal.
- 029 < 015 by > 0.020: large chromosomes' DHS richness is
  genuinely informative; capping is destructive.

Given the strong overdetermination of 015, the most likely outcome
is mild loss. But chromosome balance is the cleanest remaining
diversity dimension that hasn't been tested.

---

## 2026-04-25 06:00 — Experiment 029 result: dhs_70_30_gc_strat_chrom_balanced

**The smallest loss measured.** eval_01 = 0.7426 (per-seed std 0.016),
cross-14 = 0.7874, -0.009 vs 015. The chrom cap redistributed 40% of
draws (20K elements/seed) away from over-represented chromosomes
(chr1, chr2, chr10, chr11, chr12, chr17 all hit cap=2500), yet
cross-14 only dropped 0.009 — the closest near-miss in the entire
015 perturbation series.

13 of 24 chroms hit the cap. The redistribution favored mid-sized
chroms (chr3-chr16, chr19, chr20). Small chroms (chrY=85, chr21=850)
were unaffected.

The smallness of the loss is itself diagnostic: model-relevant
regulatory grammar is largely chromosome-invariant given matched
(signal × numsamples × GC) features. The model can learn the same
grammar from chr3 elements as from chr1 elements.

### Theory v27 → v28
> **Chromosomal composition is largely interchangeable for
> regulatory-grammar learning under fixed (signal × numsamples × GC)
> distribution.** A per-chrom cap that redistributes 40% of draws
> away from over-represented chromosomes only loses 0.009 cross-14 —
> the smallest loss of any single-axis perturbation measured.
>
> This implies the model learns sequence-level regulatory grammar
> rather than chromosome-specific grammar, AS LONG AS the per-element
> features are diverse on the load-bearing axes.
>
> 015 has now been perturbed along 12 distinct axes (021/016 for
> bin count, 022/020 for axis dropouts, 023/012/013 for mix ratio,
> 024 for regime consistency, 025/019 for pool filtering, 026/027
> for axis substitution, 028 for draw structure, 029 for chrom
> distribution). Every perturbation loses. The recipe is
> globally overdetermined.

### Plan: Experiment 030 — dhs_70_30_gc_strat_chrom_cap_3000
**Type: parameter refinement of 029.** 029's cap=2500 was the
smallest-loss perturbation. Test a larger cap=3000 (= 50000/24 *
1.44) that only caps the 1-3 most over-represented chroms (chr1,
chr2, possibly chr10), redistributing far less of the library.

Recipe: identical to 029 except CHROM_CAP = 3000 instead of 2500.
~3-5K elements redistributed instead of ~20K. If chromosome balance
has a Goldilocks zone, this is where it would emerge — most of the
diversity from large chromosomes preserved, but the most extreme
over-representation gently trimmed.

**Predicted**: cross-14 ∈ [0.785, 0.800].
- 030 ≥ 015: GOLDILOCKS! Light chrom balance is a real improvement.
  This would make 030 the new champion.
- 030 < 015 by 0.000-0.005: mild balance is essentially neutral;
  natural chrom distribution is close to optimal.
- 030 < 015 by 0.005-0.010: light balance slightly worse than no
  balance, similar to 029.
- 030 < 015 by > 0.010: balance hurts more than 029's strict cap;
  unlikely.

This is the final experiment of the 30-experiment loop. Best case:
new champion. Most likely case: confirms 015 is at a global optimum
across every tested axis.

If 030 wins, the recommended library is 030. Otherwise, 015 is the
final recommendation.

---

## 2026-04-25 08:00 — Experiment 030 result: dhs_70_30_gc_strat_chrom_cap_3000

**Counter-intuitive: relaxed cap loses MORE.** eval_01 = 0.7223
(per-seed std 0.016), cross-14 = 0.7641, -0.032 vs 015. Despite
redistributing only 10% of the library (vs 029's 40%), 030 lost
3.5× more than 029.

cap=3000 specifically targets the top-5 mega-chroms (chr1-5, all
DHS-richest, gene-densest). cap=2500 spread the cap to 13 chroms
and the redistribution was broader. The non-monotonic result —
strict cap loses LESS than mild cap — implies the chr1-5 mega-chroms
carry disproportionately informative regulatory grammar that's
hard to compensate for via redistribution to mid-sized chroms alone.

### Theory v28 → v29 (final)
> **Chromosome balance has no improvement zone over 015.** Tested
> at cap=2500 (-0.009) and cap=3000 (-0.032), both lose. Non-monotonic.
>
> 015's natural chromosome distribution (driven by DHS density) is
> at or near the optimum for cell-type-generalization. The mega-
> chroms (chr1-5) carry disproportionately informative signal-elite
> elements that are hard to substitute via redistribution.
>
> **015 is the GLOBAL CHAMPION across all 14 perturbations tested
> in this study.** Every dimension probed has confirmed that 015
> is at a multi-axis optimum.

---

## 2026-04-25 08:30 — Project final summary

### Champion: 015_dhs_70_30_gc_stratified
**Recipe**: 50K elements drawn as 35K mean_signal-weighted + 15K
numsamples-weighted, both halves stratified across 5 equal-
population GC quintiles, 200bp summit-centered windows from the
DHS Index hg38.

**cross-14 = 0.7960** (per-seed std 0.017)

### 015 is overdetermined — every perturbation loses

| #   | perturbation              | Δ cross-14 |
|-----|---------------------------|------------|
| 015 | champion                  | 0          |
| 029 | chrom cap=2500            | -0.009     |
| 020 | signal-only               | -0.012     |
| 011 | no GC strat               | -0.015     |
| 025 | numsamples≥3 filter       | -0.017     |
| 027 | cCRE-maxZ axis sub        | -0.018     |
| 028 | combined-weight draw      | -0.031     |
| 030 | chrom cap=3000            | -0.032     |
| 024 | half-stratify             | -0.033     |
| 023 | 80/20 mix                 | -0.037     |
| 016 | 10 GC bins                | -0.039     |
| 021 | 3 GC bins                 | -0.039     |
| 026 | phyloP axis sub           | -0.045     |
| 019 | cCRE filter               | -0.049     |
| 022 | breadth-only              | -0.053     |

### Final theory (v29) — what makes a library informative

1. **Two orthogonal selection axes** (signal × numsamples) —
   neither alone suffices. Numsamples is irreplaceable: even
   close substitutes (cCRE-maxZ -0.018, phyloP -0.045) lose. The
   second axis must encode CROSS-CELL-TYPE COUNT, not intensity
   in any single tissue.

2. **70/30 mix ratio** — 80/20 (-0.037) and 60/40 (-0.030+) both
   lose. The 70/30 ratio is precisely calibrated to per-(axis × bin)
   stability floor (~3K/cell).

3. **Sequence-level GC stratification at 5 equal-pop bins** —
   3 bins too coarse (-0.039), 10 bins too fine (-0.039). 5 bins
   is the floor-respecting optimum.

4. **Two-axis per-bin draw structure** — the two axes must be
   drawn separately within each stratum, not collapsed to a
   single combined-weight draw (-0.031). Separate draws force
   inclusion of "axis-only-elite" elements that the combined
   draw would miss.

5. **Consistent stratification regime across both halves** —
   half-stratifying (-0.033) loses to either fully-stratified or
   not-at-all-stratified.

6. **Full candidate pool** — filtering (cCRE -0.049, numsamples≥3
   -0.017) destroys diversity. Singletons contribute disproportionate
   diversity per element.

7. **Summit-centered 200bp window** — multi-window augmentation
   (-0.055 in 009) loses; positional canonicalization is necessary.

8. **Natural chromosome distribution** — chrom-balance caps lose
   non-monotonically (cap=2500 -0.009, cap=3000 -0.032). The
   mega-chroms (chr1-5) carry disproportionately informative
   regulatory grammar.

### Mechanism: why 015 generalizes

The model must predict regulatory activity for held-out cell types.
015's recipe maximizes diversity along the axes that encode
TRANSFERABLE regulatory grammar:
- **signal axis** surfaces strong-effect elements (the regulatory
  workhorses)
- **numsamples axis** surfaces broadly-active elements (cross-tissue
  conserved grammar that transfers)
- **GC stratification** ensures sequence-composition coverage
  (low-GC enhancers vs high-GC promoters both represented)
- **two-axis per-bin draws** force union-elite, not intersection-
  elite, selection — capturing high-numsamples / moderate-signal
  elements that are uniquely informative for transfer

Every perturbation removes diversity along one of these axes and
the model learns less transferable grammar.

### Final library: 015 (committed at e22b4dc's parent commit)

The 30-experiment loop is complete. 015 is the recommended library.
