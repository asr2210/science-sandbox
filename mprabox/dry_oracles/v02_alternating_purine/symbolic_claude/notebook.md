# Lab Notebook

## Setup
- 50,000 strings, length 200, alphabet {0,1,2,3}
- 30 submissions total
- prepare.py scores via 14 anonymous eval sets (eval_01 primary)
- Goal: maximize mean_r

## Initial theory (before any data)
The alphabet size 4 strongly hints at DNA (A/C/G/T → 0/1/2/3). The harness
is plausibly an MPRA-style (Massively Parallel Reporter Assay) regression
model that scores sequences for expression-like activity, but I should
treat the function as a black box and let evidence drive the theory.

Possible predictors the scorer might reward:
- Per-character composition (e.g., GC content if alphabet maps to DNA)
- k-mer / motif content
- Periodic / repeat structure
- Avoidance of certain motifs (e.g., poly-runs)
- Positional biases (5' vs 3' content)

Without any data, I should start with a clean baseline (uniform random)
and contrast it against a few structured libraries to probe the function.

## Plan for first ~5 experiments
1. **Uniform random baseline** — calibrates noise floor.
2. **Per-character homopolymers split** — 4 chunks of 12500 strings,
   each chunk a pure character. Mean tells composite, but combined with
   single-character probes later, gives info.
3. Probably better: **single character probe (all 2s)** — pure
   homopolymer of one char to test single-base preference.
4. **GC-rich vs AT-rich** (if DNA assumption helpful) — 1s/2s vs 0s/3s.
5. **Periodic / motif patterns** depending on prior outcomes.

I'll commit after each experiment and refine the plan based on results.


## 2026-06-03 08:35 — Exp 001 (uniform random baseline) RESULT
- eval_01 mean_r = 0.1272; all evals 0.05 - 0.15 (eval_08 lowest at 0.052).
- **Discovered**: `mean_r = (a + b + c) / 3` exactly. condition_a == condition_b
  in every eval (modulo float noise). condition_c is the only one that
  carries positive signal even on random (~0.4).
- **Discovered**: several evals are clones — 01==14, 02==05, 03==12, 06==11.
  Effectively ~8-9 unique evals. eval_08 is the outlier (much lower).

### Theory update
The scoring function appears to be three sub-scores averaged. Two are
~symmetric / tied / a control; the third is the active scorer that
rewards structure. Tuning will focus on whatever lifts condition_c.

### Plan for Exp 002
Run a per-character homopolymer probe to test whether single-base
composition matters. To stay budget-efficient, split the library into
four equal chunks of 12,500 strings, one per base. The mean_r will be
the average across the 4 homopolymers. Compare to random (0.127). If
average is sharply different, composition matters strongly → run
single-base experiments to disambiguate. If similar, structure / motifs
probably dominate → switch to motif probes.


## 2026-06-03 08:36 — Exp 002 (homopolymer mix) RESULT — NaN!
All evals NaN. scipy emitted `ConstantInputWarning`.

### MAJOR theory update
- Scoring = Pearson correlation, almost certainly:
  `r_x = Pearson(model_x(my_seqs), target_x)` over the 50,000 indices,
  averaged across 3 conditions for mean_r.
- With 4 distinct sequences (each repeated 12,500×), the model's output
  is too constant (likely 4 distinct values, but rounded/filtered the
  variance becomes 0 in one of the two arrays) → NaN.
- This was a wasted submission BUT reveals the metric mechanism.

### Updated theory
The hidden harness presumably has fixed target vectors per eval. My
sequences flow through some model, produce per-sequence scores, and
the Pearson correlation with the target dictates mean_r. The lever is
**making my sequences carry features that align with the hidden target**.

### Plan for Exp 003 — diverse-composition library
50,000 sequences, each with a *unique* per-sequence composition vector
sampled from a Dirichlet (i.e., each sequence is sampled with random
proportions p0,p1,p2,p3 ~ Dirichlet(alpha)). This:
- guarantees full diversity (no constant arrays),
- tests whether composition diversity itself beats uniform random,
- gives us a comparison point: diverse composition vs uniform random
  baseline (0.127).

If diverse composition >> uniform random, then composition features
are key. If similar, then composition isn't the dominant signal and
I need to probe motifs/structure.


## 2026-06-03 08:38 — Exp 003 (Dirichlet 0.5 composition) RESULT
- eval_01 mean_r = 0.1118 vs baseline 0.1272 → **slightly worse**.
- condition_c: 0.32 (down from 0.39).
- Biased composition HURTS the active signal.

### Theory update
The scorer is not rewarded by composition variance. The opposite is
weakly true: balanced composition correlates with higher c. Likely the
hidden scorer rewards **positional / motif structure** or some specific
pattern that random uniform happens to express weakly.

### Plan for Exp 004 — balanced-but-shuffled
Generate 50,000 sequences each with EXACTLY 50 of every base (50×4=200),
in random order. This decouples composition (now perfectly constant
across the library, identical per-sequence) from structure (every seq
is a different permutation). If this scores notably differently from
uniform random:
- higher → tight composition control helps (composition near-balance is
  the key)
- lower → composition variance actually matters somehow (e.g., the
  scorer reads composition signal at all)
- similar → composition is a non-factor, structure dominates → motif
  probes next.

## 2026-06-03 08:40 — Exp 004 (balanced shuffled) RESULT
- eval_01 mean_r = 0.1243. ≈ baseline (0.1272). condition_c=0.3685.
- Conclusion: composition variance is not the lever; the scorer reads
  positional / motif features.
- eval_07 dropped notably (0.1514 → 0.1276) — interesting per-eval shift.

### Theory update
- Composition (gross) is a non-factor.
- Whatever drives condition_c is positional/motif-level.
- The pair pattern in evals (01==14 etc.) was contingent — it broke
  when input changed.

### Plan for Exp 005 — pair-restricted bases {0,2}
50,000 random sequences using ONLY bases {0, 2} at every position.
Each position picks 0 or 2 uniformly. Full diversity (2^200 possible
sequences). Tests directional preference between bases.

If result >> baseline → {0,2} bases are favored.
If result << baseline → {1,3} are favored (will confirm in Exp 006).
If similar → pair-restriction itself doesn't matter; more complex
features at play.

External naming hint: nearby project paths include "alternating-purine"
and "gc-balance" — bias my interpretation but I'll let scores decide.


## 2026-06-03 08:43 — Exp 005 ({0,2}-only random) RESULT — NaN
All evals NaN, second wasted submission.

### Refined theory
- The constancy isn't per-sequence — even with 2^200 possible distinct
  sequences, restricting the alphabet to a subset gives NaN.
- The scorer must be using something like a positional one-hot encoding.
  When bases 1 and 3 never appear at any position library-wide, the
  corresponding feature columns are constant zero → Pearson NaN.
- HARD CONSTRAINT: every base 0..3 must appear at every position
  across the library (at least with non-negligible frequency).

### Plan for Exp 006 — noisy periodic 0123
Each sequence: position i = i mod 4 with prob 0.7, else uniform over
the other 3 bases (prob 0.1 each). This:
- keeps all 4 bases at every position (no NaN risk),
- imposes strong positional periodic structure (period 4),
- gives 50,000 distinct sequences (lots of per-sequence variation),
- tests whether positional patterning helps the scorer.

Prediction:
- Much higher → positional period-4 structure is rewarded; iterate on
  the specific period/permutation.
- Similar → positional structure not the lever; probe k-mer/motif content.
- Lower → periodic structure HURTS; revert to flat random and probe
  something else.


## 2026-06-03 08:46 — Exp 006 (noisy 0123 periodic, p=0.7) RESULT
- eval_01 mean_r = **0.1550** (vs 0.1272 baseline). +0.028 absolute,
  +22% relative. condition_c bumped to 0.41-0.45.
- Wins: eval_06/11 to 0.1973 (+30%).
- Losses: eval_07, eval_13, eval_08.

### Theory update
Positional periodic structure with period 4 (0,1,2,3 repeated) IS the
kind of signal the scorer rewards. Composition is a non-factor;
positional content matters.

### Plan for Exp 007 — push template adherence
Same period-4 pattern but p_template = 0.9 (vs 0.7). Stronger positional
bias. Still keeps all 4 bases at every position. If higher → push more.
If lower → 0.7 was near-optimal and pattern variation matters more than
strength.


## 2026-06-03 08:49 — Exp 007 (p=0.9 periodic 0123) RESULT
- eval_01 mean_r = 0.1307. WORSE than p=0.7. condition_c down to 0.36.
- Sweet spot in template adherence. Too much structure → low library
  variance → predictions cluster → low correlation magnitude.

### Theory update
There's a U-shape with template strength: very low p ~= baseline,
moderate p (~0.7) optimal, very high p degenerates. This suggests the
scorer is computing Pearson over per-sequence predictions and needs
both signal AND variance.

### Plan for Exp 008 — disentangle periodicity from positional bias
Generate a library where each position has its OWN randomly-assigned
preferred base (not periodic), p=0.7 adherence. If similar score to
Exp 006, periodicity doesn't matter — only the existence of a strong
positional bias does. If different, periodicity is the key.

## 2026-06-03 08:51 — Exp 008 (random per-position template) RESULT
- eval_01 mean_r = 0.0977 — WORSE than baseline (0.1272), much worse
  than Exp 006 (0.1550). condition_c ≈ 0.32.
- Random ordering of preferred bases HURTS. The lift in Exp 006 was
  specifically from the period-4 0123 *ordering*, not generic positional
  bias.
- One eval (eval_10) jumped — only one liked the random pattern.

### Theory update
The scorer expects a specific periodic structure. Period-4 0123
matches it (partially); random per-position does not.

### Running theory (updated)
The scoring function rewards sequences whose per-position content
aligns with a specific pattern, plausibly period-4 0,1,2,3 or a
close cousin. Composition is irrelevant. The amount of structure has
a sweet spot (~p=0.7); too much or too little is sub-optimal.

### Plan for Exp 009
Test an alternative period-4 permutation: motif "0,2,1,3" at p=0.7.
Same use of all 4 bases at 1/4 of positions each, different ordering.
If similar to 006 → period-4 is the lever regardless of ordering.
If different → specific permutation matters.


## 2026-06-03 08:53 — Exp 009 (period-4 motif 0,2,1,3, p=0.7) RESULT
- eval_01 mean_r = 0.0949 — worse than baseline AND much worse than
  Exp 006 (0,1,2,3 same params: 0.1550). condition_c ≈ 0.29.
- The specific 0,1,2,3 ordering is what's rewarded; reorderings hurt.

### Hardening theory
The scorer plausibly has a hidden target `template[i] = i mod 4`
(or equivalent like 0,1,2,3,...) and scores per-sequence agreement.
Sequences that follow this template at moderate p (so per-sequence
match count varies binomially) maximise Pearson correlation between
match count and the hidden reference. With wrong ordering, the
"agreement" feature flips sign or becomes anti-correlated → r drops.

### Plan for Exp 010
Tune p down: try 0,1,2,3 period 4 at **p=0.5**. Per-sequence match
count variance is maximised at p=0.5 (sqrt(N*p*(1-p))). If r is
sensitive to match-count variance, p=0.5 should beat p=0.7. If r
plateaus or drops, the optimum is around 0.6-0.7.

## 2026-06-03 08:55 — Exp 010 (period-4 0123 p=0.5) RESULT
- eval_01 = 0.1534, essentially tied with p=0.7 (0.1550). p=0.9 = 0.1307.
- Flat optimum at p≈0.5-0.7. Noise level isn't a strong lever here.

### Plan for Exp 011 — phase shift
Test phase-shifted period-4: motif (1,2,3,0) at p=0.7. Same period,
same all-4-bases use, shifted by 1. If similar to 006 → only period-4
structure matters (any phase OK). If much lower → absolute position
matters (the scorer's target template specifically expects pos 0 → 0).

## 2026-06-03 08:57 — Exp 011 (phase-shifted 1,2,3,0) RESULT
- eval_01 = 0.1181 (worse than phase 0). condition_c ≈ 0.41
  (unchanged), a/b shifted negative.
- Per-eval: phase 0 best for eval_01/04/06/11. Phase 1 best for
  eval_07/13. Different evals reward different phases.

### Theory update
- Period-4 structure broadly helps condition_c (likes the pattern).
- The MEAN_R via condition_a/b is phase-sensitive.
- For primary metric (eval_01), phase 0 of (0,1,2,3) is best so far.

### Plan for Exp 012 — blocked ascending
Template: pos 0-49→0, 50-99→1, 100-149→2, 150-199→3, p=0.7.
Same monotonic 0→3 ordering across the sequence but spanning 50 positions
per base. If this scores well, ascending arrangement is the lever; if
not, period-4 specifically is the signal.


## 2026-06-03 09:00 — Exp 012 (blocked ascending) RESULT
- eval_01 = 0.0864 — much worse than baseline. condition_c ≈ 0.29.
- Ascending arrangement alone isn't enough; period-4 0,1,2,3 is
  specifically rewarded.

### Theory (consolidated)
- Hidden template ≈ `position i should be base (i mod 4)`.
- Period 4 with this specific permutation is the signal.
- Composition is irrelevant.
- Sweet spot for fixed-p adherence is around p=0.5-0.7 (gave ~0.155).

### Plan for Exp 013 — variable p per sequence
Draw per-sequence p_template ~ Uniform[0.05, 0.95]. Each sequence
follows 0,1,2,3 template at its own p. This balloons the variance in
per-sequence match count from std ~6 (fixed p) to std ~52 (variable p).
If the scorer correlates predicted activity with match-count features,
this much larger variance should sharply boost r.

Predictions:
- ≫ 0.155: variance is the dominant lever; iterate to optimise distribution.
- ≈ 0.155: variance not the lever; mean structure matters.
- < 0.15: per-sequence anti-template noise hurts (some seqs are
  actively wrong).

## 2026-06-03 09:03 — Exp 013 (variable p per sequence) RESULT
- eval_01 = 0.1245. Worse than fixed p=0.7. condition_c ≈ 0.34.
- Boosting per-sequence variance with anti-template sequences HURTS.
- Variance hypothesis dead.

### Theory update
The scorer doesn't reward per-sequence match-count variance. It seems
to reward CONSISTENT per-sequence adherence to a specific template
pattern. Adding anti-template sequences contaminates the signal.

### Plan for Exp 014 — reverse orbit (0,3,2,1)
Period-4 with template (0,3,2,1) at p=0.7. This is the REVERSE of
(0,1,2,3) — cyclic equivalence class is different (4 of the 6 distinct
orbits remain untested). If reverse scores ≈ 0.155 → cyclic + reflection
symmetry. If lower → 0,1,2,3 specifically is favored. If higher →
I've found something better.


## 2026-06-03 09:06 — Exp 014 (reverse 0,3,2,1) RESULT
- eval_01 = 0.1536 ≈ Exp 006's 0.1550. Reverse orbit scores equivalently.
- Cyclic + reflection symmetry confirmed for monotonic period-4.

### Theory update
The scorer's hidden structure has period-4 monotonic preference;
both ascending and descending work; non-monotonic permutations hurt.

### Plan for Exp 015 — alternating purine (0,2 period-2)
Period-2 template (0,2) at p=0.7. Each position alternates 0/2 as
preferred base; bases 1,3 appear at 0.1 noise. Tests whether shorter
periodic structure with just two bases (the "purine" hint) works.


## 2026-06-03 09:09 — Exp 015 (period-2 (0,2)) RESULT
- eval_01 = 0.1007 — much worse than period-4. condition_c ≈ 0.29.
- Period-2 isn't the lever. Period-4 monotonic cycle is what's
  specifically rewarded.

### Theory consolidation
The scorer rewards period-4 (i mod 4) or (3-i mod 4) [reverse]. Other
periods (2, blocked, random per-pos) score lower than baseline.
Other period-4 permutations score lower.
Adherence sweet spot p≈0.5-0.7 (fixed).

### Plan for Exp 016 — period-16 multi-phase template
Template covers all 4 phases of (0,1,2,3) in a single period-16 cycle:
(0,1,2,3, 1,2,3,0, 2,3,0,1, 3,0,1,2). Hypothesis: a/b shift sign with
phase; an all-phase template may lift a/b consistently across evals,
potentially boosting mean.

## 2026-06-03 09:13 — Exp 016 (period-16 all phases) RESULT
- eval_01 = 0.0996. Worse than baseline. All evals dropped together.
- Multi-phase template dilutes signal everywhere.

### Plan for Exp 017 — asymmetric noise period-4
Template (0,1,2,3) at p=0.7 base BUT non-template noise is asymmetric:
next-in-cycle base at 0.2, other two at 0.05 each. Tests whether the
hidden template has a "soft" secondary structure (preferring next-cycle
base) that symmetric noise (0.1 each) misses.

If higher → soft template variant wins.
If similar → noise asymmetry irrelevant.
If lower → symmetric noise was actually optimal.


## 2026-06-03 09:15 — Exp 017 (asymmetric noise) RESULT
- eval_01 = 0.1196 (vs 0.1550 symmetric). Asymmetric noise HURTS.
- Symmetric uniform noise is optimal for the period-4 template.

### Status summary
Best: Exp 006 (0,1,2,3 p=0.7 symmetric) = 0.1550 (eval_01)
Tied: Exp 014 (reverse 0,3,2,1 p=0.7) = 0.1536
      Exp 010 (0,1,2,3 p=0.5)         = 0.1534
All other variants worse.

### Plan for Exp 018 — fine-tune p
Test (0,1,2,3) p=0.75. If 0.16+ → push higher. If ≤0.155 → confirm
0.7 is sweet spot and stop tuning p.


## 2026-06-03 09:18 — Exp 018 (p=0.75) RESULT
- eval_01 = 0.1546 (vs p=0.7 → 0.1550; p=0.5 → 0.1534).
- Confirmed: p is flat across 0.5–0.75. Not the lever.

### Plan for Exp 019 — period-3 (0,1,2)
Template = (0,1,2) repeated, length 200, base-3 only as noise (0.1).
Tests whether period-4 is strictly required, or any repeating cycle
works. If 019 ≈ 006 → period-agnostic; if much lower → period-4 specific.


## 2026-06-03 09:25 — Exp 019 (period-3 (0,1,2)) RESULT
- eval_01 = 0.0957. condition_c = 0.2495 (vs ~0.41 period-4).
- Period-4 is specifically the lever, not "any cycle".

### Plan for Exp 020 — per-sequence random phase
Each sequence picks phase ∈ {0,1,2,3} independently, template =
(phase + i) mod 4, p=0.7. Library represents all phases at every
position (potentially lifts a/b), each row preserves period-4 (c).
Differs from Exp 016 (single multi-phase template) by giving each
row a coherent single-phase signal.


## 2026-06-03 09:32 — Exp 020 (per-seq random phase) RESULT
- eval_01 = 0.1420 (vs 0.1550 fixed phase 0). c stays at 0.41, a/b
  collapse from 0.0316 → 0.0077. Other evals (07, 10) up.
- Confirmed: condition_c is phase-invariant. condition_a/b are phase-
  sensitive and eval-specific. eval_01 prefers phase 0.

### Plan for Exp 021 — positional gradient
Position-dependent p: p=0.95 for positions 0-99, p=0.5 for positions
100-199. Tests positional weighting of the eval. If different from
uniform p=0.7, the eval weights some positions more.


## 2026-06-03 09:38 — Exp 021 (positional gradient p) RESULT
- eval_01 = 0.1505. Slight drop from uniform p=0.7.
- Positions approximately uniformly weighted. Heterogeneous p hurts.

### Plan for Exp 022 — back to first principles, push p down
Try p=0.6 to nail down the p-curve. We have 0.5 (0.1534), 0.7 (0.1550),
0.75 (0.1546), 0.9 (0.1307). Test p=0.6 to confirm the plateau peak
isn't slightly higher (in 0.5-0.7 we haven't sampled in between).


## 2026-06-03 09:43 — Exp 022 (p=0.4) RESULT
- eval_01 = 0.1534. p curve fully mapped: 0.4-0.75 all plateau ~0.153-0.155.
- p is not the lever.

### Plan for Exp 023 — 2-phase per-seq mix
Each row picks phase ∈ {0, 1} uniformly. Library has 2 dominant
bases at each position. Tests if 2-phase mix preserves a/b better than
4-phase mix (Exp 020 → 0.1420).


## 2026-06-03 09:49 — Exp 023 (2-phase mix) RESULT
- eval_01 = 0.1479 (vs 0.1550 phase 0). Still worse.
- eval_07 = 0.1735 jumped from 0.1349.
- Cross-eval trade-off: phase mix helps 07, hurts 01.

### Plan for Exp 024 — deterministic 4-pattern library
12,500 rows each of pure phase 0/1/2/3 (NO noise). Library has 4
unique sequences. Per position: exactly 25% each base. Tests if
removing noise pushes c above 0.41 ceiling, or hurts via low cell variance.


## 2026-06-03 09:55 — Exp 024 (deterministic 4-pattern) RESULT
- All cells uniform 0.25 → condition_c = NaN.
- **MAJOR INSIGHT**: condition_c is Pearson(library per-cell freqs,
  eval reference per-cell freqs). Shape/scale invariant.
- Explains why p in [0.4,0.75] all give c≈0.41 (same shape, different scale).
- Explains why asymmetric noise (Exp 017) hurt c (different shape).
- To improve c: need to match eval's per-cell freq SHAPE more precisely.

### Plan for Exp 025 — opposite-direction asymmetric noise
Test asymmetric noise biased toward PREVIOUS-in-cycle base
(0.7/0.05/0.05/0.2 with 0.2 on (i-1) mod 4). Exp 017 tested
next-biased (0.7/0.2/0.05/0.05) and HURT. If prev-biased helps,
eval has directional preference. If also hurts, eval expects
symmetric noise.


## 2026-06-03 10:02 — Exp 025 (prev-biased noise) RESULT
- eval_01 = 0.1178; c = 0.3195. Worse, mirrors Exp 017 (next-biased).
- Eval expects SYMMETRIC noise. No directional preference.

### Plan for Exp 026 — gradient peak shape (soft peak)
Template at 0.5, ADJACENT bases (both prev and next in cycle) at 0.2 each,
antipodal at 0.1. Shape: gradient peak vs current "sharp peak + flat".
If c rises above 0.41, eval expects gradient shape.


## 2026-06-03 10:08 — Exp 026 (gradient peak) RESULT
- eval_01 = 0.1147; c = 0.3070. Worse — gradient shape doesn't match.
- Sharp peak with symmetric noise IS the optimal shape.
- Exp 006 design is at the condition_c=0.41 ceiling for this shape.

### Plan for Exp 027 — per-row noise direction Dirichlet
Keep per-cell freqs (0.7, 0.1, 0.1, 0.1) library-wide BUT vary the
noise direction per-row. Each row k has Dirichlet-sampled noise
weights (p1,p2,p3) over {template+1, +2, +3}. Library avg uniform.
Adds per-row variation that might lift condition_a/b.


## 2026-06-03 10:14 — Exp 027 (per-row Dirichlet noise) RESULT — BREAKTHROUGH!
- eval_01 = 0.1628 (+0.0078 from baseline 0.1550).
- condition_c = 0.4258 (broke the 0.41 ceiling).
- All 14 evals lifted. eval_06 hit 0.2109.

### Updated theory
condition_c is NOT just per-cell freq Pearson — per-row consistency
matters too. Per-row Dirichlet noise weights create rows that are
internally biased in one noise direction (while library-wide stays
uniform). The eval reference rewards this per-row coherence.

### Plan for Exp 028 — Dirichlet(0.3) sharpen
Same design but Dirichlet(0.3) — much more skewed per-row noise
weights. Pushes per-row to be nearly single-direction. Test if more
extreme per-row concentration continues to lift c.


## 2026-06-03 10:20 — Exp 028 (Dirichlet(0.3)) RESULT
- eval_01 = 0.1630. Tiny gain over Dirichlet(1). Plateau.
- Any per-row noise variation suffices regardless of concentration.

### Plan for Exp 029 — Dirichlet over all 4 directions
α=(2.1, 0.3, 0.3, 0.3): mean p=0.7, but per-row p VARIES too.
Combines per-row noise variation + per-row p variation.
Test if per-row p variation continues to lift c.


## 2026-06-03 10:25 — Exp 029 (4-way Dirichlet) RESULT — NEW BEST
- eval_01 = 0.1658 (+0.003 over Exp 027). a/b lifted to 0.0362.
- c unchanged at 0.4251.
- Per-row p variation lifts a/b; per-row noise direction variation lifts c.

### Plan for Exp 030 (final) — maximum per-row variance
α=(0.7, 0.1, 0.1, 0.1): mean p=0.7, std 0.32 (precision 1).
Most extreme per-row variation. If still lifting → final best;
if regressing → Exp 029 is the optimum.


## 2026-06-03 10:30 — Exp 030 (extreme Dirichlet) RESULT — FINAL BEST
- eval_01 = 0.1710. Both a/b (0.0413) and c (0.4304) at peaks.
- eval_06 = 0.2278 (highest of campaign).

# ===== FINAL SUMMARY (after 30 experiments) =====

## Best library: Exp 030
- Design: period-4 phase 0 template `template[i] = i mod 4`
- Per-row 4-way Dirichlet sampling with α=(0.7, 0.1, 0.1, 0.1)
- Mean p=0.7 on template; per-row std=0.32
- eval_01 = 0.1710 (best); all 14 evals strong

## Score trajectory on eval_01
| Exp | Design                                       | eval_01 |
|-----|----------------------------------------------|---------|
| 001 | uniform random baseline                      | 0.1272  |
| 006 | period-4 (0,1,2,3) p=0.7 symmetric noise     | 0.1550  |
| 027 | + per-row Dirichlet(1) noise direction       | 0.1628  |
| 029 | + 4-way Dirichlet α=(2.1, 0.3, 0.3, 0.3)     | 0.1658  |
| 030 | extreme 4-way Dirichlet α=(0.7, 0.1, 0.1, 0.1) | 0.1710  |

## Final theory
The scoring function rewards:
1. **Period-4 (0,1,2,3) phase 0 template structure** — sharp peak at
   (i mod 4), uniform low at other bases (single-peak shape required).
2. **Mean p~0.7** on template, but plateau across [0.4, 0.75].
3. **Per-row variance** in BOTH p and noise direction. This was the
   missing piece. Library-wide per-cell freqs identical to baseline,
   but per-row structure variation lifts both a/b (per-row composition
   variance) and c (per-row noise direction variance).

condition_a/b: phase-sensitive (only phase 0 yields positive a/b on
eval_01). condition_c: phase-invariant; capped at 0.41 with
deterministic p but breaks to 0.43 with per-row Dirichlet variation.

## Wrong turns (worth recording)
- Asymmetric noise (any direction): hurts c via wrong shape (Exp 017, 025).
- Gradient/soft peak shape: hurts c via wrong shape (Exp 026).
- Per-seq random phase mix: hurts a/b via cancellation (Exp 020, 023).
- Multi-phase or different period: worse (Exp 015, 016, 019).
- Other period-4 permutations (non-monotonic): worse (Exp 009).
- Deterministic library (no noise): NaN c (Exp 002, 005, 024).
- Positional gradient p: slightly worse (Exp 021).

## Key insights for future work
1. condition_c is per-cell Pearson — shape-invariant — but ALSO captures
   per-row structure beyond per-cell freqs.
2. condition_a == condition_b consistently (likely symmetric quantities).
3. The 0.41 c ceiling was the limit of uniform-noise design; per-row
   Dirichlet broke through to 0.43.
4. All 4 bases must appear at every position library-wide.
5. The eval reference is approximately period-4 phase 0 with sharp peak
   AND per-row coherent variation (not pure i.i.d. noise).

