# Baseline observations (from exps 001 & 002)

## What `prepare.py` rewards
- A 50K library of pure uniform random 200bp gives eval_01 = **0.4192** (K562 0.59, HepG2 0.62, SK-N-SH 0.045).
- Planting 3-5 short canonical TF consensus motifs per random 200bp **does NOT help** (eval_01 dropped 0.007). Most likely because (a) short motifs already occur often by chance, (b) the model is learning compositional features, not motif identity, and planting disrupts those features.

## Asymmetric cell-type behavior
- **K562/HepG2** are easy: ~0.6 r is achievable from pure random sequences. The MPRA activity in these cell types has strong compositional predictors.
- **SK-N-SH** is hard: r ≈ 0.045 from both random and motif-planted libraries. SK-N-SH activity in synthetic 200bp libraries appears not learnable from compositional or short-motif features. Almost certainly needs genomic context (real CRE sequences).

## Eval-set landscape
- Most of eval_01..14 cluster tightly with K562/HepG2/SK-N-SH split ≈ 0.59/0.62/0.04.
- eval_08 is the LOWEST outlier (mean_r ≈ 0.385 in 001, 0.375 in 002) — possibly a stricter or distinct held-out distribution.
- eval_04, 07, 09, 10, 13 are slightly higher than the others (~0.42-0.43 vs ~0.42).

## What doesn't work
- **Short consensus motif planting** in random backgrounds — small or negative effect.

## What to try next
- **Mixtures of random + real CREs** — exp 003 showed these two are complementary.
- **PWM-sampled motif instances** instead of single consensus (more diversity per motif).
- **Synthetic sequences with biologically plausible co-occurring motifs** + flanking context.

## Update from exp 003 (ENCODE V4 cCREs)
- Real cCREs **dropped K562/HepG2** (0.59→0.55, 0.62→0.56) but **lifted SK-N-SH** (0.045→0.079).
- Net: eval_01 dropped to 0.394.
- Reading: composition diversity (random) and biological grammar (CREs) drive different cell-type generalization. They should be combined.

## Things to know
- A single run is ~2 minutes wall-clock. Budget accordingly across 30 experiments.
- The `mean_r` reported per eval is the mean of `k562_r, hepg2_r, sknsh_r`. So lifting SK-N-SH from 0.04 → 0.4 alone would lift mean_r ~+0.12.
