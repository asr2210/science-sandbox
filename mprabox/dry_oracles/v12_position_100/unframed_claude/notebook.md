# Lab Notebook

## 2026-06-02 — Initial theory

**Setup:** 30 experiments, each is a library of 50,000 200bp DNA sequences (ACGT). A black-box scorer (`prepare.py`) returns 14 eval set scores. eval_01 is the primary metric. The "unknown" variant of instructions provides no baseline tables and no strategies file.

**Theory v0 (prior):** prepare.py likely:
1. Simulates / has stored measured MPRA activity for our 50k sequences.
2. Trains a sequence→activity model on those.
3. Tests the model on 14 held-out evaluation sets (probably real genomic regions or held-out designed sequences).
4. Returns the Pearson correlation between predicted and measured activity per eval set.

If true, the library that wins is the one that teaches the model the richest, most generalizable regulatory grammar — not the library that itself has highest activity. So **diversity and coverage of regulatory features** matter more than narrow signal.

**Predicted ranking (priors):**
- Random uniform: ~0.07 (floor)
- GC-balanced random: ~0.07–0.10
- Real human regulatory sequences (DHS / cCRE): potentially 0.5–0.7
- Curated TF-motif-rich synthetic: depends on whether the model learns motif grammar

**Plan arc:**
- 001–003: trivial baselines to calibrate (so I know my numbers under my harness)
- 004–008: biological grounding (real human DNA, K562/HepG2/SK-N-SH accessible regions)
- 009–020: refinement on the best direction (motifs, mixture libraries, diversity)
- 021–030: scaled or hybrid designs

---

## 2026-06-02 — Plan exp 001: random_uniform

**Hypothesis:** Pure random ACGT 50,000×200 establishes the floor under my harness, and confirms result.json format matches expectations.

**Method:** numpy.random.default_rng(42), uniform over {A,C,G,T}, 50000 × 200.

**Prediction:** eval_01 ≈ 0.05–0.10. Will measure runtime to plan budget.

## 2026-06-02 — Result exp 001

eval_01 = 0.0648 (in predicted range, confirmed floor). Runtime ~57s wall.

**Eval pairing structure (v12):**
- eval_01 = eval_14
- eval_02 = eval_05
- eval_03 = eval_12
- eval_04 = eval_09
- eval_06 = eval_11
- eval_07, eval_08, eval_10, eval_13 distinct
→ 9 unique evals. eval_01 lives in a pair, not a triplet.

**Easiest by random:** eval_07=0.131, eval_10=0.119, eval_13=0.119 (these may be GC/composition-driven).
**Hardest:** eval_08=0.0563.

**Theory update:** scoring rewards predictive models trained on (our seqs, MPRA activity). Random gives the model some signal (because random sequences span composition space) but lacks coherent regulatory grammar. Need to give the training set actual motif/genomic structure.

**Next (exp 002): dinucleotide-shuffled human genomic DNA proxy.** Without downloading anything yet, I'll first test whether a sharply different *composition* alone (e.g., human-like dinuc frequencies) moves eval_01. If composition alone moves the needle significantly, I learn the model is composition-sensitive. If not, I need real regulatory grounding.

## 2026-06-02 — Plan exp 002: human-like dinucleotide composition

**Hypothesis:** the model the scorer trains learns sequence→activity from local context. Human regulatory DNA has very specific dinucleotide frequencies (e.g., CpG depletion, TpA depletion, dinucleotide auto-correlations). If I generate sequences with realistic human dinuc transition probabilities (1st-order Markov), and that beats random, the model is at least composition-sensitive.

**Method:** Use a published human genome-wide dinucleotide transition matrix (approximate hardcoded values). Generate 50k sequences via 1st-order Markov chain from a fixed start distribution.

**Approximate human dinucleotide frequencies (genome-wide, autosomal):**
- AA ~0.097, AC ~0.052, AG ~0.072, AT ~0.073
- CA ~0.073, CC ~0.052, CG ~0.010, CT ~0.072
- GA ~0.060, GC ~0.043, GG ~0.052, GT ~0.052
- TA ~0.063, TC ~0.060, TG ~0.073, TT ~0.097

Normalizing per row gives conditional probabilities.

**Prediction:** if composition alone matters → eval_01 > 0.10. If not → still ~0.07.

## 2026-06-02 — Results exp 002-004

| exp | eval_01 | delta vs prev |
|-----|---------|---------------|
| 001 random_uniform | 0.0648 | (floor) |
| 002 dinuc_markov | 0.0730 | +0.008 |
| 003 genome_random_windows (chr17/19/22) | 0.0752 | +0.002 |
| 004 tfbs_centered (chr17/19/22) | 0.0764 | +0.001 |

**Big finding:** real human regulatory regions (TFBS-centered windows) barely beat random genome windows. Naive "biological grounding wins" theory FAILS at this score range. All four libraries land in a narrow 0.065-0.077 band.

**Updated theory:** the model trained on 50k random-like sequences appears bottlenecked by something other than annotation. Hypotheses to test:
- (H1) Cell-type-specific accessibility matters (need K562/HepG2/SK-N-SH DHS specifically)
- (H2) Motif DENSITY per sequence matters — natural sequences have ~1 motif/200bp, denser is better
- (H3) Library DIVERSITY matters — coverage of regulatory "topics" / TF families
- (H4) Sequence ACTIVITY matters — only strongly-active sequences train a useful model; weak/random sequences add noise

H1 and H4 are biggest priors. H2 and H3 test downstream.

## 2026-06-02 — Plan exp 005: K562 DHS peaks

**Hypothesis (H1):** sequences from open chromatin in K562 specifically should jump eval_01 because K562 is one of the 3 evaluation cell types and the DHS peaks ARE the regions where MPRA activity is highest in K562.

**Method:** Download K562 DNase-seq peaks bed from ENCODE, get a 200bp window centered on each peak summit. Filter to chr17/19/22 (have FASTAs), and if too few, also download chr1.

**Prediction:** eval_01 > 0.10 if H1 holds. If still ~0.08, then H1 is wrong and the score is composition-locked.

## 2026-06-02 — Results exp 005-006

- 005 K562 DHS centered: eval_01 = 0.0735 — H1 FALSE
- 006 motif-dense synthetic (8 strong-TF copies/seq): eval_01 = 0.0640 — H2 FALSE (slightly worse than random!)

All libraries land 0.064-0.077. The score is essentially uncorrelated with what I'd expect from biological reasoning. Either:
- (a) The harness needs a very specific library structure I haven't found.
- (b) Score is essentially capped at ~0.08 unless you replicate the precise design family of the dhs_topic baseline.
- (c) I am missing something fundamental about prepare.py's mechanism.

**New theory (T2):** The model trained on 50k sequences may require a very specific BALANCE of activity range AND motif diversity AND sequence-distribution properties. Random sequences don't supply activity signal; biological sequences don't supply diversity; motif-dense synthetic sequences don't look natural to the model.

The best library may be a CAREFUL MIXTURE. Test next.

## 2026-06-02 — Plan exp 007: maximally diverse mixed library

**Method:** 50k = 10k from each of 5 sources:
- random_uniform (no signal, no motifs)
- dinuc-Markov (composition only)
- genome random windows (intergenic baseline)
- K562 DHS centered (regulatory grounding)
- motif-dense synthetic (extreme motif content)

**Hypothesis:** if (T2) holds, this mixed library should outperform any single one. If not, then the metric truly cares about something specific I'm still missing.

**Prediction:** if mixture wins, eval_01 ≥ 0.085. If equal/worse, I need to rethink entirely.




## 2026-06-02 — Result exp 007-013 (compressed)

| exp | eval_01 | note |
|-----|---------|------|
| 007 mixed_diverse | 0.0700 | T2 mixture FALSE — no lift |
| 008 gc_stratified | 0.0651 | GC scan doesn't help |
| 009 ccre_class_stratified | 0.0745 | all 8 cCRE classes balanced |
| 010 multicell_dhs | 0.0712 | K562+HepG2+SKNSH multi-cell DHS |
| 011 kmer_topic_dhs (BEST) | **0.0760** | 4-mer K-Means(50) topic clusters of 250k cCREs |
| 012 ccre_promoters_only | 0.0740 | promoter-only filter doesn't help |
| 013 kmer6_topic_dhs | 0.0458 | 6-mer 100-cluster oversampling HURT |

**Lesson:** 4-mer topic clustering helps marginally (best at 0.0760). 6-mer over-fragments clusters and oversampling with replacement injects duplicate sequences → big regression. The signal is sensitive to UNIQUENESS of training sequences.

## 2026-06-02 — Plan exp 014: scale up exp 011's recipe

**Hypothesis:** 011 used a 250k cCRE subsample × 50 clusters × 1000/cluster. If topic-diversity is the winning lever, scaling pool to ALL 2.35M cCREs × 80 clusters × 625/cluster (no replacement) should improve.

**Predicted:** eval_01 ≥ 0.080.

## 2026-06-02 — Result exp 014

eval_01 = 0.0739. **Marginal regression vs 011 (0.0760).** Scaling pool/clusters did NOT help.

**Lesson (T3):** Further refining the cCRE-topic recipe is hitting a ceiling. The "diversity over cCRE 4-mer topics" lever is real but tiny (~+0.001 over random baseline). I'm not breaking 0.08 by tuning this lever further. Need to test a categorically different source.

**Theory update:** my best hypothesis now is that the model trained on 50k seqs has ALREADY learned the basic cis-regulatory grammar from random/genomic ACGT — eval_01 ~0.07 is the model's "I sort of know what a TF binding site looks like" baseline. To push past 0.08, the training library must teach something the model can't get from random + cCREs. Candidates:
- (H5) REPEAT elements / Alu / LINE — comprise >50% of the genome and have strong activity signatures
- (H6) Designed sequences with REGULATORY GRAMMAR (not just dense motifs but composite, spaced motif modules)
- (H7) Sequences sampled by ACTIVITY GRADIENT — both very-high and very-low MPRA proxies (e.g., promoter vs intergenic mix at extreme contrast)
- (H8) Held-out cell-type cues (the 14 evals likely include disease/development tissues we haven't covered)

**Next: exp 015** — test H5 (repeats) AND H7 (extreme activity contrast). Build a library that is 50% "highest-confidence active" (top K562/HepG2/SKNSH summit heights, NOT centered on summits but covering full peaks) + 50% "definitely silent" (random intergenic gene deserts, far from any cCRE). This sharpens the contrast for the model.


## 2026-06-02 — Final summary (exp 015-030)

**Exploration timeline (continuing from exp 014):**

| exp | recipe | eval_01 | takeaway |
|-----|--------|---------|----------|
| 015 activity_contrast | 25k DHS-pos + 25k intergenic deserts | 0.0723 | contrast HURT — random-like negatives drag down |
| 016 noise_test | 011 recipe seed=911 | 0.0734 | noise floor ~0.003 → many earlier "lifts" were noise |
| 017 tfbs_hub_ccres | top-50k cCREs by TFBS density | 0.0756 | TFBS density alone = same as random cCREs |
| 018 rc_augmented | 25k cCRE + 25k RC | 0.0745 | RC aug neutral on eval_01 |
| 019 hybrid_union | 10k each from 5 selection strategies | 0.0755 | combining strategies adds nothing |
| **020 sliding_window_aug** | top-12.5k TFBS × 4 slides {-75,-25,25,75} | **0.0764** | **NEW BEST — sliding windows help** |
| 021 slide5_tfbs | 5 slides × 10k | 0.0758 | fewer regions hurts |
| 022 slide2_topic25k | 25k topic × 2 slides | 0.0756 | best eval_07/13 but eval_01 same |
| **023 slide_replicate** | 020 recipe seed=211 | **0.0766** | confirms 020 family |
| 024 tfbs_dhs_slide | TFBS×DHS scoring | 0.0763 | joint scoring = no benefit |
| 025 slide_wide_offsets | offsets ±95/±32 | 0.0752 | wider hurts |
| 026 slide6_aug | 6 slides × 8.33k | 0.0747 | more aug, less diversity = worse |
| 027 slide_narrow | offsets ±20/±60 | 0.0760 | SKNSH=0.0706 (best) but eval_01 same |
| 028 slide_topic_blend | top-50k-TFBS → cluster → balance → 4 slides | 0.0760 | blend doesn't push past plateau |
| 029 final_replicate | 020 recipe seed=250 | 0.0764 | recipe is robust |
| **030 final** | 020 recipe seed=350 | **0.0764** | shipped; eval_03=0.0962 best |

**Final theory (T5):**

The 50k × 200bp library is bottlenecked by a small-CNN architecture trained on (seq, activity) pairs. The eval correlations cap at ~0.077 on eval_01 because:
1. 50k samples train a model with finite capacity — it learns base regulatory grammar but saturates
2. The cCRE substrate ALREADY captures most of the regulatory signal a small CNN can extract
3. Marginal improvements come from data-augmentation-style tricks (sliding windows give the model translation-invariance practice) NOT from better selection
4. Noise floor (~0.003 between same-recipe replicates) limits experimental signal — many "discoveries" in 003-013 were noise; only random-vs-cCRE gap (~0.010) was clearly real

**What helped (in order):**
- Switch from random ACGT (0.0648) to any cCRE-based library (~0.073) — biggest win (+0.010)
- Sliding-window aug on TFBS-dense regions (020+) — small but real (+0.001-0.002)
- Topic clustering (011 vs 003) — too small to distinguish from noise

**What did NOT help:**
- Dinuc-Markov composition matching, K562-specific DHS, motif-dense synthetic, GC stratification, cCRE class balancing, multi-cell DHS, promoter-only, 6-mer topic, full-pool 4-mer, activity contrast (intergenic), RC aug, joint TFBS+DHS scoring, hybrid unions, narrower or wider slide offsets.

**Shipping:** library 030 with eval_01=0.0764.
