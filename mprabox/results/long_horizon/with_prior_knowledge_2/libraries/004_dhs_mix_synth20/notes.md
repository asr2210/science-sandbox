# 004_dhs_mix_synth20

## What I tested
40% mean_signal-weighted DHS + 40% numsamples-weighted DHS + **20%
i.i.d. uniform random {A,C,G,T} sequences**. Hypothesis: adding a small
dose of synthetic OOD coverage on top of the winning 003 recipe would
fix the eval_08 deficit while keeping in-distribution gains.

## Result — surprising negative
| metric | 004    | 003 (best) | Δ      |
|--------|--------|------------|--------|
| eval_01 | 0.6977 | 0.7327 | **-0.035** |
| eval_07 | 0.7054 | 0.7618 | **-0.056** |
| eval_08 | 0.6775 | 0.6984 | -0.021 *(even eval_08 got worse)* |
| eval_13 | 0.6887 | 0.7469 | -0.058 |
| cross-14 | 0.7360 | 0.7735 | **-0.038** |

Per-seed eval_01: 0.6831 / 0.6923 / 0.7178 — wider spread than 003 too.

**Adding random synthetic hurt every single eval, including eval_08
which I expected to benefit.**

## What this updates
The published `synth_oracle` (eval_08=0.7696) and `dhs_synth`
(eval_08=0.7523) baselines clearly help eval_08 with synthetic — but
strategies.md notes `synth_oracle` is "oracle-labeled" and the contrast
with `mpra_real` (real labels, much worse: eval_01=0.6026) tells the
same story: **real MPRA measurements on random sequences are noisy and
hurt training when included as 20% of the data.**

In MY pipeline (no oracle access — sequences get real MPRA measurements),
the value of synthetic is the OPPOSITE of what the published baselines
show. I cannot oracle-label, so synthetic = noisy training data.

### Lever I had assumed was useful → discarded
"Add random sequences for OOD coverage" doesn't work in my pipeline.
The third axis (OOD coverage) requires either oracle labels or genome-
derived sequences with low intrinsic noise — not pure random.

## Implications for next experiment
- Stop trying to add purely-random sequences.
- The lever for eval_08 must be something else: maybe k-mer diversity
  *within real DHS*, or augmentation that preserves regulatory structure
  but extends coverage (motif-shuffled, dinucleotide-shuffled, etc.) —
  but those all share the noisy-label problem.
- Best path forward: stay on the genome, find more orthogonal real-DNA
  axes within DHS / cCRE space.
