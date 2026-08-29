# MPRA Library Design Lab Notebook

Append-only. Newest entries at the bottom.

## 2026-06-02 16:30 — Initial theory and plan

### Setup
- 50,000 sequences x 200bp, measured in K562/HepG2/SK-N-SH
- Evaluated on 14 anonymous sets; goal = sequence-to-activity model that generalizes to **unseen cell types**
- 30 experiments allowed; eval_01 is primary

### Initial theory (T0)
A library is informative for cross-cell-type generalization if the *features* the model learns from it transfer. Most regulatory grammar is shared across cell types: TF motifs, GC content, dinucleotide periodicity, chromatin-context proxies (e.g. CpG islands), repressor sites. Cell-type-*specific* features come from which TFs are expressed, but the syntactic rules of how motifs combine into enhancers/promoters are largely shared.

Therefore the most informative library should:
1. **Cover the regulatory motif vocabulary broadly** — many TF families, many spacings, many orientations
2. **Span the activity range densely** — including silencers / non-functional sequences (model needs to learn what does *nothing* too)
3. **Avoid over-representing K562/HepG2/SK-N-SH–specific grammar** — that would create cell-type-biased features
4. **Be sequence-diverse** — k-mer diversity prevents the model from memorizing motifs in narrow sequence contexts
5. **Include negative/random controls** — pure-random sequences as a "baseline expression" anchor

### Predictions
- Pure random DNA: low ceiling because no motif structure → model learns only base-composition effects
- Natural human DNA (random genomic): better than random, learns natural motif co-occurrence statistics
- Promoter/enhancer enriched: even better, dense in functional grammar
- Synthetic motif-tiled DNA: high diversity per nucleotide, possibly best for motif coverage but lacks natural context
- A mix > any pure source

### Experimental roadmap (revisable after each result)
1. exp 001: pure random DNA — baseline floor
2. exp 002: natural human DNA from random genomic windows — naturalness baseline
3. exp 003: synthetic motif-rich (JASPAR motifs embedded in random) — motif-density test
4. exp 004: ENCODE cCRE (candidate cis-regulatory elements) — functional density
5. exp 005-30: refine based on what wins

### Constraints I noticed
- prepare.py is sealed; treat as wet-lab
- I do not know what eval sets contain
- Must not peek at eval_sets.pkl (in parent dir)

### What "generalize beyond labeled cell types" implies for library design
A model trained on K562/HepG2/SK-N-SH labels learns a mapping seq → 3-vector. When applied to cell type X, the model has no label for X. To predict X, it must rely on features shared with the training cell types. The library should therefore maximize the *shared* feature surface area the model can learn — motif identities, motif syntax, GC effects — and minimize sequences whose activity is dominated by features only meaningful in one of K562/HepG2/SK-N-SH (e.g. very strong cell-type-specific TFBS combinations).

## 2026-06-02 16:35 — Exp 001 result: random DNA mean_r=0.307

### Result
- eval_01 = 0.3068 (primary)
- range across 14 evals: 0.110 to 0.402
- 88s wall, 56s training
- See `libraries/001_random_uniform/notes.md`

### Surprises
1. **r=0.30 from random DNA is high.** I expected r≈0 to 0.1. Either: (a) GC/composition really do explain ~30% of MPRA variance, (b) the reporter has strong baseline expression governed by composition, or (c) the eval set has limited dynamic range so even a weak predictor scores. Most likely (a)+(b).
2. **K562 always == HepG2.** Not "approximately equal" — exactly equal in every eval and every metric. For random DNA the model collapses to predicting them identically. Open question: do real DNA libraries break this symmetry, or is K562 == HepG2 a built-in property of the eval labels?
3. **9 distinct evals, not 14.** Several evals return identical numbers (e.g. eval_01==eval_05==eval_14). Reasonable working assumption: 14 evals but with duplicates / overlaps.
4. **eval_07 easiest, eval_08 hardest.** eval_08 = 0.11 even with random sequences — could be a held-out set with very different properties (e.g. only high-expressors, only one cell type).

### Theory update
- Baseline floor for composition-only signal: ~0.30 mean_r.
- The remaining headroom must come from motif content and motif syntax.

### Next experiment plan (002)
**Natural genomic DNA from random windows.** This isolates the question: does the model improve when it sees *natural* base-composition statistics (CpG depletion, k-mer co-occurrence, dispersed motifs)? If 002 ≫ 001, then natural composition matters. If 002 ≈ 001, then motif density is what matters and 002 is too dilute.

Justification for cross-cell-type generalization: natural human DNA contains the universal regulatory grammar (TFBS, splice signals, CpG islands) that any cell type's regulatory machinery uses. A model trained on it will learn features shared across all human cell types, not features specific to K562/HepG2/SK-N-SH.

Source: I will sample 200bp windows from the human reference genome (hg38). I don't have it locally — need to download chrom-by-chrom from UCSC, or use a faster source.

## 2026-06-02 16:38 — Exp 002 result: natural genomic mean_r=0.480

### Result
- eval_01 = 0.4798 (+0.173 vs random, +56% relative)
- eval_07 = 0.6002 best; eval_08 = 0.0934 worst (**regressed** vs random!)
- 82s wall

### Big takeaways
1. **Natural genomic DNA crushes random DNA** on 13/14 evals. Natural
   composition + dispersed regulatory motifs matter a lot.
2. **eval_08 regressed** from 0.110 to 0.093. eval_08 likely contains
   sequences with very different statistics from natural genomic DNA —
   maybe purely synthetic, or designed adversarial sequences. The fact
   that *random uniform DNA* did better on eval_08 supports this.
3. K562 == HepG2 still holds exactly. Confirmed property of eval labels.
   I will report mean_r and not chase K562/HepG2 distinction.

### Theory update
- Composition + natural regulatory grammar dominates the signal.
- Cell-type-specific tuning isn't needed to reach r=0.48 — universal
  features go a long way. This is good news for generalization.
- The headroom from here is in *enrichment* (regulatory density) and
  *coverage* (sequence-space diversity), not in "K562-specific tricks".
- eval_08 hints that the eval set is *not* monolithic. Some evals reward
  natural DNA; one penalizes it. A diverse library may need to deliberately
  include sequences unlike natural DNA to stay competitive on eval_08.

### Hypothesis for exp 003
**ENCODE cCRE-centered sequences** (200bp windows centered on cCREs from
ENCFF286VQG, 2.3M elements). If regulatory density is what matters, this
should beat random natural DNA on most evals. But it may regress further
on eval_08 since it's even more "natural".

Generalization argument: cCREs are the union of regulatory regions identified
across many cell types (not just K562/HepG2/SK-N-SH). They're the
"vocabulary" of human gene regulation — model trained on them should
transfer to any cell type that uses the same vocabulary.

## 2026-06-02 16:43 — Exp 003 result: cCRE-centered mean_r=0.345 (SURPRISE: worse than exp 002)

### Result
- eval_01 = 0.3446 (vs 0.4798 natural genomic, **-0.135**)
- eval_07 = 0.2826 (vs 0.6002, **-0.32**, massive)
- Almost back down to random-DNA baseline

### This contradicts my prediction
I expected cCRE > natural because cCREs are denser in regulatory motifs.
The opposite happened. Need to take this seriously, not explain away.

### Refined theory (T1)
A library is informative if it covers the **(sequence × activity) space**
broadly, not if it's dense in functional motifs. The model must learn:
- which sequences are inactive (the most common kind in the genome)
- which sequences are weakly active
- which are strongly active and why
A cCRE-only library is missing the "inactive" half of the activity axis.
The model trained on it cannot learn to *discriminate* between active and
inactive in eval — every input looks active to it.

### What does this mean for cross-cell-type generalization?
The previous T0 said: "Cover the regulatory motif vocabulary broadly."
The new T1 says: "Cover the activity range broadly *and* the motif
vocabulary." These are different! Dense motif libraries can collapse the
activity range.

For a model evaluated in unseen cell types, the most generalizable signal
is **what makes a sequence active vs inactive in *any* cell type** —
which requires seeing both halves.

### Next experiment plan (004)
**Mix: 25K random natural genomic + 25K cCRE-centered.** Tests whether
the cCRE component adds value when paired with broad-coverage natural DNA.
- If mix > 0.48 (exp 002): cCRE adds value, just needs the natural-DNA
  backbone.
- If mix ≈ 0.48: cCRE neither helps nor hurts when diluted.
- If mix < 0.48: cCRE actively harms even when diluted (the negative
  examples in 25K of natural don't compensate for biased 25K cCRE).

This is the single most informative next experiment given the result.

## 2026-06-02 16:46 — Exp 004 result: mix natural+cCRE mean_r=0.494 (small gain)

### Result
- eval_01 = 0.4937 (+0.014 vs pure natural; +0.149 vs pure cCRE)
- Marginal but consistent gain over natural on 13/14 evals
- eval_08 still ~0.09 — unaffected by anything I've tried

### Theory update (T2)
- Library diversity > library purity. Mix outperforms pure.
- The natural-DNA backbone provides activity-range coverage (positive AND negative examples). cCRE adds motif density.
- Diminishing returns when adding cCRE on top of natural: marginal gain only 3% relative.
- eval_08 is special — none of natural, cCRE, or mix moves it. Suggests it tests sequences with very different statistics from human genome.

### eval_08 hypothesis
eval_08 might contain:
- Pure synthetic / random sequences (no natural features to detect)
- Sequences from a non-human species
- Sequences from a very specific motif class (e.g. just one TF's binding sites)
- Sequences where activity is dominated by k-mer entropy or composition outliers
Test: a synthetic motif library should either help eval_08 (if motifs matter)
or leave it alone (if eval_08 is "anti-natural" in some other way).

### Next experiment (005)
**Synthetic JASPAR motif library.** Embed 1-3 JASPAR motif hits into
random backgrounds. 50K sequences, motif diversity covering many TF families.
- If 005 > 0.50 on eval_01: motifs are the main signal; library design
  should be motif-driven.
- If 005 ≈ 0.40 (like cCRE): motif-only also collapses activity range.
- If 005 specifically lifts eval_08: eval_08 tests motif-rich synthetic.

This tests whether **explicit motif coverage** can substitute for natural-DNA
context, which would be informative about what the model learns vs what
the eval set requires.

## 2026-06-02 16:48 — Exp 005 result: synthetic motif library mean_r=0.155 (SURPRISE: worse than random)

### Result
- eval_01 = 0.1548 — worse than random uniform DNA (0.31)
- Catastrophic on all but eval_07 (0.38) and eval_13 (0.30)
- Hypothesis "motif content drives signal" → falsified

### Theory update (T3)
- Motif content alone, in unnatural context, is **adversarial**.
- The model learns from the *distribution* of sequences (k-mer co-occurrence,
  dinucleotide context, etc.) at multiple scales — not just from local motif
  hits.
- Random-background + isolated motifs creates a distribution that confuses
  models trained for natural sequence prediction.
- **Lesson:** the library must look like the regulatory landscape, in shape
  not just in content.

### Combined picture so far
| Library | eval_01 | Notes |
|---|---|---|
| Random uniform | 0.307 | composition floor |
| Natural genomic | 0.480 | base case |
| cCRE-only | 0.345 | activity collapse + distribution shift |
| Natural+cCRE mix | 0.494 | best so far |
| Synthetic motif | 0.155 | adversarial distribution |

### Refined theory (T3)
A library is informative if and only if its sequence distribution **matches the
distribution of plausible regulatory genomes** the eval set is drawn from.
Within that constraint, more motif content and activity diversity help. But
violating that constraint (synthetic, all-cCRE) costs more than motif
density gains.

### For cross-cell-type generalization
This makes sense: the model's task is to read genomic sequences as functional
regulatory elements. The transferable features come from learning the
language of natural sequences, not from memorizing specific motif
appearances. Any cell type that uses the same DNA substrate will care about
the same features.

### Next experiment (006)
**Motifs embedded in NATURAL background.** 50K natural genomic windows,
augmented with 1-2 JASPAR motif insertions per sequence. Tests if motif
augmentation provides additive value on top of natural context.
- If 006 > 0.49: motif augmentation helps in natural context.
- If 006 ≈ 0.49: natural context already contains enough motif diversity.
- If 006 < 0.49: insertion disrupts natural context (also possible).

This is a clean test of "natural context + extra motif coverage."

## 2026-06-02 16:53 — Exp 006 result: natural + inserted motifs mean_r=0.470 (slightly worse than pure natural)

### Result
- eval_01 = 0.4701 (vs 0.480 pure natural, -0.01)
- Mirrors exp 002 pattern, slightly attenuated everywhere

### Confirms theory T3
Inserted motifs in natural background slightly hurt — they create
unnatural motif-flank pairings. The model values natural context
*everywhere*, including the bases around each motif.

Real cCRE > synthetic motif insertion, even when the natural backbone
is the same. cCRE sequences carry the motif in its naturally-evolved
context, which evidently matters for the model.

### Sharper theory (T4)
The model learns a structural prior over **natural regulatory genomes**.
Anything that violates it (synthetic flanks, forced insertions, distribution
shift to all-active sequences) hurts. Maximum information per sequence is
extracted when the sequence is a natural region of the human genome,
possibly one that is enriched for regulatory features.

For cross-cell-type generalization, this prior is universal — it's the
same DNA grammar regardless of which cell type reads it. So a model
trained on naturalness-respecting libraries should transfer well.

### Most-informative next experiments
Now I want to explore the orthogonal directions that respect naturalness:

1. **Multi-source natural diversity**: ENCODE DHS index (3.6M elements from
   438 biosamples). Tests if regulatory atlases covering more cell types
   are a better source than cCRE alone. Critical for generalization since
   it samples across cell types.
2. **Natural+cCRE ratio sweep**: 75/25, 25/75 to find the curve's peak.
3. **Promoter vs enhancer**: PLS-only mixed with natural vs dELS-only
   mixed with natural — does the type of regulatory element matter?
4. **Augmentation**: reverse-complement, mild k-mer-preserving shuffle —
   purely "free" diversity at no naturalness cost.

I will go with #1 first: download DHS index, mix 25K natural + 25K DHS.
This is the test of "regulatory diversity across cell types" — the most
direct test of cross-cell-type generalization premise.

## 2026-06-02 16:54 — Plan exp 007

DHS Index hg38: from Meuleman et al. 2020 Nature, 3.59M DHSs called across
438 biosamples. URL discoverable at meuleman.org. If too large, use just
the high-confidence subset.

## 2026-06-02 16:56 — Exp 007 result: natural+DHS mix mean_r=0.490 (~tied with cCRE mix)

### Result
- eval_01 = 0.4898 (natural+DHS) ≈ 0.4937 (natural+cCRE, exp 004)
- Pattern nearly identical to exp 004 on all evals
- eval_08 still 0.10

### Interpretation
The "which regulatory atlas" choice doesn't matter much: cCRE and DHS
give equivalent marginal lift over pure natural. What matters is HAVING
a regulatory enrichment component on top of a natural-DNA backbone.

This is a small disappointment for the cross-cell-type hypothesis: DHS
samples 438 biosamples, much more diverse than cCRE which was
ENCODE-centric. The fact that they perform identically suggests the model
is NOT extracting cell-type-specific signal from the regulatory subset
— it's just learning "this is a regulatory-looking sequence" vs "this is
genomic background."

### Theory update (T4 stable)
The library that maximizes cross-cell-type generalization is:
- Mostly NATURAL human genomic DNA (composition + activity range)
- Plus 30-50% regulatory enrichment from ANY atlas (motif density)
- Diminishing returns past 2 sources

Specific cell-type provenance of regulatory regions matters less than I
thought. The model learns universal regulatory features either way.

### Next experiment plan
Most informative single experiment: test a true 3-way mix to confirm
the "saturation" hypothesis. If 3-way ≈ 2-way ≈ 0.49, mix is saturated.
If 3-way > 2-way, more sources still help.

Alternative: pursue eval_08 (immune to everything so far). Try
dinucleotide-shuffled natural — high entropy, natural-like composition.
This could test whether eval_08 cares about k-mer-randomness more than
about regulatory grammar.

Decision: do BOTH in one experiment. exp 008 = 20K natural + 15K cCRE +
15K dinuc-shuffled natural. Multi-source AND eval_08-targeted.

## 2026-06-02 17:00 — Exp 008 result: 3-way mix shuffled mean_r=0.493 (plateau confirmed)

### Result
- eval_01 = 0.4934, essentially tied with exp 004 (0.4937)
- 3-way mix doesn't beat 2-way mix
- eval_08 = 0.09, not helped by shuffled controls

### Important finding: PLATEAU at ~0.49
Across 4 different mixes (natural, natural+cCRE, natural+DHS, 3-way),
performance saturates at ~0.49 on eval_01. The library composition has
reached the bound that natural-DNA-based strategies can hit.

### What this tells us
- The model's ability to predict ANY natural-style eval set tops out around
  ~0.49 with a natural-only library. Above that requires either:
  (a) sequences from genuinely different distributions (cross-species,
      activity-stratified, etc.)
  (b) a model architecture change (out of our control)
- eval_08 isn't reachable by any "respect naturalness" library. It tests
  something orthogonal.

### Refined theory (T5)
A library is informative for cross-cell-type generalization if its
sequence distribution matches plausible regulatory genomes. The natural
baseline achieves ~0.48; adding small amounts of curated regulatory
content (cCRE/DHS) lifts to ~0.49. Beyond this, the bottleneck is
**information per sequence** — not source diversity but *what the
model can extract from 50K x 200bp sequences*.

This implies further experiments should test:
- Different **sequence selection strategies** for the same 50K budget
  (e.g., maximize k-mer entropy, maximize cCRE overlap, etc.)
- Whether **larger natural contexts** sampled into 200bp windows behave
  differently (e.g., always take 200bp from middle of a 1000bp window
  centered on a transcription start site)
- Whether **cross-species DNA** (mouse) added to the mix breaks the plateau

### Next experiment (009): off-center cCRE windows
Take 25K natural + 25K windows containing a cCRE at a random offset
(not centered). Tests if positional diversity of regulatory elements
within natural windows helps, or whether centering was already optimal.

## 2026-06-02 17:05 — Exp 010 result: human+mouse mix mean_r=0.474 (mouse hurts slightly)

### Result
- eval_01 = 0.4739 (vs 0.4798 pure human natural, -0.006)
- Mouse mix is **worse** than pure human
- eval_08 = 0.0962 (slight improvement, the first thing to nudge it up)

### Interpretation
- Regulatory grammar is largely shared across mammals but not perfectly.
  Mouse adds ~1-3% relative noise that hurts on human-eval.
- For human-cell-type generalization, human-only sampling is optimal.
- Mouse may contribute to eval_08 (the immune one), suggesting eval_08
  contains "OOD-like" sequences where evolutionary diversity helps.

### Theory T5 stable
The library should be drawn from the **species you want to predict in**.
Cross-species adds noise. For cross-cell-type generalization within human,
human DNA is the right source.

### Best so far
exp 009 (off-center cCRE mix) = 0.4956 on eval_01.

### Plateau analysis
~0.49-0.50 ceiling across all natural-based libraries I've tried.
Variation between strategies: 0.474 to 0.496 — ~5% relative spread.

### Next experiment plan (011)
Approach the plateau from a different angle: **focus on the *type* of
regulatory enrichment**. Specifically, mix natural with PROMOTER-only
windows (cCRE PLS class only) vs natural with ENHANCER-only (dELS only).
Tests if there's a regulatory class that's particularly informative.

Alternative: try a 4-way mix that combines all winning ingredients
(natural + cCRE-offcenter + DHS + small mouse).

Going with the 4-way mix. It's the most direct test of "can I stack
all small gains into a bigger one."

## 2026-06-02 17:10 — Exp 011 result: 4-way mix mean_r=0.5012 (PLATEAU BROKEN, NEW BEST)

### Result
- eval_01 = **0.5012** — first time over 0.50!
- Improvements vs 2-way mix on every eval except eval_08 (and eval_07 slight drop 0.602→0.596)
- Time 73s

### Big finding: MULTI-SOURCE STACKING WORKS
Stacking 4 sources (natural + cCRE + DHS + mouse) gives ~+0.006 mean_r
over best 2-way. Even though cCRE and DHS are correlated (both
"regulatory open chromatin"), having both adds signal. The 5K mouse
component, despite hurting in pure-mouse mix, contributes a slight
positive when constrained <10%.

### Refined theory (T6)
The library is informative if it spans the **plausible regulatory
sequence distribution** AND if it provides **diverse perspectives on
that distribution**. Having multiple sources for the regulatory subspace
(cCRE + DHS) and a small species-diversity component (mouse) reduces
model bias toward any single source's idiosyncrasies. Each source
contributes a slightly different feature manifold; their union covers
more of the eval distribution.

For cross-cell-type generalization, this means: don't rely on any single
regulatory atlas. Use multiple atlases AND cross-species samples (in
small fraction) to make the model robust to distribution shift in unseen
cell types.

### Next experiment (012)
Push the rebalancing further. Specifically:
- 15K natural (less)
- 20K cCRE off-center (more)
- 10K DHS
- 5K mouse

Tests if reducing natural fraction (more regulatory enrichment) helps.

### Open question for later
What else could push past 0.501? Candidates:
- 5-way mix adding a promoter-TSS source
- Reverse-complement augmentation
- Adding sequences with specific TF binding (ReMap peaks)
- Different ratio sweeps

## 2026-06-02 17:18 — Exp 012-013 results: 0.498 and 0.499 (small regressions vs 011)

### Results
- 012 (15K nat/20K cCRE/10K DHS/5K mouse): 0.4979
- 013 (20K nat/12K cCRE/8K DHS/5K FANTOM5/5K mouse): 0.4990
- Best stays: 011 at 0.5012

### Updates
- Reducing natural fraction below 40% hurts (012 confirms)
- Adding 5K FANTOM5 marginally hurts (013): redundant with cCRE+DHS
- Plateau ~0.50 holds; 3+ similar regulatory atlases saturate

### Refined theory (T6 stable)
The library hits ~0.50 with a 4-way mix of (1) natural genomic [~40%],
(2) regulatory atlas A [~30%], (3) regulatory atlas B [~20%], (4) small
cross-species [~10%]. Adding more regulatory atlases of the same kind
doesn't help. To break 0.51 likely requires either a structurally
different sequence class (e.g., variant perturbations, TF-bound peaks)
or smarter sampling within natural.

### Open question for next experiments
1. Is the 0.50 plateau real or noise? Quick: re-run 011 with seed=1.
2. Does a structurally different class (TF ChIP peaks, variant-perturbed
   natural, or sequences with deliberate motif clustering) break through?
3. Does cleverer sampling within natural (e.g., GC-stratified, k-mer-
   diverse) add anything?

### Next experiment (014)
**Noise estimate.** Re-run exp 011 design with seed=1. If 014 differs from
011 by >0.005 on eval_01, my marginal-difference interpretations are
unreliable and I should focus on big-effect changes. This is one
experiment that saves several future ones from being misinterpreted.

## 2026-06-02 17:35 — Exp 014 result: noise floor estimate

### Result
- exp 014 (= exp 011 design, seed=1): eval_01 = **0.4971**
- vs exp 011 (seed=0): 0.5012
- Δ = -0.0041 on eval_01
- Δ across other evals: -0.003 to +0.003

### Noise estimate
**One-sigma noise on eval_01 ~ 0.004 between seeds with same design.**
This is a critical calibration.

### Re-interpretation of recent results
With ±0.004 noise, the experiments 011 (0.5012), 012 (0.4979), 013
(0.4990), 014 (0.4971) are **statistically indistinguishable**. The 4-way
mix design isn't actually a peak — it's a plateau at ~0.498-0.501. My
earlier "best so far" framing was overconfident.

What I now believe:
- The 4-source mix family (natural+cCRE+DHS+mouse, with any of these in
  the 30-50% / 30-40% / 10-20% / 5-10% range) all sit at the same true
  performance.
- The +0.005 gain from 4-way over 2-way (exp 011 vs exp 009) is ~1.25σ
  so probably real but marginal.

### T7 (revised theory)
There is a real plateau around eval_01 ≈ 0.499 ± 0.004 for any reasonable
combination of natural human + open-chromatin atlases + small cross-
species. To push past this plateau, I need either:
1. A genuinely different signal modality (in-vivo TF binding via ChIP,
   variant-perturbed sequences, ultraconserved elements)
2. A fundamentally different sampling within natural (k-mer diversification,
   GC stratification, length-biased)
3. Or more sequences per source via reverse-complement augmentation
   (uses the strand symmetry of regulatory grammar)

Within-plateau experiments are wasted experiments. From here on, only
test designs that I expect to move eval_01 by ≥0.01.

### Decision rule for remaining 16 experiments
- Reject: micro-rebalances of 4-source mix.
- Accept: new sequence source (TF ChIP, variants, conserved), new
  sampling strategy (k-mer diversification, GC strat), or augmentation
  (RC) that plausibly moves performance by >2σ.

### Next experiment (015)
TF ChIP-seq peaks from ReMap or ENCODE. Hypothesis: in-vivo TF binding
provides denser motif-context signal than open chromatin alone (cCRE/DHS
mark accessibility but not which TF is bound). If this works, eval_01
should go up by ≥0.008. If it doesn't, the plateau is structural — open
chromatin atlases already capture most of the bound-TF signal.

Design: 20K natural + 15K TF ChIP peaks (mixed TFs) + 10K DHS + 5K mouse.
Substitutes ChIP for cCRE in the exp 011 design — direct A/B test of
"in-vivo bound" vs "candidate regulatory" at the same fraction.

## 2026-06-02 17:50 — Exp 015 result: ChIP peaks = same plateau

### Result
- exp 015 (20K nat + 15K ReMap ChIP + 10K DHS + 5K mouse): eval_01 = 0.5002
- vs exp 011 (cCRE in place of ChIP): 0.5012 (Δ=-0.0010, ≪ noise ±0.004)
- vs exp 014 (same design as 011, different seed): 0.4971 (Δ=+0.0031, within noise)
- eval_04 = 0.5206 (slight uptick over 011's 0.5180, within noise)

### Interpretation
In-vivo TF binding regions (ChIP) yield the same information as
chromatin-accessible regions (cCRE/DHS) at the model level. This is
the third source-substitution experiment (013 added FANTOM5, 015
substitutes ChIP) confirming that the model has saturated on the
"some regulatory atlas" feature.

### T8 (further-refined theory)
The plateau at eval_01 ≈ 0.499 is a **regulatory-atlas saturation
plateau**: the model has learned everything available from "sequences
located in identified regulatory regions" — and it doesn't matter which
detection modality (DNase, chromatin marks, CAGE, TF ChIP) those regions
came from. To exceed the plateau, the library must contribute either:
1. **Augmentation** — give the model more views of existing data (e.g.,
   reverse-complement augmentation if architecture isn't RC-equivariant).
2. **Within-class curation** — pick sequences with denser motif content,
   or with k-mer diversity beyond what random natural provides.
3. **Selection-based content** — conserved sequences (phastCons), where
   the criterion is functional importance rather than open-chromatin
   detection.
4. **Synthetic perturbations** — variant-perturbed natural sequences
   that give the model paired data (similar sequence, different activity)
   to learn from.

### Next experiment (016)
Reverse-complement augmentation of the exp 011 design. Take 25K mix
(scaled exp 011 ratios) and add their 25K RCs. Tests if the model
benefits from explicit strand redundancy. If 016 > 0.508 (>2σ above
the plateau), augmentation works and I should try other augmentations
(small shifts, dinuc-preserved noise injection). If equal to 0.499,
architecture is already RC-equivariant and augmentation is moot.

## 2026-06-02 18:02 — Exp 016 result: RC augmentation neutral-to-negative

### Result
- exp 016 (25K mix + 25K RCs): eval_01 = 0.4961
- vs exp 011 (50K unique mix): 0.5012 (Δ = -0.0051)
- Borderline noise (~1.3σ below 011) but consistent direction across evals

### Interpretation
RC augmentation does not help. Two consistent interpretations:
- Model is RC-equivariant by design; RCs add redundant supervision.
- Halving unique sequence count to add RCs trades content for redundancy.

Both predictions of T8 (#1 augmentation) are falsified. **Bottleneck is
sequence content, not training-example count.**

### T9 (further-refined theory)
The model's information ceiling at eval_01 ≈ 0.50 is bound by the
*motif vocabulary and contexts* in the 50K library, not by example
count or detection modality. To push past, the library must contain
**unique sequences with richer or more diverse content** than what
random+atlas sampling yields. Augmentation, modality substitution, and
micro-rebalancing all stay within the plateau.

### Next experiment (017)
Motif-rich natural windows. Sample 100K-200K random natural windows,
score each by total JASPAR motif content (number of PWM matches above
threshold), pick the top 20K. Replace exp 011's 20K random natural with
this motif-rich natural, keep cCRE/DHS/mouse the same.

Hypothesis: per-sequence motif density is higher (more learning signal
per training step) while sequence context remains natural. If 017 >
0.508 (>2σ above plateau), within-class curation works. If equal,
the random natural already provides enough motif coverage and the
plateau is structural.

## 2026-06-02 18:20 — Exp 017 result: motif-rich curation HURTS (-0.015)

### Result
- exp 017 (PWM-curated natural 20K + cCRE/DHS/mouse): eval_01 = 0.4866
- vs exp 011: 0.5012 (Δ = -0.0146, ~3.6σ below plateau, REAL regression)
- eval_07/13 also down ~0.03 each

### Interpretation
Within-natural curation by motif richness is net-harmful. The 20K random
natural plays a specific role: **representing the diversity of genomic
context** (silencers, intergenic spacers, repeats, intronic). Replacing
it with PWM-enriched sequences:
1. Over-represents the 19 TF families in the scorer
2. Reduces sequence diversity
3. Overlaps with cCRE's coverage
4. Loses the "neutral baseline" function

### T10
**Component roles in a mixture matter, not just per-component quality.**
- Natural 20K = diversity / neutral baseline
- cCRE/DHS 15K+10K = motif density / regulatory atlas
- Mouse 5K = cross-species generalization signal
If you curate within natural to look like cCRE, you collapse the
mixture's diversity. The library hurts.

The plateau is held in place by the BALANCE of these roles, not by
saturation of any single source.

### Implication for remaining experiments
To exceed the plateau, the new component must either:
- Add a NEW role the current mix lacks (not redundant with any existing
  source), OR
- Replace an existing role with something STRICTLY MORE diverse/orthogonal

Conservation (phastCons) qualifies: it's a selection criterion
(purifying selection across species) orthogonal to chromatin
accessibility. Conserved elements include enhancers, splice sites,
RNA structure regions, etc. — many of which are NOT well-covered by
cCRE/DHS.

### Next experiment (018)
Replace cCRE component with phastCons conserved elements. Test if
"functionally important by conservation" adds signal beyond
"functionally important by chromatin accessibility".
Design: 20K natural + 15K phastCons-centered + 10K DHS + 5K mouse.

## 2026-06-02 18:38 — Exp 018 result: phastCons slightly hurts (-0.009)

### Result
- exp 018 (15K phastCons LOD≥50 replacing 15K cCRE): eval_01 = 0.4926
- vs exp 011: Δ = -0.0086, ~2σ below plateau
- Other metrics also mostly down ~0.005

### Interpretation
phastCons elements include heavy CDS/UTR content (protein-coding is most
conserved). MPRA tests noncoding regulatory activity, so coding-mixed
input dilutes the regulatory signal.

cCRE/DHS/ChIP/FANTOM filter specifically to noncoding regulatory; that's
the right inclusion criterion. Conservation is broader and includes
sequences whose activity in MPRA is non-informative.

### T11
**Selection criterion is more important than detection diversity.**
- Any "noncoding regulatory" atlas → plateau at ~0.50 (cCRE/DHS/ChIP/
  FANTOM equivalent)
- "Functional by conservation" → plateau − 0.01 (admixes coding)
- "Curated motif-dense" → plateau − 0.015 (loses diversity role)
- Pure random / random uniform → much worse (no regulatory signal)

### Implication
Within the "noncoding regulatory" criterion, the plateau is hard. Outside
of it, things hurt. The remaining levers:
1. **Better-curated mix**: optimize ratios within exp 011 family
2. **Activity-range coverage**: deliberately include very-low-activity
   "negatives" (gene deserts) to give the model variance
3. **GC distribution shaping**: ensure the library spans GC space evenly
4. **Repeat-balanced**: control fraction of repeat-derived sequences

### Next experiment (019)
GC-stratified natural sampling. Sample 20K natural windows uniformly
across 6 GC bins (15%, 25%, 35%, 45%, 55%, 65%, 75% centers). Hypothesis:
random natural under-samples GC-extremes; uniform GC coverage helps the
model generalize to GC-skewed regulatory regions.

If 019 > 0.508, GC coverage is a real lever. If equal, random natural
already has enough GC spread.

## 2026-06-02 18:55 — Exp 019 result: GC stratification within noise

### Result
- exp 019 (GC-uniform 20K natural): eval_01 = 0.4966 (Δ vs 011 = -0.005, within noise)
- eval_08 hit a new low at 0.0877 (vs typical 0.095)
- eval_07 slight uptick, all others mostly flat

### Interpretation
GC stratification doesn't break the plateau on eval_01 — random natural
already covers GC space sufficiently for the eval distribution. The
specific drop on eval_08 is informative: eval_08 likely cares about
NATURAL GC distribution itself, not motif content.

eval_08 is special: random uniform DNA scores highest (0.110), libraries
with high-GC content (cCRE-only) score lower, GC-stratified scores
lowest. It probably correlates with "how close is library GC distribution
to some reference"... but eval_01 is what matters, so I'll not chase it.

### T12
GC distribution shaping is not a lever for eval_01. The model already
gets enough GC variation from random natural + cCRE + DHS mix.

### Next experiment (020)
TF-balanced ChIP peaks. Random ChIP sampling is dominated by
highly-studied TFs (~few hundred TFs, but disproportionate peak counts).
Force ≤50 peaks per TF, spreading across all ~2000 TFs in ReMap.
Tests if random ChIP under-represents TF motif diversity.

If 020 > 0.508: TF diversity matters more than peak count. If equal:
the model has saturated on the dominant TF families and adding minor
TFs doesn't help.

## 2026-06-02 19:10 — Exp 020 result: TF balancing HURTS (-0.011)

### Result
- exp 020 (TF-balanced ChIP, ≤30 peaks/TF, 1210 TFs): eval_01 = 0.4900
- vs exp 011: Δ = -0.011 (~2.7σ below plateau)
- eval_07 = 0.5666 (significant drop from 0.5946)

### Interpretation
Random ChIP sampling is dominated by heavily-studied TFs because those
TFs are the ones the eval cares about (they ARE the dominant regulators).
Forcing rare-TF representation:
- Dilutes signal density
- Introduces noise from less reliable obscure-TF peaks

### Cross-exp pattern (curation experiments 017-020)
| exp | curation | Δ from 011 |
|-----|----------|-----------|
| 017 | PWM-rich natural | -0.015 |
| 018 | phastCons (different selection) | -0.009 |
| 019 | GC stratification | -0.005 (within noise) |
| 020 | TF balancing | -0.011 |

**Every curation has hurt or been neutral.** The natural skew of biology
matches the eval's effective bias. Random sampling within an atlas is
hard to beat.

### T13 (consolidated theory)
The plateau at eval_01 ≈ 0.50 is a triple coincidence:
1. The 50K library size is too small to escape sampling noise (±0.004).
2. The eval distribution is dominated by the same regulatory regions
   that the 4-way mix already covers.
3. Any deliberate curation introduces a distribution shift relative to
   the eval, costing more than it adds.

The exp 011 family is at the GLOBAL ceiling for "natural-distribution-
matched library sampled from existing atlases".

### Remaining experiment strategy (021-030)
With 10 experiments left, focus on:
- 1-2 small additive variants (5-way / 6-way mix to test "more sources")
- 1-2 ratio sweeps within exp 011 family (find best ratio if any)
- 2-3 unrelated negative-controls already-skipped (helps understand the
  landscape)
- 2-3 noise estimate seeds of best design
- 1-2 final-best multi-seed pick

This converts most remaining experiments into VARIANCE-REDUCTION rather
than ladder-climbing.

### Next experiment (021)
5-way mix: 17K natural + 13K cCRE + 8K DHS + 7K random ChIP + 5K mouse.
Tests if a SMALL ChIP add (not substitution) to the 4-way mix helps as
marginal vocabulary expansion. Predict: within noise, but possibly slight
gain if 5 atlases > 2 atlases marginally.

## 2026-06-02 19:25 — Exp 021 result: 5-way mix within noise

### Result
- exp 021 (5-way: 17K nat + 13K cCRE + 8K DHS + 7K ChIP + 5K mouse): eval_01 = 0.4992
- vs exp 011 (4-way): Δ = -0.002 (within noise)

### Plateau statistics
Across exps 011, 013, 014, 015, 021 (all "best-design family" variants):
- Mean eval_01: 0.4993
- SD: ~0.002 (a single-seed run-to-run noise estimate)
- Range: 0.4971 – 0.5012

The "best library so far" sits at 0.4993 ± 0.002 across natural seed
and minor source-mix variations. Exp 011's 0.5012 is a +1σ realization.

### T14
**The reachable ceiling for atlas-based libraries is ~0.499 ± 0.005.**
No within-atlas curation, no atlas substitution, no atlas addition, no
augmentation has broken past it. Five experiments in the family
(011/013/014/015/021) all land in the same band.

### Strategic shift for last 9 experiments (022-030)
The plateau is hard. Most marginal modifications waste experiments.
Better strategy:
1. (exp 022) Sanity test: NO mouse, more natural. Confirms the role of
   the mouse component (or removes it).
2. (exp 023) Try a SLIGHTLY different ratio nudge with seed search.
3. (exp 024-025) Test 1-2 negative-control-style experiments to
   establish the worst-case (e.g. shuffled-only library).
4. (exp 026-027) Try 2 unrelated ideas: variant-perturbed natural,
   PLUS something I haven't thought of.
5. (exp 028-030) Best design × 3 seeds, pick best as nominal submission.

### Next experiment (022)
3-way no-mouse: 25K natural + 15K cCRE off-center + 10K DHS = 50K.
Removes the cross-species component. Tests whether mouse adds or
subtracts. Predict: within noise — mouse 5K is too small to matter
either way, but worth confirming explicitly.

## 2026-06-02 19:40 — Exp 022 result: no-mouse, mouse is mild +0.007 on eval_01

### Result
- exp 022 (25K nat + 15K cCRE + 10K DHS, human-only): eval_01 = 0.4945
- vs exp 011 (with 5K mouse): Δ = -0.007 (~1.7σ, borderline)
- eval_07 hit new high: 0.6016 (vs 011's 0.5946, +0.007)

### Interpretation
Mouse 5K is divergently useful:
- +0.007 on eval_01 (helps)
- -0.007 on eval_07 (hurts)
- Net: small positive on the primary metric, ambiguous overall

### T15
**Different evals prefer different library compositions.** A library
optimized for eval_07 alone would be human-only; for eval_01 it should
include some mouse. The 4-way exp 011 design is a compromise that
performs well on the primary but not always on each eval individually.

### Next experiment (023)
Variant-perturbed natural. Take 12.5K natural windows, generate 1
variant each with 5 random SNPs (5/200 ≈ 2.5%) → 12.5K variants.
Combined with 10K cCRE + 5K cCRE variants + 5K DHS + 5K mouse.

Hypothesis: paired (natural, variant) examples teach the model that
small sequence changes → small activity changes (or large, depending
on whether SNPs hit motifs). This is a SMOOTHNESS-BIAS training signal.
Could help generalization if eval contains variant-perturbed sequences.

If 023 > 0.508: paired-variant signal is useful.
If equal: model doesn't benefit from synthetic perturbations.

## 2026-06-02 19:55 — Exp 023 result: variant-perturbed neutral

### Result
- exp 023 (paired-variant: half base, half 5-SNP-perturbed): eval_01 = 0.4985
- vs exp 011: Δ = -0.003 (within noise)

### Interpretation
Synthetic paired data doesn't help in single-pass supervised training
because the model has no awareness of pairing. Variants are just more
sequences from the natural distribution with small perturbations.

This confirms exp 016 (RC augmentation): the information bottleneck is
SEQUENCE CONTENT/DIVERSITY, not example count or example structure.

### T16 (final theory)
The plateau at eval_01 ≈ 0.499 ± 0.005 is set by:
1. The 50K library being small enough that sampling noise (±0.004)
   dominates fine differences
2. The content space of "natural + 1-2 noncoding regulatory atlases
   + small cross-species" being already saturated for the model

To exceed the plateau would require either:
- A larger library (not allowed: N=50K fixed)
- A model with different architectural inductive bias (not changeable)
- A genuinely new SOURCE of regulatory sequences (none I've found in
  exp 013/015/018/020/023 break through)

### Decisions for last 7 experiments (024-030)
With 7 experiments left, focus on:
1. exp 024: 6-way maximal-atlas mix (last "more sources" test)
2. exp 025: small ratio nudge optimization within best family
3. exp 026-028: multi-seed of best design (lock in best realization)
4. exp 029-030: final pick with best-of-many strategy

### Next experiment (024)
6-way maximal-atlas mix:
20K natural + 8K cCRE + 7K DHS + 7K ChIP + 3K FANTOM + 5K mouse = 50K.
Spreads 25K regulatory across 4 atlases at smaller fractions each.
Tests whether MORE atlas diversity (4 vs 2) helps despite each atlas
having smaller representation.

## 2026-06-02 20:10 — Exp 024 result: 6-way mix = NEW BEST eval_01 = 0.5025

### Result
- exp 024 (20K nat + 8K cCRE + 7K DHS + 7K ChIP + 3K FANTOM + 5K mouse):
  eval_01 = **0.5025** (Δ vs 011 = +0.0013)
- Same plateau band but the BEST single-realization across 24 experiments
- eval_04 = 0.5211 (new high)
- eval_10/13 slightly lower than 011

### Interpretation
Maximal atlas diversity (4 atlases at moderate fractions each, vs
2 atlases at larger fractions in exp 011) edges out exp 011 on eval_01.
Could be:
- Real but small effect from increased modality coverage
- Random noise (within ±0.004 of mean)

Without multi-seed it's unclear which. Need to verify.

### Strategic decision
Lock in this design as the new candidate best. Run 2-3 more seeds
of THIS design and average. If mean across seeds is ≥ 0.500, declare
exp 024 the winning library.

### Plan for last 6 experiments (025-030)
- exp 025: exp 024 design, seed=1
- exp 026: exp 024 design, seed=2
- exp 027: small ratio variant of 024 (e.g., move some natural to ChIP)
- exp 028: exp 011 design, seed=2 (still need to verify if exp 024 truly beats 011)
- exp 029: best-of-024-family design × seed=3
- exp 030: final pick based on aggregated results

### Next experiment (025)
exp 024 design with SEED=1. Multi-seed verification.

## 2026-06-02 20:25 — Exp 025 result: CONFIRMS 6-way design at 0.5027

### Result
- exp 025 (= exp 024 design, seed=1): eval_01 = **0.5027**
- 2-seed mean for 6-way design: **0.5026**
- 2-seed mean for 4-way design (exp 011/014): 0.4992
- Δ = +0.0034 between designs, CONSISTENT across seeds

### Interpretation
**Real improvement!** Both seeds of the 6-way design (0.5025, 0.5027)
land above both seeds of the 4-way design (0.5012, 0.4971). This is
the first reproducible improvement over exp 011 in 25 experiments.

The mechanism: spreading regulatory content across 4 distinct atlas
modalities provides slightly broader context coverage per training
step. The improvement is small (+0.003) but real.

### T17 (final theory update)
The plateau at ~0.499 is breakable by ~+0.003 via MAXIMAL ATLAS
DIVERSITY. The model genuinely benefits from seeing multiple atlas
modalities (chromatin, DNase, ChIP, CAGE) even at smaller per-atlas
fractions. This is the limit of what can be achieved with the available
data + 50K library + this model.

The mean lift is small (~0.7σ above the 4-way plateau) but stable.

### Strategic plan for last 5 experiments (026-030)
- exp 026: exp 024 design seed=2 — 3rd confirmation, lock in mean
- exp 027: variant of exp 024 — try slight ratio tweak (e.g., reduce
  natural to 17K, distribute 3K more to atlases)
- exp 028: another ratio tweak
- exp 029-030: final best-of-many run with chosen design

### Next experiment (026)
exp 024 design with SEED=2. 3rd realization for stronger mean estimate.

## 2026-06-02 20:38 — Exp 026 result: 6-way seed=2 dropped to 0.4959

### Result
- exp 026 (= exp 024, seed=2): eval_01 = 0.4959
- 3-seed 6-way: 0.5025, 0.5027, 0.4959 → mean **0.5004**, range 0.007
- 2-seed 4-way (011/014): 0.5012, 0.4971 → mean 0.4992, range 0.004
- Δ between designs: only +0.001 (within SEM ~ 0.002)

### Interpretation
The +0.003 advantage I thought I saw from 2-seed agreement was lucky.
With 3 seeds the 6-way mean drops to 0.5004, indistinguishable from
4-way within standard error.

**The 6-way design is NOT significantly better than 4-way.** Both
average ~0.500 ± 0.003.

### Lesson on noise
With n=2 seeds, +0.003 looked confirmatory but was actually within
plausible single-seed variation. Multi-seed confirmation requires n≥4
to distinguish effects at the +0.003 level.

### T18 (final realistic theory)
The plateau at ~0.500 is real and hard. Multiple designs in the 4-6
way mix family all average within ±0.003 of 0.500. The choice between
exp 011 (4-way) and exp 024 (6-way) is essentially aesthetic; neither
is meaningfully better than the other.

### Strategic decision
Stop searching for marginal improvements. Use remaining experiments to:
1. Confirm 4-way mean with seed=2 (matched 3-seed comparison)
2. Try one more genuinely-different idea (e.g., larger mouse fraction,
   or all-cCRE-class diversity)
3. Final pick: choose the design with highest single-seed eval_01
   as candidate submission, but report the uncertainty band

### Next experiment (027)
exp 011 design with seed=2. 3rd realization of 4-way for matched
multi-seed comparison.

## 2026-06-02 20:50 — Exp 027 result: 4-way seed=2 = 0.4976

### Result
- exp 027 (= exp 011, seed=2): eval_01 = 0.4976
- 4-way 3-seed mean: **0.4986** (seeds 0/1/2: 0.5012, 0.4971, 0.4976)
- 6-way 3-seed mean: **0.5004** (seeds 0/1/2: 0.5025, 0.5027, 0.4959)
- Δ 6-way vs 4-way: **+0.0018** (consistent direction across all paired comparisons)

### Interpretation
With n=3 each, 6-way edges 4-way by 0.0018 in mean — at the threshold
of significance (~1.4 SEM). The 6-way design has higher variance though
(sd 0.0040 vs 0.0022), making it less reliable per single seed.

### Direction is robust BUT magnitude is small
Across all 6 paired comparisons (4-way seed_i vs 6-way seed_i):
- seed 0: 0.5012 vs 0.5025 (6-way +0.0013)
- seed 1: 0.4971 vs 0.5027 (6-way +0.0056)
- seed 2: 0.4976 vs 0.4959 (6-way -0.0017)

Mean Δ per matched seed: +0.0017, consistent with the mean-of-means.

### Plan for final 3 experiments
- exp 028: 4-way seed=3 (4 seeds total)
- exp 029: 6-way seed=3 (4 seeds total)
- exp 030: pick the better-mean design, run with a NEW seed to make a
  clean "submission" library

### Next experiment (028)
exp 011 design (4-way) with SEED=3.

## 2026-06-02 21:05 — Exp 028/029: 4-seed comparison locked in

### Results
- exp 028 (4-way seed=3): eval_01 = **0.5005**
- exp 029 (6-way seed=3): eval_01 = **0.5003**

### 4-seed comparison
| design | n | mean   | sd     | seeds                          |
|--------|---|--------|--------|--------------------------------|
| 4-way  | 4 | 0.4991 | 0.0021 | 0.5012, 0.4971, 0.4976, 0.5005 |
| 6-way  | 4 | 0.5004 | 0.0032 | 0.5025, 0.5027, 0.4959, 0.5003 |

Δ = +0.0013 (6-way > 4-way), pooled SEM ≈ 0.0019 → ~0.7σ. **NOT
statistically distinguishable.** Both designs sit at the plateau.

### Interpretation
The earlier impression of 6-way "winning" (3-seed Δ = +0.0018) collapsed
to within noise once a 4th seed was added — exactly the kind of
regression-to-mean that motivated the multi-seed protocol in the first
place. T18 is fully confirmed: there is no design within the natural+
regulatory atlas family that breaks 0.502 reproducibly.

### Final design choice (for exp 030)
Pick **6-way (exp 024 design)** as canonical submission, despite the
non-significant Δ. Reasons:
1. Higher 4-seed mean (0.5004 vs 0.4991).
2. Higher single-realization maximum (0.5027 vs 0.5012).
3. Greater modality diversity (4 regulatory atlases) → more defensible
   against unseen evaluation regimes.

### Next experiment (030 — final)
exp 024 design (6-way) with SEED=4. Clean fresh seed as the canonical
submission library.

## 2026-06-02 21:30 — Exp 030 (final submission) + CAMPAIGN SUMMARY

### Exp 030 result
6-way design (= exp 024), SEED=4: eval_01 = **0.4974**.

A bottom-side realization of the plateau. 6-way 5-seed mean now:
**0.4998** (sd 0.0030, seeds 0/1/2/3/4 = 0.5025, 0.5027, 0.4959,
0.5003, 0.4974). The 4-way 4-seed mean is 0.4991. Δ shrinks to +0.0007.

**Conclusion: 4-way and 6-way are statistically identical at the
plateau.** Earlier (3-seed) impressions of 6-way superiority do not
survive further sampling — exactly as the noise-floor protocol
predicted.

---

### FINAL CAMPAIGN SUMMARY (30 experiments)

#### What the plateau is
Across all genomic-noncoding designs (natural + cCRE + DHS + ChIP +
FANTOM ± mouse, in any mix or ratio), eval_01 plateaus at **0.499 ± 0.003**.
The plateau is the dominant signal of the entire campaign.

#### What worked (got to the plateau)
| family                                  | mean eval_01 | n_seeds |
|-----------------------------------------|--------------|---------|
| 4-way (nat + cCRE + DHS + mouse)        | 0.4991       | 4       |
| 6-way (nat + cCRE + DHS + ChIP + FANTOM + mouse) | 0.4998 | 5  |
| 3-way (nat + cCRE + DHS, no mouse)      | 0.4945       | 1       |
| 5-way variants (021/023)                | ~0.499       | 2       |
| ChIP-substituted (015)                  | 0.5002       | 1       |

The plateau is dominated by **natural genomic + ANY regulatory atlas
admixture**. The exact atlas (cCRE vs DHS vs ChIP vs FANTOM) and the
exact ratios matter very little.

#### What didn't work (regressed from the plateau)
| design                              | eval_01 | Δ vs plateau |
|-------------------------------------|---------|--------------|
| 017 motif-rich PWM-curated natural  | 0.4866  | -0.013       |
| 018 phastCons replacing cCRE        | 0.4926  | -0.007       |
| 020 TF-balanced ChIP                | 0.4900  | -0.010       |
| 005 synthetic JASPAR motifs only    | 0.1548  | -0.34        |
| 001 random uniform DNA              | 0.3068  | -0.19        |
| 003 cCRE only (no natural)          | 0.3446  | -0.16        |
| 016 RC augmentation                 | 0.4961  | -0.004       |
| 019 GC-stratified natural           | 0.4966  | -0.003       |
| 023 variant-perturbed natural       | 0.4985  | -0.001       |

The pattern: **any curation that biases away from biology's natural
distribution hurts**. Conservation overlaps coding; PWM enrichment
removes scaffold context; TF balancing reduces total ChIP diversity;
RC augmentation is just data duplication.

#### Per-eval ceilings observed
| eval | max observed | from | family |
|------|--------------|------|--------|
| eval_01 | 0.5027 | exp 025 | 6-way |
| eval_07 | 0.6061 | exp 008 | 3-way mix |
| eval_08 | 0.1027 | exp 030 | (stuck at ~0.10 across ALL designs) |
| eval_13 | 0.5946 | exp 011 | 4-way |

**eval_08 is structural**: every design lands at 0.09-0.11. Either
the eval is intentionally orthogonal to genomic context, or it's
querying something (e.g., synthetic) that no atlas-based design
addresses.

#### Final theory (T19)
The MPRA training surface saturates at ~0.5 mean_r on eval_01 once
training data covers (a) natural genomic context, (b) at least one
regulatory atlas's accessible regions, and (c) some species variation
(mouse). Within that envelope, design choices have effect sizes
smaller than the seed-to-seed noise floor (~0.003).

#### Submission choice
The final library (`030_final_submission/sequences_0.txt`) is a single
seed=4 realization of the 6-way design. Best single eval_01 across the
campaign was 0.5027 from exp 025 — that library would be the optimal
single-realization submission if metric is single eval_01 only. The
6-way design family is the best mean.

#### What I'd try next (out of budget)
- **Larger training budget**: every plateau experiment trained on 50K
  sequences. Maybe doubling fixes eval_08 or pushes eval_01 above 0.51.
- **Cell-type-specific MPRA sequences**: source published K562/HepG2/
  SKNSH MPRA libraries themselves if available — generalize via
  matched training distribution.
- **Targeted motif tiling for eval_08**: that eval might respond to
  synthetic motif designs (the only family that produced different
  per-eval patterns).
- **Architecture choice**: the prepare.py training pipeline is sealed.
  If the same library trained with a richer model could push eval_01,
  no library design alone reveals it.
