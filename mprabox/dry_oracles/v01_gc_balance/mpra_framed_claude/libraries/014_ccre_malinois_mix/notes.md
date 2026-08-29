# 014_ccre_malinois_mix

## Setup
25k stratified cCREs (halved exp 002 quotas) + 25k random Malinois
oligos = 50k mixed library.

## Result
- eval_01 = 0.6922 vs cCRE-only 0.6921 (**tied**)
- eval_04 = 0.5993 vs 0.5977 (+0.002, in noise)
- eval_07 = 0.7559 vs 0.7562 (tied)
- eval_10 = 0.6655 vs 0.6673 (~tied)

## Interpretation
Combining two large, near-equivalent-quality data sources gives no
visible lift on eval_01. The marginal gain from each source's
*complementary* information appears to be ~0 — they cover the same
regulatory grammar from the model's perspective.

This is the 6th library at ~0.69 (002, 005, 006, 010, 011, 014). The
ceiling is now extremely well-established. The model trained for 30s
saturates at this level for any reasonable mix of biological
regulatory sequences.

## Theory update → T6
The ~0.69 ceiling is not about the *source* of training sequences but
about either:
1. Model capacity / training budget — 30s isn't enough to use additional
   diversity
2. Eval intrinsic noise — eval_01 has a real correlation ceiling
3. Some orthogonal signal that none of cCRE / DHS / Malinois exposes

Going to test (3) next: try ChIP-seq peaks (direct TF binding evidence)
and ABC enhancer predictions (different annotation principle). If
those also hit 0.69, then (1) or (2) is the binding constraint and
library tweaks can't move the needle.
