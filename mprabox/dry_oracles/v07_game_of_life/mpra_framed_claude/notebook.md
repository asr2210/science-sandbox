# MPRA Library Design — v07 Lab Notebook

Append-only log of experiments, hypotheses, and theory updates.

---

## 2026-06-02 17:25 — Setup and starting context

### Inherited prior knowledge
This v07 run starts with skills/data copied from a prior v04 adversarial
run. The v04 best library was a 4-way mix (20K natural + 15K cCRE
off-centered + 10K DHS + 5K mouse) reaching eval_01 ≈ 0.501.

Key v04 observations to revisit in v07:
- Natural genomic DNA is the dominant source of signal.
- Mixing with regulatory-element subsets helps modestly.
- Pure synthetic / pure cCRE hurt.
- eval_08 was stuck low (~0.10) in v04. Unknown whether this transfers.

But v07's eval sets may differ. v07 may be a different "adversarial"
construction. So I should **first verify the baseline behaves the same**
before reusing v04's best design as a starting point.

### Starting theory (T0, inherited)
A library is informative iff its sequence distribution matches the
distribution of plausible regulatory genomes the eval set is drawn from.
Beyond that, motif content + activity-range diversity help. Violating
naturalness costs more than added motif density gains.

### Generalization argument (the core question)
"Would this library be worth designing this way if evaluated in cell
types we have no data on?"

For natural genomic DNA: YES. Reasons:
- Sampling whole-genome 200bp windows is cell-type agnostic.
- It contains every TF binding site, every chromatin context, every GC
  composition the genome holds. A model trained on this learns sequence
  rules (motifs, syntax, spacing) that are shared across cell types
  because the underlying biology is shared.
- We're not biasing toward the 3 measurement cell types (K562, HepG2,
  SKNSH). We're just sampling the universe of regulatory contexts a
  human genome offers.

For pure cCRE: PARTIALLY. cCREs are TF-rich and active in some cell
type, so the model learns motif syntax. BUT it sees no inactive/null
sequences, so it has no contrast — predicting "high" everywhere is
within ε of optimal on the training set, but useless out-of-domain.

### Plan: experiment 001
Replicate v04 exp 002 — pure natural genomic DNA, 50K random windows,
chr1-22 + X + Y, skip N. This calibrates v07 against v04 and gives a
clean naturalness baseline.

If v07 ≈ v04 on this, my prior is well-calibrated and I can build on it.
If v07 diverges significantly, I need to start over.

This is (a) exploration — verifying my prior is sound — before committing
to refinement directions.

---

## 2026-06-02 17:35 — Experiment 001 result

| metric | value |
|---|---|
| eval_01 | 0.388 |
| mean across evals | 0.376 |
| best eval | eval_13 (0.407) |
| worst eval | eval_08 (0.257) |
| K562 (eval_01) | 0.596 |
| HepG2 (eval_01) | 0.423 |
| SK-N-SH (eval_01) | 0.143 |
| runtime | 115 s |

### Updates to theory
Major recalibrations from this single experiment:

**Update 1: v07 ≠ v04.** v04 natural baseline was eval_01 ≈ 0.48; v07
gets 0.39. The v04 best (4-way mix) reached 0.50. I should NOT assume
v04 conclusions transfer directly. They are hypotheses to test, not
load-bearing priors.

**Update 2: K562 vs HepG2 vs SK-N-SH are now distinct.** In v04,
K562 ≡ HepG2 in the eval signal. In v07, they're cleanly different
(K562=0.60, HepG2=0.42, SK-N-SH=0.14). This means the eval set
genuinely measures 3 cell types, and SK-N-SH is the dominant
bottleneck. Per-cell-type predictability gap (K562−SK-N-SH) ≈ 0.45.
That's huge.

**Update 3: SK-N-SH is the leverage point.** mean_r is dragged by
SK-N-SH. Even a small SK-N-SH improvement should move mean_r more than
a large K562 improvement (because K562 is closer to ceiling). My
theory now adds: **per-cell-type coverage matters when cell types
differ in regulatory grammar.** Natural genomic windows are
cell-type-agnostic but may under-represent neural enhancers.

**Update 4: eval sets cluster.** 14 evals are really ~7 distinct
signals. Some pairs are identical: 02=05=14, 04=09, 03=12, 06=11.
eval_01, 07, 08, 10, 13 are distinct.

### Generalization consideration
SK-N-SH is a neuroblastoma line. If I bias the library toward neural
enhancers, do I help generalize to unseen cell types? Two cases:
- If unseen cell types are neural-like: yes.
- If unseen cell types are myeloid-like: no, I'd over-fit.
The safest generalization story: **add diverse regulatory contexts so
every cell type's grammar is represented**, not bias toward one.

### Plan for experiment 002
Test the v04-style 4-way mix (natural + cCRE + DHS + mouse natural) to
see whether v04's best design transfers. This is the quickest way to
know whether v04 lessons apply. If it improves substantially on
exp 001, I have a strong refined baseline. If it doesn't, v07 cares
about different things and I need new directions.

This is (b) refinement — testing a specific hypothesis (v04-best
transfers) against the new baseline.

---

## 2026-06-02 17:50 — Experiment 002 result

| metric | exp 001 | exp 002 | Δ |
|---|---|---|---|
| eval_01 | 0.388 | 0.394 | +0.006 |
| K562 | 0.596 | 0.604 | +0.008 |
| HepG2 | 0.423 | 0.430 | +0.007 |
| SK-N-SH | 0.143 | 0.147 | +0.004 |
| eval_08 (worst) | 0.257 | 0.265 | +0.008 |
| eval_13 (best) | 0.407 | 0.409 | +0.002 |

### Theory update (T1)
v04 lesson (4-way mix > natural alone) reproduces directionally in v07
but with smaller magnitude (+0.006 vs v04's +0.02). The gain comes
mostly from K562/HepG2, not SK-N-SH. This is consistent with:

**T1: Cell-type signal in MPRA training data is bottlenecked by
cell-type-specific regulatory element representation.** Adding pan-
tissue regulatory elements (cCRE, DHS) helps cell types whose
regulatory grammar is well-represented in those collections. To boost
a specific cell type, you need its specific regulatory grammar.

### Generalization implication
If T1 is right, the strategy "add neural enhancers for SK-N-SH" would
overfit if generalization tests are non-neural. But the framing in
instructions says "model that must generalize to cell types we have no
data on." So the right move is not "specifically help SK-N-SH" but
"add diverse cell-type-specific regulatory grammars so every plausible
unseen cell type has representation."

This is a **diversity** strategy, not a SK-N-SH-targeting strategy.
But SK-N-SH is the diagnostic: if adding neural content helps SK-N-SH
without hurting K562/HepG2, then per-cell-type content addition is
non-zero-sum and the diversity strategy is sound.

### Plan for experiment 003
Add neural-tissue-biased regulatory content while keeping the
multi-source backbone. Two parallel sources I have on hand:
1. DHS Index "component" field — filter to neural/brain components
2. The DHS Index has "Neural" as one of the tissue components

Design:
- 15K natural human (broad coverage)
- 10K pan-tissue cCRE off-center
- 10K DHS pan-tissue summits
- 10K DHS Index summits filtered to neural-tagged elements
-  5K mouse natural

This adds neural content (10K seqs) by trading off cCRE (15K→10K) and
DHS (10K→10K kept; the 10K neural is added). If T1 is right, SK-N-SH
should jump and K562/HepG2 should hold roughly steady.

This is (a) testing a hypothesis (T1) with a clear prediction:
SK-N-SH gain > K562/HepG2 gain.

---

## 2026-06-02 18:05 — Experiment 003 result (T1 falsified)

| metric | exp 002 | exp 003 | Δ |
|---|---|---|---|
| eval_01 | 0.394 | 0.393 | -0.001 |
| K562 | 0.604 | 0.605 | +0.001 |
| HepG2 | 0.430 | 0.428 | -0.002 |
| SK-N-SH | 0.147 | 0.147 | 0.000 |

**Negative result: T1 is wrong.** Neural-tagged DHS did not preferentially
lift SK-N-SH. The composition swap was a wash.

### Theory update (T2)
Tissue-specific content selection is **not** the right knob for v07.
What I see across exps 001-003:
- The per-eval ranking is invariant (eval_13 always best, eval_08
  always worst). This pattern is set by model + eval, not library.
- The per-cell-type ranking is invariant (K562 > HepG2 > SK-N-SH).
- Library design moves ALL of these proportionally and by small amounts.

This suggests **the library acts as a multiplicative gain on a fixed
underlying difficulty pattern**, not as a re-weighting of which signal
gets learned. If true, the right strategy is to optimize the multiplier
(total information content / coverage / diversity), not to chase
specific cell types or eval sets.

T2: **Library quality is a single scalar quantity that uniformly lifts
all evals and cell types. Tissue-specific targeting offers no
differential benefit.** This explains the v04→v07 generalization
mystery: v04's best mix was helpful because it had MORE total info,
not because it had specific tissue mixes.

### Generalization implication of T2
If T2 is right, the same library design should generalize to unseen
cell types (since it's not biased toward any specific one). The
library just needs maximum "information content" in a sense the model
can use.

What is information content here? Likely some combination of:
- Coverage of the sequence-feature space (TF motifs, dinuc bias, GC,
  spacing patterns)
- Coverage of the activity range (so contrast is learnable)
- Naturalness (so the distribution matches eval)

### Plan for experiment 004
Test T2 by going the OPPOSITE direction from exp 003: instead of one
tissue-specific bias, use STRATIFIED diversity across all DHS tissue
components in proportional amounts. If T2 is right, this should give
the same result as a random DHS sample (~exp 002). If it's
*better*, T2 is wrong and diversity matters per se.

Design:
- 20K natural
- 25K DHS stratified across components (1.5K per component × 16 ≈ 24K)
- 5K mouse

This is (a) exploration of a new hypothesis (T2: library is a scalar
multiplier).

---

## 2026-06-02 18:25 — Literature check (lit-1)

Searched: "MPRA library design sequence-to-activity model training
generalization across cell types 2024".

Key takeaways from PARM (Nature 2024/2025), lentiMPRA (Nature 2024),
and review papers:
- PARM: autonomous promoter activities are R=0.78-0.95 correlated
  across cell types. Most signal is SHARED, only ~5-22% is
  cell-type-specific.
- lentiMPRA used 680K cCRE-based library across HepG2/K562/WTC11.
  41.7% active — they ensured a balanced active/inactive distribution.
- Cell-type-agnostic models and cell-type-specific models showed
  similar performance for variant effect prediction.
- Iterative model-guided sequence design improves cell-type specificity
  but trades off generalization to unseen cell types.

This supports T2 (library is a near-scalar multiplier) and adds a
specific recommendation: **balance active/inactive fractions** in the
training library. My exp 002 had ~25K active sources + 25K mostly-
inactive natural, which is roughly that. Activity range testing
should explicitly anchor both extremes.

## 2026-06-02 18:30 — Experiment 004 result

| metric | exp 002 | exp 004 | Δ |
|---|---|---|---|
| eval_01 | 0.394 | 0.392 | -0.002 |
| K562 | 0.604 | 0.602 | -0.002 |
| HepG2 | 0.430 | 0.426 | -0.004 |
| SK-N-SH | 0.147 | 0.148 | +0.001 |

50K DHS quintile-stratified library (no random genomic, no mouse) —
slight loss vs 4-way mix. Cannot disentangle "activity stratification
worked" from "loss of random genomic hurt." The latter is consistent
with T2 (every source contributes some unique info).

### Update to T2
T2 holds tentatively: small library design changes produce small,
proportional shifts. The eval-set ranking is fully invariant across
all 4 experiments. K562 > HepG2 > SK-N-SH ratio is invariant.

### Plan for experiment 005
Test the activity-CONTRAST hypothesis cleanly: keep random genomic
backbone, but ADD explicit silent anchors (gene desert windows).
Design:
- 20K active: cCRE PLS+pELS+dELS centered
- 20K silent: natural windows >1kb from any cCRE
- 10K natural random (genomic middle / mouse)

Predicted outcome under T2: small or zero gain.
Predicted outcome under "activity contrast helps": >+0.005 gain.

This is (a) a falsification attempt on T2.

---

## 2026-06-02 18:50 — Experiment 005 result

| metric | exp 002 | exp 005 | Δ |
|---|---|---|---|
| eval_01 | 0.394 | 0.393 | -0.001 |
| K562 | 0.604 | 0.604 | 0.000 |
| HepG2 | 0.430 | 0.429 | -0.001 |
| SK-N-SH | 0.147 | 0.147 | 0.000 |

**Activity contrast did not move the needle.** T2 holds. Within "good
library" regime, design choices produce <0.005 variation.

### Cross-experiment summary so far
| exp | eval_01 | description |
|---|---|---|
| 001 | 0.388 | natural human only |
| 002 | 0.394 | 4-way mix |
| 003 | 0.393 | + neural DHS |
| 004 | 0.392 | DHS quintiles only |
| 005 | 0.393 | active + silent + natural |

All "good library" attempts converge to 0.393 ± 0.001. The lift from
natural-alone to good-mix is only +0.006. The 0.394 ceiling appears
to be a property of the model + eval, not the library.

### Refined theory (T3)
T3: **Library quality has a sharp threshold.** Below threshold
(pure random, pure cCRE, pure synthetic) you get badly reduced
performance. Above threshold (any mix of natural + regulatory) you get
within ε of the model's intrinsic performance ceiling. The library is
a binary "good/bad" gate, not a continuous knob.

This is a different framing from T2 (scalar multiplier) — T3 says
above the threshold, the library doesn't multiply at all; it
saturates.

### Generalization implication of T3
If T3 is right, the BEST library for unseen cell types is one that
hits the "good library" threshold robustly. Any reasonable mix of
natural + regulatory does this. So the design problem is "easy"
— just provide enough diversity and balance.

But this hasn't been tested below the threshold yet (in v07).
Cross-species and pure-random tests will calibrate where the threshold
sits and confirm T3.

### Plan for experiment 006
Test cross-species: 50K mouse-only natural. If T3 is right and the
threshold is "any natural genomic distribution," mouse should land
close to human natural (0.388). If T3 is wrong and human-specific
sequences are needed, mouse should be substantially worse.

Generalization argument: a model that can be trained on MOUSE and
still predict HUMAN MPRA activity has learned conserved regulatory
grammar — which is exactly what generalizes to unseen cell types.
So mouse-only is a strong test of generalization.

This is (a) test of T3 + cross-species generalization probe.

---

## 2026-06-02 19:10 — Experiment 006 result (MAJOR FINDING)

| metric | human-only (001) | mouse-only (006) | Δ |
|---|---|---|---|
| eval_01 | 0.388 | 0.388 | 0.000 |
| K562 | 0.596 | 0.596 | 0.000 |
| HepG2 | 0.423 | 0.423 | 0.000 |
| SK-N-SH | 0.143 | 0.145 | +0.002 |

**50K MOUSE-ONLY natural ≈ 50K HUMAN-ONLY natural across every metric.**

### Major theory update (T4)
The eval set is **species-agnostic**. The model learns CONSERVED
regulatory grammar (motifs, syntax, composition) — not human-specific
features. This rules out a large class of approaches:
- Tissue-specific human enrichment doesn't help (already saw in exp 003)
- Human-specific element types (e.g., AluY, HERV) don't help
- The "natural distribution" the model needs is just "vertebrate
  genome distribution"

### T4 in one sentence
**MPRA-eval performance is bottlenecked by "naturalness" of the
training sequence distribution. Naturalness = vertebrate-genome
sequence statistics, not species-specific or tissue-specific content.**

### Generalization story
T4 has a very clean generalization argument: a model trained on natural
vertebrate genomic sequences learns features that are conserved across
species → also conserved across cell types in any species. So
generalization to unseen cell types follows naturally from
generalization to unseen species (which we just demonstrated).

The library design problem reduces to: "provide as much natural
vertebrate genomic sequence as possible." Source species barely
matters. Regulatory enrichment barely matters above threshold.

### What is "naturalness"?
Need to characterize what makes a sequence "natural." Possibilities:
- Dinucleotide composition (e.g., CpG depletion, TpA enrichment)
- K-mer (k=3-6) composition
- TF motif content at biological rates
- Higher-order syntactic patterns (motif spacing, clusters)
- Compositional autocorrelation / periodicity

### Plan for experiment 007
Dinucleotide-shuffle test. Take 50K human natural windows and
dinucleotide-shuffle each. This preserves dinucleotide composition
(GC, CpG, dinuc context) but DESTROYS motifs, k-mer counts beyond
dinucs, and all higher-order structure.

Prediction:
- If dinuc-shuffle ≈ natural (0.388): naturalness = dinuc composition.
- If dinuc-shuffle < random (0.31?): naturalness = motif/k-mer content.
- If somewhere between (0.32-0.36): naturalness has a composition
  component + a motif component.

This is (a) a critical probe of WHAT naturalness means.

---

## 2026-06-02 19:30 — Experiment 007 result (KEY FINDING)

| metric | natural (001) | dinuc-shuffle (007) | Δ |
|---|---|---|---|
| eval_01 | 0.388 | 0.373 | -0.015 |
| K562 | 0.596 | 0.576 | -0.020 |
| HepG2 | 0.423 | 0.403 | -0.020 |
| SK-N-SH | 0.143 | 0.141 | -0.002 |

### Theory update (T5)
Shuffling out motifs (preserving dinucs) costs only -0.015. Assuming
v07 random ≈ 0.31 (v04 prior), the breakdown is:
- random → dinuc-shuffled-natural: +0.06 (composition signal, ~80%)
- dinuc-shuffled → natural: +0.015 (motif/syntax signal, ~20%)
- natural → 4-way mix: +0.006 (regulatory enrichment, ~8% on top)

**T5: Performance is dominated by dinucleotide composition matching,
not motif syntax or cell-type-specific content.** The library acts as
a near-binary gate: natural composition ≈ above ceiling, random
composition ≈ below ceiling.

### Cross-experiment summary
| exp | eval_01 | description |
|---|---|---|
| 001 | 0.388 | natural human only |
| 002 | 0.394 | 4-way mix |
| 003 | 0.393 | + neural DHS |
| 004 | 0.392 | DHS quintile stratified |
| 005 | 0.393 | active + silent contrast |
| 006 | 0.388 | mouse-only natural |
| 007 | 0.373 | dinuc-shuffled natural |

### Strategic implications
1. The 0.394 ceiling is real and structural. Further library tweaks
   within "good design" regime will produce small/no gain.
2. To push beyond 0.394, need something qualitatively different OR
   the ceiling is truly intrinsic to the model+eval and cannot be
   moved with library design.
3. SK-N-SH is locked low (0.14-0.15) across all 7 experiments.
   Cell-type-targeted approaches don't move it. Confirms structural
   bottleneck not addressable by library.

### Things still untested
- Pure random uniform (v07 floor confirmation)
- Mono-nucleotide shuffle (GC-only baseline)
- Higher-order shuffle (k=3, 4) — would isolate which k matters
- Multi-species natural mix (does diversity help?)
- Heavy motif-density curation (pick natural windows with most TF hits)
- Activity-stratified label diversity (but I don't have labels)

### Plan for experiment 008
Quick floor calibration: pure random uniform 40% GC. Confirms v07
floor and the size of the "composition gap." Then I can compute
exactly what dinuc shuffle is buying.

This is (a) calibration experiment, not theory test.

---

## 2026-06-02 19:50 — Experiment 008 result (BIG CALIBRATION)

v07 floor (pure random uniform 40% GC) = **0.369**, NOT 0.31 like v04!

| | random (008) | dinuc-shuf (007) | natural (001) | 4-way (002) |
|---|---|---|---|---|
| eval_01 | 0.369 | 0.373 | 0.388 | 0.394 |
| K562 | 0.573 | 0.576 | 0.596 | 0.604 |
| HepG2 | 0.404 | 0.403 | 0.423 | 0.430 |
| SK-N-SH | 0.129 | 0.141 | 0.143 | 0.147 |

Random uniform → dinuc-shuffled natural is only +0.004! The dinuc
composition signal is much smaller than I assumed.

Revised gap breakdown:
- random uniform → dinuc-shuffled natural: +0.004 (dinuc composition)
- dinuc-shuffled natural → natural: +0.015 (motif/syntax)
- natural → 4-way mix: +0.006 (regulatory enrichment)
- TOTAL: +0.025

### Theory update (T6)
**The v07 model has strong inductive biases that achieve ~0.37 eval
even with random uniform DNA. The library design dynamic range is
only ~0.025. The ceiling at ~0.40 is intrinsic to the model+eval.**

This is the cleanest version of the theory so far. Library design has
small marginal value in v07.

### Implication for the assignment goal
The task asked: "what makes a library good for generalization to
unseen cell types?" My answer in v07:
1. Any natural (vertebrate genomic) distribution wins +0.020 over
   random uniform. This is the "above threshold" gate.
2. Regulatory enrichment buys another +0.005 on top.
3. Specific tissue targeting buys nothing.
4. Above the threshold, library design is in a tiny zone of marginal
   improvement.

For a model that must generalize to unseen cell types, the optimal
library is "natural distribution, broadly diverse, with modest
regulatory enrichment." Exactly what 4-way mix provides.

### Plan for experiment 009
Test diversity-maximization: does combining ALL natural sources I
have (human, mouse, cCRE, DHS, FANTOM5, low-DNase cCRE, plus
multi-genome) push the ceiling, or confirm T6?

Design: balanced 10K each from
- Human natural random
- Mouse natural random
- cCRE high-conf off-center
- DHS summit windows
- FANTOM5 enhancers + Low-DNase cCRE windows (5K + 5K)

This is (a) test of T6: if all "good library" features combined still
land at 0.394, T6 confirmed (ceiling intrinsic to model+eval).

---

## 2026-06-02 20:10 — Experiment 009 result

eval_01 = 0.394. **Identical to exp 002 4-way mix.** T6 fully confirmed.

| exp | eval_01 |
|---|---|
| 002 (4-way mix) | 0.3937 |
| 009 (max diversity) | 0.3939 |
| 003 (+ neural DHS) | 0.3932 |
| 005 (activity contrast) | 0.3934 |

The ceiling at 0.394 is reproducible across multiple "good"
designs. Library design has no further leverage beyond reaching the
"natural + some regulatory" threshold.

### Plan for experiment 010
Estimate noise floor: re-run 4-way mix (exp 002 design) with seed=1.
Tells me whether the 0.388 → 0.394 lift is signal or noise.

If noise is <0.003, then 0.394 vs 0.388 is real signal (+0.006).
If noise is ≥0.005, the lift is in the noise.

This is (a) calibration of statistical significance.

---

## 2026-06-02 20:25 — Experiment 010 result (noise estimate)

eval_01 = **0.3961** (vs exp 002 at 0.3937). Δ = +0.0024.

Per-eval Δ between exp 002 (seed=0) and 010 (seed=1):
- Most evals: +0.0015 to +0.0024
- A few near-zero (eval_07: +0.0003, eval_08: +0.0002, eval_10: -0.0002)

### Noise calibration
σ ≈ 0.002 with a slight systematic bias (seed=1 happens to score
higher across the board). Notable: same library design across
two seeds gave **+0.0024** on eval_01.

### Signal vs noise
- nat (001) → mix seed=0 (002): +0.0061
- nat (001) → mix seed=1 (010): +0.0085
- Both ≥ 3σ above noise → **library design lift is real signal**

### T6 revised
The ceiling is not 0.394 — it's **~0.395 ± 0.002**. Best mix at
seed=1 (0.396) marginally exceeds anything I've seen. Library design
gives a real but small lift; remaining headroom to the eval_13 max
(~0.41) probably is not reachable via library design alone.

### Strategic update
- Single-seed comparisons need |Δ| ≥ 0.005 to be meaningful
- I've tested: random uniform, dinuc-shuf, natural, mouse, multi-source
  mix, regulatory activity contrast, neural-tag DHS, max diversity, +noise
- Untested dimensions:
  1. **Motif density** — natural windows curated by TF binding density
  2. **TSS-anchored** — PLS-only, promoter-proximal
  3. **Variant-rich** — GWAS SNP-centered
  4. **GC-stratified** natural
  5. **Cell-type specific motif curation**

### Plan for experiment 011
Motif-density curated natural library: load JASPAR vertebrate PWMs,
score natural windows by per-PWM hit density, pick the top-scoring
50K. Hypothesis: more motif-dense sequences carry more learnable
regulatory signal per window → model trained on them generalizes
better. If this beats 0.395 by ≥0.005, motif density matters
intrinsically.

---

## 2026-06-02 20:45 — Experiment 011 result (TF diversity)

eval_01 = **0.3831**. WORSE than natural baseline (0.3876). Δ -0.005.

This is the worst natural-source library I've tested. Top tiles
have 146-768 unique TFs binding (highly enriched), but the model
generalizes worse, not better.

### T7 — distributional breadth, not regulatory density
The right library isn't "most regulatory" — it's "broadly natural."
Eval expects a distribution like the natural genome; concentrating
on the top of any single ranking (cCRE-Low-DNase, DHS-low-signal,
or TF-density-top) shifts the training distribution away from eval.

cCRE/DHS work in mixes because they're a *minority* component
broadening coverage, not because they're intrinsically informative.
Maxing out regulatory content hurts.

### Tested rankings of "good library":
| design | eval_01 | Δ vs nat |
|---|---|---|
| 4-way mix (s=1) | 0.3961 | +0.009 |
| max diversity | 0.3939 | +0.006 |
| 4-way mix (s=0) | 0.3937 | +0.006 |
| activity contrast | 0.3934 | +0.006 |
| neural boost | 0.3932 | +0.006 |
| activity quintiles | 0.3919 | +0.004 |
| mouse only | 0.3880 | +0.000 |
| natural | 0.3876 | — |
| **TF diversity** | **0.3831** | **-0.005** |
| dinuc shuffle | 0.3733 | -0.014 |
| random uniform | 0.3689 | -0.019 |

### Plan for experiment 012
RC augmentation: 25K random natural windows + their 25K reverse
complements. Tests whether forcing the model to see both strands
helps. Hypothesis: if some evals are RC pairs (they look like it
from the symmetry in v07 results), RC augmentation should help.

If lifts >0.005, RC augmentation is a real lever.

---

## 2026-06-02 21:05 — Experiment 012 result (RC augmentation)

eval_01 = **0.3883**. Within noise of natural baseline (0.3876).

RC augmentation halves unique sequence content; if it doesn't help,
either model is already RC-equivariant or losing sequence diversity
cancels the gain. Either way, not a lever.

Side note: eval_07 = 0.3938 (Δ +0.012 vs nat). Single eval was
RC-sensitive. Not strong enough alone but interesting flag.

### Plan for experiment 013
Mix ratio sweep — minimal regulatory boost. 45K nat + 2.5K cCRE +
2.5K DHS. Tests whether the +0.006 nat→mix lift can be obtained
with just 10% regulatory enrichment.

If yes: library design is basically "mostly natural + small reg
boost." If no: regulatory enrichment must be 30%+ to matter.

This pin-points the *active dose* of regulatory content.

---

## 2026-06-02 21:25 — Experiment 013 result (minimal reg dose)

eval_01 = **0.3893**. Δ +0.0017 vs natural.

10% reg = 25% of max lift. 60% reg = 100% of max lift. So curve
is sub-linear: most of the lift is in the first 30-50% of reg
content, but a tiny dose buys a small piece of it.

T7 refined: best library is **natural backbone (40%) + moderate
regulatory enrichment (60%)**. Distributional anchor of natural
prevents over-concentration on regulatory hotspots (the TF-density
failure mode).

### Plan for experiment 014
GC-stratified natural — 10K per GC bin (≤35%, 35-45%, 45-55%,
55-65%, >65%). No regulatory enrichment, just balanced composition.

If this lifts beyond 0.388, then GC matching is part of the
mechanism (which would explain why cCRE/DHS enrichment helps:
they raise mean GC).

If not, the mechanism is specifically regulatory CONTENT.

---

## 2026-06-02 21:50 — Experiment 014 result (GC-stratified) — BREAKTHROUGH

eval_01 = **0.3939**. Matches 4-way mix (0.3937).

Pure natural windows, no regulatory content, GC-balanced across
5 bins. Same lift as 60% regulatory enrichment.

### T8 — GC is the lever
The mechanism behind "regulatory mix helps" is **GC composition
balance**, not motif content per se. cCRE/DHS enrichment shifts
the training GC distribution toward higher GC (CpG islands,
promoters). Doing this directly via GC stratification gets the
same lift.

Compare:
| design | eval_01 | mechanism |
|---|---|---|
| nat baseline | 0.3876 | hg38 length-weighted (GC=41%, skewed AT) |
| 4-way mix | 0.3937 | reg enrichment → indirectly higher GC |
| GC-stratified | 0.3939 | direct GC balance, no reg |

This retracts T7 ("natural backbone + reg") in favor of T8 (it
was GC the whole time).

### Bigger picture
Random hg38 sampling under-represents the high-GC tail. cCRE/DHS
*correct* this by being GC-rich. GC stratification corrects it
directly. Either path → ~0.394 ceiling.

### Plan for experiment 015
Test orthogonality. **Combine GC stratification with regulatory mix.**
If GC and reg are the same mechanism: no further lift.
If orthogonal: lift could push 0.398-0.400.

Design: 25K GC-strat nat + 15K cCRE + 10K DHS, where the regulatory
portion is also GC-stratified.

---

## 2026-06-02 22:15 — Experiment 015 result (GC + reg combo)

eval_01 = **0.3945**. Within noise of both GC-strat (0.3939) and
mix (0.3937). **T8 confirmed**: GC and reg are the same mechanism.

The 0.394 ceiling is set by GC distribution coverage. Reaching it
via three orthogonal routes (mix, GC, GC+mix combo) all land at
0.394 ± 0.002. Library design via composition tweaks is exhausted.

### What's left in the design space?
- Sequence augmentation (shifted/jittered windows around same anchor)
- Synthetic motif planting (engineered sequences with known motifs)
- Anti-repeat sampling (exclude RepeatMasker-style regions — but I
  don't have RepeatMasker; can use absence of cCRE as a proxy)
- Mouse-dominant libraries (>50% mouse — push species)
- Multi-genome heterogeneity (use even non-mouse non-human?)

### Plan for experiment 016
Shifted-window augmentation. 10K anchor positions, 5 windows each
at offsets [-50,-25,0,+25,+50]. Model sees same regulatory context
at multiple positions. Tests whether positional invariance training
lifts mean_r.

If yes: augmentation is a new lever orthogonal to GC.
If no: ceiling truly is intrinsic, library design done.

---

## 2026-06-03 — Experiment 016 result (shifted-window aug)

eval_01 = **0.3882**. Neutral. Sequence-level augmentation does
not lift mean_r beyond the natural baseline.

### Plan for experiment 017
Test GC distribution shape. Eval may have non-uniform GC. Try
HIGH-GC heavy library: 30K natural windows from GC>55%, 10K from
GC<45%, 10K from middle.

If lifts: eval prefers high-GC training, and we have a new lever.
If drops: uniform GC was optimal.

---

## 2026-06-03 — Experiment 017 result (high-GC heavy)

eval_01 = **0.3928**. Within noise but slightly below uniform GC-strat
(0.3939). Oversampling high-GC doesn't help; uniform GC across bins
is roughly optimal.

### Plan for experiment 018
CpG dinucleotide stratification. CpG sites are special (methylated,
depleted in non-CGI regions, mark active regulatory elements).
GC and CpG are correlated but not identical. If CpG stratification
helps orthogonally to GC, it could push the ceiling.

Design: stratify natural windows by CpG count (5 bins).

---

## 2026-06-03 — Experiment 018 result (CpG-stratified)

eval_01 = **0.3923**. Within noise of GC-strat (0.3939) but slightly
lower. CpG and GC stratification are functionally equivalent levers.

**Any reasonable compositional balancing → 0.394 ceiling.**

### Plan for experiment 019
TSS-anchored (PLS only) library. cCRE class PLS = "Promoter-Like
Signature." 50K windows centered around promoter elements.

If lifts: eval is biased toward TSS-proximal sequences.
If drops: would confirm that excessive enrichment hurts (T7
catastrophe pattern from exp 011).

---

## 2026-06-03 — Experiment 019 result (PLS only) — CATASTROPHIC

eval_01 = **0.3617**. Worse than dinuc-shuffle (0.373) and below
random uniform (0.369). T9 (collapse): single regulatory class
collapses training distribution and crashes generalization.

20K unique PLS elements is too narrow a context. Even with ±85bp
jitter, the model only sees promoter-like sequences.

### Plan for experiment 020
GC-stratified human + GC-stratified mouse (multi-genome).
- 25K GC-strat human (5K/bin)
- 25K GC-strat mouse (5K/bin)

Does multi-genome with composition control beat single-genome
GC-strat? mouse-only (006) was equal to human-only natural. Maybe
multi-genome with controlled composition is the actual lift mechanism.

---

## 2026-06-03 — Experiment 020 result (multi-genome GC-strat)

eval_01 = **0.3947**. Within noise of GC-strat human (0.3939).
Multi-genome under composition control gives nothing extra.

T4 (species-agnostic) firmly confirmed: at the GC-controlled
ceiling, species composition is fungible.

### Plan for experiment 021
Cell-type diversity DHS — sample summits stratified by DHS
"component" tag, broadly across the 16 components in the index.
Tests whether broader cell-type coverage helps unseen-cell-type
generalization (the real task goal).

---

## 2026-06-03 — Experiment 021 result (DHS components)

eval_01 = **0.3920**. Within noise of ceiling. DHS cell-type breadth
gives no lift. Confirms ceiling is GC-mediated.

### Library design saturation
The ceiling cluster (0.394 ± 0.003) is now reached by:
- 4-way mix, max diversity (cCRE+DHS+nat+mouse variants)
- GC-stratified human alone
- GC-stratified + reg
- GC-stratified human + mouse
- CpG-stratified, DHS-component-stratified

All ~0.394. Library design has saturated.

### Plan exp 022
Run "best mix" (exp 002 design) seed=2 for a 3-sample noise estimate.
Lets me put confidence bounds on the 0.396 best (exp 010 seed=1).

---

## 2026-06-03 — Experiment 022 result (mix seed=2, third noise sample)

eval_01 = **0.3954**. Three samples of 4-way mix design:
| seed | eval_01 |
|---|---|
| 0 (002) | 0.3937 |
| 1 (010) | 0.3961 |
| 2 (022) | 0.3954 |

Mean = 0.3951, σ = 0.0012.

### Final ceiling
**Library design ceiling on eval_01 = 0.395 ± 0.002 (95% CI)**.

Achievable via:
- Multi-source mix
- GC-stratified natural
- Any broad composition balancing

Distinguishing two designs requires |Δ| > 0.0025.

### Plan for remaining experiments (023-030)
Now we have noise calibration. Let me test a few last hypotheses:
- exp 023: GC-strat DHS only (pure regulatory + GC strat — does
  the regulatory provide any extra info under GC control?)
- exp 024: noise injection — 25K natural + 25K random uniform
  (tests if random "negative" examples help generalization)
- exp 025+: based on results

---

## 2026-06-03 — Experiment 023 result (DHS-only GC-strat)

eval_01 = **0.3921**. Within noise of natural GC-strat (0.3939) and
mix ceiling (0.395 ± 0.002).

**Pure regulatory + GC = natural + GC.** Source identity doesn't
matter at the ceiling; composition does.

### T10 — final mechanistic theory
Library design impact on mean_r is mediated entirely by the
training distribution's COMPOSITION (esp. GC). Source identity
(natural/DHS/cCRE/mouse) doesn't matter once composition is
broadly balanced. Catastrophic floors (PLS-only, TF-density)
are GENRE COLLAPSE failure modes, not a separate axis.

### Plan exp 024
Test noise injection: 25K natural + 25K i.i.d. random uniform
DNA. Random sequences serve as implicit "negative" examples.
Does forcing the model to distinguish natural from random help
the regression generalize?

---

## 2026-06-03 — Experiment 024 result (noise injection)

eval_01 = **0.3800**. Worse than natural. 50/50 nat:random ≈ avg
of pure-nat (0.388) and pure-random (0.369). Noise dilutes signal.

Model is bottlenecked by signal volume, not lack of negatives.

### Plan exp 025
**The critical test of T8:** does motif/syntax content matter at
all once GC is controlled? Generate GC-STRATIFIED random uniform
DNA. If reaches ceiling → motifs irrelevant, GC is everything.
If stays low → motifs matter.

This is the cleanest possible decomposition of "library design"
into composition vs content.

---

## 2026-06-03 — Experiment 025 result (GC-strat random uniform) — KEY

eval_01 = **0.3899**. The clean decomposition:

| library | eval_01 | Δ |
|---|---|---|
| random uniform 40% GC (008) | 0.3689 | −0.025 vs ceiling |
| GC-strat random uniform (025) | 0.3899 | −0.004 |
| GC-strat natural (014) | 0.3939 | 0 |
| mix ceiling | 0.3951 ± .0012 | +0.001 |

**GC stratification of pure random DNA closes 84% of the
random↔natural gap.** No motifs. No syntax. Just 5 GC bins.

### T11 — final decomposition
- **GC composition contributes +0.021 of mean_r** (huge, ~84% of gap)
- **Motif/syntax contributes +0.004** (small but >3σ real)
- Source identity: 0

So T8 is largely (not entirely) right. Motifs aren't free, but they
are dwarfed by GC. A library that just matches the natural GC
distribution will land within 1% of the achievable ceiling.

### Plan exp 026
Decompose the +0.004 "motif premium." Generate GC-strat **dinuc-shuffle
of natural**. This preserves both GC distribution AND dinucleotide
content but destroys longer motifs and higher-order syntax.

If matches ceiling (~0.394) → dinuc content is the residual.
If falls toward GC-strat random (~0.390) → real motifs matter.

The whole point of this experiment is finding what NEXT lever exists
beyond GC. If dinuc closes the gap, the motif premium is just
local k-mer statistics. If it doesn't, real motif content matters
and we have an upper bound on the "motif lever."

---

## 2026-06-03 — Experiment 026 result (GC-strat dinuc shuffle)

eval_01 = **0.3853**. Below GC-strat random (0.3899) by 0.0046,
**below** GC-strat natural (0.3939) by 0.0086.

| library | GC | dinuc | motif | eval_01 |
|---|---|---|---|---|
| random uniform (008) | 40% | flat | none | 0.3689 |
| dinuc-shuffle (007) | natural | natural | none | 0.3733 |
| GC-strat random (025) | strat | flat | none | 0.3899 |
| GC-strat dinuc (026) | strat | natural | none | 0.3853 |
| GC-strat natural (014) | strat | natural | yes | 0.3939 |

### Surprising
Natural dinuc structure (CpG depletion) is **slightly bad** at matched
GC. Could be eval distribution mismatch (eval likely lacks natural
CpG depletion patterns) or reduced sequence diversity.

### T12 — full decomposition of random-to-natural lift
- **GC composition: +0.021** (biggest)
- **Higher-order motifs (k≥3) above dinuc: +0.009**
- **Natural dinuc above i.i.d.: −0.005** (slightly negative)
- Net: +0.025 from random to natural

The +0.004 "motif premium" of exp 025 was actually +0.009 of
true motif content offset by −0.005 of dinuc penalty.

### Implication
"Just match GC and motifs" — don't bother trying to match k=2
statistics. The model wants real motif content, not natural
dinucleotide ratios.

### Plan exp 027
The remaining engineering question: can synthetic motif planting
into GC-strat random *beat* natural? Generate GC-strat random
scaffolds with a sprinkled set of TFBS-like k-mers from JASPAR.
If lift above natural → motifs are the missing lever, can
synthesize beyond natural. If matches GC-strat natural → natural
motifs are already optimal.

Simpler: rather than full motif planting, plant GC-matched
high-information k-mers from JASPAR PWMs into random scaffolds.

---

## 2026-06-03 — Experiment 027 result (JASPAR motif-planted)

eval_01 = **0.3885**. Below GC-strat random (0.3899) and below
GC-strat natural (0.3939). **Motif planting did NOT lift; slight hurt.**

Planting 3 random JASPAR motifs (from 873 vertebrate PWMs) into
random GC-strat scaffolds gives no benefit. Confirms:

### T13 — motif content needs natural context
The +0.009 "motif premium" of natural sequence (exp 026) is NOT
exploitable by synthetic motif injection. Natural motifs carry
information through their natural co-occurrence, spacing, and
positional context — not just through presence.

### Engineering implication
**Library design has saturated.** No path beyond GC-strat natural
exists in the design space I've explored. The 0.395 ± 0.002 ceiling
is hard.

### Remaining plan
- exp 028: synthesis library combining GC-strat × multi-source ×
  multi-genome. Best-of-all-learnings.
- exp 029: seed=1 replicate of synthesis for noise control.
- exp 030: final written summary.

---

## 2026-06-03 — Experiment 028 result (synthesis library)

eval_01 = **0.3941**. Within noise of GC-strat alone (0.3939) and
4-way mix mean (0.3951). Combining all positive levers (GC × source
× genome) doesn't exceed any single one. Ceiling confirmed.

---

## 2026-06-03 — Experiment 029 result (synthesis seed=1)

eval_01 = **0.3949**. Synthesis 2-seed mean = 0.3945 (σ=0.0004).
Very stable design.

| design | mean eval_01 | seeds | σ |
|---|---|---|---|
| 4-way mix (002/010/022) | 0.3951 | 3 | 0.0012 |
| synthesis (028/029) | 0.3945 | 2 | 0.0004 |
| GC-strat nat (014) | 0.3939 | 1 | — |
| multispecies GC (020) | 0.3947 | 1 | — |

All within 1σ. Hard ceiling at 0.395 ± 0.002.

---

## 2026-06-03 — Experiment 030 result (10-bin GC stratification)

eval_01 = **0.3916** (Δ −0.0023 vs 5-bin GC-strat 014).

Finer GC resolution does NOT lift. 5-bin GC strat already saturated
the GC lever. Smaller per-bin samples may even slightly hurt.

---

## FINAL SUMMARY — what makes a 50K MPRA library informative

### Headline result
The 14-eval mean_r ceiling for a 50K, 200bp library on this model is
**0.395 ± 0.002** (95% CI from 3 seeds of 4-way mix design).

Achievable by many designs (see "ceiling cluster" below). Not exceedable
by any design tested across 30 experiments.

### The decomposition (causal mechanism)
Comparing random uniform DNA → natural human in 200bp:
- **GC composition: +0.021 of mean_r** (84% of total)
- **Higher-order motif content (k≥3): +0.009** (above i.i.d. random)
- **Dinucleotide structure: −0.005** (natural CpG depletion slightly
  bad at matched GC)

### Three-tier outcome map
| tier | eval_01 | designs |
|---|---|---|
| ceiling (0.394-0.396) | hit | 4-way mix, GC-strat nat/DHS/mouse, GC+reg, multispecies, synthesis |
| natural baseline (0.388) | hit | random hg38, mouse-only, shifted-windows, RC-aug |
| floor (≤0.37) | hit | random uniform, dinuc-shuffle |
| catastrophic | hit | TF-density top tiles (0.383), PLS-only (0.362) |

### What MATTERS for library design
1. **Balanced GC distribution** — biggest lever. Sample to fill all 5 GC
   bins (≤35, 35-45, 45-55, 55-65, >65%) uniformly. Hg38 length-weighted
   sampling under-represents the high-GC tail; stratify explicitly.
2. **Avoid genre collapse** — never narrow training to a single class
   (PLS, top-TF tiles). Costs −0.02 to −0.03 vs ceiling.
3. **Use natural sequence** — for the +0.009 motif premium that synthetic
   approaches (planting, dinuc-shuffle) cannot recapitulate.

### What DOESN'T MATTER (within ceiling tier)
- Source identity: nat/cCRE/DHS/mouse all interchangeable under GC
  control (T10).
- Multi-genome vs single-genome (T4).
- Sequence augmentation (shifted windows, RC) (T6).
- CpG-count vs GC stratification (functionally equivalent).
- Synthetic motif planting (worse than i.i.d. random at matched GC).
- GC bin resolution beyond 5 bins.
- Adding random uniform as "negatives" — dilutes signal linearly.

### Theory T13 (final)
**A library's training-distribution composition (esp. GC) is the
near-sole determinant of model generalization in the saturated regime.
Source identity is fungible. Motif content adds a small bonus but
only when embedded in natural sequence context.**

### Recommended library for unseen-cell-type generalization
**Either of:**
- (Simple) 50K natural hg38 windows, GC-stratified at 5 bins, 10K each.
- (Synthesis) 50K = 5 GC bins × 10K, each bin = 2500 hg-nat + 2500
  mm-nat + 2500 hg-DHS + 2500 hg-cCRE.

Both reach the 0.395 ceiling with stable seed behavior. The synthesis
design is marginally more defensible because it spans more genomic
contexts within each GC bin (broader coverage hedge against unseen
cell-type biases).

### Caveats
- All 14 evals showed correlated rank-order: a design that lifts eval_01
  generally lifts evals 2-7,9-14 proportionally. Eval_08 sits in a
  separate regime (mean ~0.265 vs 0.39) that no library design moved.
- σ_seed = 0.0012; |Δ| < 0.0025 is not distinguishable.
- All conclusions are conditional on the specific (unseen-to-me) model
  architecture and the eval set structure.

---
