# Experiment 021 — 50k pure dense motifs (35-50/seq), no cCRE

## What I tested
50k pure motif scaffolds at 35-50 inserts/seq. No real biology.
Tests: (a) where 018's eval_07 record came from (motifs alone or
pELS contribution); (b) whether pure motifs can hit broad mean.

## Result — broad lift, two big losses
- eval_01/02/05/14: 0.0034 (record for these — "broad baseline" evals)
- eval_03/12: 0.0030 (record)
- eval_06/11: 0.0031 (record)
- eval_13: mean=0.0031, HepG2=0.0126 (new HepG2 record on eval_13)
- eval_07: **-0.0012** (lost 018's 0.0109 — confirms pELS contributed)
- eval_08: **-0.0012** (lost 012's 0.0117)
- eval_10: 0.0011 (lost 013's 0.0085)
- Mean across 14 ≈ 0.0022 (vs 012's 0.0029)

## What this tells me
**Pure dense motifs lifts a huge swath of evals (8/14) but loses the
3 most "specific" evals (07, 08, 10).** The pELS in 018 was directly
contributing to eval_07's 0.0109 — losing pELS, eval_07 vanishes.

**Key insight about the eval set:** several evals (01/02/05/14;
03/12; 06/11) appear to be CORRELATED or duplicated. Pure motifs
hits all of them at 0.0034. This is the "broad baseline" — most evals
just need representative TF content.

The 3 "specific" evals (07, 08, 10) each need a different non-motif
ingredient: pELS+low-density for 08, pELS+high-density for 07,
dELS+low-density for 10.

## Updates to theory
**v3.12 → v3.13:** The 14 evals decompose into:
- ~8 "broad" evals → respond to general TF motif content
- ~3-4 "specific" evals → respond to specific motif×cCRE pairings
- 1-2 hardest evals → no recipe lifts them broadly (eval_04/09)

Mean is maximized by hitting all broad evals AND one specific eval.
012's recipe (low-density + pELS) hits broad + eval_07 + eval_08.
That's why 012 is the leader.

## Next
Try the *inverse* of pure motifs: take REAL pELS sequences and
INSERT motifs into them. Tests whether real backbone context
(vs random ACGT backbone) gives the model better feature learning.
"Motif-enhanced real pELS" is a novel sequence design.
