# 025_pels_mut0p5pct — notes

## Design
50K pELS, 0.5% mutation rate (~1 sub per 200bp). Same as 023
except for noise rate. Intended to test the lower bracket of
the proposed 1% sweet spot.

## Result vs. mutation dose-response

| eval | clean012 | mut0.5%025 | mut1%023 | mut3%024 |
|------|----------|------------|----------|----------|
| 01   | 0.7203   | 0.7073     | 0.7230   | 0.6902   |
| 02   | 0.8129   | 0.7997     | 0.8144   | 0.7821   |
| 03   | 0.7958   | 0.7833     | 0.7981   | 0.7634   |
| 04   | 0.7603   | 0.7497     | 0.7659   | 0.7347   |
| 05   | 0.7203   | 0.7074     | 0.7230   | 0.6901   |
| 06   | 0.8133   | 0.8002     | 0.8147   | 0.7826   |
| 07   | 0.7489   | 0.7337     | 0.7503   | 0.7081   |
| 08   | 0.6844   | 0.6723     | 0.6916   | 0.6611   |
| 09   | 0.8238   | 0.8124     | 0.8303   | 0.7950   |
| 10   | 0.7729   | 0.7572     | 0.7765   | 0.7412   |
| 11   | 0.7083   | 0.6958     | 0.7108   | 0.6786   |
| 12   | 0.6853   | 0.6735     | 0.6877   | 0.6549   |
| 13   | 0.7473   | 0.7334     | 0.7511   | 0.7079   |
| 14   | 0.8129   | 0.7998     | 0.8144   | 0.7821   |

Mean: clean **0.758**, 0.5% **0.745**, 1% **0.761**, 3% **0.727**.

## Interpretation — sweet spot probably noise

The dose-response is NOT smooth. 0.5% sits BELOW clean by
-0.013 on every single eval, while 1% sits ABOVE clean by
+0.003 on every eval. A well-behaved monotonic regularization
would put 0.5% between clean and 1%, not below clean.

**Most parsimonious explanation:** the +0.003 win at 1% was
within seed noise. With seed-to-seed variance for these
experiments easily 0.005-0.02 on individual evals, a +0.003
mean shift is not robust evidence for a real effect. The
broader trend is that mutation noise is neutral-to-harmful
across the board.

**Per-seed eval_01 spread for 025:**
- seed 0: 0.6993
- seed 1: 0.6846
- seed 2: 0.7380 (outlier)
- range: 0.054, std ~0.027

That spread alone exceeds the entire 023-vs-012 gap. We have
been chasing measurement noise.

**Alternative hypothesis (unlikely but possible):** there is a
genuine non-monotonic phenomenon where 1 substitution is
"weird" (creates a single isolated lesion that the model
overfits to) but 2 substitutions disperse the perturbation
across the sequence. This would imply a gain only at exactly
2 subs/200bp. This is a far less parsimonious story than
"noise" and we would need many more seeds to support it.

## Theory update

**Mutation noise as augmentation: rejected.** Adding to the
augmentation playbook null findings:

| augmentation                           | mean_r | Δ vs pELS |
|----------------------------------------|--------|-----------|
| pELS clean (012)                       | 0.758  |   0       |
| pELS + 0.5% mut (025)                  | 0.745  | -0.013    |
| pELS + 1% mut (023)                    | 0.761  | +0.003 (noise) |
| pELS + 3% mut (024)                    | 0.727  | -0.031    |
| pELS + RC (016)                        | 0.741  | -0.017    |
| pELS + offset (017)                    | 0.741  | -0.017    |
| pELS longest (021)                     | 0.751  | -0.007    |
| pELS shortest (022)                    | 0.739  | -0.019    |

**Every per-element transformation we have tried fails.** The
clean pELS-only library at 0.758 is the augmentation ceiling.

This is itself a strong finding: **there is no easy
augmentation win for this generalization problem.** The model
learns from sequence content, and any modification — even
gentle ones — degrades that signal.

## Implication for next 5 experiments

We have exhausted the augmentation axis. Five experiments
remain. Pivot to:
- **Class combinations** — top performers (pELS, pELS-long,
  CA-H3K4me3) combined; could a multi-class library exceed
  any single class?
- **GC content stratification** — does enriching for matched
  GC vs eval sets help?
- **Functional partitioning** — top quartile by some functional
  signal (e.g., conservation, accessibility score) vs
  bottom quartile.

## Next experiment

**Exp 026: pELS + CA-H3K4me3 combo.** 25K pELS + 25K
CA-H3K4me3 shuffled. Top two single-class performers (012
mean=0.758, 019 mean=0.749). If the union exceeds 0.758, we
have evidence that diversification along the
annotation-evidence axis helps. If it falls between or below,
single-class is hard to beat by simple union.
