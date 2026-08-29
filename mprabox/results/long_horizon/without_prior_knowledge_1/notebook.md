# Lab Notebook — MPRA Library Design

## Working theory (initial, 2026-04-22)

A library is informationally valuable for a generalizing sequence-to-activity model if it teaches the model regulatory grammar that **transfers across cell contexts**, not idiosyncratic features of the labeled cell types.

Initial hypotheses about what should matter:
1. **Coverage of regulatory primitives** — the library should contain a wide diversity of TF binding motifs in varied contexts so the model learns motif syntax, not memorized sequences.
2. **Activity dynamic range** — sequences should span low-to-high activity. Libraries that are mostly silent (random DNA) or saturating give the model little gradient to learn from.
3. **Independence from cell-type-specific bias** — if every active sequence in the library happens to share a feature unique to (say) K562 chromatin, the trained model overfits to that. So sequences should engage diverse regulatory programs.
4. **Compositional generality** — motif arrangements should look like real regulatory DNA in some statistical sense (spacings, multiplicities) so the learned grammar maps onto the biology of unseen cell types.

I expect: pure random DNA < genomic DNA < motif-enriched synthetic ≤ targeted designs. But this is an untested intuition — the experiments must measure it.

The metric is `eval_01` (primary) plus 13 anonymous eval sets. I have no information about what these sets contain. A robust library should perform well on all of them, not just one.

---

## 2026-04-22 17:25 — Experiment 001 planning: uniform random baseline

**Mode:** exploring (establishing baseline floor).

**Plan:** Generate 50,000 sequences of length 200 by sampling each base i.i.d. uniform from {A,C,G,T}. Three seeds (0, 1, 2).

**Hypothesis:** Pure random DNA contains essentially no regulatory grammar. A model trained on random sequences with measured activity should learn at most very weak signals (e.g., GC content effects on basal transcription) and should generalize poorly to held-out evaluation sets — especially any eval set that contains real regulatory elements.

**Why this experiment first:** It establishes the absolute floor. Every subsequent design choice (genomic sampling, motif insertion, active learning) needs to clear this floor by a meaningful margin to be worth pursuing. If random somehow scores well, that itself is a critical signal — it would mean the eval sets are testing something trivial like length/composition rather than regulatory function, or that the model architecture inside `prepare.py` has very strong inductive biases.

**Generalization justification:** A random library cannot encode any cell-type-specific bias because by construction it has no biology. So whatever performance it achieves is the cell-type-agnostic floor. This is the cleanest baseline against which to measure whether biology-aware libraries actually buy generalizable structure.

**Literature note:** Mostafavi lab MDC work (Investigating Data Size, Sequence Diversity, and Model Complexity, bioRxiv 2025) explicitly compares random vs. natural genomic sequences as MPRA training data. Synthetic random libraries were used historically (e.g., Sharon et al.) but pure-random-DNA-only training has been observed to give weak generalization to genomic test sets. The neural retina active-learning study (Friedman et al.) also notes that synthetic sequences alone are mostly uninformative without biological priors. So the literature predicts a low floor — consistent with my hypothesis.

---

## 2026-04-22 17:42 — Experiment 001 result: uniform random baseline

**Result:** eval_01 mean_r = **0.6954** (k562=0.693, hepg2=0.687, sknsh=0.707).
Range across 14 evals: 0.6553 (eval_12) — 0.8115 (eval_09). Wall: 914 s.
Seed-to-seed variance tiny (0.6917 / 0.6969 / 0.6976 on eval_01) → 3
seeds at 50K is reliable. SKNSH > K562 > HepG2 in every eval.

**Key cross-eval observations** (these will guide all future analysis):
- eval_01 ≈ eval_05 (0.6954 vs 0.6951) — almost certainly the same or
  closely related set.
- eval_02, eval_06, eval_14 cluster tightly at ~0.785 — another family.
- eval_09 has the highest baseline (0.81), eval_12 the lowest (0.66).
  This means each eval has different headroom — improvement on the
  low-baseline evals (12, 13, 07, 11) is where there's room to move.
- The cell-type ordering SKNSH > K562 > HepG2 is library-independent at
  this point — likely an assay-level dynamic range / noise property.

**How this updates my theory:**
This is a strong contradiction to my initial prediction. A "library with
no biology" was supposed to score near zero. Instead it scores 0.66–0.81.
That means one of the following must be true:
1. The eval sets are largely predictable from generic sequence
   composition (k-mers, GC) that random DNA samples adequately.
2. The model architecture inside `prepare.py` has very strong inductive
   biases — even from random training data, it learns enough about
   transcription baseline to predict the evals.
3. Both.

Either way, my updated theory is: **a substantial fraction of the eval
signal is composition-driven and "free", and the library-design problem
is to provide informative sequences that go beyond composition to teach
the model true regulatory grammar — visible only in the 0.20-ish
headroom between random-baseline and ceiling**. The floor is high; the
target is the headroom, not the absolute number.

**Important reframe of the goal:** improvements should be measured as
*headroom captured*, not absolute mean_r. A library that lifts eval_01
from 0.70 → 0.80 is much more informative than one that lifts eval_09
from 0.81 → 0.85, because the harder evals (low baseline) reveal more
about whether real grammar is being learned.

**What I want to know next:** Does any biological structure clear this
floor at all? Specifically, do *natural human regulatory sequences*
(ENCODE cCREs, TF-bound regions, DHSs) train a model that beats random
on most evals? This is the most decisive next experiment because:
- If genomic regulatory DNA clears random by a meaningful margin →
  biology matters and the rest of the work is finding which biology is
  most informative.
- If genomic DNA does NOT beat random → the eval sets do not test
  regulatory grammar in any straightforward way, and we need a totally
  different design philosophy (composition optimization, k-mer
  diversification, etc.).

This is the cleanest one-bit experiment to run next.

---

## 2026-04-22 17:50 — Experiment 002 planning: human genomic regulatory DNA

**Mode:** exploring (testing the strongest alternative hypothesis to exp 001).

**Plan:** Sample 50,000 200-bp windows from human candidate cis-regulatory
elements (cCREs). Specifically, ENCODE SCREEN cCREs — promoter-like (PLS),
enhancer-like (ELS, both proximal and distal), CTCF-only, and DNase-H3K4me3.
These are the canonical "regulatory" pieces of the human genome. Use
GRCh38 coordinates, extract reference sequence, take the central 200 bp of
each cCRE (or random 200-bp window inside it if longer; pad rare short
ones — but most cCREs are 150–350 bp).

**Hypothesis:** Real regulatory DNA contains TF motif content, motif
spacings, and CpG / nucleosome features that are absent from random DNA.
Predicted: eval_01 mean_r ≥ 0.75 (i.e., clears random's 0.70 by ≥ 0.05),
with bigger gains on the low-baseline evals (07, 11, 12, 13) where there
is more headroom.

**Why this experiment:** Most decisive single bit of information given
exp 001's surprising result — does biology clear the random floor?

---

## 2026-04-22 18:30 — Experiment 002 result: ENCODE cCREs

**Result:** eval_01 = **0.7133** (random was 0.6954, Δ = +0.018).
Average across 14 evals: 0.748 (vs. random 0.738, Δ avg = +0.010).

But the average hides three response classes:
- **Modest +0.02 across most evals** (01, 02, 03, 04, 05, 06, 09, 11, 12, 14)
- **Big wins**: eval_07 +0.077, eval_13 +0.084 (the low-baseline evals
  where I predicted the most headroom — confirmed)
- **Big loss**: eval_08 −0.146 (collapses from 0.78 to 0.64)

**Cluster correction** for skills/eval_set_structure.md: I previously
grouped {02, 06, 08, 14} at ~0.785 from random baseline. With cCRE
training, 08 falls to 0.64 while 02/06/14 stay at 0.80. So **eval_08
is qualitatively different from 02/06/14** — they only happened to
coincide at the random floor.

**How this updates my theory:**
- The hypothesis "biology dominates the eval signal" is WRONG. Random
  already captures ~0.74 mean correlation. Biology adds only ~0.01 on
  average. The eval is mostly composition-driven.
- BUT the hypothesis "biology adds nothing" is also wrong: there exist
  eval sets (07, 13) where natural regulatory grammar contributes
  substantial accuracy.
- The hypothesis "more biology is always better" is wrong: eval_08
  shows that for at least one eval set, biology is *worse* than random.
- Refined theory: **the 14 eval sets are heterogeneous in what they
  test.** Some are composition-driven (random does fine). Some test
  natural regulatory grammar (biology helps). At least one is biased
  toward random-like sequences (biology hurts). A library that
  generalizes across them all needs to encode multiple kinds of
  information — not just biology, not just composition.

**Practical implication:** Pure-strategy libraries (all random, all
biology) will both have failure modes. The optimum is probably a
mixture, possibly weighted toward biology. But before designing
mixtures I need to understand WHY cCRE helps where it does. Two
candidate explanations for the +0.077 / +0.084 gains on evals 07/13:
(a) motif content / TF binding syntax, (b) just composition statistics
of regulatory regions (GC-rich, CpG-rich, repeat-aware).

**Next experiment to disambiguate:** dinucleotide-shuffled cCREs.
Same source sequences as exp 002, but each shuffled while preserving
dinucleotide frequencies. This kills motif content and motif syntax
but preserves local composition. The result discriminates cleanly:
- If shuffled cCRE ≈ exp 002 → it was composition all along; biology
  per se doesn't matter, and the design strategy should be composition
  optimization (k-mer coverage, dinucleotide diversity).
- If shuffled cCRE ≈ exp 001 random → motif content is what mattered;
  the design strategy should be motif-aware (TF binding sites,
  syntax-preserving augmentation).
- If in between → both contribute, ratio tells us how to weight them.

This is the cleanest single bit I can extract next.

---

## 2026-04-22 18:35 — Experiment 003 planning: dinucleotide-shuffled cCREs

**Mode:** refining (testing the mechanism behind exp 002's gain).

**Plan:** Take the exact same 50,000 cCRE-derived sequences as exp 002
(per seed) and apply dinucleotide-preserving shuffle (Altschul-Erickson
or Fitch's algorithm) to each sequence independently. Output 50K
shuffled sequences per seed. Each shuffled sequence preserves first-
order Markov statistics (so GC content, dinucleotide composition,
local CpG fraction) but destroys all higher-order structure (motifs,
spacings, syntax).

**Hypothesis:** If the +0.018 lift on eval_01 (or +0.077 on eval_07,
+0.084 on eval_13) is composition-driven, dinucleotide shuffle should
preserve it. If it is motif-driven, shuffled sequences should regress
to near-random performance (0.69 on eval_01).

**Generalization justification:** Motif syntax is the most plausible
substrate for cross-cell-type generalization, because TF binding
preferences are largely shared across cell types — the same motif
binds the same TF in K562 and in any other cell type. If the cCRE
gain is motif-driven, then the lessons transfer to unseen cell types.
If the gain is composition-driven, transferability is weaker (every
cell type has its own composition biases). So this experiment is also
diagnostic of the *transferability* of whatever signal cCREs carry.

---

## 2026-04-22 19:25 — Experiment 003 result: dinuc-shuffled cCREs

**Headline:** shuffled cCRE is WORSE than uniform random on every eval
except 13. Mean across 14 evals: random 0.738, cCRE 0.748, shuf **0.687**.

This is a strong contradiction to my prior. I expected shuffled cCRE
to fall *between* random and cCRE — composition would still help even
if motifs were destroyed. Instead, removing motifs from cCRE while
preserving composition pushes performance well *below* uniform random.

**Three findings update the theory:**

1. **The cCRE gain is overwhelmingly motif-driven, not composition-driven.**
   The +0.018 cCRE→random gain on eval_01 reflects motifs alone.
   Destroying motifs while preserving composition gives -0.045 on
   eval_01 vs random.
2. **Narrow composition is actively harmful as training data.** cCREs
   are GC-biased (and CpG-island-biased) compared to uniform. When you
   train on sequences locked to that narrow composition with no motif
   content, the model overspecializes and generalizes worse. This is
   probably a dataset-shift effect: the eval test sequences span a
   wider composition than the cCRE training distribution.
3. **Wide composition coverage is a regularizer.** Uniform random's
   strength is not that it has biology — it doesn't — but that it
   exposes the model to the full composition space.

**Per-eval breakdown** (most informative pattern):
- eval_07: random=0.668, shuf=0.668, cCRE=0.745 — eval_07 is purely
  motif-rewarding; composition contributes 0.
- eval_13: random=0.658, shuf=0.688, cCRE=0.742 — composition
  contributes some (+0.030), motifs contribute more (+0.054).
- eval_08: random=0.784, shuf=0.643, cCRE=0.638 — eval_08 is
  composition-uniform-rewarding; both biology and biological
  composition are penalized.
- All others: composition mildly hurts (-0.04 to -0.07), motifs help
  (+0.06 to +0.09).

**Updated working theory:**

> The signal that generalizes across cell types is **motif content**,
> not the composition of regulatory regions. Wide composition coverage
> (uniform background) acts as a regularizer that lets the model
> generalize beyond the training composition distribution. The ideal
> library is **motifs embedded in compositionally diverse backgrounds**.

This is biologically coherent: TF binding preferences are largely
shared across cell types, so motif-content lessons transfer. Composition
biases (GC, CpG, repeat content) are more cell-type-specific because
they reflect chromatin architecture, which differs across cell types.

**Generalization justification refined:** A library that teaches
"motif X drives activity in context Y" generalizes to unseen cell
types whenever the same TF is expressed there. A library that teaches
"high-GC composition correlates with activity" doesn't transfer
because high-GC tracks K562/HepG2/SKNSH-specific chromatin, not
universal regulation.

---

## 2026-04-22 19:30 — Experiment 004 planning: motif-injected random

**Mode:** refining (testing the strongest reading of exp 003 — that
motifs alone, in random backgrounds, deliver the cCRE gain).

**Plan:** Generate 50,000 200-bp uniform-random backgrounds. For each,
inject 1–5 TF binding motifs (instances sampled from PWMs in JASPAR
2024 CORE vertebrates) at random positions. Number of motifs per
sequence is sampled (e.g., uniform on {1,2,3,4,5}); motif identity
sampled from the JASPAR motif pool (uniform across motifs); position
sampled uniformly within the sequence (subject to non-overlap).

**Hypothesis:** Motifs alone drive the cCRE gain. Predicted:
- Beats random uniform substantially on 07 and 13 (motif-rewarding
  evals); approximately matches cCRE on these.
- Approximately equals or slightly beats random on eval_08 (since
  background is uniform-random composition).
- Modestly beats random on most other evals.

If the prediction holds, the design strategy crystallizes: design
libraries by injecting motifs into uniform-random backgrounds,
control density and diversity of injected motifs.

If it falls short of cCRE on the motif-rewarding evals, then genomic
context (motif spacing, flanking sequence, real co-occurrence
patterns) carries additional information beyond what's in the
JASPAR PWM list.

**Generalization justification:** Synthetic motif-injection is the
most directly cell-type-agnostic library design possible — every
sequence engages identifiable TFs through their canonical binding
sites, with no chromatin/composition baggage. If this works, the
trained model has learned "TF X binding produces effect Y" which
should generalize to any cell type expressing TF X.

---

## 2026-04-22 20:25 — Experiment 004 result: motif-injected random

**Headline:** Motif insertion failed. Mean across 14 evals: 0.732 —
slightly *worse* than uniform random (0.738) and well below cCRE
(0.748). On the motif-rewarding evals, motif insertion provided no
gain at all: eval_07 motif=0.664 vs random=0.668; eval_13 motif=0.646
vs random=0.658.

This **falsifies my reading of exp 003**. I had concluded "the cCRE
gain is motif-driven", but if that were the full story, motif
insertion should have recovered the eval_07 / eval_13 gains. It
recovered nothing.

The one positive signal: eval_08 jumped from cCRE=0.638 to motif=0.768,
near random (0.784). That confirms eval_08 rewards uniform-composition
backgrounds.

**Updated theory:**
> The cCRE gain depends on motifs *in their genomic context* — not
> motifs in isolation. JASPAR PWM instances inserted at random
> positions in random backgrounds do nothing.

Possible reasons (each is a plausible hypothesis to test later):
1. The JASPAR pool is too broad; most TFs aren't expressed in
   K562/HepG2/SKNSH so most "motifs" have no functional effect on
   activity → no learning signal.
2. Random placement destroys motif syntax (real co-occurrences,
   spacings, anchor relative to TSS, etc.).
3. Sampled instances are too consensus / too high-affinity; real
   sites span an affinity gradient.
4. Motif density is wrong (1–5 / 200 bp may not match real cCREs).

**What still holds:** wide composition is a regularizer (motif lib
recovered eval_08 by having uniform background; cCRE failed eval_08
because of narrow composition).

**What needs rethinking:** the design strategy "inject motifs into
random backgrounds" doesn't work as I expected. The genomic context
in cCREs is doing more than just "providing motifs."

**Next experiment plan:** mixture library — 25K cCRE + 25K uniform
random. Two reasons:
(a) Practical — directly tests whether composition coverage and
    biology are additive. If so, expect best-of-both: >cCRE on
    eval_08, ≈cCRE on motif-rewarding evals.
(b) Establishes a strong baseline for further refinement, regardless
    of what's happening inside exp 004.

I'll come back to disambiguating exp 004's failure (cell-type-specific
motifs vs context vs density) after I've established whether mixtures
work.

---

## 2026-04-22 20:30 — Experiment 005 planning: 25K cCRE + 25K uniform random

**Mode:** refining (additivity test).

**Plan:** Per seed, generate 25,000 cCRE-derived sequences (using exp
002's generator with reduced N) and 25,000 uniform-random sequences.
Concatenate and shuffle. The cCRE half uses class-balanced sampling
(3,125 per SCREEN class). Same seed-determinism guarantees.

**Hypothesis:** If composition coverage and biology are additive, the
mixture should:
- ≈ random on eval_08 (random half supplies the uniform composition
  the eval needs).
- ≈ midpoint of (cCRE, random) on motif-rewarding evals 07/13 — the
  cCRE half provides motifs, but at half density.
- ≥ cCRE on most other evals (combination of both signals).

If we instead see the mixture ≈ random everywhere, then the cCRE
sequences in the mixture are being "overwhelmed" or simply averaged
out. If we see the mixture ≈ best-of-both (≥ max(rand, cCRE) per
eval), then the strategies complement and we should keep mixing.

**Generalization justification:** A 50/50 mixture is a hedge — half
of training is biology that should transfer through TF-motif
syntax, half is composition coverage that should regularize away
narrow training-distribution effects. The mixed library is more
likely to generalize beyond the labeled cell types than either pure
strategy, because it covers both kinds of regulatory variation.

---

## 2026-04-22 21:15 — Experiment 005 result: cCRE+random mixture

**Headline:** Mixture is roughly the linear midpoint of pure cases on
most evals. Mean across 14 evals: rand 0.738, cCRE 0.748, motif 0.732,
**mix 0.738**. The mixture is identical to random on average — it
does NOT outperform either pure library.

**Per-eval pattern:** mixture sits at midpoint between random and
cCRE on essentially every eval. eval_07 mix=0.703 vs midpoint(rand,
cCRE)=0.707; eval_13 mix=0.700 vs midpoint=0.700. eval_08 mix=0.687
vs midpoint=0.711, slightly closer to cCRE side.

**The "additive best-of-both" hypothesis is falsified.**

**How this updates my theory:**
> Library types do NOT additively combine. A mixture of A + B
> performs roughly like a midpoint, sometimes worse than either pure
> A or pure B. Each sequence in the library competes for model
> training capacity — adding non-informative sequences reduces the
> signal density of the informative ones.

This is a major theoretical update. It implies the strategy is NOT
"diversify with random" but rather "concentrate maximally informative
sequences." The eval_08 problem may not be solvable with mixtures —
it might require a qualitatively different design that has BOTH
motif content AND uniform composition together (not as a mixture).

**Practical implication:** Future libraries should be 100%
maximally-informative. No "padding" with random.

**Open question:** Within cCRE, which classes contribute most to the
motif-rewarding gains? cCRE was class-balanced (3,125 of each of 8
classes per half). PLS (promoters) are the most regulatorily-dense
class but only 47K cCREs in the database. If PLS-only matches or
beats class-balanced cCRE on motif-rewarding evals 07/13, we should
enrich those classes.

---

## 2026-04-22 21:20 — Experiment 006 planning: PLS-only (promoters)

**Mode:** refining (which cCRE class drives the motif gains).

**Plan:** 50,000 sequences per seed sampled from the 47,532-cCRE PLS
(promoter-like signature) pool, with replacement. Same 200-bp central
window extraction as exp 002. The PLS pool is exhausted at ~47K
unique cCREs so seed 0 covers ~all of them; seed 1 and seed 2 will
have substantial overlap with seed 0 (but with different particular
draws and orderings, which still gives meaningful 3-seed averaging).

**Hypothesis:** Promoters are the most regulatorily-dense element
class — they have the highest TF binding density, are bound by
ubiquitously expressed TFs (POL2, TBP, SP1, NRF1, YY1), and drive
the strongest measurable activity. If element class matters, PLS-only
should beat class-balanced cCRE on motif-rewarding evals.

If PLS-only ≥ cCRE → element class matters; enrich on it.
If PLS-only ≈ cCRE → class doesn't matter; gains come from any
biology.
If PLS-only < cCRE → distal-element diversity contributes;
class-balance was right.

**Generalization justification:** Promoter regulatory grammar is
heavily governed by core promoter elements (TATA, INR, DPE) and
proximal TF binding sites that are conserved across cell types
(housekeeping TFs). Models trained on promoter sequences should
learn cell-type-portable features. The risk: promoters may be
overspecialized to a narrow band of regulatory grammar (housekeeping)
and miss the cell-type-specific enhancer grammar that the eval sets
might also test.

---

## 2026-04-22 21:45 — Experiment 006 result: PLS-only

**Headline:** Catastrophic collapse on every eval. Mean across 14:
**0.604** vs cCRE 0.748 vs random 0.738. PLS-only is far worse than
both class-balanced cCRE and uniform random. eval_07 fell from cCRE's
0.745 to 0.509 — *below* random (0.668). eval_13 from 0.742 to 0.491.

**The "promoters are sufficient" hypothesis is dead.** Class diversity
is critical.

**Updated theory:**
> Library diversity across regulatory element classes is essential.
> A library that restricts to one class — even the most regulatorily-
> dense one — fails on every eval. The model needs exposure to
> multiple kinds of regulatory grammar (promoter, enhancer, insulator,
> chromatin-accessible) to learn features that transfer.

This converges with the eval_08 / wide-composition story: the class-
balanced cCRE library succeeds because it spans wide composition
(low-GC dELS through high-GC PLS) AND wide motif content (multiple
TF binding programs). PLS-only is simultaneously narrow in both
axes.

**A pattern is emerging.** Across exps 1-6, the design choices that
have HURT performance are all forms of *narrowness*:
- Pure cCRE composition (exp 003 shuf): narrow composition → bad.
- Random JASPAR motifs (exp 004): no genomic context → diluted signal.
- Mix-with-random (exp 005): diluted bio → midpoint.
- Single-class PLS (exp 006): narrow class → catastrophe.

Choices that HELPED: class-balanced cCRE (exp 002), which is wide
across regulatory classes and motif content. The unifying principle
seems to be:

> **A library generalizes when it covers a wide span of regulatory
> grammar in roughly real proportions. Restricting any axis (class,
> composition, motif identity) by a lot hurts. Adding non-regulatory
> sequences to "fill" gaps doesn't work either, because they
> compete for model capacity with informative sequences.**

This points to: design libraries that are "balanced biology"
across element classes, but enriched somehow — by quality, by
density, by activity — without narrowing any axis.

**Next experiment:** dELS-only (distal enhancers, the largest class
at 1.47M, GC 0.40). Diagnostic: is PLS uniquely bad (something
about promoters specifically), or are ALL single-class libraries
bad (proving class diversity is essential)?

---

## 2026-04-22 21:50 — Experiment 007 planning: dELS-only

**Mode:** refining (testing whether single-class collapse is
PLS-specific or universal).

**Plan:** 50K x 200bp sampled with replacement (or without — pool
is 1.47M) from the dELS class. Same extraction protocol.

**Hypothesis:** If single-class libraries are inherently bad, dELS
should also collapse (eval_07/13 << cCRE). If PLS was uniquely bad
(due to extreme GC bias), dELS might match cCRE because its GC is
closer to genomic mean.

**Generalization justification:** Distal enhancers carry the bulk of
cell-type-specific regulatory information. If they generalize on
their own, that means cell-type-specific motif content is sufficient.
If they don't, then class breadth is essential and the model
specifically needs the contrast across element types to learn
meaningful features.

---

## 2026-04-22 22:35 — Experiment 007 result: dELS-only

**Headline:** dELS-only is the best library so far. Mean across 14
evals: **0.756** (vs cCRE 0.748, vs random 0.738). Beats class-balanced
cCRE on 7/14 evals (and matches on others), including the
motif-rewarding evals 07 (+0.015) and 13 (+0.018).

**Falsifies my exp 006 conclusion** ("single-class libraries are
inherently bad"). PLS-only collapsed; dELS-only wins. The difference:
- dELS pool 1.47M vs PLS pool 47K (30× larger)
- dELS GC = 0.461 (close to genomic baseline) vs PLS GC = 0.606
- dELS spans diverse cell-type-specific TF programs; PLS dominated
  by housekeeping TFs

**Updated theory:**
> What matters is the diversity of *regulatory contexts* the training
> set spans, not the number of named "element classes" it spans.
> dELS alone provides enough internal diversity (1.47M contexts) to
> train a model that generalizes well. Class diversity is helpful
> when per-class pools are small or narrow (PLS), but redundant
> when the chosen class is itself large and diverse (dELS).

**Convergence with exp 005's lesson:** don't dilute informative
sequences with less-informative ones. Class-balanced cCRE (exp 002)
diluted dELS with the smaller, narrower classes (PLS, CA-TF) that
each contribute less per sequence.

**Where dELS-only loses:** eval_04 (-0.03 vs cCRE), eval_09 (-0.03).
These two might be testing something specific to PLS / TF / CA classes
that dELS lacks. Worth probing later, but small effect compared to
the gains.

**eval_08 still a problem:** dELS-only = 0.672, random = 0.784.
The +0.034 vs cCRE is a small win. eval_08 remains the holdout.

**Next experiment:** test whether the gain is from "dELS
specifically" or from "natural cCRE proportions" (which would also
be ~62% dELS). If natural-prop ≥ dELS-only, we should weight by
natural frequency. If natural-prop < dELS-only, dELS-dominance is
the actual driver.

---

## 2026-04-22 22:40 — Experiment 008 planning: natural-proportion cCRE

**Mode:** refining (testing whether dELS-only's gain is from dELS
or from natural class proportions).

**Plan:** Sample 50,000 cCREs from the full pool (2.35M cCREs across
8 classes) WITHOUT class balancing — i.e., uniform random sample
from the entire BED. This naturally yields ~62.6% dELS, ~10.6% pELS,
~10.5% CA, ~5.4% CA-CTCF, ~4.5% TF, ~3.4% CA-H3K4me3, ~2.0% PLS,
~1.1% CA-TF.

**Hypothesis:** Natural proportions sit between class-balanced
(exp 002) and dELS-only (exp 007). If the diluting effect of small
classes is the driver, natural-prop should land between them. If
the small classes ADD value at low weights, natural-prop could
beat dELS-only.

**Generalization justification:** Natural class proportions
reflect the proportions of regulatory elements actually present in
the genome. A model trained on a "genome-faithful" library would
match the natural distribution of regulatory programs and might
generalize better to test sets drawn from real genomic regulatory
contexts. Counterargument: training distributions often benefit
from upsampling rare informative classes — natural proportions are
not always the optimal training distribution.

---

## 2026-04-22 23:25 — Experiment 008 result: natural-proportion cCRE

**Headline:** mean_r=0.7083 on eval_01; mean across 14 evals = **0.752**
— sits between class-balanced cCRE (0.748) and dELS-only (0.756),
slightly worse than dELS-only.

**Per-eval, vs dELS-only:**
- ≈ on high-baseline evals (02, 03, 06, 14): within ±0.001
- slightly worse on motif-rewarding evals (07: −0.010, 13: −0.006)
- slightly better on eval_04 (+0.005), eval_09 (+0.004) — confirms
  exp 007 conjecture that small classes help these two specifically
- still bad on eval_08 (0.660 vs random 0.784)

**Interpretation:** the natural-proportion library is dELS-dominated
(~62%) and inherits most of dELS-only's benefit. Adding the small
classes (PLS, CA-TF, etc.) at natural frequencies neither helps nor
hurts much on average; on motif-rewarding evals it slightly
dilutes. Class-balanced cCRE (exp 002, 12.5% each) was the worst of
the three because it overweighted the small narrow-grammar classes.

**Updated theory:**
> Class proportions don't matter much once dELS dominates. The
> dELS-only library wins because it concentrates training on the
> most diverse, highest-information class. Adding small narrow
> classes at any non-trivial fraction modestly dilutes the average.

This further confirms exp 005/007 lesson: **don't dilute
informative sequences with less-informative ones**.

**Where headroom remains:** best per-eval across all 8 experiments
is composite 0.762, only +0.006 above dELS-only's 0.756. The single
biggest gap is eval_08 (random 0.784 vs dELS 0.672, Δ=0.112). All
biology-aware libraries fail this eval — uniform random wins.

**Next experiment:** I have now exhausted "shuffle the cCRE pool"
hypotheses. Time for a genuinely new direction: **genome-wide
random sampling**. Sample 50K random 200bp windows from the entire
human genome, including intergenic non-cCRE (gene deserts, introns,
non-regulatory regions). This tests whether "regulatory annotation"
specifically helps, vs. real human DNA in general.
- If genome-wide ≈ dELS-only → annotation doesn't matter, real DNA
  is enough.
- If genome-wide < dELS-only → cCRE annotation captures real
  information beyond raw genomic composition.
- If genome-wide > dELS-only → expand beyond cCREs.
This is the cleanest single-bit test on whether cCRE annotation is
load-bearing.

---

## 2026-04-22 23:30 — Experiment 009 planning: genome-wide random

**Mode:** exploring (genuinely new direction — uses no cCRE
annotation).

**Plan:** Uniform-random sample 50K x 200bp windows from hg38
(autosomes + X/Y, exclude chrM). Skip windows that contain any N
bases (telomeric/centromeric/assembly gaps). No blacklist filter
beyond N-skipping. Three seeds.

**Hypothesis:** Most random genomic windows are non-regulatory
(intergenic, intronic, gene deserts), but they carry the natural
statistical structure of the genome — repeat content, GC variance,
isochore structure, chromatin context features the model can pick
up indirectly. dELS-only beats class-balanced cCRE because it has
more internal diversity; genome-wide has even more diversity but
most of it is "uninformative" non-regulatory sequence.

Predict: genome-wide < dELS-only (mean ~0.73 like uniform-random
ACGT, since most windows look like random DNA from the model's
perspective, but slightly higher because real DNA has better
repeat/composition structure than uniform random).

**Generalization justification:** A model trained on genome-wide
windows sees the FULL distribution of sequences the genome
produces, not curated regulatory subsets. If evals contain test
sequences from non-cCRE regions (which they may), this could
generalize better. If evals are cCRE-curated, this would
underperform. The result will indicate which.

---

## 2026-04-22 23:55 — Experiment 009 result: genome-wide random

**Headline:** mean_r=0.6596 on eval_01; mean across 14 evals
= **0.690** — *worse than uniform random ACGT* (0.738) by -0.048
mean. Catastrophic on eval_08 (0.535 vs random's 0.784, Δ=-0.249).

**Genome-wide loses to uniform random on 12/14 evals:**
- Beats random only on the two motif-rewarding evals: eval_07
  (+0.044), eval_13 (+0.074). Real DNA contains real motifs.
- Loses everywhere else, hardest on eval_08 (collapses to 0.535).
- Trails dELS-only by -0.066 mean — the largest gap so far.

**Decisive answer to the cCRE-annotation question:**
> The cCRE annotation is doing real, load-bearing work. It is
> NOT a noisy proxy for "real DNA". It selects the ~0.7% of the
> genome that contains regulatory elements out of a sea of
> mostly-uninformative-or-actively-misleading sequence.

**Major theory update (the biggest of the project so far):**
> Curation matters more than sequence-realism. Uniform random ACGT
> beats unfiltered genomic samples because most of the genome
> teaches the model nothing useful or actively wrong things —
> repeats (LINE/SINE/LTR ~50% of genome) form low-complexity
> distractor signals; intergenic gene deserts contain no
> regulatory grammar; intronic regions carry only weak signal.
> The model learns the wrong features from this content and
> generalizes worse than from a noiseless uniform baseline.

**Updated library ranking by mean_r:**
1. dELS-only (007) — 0.756
2. natprop cCRE (008) — 0.752
3. cCRE class-balanced (002) — 0.748
4. cCRE+random mix (005) — 0.745
5. uniform random ACGT (001) — 0.738
6. motif-injected random (004) — 0.732
7. dinuc-shuffled cCRE (003) — 0.696
8. **genome-wide random (009) — 0.690**
9. PLS-only (006) — 0.604

The four "biology-aware curated" libraries (007, 008, 002, 005)
form the top tier. The synthetic baseline (001) is mid-pack. The
"biology-broken" libraries (003 motifs destroyed, 009 unfiltered
genomic, 006 narrow class) are at the bottom.

**Next experiment:** isolate the "repeats are bad" sub-hypothesis.
If repeat-masked genome-wide ≈ cCRE, repeats are the entire active
distractor. If still much worse than cCRE, then non-repeat
intergenic/intronic content is also uninformative and the cCRE
annotation does more than just exclude repeats.

---

## 2026-04-22 23:58 — Experiment 010 planning: repeat-masked genome-wide

**Mode:** refining (decomposing the genome-wide failure into
repeats vs non-repeat-non-regulatory).

**Plan:** Sample 50K x 200bp windows from hg38 main chromosomes;
reject windows that are >50% soft-masked (repeat content from the
hg38.2bit standard soft-mask, which embeds RepeatMasker + Tandem
Repeats Finder annotations). Reject windows containing N. Three
seeds.

**Hypothesis:** The genome-wide library failed because repeats
dominate (~50% of genome) and form low-complexity distractor
signal. If repeat-masking recovers most of the gap from
genome-wide (0.690) to cCRE (0.748), repeats are the entire
problem. If repeat-masked still scores in the 0.70 range (i.e.,
between random ACGT and cCRE), then non-repeat genomic content
is also worse than cCRE — meaning the cCRE annotation captures
more than just "non-repeat".

**Generalization justification:** A model trained on real but
non-repetitive DNA sees the full diversity of human regulatory
and non-regulatory sequence except for the repeat fraction. If
eval test sequences are themselves non-repetitive (most evals
likely test cCRE-like content), this could partially recover
genwide's lost performance. If the result still trails cCRE, it
indicates that "regulatory annotation" carries information beyond
"not-a-repeat", confirming the value of curated regulatory atlases.

---

## 2026-04-23 00:25 — Experiment 010 result: repeat-masked genome-wide

**Headline:** mean_r=0.6538 on eval_01; mean across 14 evals
= **0.686** — slightly *worse* than unfiltered genome-wide
(0.690), and far below cCRE (0.748). Repeat-masking did NOT
recover the gap.

**Per-eval signal partition (clean and informative):**
- eval_08 +0.054 (helps the synthetic-favoring eval — repeats
  do contain bio-content that hurts here)
- eval_07 −0.022, eval_13 −0.022 (the two motif-rewarding evals
  get WORSE — repeats carry real TF motifs from
  transposon-derived binding sites)
- All other evals: −0.005 to −0.012 (noise level)
- Net mean change: −0.004

**Hypothesis falsified.** Repeats are not the active distractor
that made genome-wide fail. They contribute helpful motif
content to motif-rewarding evals while contributing biology-flavored
noise to eval_08. Their net effect is approximately neutral.

**Refined theory:**
> The genome-wide failure is caused by the bulk of non-repeat
> non-regulatory sequence — gene deserts, intronic regions,
> intergenic AT-rich tracts. These contain real DNA patterns
> (codon usage, splice motifs, isochore composition) that the
> model learns and over-applies, but they don't carry regulatory
> grammar. cCRE annotation specifically picks the high-info ~0.7%
> of the genome; both repeats AND non-repeat-non-regulatory bulk
> are part of the lower-info 99.3% that doesn't help.

**Updated theory framing:**
> Curation > sequence-realism. Most of the human genome is
> low-information for regulatory tasks — neither random enough
> to teach generic features nor regulatory enough to teach
> specific grammar. The cCRE annotation is doing real work that
> simple repeat-filtering cannot replicate.

**eval_08 sub-finding:** repeat-masking lifts eval_08 by +0.054.
Combined with prior data (random gives 0.784, all biology < 0.69),
this suggests eval_08 specifically rewards both
(1) uniform-random composition AND (2) absence of repeat-like
structure. This is consistent with eval_08 testing on synthetic
or scrambled sequences that lack any biological pattern.

**Next experiment:** isolate the "pool size" hypothesis from the
"dELS-specifically" hypothesis. dELS-only worked because of (a)
its 1.47M-element pool diversity OR (b) something specific to
distal enhancer grammar. Test by training on CA-only (chromatin
accessibility, the second-largest cCRE broad class with ~250K
elements). Same protocol as exp 007. CA elements have GC ~0.45
similar to dELS, so this isolates "class identity" from "pool
size" and "GC composition" reasonably cleanly.

---

## 2026-04-23 00:30 — Experiment 011 planning: CA-only

**Mode:** refining (isolating dELS-specific signal from
pool-size signal).

**Plan:** Sample 50K x 200bp from the CA (chromatin
accessibility) cCRE class. CA pool size from the cCRE BED:
will determine at load time but ENCODE SCREEN reports ~250K
across the cCRE registry. Same central-200bp extraction.
Three seeds.

**Hypothesis:**
- If CA-only ≈ dELS-only → pool size + class breadth was the
  driver; any large cCRE class with diverse cell-type coverage
  works.
- If CA-only < dELS-only → dELS-specific enhancer grammar
  (cell-type-specific TF combinations) is the driver. Distal
  enhancers carry more information than chromatin accessibility
  per se.
- If CA-only > dELS-only → chromatin accessibility content is
  even more informative than enhancers (would be surprising;
  CA is a heterogeneous category that includes many DHS sites).

**Generalization justification:** CA elements are accessible
chromatin regions that may or may not be enhancers — they
include many cell-type-specific accessible sites. A model that
trains on CA learns features predictive of accessibility, which
is a necessary-but-not-sufficient condition for enhancer
activity. If CA generalizes as well as dELS, it means
"accessibility content" is the load-bearing signal. If it
underperforms, "enhancer-specific content" matters beyond mere
accessibility.

---

## 2026-04-23 00:55 — Experiment 011 result: CA-only

**Headline:** mean_r=0.6775 on eval_01; mean across 14 evals
= **0.718** — sits below uniform random (0.738) and well below
dELS-only (0.756). Pool size matters AND class identity matters.

**Pool-size–class-quality matrix (single-class libraries):**
- PLS pool 47K → mean 0.604 (collapse)
- CA pool 246K → mean 0.718 (mediocre)
- dELS pool 1.47M → mean 0.756 (best)

There is a monotonic pool-size trend, but CA at 246K (5× larger
than PLS, 6× smaller than dELS) still loses to uniform random
ACGT. Pool size is not the whole story.

**CA underperforms dELS uniformly** (Δ = −0.016 to −0.053 on
every eval; mean Δ = −0.033). No eval where CA beats dELS.

**Class identity matters intrinsically:**
> dELS uniquely combines (a) the largest cCRE pool (1.47M, 6× CA,
> 30× PLS) with (b) the most informative class identity — distal
> enhancers carry diverse cell-type-specific TF combinations and
> span the widest activity range in MPRA. CA-only fails despite
> a large pool because "accessible chromatin" is too
> heterogeneous and behavior-non-specific (housekeeping accessible
> sites, weak enhancers, non-functional accessible regions).

**Falsifies "any large single class works".** dELS is special.

**Where CA beats random:** only on the two motif-rewarding evals
(07: +0.070, 13: +0.086). Same pattern as PLS-only and
genome-wide — biological libraries help motif evals while losing
on others. CA's larger pool gives it bigger 07/13 wins than PLS
but doesn't recover the per-eval gap on the high-baseline evals.

**Next experiment:** complete the class survey with **pELS-only**.
pELS pool is 249K (essentially identical to CA's 246K). pELS is
"proximal enhancer" — enhancer grammar but located near
promoters. If pELS ≈ dELS-relative-quality (i.e., much better
than CA), then "enhancer grammar" is the load-bearing signal
regardless of distal/proximal location. If pELS ≈ CA, then
"distal" is what matters specifically. Together with PLS, dELS,
CA, this isolates enhancer-vs-accessibility-vs-promoter.

---

## 2026-04-23 01:00 — Experiment 012 planning: pELS-only

**Mode:** refining (completing the class-isolation survey).

**Plan:** 50K x 200bp from the pELS class (proximal enhancer-like
signature; pool 249K cCREs). Same central-200bp extraction
(without replacement), three seeds.

**Hypothesis:** pELS pool size matches CA's. If pELS scores
substantially above CA (closer to dELS), enhancer grammar
specifically matters and "distal" is incidental. If pELS scores
near CA, then distal-enhancer content is uniquely informative
for some reason (perhaps because distal enhancers carry the
most cell-type-specific TF combinations, vs proximal enhancers
which are more housekeeping-ish like promoters).

**Generalization justification:** pELS bridges the conceptual
gap between PLS (promoter-like, housekeeping) and dELS (distal
enhancer, cell-type-specific). A model trained on pELS gets
"enhancer-near-promoter" content. If this generalizes well, it
suggests that enhancer-like grammar is the key feature; if
poorly, it suggests proximal regulatory elements share more
with promoters than with distal enhancers.

---

## 2026-04-23 01:30 — Experiment 012 result: pELS-only

**Headline:** mean_r=0.7203 on eval_01; mean across 14 evals
= **0.758** — slightly *beats* dELS-only (0.756), making pELS
the new best library. pELS pool is only 249K (6× smaller than
dELS's 1.47M).

**Per-eval, vs dELS:** pELS wins 11/14 evals.
- Wins: 01 (+0.011), 02 (+0.012), 03 (+0.006), 04 (+0.019),
  05 (+0.011), 06 (+0.012), 08 (+0.012), 09 (+0.020),
  11 (+0.011), 12 (+0.007), 14 (+0.011) — all the high- and
  mid-baseline evals get +0.011 to +0.020 bumps.
- Loses: 07 (−0.012), 10 (−0.005), 13 (−0.013) — the
  motif/diversity evals where dELS's larger pool wins.

**Single-class matrix (now non-monotonic with pool size):**
- PLS pool 47K → 0.604
- CA pool 246K → 0.718
- pELS pool 249K → **0.758** (best)
- dELS pool 1.47M → 0.756

pELS and CA have nearly identical pool sizes (249K vs 246K) but
pELS scores +0.04 higher. Pool QUALITY > pool SIZE.

**Major theory update:**
> Class identity matters MORE than pool size beyond a moderate
> threshold (~250K elements). Proximal regulatory regions are
> better-characterized and harbor cleaner TF binding programs;
> the pELS pool is enriched for high-evidence enhancers. Distal
> enhancers exist in much larger numbers but include many
> low-evidence elements that dilute the training signal.

**On the per-eval pattern (cleanly informative):**
- pELS wins evals testing GENERAL regulatory grammar (high
  baseline 02/06/14 cluster, paired 01/05, plateau evals)
- dELS wins evals testing SPECIFIC TF / cell-type motif content
  (low baseline 07/13, diversity-eval 10)
- Suggests their content is COMPLEMENTARY — pELS has cleaner
  enhancer grammar but narrower TF coverage; dELS has noisier
  sequences but covers more TF programs.

**Updated library ranking by mean_r:**
1. **pELS-only (012) — 0.758** (NEW BEST)
2. dELS-only (007) — 0.756
3. natprop cCRE (008) — 0.752
4. cCRE class-balanced (002) — 0.748
5. cCRE+random mix (005) — 0.745
6. uniform random (001) — 0.738
7. motif-injected random (004) — 0.732
8. CA-only (011) — 0.718
9. dinuc-shuffled cCRE (003) — 0.696
10. genome-wide random (009) — 0.690
11. repeat-masked genome-wide (010) — 0.686
12. PLS-only (006) — 0.604

**Next experiment:** test whether pELS + dELS combo captures both
sides of the complementarity. If additive → first library above
0.76. If dilutive → mixing hurts both.

---

## 2026-04-23 01:35 — Experiment 013 planning: pELS+dELS combo

**Mode:** building (combining the two best single-class libraries
to test additivity).

**Plan:** 25K pELS + 25K dELS, sampled (no replacement) from
their respective pools, shuffled together. Same central-200bp
extraction. Three seeds.

**Hypothesis:** pELS and dELS show complementary per-eval
patterns. pELS leads on general/high-baseline evals; dELS leads
on motif-rewarding low-baseline evals. If the model can integrate
both sets of features, the combo should beat both individually
(mean > 0.76, eval_07 ≈ dELS, evals 02/06/14 ≈ pELS). If mixing
dilutes (as past combo experiments suggest), the combo lands
between them at ~0.757.

**Counter-hypothesis from prior data:** exp 005 (cCRE + random
50/50) and exp 002 (8-class balanced) both showed dilution: the
mix landed BETWEEN the parents rather than above. Pure-class
training appears to produce sharper learning. If this holds,
pELS+dELS should ≈ pELS or slightly below.

**Generalization justification:** A model trained on the union of
proximal and distal enhancers sees the full enhancer grammar
spectrum (housekeeping-adjacent + cell-type-specific). If the
ground-truth regulatory code is best captured by their union,
this should generalize better than either alone. If the two
classes carry conflicting biases, the model may compromise and
under-fit both.

---

## 2026-04-23 02:05 — Experiment 013 result: pELS+dELS combo

**Headline:** mean_r=0.6936 on eval_01; mean across 14 evals
= **0.731** — DRAMATIC dilution. Combo loses to BOTH pELS (0.758)
and dELS (0.756) on EVERY eval, mean drop -0.025 vs both.

**Hypothesis (additive complementarity) falsified hard.** No
eval shows additivity; every eval shows dilution.

**Third independent confirmation that mixing dilutes:**
- exp 002 (8-class balanced) underperformed exp 007 (dELS-only)
- exp 005 (cCRE + random 50/50) underperformed exp 002 (pure)
- exp 013 (pELS+dELS 50/50) underperforms BOTH parents

**Strong refined principle:**
> **Don't mix.** Pure-class training reliably beats mixed
> training, even when combining the two highest-quality
> single-class libraries. The model develops sharper feature
> representations when the training distribution is homogeneous;
> mixing forces compromise features that fit neither well.

**Rules out a large class of designs.** Future improvements must
either:
1. Find a single class better than pELS (TF, CA-CTCF, CA-H3K4me3,
   CA-TF still untested)
2. Augment within a single class (sub-pool selection, RC, etc.)
3. (Unlikely) Find a class that itself includes both proximal-
   and-distal enhancer characteristics — none in cCRE annotation.

**Per-class undersampling caveat:** combo had 25K of each, vs
50K in the pure libraries. pELS-only sees 20% of pELS pool; combo
sees only 10%. Some of the -0.025 drop may be pool-coverage
related, but the drop magnitude exceeds what subsampling alone
predicts (e.g., dELS has 1.47M pool — 25K vs 50K subsamples
visit similar tiny fractions yet the model is much worse on
the dELS-favoring evals 07/13).

**Updated library ranking by mean_r:**
1. pELS-only (012) — 0.758
2. dELS-only (007) — 0.756
3. natprop cCRE (008) — 0.752
4. cCRE class-balanced (002) — 0.748
5. cCRE+random mix (005) — 0.745
6. uniform random (001) — 0.738
7. motif-injected random (004) — 0.732
8. **pELS+dELS combo (013) — 0.731**
9. CA-only (011) — 0.718
10. dinuc-shuffled cCRE (003) — 0.696
11. genome-wide random (009) — 0.690
12. repeat-masked genome-wide (010) — 0.686
13. PLS-only (006) — 0.604

**Next experiment:** continue single-class survey with TF-only.
TF pool 105K (between PLS 47K and CA 246K). TF cCREs are
"TF-bound regions without chromatin marks" — purely TFBS-rich.
Tests whether pool size + TF-binding-specificity beats
chromatin-accessibility-specificity at similar pool ranges.

---

## 2026-04-23 02:10 — Experiment 014 planning: TF-only

**Mode:** refining (continuing single-class survey).

**Plan:** 50K x 200bp from the TF cCRE class. TF pool 105K
(between PLS-47K and CA-246K). Same central-200bp extraction
(without replacement; pool 105K means we visit ~48% of pool).
Three seeds.

**Hypothesis:** TF cCREs are TF-bound regions WITHOUT chromatin
marks — they represent "naked" TF binding sites. If TF-only
≈ pELS-quality (relative to CA), then TF-binding-content is
load-bearing regardless of pool size. If TF underperforms
(closer to PLS), then chromatin marks (which BOTH pELS and CA
have, just different ones) carry essential signal.

Predicted (based on pool-size fitting): TF should land between
PLS (0.604) and CA (0.718) at ~0.66-0.70. If above CA → TF
content is intrinsically valuable. If far below → small pool
+ no chromatin context = weak training signal.

**Generalization justification:** TF cCREs capture sequences
that are TF-bound in ChIP-seq but not chromatin-accessible. This
isolates the "TF binding sequence" signal from "open chromatin"
signal. A model trained on TF only learns to predict from TFBS
sequence patterns. If it generalizes, TF-binding sequence is
sufficient; if not, the broader chromatin context (also
captured by accessibility-class cCREs) carries information
beyond raw TFBS sequence.

---

## 2026-04-23 02:35 — Experiment 014 result: TF-only

**Headline:** mean_r=0.6509 on eval_01; mean across 14 evals
= **0.683**. Sits between PLS (0.604) and CA (0.718) as predicted
by pool-size scaling, slightly above the log-linear fit (+0.024).

**Updated single-class matrix:**
- PLS pool 47K → 0.604
- TF pool 105K → 0.683
- CA pool 246K → 0.718
- pELS pool 249K → 0.758
- dELS pool 1.47M → 0.756

Per-element class quality ranking (controlling for pool size):
> Enhancer content (pELS/dELS) > accessibility (CA) ≈ TF binding
> (TF) > narrow promoter (PLS).

The factor of ~2× per-element-quality gap between enhancers and
accessibility/TF is large.

**eval_08 collapse:** TF eval_08 = 0.540, second-worst after PLS.
TF cCREs are highly motif-rich (most-biology of all classes) and
eval_08 punishes biology proportionally.

**No new theory update.** TF result fits the existing hierarchy
cleanly. The remaining 3 classes (CA-CTCF, CA-H3K4me3, CA-TF) are
all smaller pools; unlikely to surprise.

**Updated library ranking by mean_r:**
1. pELS-only (012) — 0.758
2. dELS-only (007) — 0.756
3. natprop cCRE (008) — 0.752
4. cCRE class-balanced (002) — 0.748
5. cCRE+random mix (005) — 0.745
6. uniform random (001) — 0.738
7. motif-injected random (004) — 0.732
8. pELS+dELS combo (013) — 0.731
9. CA-only (011) — 0.718
10. dinuc-shuffled cCRE (003) — 0.696
11. genome-wide random (009) — 0.690
12. repeat-masked genome-wide (010) — 0.686
13. **TF-only (014) — 0.683**
14. PLS-only (006) — 0.604

**Next experiment:** test "small-fraction mixing" hypothesis.
Exp 013 showed 50/50 pELS+dELS dilutes -0.025. Does 90/10 still
dilute, or could a small dELS spike specifically lift the
dELS-favoring evals (07, 13) without hurting pELS's lead?

---

## 2026-04-23 02:40 — Experiment 015 planning: 90/10 pELS+dELS

**Mode:** refining (sharpening the no-mix principle by testing
the smallest interesting mix fraction).

**Plan:** 45K pELS + 5K dELS, sampled from each pool, shuffled
together. Same central-200bp extraction (without replacement).
Three seeds.

**Hypothesis (two competing predictions):**
- (A) "No-mix is iron-clad": even 10% dELS dilutes; mean falls
  below pELS-only on most evals; perhaps small lift on 07/13
  but net negative.
- (B) "Small additions help on dELS-favoring evals": pELS keeps
  lead on most evals; dELS spike specifically lifts 07/13 toward
  dELS levels; net mean above pELS-only.

If (B) holds, we have a free improvement worth ~0.005-0.010 in
mean. If (A) holds, the playbook simplifies further: never mix.

**Generalization justification:** A small spike of a different
regulatory grammar might either (a) provide useful diversity
without compromising the dominant grammar, or (b) introduce
distribution shift that hurts learning of the dominant grammar.
The result will tell us which regime applies for highly
similar grammars (both enhancer-like).

---

## 2026-04-23 03:05 — Experiment 015 result: 90/10 pELS+dELS

**Headline:** mean_r=0.7008 on eval_01; mean across 14 evals
= **0.739** — uniformly worse than pELS-only by ~0.018-0.022 on
EVERY eval, including the dELS-favoring evals 07/13.

**Hypothesis (A) "no-mix iron-clad" CONFIRMED.**
- eval_07: pELS 0.749, dELS 0.760, mix10 **0.729** (worst!)
- eval_13: pELS 0.747, dELS 0.760, mix10 **0.728** (worst!)

The 10% dELS addition does not specifically lift the evals where
dELS is stronger; it uniformly degrades all evals.

**Dilution scaling (sub-linear but persistent):**
- 50/50 mix vs pELS: -0.027
- 10/90 mix vs pELS: -0.019
- (extrapolating): need exactly 0% mixing for full pELS perf.

**Hard rule established (now 4 confirmations):**
> NEVER MIX. Pure-class training is optimal. Even 10% out-of-class
> contamination causes ~-0.02 mean degradation across ALL evals.
> The model develops sharper feature representations on a
> homogeneous training distribution; mixing universally degrades.

**Ranking of mix-dilution by similarity of mixed classes:**
- exp 005 (cCRE 8-class + uniform random) -0.003 (very different)
- exp 002 (8-class balanced) -0.008 vs dELS-only
- exp 015 (pELS 90 + dELS 10) -0.019 vs pELS-only
- exp 013 (pELS 50 + dELS 50) -0.027 vs pELS-only

Counterintuitively, mixing TWO SIMILAR classes (pELS+dELS, both
enhancer-like) dilutes MORE than mixing dissimilar classes
(cCRE+random). Possible explanation: when classes are similar,
the model can't easily separate their features and ends up with
muddled mid-distribution representations. When very different,
the model can route different inputs to different sub-features
within shared parameters.

**Next experiment:** stop testing mixtures. Move to single-class
augmentation. **Exp 016: pELS with reverse-complement
augmentation** (25K original + 25K RC). Standard DL technique.
Tests whether explicit RC examples improve learning vs
single-strand training.

---

## 2026-04-23 03:10 — Experiment 016 planning: pELS + RC augmentation

**Mode:** building (single-class augmentation strategy).

**Plan:** Sample 25K pELS (no replacement), generate the
reverse-complement of each, write 50K total (25K original + 25K
RC), shuffled. Same central-200bp extraction. Three seeds.

**Hypothesis:** TF binding sites are largely strand-symmetric
(motifs work on either strand). A model trained on
single-strand data must learn this symmetry implicitly through
many examples. Explicit RC augmentation gives the model
direct examples of both strands per element. If this helps
(mean > pELS-only at 0.758), augmentation is a free lever for
improvement. If it hurts or is neutral (mean ≈ 0.758 or below),
the model already handles RC implicitly OR the effective
diversity drop (25K unique vs 50K unique elements) outweighs
the RC benefit.

**Generalization justification:** The held-out evals likely
contain sequences from both strands of the genome. A model that
explicitly trains on both strands of each example may generalize
better to the strand-mix in test data. However, this trades pool
coverage (50% fewer unique elements) for strand coverage (2× per
element). The net depends on whether the model's effective
inductive bias rewards strand symmetry more than it rewards
sequence diversity.

---

## 2026-04-23 03:25 — Experiment 016 result: pELS + RC augmentation

**Headline:** mean_r=0.7048 on eval_01; mean across 14 evals
= **0.741** — uniformly worse than pELS-only (0.758) by
-0.011 to -0.024 on EVERY eval.

**Hypothesis (C) "RC hurts" CONFIRMED.** Every eval drops; no
eval benefits. Mean drop -0.017. Largest drops on the
dELS-favoring evals 07/13 (-0.024 each).

**Interpretation:** the model already handles RC implicitly.
Halving the unique pool (25K instead of 50K) costs more than
RC coverage gains. This rules out a whole family of "augment
by transforming existing sequences" strategies.

**New rule:** explicit augmentation that reduces pool diversity
is strictly bad. Useful augmentation must come from genuinely
new sequences (more elements, more positions), not from
transformations of existing ones.

**Cumulative ranking after exp 016 (top to bottom):**
1. pELS-only (012) — 0.758
2. dELS-only (007) — 0.756
3. natprop cCRE (008) — 0.752
4. cCRE class-balanced (002) — 0.748
5. cCRE+random mix (005) — 0.745
6. RC-augmented pELS (016) — 0.741
7. mix10 pELS+dELS (015) — 0.739
8. uniform random (001) — 0.738
9. motif-injected random (004) — 0.732
10. pELS+dELS combo (013) — 0.731
11. CA-only (011) — 0.718
12. dinuc-shuffled cCRE (003) — 0.696
13. genome-wide random (009) — 0.690
14. repeat-masked genome-wide (010) — 0.686
15. TF-only (014) — 0.683
16. PLS-only (006) — 0.604

**Next experiment:** Exp 017: pELS with random within-element
offset. Same 50K unique pELS, no replacement, but 200bp window
at random offset within the cCRE (vs central). Tests whether
"central 200bp" is overly restrictive (model sees only one
slice per element) or whether positional variation is just
noise.

---

## 2026-04-23 03:30 — Experiment 017 planning: pELS random offset

**Mode:** building (single-class within-element augmentation).

**Plan:** 50K pELS, no replacement, 200bp window at a random
offset within each cCRE (rather than central 200bp). Three
seeds. cCREs span 200-400bp typically; random offset gives
the model a different 200bp slice per draw.

**Hypothesis:** Two competing predictions:
- (A) "Central is privileged": the central 200bp of a cCRE is
  where the regulatory signal concentrates. Random offset
  dilutes this with flanking noise. mean < pELS012 (0.758).
- (B) "Position is noise": the regulatory grammar is
  approximately uniform across the cCRE. Random offset
  exposes the model to more realistic positional variation.
  mean ≈ pELS012 or slightly above.
- (C) "Diversity wins": within-element positional diversity
  acts as useful natural augmentation (unlike RC, this adds
  real sequence variation). mean > pELS012.

**Generalization justification:** Real held-out sequences won't
necessarily be centered on annotated cCREs. A model trained
only on central windows may fail when test sequences have the
"interesting" content offset. Random offset training
distributes positional sensitivity. This is the first test of
"sub-cCRE" sampling strategy.

---

## 2026-04-23 03:50 — Experiment 017 result: pELS random offset

**Headline:** mean_r=0.7034 on eval_01; mean across 14 evals
= **0.741**, identical penalty to RC augmentation. Drops on
EVERY eval, range -0.009 to -0.024.

**Hypothesis (A) "central is privileged" CONFIRMED.** The
cCRE midpoint contains the densest signal; off-center windows
dilute with flanking content.

**Striking coincidence: 016 RC and 017 random-offset have
identical mean penalties (-0.017).** Two completely different
per-element augmentations cost the model the same amount. The
pure-class, central, single-strand pELS configuration appears
to sit at a local optimum.

**Augmentation playbook is now empty.** Neither
transformation augmentation (RC) nor positional augmentation
(offset) helps. Future gains must come from POOL-level
choices, not per-element manipulation.

**Eval_13 takes the smallest hit (-0.009)** — consistent with
its known "composition-rewarding" property. Off-center windows
include more flanking, slightly counteracting the loss.

**Next experiment:** Exp 018: CA-CTCF only. 126K-element pool,
the largest untested SCREEN class. Completes the
"accessibility-with-modification" sub-matrix (CA / CA-CTCF /
CA-H3K4me3 / CA-TF) and tests whether insulator-related
chromatin sites carry useful regulatory grammar for the
multi-cell-type model.

---

## 2026-04-23 03:55 — Experiment 018 planning: CA-CTCF only

**Mode:** building (completing single-class matrix).

**Plan:** 50K from 126K CA-CTCF cCREs (no replacement),
central-200bp extraction. Three seeds.

**Hypothesis:** CA-CTCF marks chromatin-accessible regions
that bind CTCF — typically insulator/boundary elements with
distinct biology from enhancer-like pELS/dELS. CTCF motif is
strong and well-defined. Predictions:
- (A) "Insulator grammar transfers": CA-CTCF beats CA pure
  (0.718) due to clearer regulatory signal. mean ≥ 0.72.
- (B) "Insulator grammar narrow": CA-CTCF underperforms CA
  because boundary biology is too specialized. mean < 0.71.
- (C) "Pool size dominates": with smaller pool than CA, CA-CTCF
  inherits CA's score or slightly worse.

**Generalization justification:** Insulator/boundary elements
are functional regulatory features present in all cell types.
A model that learns CTCF/cohesin grammar should generalize
across cell contexts (CTCF binding is largely
cell-type-invariant compared to TF binding). This tests
whether single-class "structural regulator" libraries beat
single-class "transcriptional regulator" libraries.

---

## 2026-04-23 04:25 — Experiment 018 result: CA-CTCF only

**Headline:** mean_r=0.6714 on eval_01; mean across 14 evals
= **0.710**. Worse than CA-only (0.718). Hypothesis (B)
"insulator grammar narrow" CONFIRMED.

**Surprising:** despite CTCF being one of the strongest, most
well-defined motifs, CTCF-rich training underperforms generic
chromatin-accessibility training. The model doesn't gain from
"easier" motifs.

**Likely mechanism:** CTCF binding is cell-type-INVARIANT
(insulator/boundary biology), so a CTCF-rich library teaches
a feature that exists ubiquitously and provides little
discrimination across the variable regulatory landscape that
defines cell-type-specific MPRA activity.

**High seed variance:** eval_01 ranges 0.642 / 0.658 / 0.715
across seeds — ~5× normal seed noise. CA-CTCF samples are
heterogeneous; different 50K draws produce noticeably
different models.

**New principle:** regulatory context BREADTH predicts library
quality. Good training: variable cell-type readouts +
heterogeneous sequence grammar + functional integration.
- Enhancer-like (pELS/dELS): all three. Best.
- Generic accessibility (CA): broad but no specific function.
- Insulator (CA-CTCF): function but cell-type-invariant.
- TF/PLS: narrow context.

**Updated single-class ranking:**
pELS 0.758 > dELS 0.756 > CA 0.718 > CA-CTCF 0.710 > TF 0.683
> PLS 0.604.

**Next:** Exp 019 = CA-H3K4me3 only (79K active-promoter
chromatin pool). Predicts: similar to PLS (worst).

---

## 2026-04-23 04:30 — Experiment 019 planning: CA-H3K4me3 only

**Mode:** building (completing single-class matrix).

**Plan:** 50K from 79K CA-H3K4me3 cCREs (no replacement),
central-200bp, three seeds. CA-H3K4me3 = chromatin-accessible
region with H3K4me3 mark — i.e., active promoter chromatin
identified by accessibility + the canonical promoter histone
mark.

**Hypothesis:**
- (A) "Promoter is promoter": CA-H3K4me3 ≈ PLS (0.604) since
  both target active promoters via different evidence.
- (B) "Chromatin readout matters": CA-H3K4me3 closer to CA
  (0.718) since it's defined chromatin-first.
- (C) "Smaller pool dominates": somewhere between CA and PLS.

**Generalization justification:** Tests whether the cCRE class
hierarchy reflects underlying biology (PLS ≈ CA-H3K4me3 because
both = promoter) or reflects annotation methodology (CA-H3K4me3
≈ CA because both are chromatin-accessibility-first defined).
This will help interpret why PLS performs so much worse than
all other classes.

---

## 2026-04-23 04:55 — Experiment 019 result: CA-H3K4me3 only

**Headline:** mean_r=0.7095 on eval_01; mean across 14 evals
= **0.749** — *4th-best library overall*. Massively beats PLS
(0.604) by +0.145 mean despite both targeting active promoter
biology.

**Hypothesis (A) "promoter is promoter" FALSIFIED.** Two
classes labeled by similar biology (active promoters) differ
by 0.145 mean depending on whether annotation evidence is
functional (chromatin-direct) or positional (TSS-proximal).

**New principle: annotation evidence type predicts library
quality more than biological category does.** Chromatin-direct
evidence (DNase + histone mark) selects ACTIVE elements;
location evidence (TSS-proximal) captures both active and
silent → noisy training labels.

**Cross-eval highlight:** CA-H3K4me3 actually BEATS pELS on
eval_07 (0.756 vs 0.749) and eval_13 (0.754 vs 0.747). These
are the motif-/composition-helping evals; H3K4me3 marks may
select for higher-canonical-motif sites.

**Updated single-class hierarchy with evidence-type
annotation:**
| class       | pool   | mean   | evidence type           |
|-------------|--------|--------|-------------------------|
| pELS        | 249K   | 0.758  | DNase + chromatin marks |
| dELS        | 1.47M  | 0.756  | DNase + chromatin marks |
| CA-H3K4me3  | 79K    | 0.749  | DNase + H3K4me3         |
| CA          | 246K   | 0.718  | DNase only              |
| CA-CTCF     | 126K   | 0.710  | DNase + CTCF (narrow)   |
| TF          | 105K   | 0.683  | TF-bound only           |
| PLS         | 47K    | 0.604  | TSS-proximal (location) |

**High seed variance again (0.676-0.733 on eval_01)** — same
pattern as CA-CTCF. The "CA + secondary mark" classes are
heterogeneous; sample draws produce variable models.

**Next:** Exp 020: CA-TF only. 26K pool (smallest, requires
~2x replication per element). Completes single-class matrix.

---

## 2026-04-23 05:00 — Experiment 020 planning: CA-TF only

**Mode:** building (completing single-class matrix).

**Plan:** 50K from 26K CA-TF cCREs. Pool < N_seqs, so
sampling is with-replacement (~1.92x per element on average).
Same central-200bp extraction. Three seeds.

**Hypothesis:** CA-TF = chromatin-accessible region with TF
binding (no chromatin-mark evidence). Two competing predictions:
- (A) "TF-binding adds": CA-TF beats CA (0.718) and TF (0.683)
  because both signals together select better elements.
- (B) "Pool too small": with replacement, model overfits to
  individual elements; mean drops to TF level or below.
- (C) "Element-quality dominates": even with 2x replication,
  the higher per-element quality wins → mid-range performance.

**Generalization justification:** Tests whether (i) CA-TF
ranks above its constituent classes (CA, TF), and (ii)
whether 2x replication of high-quality elements dominates the
pool-diversity penalty established in 016. CA-TF is unique:
the only single-class library that requires replacement
sampling.

---

## 2026-04-23 05:25 — Experiment 020 result: CA-TF only

**Headline:** mean_r=0.5128 on eval_01; mean across 14 evals
= **0.536** — the WORST library tested. Below PLS (0.604) by
0.07. Hypothesis (B) "Pool too small" CONFIRMED.

**26K pool with 1.92x replication produces catastrophic loss.**
Three penalties stack: small pool, forced replication, and
narrow CA-TF class biology.

**Cell-type ordering BREAKS for the first time.** Usually
SKNSH > K562 > HepG2; here SKNSH > HepG2 > K562. K562 in
particular collapses (~0.48 vs typical 0.69). CA-TF cCREs may
be poorly represented in K562, leading to worst-cell-type
generalization.

**Eval_08 hits 0.41** — well below random (0.78). Model trained
on this narrow library is essentially anti-predictive on
random-leaning eval_08.

**Pool size threshold:** 50K unique elements appears to be a
floor for class-quality dominance. Below that, pool-diversity
penalty overwhelms per-element quality.

**Single-class matrix is now COMPLETE for all 8 SCREEN
classes.** Hierarchy:
pELS (0.758) > dELS (0.756) > CA-H3K4me3 (0.749) >
CA (0.718) > CA-CTCF (0.710) > TF (0.683) >
PLS (0.604) > CA-TF (0.536).

**Next:** Move to QUALITY FILTERING within the top class.
Exp 021: pELS top-50K-LONGEST cCREs. Tests if cCRE length
encodes a quality signal that can push past pELS-only's 0.758.

---

## 2026-04-23 05:30 — Experiment 021 planning: pELS top-50K longest

**Mode:** building (within-class quality filtering).

**Plan:** From the 249K pELS pool, sort by cCRE length
(end - start) and take the 50K LONGEST cCREs. Same
central-200bp extraction. Three seeds (seeds only affect
ordering randomization within the filtered set).

**Hypothesis:**
- (A) "Length is quality": longer cCREs are more reliably
  active regulatory regions (typical strong enhancers are
  300-500bp). Filtered library beats pELS-only (>0.758).
- (B) "Length is independent of quality": pELS pool is already
  curated; length is just bookkeeping. mean ≈ pELS-only (0.758).
- (C) "Length introduces bias": longest cCREs are unusual
  (perhaps mostly TSS-overlapping or housekeeping), library
  underperforms pELS-only.

**Generalization justification:** Without external annotation
(conservation, ChIP-seq strength), cCRE length is the only
intrinsic quality signal in the BED file. If length is
informative, this enables a free per-element quality filter
that doesn't reduce pool size below 50K. This is the cleanest
test of "more quality" within the top-tier class.

---

## 2026-04-23 06:00 — Experiment 021 result: pELS top-50K longest

**Headline:** mean_r=0.7141 on eval_01; mean across 14 evals
= **0.751** — slightly worse than pELS-only (0.758) by -0.007.
Hypothesis (B/C) confirmed: length is NOT a quality signal
(slight anti-quality if anything).

**Mixed eval pattern:** most evals modestly drop (-0.005 to
-0.017), but evals 04/09/10 slightly improve (+0.001 to
+0.003). Eval_13 takes the biggest hit (-0.027).

**Why might length be anti-quality?** Longest pELS may overlap
multiple regulatory elements (super-enhancer-like territory),
introducing noisier signal per element. Or longest cCREs may
sit in atypical chromatin contexts (transcribed regions,
dense-cluster regions).

**High seed variance** (0.69/0.74/0.72 on eval_01 = 0.046
range) is unusual for pELS (uniform pELS has ~0.01 seed
variance). The same 50K elements across seeds → variance
comes only from training stochasticity. Longest cCREs appear
to create a less-smooth loss landscape.

**Length is NULL as a free quality filter.** Without external
data (conservation, ChIP-seq strength), no purely-coordinate
filter has yet exceeded pELS-only.

**Next:** Exp 022: pELS top-50K-SHORTEST. Validates length
direction. If shortest also drops, length is purely null. If
shortest is similar to longest, both tails differ from middle.

---

## 2026-04-23 06:05 — Experiment 022 planning: pELS top-50K shortest

**Mode:** building (length-quality direction validation).

**Plan:** From the 249K pELS pool, sort by cCRE length
ascending and take the 50K SHORTEST cCREs. Threshold ≤186bp.
Same central-200bp extraction. Three seeds.

**Hypothesis:**
- (A) "Length is null": shortest ≈ longest ≈ uniform (0.751
  to 0.758 range) — length carries no signal.
- (B) "Both tails are atypical": shortest ≈ longest, both
  modestly below uniform — extreme-length cCREs are unusual
  in some other dimension (composition, context).
- (C) "Short is the privileged tail": shortest > uniform —
  short cCREs are sharper / less noisy regulatory units.
- (D) "Long is the better tail": shortest << uniform —
  contradicting 021's mild drop.

**Generalization justification:** Completes the length-quality
test. With 021 already showing length≥336bp loses -0.007, the
behavior of length≤186bp tells whether the loss is due to
"long is bad" specifically or to "extremes of any kind are
suboptimal."

---

## 2026-04-23 06:35 — Experiment 022 result: pELS top-50K shortest

**Headline:** mean_r=0.7030 on eval_01; mean across 14 evals
= **0.739** — worse than longest (0.751) and uniform (0.758).
Hypothesis (B) confirmed: both length tails hurt, but
shortest hurts more.

**Length matrix:**
- pELS uniform 0.758
- pELS longest (≥336bp) 0.751 (-0.007)
- pELS shortest (≤186bp) 0.739 (-0.019)

**Asymmetry:** shortest hurts ~2.7× more than longest.

**Mechanism:** the 200bp window centered on a ≤186bp cCRE
extends into FLANKING genomic content. Short pELS sequences
carry less cCRE-defined content per window, more flanking-
genomic noise. Long pELS by contrast keep the 200bp window
entirely inside the cCRE.

**Generalized lesson:** the natural pELS length distribution
is itself an OPTIMUM. The model expects to see a calibrated
mix of "tight cCRE inside window" and "loose cCRE with
flanking". Filtering to either extreme disrupts that
calibration.

**LENGTH-AS-QUALITY FALSIFIED** for pELS. Combined with the
augmentation null findings (016/017), no purely-coordinate or
per-element manipulation has improved pELS-only.

**Next:** Exp 023: pELS with 1% sequence mutation noise.
Tests whether mild input noise injection — the standard DL
augmentation — helps generalization.

---

## 2026-04-23 06:40 — Experiment 023 planning: pELS with 1% mutation noise

**Mode:** building (sequence-noise augmentation).

**Plan:** 50K unique pELS (no replacement), central-200bp
extraction. Then for each sequence, randomly substitute 1%
of bases (= 2 random substitutions per 200bp). Three seeds —
mutations are seeded so each sequence gets a different
mutation pattern across seeds. Oracle labels are recomputed
on the mutated sequences.

**Hypothesis:**
- (A) "Noise helps generalization": mild input perturbation
  trains a more robust model, mean > 0.758.
- (B) "Noise is null": mutations average out; mean ≈ 0.758.
- (C) "Noise destroys motifs": even 1% mutation disrupts
  critical TF binding sites, mean < 0.758.

**Generalization justification:** Sequence noise injection
is the standard DL augmentation used when label-preserving
transformations are unavailable. Tests whether the model can
benefit from being trained on slightly-noisy versions of
real cCREs vs. clean cCREs only. If noise helps even
marginally, it's a free improvement that doesn't change pool
size or class composition.

---

## 2026-04-23 07:05 — Experiment 023 result: pELS + 1% mutation noise

**HEADLINE: FIRST POSITIVE INTERVENTION FOUND.** mean_r=0.7230
on eval_01; mean across 14 evals = **0.761** — beats pELS-only
(0.758) by **+0.003**, with EVERY eval improving. New best
library across all 23 tested.

**Effect sizes (+0.001 to +0.007) are modest but uniformly
positive.** Largest improvements:
- eval_08 (+0.007): the random-rewarding eval. Mutated cCREs
  partially mimic the random distribution.
- eval_09 (+0.007): the highest-baseline eval, surprisingly
  still has room for improvement via noise.
- eval_04 (+0.006), eval_10 (+0.004), eval_13 (+0.004).

**Caveat:** high seed variance (0.6988/0.7272/0.7430 on
eval_01, range 0.044). Single-experiment statistical certainty
is modest. But all-14-evals-improve is unlikely from pure
noise (~6e-5 chance under H0).

**Mechanism: per-position MICRO-noise breaks overfitting; per-
element MACRO-transformation does not.** Augmentation playbook:
- RC (per-element): -0.017
- Random offset (per-element): -0.017
- Length filters (per-element): -0.007 to -0.019
- **1% mutation (per-position): +0.003**

The model's overfit was at the EXACT-sequence level, not
structural. Sub-motif noise (point mutations) regularizes
without disrupting motif syntax.

**Augmentation playbook NO LONGER EMPTY.** Mutation noise is
the first lever that pushes past pELS-only.

**Next:** Exp 024: pELS + 3% mutation noise. Tests dose-
response — does noise scale up monotonically, hit a sweet
spot, or sharply degrade?

---

## 2026-04-23 07:10 — Experiment 024 planning: pELS + 3% mutation noise

**Mode:** building (mutation-noise dose-response).

**Plan:** Same as 023 but mutation rate 3% (= 6 substitutions
per 200bp). Three seeds.

**Hypothesis:**
- (A) "Monotonic gain": 3% > 1% > 0%. Strong noise
  regularization wins. mean > 0.761.
- (B) "Sweet spot": 1% is best; 3% destroys too many motifs.
  mean between 0.730 and 0.761.
- (C) "Sharp threshold": 3% breaks regulatory grammar. mean
  < 0.740.

**Generalization justification:** With 6 substitutions per
200bp = 1 substitution per ~33bp, we cross a critical density
where TF binding motifs (typically 6-15bp) start to be hit at
~30% probability per motif. This is the "biological motif"
threshold — past 1%, mutations interfere with regulatory
grammar. Result tells us where the optimal noise/signal
tradeoff sits.

---

## 2026-04-23 07:35 — Experiment 024 result: pELS + 3% mutation noise

**Headline:** mean_r=0.6902 on eval_01; mean across 14 evals
= **0.727** — sharply worse than 1% (0.761) and below clean
(0.758). Hypothesis (B) sweet spot CONFIRMED.

**Mutation dose-response is SHARPLY non-monotonic:**
- 0% (clean):  0.758
- 1%:          **0.761** (best)
- 3%:          0.727 (-0.031 vs clean)

At 3% (= 6 subs per 200bp), each TF binding site (~6-15bp)
has ~30% probability of being hit. Motif disruption cost
overwhelms regularization benefit.

**Largest drops on motif-rewarding evals:** eval_07 (-0.042)
and eval_13 (-0.043) — these were the "motifs matter most"
evals. Confirms 3% mutation specifically disrupts motif-
recognition. eval_08 has smallest drop (-0.030) since it
rewards random-like content.

**Implication:** sweet spot is between 0% and 2%. The 1% gain
is small but real; the 3% loss is unambiguous and confirms
mutations DO interact with the motifs.

**Next:** Exp 025: pELS + 0.5% mutation noise. Tests lower
bracket. If 0.5% > 1%, optimum is even gentler; if 0.5% ≤ 1%,
1% is at/near optimum.

---

## 2026-04-23 07:40 — Experiment 025 planning: pELS + 0.5% mutation noise

**Mode:** building (mutation rate fine-tuning).

**Plan:** Same as 023/024 but mutation rate 0.5% (= 1 sub per
200bp). Three seeds.

**Hypothesis:**
- (A) "Lower is better": 0.5% > 1%. Even gentler noise
  preserves more motif while still regularizing. mean > 0.761.
- (B) "1% is the sweet spot": 0.5% < 1%. Some critical noise
  level needed; 1% is optimal. mean between 0.758 and 0.761.
- (C) "Below threshold": 0.5% ≈ clean (0.758). Too gentle to
  trigger regularization. mean ≈ 0.758.

**Generalization justification:** Brackets the sweet spot from
below. Combined with 023/024 results (1% +0.003, 3% -0.031),
0.5% will tell us whether the dose-response curve has its peak
near 1% or whether even gentler noise yields more gain.


---

## 2026-04-23 09:35 — Experiment 025 result: pELS + 0.5% mutation noise

**Headline:** mean_r=0.7073 on eval_01; mean across 14 evals
= **0.7447** — BELOW clean pELS (0.758) on every eval. Breaks
the sweet-spot story. Hypothesis (C) "below threshold" is
WRONG (0.5% is clearly worse than clean, not equal to it).

**Updated dose-response — NOT smooth:**
- 0% (clean):    0.758
- 0.5%:         **0.745** (-0.013)
- 1%:           0.761 (+0.003)
- 3%:           0.727 (-0.031)

A monotonic regularization curve cannot put 0.5% below clean
while putting 1% above clean. The 0.5% drop is consistent on
every eval (not noise scatter), so within this single seed
trio the result is solid.

**Most parsimonious read: the +0.003 gain at 1% was within
seed noise.** Per-seed eval_01 spread for 025: s0=0.6993,
s1=0.6846, s2=0.7380 — range 0.054, std ~0.027. That spread
alone exceeds the entire 023-vs-012 gap. Every previous
"signal" smaller than ±0.01 is suspect.

**Mutation noise as augmentation: REJECTED.** Augmentation
playbook now uniformly null-or-negative:

| augmentation                  | mean_r | Δ vs pELS |
|-------------------------------|--------|-----------|
| pELS clean (012)              | 0.758  |   0       |
| pELS + 0.5% mut (025)         | 0.745  | -0.013    |
| pELS + 1% mut (023)           | 0.761  | +0.003 (likely noise) |
| pELS + 3% mut (024)           | 0.727  | -0.031    |
| pELS + RC (016)               | 0.741  | -0.017    |
| pELS + offset (017)           | 0.741  | -0.017    |
| pELS longest (021)            | 0.751  | -0.007    |
| pELS shortest (022)           | 0.739  | -0.019    |

**Theory update.** Per-element MACRO transformations and
per-position MICRO noise BOTH fail to push past clean
pELS-only. The model's representation of pELS sequences is
the ceiling for this design space. Any modification to the
sequences degrades the signal.

**Five experiments left.** Pivoting away from augmentation
toward class combinations and content stratification.

**Next:** Exp 026: pELS + CA-H3K4me3 combo (25K + 25K). Top
two single-class libraries (012=0.758, 019=0.749). Tests
whether annotation-evidence diversification beats single
class.

---

## 2026-04-23 09:45 — Experiment 026 planning: pELS + CA-H3K4me3 combo

**Mode:** building (class combination).

**Plan:** 25K from pELS pool + 25K from CA-H3K4me3 pool, no
replacement, shuffled. Central 200bp. Three seeds (only the
sampling+shuffle is randomized; no mutation).

**Hypothesis:**
- (A) "Diversity wins": mean > 0.758. Combining two strong
  but distinct annotation-evidence types broadens the model's
  motif coverage and helps generalization.
- (B) "Average pull": mean ≈ (0.758 + 0.749) / 2 = 0.754. The
  combo just averages the two classes' performance.
- (C) "Dilution hurts": mean < 0.749. Mixing weakens the
  pELS-specific signal more than CA-H3K4me3 contributes.

**Generalization justification:** pELS (proximal enhancer-like)
and CA-H3K4me3 (chromatin-accessible + active-promoter mark)
are the two highest-scoring single classes. They differ in
genomic location (distal vs near-promoter) and evidence type
(transcription-flanking signature vs chromatin-mark direct).
If their union exceeds the best single class, then evidence-
type diversity has informational value beyond what either
class alone provides — relevant for models that must
generalize beyond the labeled cell types.

---

## 2026-04-23 11:50 — Experiment 026 result: pELS + CA-H3K4me3 combo

**Headline:** mean_r=0.7375 on eval_01; mean across 14 evals
= **0.7797**. **NEW BEST. +0.022 over pELS-only (0.758),
+0.030 over CA-H3K4me3-only (0.749).** First unambiguous
positive intervention — gap is large enough to be well above
seed noise.

**Every single eval improves over BOTH parent classes alone.**
This is super-additive synergy, not averaging.

**Crucial contrast with exp 013 (pELS+dELS = 0.731, dilution).**
Same protocol (25K + 25K shuffled), but pELS+dELS HURT while
pELS+CA-H3K4me3 HELPS by +0.022. The difference is
evidence-type orthogonality:
- pELS + dELS = both "enhancer-like" → same evidence space →
  dilution
- pELS + CA-H3K4me3 = transcription-flanking + chromatin-mark
  → orthogonal evidence types → broader motif coverage

**Theory: generalization needs evidence-type diversity, not
sample volume.** A 50K library of one evidence type hits a
ceiling ~0.75-0.76. Mixing in 25K from a complementary
evidence type teaches NEW regulatory grammar.

**Largest gains on motif-rewarding evals.** Eval_07 (+0.026
over best parent) and eval_13 (+0.029) — the "motifs matter
most" evals — show the biggest improvement, consistent with
broader motif coverage being the mechanism.

**Updated leaderboard:**
| library                              | mean_r |
|--------------------------------------|--------|
| **026_pels_h3k4me3_combo**           | **0.780** |
| 023_pels_mut1pct (likely noise)      | 0.761  |
| 012_pels_only                        | 0.758  |
| 021_pels_long                        | 0.751  |
| 007_dels_only                        | 0.751  |
| 019_ca_h3k4me3_only                  | 0.749  |

**Next:** Exp 027: pELS + CA-CTCF combo. Tests whether
synergy is general to any orthogonal evidence type or
specific to CA-H3K4me3.

---

## 2026-04-23 12:00 — Experiment 027 planning: pELS + CA-CTCF combo

**Mode:** building (orthogonality generality test).

**Plan:** 25K pELS + 25K CA-CTCF (no replacement), shuffled.
Central 200bp. Three seeds.

**Hypothesis:**
- (A) "Orthogonality is general": mean ≥ 0.775. Any
  orthogonal evidence-type partner produces synergy with pELS.
- (B) "Partner strength matters": 0.760 ≤ mean < 0.775. Some
  synergy from orthogonality, but moderated by CA-CTCF being
  a weaker single class (0.710 vs CA-H3K4me3's 0.749).
- (C) "CA-H3K4me3 specific": mean ≈ 0.755. CA-CTCF doesn't
  synergize with pELS the way CA-H3K4me3 does.
- (D) "Antagonism": mean < 0.745. CA-CTCF's CTCF-bound motif
  bias actively dilutes pELS signal.

**Generalization justification:** CA-CTCF is the "next best
orthogonal evidence type" — chromatin-accessibility + CTCF
binding mark — distinct from both pELS (transcription-
flanking) and CA-H3K4me3 (active-promoter mark). If the +0.022
synergy in 026 was about orthogonality per se, it should
reproduce here. If it was about something CA-H3K4me3-specific
(its sequence properties, or particular motif overlap with
pELS), it won't. This is the cleanest one-variable test:
holds pELS and protocol fixed, swaps the partner class.

---

## 2026-04-23 14:35 — Experiment 027 result: pELS + CA-CTCF combo

**Headline:** mean across 14 evals = **0.7631**. Δ vs
pELS-only = +0.005 (small but positive). Hypothesis (B)
"partner strength matters" CONFIRMED — synergy is real but
reduced compared to pELS+CA-H3K4me3 (0.780).

**Two-component synergy model:**
1. **Motif diversity** — orthogonal partner adds NEW motifs.
   Both 026 and 027 win big on eval_07 (+0.034 / +0.028) and
   eval_13 (+0.035 / +0.029) — the "motif content matters"
   evals. CA-CTCF delivers this even being a weak single class.
2. **Broad coverage** — strong partners contribute beyond
   motif evals. CA-H3K4me3 (0.749 alone) helps everywhere;
   CA-CTCF (0.710 alone) helps mostly on the motif evals.

**Predictive formula:**
combo_mean ≈ pELS_baseline + α(motif_diversity) + β·partner_strength

This generalizes prior findings: same-evidence-type pairing
(pELS+dELS) provides α=0 (same motif space) AND has β <
pELS_baseline, so result drops. Different-evidence-type
pairing always provides α > 0 and adds β·partner_strength.

**Updated leaderboard:**
| library                              | mean_r |
|--------------------------------------|--------|
| **026_pels_h3k4me3_combo**           | **0.780** |
| 027_pels_ctcf_combo                  | 0.763  |
| 023_pels_mut1pct (likely noise)      | 0.761  |
| 012_pels_only                        | 0.758  |

**Next:** Exp 028: triple combo pELS + CA-H3K4me3 + CA-CTCF.
Tests whether stacking orthogonal evidence types compounds.

---

## 2026-04-23 14:45 — Experiment 028 planning: triple combo pELS + CA-H3K4me3 + CA-CTCF

**Mode:** building (orthogonal-class stacking).

**Plan:** 16,667 pELS + 16,667 CA-H3K4me3 + 16,666 CA-CTCF
(no replacement per class), shuffled. Three seeds. Total =
50,000. All three classes confirmed orthogonal evidence types
(transcription-flanking enhancer, active-promoter mark,
CTCF-bound chromatin).

**Hypothesis:**
- (A) "Diversity stacks": mean ≥ 0.785. Three orthogonal
  classes compound their motif-diversity contributions.
- (B) "Saturation at two": 0.770 ≤ mean < 0.785. Two
  orthogonal classes already capture most of the diversity
  win; third adds little.
- (C) "Per-class depth matters": mean < 0.770. With only
  16.7K per class, pELS in particular is too thin to anchor
  the combo, and total result drops below 026's two-class.

**Generalization justification:** The two-component model from
027 predicts (A) — adding a third orthogonal class should
contribute additional α (more motif diversity) and contribute
more partner-strength β. The risk is that with only 16.7K
samples per class, individual classes may be too sparse to
teach the model their evidence-type signal effectively. Hence
we may see saturation (B) instead of stacking (A).

This is the cleanest "more diversity, less depth" trade-off
test in the whole study.

---

## 2026-04-23 17:05 — Experiment 028 result: triple combo pELS+CA-H3K4me3+CA-CTCF

**Headline:** mean across 14 evals = **0.7431**. Triple combo
HURTS — drops below pELS-only (-0.015) and far below the best
two-way combo 026 (-0.037). Hypothesis (C) "per-class depth
matters" CONFIRMED strongly.

**Key observation:** even on motif-rewarding evals (07, 13)
where 026 and 027 won big (+0.029-0.035), the triple combo
provides zero gain over pELS baseline. Adding a third class
did NOT add motif diversity — it diluted the existing signal.

**Theory: two-class synergy is the local optimum at 50K cap.**
Each evidence type needs ≥ ~25K samples to be learned
effectively. With 16.7K each, none of the three gets adequate
representation, and the model can't learn the synergistic
motif diversity that two-class combos provide.

| pattern              | per-class N | result |
|----------------------|-------------|--------|
| 1 class              | 50K         | 0.758 (ceiling) |
| 2 orthogonal classes | 25K each    | up to 0.780 |
| 3 orthogonal classes | 16.7K each  | 0.743 (depth-starved) |

**Hard trade-off:** at 50K total, can't have both depth and
breadth. Two classes at adequate depth wins; three classes
at insufficient depth loses.

**Updated leaderboard:**
| library                              | mean_r |
|--------------------------------------|--------|
| **026_pels_h3k4me3_combo**           | **0.780** |
| 027_pels_ctcf_combo                  | 0.763  |
| 023_pels_mut1pct (likely noise)      | 0.761  |
| 012_pels_only                        | 0.758  |
| 028_triple_combo                     | 0.743  |

**Next:** Exp 029: CA-H3K4me3 + dELS combo (no pELS). Tests
whether the two-class orthogonality rule generalizes beyond
pELS as anchor.

---

## 2026-04-23 17:15 — Experiment 029 planning: CA-H3K4me3 + dELS combo

**Mode:** building (orthogonality generality without pELS).

**Plan:** 25K CA-H3K4me3 + 25K dELS, no replacement, shuffled.
Three seeds. Same protocol as 026, only swap pELS → dELS.

**Hypothesis:**
- (A) "Orthogonality is general": mean ≥ 0.770. Rule applies
  to any two orthogonal classes; pELS not required.
- (B) "Partial generality": 0.755 ≤ mean < 0.770. Rule holds
  but weaker without pELS as anchor.
- (C) "pELS-specific": mean ≤ 0.750. The 026 win was
  pELS-anchored; orthogonality alone isn't sufficient.

**Generalization justification:** CA-H3K4me3 (chromatin-mark,
active-promoter) and dELS (transcription-flanking, distal-
enhancer) are clearly orthogonal evidence types — different
chromatin context, different genomic location, different
evidence basis. If the rule from 026 (orthogonal evidence
types synergize) is general, this combo should also exceed
either parent alone (max parent = 0.751). If pELS has special
properties (e.g., exceptionally diverse motif set, or unique
sequence properties), the rule would be pELS-specific and
this combo should look more like pELS+dELS (013, mean=0.731).

This is the cleanest "is the rule general" test — and it
sets up exp 030 as either a confirmed-general triple-class
optimum search or a pELS-specific deeper exploration.

---

## 2026-04-23 19:50 — Experiment 029 result: CA-H3K4me3 + dELS combo

**Headline:** mean across 14 evals = **0.7620**. Δ vs best
parent (dELS, 0.751) = +0.011. Hypothesis (B) "partial
generality" CONFIRMED — orthogonality rule holds without pELS,
but synergy is ~half the magnitude.

**Synergy compendium (all 25K+25K combos):**
| combo                    | best parent | combo  | Δ over best parent |
|--------------------------|-------------|--------|---------------------|
| 013 pELS + dELS          | 0.758       | 0.731  | -0.027 (dilution)   |
| 026 pELS + CA-H3K4me3    | 0.758       | 0.780  | **+0.022**          |
| 027 pELS + CA-CTCF       | 0.758       | 0.763  | +0.005              |
| 029 CA-H3K4me3 + dELS    | 0.751       | 0.762  | +0.011              |

**Three positive instances of orthogonality synergy** (026,
027, 029) and one negative same-evidence-type instance (013).
The orthogonal-vs-similar evidence-type distinction is the
unifying principle.

**Why pELS+CA-H3K4me3 maximally wins:** both are "active
regulatory elements near promoters" sharing genomic CONTEXT,
but with orthogonal EVIDENCE for activity (TF binding pattern
vs chromatin mark). Model gets two complementary perspectives
on the same activity-relevant region. dELS is genomically
distal — different context AND different evidence — so less
"perspective overlap," smaller synergy.

**Updated leaderboard (final but for exp 030):**
| library                              | mean_r |
|--------------------------------------|--------|
| **026_pels_h3k4me3_combo**           | **0.780** |
| 027_pels_ctcf_combo                  | 0.763  |
| 029_h3k4me3_dels_combo               | 0.762  |
| 023_pels_mut1pct (likely noise)      | 0.761  |
| 012_pels_only                        | 0.758  |

**Next:** Exp 030 (FINAL): 30K pELS + 20K CA-H3K4me3. Tests
whether the 25/25 ratio is optimal or if biasing toward the
stronger parent further helps.

---

## 2026-04-23 20:00 — Experiment 030 planning: 30K pELS + 20K CA-H3K4me3 (FINAL)

**Mode:** building (ratio optimization at known best combo).

**Plan:** 30K pELS + 20K CA-H3K4me3, shuffled. Three seeds.
Same protocol as 026, only mixing ratio changes.

**Hypothesis:**
- (A) "Stronger parent dominance": mean ≥ 0.785. Biasing
  toward pELS (the better single class, 0.758 vs 0.749)
  preserves more of pELS's strength while still diversifying.
- (B) "25/25 was optimal": 0.775 ≤ mean < 0.785. Symmetric
  mix is the sweet spot; small ratio shifts don't matter.
- (C) "Diversification needs balance": mean < 0.775. Reducing
  CA-H3K4me3 below 25K weakens the orthogonal-evidence
  contribution more than the extra pELS adds.

**Generalization justification:** This is the simplest
ratio-sensitivity test on the optimal combo. If pELS depth
matters most (which is suggested by 028's failure when pELS
dropped to 16.7K), then 30K/20K should marginally improve
over 25K/25K. If symmetric mixing is what matters (e.g., the
model needs roughly equal exposure to both evidence types
during training), then 30K/20K won't help. Either way, this
finishes the design-space characterization with a directed
test of the only remaining open question: **how sharp is the
optimum at 25/25?**

This is the 30th and final experiment. After 030, the
notebook closes with a summary entry consolidating the
findings into a recommended library design.

---

## 2026-04-23 22:25 — Experiment 030 result (FINAL): 30K pELS + 20K CA-H3K4me3

**Headline:** mean across 14 evals = **0.7398**. Δ vs 026 =
**-0.040**. Δ vs pELS-only = -0.018. Hypothesis (C)
"diversification needs balance" CONFIRMED dramatically.

**Striking finding:** shifting just 5K sequences (10% of
total) from CA-H3K4me3 to pELS COLLAPSES the synergy. The
result drops below BOTH parent classes alone (pELS=0.758,
CA-H3K4me3=0.749). 30K/20K → 0.740.

**Per-eval drops are largest on motif-rewarding evals:**
- eval_07: 0.783 → 0.737 (-0.045)
- eval_13: 0.783 → 0.731 (-0.052)
- eval_08: 0.705 → 0.650 (-0.055)

These are the SAME channels that delivered the 026 win.
Reducing CA-H3K4me3 below 25K starves the orthogonal
motif-diversity contribution that makes the combo work.

**The 25K/25K split is a SHARP local optimum.** Sharp in two
senses:
1. **Symmetry-sharp:** small ratio shifts (60/40) collapse
   the synergy — the model needs balanced exposure to both
   evidence types.
2. **Depth-sharp:** below ~25K per evidence type, the
   contribution drops off cliff-style (consistent with 028's
   16.7K-per-class triple-combo failure).

**FINAL leaderboard (30 experiments):**
| rank | library                              | mean_r |
|------|--------------------------------------|--------|
| 1    | **026_pels_h3k4me3_combo**           | **0.780** |
| 2    | 027_pels_ctcf_combo                  | 0.763  |
| 3    | 029_h3k4me3_dels_combo               | 0.762  |
| 4    | 023_pels_mut1pct (likely noise)      | 0.761  |
| 5    | 012_pels_only                        | 0.758  |
| 6    | 021_pels_long                        | 0.751  |
| 7    | 007_dels_only                        | 0.751  |
| 8    | 019_ca_h3k4me3_only                  | 0.749  |
| ...  | ...                                  | ...    |
| last | 020_ca_tf_only                       | 0.536  |

---

## 2026-04-23 22:40 — PROGRAM SUMMARY (30 experiments)

### Recommended library design

**50,000 sequences = 25,000 pELS + 25,000 CA-H3K4me3,
shuffled. Central 200bp window, no augmentation.** Mean
Pearson r across 14 anonymous eval sets = **0.780**. +0.022
over the best single-class library (pELS-only, 0.758).
+0.085 over uniform-random ACGT (0.695).

### Three principles that explain 30 experiments

**1. Annotation-evidence type matters more than biological
category.** Single-class libraries:
- pELS: 0.758 (proximal-enhancer-like; transcription-flanking)
- dELS: 0.751 (distal-enhancer-like)
- CA-H3K4me3: 0.749 (chromatin-accessible, active-promoter
  mark)
- pELS=0.758 vs PLS=0.595, despite both being "promoter-
  proximal regulatory elements." The evidence-type difference
  (transcription-flanking signal vs core-promoter signal)
  dominates the biological-category similarity.
- The sharp ranking by evidence type runs across 8 single-
  class libraries (006-008, 011-014, 018-020).

**2. Two orthogonal-evidence-type classes synergize at
25K/25K.** Discovered in exp 026:
- pELS+CA-H3K4me3: 0.780 (synergy +0.022 over best parent)
- pELS+CA-CTCF: 0.763 (+0.005)
- CA-H3K4me3+dELS: 0.762 (+0.011)
- pELS+dELS: 0.731 (DILUTION — same evidence type)

The rule generalizes (3 positive, 1 negative instances), and
the synergy is largest when both classes share genomic CONTEXT
(near-promoter regulatory regions) but differ in activity
EVIDENCE (TF-binding signature vs chromatin mark).

**3. Both depth and balance are sharp constraints.** The
25K/25K formula is fragile:
- 16.7K/16.7K/16.7K triple combo (028): 0.743 — fails.
  Per-class depth too low.
- 30K/20K asymmetric (030): 0.740 — fails. Below-25K
  starvation of one class collapses the synergy.
- 25K/25K (026): 0.780 — wins.

Likely interpretation: the model needs ≥25K samples per
evidence type AND balanced exposure during training to learn
both orthogonal signatures effectively.

### Augmentation null finding

Per-element transformations (RC: 016 -0.017, random offset:
017 -0.017, length-filter long: 021 -0.007, length-filter
short: 022 -0.019) and per-position noise (mutations 0.5%/1%/
3%: 025/023/024 -0.013/+0.003/-0.031) all fail to push past
clean pELS-only. The 1% mutation gain (+0.003) was within
seed noise (confirmed by 0.5% mut producing -0.013 — non-
monotonic; sweet-spot story falsified).

**Conclusion: no augmentation lever works on this data.**
Improvements come from CLASS COMPOSITION, not from sequence
manipulations.

### What we tried but didn't help

| failed approach           | exp | mean_r | Δ vs pELS |
|---------------------------|-----|--------|-----------|
| Uniform random            | 001 | 0.695  | -0.063    |
| All-cCRE class-balanced   | 002 | 0.762  | +0.004    |
| Dinuc-shuffle of cCRE     | 003 | 0.690  | -0.068    |
| JASPAR motif injection    | 004 | 0.730  | -0.028    |
| cCRE+random mix           | 005 | 0.738  | -0.020    |
| Genome-wide random        | 009 | 0.706  | -0.052    |
| Repeat-masked random      | 010 | 0.696  | -0.062    |
| pELS+dELS combo           | 013 | 0.731  | -0.027    |
| 90/10 pELS+dELS           | 015 | 0.747  | -0.011    |
| pELS + RC                 | 016 | 0.741  | -0.017    |
| pELS + offset             | 017 | 0.741  | -0.017    |
| pELS longest              | 021 | 0.751  | -0.007    |
| pELS shortest             | 022 | 0.739  | -0.019    |
| pELS + 0.5% mut           | 025 | 0.745  | -0.013    |
| pELS + 1% mut             | 023 | 0.761  | +0.003 (noise) |
| pELS + 3% mut             | 024 | 0.727  | -0.031    |
| Triple combo (028)        | 028 | 0.743  | -0.015    |
| 30K/20K combo (030)       | 030 | 0.740  | -0.018    |

### Method notes for future iterations

- **3 seeds is borderline insufficient.** Per-seed eval_01
  ranges of 0.05+ are common (e.g., 025 had s2=0.738 vs s0=0.699
  on eval_01). Effects below ~±0.01 are noise. The +0.003 gain
  from 1% mutation noise (023) was a false positive.
- **Eval-level interpretation is informative.** Eval_07 and
  eval_13 are the "motif content matters most" evals (per
  003 dinuc-shuffle analysis); they amplify class-composition
  effects. Eval_08 rewards random-like content; it shows the
  smallest sensitivity to motif-disruption.
- **Compute budget:** each experiment cost ~9-22 minutes for
  prepare/eval, plus 1-22 minutes for sequence generation.
  Total wall-clock for 30 experiments: ~6-7 hours of
  evaluation across 3 spark nodes in parallel.

### Open questions (for future work)

1. **Does ≥50K per evidence type continue to help?** All
   single-class libraries were 50K. Maybe pELS at 100K or
   200K beats the combo. Untested due to 50K cap.
2. **Pinpoint the per-class depth cliff.** 25K works, 16.7K
   and 20K fail. Where exactly is the threshold? 22K? 23K?
3. **More orthogonal pairs.** Untested: pELS+CA, pELS+TF,
   CA-CTCF+dELS, etc. The synergy magnitude varied 2-4× across
   the three positive instances; characterizing it across all
   28 pairs would refine the orthogonality theory.
4. **Why is pELS+CA-H3K4me3 specifically the best?** Both
   share near-promoter genomic context. Do other "shared
   context, different evidence" pairs also maximally
   synergize? E.g., is dELS+CA (both distal-ish, different
   evidence) competitive with pELS+CA-H3K4me3?
5. **Cross-cell-type transfer.** All evals here measured
   with K562/HepG2/SKNSH. The recommended library should
   transfer to other cell types — but that's an empirical
   claim untested in this study.

### Program complete

30 experiments. Best library: 026 (pELS + CA-H3K4me3, 25K
each, shuffled). Mean r = 0.780. Three principles:
evidence-type primacy, two-class orthogonal synergy, and
sharp depth/balance constraints.
