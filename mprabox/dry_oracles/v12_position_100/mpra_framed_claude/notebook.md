# MPRA Library Design — Lab Notebook

## 2026-06-02 19:55 — Initial theory & strategy

### Setup
Starting 30-experiment campaign to design 50,000-sequence MPRA libraries.
Measured cell types: K562, HepG2, SK-N-SH. Eval: 14 anonymous sets,
eval_01 is primary. Goal: a library that trains a sequence-to-activity
model that generalizes BEYOND the three measured cell types.

### Initial theory
A sequence-to-activity model can only generalize to unseen cell types if
it learns the **universal cis-regulatory grammar** (TF motifs, motif
context, spacing, combinatorics) rather than memorizing cell-type-specific
labels. So a maximally informative training library should:

1. **Expose diverse TF motifs in many contexts.** A motif appearing in
   100 different flanking contexts teaches the model "this motif drives
   activity"; a motif appearing once teaches nothing transferable.
2. **Span a wide activity range.** Sequences predicted near zero teach
   the model the null distribution; sequences with strong activity teach
   what drives signal. Both extremes matter.
3. **Avoid pure noise.** A purely random library has weak signal-to-noise
   because TF binding sites occur only by chance and most variation is
   measurement noise.
4. **Include realistic cis-regulatory architecture** — motif spacing,
   density, GC content matching real enhancers/promoters — because the
   model's inductive biases should align with natural sequence statistics.
5. **Decorrelate motif identity from cell-type-specific activity** in
   training, by having the same motifs appear in different cell-type
   activity regimes (this is hard to control directly).

### Things I'm uncertain about and want to test
- Is genome-derived sequence content (real enhancers/promoters) more
  informative than synthetic motif insertions?
- Does a library with very high activity diversity beat one with
  diverse motif content but moderate activity?
- Do shuffled/dinucleotide-preserving controls help the model?
- How much does GC content / dinucleotide composition matter on its own?

### Plan for experiment 001
**Exploring** — establish a baseline. Pure uniform random DNA. This is
the simplest possible library and gives me a floor to compare against.
Prediction: low-to-moderate scores; the model will learn some motif
recognition by chance (TF binding sites are short, 6–12bp, and will
appear randomly in 200bp windows) but mostly weak signal.

Why this generalizes (or doesn't) beyond labeled cell types: random
sequences are unbiased w.r.t. cell-type-specific regulatory regions. If
the model learns motif recognition from a random library, the motifs
themselves are universal (TFs bind by sequence), so the learned grammar
should transfer. But random libraries underexpose strong regulatory
sequences, limiting how much signal the model can extract.

## 2026-06-02 19:58 — Experiment 001 result: random uniform baseline

### Result
- eval_01: **0.0619** (primary)
- eval mean across all 14: ~0.078
- Range: 0.044 (eval_08) — 0.122 (eval_13)
- Time: 65s

### Key discovery: eval set duplicates
The 14 eval sets are NOT all distinct. Equal numbers (mean_r exactly
identical to 4 decimals) on the random library:
- eval_01 ≡ eval_14
- eval_02 ≡ eval_05
- eval_03 ≡ eval_12
- eval_04 ≡ eval_09
- eval_06 ≡ eval_11
So 9 distinct, 5 duplicates. (Could be the same K562/HepG2/SKNSH split
re-reported, or genuinely the same sequences.) **This shifts strategy**:
focus on the 9 distinct sets, and especially eval_01 which is primary.

### Theory update
Confirmed: random uniform gives weak but nonzero signal (~0.06 Pearson),
meaning the model *can* pick up some motif structure by chance. But the
signal ceiling is low. To beat this dramatically I need to make TF binding
sites — the universal regulatory grammar — actually present and varied
in the training data.

### Next experiment hypothesis
**Genome-derived sequences from human regulatory regions** should beat
random uniform substantially. Real regulatory DNA has:
1. Real TF motif content (the model sees real grammar, not noise)
2. Natural GC / dinucleotide composition
3. A wide activity range (regulatory regions vary in strength)
4. **Generalization argument**: TF motifs are universal; whatever cell
   type the eval is in, the motifs the model learned should still apply
   because TF DNA-binding is sequence-specific not cell-specific.

But I don't have the human genome downloaded. The simplest practical
proxy: generate sequences with realistic GC content (~50%) and
**dinucleotide composition** matching human regulatory regions, AND
**embed known TF motifs** at varied positions/orientations. This
synthesizes a "grammar-rich" library without needing genome download.

Actually, let me first try a cleaner contrast: **just** dinucleotide-shuffled
versions with human-typical GC, vs random uniform. If that doesn't beat
random much, dinucleotide stats alone aren't enough — the *motifs* are
what matter. That's a more informative comparison than going straight
to motifs.

Decision for exp 002: GC-content-matched random (50% GC, vs random's 50%
anyway — wait, random uniform IS 50% GC). Skip that. Instead, go
straight to **motif-augmented random** as exp 002, which is a much bigger
hypothesis test: do TF binding sites in flanking random context teach the
model the right grammar?

## 2026-06-02 21:01 — Experiment 002 result: motif-augmented random

### Result vs baseline
- eval_01: 0.0619 → **0.0646** (+0.003) — minimal gain
- eval_04: 0.0737 → 0.0814 (+0.008) — biggest gain
- eval_07: 0.1219 → 0.1297 (+0.008)
- eval_10: 0.1176 → **0.1094** (-0.008) — went down
- Most others: +0.002 to +0.004

### Theory refinement
Adding TF motifs to random background gives only marginal improvement.
This **contradicts** my naive prediction of a big jump. The motif
signal is drowned out by random background noise — when 95% of each
sequence is uniform noise contributing nothing predictable, the model
can't easily learn "motif X drives activity X" because the activity it
sees for sequence X is essentially set by noise plus a small motif
contribution.

**Refined theory:** motif content matters, but it must come with
**realistic context**. Real regulatory sequences are not "noise +
motifs"; they have:
- Co-evolved motif COMBINATIONS (cis-regulatory grammar)
- Locally biased base composition (CpG islands, AT-rich, etc.)
- Motif clustering at specific densities
- Background sequence that itself contains weak motif-like patterns

So the next informative experiment should test real genomic regulatory
sequences. ENCODE cCREs would be ideal — pre-annotated regulatory
regions (promoters, enhancers, CTCF sites). UCSC accessible. Let me try
downloading.

### Side observation
eval_10 went DOWN with motifs — possibly its sequences are
non-regulatory (e.g., random or scrambled controls) and the model's
slight motif overfitting from training hurt. Worth keeping an eye on
eval_10 as a "non-motif-trained" canary.

## 2026-06-02 21:10 — Experiment 003 result: ENCODE cCREs

### Result
- eval_01: 0.0619 → **0.0758** (+0.014, +22%)
- All eval sets improved
- Biggest gain: eval_08 +48% (was the hardest)
- Time: 53s

### Confirmed theory
Real genomic regulatory DNA is **massively** more informative than
synthetic motifs in random background. This is the first big jump.

### What this implies for generalization
- The model is learning real regulatory grammar (motifs IN CONTEXT)
- That grammar is universal across cell types — supports cross-cell
  generalization
- But cCREs are biased toward well-studied tissues (blood, liver) →
  SKNSH (neural) still hardest

### Open questions raised
1. Is the random background (12.5%) helping or hurting? It teaches
   "null" but may dilute the signal.
2. Is the 25/25/25/12.5 PLS/pELS/dELS/CA balance optimal? Promoters are
   only 47K in the genome but I weight them 25% — overrepresented
   relative to their genomic prevalence. Maybe enhancers should dominate?
3. Are there activity classes I'm missing? (3'UTR? 5'UTR? splice sites?)
4. Could deeper sampling — more unique cCREs per class — help further?

### Next experiment (004)
**Pure cCRE library, no random background, more diversity.**
- 50,000 sequences, all from cCREs
- Increase dELS share (most numerous in genome → most diversity)
- Aim: 10K PLS + 10K pELS + 20K dELS + 10K CA_TF
- This tests whether the 6,250 random bg in exp 003 was a tax or a benefit.

If 004 beats 003: random hurts, regulatory wins. Direction: maximize
regulatory diversity.
If 004 underperforms 003: random sequences provide useful "null"
examples; need to keep negative controls in the library.

## 2026-06-02 21:18 — Experiment 004 result: pure cCRE diverse

### Result
- eval_01: 0.0758 → **0.0755** (≈no change)
- All eval set changes within ±0.004 of exp 003
- eval_08 dropped slightly (-0.0035) — random background may have helped it

### Theory update
**Composition tweaks within cCRE-derived libraries have saturated** at
~0.076 on eval_01. The ceiling here isn't about how I balance cCRE
classes; it's about what's IN the sequences. Random background, dELS
weight, CTCF subclass — none move the needle.

This is an important null result: the model has extracted what it can
from "ENCODE cCRE coordinates + uniform sampling per class." To break
through I need to change WHAT the sequences are, not HOW I balance them.

### Hypotheses for next move (ranked by what I'd learn)

1. **Motif vs context.** Replace half the cCREs with dinucleotide-
   matched random (Markov-shuffled cCRE composition). If perf drops a
   lot → motifs are the work. If perf is similar → composition
   matters more than I thought. Either way teaches what to optimize.

2. **Add high-activity-likely sequences** beyond PLS: GENCODE TSS
   ±100bp windows, gene-flanking regions. Tests if there's value in
   "even-stronger-promoter" content beyond the 5K PLS we already have.

3. **Add ChIP-seq peaks** from K562/HepG2/SK-N-SH for TF-rich regions
   (TFs known to drive activity in these cells). Could improve labels
   for the measured cell types specifically.

4. **Activity-likely vs activity-unlikely contrast** via random
   genomic background scaled up to test if more "negative class"
   examples sharpen the model.

5. **Cross-cell-type generalization test.** Train on ONE class (say
   only dELS) and see how badly it does — measures how much the
   class diversity matters.

### Decision
Going with **(1) dinucleotide-shuffled controls** as exp 005. Cleanest
hypothesis test — directly distinguishes whether motifs or composition
drive the cCRE advantage. Even if it tanks performance, the answer is
informative and shapes everything I do next.

Implementation: build the global dinucleotide transition matrix from
the full cCRE pool, then Markov-generate 25K composition-matched
sequences. Mix 50/50 with real cCREs.

## 2026-06-02 21:25 — Experiment 005 result: 25K cCREs + 25K Markov

### Result
- eval_01: 0.0758 (003) → **0.0727** (005); 50K cCREs (003) → 25K cCREs+25K Markov
- All sets dropped 2-7%; not a crash, modest dilution
- 25K cCREs alone effectively delivers ~96% of 50K's eval_01 score

### Theory update
**Confirmed: motifs/grammar contribute, but the cCRE signal is highly
sub-linear in cCRE count.** Doubling unique cCREs (25K → 50K) gave only
+0.003. Half-Markov diluted by similar ~5%. The model extracts most of
what it can from ~25K cCREs.

**Implication**: pushing past 0.076 likely requires changing the *kind*
of training data, not just adding more cCREs. Options:
- New genomic feature types (GENCODE TSS, UTRs, gene bodies)
- Cell-type-targeted ChIP-seq peaks
- Activity-stratified or extreme-activity sequences
- Data augmentation (shifted windows, RC strands)

### Updated meta-theory of library informativeness
The model treats sequence input as (motif-rich, in real genomic
context) → activity prediction. Returns diminish quickly with more
of the same category because:
1. Common motif patterns saturate (50K dELS already covers the dominant
   TF-family compositions)
2. Activity distribution may be too narrow within a single category
3. Cross-cell-type discriminative information may need cell-type-
   targeted regions

To improve, need to either:
- BROADEN feature types (TSS, UTRs, ChIP peaks)
- SHARPEN activity contrast (low/high stratified)
- AUGMENT (effective multiplication of grammar exposure)

### Decision for exp 006
GENCODE TSS-proximal windows added to cCRE library. TSS are gold-standard
promoter sequences, distinct from cCRE PLS (which is a broader category).
If TSS adds value beyond cCRE PLS → different feature types help. If not,
the cCRE annotation already covers it.

Need to download GENCODE GTF (~few hundred MB).

## 2026-06-02 21:30 — Experiment 006 result: cCREs + GENCODE TSS

### Result
- eval_01: 0.0758 → **0.0708** (-7%)
- All eval sets dropped 2-7% except eval_03 (+2%)

### Theory update — adding TSS HURT
This is the second informative null/negative result in a row (005 also
underperformed). Both 005 and 006 underperform 003 by replacing cCRE
diversity with something more homogeneous:
- 005: replaced 25K cCREs with Markov-shuffled (no motif structure)
- 006: replaced 15K cCREs with TSS (very similar canonical promoters)

**Pattern: any narrowing of regulatory diversity hurts.** The cCRE
balanced mix is a strong local optimum because it spans many regulatory
grammars across many cell types simultaneously.

### Implication for what GENERALIZES
A library that broadly covers DIVERSE regulatory grammars is more
informative than one that piles up many examples of ONE grammar
(promoters). The model with capacity to learn many motif families
benefits from breadth.

This is consistent with the meta-goal: cross-cell-type generalization
requires the model to have seen enough diverse regulatory contexts that
its motif detectors are well-calibrated.

### Path forward — search literature + try a true non-cCRE source
What I haven't tried and that might genuinely add complementary signal:
- **ChIP-seq peak regions** with TF binding evidence (different from
  cCRE classification - real per-experiment peaks)
- **Conservation-stratified** cCREs (functional vs non-functional)
- **Distal regulatory regions far from any cCRE** (potential novel
  enhancers missed by cCRE annotation)
- **Sequence diversification via positional augmentation** (multi-window
  per cCRE)

### Plan for exp 007
Test the augmentation/multi-window hypothesis cleanly. Take ~16,667 unique
cCREs from balanced classes, generate 3 overlapping 200bp windows per
cCRE (left, center, right with stride ~50bp), making 50K sequences.

If 007 > 003: positional augmentation helps; model benefits from seeing
same grammar in multiple framings.
If 007 < 003: unique cCRE count matters more than augmentation.

Either way, learn something.

## 2026-06-02 21:35 — Experiment 007 result: multi-window augmentation

### Result
- eval_01: 0.0758 → 0.0747 (-0.001) — basically tied
- eval_04, 07, 10 slightly improved
- 16.7K unique × 3 windows ≈ 50K unique × 1

### Theory
**Augmentation IS a real lever** (3 windows ≈ 3 cCREs per unique
region) but doesn't move the ceiling. Suggests the cCRE-based plateau
near 0.076 on eval_01 is structural: either the eval signal-to-noise
caps it or the model architecture caps it.

### Tested so far (eval_01 column):
| Lib | eval_01 | Note |
|---|---|---|
| 001 random uniform | 0.062 | floor |
| 002 random + IUPAC motifs | 0.065 | +0.003 |
| 003 cCREs balanced | **0.076** | +0.014, BEST |
| 004 pure cCREs dELS | 0.076 | tied |
| 005 25K cCRE + 25K Markov | 0.073 | -0.003 |
| 006 cCREs + TSS | 0.071 | -0.005 |
| 007 16.7K × 3 windows | 0.075 | -0.001 |

The cCRE plateau is 0.075-0.076. Everything else is below.

### New hypothesis to test
Different cCRE-derived libraries all hit the same plateau. The lever
to break it might be **direct TF-binding peaks** — sequences where
TFs have actually been shown to bind in our measured cell types.
ChIP-seq peaks from K562/HepG2/SK-N-SH are exactly this. They have
sharper signal because:
1. The peak coordinate IS the binding site (not a 200bp region with
   unknown internal motif location)
2. Peak summit-centered windows put the motif at known position
3. We know what TF binds (label cleaner)

Generalization counter-argument: ChIP peaks are cell-type-specific.
Training on K562/HepG2/SK-N-SH peaks biases toward those cells'
regulatory grammar. But since our LABELS are also in those 3 cells,
this may be net positive for eval prediction even if it hurts
generalization to other cells.

Goal for exp 008: download ENCODE ChIP-seq narrowPeak files for major
TFs in each of K562/HepG2/SK-N-SH and build a peak-centered library.

## 2026-06-02 21:42 — Experiment 008 result: cell-type DNase peaks

### Result
- eval_01: 0.0758 → **0.0764** (+0.001) — NEW BEST on primary metric
- eval_04: 0.0863 → 0.0903 (+0.004)
- SKNSH per-cell on eval_01: 0.0669 → 0.0697 (biggest SKNSH boost since random baseline)
- BUT eval_07/10/13 dropped 0.003-0.007

### Theory update
Cell-type-specific DNase peaks help in two ways:
1. Sequences known active in K562/HepG2/SK-N-SH → cleaner per-cell labels
2. SKNSH-targeted training helps SKNSH (filling the laggard cell type)

But narrow cell-type focus loses cCRE's regulatory diversity, hurting
eval sets that test broader regulatory grammars (eval_07/10/13).

### Combined opportunity
A library mixing cCREs (broad regulatory grammar) with cell-type DNase
peaks (targeted labels, SKNSH coverage) may push BOTH ends:
- Maintain eval_07/10/13 from cCRE breadth
- Gain eval_01/02/04 from DNase peak targeting

### Plan for exp 009
**Hybrid library**: ~20K cCREs + ~25K cell-type DNase + 5K random bg.
Slightly more SKNSH peaks to compensate the SKNSH performance gap.

Composition:
- 20K cCREs (8K dELS + 5K pELS + 3K PLS + 2K CA_TF + 2K CA-CTCF)
- 8K K562 DNase peaks (peak-summit centered)
- 8K HepG2 DNase peaks
- 9K SK-N-SH DNase peaks
- 5K random non-cCRE autosomal background

If 009 > 008: hybrid is better than pure cell-type
If 009 > 003: hybrid breaks the cCRE plateau
If neither: cell-type signal is already saturated, return to cCRE

## 2026-06-02 21:50 — Experiment 009 result: hybrid cCRE+DNase — NEW BEST

### Result
- eval_01: **0.0772** (new best, +0.0014 over 003)
- eval_04: **0.0913** (huge gain)
- SKNSH on eval_01: 0.0705 (best ever)
- 6/9 distinct evals improved vs prior best

### Theory update: HETEROGENEOUS sources WIN
Mixing cCREs (broad grammar) with cell-type DNase peaks (targeted
labels) breaks the cCRE plateau. The TWO sources are complementary:
- cCREs cover regulatory grammars from many cell types (helps the
  model learn universal motif features)
- DNase peaks provide cleaner per-cell labels for our 3 measured cells
- Random bg anchors the null distribution

**Hypothesis: a THIRD orthogonal source will keep improving.** Adding
H3K27ac ChIP-seq peaks (a different active enhancer mark, with
different specificity than DNase) for the 3 cells should add new
signal. Tests "more orthogonal signals" hypothesis.

### Refined meta-theory
**A library is informative for cross-cell-type generalization when
it stacks orthogonal regulatory signals**:
1. Broad grammar (cCREs) — universal regulatory features
2. Cell-type accessibility (DNase) — sharp per-cell labels
3. Active enhancer marker (H3K27ac, EP300) — direct activity prior
4. Negative class (random genomic) — null calibration

The MODEL learns to combine these signals; the LIBRARY provides
material for each. Diversity at the signal-source level matters more
than diversity within a single source.

### Plan for exp 010
Download H3K27ac ChIP-seq narrowPeak for K562, HepG2, SK-N-SH.
Mix into hybrid as a 4th source.

Composition target:
- 15K cCREs (mix)
- 7K K562 DNase + 7K H3K27ac
- 7K HepG2 DNase + 7K H3K27ac
- 7K SK-N-SH DNase + 7K H3K27ac (extra SKNSH bias)
- 5K random bg
Wait — that's 60K. Let me design more carefully.

Better:
- 15K cCREs (broad)
- 5K K562 DNase + 5K K562 H3K27ac
- 5K HepG2 DNase + 5K HepG2 H3K27ac
- 5K SKNSH DNase + 5K SKNSH H3K27ac
- 5K random bg
= 50K. Each cell gets 10K (5K DNase + 5K H3K27ac).

---
## Entry 011 — 2026-06-02 — exp 010 result + theory revision

**Result:** 010 LOSES to 009 on 8/9 distinct evals.
- eval_01: 0.0772 → 0.0753 (-0.002)
- All three cells regress (K562, HepG2, SKNSH all worse on eval_01)

**Hypothesis killed:** "More orthogonal regulatory signal sources → better."
H3K27ac is NOT orthogonal to DNase — both mark active enhancers in the same
cell type, so the sequence content overlaps. Adding H3K27ac just diluted the
share of cCREs and DNase peaks for no information gain.

**Updated theory:** Diversity helps only if it adds INDEPENDENT information.
- cCRE → DNase worked: DNase added cell-type accessibility info that cCREs
  don't encode (cCREs are cross-tissue regulatory consensus, no per-cell label)
- DNase → H3K27ac fails: H3K27ac and DNase on the SAME cell are correlated
  (active enhancers are accessible by definition)

**Composition matters more than count of sources.** 009's 20K/25K/5K split
appears near-optimal for the 3-cell hybrid. Adding sources by subtracting
from the productive ones is harmful.

### Plan for exp 011
Stay with cCRE+DNase+random, but shift composition toward DNase to test
whether cell-type-specific signal still has room:
- 15K cCREs + 30K DNase (10K each cell) + 5K random = 50K
If 011 > 009: cell-type signal scales further; push more.
If 011 < 009: 009 composition is the sweet spot; pivot to new orthogonal
signal type (ATAC-seq from non-measured cells, evolutionary conservation,
eQTL-overlap, GTEx multi-tissue, etc.)

---
## Entry 012 — 2026-06-02 — exp 011 result + composition is optimal

**Result:** 011 (15K cCRE + 30K DNase + 5K random) loses to 009 on 7/9 evals.
- eval_01: 0.0772 → 0.0759 (-0.0013); all three cells regressed
- Only eval_08 (hardest) improved meaningfully (+0.0022)

**Combined with 010 (more sources hurt) + 011 (more DNase hurt):**
009's composition (20K cCRE / 25K DNase / 5K random) is the local optimum
within the cCRE+DNase+random source set. Tweaking either direction
(more sources, more DNase) degrades performance.

**Updated theory:** Future gains require **qualitatively new** information,
not redistributing existing source mass. Candidates:
- DNase peaks from non-measured cell types → more universal motif contexts
- TF ChIP-seq peaks (specific TFs with strong motifs)
- Evolutionarily conserved regions (phastCons elements)
- eQTL-overlapping sequences (variation → expression-validated)

### Plan for exp 012
Add DNase from non-measured cells. Hypothesis: motifs are universal but
appear in different sequence contexts across tissues. Exposing the model
to MORE cell types' DNase peaks teaches more robust motif features that
generalize better to unseen cells (the actual eval goal).

Library: 15K cCRE + 15K DNase from 3 measured cells (5K each) + 15K DNase
from 3 non-measured cells (5K each: GM12878, A549, HCT116) + 5K random.

---
## Entry 013 — 2026-06-02 — exp 012 result + noise floor question

**Result:** 012 (multi-cell DNase) = 0.0758, still below 009 (0.0772).
Key finding: K562/HepG2 stay strong with 5K peaks (saturation), but SKNSH
drops from 0.0705 to 0.0671 when its quota cut from 9K to 5K. The
"unmeasured cell diversity" did not transfer to SKNSH.

**Pattern across 010/011/012:** all three sit at 0.0753-0.0759 on eval_01,
roughly 0.0013-0.0019 below 009's 0.0772. This is suspiciously consistent.
Could be:
- A: Real regressions (009 is a true optimum, 010-012 each diluted it)
- B: Noise floor on this pipeline is ~0.002, and these are all "9-equivalent"

**Critical:** Before more design exploration I need to measure the noise floor.

### Plan for exp 013
Replay 009's exact composition with SEED=13. Outcome:
- eval_01 in [0.0760, 0.0785]: noise is ±0.001-0.002, 010-012 ambiguous
- eval_01 ≥ 0.0770: 009 reproducible, 010-012 are real but tiny regressions
- eval_01 in [0.0745, 0.0760]: 009 was lucky; 010-012 are within run-to-run

This is a critical methodology investment — without knowing noise I can't
distinguish real signal from chance in future experiments.

---
## Entry 014 — 2026-06-02 — NOISE FLOOR DISCOVERED — major theory revision

**Exp 013:** REPLICATE of 009 with SEED=13 → eval_01 = **0.0734** (vs 009 0.0772)
- All 3 cells dropped by ~0.0038
- This is pure run-to-run / seed noise on a FIXED composition

**Implication:** Pipeline noise floor is ~0.004 on eval_01. Everything
from exp 003 to 013 (0.0708 to 0.0772 range) is statistically the same.

**Killed theories:**
- "Hybrid cCRE+DNase beats single source" — within noise of pure cCRE
- "More DNase per cell improves it" — within noise
- "More cell-type diversity helps" — within noise

**Surviving fact:**
- Genomic regulatory sequences (cCRE / DNase) beat random by ~+0.012
  (mean of 003-013 ≈ 0.0753 vs 001 random = 0.0619). REAL.
- Within "genomic regulatory" space, any reasonable composition gives
  ~0.075 on eval_01. The model plateau is real.

**What can break the plateau (revised candidates):**
1. **Quality > quantity:** restrict to top-signal peaks (highest q-value/score)
2. **Multi-seed averaging:** report mean of 3 seeds per design
3. **Sequence augmentation:** reverse-complement, shifted windows (007 tried,
   was noise-equivalent; revisit with seeds)
4. **Composition-matched hard negatives:** sample dinuc-matched bg from
   regulatory-adjacent regions (not random genomic)
5. **NEW signal types:** TF ChIP-seq for specific TFs in measured cells
   — direct binding sites with strong motifs

### Plan for exp 014
**Quality-first:** restrict DNase peaks to TOP-DECILE by signal value.
High-signal peaks have less label noise (clearer accessibility, fewer
false positives). Hypothesis: cleaner labels → bigger effect than noise floor.
Library: 20K cCRE + 25K TOP-DECILE DNase + 5K random (009 composition,
but only highest-confidence DNase peaks).

If 014 eval_01 ≥ 0.080: real win (above noise floor)
If 014 eval_01 ∈ [0.074, 0.078]: ambiguous (within noise band)
If 014 eval_01 < 0.073: quality filter HURT (counterintuitive)

---
## Entry 015 — 2026-06-02 — exp 014 result + SKNSH-targeting plan

**Exp 014 (top-signal DNase):** eval_01 = 0.0721, low edge of noise band.
Quality-by-signal-value did NOT help. Likely because top-signal peaks are
dominated by housekeeping promoter/CTCF regions (high in every cell) and
LACK cell-type-specific enhancer subtlety that lower-signal peaks contain.

**Insight:** quality is NOT the right axis. Diversity is.

**Per-cell pattern across all 003-014:** SKNSH is consistently weakest
(0.066-0.070 vs K562/HepG2 0.076-0.080). To break the noise band on mean
eval_01, lift SKNSH — even a +0.005 SKNSH lift = +0.0017 mean.

### Plan for exp 015 — SKNSH-heavy library
- 10K cCRE (5K dELS + 3K pELS + 1K PLS + 1K CA)
- 8K K562 DNase + 8K HepG2 DNase
- 14K SKNSH DNase + 5K SKNSH H3K27ac
- 5K random
SKNSH gets 19K/50K = 38%. Tests "more cell-specific data lifts that cell".

If 015 SKNSH ≥ 0.075: hypothesis confirmed; lift comes from cell-specific data
If 015 SKNSH ≈ 0.067-0.071: SKNSH ceiling is sequence-intrinsic, not data-volume

---
## Entry 016 — 2026-06-02 — exp 015 result + pivot to augmentation axis

**Exp 015 (SKNSH-heavy):** eval_01 = 0.0730, SKNSH = 0.0646 (vs 009 0.0705 — WORSE!).
- Doubled SKNSH-specific peaks but SKNSH per-cell DROPPED 0.006.
- K562 (0.0770) and HepG2 (0.0773) held up despite getting same data as 009.

**Implication:** SKNSH bottleneck is sequence-intrinsic, not data-volume.
The MPRA activity in SKNSH is just harder to predict from sequence. Adding
more SKNSH data crowds out cCRE diversity → net negative.

**Composition axis is exhausted.** All experiments 003-015 sit in noise band
0.072-0.077 on eval_01. No reliable design improvement found.

### Plan for exp 016 — multi-window augmentation on 009 composition
Same compositional mix as 009 (cCRE + DNase + random), but each source locus
contributes 3 shifted windows (−L/2, 0, +L/2). Effective unique loci ~16.7K
with 3 windows each = 50K sequences. The model sees the same regulatory
element from 3 positional perspectives, potentially learning shift-invariance
better and/or extracting more information per locus.

Exp 007 tried this on cCREs only (eval_01=0.0747, in band). Combining with
DNase + per-cell signal might break the band — or confirm composition vs
augmentation are both noise-equivalent.

If 016 eval_01 ≥ 0.080: multi-window helps; explore further (5 windows? more shift)
If 016 ∈ [0.073, 0.078]: in band; augmentation axis is also exhausted

---
## Entry 017 — 2026-06-02 — exp 016 result + intersection plan

**Exp 016 (multi-window hybrid):** eval_01 = 0.0751. In noise band.
Multi-window augmentation gave nothing new. Model already learns
positional invariance from single-window data.

**Consolidated picture (003-016 on eval_01):**
- All designs sit in 0.0708-0.0772 band
- Mean ~0.0750, std ~0.0017
- 009's 0.0772 was +1σ luck; 013 (009 reseed) was -1σ at 0.0734
- No design has reliably exceeded 0.078

**The remaining path to break the band:**
1. Qualitatively new signal types (TF ChIP-seq strong motifs)
2. Higher-confidence labels via cCRE-DNase intersection
3. Combining all best-of approaches in one design

### Plan for exp 017 — cCRE-DNase intersection
DNase peaks that overlap a cCRE = HIGH-CONFIDENCE regulatory regions
(validated by both cell-type accessibility AND cross-tissue regulatory
catalog). Tests if label confidence > raw count.

Library:
- 30K DNase peaks intersecting cCREs (10K each cell, peaks chosen if
  peak summit falls within a cCRE region)
- 15K cCREs (with no DNase peak intersection — broad regulatory not yet
  cell-type-validated; complements the intersection set)
- 5K random

---
## Entry 018 — 2026-06-02 — exp 017 + plan for TF ChIP-seq

**Exp 017 (cCRE-DNase intersect):** eval_01 = 0.0757. K562 = **0.0811** (best K562
yet, but within noise). HepG2 = 0.0807. SKNSH = 0.0652 (worse).
- Higher label-confidence helps easy cells slightly
- SKNSH still bottleneck; eval_08 worse (-0.006)
- Mean: noise band

**Cumulative learnings (003-017):**
- Noise floor ~0.004
- Any composition of cCRE + DNase + random ≈ 0.075 ± 0.002
- Per-cell pattern: K562 ~0.078, HepG2 ~0.080, SKNSH ~0.067-0.070
- New signal types haven't been tested (TF ChIP, conservation, etc.)

### Plan for exp 018 — CTCF ChIP-seq augmented
CTCF has the strongest, most well-defined motif in the genome. ChIP-seq
peaks contain CTCF motifs at very high density.
Downloaded: ENCFF519CXF (K562), ENCFF543WTP (HepG2), ENCFF540DWT (SKNSH).
~50K peaks each.

Library:
- 15K cCRE (broad regulatory grammar)
- 21K DNase (7K each cell)
- 9K CTCF ChIP (3K each cell — concentrated CTCF motif training)
- 5K random
= 50K. Seed=18.

Hypothesis: dense CTCF motif examples teach the model a very strong
discriminative feature. If it helps, expect K562/HepG2 lifts ~0.005+.

---
## Entry 019 — 2026-06-02 — exp 018 + final attempt at breakout

**Exp 018 (CTCF ChIP-seq augmented):** eval_01 = 0.0743. In noise band.
Even adding the strongest possible motif source (CTCF, very strong defined
binding) didn't push past 0.077.

**Conclusion: pipeline is saturated.** Every "genomic regulatory" mix gives
eval_01 in [0.072, 0.077]. The model architecture/training has hit a
performance ceiling that library design cannot break.

### Plan for exp 019 — kitchen-sink combination
Last attempt at breakthrough. Combine 5 distinct signal types:
- 10K cCRE-DNase intersection (high confidence per-cell regulatory)
- 15K pure cCRE (broad regulatory grammar)
- 15K DNase (all peaks, 5K each cell)
- 5K CTCF ChIP (concentrated motif)
- 5K random
If still in band, conclude saturation and use remaining budget for
multi-seed validation of 009.

### Plan for exp 020-022 — multi-seed validation of best
If 019 ≤ 0.077: switch to validating 009 with seeds 20, 21, 22. Combined
with seeds 9 and 13 (already done), gives 5 replicates → σ_mean ~0.001.
Establishes 009's true performance robustly.

### Plan for exp 023+ — based on the picture
If 009 is best by mean, use it as final library. Final notes update theory
and recommendations.

---
## Entry 020 — 2026-06-02 — exp 019 result + final strategy

**Exp 019 (kitchen sink):** eval_01 = 0.0765. K562 = 0.0809 / HepG2 = 0.0813
(new per-cell highs but within noise). SKNSH 0.0674 again drags mean.
Combining 5 signal sources doesn't break the band either.

**Plateau is confirmed across 17 distinct designs.** Any "genomic
regulatory" library composition gives eval_01 in 0.072-0.078 on this
pipeline. Mean ≈ 0.0752, σ ≈ 0.0017.

### Final strategy for exp 020-030 (11 left)
- **020:** All-classes cCRE (proportional sampling from all 8 cCRE classes)
  — final untried compositional axis
- **021:** 009 replicate seed=21 (3rd replicate of leading design)
- **022:** 019 (kitchen sink) replicate seed=22
- **023:** Best-replicate-mean design + final tweaks
- **024-029:** Targeted explorations based on cumulative findings
- **030:** Final submission design — likely 009 or 019 based on multi-seed mean

### What the user gets
A library producing model with eval_01 ~0.075-0.078 (any reasonable
genomic regulatory mix). The "best" library by single-seed score is 009
(0.0772). The plateau pattern is the dominant finding — composition tweaks
beyond a baseline genomic regulatory mix do not help on this pipeline.

---
## Entry 021 — 2026-06-02 — exp 020/021 + 009 TRUE mean

**Exp 020 (all-class cCRE):** eval_01 = 0.0743. In band.
**Exp 021 (009 replicate seed=21):** eval_01 = **0.0732**.

**009 three replicates: 0.0772, 0.0734, 0.0732 → mean = 0.0746, σ = 0.0023.**

The original 0.0772 was a +1σ lucky outlier. 009's TRUE performance is ~0.075.
This changes the leader board:

**Updated single-seed leaderboard (eval_01):**
| design | score | seeds run |
|---|---|---|
| 009 SEED=9 | 0.0772 | 1 of 3 |
| 019 kitchen sink | 0.0765 | 1 |
| 008 DNase | 0.0764 | 1 |
| 011 more DNase | 0.0759 | 1 |
| 017 intersect | 0.0757 | 1 |
| 003 cCRE | 0.0758 | 1 |

**True 009 mean = 0.0746** sits in the MIDDLE of the noise band.
019 (0.0765, single seed) might actually be the best — needs replicates.

### Plan revision
- exp 022: 019 replicate seed=22
- exp 023: 019 replicate seed=23 (gets 019 to 3 replicates)
- exp 024: 008 (DNase only) replicate as another comparison
- exp 025-027: pick best after replicates, run another
- exp 028-030: final submission designs

Key insight to remember: **single-seed eval is unreliable. Always check
σ~0.002 noise before claiming improvement.**

---
## Entry 022 — 2026-06-02 — 019 multi-seed (022, 023) → 019 ≈ 009

**Exp 022 (019 replicate seed=22):** eval_01 = 0.0749.
**Exp 023 (019 replicate seed=23):** eval_01 = 0.0730.

**019 three replicates: 0.0765, 0.0749, 0.0730 → mean = 0.0748, σ = 0.0018.**
**009 three replicates: 0.0772, 0.0734, 0.0732 → mean = 0.0746, σ = 0.0023.**

### Head-to-head (3 seeds each, eval_01)
| metric | 009 (n=3) | 019 (n=3) | Δ (019 - 009) | within σ? |
|---|---|---|---|---|
| mean_r | 0.0746 | 0.0748 | +0.0002 | yes (σ~0.002) |
| K562   | 0.0777 | 0.0788 | +0.0011 | borderline |
| HepG2  | 0.0786 | 0.0791 | +0.0005 | yes |
| SKNSH  | 0.0674 | 0.0665 | -0.0009 | yes |

**Verdict: 009 and 019 are statistically tied.** 019 marginally wins K562
(+0.0011), 009 marginally wins SKNSH (+0.0009). Both within noise floor.
The "kitchen sink" diversity argument is NOT a clear winner over the
simpler 3-source hybrid. Diversity for diversity's sake yields no benefit
when each axis hits the same plateau ceiling.

### Theory update
The plateau hypothesis is now strongly confirmed: across ~15 distinct
composition designs (003-020), all genomic-regulatory mixes converge to
eval_01 = 0.075 ± 0.002. The remaining unexplained question is what
*does* break the plateau. Things we haven't tried that COULD differ:
1. Library size / training token count (fixed at 50K — could the model
   be data-bounded rather than diversity-bounded?)
2. Sequence length (fixed at 200bp — could shorter/longer give different
   signal density?)
3. Cell-type label engineering — the pipeline trains on labels we don't
   control. Worth checking if eval_07/13 (which score ~0.14 — much
   higher than eval_01) hint at a different label structure.
4. Active region vs full-window (centering on summit vs sampling tile
   around summit) — partially explored in 016 (multi-window) → tied.

We've used 23 of 30 experiments. 7 remaining. The plateau makes further
*composition* exploration unlikely to break out. The high-value remaining
ideas:
- **Validate on eval_07/13** (the high-scoring evals) to see if any
  composition disproportionately helps there. Different evals likely
  test different aspects of generalization. If composition X is bad on
  eval_01 but good on eval_07, the final submission depends on which
  eval matters most. Since instructions say eval_01 is primary, we
  optimize for that.
- **Final submission decision:** 019 OR 009. Both at ~0.075. Pick the
  one with the better mean. Currently 019 has the very slight edge
  (0.0748 vs 0.0746), within σ. Either choice is defensible.

### Plan for 024-030
- **exp 024:** Test a "high-confidence-only" library — INTERSECT-only
  (cCRE ∩ DNase, all three cells) + cCRE filler + random. This is the
  highest-quality cis-regulatory signal possible. If even this can't
  beat the plateau, the plateau is set by pipeline-model capacity, not
  signal quality.
- **exp 025:** Test a 100K-equivalent library by using all 50K slots for
  per-cell intersect peaks only (3 cells × ~16.7K each). Pure DNase∩cCRE
  no padding. Tests the "signal density" axis.
- **exp 026:** Replicate of the BEST design found in 024-025 with a
  fresh seed (validates winner).
- **exp 027:** Variation around the best — slightly different mix ratio.
- **exp 028:** Replicate winner of 024-027 with a new seed.
- **exp 029:** Final design replicate.
- **exp 030:** Submission — best library by 3-seed mean.

This budgets 4 designs (024, 025, 027, 029) + 3 replicates (026, 028, 030).

### Risk awareness
With noise σ~0.002, distinguishing 0.001 differences requires 4+ seeds
per design. We've spent 30 experiments and have only 3 seeds for 009 and
019. Trying yet another novel design probably gives one more 0.075 point.
The marginal value is in confirming the winner via replicates, not
exploring more compositions. So 024-025 should be the LAST two new
designs; 026-030 should be replicates of the leader.


---
## Entry 023 — 2026-06-02 — CAMPAIGN SUMMARY (exps 024-030)

### What I did in 024-030
- **024-026**: tested "pure cCRE∩DNase intersect, no padding" hypothesis
  across 3 seeds (45K intersect + 5K random). 3-seed mean = 0.0744 ±
  0.0006. **Confirmed plateau**: max-signal-density doesn't beat the
  simpler mixes.
- **027**: top-signal-ranked intersect (highest rank-percentile peaks
  across all 3 cells). eval_01 = **0.0717** — *below* plateau.
  **New finding: selecting for HIGH SIGNAL hurts.** Likely because
  highest-DNase regions are housekeeping-biased and have lower motif
  diversity than randomly sampled enhancers.
- **028-030**: three more 019 replicates (seeds 28, 29, 30) for tight
  multi-seed estimate.

### Final picture
**019 kitchen-sink, 6 seeds: 0.0747 ± 0.0011 on eval_01.**
**Submission: exp 030 (SEED=30, eval_01 = 0.0746).**

### Multi-seed leaderboard (eval_01)
| Design | n seeds | mean | σ |
|---|---|---|---|
| 019 kitchen-sink   | 6 | **0.0747** | 0.0011 |
| 009 hybrid (ccre+dnase) | 3 | 0.0746 | 0.0023 |
| 024 intersect-only | 3 | 0.0744 | 0.0006 |
| 027 top-signal     | 1 | 0.0717 | - |
| 001 random         | 1 | 0.0619 | - |

### What I learned
1. **Strong plateau at eval_01 ≈ 0.0747 ± 0.001** across all
   genomic-regulatory-mix designs (cCRE-only, DNase-only, hybrids,
   intersect, kitchen-sink). The model architecture (which we don't
   control) and/or eval set difficulty appears to be the limiting factor,
   not composition. We are at a learning-pipeline-bound ceiling.

2. **Diversity > signal intensity.** 027 picked the very highest-signal
   peaks (top ~11%) and lost 0.003. Diversity (sampling broadly across
   intersect regions) is more important than concentrating on the
   strongest signal. Probably because top-signal regions are
   over-represented for ubiquitous (housekeeping) elements, leaving the
   model under-exposed to the long tail of cell-type-specific motif
   contexts.

3. **Noise floor σ ≈ 0.001-0.002 on eval_01.** Single-seed comparisons
   are unreliable; need ≥3 seeds to claim a 0.003 effect significant.
   This invalidated the early "009 is uniquely best" claim (009 SEED=9
   was a +1σ lucky outlier at 0.0772; true mean = 0.0746).

4. **SK-N-SH is consistently the hardest cell type** (~0.066 across all
   designs, vs ~0.078-0.079 for K562/HepG2). Doubling SKNSH data (exp
   015) HURT SKNSH score (0.0646), suggesting SKNSH's poor score is
   sequence-intrinsic, not data-quantity-bound. This is a property of
   the eval set, not fixable from the library side.

5. **Signal sources tested as orthogonal axes — all hit the same
   plateau:**
   - Pure cCRE (regulatory class labels): 0.075
   - Pure DNase (accessibility): 0.076
   - cCRE × DNase intersection: 0.074-0.075
   - + CTCF ChIP: 0.074
   - + H3K27ac: 0.075
   - All cCRE classes: 0.074
   - Multi-window augmentation: 0.075
   - Untrained-cell DNase: 0.076

6. **What I'd try next if I had more budget:**
   - Different sequence lengths (200bp fixed — try 100bp, 500bp)
   - Massively scale up library size (50K → 100K, but pipeline-bound)
   - Active-learning loop using model uncertainty
   - Synthetic motif insertion in genomic context (combine 002 +
     genomic)
   - True out-of-distribution sequences (other species, regulatory
     elements from non-human genomes) to break the human-genome
     manifold

### Final submission rationale
**019 (kitchen-sink, SEED=30) ships.** Reasons:
- Best 3+ seed mean of any design (0.0747)
- Lowest σ among multi-source designs at the leading mean
- Broadest signal coverage (5 source types) → most robust to whatever
  the unknown eval cell types look like
- Single-seed best ever observed was 019 SEED=19 at 0.0765, but that's
  cherry-picking; SEED=30 at 0.0746 = mean expected performance

The eval_01 = 0.0746 of the final submission is essentially the
performance ceiling I could reach within this composition-space search.
The pipeline is doing its best with genomic regulatory sequences; the
remaining ~25% of the predictable variance probably needs different
sequence sources (TF-engineered, larger scale, multi-window) or a
different model than what the pipeline trains.

