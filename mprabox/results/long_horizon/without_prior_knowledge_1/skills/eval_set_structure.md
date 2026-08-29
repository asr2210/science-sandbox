# Skill: known structure of the 14 anonymous eval sets

The 14 eval sets are anonymous, but each library experiment reveals
their relative difficulty. Treat this file as a living reference and
update it after every experiment.

## Baseline floor (from 001_uniform_random — pure random ACGT, 50K seqs)

| eval | mean_r | k562 | hepg2 | sknsh |
|------|--------|------|-------|-------|
| 01   | 0.6954 | 0.69 | 0.69  | 0.71  |  ← primary metric
| 02   | 0.7848 | 0.78 | 0.77  | 0.80  |
| 03   | 0.7612 | 0.76 | 0.74  | 0.78  |
| 04   | 0.7494 | 0.75 | 0.74  | 0.76  |
| 05   | 0.6951 | 0.69 | 0.69  | 0.71  |
| 06   | 0.7853 | 0.78 | 0.77  | 0.80  |
| 07   | 0.6684 | 0.68 | 0.65  | 0.67  |
| 08   | 0.7841 | 0.79 | 0.77  | 0.80  |
| 09   | 0.8115 | 0.81 | 0.80  | 0.82  |  ← highest baseline
| 10   | 0.7564 | 0.77 | 0.73  | 0.77  |
| 11   | 0.6833 | 0.68 | 0.68  | 0.69  |
| 12   | 0.6553 | 0.66 | 0.64  | 0.66  |  ← lowest baseline (most headroom)
| 13   | 0.6584 | 0.66 | 0.64  | 0.68  |
| 14   | 0.7851 | 0.78 | 0.77  | 0.80  |

## Observed clusters (refined after exp 002)

- **{01, 05}** — nearly identical scores in both random (0.6951/0.6954)
  and cCRE (0.7133/0.7133). Definitely paired/same.
- **{02, 06, 14}** — tight cluster on both libraries (~0.785 random,
  ~0.805 cCRE). Confirmed family.
- **{08}** — APPEARS to cluster with {02, 06, 14} on random (0.7841)
  but BREAKS away on cCRE (collapses to 0.6380, Δ = -0.146). eval_08
  is qualitatively different — it rewards random-like training and
  punishes natural regulatory DNA. Possibly contains synthetic /
  scrambled / random sequences as test examples.
- **{07, 13}** — biggest cCRE wins (+0.077, +0.084). Both were
  low-baseline on random; both respond strongly to natural regulatory
  grammar. These are the evals with the most accessible headroom for
  biology-aware libraries.
- **{12}** — low baseline (0.66 → 0.68 on cCRE). Smallest gain among
  low-baseline evals; harder to lift than 07/13.

## After exp 003, three signal axes per eval (motif vs composition vs random)

Compare random / cCRE / dinuc-shuffled-cCRE to decompose:
- (cCRE − shuf) = MOTIF contribution (positive = motifs help)
- (shuf − rand) = COMPOSITION contribution (positive = cCRE composition helps)
- best = best library so far

| eval | rand   | cCRE   | shuf   | motif  | comp   | best       |
|------|--------|--------|--------|--------|--------|------------|
| 01   | 0.6954 | 0.7133 | 0.6500 | +0.063 | -0.045 | cCRE 0.713 |
| 02   | 0.7848 | 0.8046 | 0.7343 | +0.070 | -0.051 | cCRE 0.805 |
| 03   | 0.7612 | 0.7870 | 0.7169 | +0.070 | -0.044 | cCRE 0.787 |
| 04   | 0.7494 | 0.7733 | 0.6833 | +0.090 | -0.066 | cCRE 0.773 |
| 05   | 0.6951 | 0.7133 | 0.6498 | +0.064 | -0.045 | cCRE 0.713 |
| 06   | 0.7853 | 0.8048 | 0.7365 | +0.068 | -0.049 | cCRE 0.805 |
| 07   | 0.6684 | 0.7452 | 0.6675 | +0.078 | -0.001 | cCRE 0.745 ← purely motif-rewarding |
| 08   | 0.7841 | 0.6380 | 0.6430 | -0.005 | -0.141 | rand 0.784 ← uniform-comp rewarding |
| 09   | 0.8115 | 0.8385 | 0.7392 | +0.099 | -0.072 | cCRE 0.838 |
| 10   | 0.7564 | 0.7635 | 0.7107 | +0.053 | -0.046 | cCRE 0.763 |
| 11   | 0.6833 | 0.7010 | 0.6408 | +0.060 | -0.043 | cCRE 0.701 |
| 12   | 0.6553 | 0.6757 | 0.6168 | +0.059 | -0.039 | cCRE 0.676 |
| 13   | 0.6584 | 0.7422 | 0.6880 | +0.054 | +0.030 | cCRE 0.742 ← only eval where comp helps |
| 14   | 0.7851 | 0.8046 | 0.7342 | +0.070 | -0.051 | cCRE 0.805 |

### Key reading
- **Motif content helps every eval except 08.** Average +0.063 over
  the 13 motif-rewarding evals.
- **cCRE composition hurts every eval except 13.** Narrow
  GC/CpG-biased composition is bad training data.
- **eval_07: purely motif-rewarding** (composition contributes 0).
- **eval_13: composition + motifs both contribute** (only such eval).
- **eval_08: rewards uniform-random composition** (both biology and
  bio-composition penalize).

### Implication for library design
The design target is **motifs in compositionally diverse backgrounds**.
Inject TF motifs into random or composition-uniform sequences rather
than sampling from genomic regions (which carry composition narrowness).

## After exp 008, "best library per eval" so far

| eval | best so far | best lib  | margin over rand |
|------|-------------|-----------|------------------|
| 01   | 0.7133      | 002 cCRE  | +0.018           |
| 02   | 0.8046      | 002 cCRE  | +0.020           |
| 03   | 0.7897      | 007 dELS  | +0.029           |
| 04   | 0.7733      | 002 cCRE  | +0.024           |
| 05   | 0.7133      | 002 cCRE  | +0.018           |
| 06   | 0.8048      | 002 cCRE  | +0.020           |
| 07   | 0.7605      | 007 dELS  | +0.092           |
| 08   | 0.7841      | 001 random| +0.000           |
| 09   | 0.8385      | 002 cCRE  | +0.027           |
| 10   | 0.7779      | 007 dELS  | +0.022           |
| 11   | 0.7010      | 002 cCRE  | +0.018           |
| 12   | 0.6782      | 007 dELS  | +0.023           |
| 13   | 0.7605      | 007 dELS  | +0.102           |
| 14   | 0.8046      | 002 cCRE  | +0.020           |

A library that scored each eval's best would average ~0.762.
dELS-only (007) alone gets 0.756; class-balanced cCRE (002) gets
0.748; natural-prop cCRE (008) gets 0.752. Headroom above dELS-only
is small (~0.006) and dominated by eval_08 (random's +0.112 over
dELS).

## After exp 023, library ranking by mean across 14 evals

| rank | library                                | mean_r |
|------|----------------------------------------|--------|
| 1    | **023 pELS+1%mut**                     | **0.761** ★ |
| 2    | 012 pELS-only                          | 0.758  |
| 3    | 007 dELS-only                          | 0.756  |
| 4    | 008 natural-proportion cCRE            | 0.752  |
| 5    | 021 pELS-longest                       | 0.751  |
| 5    | 019 CA-H3K4me3-only                    | 0.749  |
| 7    | 002 class-balanced cCRE                | 0.748  |
| 8    | 005 cCRE+random 50/50 mix              | 0.745  |
| 9    | 016 RC-augmented pELS                  | 0.741  |
| 9    | 017 pELS random offset                 | 0.741  |
| 11   | 015 mix10 pELS+dELS                    | 0.739  |
| 11   | 022 pELS-shortest                      | 0.739  |
| 13   | 001 uniform random ACGT                | 0.738  |
| 14   | 004 motif-injected random              | 0.732  |
| 15   | 013 pELS+dELS combo                    | 0.731  |
| 16   | 011 CA-only                            | 0.718  |
| 17   | 018 CA-CTCF-only                       | 0.710  |
| 18   | 003 dinuc-shuffled cCRE                | 0.696  |
| 19   | 009 genome-wide random                 | 0.690  |
| 20   | 010 repeat-masked genome-wide          | 0.686  |
| 21   | 014 TF-only                            | 0.683  |
| 22   | 006 PLS-only                           | 0.604  |
| 23   | 020 CA-TF-only                         | 0.536  |

## ★ NEW BEST: 1% mutation noise on pELS

First positive intervention found across 23 experiments. EVERY
eval improved (+0.001 to +0.007). Mean +0.003 over pELS-only.

Augmentation playbook updated: per-element MACRO transformations
hurt (RC, offset, length filters), per-position MICRO noise
helps. The model was overfitting to exact-sequence level, not
structural level. Sub-motif noise (point mutations) regularizes
without disrupting motif syntax.

## Augmentation null finding (exp 016 + 017)

Two completely different per-element augmentations cost the
exact same -0.017 mean penalty on top of pELS-only:

| exp | trick                        | unique | mean  | Δ      |
|-----|------------------------------|--------|-------|--------|
| 012 | central, no augmentation     | 50K    | 0.758 |  base  |
| 016 | central + RC, half pool      | 25K    | 0.741 | -0.017 |
| 017 | random offset, full pool     | 50K    | 0.741 | -0.017 |

The pELS configuration "central window, single strand, full
unique pool" sits at a local optimum. Per-element augmentation
playbook is empty. Future gains must come from POOL-level
operations (better class selection, quality filtering).

## Negative result: RC augmentation (exp 016) hurts pELS

25K unique pELS + 25K reverse-complements (50K total) gives
mean 0.741, uniformly -0.017 worse than 50K unique pELS-only
(0.758). Every eval drops; no eval benefits. Two implications:
- Model already handles strand symmetry implicitly
- Pool diversity (unique elements) > strand coverage

**Rule:** augmentations that reduce pool diversity are bad.
Useful augmentation must add genuinely new sequences (more
elements, more positions), not transformations of existing ones.

## Robust finding: mixing dilutes (4 independent confirmations)

| comparison                              | Δ from mix |
|-----------------------------------------|------------|
| 002 cCRE 8-class vs 007 dELS pure       | -0.008     |
| 005 cCRE+random vs 002 cCRE pure        | -0.003     |
| 013 pELS+dELS 50/50 vs 012 pELS pure    | -0.027     |
| 015 pELS+dELS 90/10 vs 012 pELS pure    | -0.019     |

Pure-class libraries beat mixtures at every ratio tested.
Counterintuitively, mixing TWO SIMILAR classes (pELS+dELS,
both enhancer-like) dilutes MORE than mixing dissimilar
(cCRE+random). Possible explanation: similar classes blur the
model's feature representations; very different classes can
route through different sub-features.

**Hard rule for this dataset: NEVER MIX. Single-class training
is optimal at any tested ratio.**

## Single-class library matrix (after exp 020 — COMPLETE)

| class       | pool size | mean_r | seed σ   | evidence type           |
|-------------|-----------|--------|----------|-------------------------|
| pELS        |   249,464 | 0.758  | low      | DNase + chromatin marks |
| dELS        | 1,469,205 | 0.756  | low      | DNase + chromatin marks |
| CA-H3K4me3  |    79,246 | 0.749  | **HIGH** | DNase + H3K4me3         |
| CA          |   245,985 | 0.718  | low      | DNase only              |
| CA-CTCF     |   126,034 | 0.710  | **HIGH** | DNase + CTCF (narrow)   |
| TF          |   105,286 | 0.683  | low      | TF-bound only           |
| PLS         |    47,532 | 0.604  | low      | TSS-proximal (location) |
| CA-TF       |    26,102 | 0.536  | low      | DNase + TF (small pool) |

**Key principle: annotation evidence type predicts library
quality more than biological category does.** PLS and CA-H3K4me3
both target active promoter biology; they differ by 0.145 mean
because PLS uses LOCATION evidence (TSS-proximal) while
CA-H3K4me3 uses FUNCTIONAL evidence (chromatin signal).

**Hierarchy:** pELS/dELS (enhancers) > CA-H3K4me3 (chromatin-
confirmed promoters) > CA (accessibility-only) > CA-CTCF
(insulator, narrow grammar) > TF (binding-only) > PLS
(location-only).

**Lessons:**
- Prefer chromatin-direct evidence over location/binding-only
- Enhancer classes win independent of pool size (pELS 249K
  beats dELS 1.47M)
- "CA + secondary mark" classes have higher seed variance —
  heterogeneous samples within class

## Best per-eval after exp 012

| eval | best   | best lib       | who beats current 1st-rank? |
|------|--------|----------------|------------------------------|
| 01   | 0.7203 | 012 pELS       | pELS (was 002 cCRE)          |
| 02   | 0.8129 | 012 pELS       | pELS                         |
| 03   | 0.7958 | 012 pELS       | pELS (was 007 dELS)          |
| 04   | 0.7733 | 002 cCRE       | -                            |
| 05   | 0.7203 | 012 pELS       | pELS                         |
| 06   | 0.8133 | 012 pELS       | pELS                         |
| 07   | 0.7605 | 007 dELS       | -                            |
| 08   | 0.7841 | 001 random     | -                            |
| 09   | 0.8385 | 002 cCRE       | -                            |
| 10   | 0.7779 | 007 dELS       | -                            |
| 11   | 0.7083 | 012 pELS       | pELS                         |
| 12   | 0.6853 | 012 pELS       | pELS (was 007 dELS)          |
| 13   | 0.7605 | 007 dELS       | -                            |
| 14   | 0.8129 | 012 pELS       | pELS                         |

pELS now holds 8/14 best-per-eval positions, dELS has 3 (07, 10,
13 — motif/diversity), cCRE has 2 (04, 09), random has 1 (08).
Composite "best per eval" library would average 0.766; pELS-only
gets 0.758 (only 0.008 below the oracle).

The cliff: every "biology-rich CURATED" library (002, 005, 007,
008) beats uniform random ACGT. Every "biological but
UN-curated/broken" library (003, 009, 006) loses to it. Curation
of regulatory annotation carries more value than "real-DNA-ness".

## After exp 009, eval_08 cliff structure

eval_08 punishes biological content monotonically with how much
curation is removed and how much repeat / narrow-content is added:

| library                    | eval_08 | Δ vs random |
|----------------------------|---------|-------------|
| 001 uniform random         | 0.7841  | +0.000      |
| 005 cCRE+random mix        | 0.6872  | -0.097      |
| 007 dELS-only              | 0.6720  | -0.112      |
| 008 natprop cCRE           | 0.6603  | -0.124      |
| 002 cCRE class-balanced    | 0.6380  | -0.146      |
| 003 dinuc-shuffled cCRE    | 0.6430  | -0.141      |
| 006 PLS-only               | 0.4774  | -0.307      |
| 009 genome-wide random     | 0.5351  | -0.249      |

eval_08 specifically rewards uniform-random composition; any
biological content hurts it; un-curated genomic content (009) hurts
it dramatically; collapsed-narrow-class (006) hurts it most.
eval_08 is now strongly suspected to be either purely synthetic
sequences or sequences with deliberately-randomized composition.

## Negative result: motif insertion (exp 004) doesn't transfer
Random JASPAR PWM instances inserted into random backgrounds give
mean_r 0.732 — worse than uniform random alone, and provides no
gain on the motif-rewarding evals 07 / 13. This means **motif
content alone is not sufficient**; context (genomic syntax, real
co-occurrence patterns, cell-type-relevant TF identity) carries
critical information.

## Per-cell ordering (consistent across all evals on random library)

SKNSH > K562 > HepG2 in essentially every eval. Likely an assay-level
property (dynamic range / noise) rather than library-driven.

## How to read a new result

- Subtract baseline floor to get *headroom captured*. That's the real
  metric of design quality.
- Look for *cluster-breaking* libraries: a design that improves one
  cluster but not another is more diagnostic than uniform improvement.
- If a library uniformly lifts every eval, it's probably teaching the
  model a generic feature. If a library sharply lifts the
  low-baseline evals (07, 11, 12, 13) but not the high-baseline ones,
  it's probably teaching real regulatory grammar.
