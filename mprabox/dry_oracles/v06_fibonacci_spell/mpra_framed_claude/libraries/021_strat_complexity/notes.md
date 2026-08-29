# 021 — Complexity (distinct-trimer) stratified chr22

## What I tested
50k chr22 windows stratified into 5 quantile bins by DISTINCT TRIMER
count per 200bp window (a Shannon-entropy proxy). 10k per bin.
Random orientation. Seed=42.

## Bin distribution observed
- Bin 0: trimers 5-52 (low-complexity tail), mean GC 0.459
- Bin 1: trimers 52-54, mean GC 0.457
- Bin 2: trimers 54-56, mean GC 0.465
- Bin 3: trimers 56-58, mean GC 0.476
- Bin 4: trimers 58-64 (high-complexity), mean GC 0.493

Bin 0 is a wide tail (lots of low-complexity windows lumped together).
Bins 1-4 span a narrow range. Mean GC across bins varies only 0.46-0.49.

## Result — ties 012 on eval_01
- eval_01 = 0.1367 (012: 0.1367, tied)
- mean of evals = 0.1294 (012: 0.1308, -0.001)
- K562: 0.038 (012: 0.038)
- HepG2: 0.174 (012: 0.174)

No improvement. Complexity stratification is essentially equivalent to
GC stratification on chr22 (because GC and complexity are correlated:
low-complexity regions are AT-rich repeats).

## Theory update
Complexity is NOT a useful new axis on chr22. It's mostly a re-
expression of GC + repeat-region content. Other stratification axes
are needed to extract more gain.

## What to try next
022: Stride=10 dense sampling with 10-bin GC strat. Each bin draws
5k from a 4x larger pool (after position-dedup at 50bp), giving the
selection process more diversity to choose from.

Hypothesis: the 013 plateau (0.1375) may reflect limited choice in
each bin — only 78k candidates per bin from stride=50. Stride=10
gives 312k → more diverse 5k.
