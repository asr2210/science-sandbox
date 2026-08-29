# Lab Notebook

## 2026-06-03 17:05 — Setup & initial theory

**Context**: I'm given a black-box scoring function for 50,000 DNA sequences
(200bp each). Eval set names mention `k562_r`, `hepg2_r`, `sknsh_r` — these
are K562, HepG2, and SK-N-SH cell lines. Strong prior: this is an MPRA-style
(Massively Parallel Reporter Assay) regulatory activity scorer. There are 14
eval sets, eval_01 is primary metric. I have 30 experiments.

**Initial theory (v0)**: The scoring function rewards sequences that drive
transcriptional activity in cell-line-like contexts. Likely rewards:
- Transcription factor binding site (TFBS) content
- Specific cell-line-relevant motifs
- Possibly GC content / CpG islands
- Possibly avoidance of repressive elements

**Caveats**: It could also be a model trained on MPRA data — in which case
it rewards sequences that "look like" high-activity enhancers to the model,
which may have learned shortcuts that don't fully reflect biology.

**Plan for first experiments**:
1. Exp 001: Uniform random sequences (25% each base) — baseline
2. Exp 002: Sweep GC content if baseline is informative
3. Exp 003+: Add known motifs

I will hold off on heavy motif design until I have a baseline number. The
metric is mean_r — likely a correlation. So scores can be negative (anti-
correlation), 0 (random), or positive.

## 2026-06-03 17:08 — Planning Exp 001 baseline

Uniform random 200bp sequences. No structure. Predict mean_r near 0 across
all evals. This tells me: (a) range of scores, (b) whether random has any
direction, (c) any obvious bias in any single eval.

## 2026-06-03 17:25 — Exp 002 result & theory update

Exp 002 (3 motifs per seq) gave only +0.003 mean_r over random. Small.
Possible reasons:
- The metric is a *correlation across the library*, so what matters
  may be DIVERSITY, not absolute motif content
- Random 200bp already has many short motifs by chance
- The model may not weight my chosen motifs heavily

**Theory v1**: The score is `r` (Pearson?) between two quantities computed
across the 50k sequences (likely model-predicted activity vs target/ground
truth). To raise `r`:
- Provide LARGE DYNAMIC RANGE in predicted activity (so both axes have
  high variance)
- Make sequences the model is CONFIDENT about (less noise)
- Avoid making the library too HOMOGENEOUS (which crushes variance)

This predicts: extreme homogeneous libraries (homopolymers) will tank r
because variance collapses. Diverse libraries with strong cell-type-
specific signals should boost r.

## 2026-06-03 17:28 — Planning Exp 003

Try a CpG-island-like library: GC=70%, CG dinucleotide enriched. This
captures the "promoter" prior. Will tell me if composition (not motif
content) is the dominant lever.

## 2026-06-03 17:55 — Exp 005 & 006 results, theory update v2

Exp 005 (6 dense motifs/seq): eval_01=0.4101 (-0.010 vs random). HURT.
Exp 006 (real human genomic windows): eval_01=0.3975 (-0.023 mean)
  but K562=0.54 (-0.04), HepG2=0.55 (-0.07), SKNSH=0.099 (+0.04 !!)

**The cell types want DIFFERENT compositions.**

K562 (myeloid) and HepG2 (liver) prefer random ~50% GC libraries.
SKNSH (neuron) strongly prefers natural human DNA composition.

**Theory v2**: The black-box scorer correlates predicted activity with
ground truth across 50k sequences. The model has different biases per
cell type:
- K562/HepG2 model heads were trained on data where ~50% GC random-like
  sequences are well-distributed in predicted activity → random gives
  high correlation
- SKNSH head needs natural sequence features (AT-rich, homeobox-like,
  CpG-depleted) to generate diverse predicted activities → natural DNA
  triples its r vs random

The aggregate mean_r weighs all three equally. A mixed library that
gives each cell-type-head what it likes could lift mean_r above either
pure baseline.

## 2026-06-03 17:58 — Planning Exp 007 (mixed library)

Half random + half natural. Predicts: K562 ~midway 0.56, HepG2 ~midway
0.58, SKNSH ~midway 0.08 → mean ~0.41 IF correlation is linear in
composition mixture. But if the metric rewards dynamic range, the
mixture might be HIGHER than either component.

## 2026-06-03 18:50 — Major theory update after 11 experiments

| # | Lib | eval_01 | K562 | HepG2 | SKNSH |
|---|-----|---------|------|-------|-------|
| 001 | random seed=0 | 0.4203 | 0.585 | 0.618 | 0.059 |
| 002 | random+3 broad motifs | 0.4232 | 0.594 | 0.624 | 0.052 |
| 003 | GC=70% | 0.3567 | 0.505 | 0.523 | 0.042 |
| 004 | GC=30% | 0.3692 | 0.510 | 0.536 | 0.061 |
| 005 | 6 dense celltype motifs | 0.4101 | 0.580 | 0.614 | 0.036 |
| 006 | natural hg38 | 0.3975 | 0.541 | 0.552 | **0.099** |
| 007 | 25k rand + 25k nat | 0.3967 | 0.544 | 0.558 | 0.089 |
| 008 | Markov-1 natural | 0.4094 | 0.571 | 0.595 | 0.062 |
| 009 | random+3 neural | 0.4186 | 0.587 | 0.620 | 0.049 |
| 010 | ENCODE cCREs | 0.3898 | 0.543 | 0.559 | 0.068 |
| 011 | random seed=42 | **0.4235** | 0.592 | 0.623 | 0.055 |

**Noise floor**: Random with seed=0 vs seed=42 differ by +0.0032 on
eval_01. So anything within ±0.005 of random baseline is noise.
Exp 002's "improvement" (+0.003) was within noise.

**Theory v3 (current)**:
The metric (mean_r) is a correlation between predicted activity and a
reference distribution across 50k sequences. The reference appears
matched to RANDOM sequences. Any departure (high/low GC, motifs,
natural DNA, even real ENCODE cCREs) reduces match → lower correlation.

This is essentially "the model expects random-like inputs and disagrees
with itself on structured inputs". The only way to beat random is to
match its statistical properties even more exactly OR to find a
specific perturbation the model rewards.

**Cell-type trade-off**:
- K562/HepG2 peak at random (~0.58, 0.62) — they LOVE 50% GC
- SKNSH peaks at natural DNA (~0.10) — natural higher-order structure
- These are anticorrelated: can't get both simultaneously

The mean_r is dominated by the high-r cell types (K562/HepG2), so
random wins on aggregate.

## 2026-06-03 18:52 — Planning Exp 012

Try mononucleotide-shuffled natural sequences. Each natural sequence is
permuted in place. Preserves per-seq GC content (which varies in natural
DNA from ~30 to 70%) but destroys all motifs. Tests whether natural's
SKNSH boost is (a) per-sequence-GC variance or (b) actual motif content.

## 2026-06-03 19:30 — Catching up on Exp 012-019, chimera dose-response

After running Exp 012 (shuffled natural → 0.3632, both lower than random
and lower than natural; mono-shuffling natural BREAKS SKNSH-friendly
features AND keeps a non-50% GC), I tested several variants:

| # | Lib | eval_01 | Notes |
|---|-----|---------|-------|
| 012 | shuffled natural | 0.3632 | worst — destroys both |
| 013 | balanced 50:50:50:50 | 0.3242 | strict balance HURTS, kills variance |
| 014 | natural GC∈[0.45,0.55] | 0.3987 | natural+GC filter ≈ unfiltered natural |
| 015 | chimera 170 rand + 30 nat | 0.4197 | mild improvement over random=0.4203 |
| 016 | chimera 140 rand + 60 nat | 0.4059 | too much natural |
| 017 | chimera 190 rand + 10 nat | **0.4248** | **NEW BEST** |
| 018 | chimera 180 rand + 20 nat | 0.4216 | between 10 and 30 |
| 019 | chimera 195 rand + 5 nat | 0.4136 | too small, hurts |

**Theory v4**: Small natural inserts in a random scaffold give SKNSH a
tiny boost (+0.01 on its r) while leaving K562/HepG2 essentially
unaffected. There's a "sweet spot" around 10bp: large enough to encode
SKNSH-relevant features (homeobox/bHLH motifs) but small enough to
preserve the random scaffold that K562/HepG2 like.

- 0bp insert (pure random seed=42): 0.4235
- 5bp insert: 0.4136 (worse — adds variability without info)
- 10bp insert: 0.4248 (NEW BEST, +0.013 vs random)
- 20bp insert: 0.4216
- 30bp insert: 0.4197
- 60bp insert: 0.4059

The 5bp result is interesting: smaller is NOT better. There must be a
minimum information content for natural inserts to confer SKNSH benefit
that outweighs the random-scaffold perturbation.

## 2026-06-03 19:32 — Planning Exp 020 (multi-insert)

Try 2× 10bp natural inserts at random non-overlapping positions in a
200bp random scaffold. If the benefit is additive (each 10bp insert
contributes +0.013 to SKNSH r), I should see ~0.025 above random.
If the benefit saturates immediately, I'll see ~0.4248 (= same as 1×).
If the perturbation cost compounds faster than the SKNSH gain, lower.

This is critical: tells me whether to push toward more/smaller inserts
or hold at 1× 10bp.

## 2026-06-03 19:55 — Major theory update v5: Exp 017 was seed noise

After Exp 020 (2× 10bp insert → 0.4129), Exp 021 (10bp fixed center →
0.4186), and crucially **Exp 022 (10bp insert seed=42 → 0.4202)**:

The chimera 10bp "win" in Exp 017 (0.4248) was lucky seed noise.

| condition | seed 0 | seed 17 | seed 42 |
|-----------|--------|---------|---------|
| pure random | 0.4203 | — | 0.4235 |
| chimera 10bp | — | 0.4248 | 0.4202 |

Chimera mean (seed 17,42) = 0.4225. Random mean (seed 0,42) = 0.4219.
Delta = +0.0006, well within ±0.003 noise floor.

**Theory v5**: The metric is essentially saturated for random ~50% GC
libraries. The 14 evals correlate predicted activity with a reference
that *itself* was constructed from random-like 200bp sequences. Any
structured perturbation either:
  - leaves K562/HepG2 untouched but adds SKNSH variance ~0
  - or breaks K562/HepG2 fit (large negative effect)

The variance across seeds at random baseline (±0.003) defines a
hard floor on detectable improvements.

**Strategy pivot**: Stop trying to add natural structure. Instead:
- Sweep multiple seeds to characterize noise distribution
- Try MICRO-perturbations to random: per-base probability shifts
  (e.g., 26/24/24/26 vs 25/25/25/25)
- Try dinucleotide-corrected random
- Try forcing UNIFORM per-base counts (not per-seq but pool-wide)
- Try LARGER N (if more samples per library matter)

If nothing beats 0.4235 by >0.003, accept random as the answer and
report the noise distribution.

## 2026-06-03 19:58 — Planning Exp 023

Run random seed=99 to add a third data point on the noise distribution.
This costs only 1 experiment and gives me a tighter estimate of the
ceiling. If 0.420±0.003 is the true ceiling, I should redirect my
remaining experiments to micro-perturbation sweeps.

## 2026-06-03 20:35 — FINAL SUMMARY (30 experiments complete)

**Best library found**: `libraries/026_random_seed2024/`
**Best eval_01 mean_r**: 0.4278
**Method**: pure uniform random 200bp sequences (25% each base), seed=2024.

### Complete ranking (top 10)
| Rank | Lib | eval_01 | Description |
|------|-----|---------|-------------|
| 1 | 026 | 0.4278 | random seed=2024 |
| 2 | 025 | 0.4277 | random seed=314 |
| 3 | 027 | 0.4273 | random p_A=p_T=0.27 (AT bias) seed=314 |
| 4 | 029 | 0.4268 | random seed=65537 |
| 5 | 023 | 0.4251 | random seed=99 |
| 6 | 017 | 0.4248 | chimera 190 rand + 10 nat seed=17 |
| 7 | 030 | 0.4241 | random seed=42424242 |
| 8 | 011 | 0.4235 | random seed=42 |
| 9 | 024 | 0.4234 | random seed=7 |
| 10 | 002 | 0.4232 | random + 3 broad motifs |

### What was tried
- **Random baselines** (8 seeds): 0.4203 – 0.4278, mean 0.4250, std 0.0024
- **TF motifs**: 3 canonical (002 = 0.4232), 6 cell-type-dense (005 = 0.4101)
- **Composition**: GC=30% (004=0.3692), GC=70% (003=0.3567), GC=46% (027=0.4273), GC=54% (028=0.4213)
- **Natural DNA**: full natural (006=0.3975), GC-filtered (014=0.3987), cCREs (010=0.3898)
- **Markov-1 natural**: 008=0.4094
- **Mixtures**: 25k+25k (007=0.3967), shuffled natural (012=0.3632)
- **Forced balance**: 50:50:50:50 per seq (013=0.3242 — worst)
- **Neural motifs**: random+3 homeobox/bHLH (009=0.4186)
- **Chimeras** (random + natural insert): 5bp (019=0.4136), 10bp (017=0.4248 lucky seed; 022=0.4202 seed=42), 20bp (018=0.4216), 30bp (015=0.4197), 60bp (016=0.4059), 2×10bp (020=0.4129), 10bp center fixed (021=0.4186)

### Theory v6 (final)
The black-box scorer's 14 evals correlate predicted activity with a
reference distribution computed on 50k 200bp sequences. The aggregate
mean_r is dominated by the K562 and HepG2 cell-type heads, which both
prefer ~50% GC i.i.d. random sequences. The SK-N-SH head likes natural
DNA structure but contributes ~3× less in r-magnitude (~0.05-0.10 vs
~0.59 / 0.62), so SKNSH-favorable libraries pay too much in K562/HepG2
to net positive.

Random baseline saturates around 0.425 ± 0.003. The seed lottery sets
the achievable max. No structured perturbation tested broke this
ceiling, and the dynamic range of "structured" perturbations is
overwhelmingly negative: GC bias, motif density, natural content, and
forced composition all reduce mean_r more than seed-variance can rescue.

### What I would try with more budget
1. **Massive seed sweep** (50-100 seeds) to find rare seeds in the top
   tail (might reach ~0.43)
2. **Per-sequence GC variance probe**: keep mean GC at 0.50 but vary
   per-seq GC widely (random uniform [0.40, 0.60]). The SKNSH head's
   preference for natural may be GC-variance-driven.
3. **Conditional dinucleotide tuning**: keep mononucleotide at uniform
   but slightly bias dinucleotides like TpA↑ or CpG↓ to match natural.
4. **Ensemble pick**: generate 5x oversampled, then score & subset to
   the top 50k — but this requires running prepare.py on each block,
   so it costs experiment budget.

### Submitted library
`libraries/026_random_seed2024/sequences_0.txt` (50,000 sequences,
200bp each, uniform random with numpy seed=2024). mean_r=0.4278.
