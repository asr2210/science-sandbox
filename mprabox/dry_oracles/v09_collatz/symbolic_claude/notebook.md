# Lab Notebook — String Optimization

## Task summary
- 50,000 strings, length 200, alphabet {0,1,2,3}
- Black-box scorer; eval_01 is primary metric across 14 eval sets
- Each eval also returns condition_a, condition_b, condition_c (unknown meaning)
- 30 experiments budget

## Initial theory (pre-experiment)
The alphabet {0,1,2,3} of length 200 strongly resembles DNA sequences
(A/C/G/T) at a typical regulatory-element scale (200 bp), common for
MPRA (massively parallel reporter assay) libraries. 14 eval sets each
returning 3 conditions (a/b/c) is consistent with MPRA-style scoring
in 14 cell types/contexts with 3 sub-measurements (e.g., replicates
or fractions). Mean_r is likely Pearson correlation or fraction of
"functional" elements.

Working hypothesis H0: scorer rewards strings that look like real
regulatory elements: balanced GC, presence of TF-binding-like motifs,
moderate complexity (not all-same, not maximally random).

First-pass questions to resolve cheaply:
1. What does a uniform-random library score? (baseline)
2. Does global character frequency matter?
3. Does diversity across library matter, or per-string properties?

## 2026-06-02 18:15 — Plan Experiment 001: uniform random baseline
Goal: establish baseline. Generate 50k iid uniform random strings of
length 200 from {0,1,2,3} with fixed seed. Predict mean_r near "neutral"
— probably low but nonzero. Comparing to later, biased libraries
will tell us what the scorer rewards.

## 2026-06-02 18:25 — Experiment 001 result
Uniform random baseline. eval_01 mean_r=0.2399 (a=0.14, b=-0.05, c=0.63).
Confirmed mean_r = (a+b+c)/3 arithmetically. Several evals are exact
duplicates of each other (01==14, 02==05, 03==12, 04==09, 06==11),
so effective unique evals ≈ 9. eval_08 is an outlier (much lower
across all conditions). Theory holds — random is "neutral".

## 2026-06-02 18:30 — Experiment 002 result
Mixed library of 4 sub-populations each with 70% single-char bias.
eval_01 mean_r=0.1402 — DOWN from 0.24 by ~0.10. All three conditions
fell. STRONG signal that compositional balance matters: any sub-
population with extreme single-char bias damages scores.

Updated theory: scorer rewards balanced character composition near
25%/25%/25%/25%. Random uniform is close to optimal on this axis.
Improvements need to come from STRUCTURE / motifs / diversity at a
level beyond marginal character frequency, while preserving balance.

## 2026-06-02 18:32 — Plan Experiment 003: low diversity library
Goal: does between-sequence diversity matter, or only per-sequence
properties? Generate one random "template" of length 200 with
balanced composition, then 50k copies each with 5% iid mutations.
Composition stays uniform; within-library diversity collapses. If
condition c drops significantly, diversity matters. If it stays
similar to random, c is per-sequence.

## 2026-06-02 18:38 — Experiment 003 result
Low diversity (one template + 5% mutations per copy, balanced composition).
eval_01 mean_r=0.1602. Conditions a and b FLIPPED sign:
- a: 0.14 → -0.13 (a prefers diversity)
- b: -0.05 → +0.14 (b prefers similarity/structure)
- c: 0.63 → 0.47 (c prefers diversity)
This is a real finding: the three conditions are NOT aligned. Net
score worsens because the gain on b doesn't compensate the loss on
a + c.

Updated theory: scorer = arithmetic mean of three properties of the
library:
  a: rewards diversity (or per-sequence variability)
  b: rewards structure/cross-sequence regularity
  c: rewards diversity AND uniform composition (strongest term, but
     also drops with bias and with low diversity)

To beat uniform random we likely need a library with: balanced
composition, high between-sequence diversity, AND structural
features that help b without collapsing diversity.

## 2026-06-02 18:45 — Plan Experiment 004: uniform + inserted motif
Goal: add structure that condition b might like, without collapsing
diversity. Generate uniform random length-200 sequences; in each,
overwrite a 12-char window at a random position with a fixed balanced
periodic motif "012301230123". Composition stays uniform (motif is
balanced). Diversity stays high (window is small). Predict modest
boost on b, neutral on a/c, net up.

## 2026-06-02 18:55 — Experiment 004-005 results
Exp 004 (random-position 12bp motif): 0.2235 (down 0.016). Random
placement gives no cross-sequence alignment — confirmed b doesn't
react.
Exp 005 (fixed 48-char "0123" prefix): 0.2661 (UP 0.026!). Big
improvement. Fixed-position scaffold creates cross-sequence
alignment. b flipped from -0.05 to +0.01, c held at 0.65.

## 2026-06-02 19:00 — Experiment 006 result (UNEXPECTED)
Doubled scaffold to 100 chars period-4 prefix.
eval_01 collapsed to -0.149.
- a: 0.097 (slightly down)
- b: +0.10 (continued rising — b loves more alignment)
- c: -0.65 (SIGN FLIPPED from +0.65)
- Composition still balanced.

Lesson: c has a nonlinear cliff. Excessive scaffold (or excessive
periodicity?) flips c sign. The b axis kept improving as expected
but c collapse overwhelmed it.

Updated theory:
- a: rewards within-library diversity (suffers with template/long
  scaffold)
- b: rewards cross-sequence alignment at fixed positions (rises
  monotonically with scaffold length, up to tested limit)
- c: highly sensitive to MORE STRUCTURE than some threshold —
  particularly to periodic content. Could be measuring something
  like "fraction of positions whose distribution looks random across
  the library" or "library entropy at the position level". Long
  periodic scaffold tanks it.

Next: isolate length vs periodicity. Exp 007 = 48-char RANDOM fixed
scaffold (same length as 005, no periodicity). If c stays positive,
length 48 itself is the safe regime. If c flips even at 48 with
random content, periodicity in 005 was carrying us; if c is higher
than 0.65, random > periodic.

## 2026-06-02 19:30 — Experiments 007-014 results & theory refinement

| Exp | Design | eval_01 | a | b | c |
|---|---|---|---|---|---|
| 005 | scaffold 48 prefix | 0.266 | 0.137 | +0.010 | 0.651 |
| 007 | scaffold 48 random | 0.265 | 0.141 | +0.023 | 0.632 |
| 008 | scaffold 72 prefix | 0.274 | 0.133 | +0.052 | 0.638 |
| 010 | scaffold 80 prefix | 0.113 | 0.132 | +0.001 | 0.205 |
| 006 | scaffold 100 prefix | -0.149 | 0.097 | +0.105 | -0.648 |
| 009 | scaffold 48+48 ends | -0.142 | 0.108 | +0.100 | -0.634 |
| 011 | Markov no-self-repeat | 0.176 | 0.039 | +0.064 | 0.424 |
| 012 | full palindrome | 0.292 | 0.142 | +0.111 | 0.622 |
| 013 | direct repeat | 0.235 | 0.138 | -0.043 | 0.611 |
| 014 | palindrome + 24 scaffold prefix | **0.307** | 0.141 | +0.121 | 0.657 |

Key theory updates:
- b rewards REVERSE-COMPLEMENT palindrome (012 boost) but NOT
  direct repeats (013). So scoring is RC-symmetric, suggesting the
  underlying scorer treats the alphabet as DNA with complement
  0<->3, 1<->2 (matches A<->T, C<->G if 0=A,1=C,2=G,3=T or any
  isomorphic pairing).
- b also gets a boost from cross-sequence positional alignment
  (scaffold), additive with palindrome.
- c cliff at ~80 contiguous fixed positions OR ~96 split fixed
  positions (entirely deterministic, library-level entropy = 0 at
  those positions). Palindrome positions have full per-position
  entropy (just RC-paired), so they don't count against c cliff.
  In exp 014: 48 truly fixed (scaffold + its mirror) + 152
  palindrome-paired. c=0.657, no cliff issue.

New theory:
- a: rewards per-sequence "useful variance" — i.e., each sequence
  carries informative content. Hurt only by extreme bias (002) or
  unnatural Markov structure (011).
- b: rewards REVERSE-COMPLEMENT internal palindromic structure
  AND cross-sequence scaffold alignment. Both are forms of
  "alignment".
- c: rewards balanced composition + adequate library-level
  positional diversity. Cliff at ~80 fixed positions.

## 2026-06-02 19:35 — Plan Experiment 015
Push scaffold within palindrome to 36 chars (72 total fixed positions).
Approach the cliff carefully. If c stays > 0.65, can push further.

## 2026-06-02 20:30 — Catchup: Experiments 015-022 results

| Exp | Design | eval_01 |
|---|---|---|
| 014 | palindrome + 24 scaffold prefix (BEST) | **0.3066** |
| 015 | palindrome + 36 scaffold prefix | 0.3018 |
| 016 | four palindromes of length 50 | 0.3042 |
| 017 | palindrome + 12 scaffold prefix | 0.3051 |
| 018 | scaled palindrome A+RC(A)+A+RC(A) | 0.2922 |
| 019 | palindrome alt-complement 0<->1, 2<->3 | NaN |
| 020 | palindrome + dense 4-mer tail | NaN |
| 021 | palindrome + 48 NOISY scaffold (20% mut) | 0.3036 |
| 022 | library-level RC pairs (no per-seq palin) | 0.2504 |

Theory updates:
- Complement is specifically 0<->3, 1<->2 (exp 019 NaN under alt). NOT
  a generic palindrome detector.
- b is PER-SEQUENCE palindrome, NOT library-level RC pairing (exp 022).
  Confirms b reads each sequence's internal RC structure.
- Over-constraining sequences with tiled palindromic motifs (exp 020)
  collapses scoring to NaN — likely because some condition's input
  becomes constant.
- Scaffold length sweet spot in palindrome: 24 > 12 > 36 > 48. The
  marginal gain of more scaffold is small and turns negative past ~24.
- Splitting palindrome into 4 (exp 016) hurts slightly vs one big.
- Scaled palindrome (each half palindromic too) over-constrains —
  reduces per-sequence informative variance → hurts a, net down.
- Noisy scaffold (exp 021) hurts vs fixed (014) — periodic alignment
  needs to be clean.

Best remains exp 014: palindrome + 24 period-4 scaffold prefix at 0.3066.

## 2026-06-02 20:35 — Remaining experiment plan (8 left)
Hypotheses to test, prioritized:

H1 — Multi-scale palindrome: nested palindromes at different lengths
might give b multiple alignment signals (exp 018 had 2 scales but
over-constrained; try less restrictive multi-scale).
H2 — Scaffold content axis: does the SPECIFIC scaffold pattern matter
beyond just "fixed positions"? E.g., random vs periodic.
H3 — Sweet spot scan: scaffold 6, 18, 30 — fill in 014's local
neighborhood for fine tuning.
H4 — Distributed scaffold: multiple short scaffolds at different
positions in palindrome — does b reward more anchor points?
H5 — Palindrome with structured (motif-rich) free half — embed
multiple specific palindromic 6/8-mers without over-constraining.

Plan (subject to revision based on results):
- Exp 023: scaffold 18 in palindrome (fine-tune length)
- Exp 024: distributed scaffold 4x6 at positions 0,24,48,72 in palindrome
- Exp 025: palindrome with RC-palindromic 24-char random motif as scaffold
- Exp 026-030: iterate on best

## 2026-06-02 21:30 — Experiments 023-030: motif scaffold breakthrough

| Exp | Design | eval_01 | a | b | c |
|---|---|---|---|---|---|
| 014 | palin + period-4 [0123] x6 (24 chars) | 0.3066 | 0.141 | 0.121 | 0.657 |
| 023 | palin + period-4 18 char | 0.3030 | 0.143 | 0.118 | 0.649 |
| 024 | palin + 4x6 distributed period-4 | 0.3053 | 0.142 | 0.125 | 0.649 |
| 025 | palin + 6-mer palin tiled in tail | 0.2546 | 0.128 | 0.058 | 0.578 |
| 026 | palin + 4x CACGTG (E-box, GC palin) | 0.3121 | 0.141 | 0.143 | 0.652 |
| 027 | palin + 6x CACGTG (36 char) | 0.3047 | 0.122 | 0.142 | 0.650 |
| 028 | palin + 4x AATATT (AT palin) | 0.3155 | 0.135 | 0.172 | 0.640 |
| 029 | palin + 4x AAATTT | 0.3147 | 0.136 | 0.172 | 0.636 |
| 030 | palin + 3x AAAATTTT (BEST) | **0.3177** | 0.138 | 0.174 | 0.641 |

KEY DISCOVERY: scaffold MOTIF CONTENT matters substantially for b.
The boost ordering:
  period-4 [0,1,2,3]: b=0.12 (least)
  E-box CACGTG (GC-rich palin): b=0.14
  AT-rich palindromes (AATATT, AAATTT, AAAATTTT): b=0.17 (most)

The signal is consistent across all eval sets — it's not just one
eval being noisy.

Final theory:
- The scorer's b component looks like a "transcription factor motif
  presence" detector that prefers AT-rich palindromic motifs (often
  associated with HOX/HMG-family TF binding sites). RC-palindrome
  is necessary but not sufficient — the alphabet content within the
  motif drives a 50% additional boost over generic.
- a, c remain governed by diversity & balance respectively;
  AT-rich scaffold has a tiny cost on each (~0.005), but the b
  gain (~0.05) more than compensates.
- Optimal recipe: 200-bp RC palindrome (the structural backbone)
  + a fixed ~24-char AT-rich palindromic scaffold prefix
  (the cross-sequence "TF binding site" anchor).

## Final ranking
1. **030 (palindrome + 3x AAAATTTT)**: eval_01 = 0.3177 ★
2. 028 (palindrome + 4x AATATT): eval_01 = 0.3155
3. 029 (palindrome + 4x AAATTT): eval_01 = 0.3147
4. 026 (palindrome + 4x CACGTG): eval_01 = 0.3121
5. 014 (palindrome + period-4 24): eval_01 = 0.3066

Improvement vs random baseline (0.2399): +0.078 (+32% relative).

## Lessons / skills earned
- Decompose mean_r into a/b/c early — diagnoses what lever each
  experiment moves and avoids being confused by net-cancel effects.
- Eval sets contain duplicates; map them once and you save sweep time.
- Cliffs are real: some axes have nonlinear thresholds (c collapses
  at ~80 fixed positions). Sweep gently near regime changes.
- When you find a new structural lever (palindrome, scaffold), test
  variants of the lever (length, position, content) — content of
  scaffold mattered MORE than length once the structure was right.
- Over-constraining sequences (exp 020, 025) kills per-sequence
  variance signals AND can produce NaN cliff failures. Keep entropy.

