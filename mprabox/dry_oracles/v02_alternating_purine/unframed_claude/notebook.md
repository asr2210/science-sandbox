# Lab Notebook — Sequence Optimization

## 2026-06-03 — Initial setup and theory

**Task**: Generate 50,000 200bp DNA sequences that maximize correlations
returned by black-box `prepare.py`. Primary metric: `eval_01.mean_r`.
30 experiments total.

**Initial theory**:
- The score is Pearson/Spearman correlation (r-value, -1 to 1).
- 14 eval sets exist but many pair up to identical scores — likely
  ~7-9 unique oracles. K562 and HepG2 give IDENTICAL scores on random,
  so they share one oracle.
- "mean_r" = mean of (k562_r, hepg2_r, sknsh_r).
- Most plausible mechanism: prepare.py uses my sequences to train a
  model that is then evaluated against held-out MPRA test sequences.
  Higher diversity / better-spanning library → higher held-out r.
  Alternative: my library is correlated to something fixed; unlikely
  given the 50k size and "library" framing.
- Could also be: oracle scores my sequences with predicted activity,
  and correlation is with a sequence-level feature that they extract.

**Random baseline (exp 001) result**:
- eval_01.mean_r = 0.1307
- eval_01.k562_r = 0.008, hepg2_r = 0.008, sknsh_r = 0.3761
- SKNSH ~ 0.37 from random — much higher than 0 — so SKNSH oracle
  responds well to nucleotide composition / k-mer distribution of
  random sequences.
- K562/HepG2 essentially zero on random — they need specific features.

**What to test next**:
- Experiment 002: Real human regulatory sequences (use a known
  enhancer / promoter pool from public data) — see if real biological
  sequences outperform random.
- Experiment 003: All-A or low-complexity baseline to bracket the floor.
- Experiment 004: Sequences with tandem TF motif insertions for
  K562/HepG2 relevant TFs (GATA1, MYC, HNF4A).

## 2026-06-03 — Experiment 001 result
- Library: 50k uniformly random 200bp.
- eval_01.mean_r = 0.1307 (k562=0.008, hepg2=0.008, sknsh=0.376)
- Time: 41.2s
- Update theory: SKNSH responds to neutral content, K562/HepG2 need
  motifs. Aim next: pull real human regulatory sequences.

## 2026-06-03 — Experiments 002-005 update

**002 GC60**: eval_01.mean=0.0995 — worse than random.
**003 GC40**: eval_01.mean=0.1287 — same as random.
  → Composition bias alone is not the lever.
**004 TF motif mix**: eval_01.mean=0.1112 — slightly worse than random.
  → Random motif insertion doesn't help. Maybe motifs need to be
    in proper context, or the model has its own oracle that doesn't
    care about these specific consensus motifs.
**005 Malinois random 50k**: eval_01.mean=**0.1524** — best so far!
  → SKNSH boosted to 0.46 (from 0.38 random).
  → K562 and HepG2 STILL IDENTICAL TO 4 DECIMALS across all runs.
    Confirmed they are reported as same value (likely same oracle).
  → mean_r = (2*k562_oracle + sknsh)/3. Even on real bio, k562
    component drifts -0.06 to +0.05 across evals — noise-like.
  → Real biological sequences modestly help SKNSH; K562/HepG2 oracle
    seems insensitive to library composition.

**Theory v2**: prepare.py has 2 effective oracles per eval:
  (1) K562/HepG2 oracle — output near-flat regardless of input,
      correlation hovers around 0 with high variance across evals.
  (2) SKNSH oracle — sensitive to sequence content; biological
      sequences give r=0.45–0.51.

The mean_r is dominated by SKNSH ÷ 3 because K562/HepG2 contribute zero.
So pushing SKNSH up is the most reliable lever.

**Next**: Exp 006 — max-variance SKNSH library (top + bottom of Malinois
SKNSH log2FC). Hypothesis: extreme activity range gives highest
correlation with SKNSH oracle.

## 2026-06-03 — Experiments 006-016 results

| exp | strategy | eval_01 | K562 | SKNSH |
|-----|----------|---------|------|-------|
| 005 | Malinois random 50k | 0.152 | 0.00 | 0.46 |
| 006 | SKNSH extremes | 0.161 | 0.01 | 0.46 |
| 007 | per-cell extremes (triextreme) | 0.171 | 0.03 | 0.45 |
| 008 | top |abs-max| | 0.155 | 0.02 | 0.42 |
| 009 | K562 extremes only | 0.170 | 0.03 | 0.44 |
| 010 | z-score (|lfc|/se) extremes | 0.162 | 0.02 | 0.45 |
| 011 | HepG2 extremes only | 0.170 | 0.03 | 0.45 |
| 012 | CRE-biased + per-cell extremes | 0.171 | 0.03 | 0.45 |
| 013 | K562 stratified (10 bins) | 0.174 | 0.03 | 0.46 |
| 014 | TRI-STRATIFIED 5×5×5 in (K,H,S) | **0.186** | 0.05 | 0.46 |
| 015 | SKNSH stratified (10 bins) | 0.168 | 0.02 | 0.46 |
| 016 | per-cell strat union (10 bins×3 cells) | 0.179 | 0.04 | 0.47 |

**Theory v3**:
- The scoring rewards a library whose joint (K562, HepG2, SKNSH) activity
  distribution is well-spread. Bimodal extremes → ~0.17. Uniform joint
  coverage (3D stratification) → ~0.19.
- K562 and HepG2 oracles give identical scores — same oracle, reported twice.
- SKNSH is saturating around 0.46–0.51 on Malinois data; hard to push higher.
- K562 oracle responds to balanced libraries (got +0.05 in 014 vs +0.00 in 005).

**Next ideas**:
- Exp 017: finer 6×6×6 grid (216 cells)
- Exp 018: coarser 4×4×4 grid (64 cells)
- Exp 019: tri-stratified + CRE bias
- Exp 020: tri-stratified + intra-cell |lfc| ranking (pick most-extreme within each cube cell)

## 2026-06-03 — Final summary (30 experiments complete)

### Top 5 by eval_01.mean_r
1. **018_tri_strat_4x4x4** — 0.1909 (winner)
2. 027_4x4x4_seed_blend — 0.1906
3. 028_tri_strat_5x5_2D_KH — 0.1896
4. 026_4x4x4_residuals — 0.1888
5. 022_4x4x4_seed100 — 0.1870

### Key findings (final theory)

**Mechanism**: prepare.py very likely trains a small CNN on (my_sequences,
oracle_activity) pairs and evaluates Pearson r against held-out test
labels. The oracle is itself trained on the Malinois (Gosai et al 2024)
MPRA dataset, since real Malinois sequences (0.15) far outperform
synthetic ones (0.11-0.13).

**Key insights**:
- **K562 and HepG2 oracles give numerically identical scores** to 4
  decimals every run. They are the same oracle reported twice. So
  mean_r = (2*K562 + SKNSH) / 3. Trying to "lift K562" and "lift HepG2"
  separately is impossible.
- **SKNSH oracle is sensitive to composition** — gives r ~ 0.38 on
  uniformly random sequences, ~0.46 on real Malinois sequences. Caps
  around 0.5 on Malinois data.
- **K562/HepG2 oracle needs balanced joint coverage** — flat (~0.00)
  on random, 0.03 on single-cell extremes, ~0.05 on 3D-stratified
  Malinois sequences. Best obtainable was ~0.06 on the winning library.
- **Joint coverage > extremes > random**. The trained downstream
  CNN needs to see sequences spanning all combinations of (K562,
  HepG2, SKNSH) activity, not just the high-activity tails.
- **4×4×4 stratification is the sweet spot**. 64 cells × ~782 seqs.
  Finer (5×5×5, 6×6×6) and coarser (2×2×2, 3×3×3) both lose.
  Hypothesis: 64 cells gives enough resolution for activity gradient
  while keeping per-cell sample size large enough for the oracle to
  see within-bin variation.

### What did NOT help
- GC bias either direction (002, 003 ≤ random)
- Random TF motif insertion (004) — actually slightly worse
- Single-cell focused extremes (006, 009, 011) — capped at ~0.17
- Top-by-|absmax| (008) — over-weights SKNSH extremes
- Z-score-filtered "clean" sequences (010, 019, 029) — too narrow
- Adding CRE class bias (012, 020) — slightly worse
- Marginal uniform via importance weighting (024) — slightly worse
- Within-bucket selection by max-z (019) — worse than random
- PCA decorrelation (026) — neutral
- Seed-union restratification (030) — neutral / slightly worse

### What WORKED
- Switching from synthetic to real Malinois MPRA: +0.02 over random
- Per-cell extremes (007): +0.02 over Malinois random
- 1D K562 quantile stratification (013): +0.02 over per-cell extremes
- 3D joint quantile stratification (014): +0.01 over 1D
- Coarser 3D grid 4×4×4 (018): +0.005 over 5×5×5
- Best score: **0.1909**, an absolute lift of **+0.060** over random
  baseline (0.131).

### Variance across runs
- Same strategy with different seeds: ±0.005
- The ~0.19 plateau is real; we are at the noise floor of useful gains
  from sampling strategy alone. Further improvement likely needs a
  trained oracle to score and select candidates (e.g., train Malinois
  CNN on the data, predict, choose by predicted variance).

### Operational notes
- prepare.py runs in ~30-45s per 50k-seq library
- Total 30 experiments completed in <1h wall time
- Initial git lock issues were a parallel-agent conflict; resolved
  by waiting and using direct file paths in `git add`.
