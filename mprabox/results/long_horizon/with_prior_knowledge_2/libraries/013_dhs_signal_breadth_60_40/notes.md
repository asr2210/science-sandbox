# 013_dhs_signal_breadth_60_40

## What I tested
Bracket the 70/30 winner (011) from the breadth-leaning side: 30K
mean_signal-weighted + 20K numsamples-weighted. Together with 012
(80/20), this was supposed to determine whether 70/30 is a peak or
a plateau. Decision rules were committed in advance.

## Result — collapse on the breadth side too
| metric   | 013    | 011 (70/30) | 003 (50/50) | 012 (80/20) | Δ vs 011 |
|----------|--------|-------------|-------------|-------------|----------|
| eval_01  | 0.7119 | 0.7383      | 0.7327      | 0.7055      | -0.026   |
| eval_07  | 0.7334 | 0.7751      | 0.7618      | 0.7309      | -0.042   |
| eval_08  | 0.6636 | 0.7041      | 0.6984      | 0.6523      | -0.041   |
| eval_13  | 0.7160 | 0.7644      | 0.7469      | 0.7229      | -0.048   |
| cross-14 | 0.7501 | 0.7811      | 0.7735      | 0.7433      | -0.031   |

Per-seed eval_01: 0.7215 / 0.7328 / 0.6815 (std ≈ 0.027 — wide,
matching 012's instability rather than 011's tight 0.002).

Trajectory now: 50/50 → 60/40 → 70/30 → 80/20 = 0.7735 → 0.7501 →
0.7811 → 0.7433. Highly non-monotone — and 60/40 is *worse* than
50/50 despite being closer to the 70/30 peak.

## Why it collapsed
The naive theory from 012 ("each axis must clear a stability floor")
doesn't fully explain 013 — at 20K breadth + 30K signal, both axes
should be well above any threshold (012 had 10K breadth and was
unstable; 003 had 25K breadth and was tight). Yet 013 has 012-level
variance.

A better explanation: **011's 70/30 ratio sits in a narrow stable
basin, and any deviation — in either direction — destabilizes the
optimization**. The seed-2 outlier (0.6815) is a model that landed
in a much worse local optimum. With a different seed selection 013
might come in higher; with adversarial seeds 011 might come in lower.

A 3-seed test cannot reliably resolve which ratio is "best" once
two configurations both land in the high-variance regime.

## Theory update
The relevant story is bimodal:
1. **70/30 is uniquely stable** within the ratio sweep (per-seed std
   0.002 vs 0.022-0.027 for neighbors). This is the strongest
   single signal across the entire experiment series — much
   tighter than the model-noise floor (~0.005 from training-seed
   variance alone).
2. **Off-peak ratios are high-variance**, which means single 3-seed
   evaluations can't distinguish them well. Any further ratio
   experiment would burn budget on noise.

The implication is *not* "70/30 is a knife-edge optimum we should
explore at higher resolution" — it's "the ratio sweep has yielded
its information; further sweeps will not pay back". Pivot.

## Decision (executing committed rule)
013 < 011 by > 0.003 cross-14 → **70/30 confirmed as peak. Lock the
ratio. Pivot to NEW LEVERS for 014+.**

## Next
014: introduce a TRULY orthogonal data axis. Candidates ranked by
information-orthogonality to mean_signal+numsamples:
- TF ChIP-seq density per DHS (independent assay, motif-grounded)
- DHS-specific sequence content scores (e.g., GC%, CpG, simple
  k-mer entropy) — sequence-derived, fully orthogonal to assay
- Cross-species DHS conservation (different signal type than phyloP)

phyloP failed as a positive weight (007). cCRE class (008) and cCRE
maxZ (010) are correlated DHS-derived metrics. The next axis must
be from a different *measurement modality* or from the *sequence
itself*, not another DNase derivative.
